# /// script
# requires-python = ">=3.11"
# dependencies = ["fal-client>=0.5", "google-genai>=2.3", "replicate>=1.0", "pillow>=10", "pillow-heif>=0.18"]
# ///
"""PROTÓTIPO. Gera Character Sheets (e stills de casal) com 3 modelos para comparar o House Style.

Uso (dentro de prototypes/house-style/, com .env preenchido):

  uv run generate.py --phase direction                 # fase 0: 3 direções, só Nano Banana 2.1
  uv run generate.py --phase model --direction A       # fase A: 3 modelos na direção escolhida
  uv run generate.py --phase couple --direction A      # fase B: stills de casal nos 3 modelos
  uv run generate.py --phase pivot --direction A --model nano   # fase C: nível 3 no vencedor
  uv run generate.py --model flux --direction B --level 2 --n 1 --person ana   # chamada avulsa

Provedor padrão: fal.ai (--provider fal, decisão de 2026-11-08). --provider direct usa Gemini API
direto + Replicate, o caminho previsto para produção.

Entradas: photos/<pessoa>/*.jpg (3 fotos: frontal, 3/4, corpo inteiro). Exatamente 2 pastas.
Saídas:   out/<direção><nível>/<modelo>/<pessoa>-<k>.png e out/runs.jsonl (latência, custo, prompt).
Guarda de orçamento: recusa a rodar se gasto + estimado > --cap (padrão US$ 15).

Fotos e saídas NUNCA entram no git (o repositório é público). Ver .gitignore.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

import prompts

register_heif_opener()  # fotos HEIC do iPhone

HERE = Path(__file__).parent
PHOTOS = HERE / "photos"
OUT = HERE / "out"
RUNS = OUT / "runs.jsonl"

# Preços de tabela (USD por imagem 1K), pesquisa de 2026-11-07. n = número de imagens de entrada.
PRICE_FAL = {
    "nano": lambda n: 0.040 + 0.002 * n,
    "flux": lambda n: 0.048,
    "seedream": lambda n: 0.0675 + 0.0045 * max(n - 1, 0),
}
PRICE_DIRECT = {
    "nano": lambda n: 0.0336 + 0.004,  # saída 1120 tokens + ~2.5K tokens de entrada; recalculado pelo usage
    "nanopro": lambda n: 0.134 + 0.004,
    "flux": lambda n: 0.024,  # Replicate; tabela BFL seria 0,048
    "seedream": lambda n: 0.045,
}
GEMINI_IN_PER_TOKEN = 1.50 / 1_000_000
GEMINI_OUT_PER_TOKEN = 30.0 / 1_000_000
GEMINI_PRO_OUT_PER_TOKEN = 120.0 / 1_000_000  # 0,134 USD / 1120 tokens

FAL_ENDPOINTS = {
    "nano": "google/nano-banana-2.1/edit",
    "flux": "fal-ai/flux-3-image/edit",
    "seedream": "bytedance/seedream/v5/pro/edit",
}
DIRECT_IDS = {
    "nano": "gemini-nano-banana-2.1",
    "nanopro": "gemini-3-pro-image",
    "flux": "black-forest-labs/flux-3-image",
    "seedream": "bytedance/seedream-5-pro",
}
MODELS = ["nano", "flux", "seedream", "nanopro"]


def load_env() -> None:
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if v.strip():
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))


def people() -> list[str]:
    if not PHOTOS.exists():
        sys.exit(f"Crie {PHOTOS}/<pessoa>/ com 3 fotos por pessoa.")
    ps = sorted(p.name for p in PHOTOS.iterdir() if p.is_dir() and not p.name.startswith("_"))
    if len(ps) != 2:
        sys.exit(f"Esperava exatamente 2 pastas em {PHOTOS}, achei {ps}")
    return ps


def photo_bytes(person: str, max_side: int = 1024) -> list[tuple[bytes, str]]:
    """Fotos da pessoa redimensionadas em memória (payload menor, menos tokens)."""
    exts = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
    files = sorted(f for f in (PHOTOS / person).iterdir() if f.suffix.lower() in exts)
    if not files:
        sys.exit(f"Nenhuma foto em {PHOTOS / person}")
    out = []
    for f in files:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")  # respeita a rotação do iPhone
        im.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=85)
        out.append((buf.getvalue(), "image/jpeg"))
    return out


def spent() -> float:
    if not RUNS.exists():
        return 0.0
    return sum(json.loads(l).get("cost_usd", 0) for l in RUNS.read_text().splitlines() if l.strip())


def record(row: dict) -> None:
    OUT.mkdir(exist_ok=True)
    with RUNS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------- fal.ai ----------

_fal_url_cache: dict[bytes, str] = {}


def fal_ref_urls(refs: list[tuple[bytes, str]], upload: bool) -> list[str]:
    """Por padrão data URIs: as fotos não ficam copiadas no CDN do fal (que é público por URL).
    --upload troca para upload no CDN se o payload inline der problema."""
    import fal_client

    urls = []
    for b, m in refs:
        if upload:
            if b not in _fal_url_cache:
                _fal_url_cache[b] = fal_client.upload(b, m)
            urls.append(_fal_url_cache[b])
        else:
            urls.append(f"data:{m};base64,{base64.b64encode(b).decode()}")
    return urls


def call_fal(model_key: str, prompt: str, refs: list[tuple[bytes, str]], seed: int, upload: bool) -> tuple[bytes, dict]:
    import fal_client

    if model_key not in FAL_ENDPOINTS:
        raise RuntimeError(f"{model_key} não está mapeado no fal.ai; use --provider direct")
    urls = fal_ref_urls(refs, upload)
    if model_key == "nano":
        args = {"prompt": prompt, "image_urls": urls, "aspect_ratio": "9:16", "resolution": "1K",
                "num_images": 1, "output_format": "png", "seed": seed}
    elif model_key == "flux":
        args = {"prompt": prompt, "image_urls": urls, "aspect_ratio": "9:16", "resolution": "1k",
                "output_format": "png"}
    else:
        args = {"prompt": prompt, "image_urls": urls, "image_size": {"width": 768, "height": 1365},
                "num_images": 1, "output_format": "png", "watermark": False}
    metrics: dict = {}

    def on_update(ev):
        if isinstance(ev, fal_client.Completed):
            metrics.update(ev.metrics or {})

    result = fal_client.subscribe(FAL_ENDPOINTS[model_key], arguments=args, with_logs=True, on_queue_update=on_update)
    url = result["images"][0]["url"]
    if url.startswith("data:"):
        data = base64.b64decode(url.split(",", 1)[1])
    else:
        data = urllib.request.urlopen(url).read()
    return data, {"api": "fal", "inference_s": metrics.get("inference_time"),
                  "cost_usd": PRICE_FAL[model_key](len(refs)), "description": result.get("description")}


# ---------- direto (Gemini API + Replicate), caminho de produção ----------


def call_gemini(model_key: str, prompt: str, refs: list[tuple[bytes, str]]) -> tuple[bytes, dict]:
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = DIRECT_IDS[model_key]
    out_price = GEMINI_PRO_OUT_PER_TOKEN if model_key == "nanopro" else GEMINI_OUT_PER_TOKEN
    try:
        # Forma generate_content (verificada peça a peça; não vista oficialmente para este model id).
        resp = client.models.generate_content(
            model=model,
            contents=[prompt, *[types.Part.from_bytes(data=b, mime_type=m) for b, m in refs]],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="9:16", image_size="1K"),
            ),
        )
        img = next((p.inline_data.data for p in resp.parts if p.inline_data), None)
        if img is None:
            raise RuntimeError(f"sem imagem na resposta: {resp.text!r}")
        um = resp.usage_metadata
        in_tok = um.prompt_token_count or 0
        out_tok = sum(d.token_count for d in (um.candidates_tokens_details or []) if str(d.modality).endswith("IMAGE")) or (um.candidates_token_count or 0)
        return img, {"api": "generate_content", "in_tokens": in_tok, "out_tokens": out_tok,
                     "cost_usd": in_tok * GEMINI_IN_PER_TOKEN + out_tok * out_price}
    except Exception as e:  # noqa: BLE001
        print(f"    generate_content falhou ({type(e).__name__}: {e}); tentando interactions", file=sys.stderr)
        inter = client.interactions.create(
            model=model,
            input=[{"type": "text", "text": prompt}]
            + [{"type": "image", "data": base64.b64encode(b).decode(), "mime_type": m} for b, m in refs],
            response_format={"type": "image", "aspect_ratio": "9:16", "image_size": "1K"},
        )
        img = base64.b64decode(inter.output_image.data)
        usage = getattr(inter, "usage", None)
        in_tok = getattr(usage, "total_input_tokens", 0) or 0
        out_tok = getattr(usage, "total_output_tokens", 0) or 1120
        return img, {"api": "interactions", "in_tokens": in_tok, "out_tokens": out_tok,
                     "cost_usd": in_tok * GEMINI_IN_PER_TOKEN + out_tok * out_price}


def call_replicate(model_key: str, prompt: str, refs: list[tuple[bytes, str]]) -> tuple[bytes, dict]:
    import replicate

    files = [io.BytesIO(b) for b, _ in refs]
    for i, f in enumerate(files):
        f.name = f"ref{i}.jpg"
    if model_key == "flux":
        inp = {"prompt": prompt, "images": files, "aspect_ratio": "9:16", "resolution": "1k",
               "output_format": "png", "grounding": False}
    else:
        inp = {"prompt": prompt, "image_input": files, "aspect_ratio": "9:16", "size": "1K",
               "output_format": "png"}
    pred = replicate.predictions.create(model=DIRECT_IDS[model_key], input=inp)
    pred.wait()
    pred.reload()
    if pred.status != "succeeded":
        raise RuntimeError(f"{pred.status}: {pred.error}")
    out = pred.output
    first = out[0] if isinstance(out, list) else out
    data = first.read() if hasattr(first, "read") else urllib.request.urlopen(first).read()
    return data, {"api": "replicate", "inference_s": (pred.metrics or {}).get("predict_time"),
                  "cost_usd": PRICE_DIRECT[model_key](len(refs))}


def generate(provider: str, model_key: str, prompt: str, refs: list[tuple[bytes, str]], seed: int, upload: bool) -> tuple[bytes, dict]:
    t0 = time.time()
    if provider == "fal":
        img, meta = call_fal(model_key, prompt, refs, seed, upload)
    elif model_key in ("nano", "nanopro"):
        img, meta = call_gemini(model_key, prompt, refs)
    else:
        img, meta = call_replicate(model_key, prompt, refs)
    meta["latency_s"] = round(time.time() - t0, 1)
    return img, meta


# ---------- jobs ----------


def plan(args) -> list[dict]:
    ps = people()
    jobs = []
    if args.phase == "direction":
        for d in "ABC":
            lv = 3 if d == "C" else 2
            for p in ps:
                for k in range(args.n or 2):
                    jobs.append(dict(model="nano", direction=d, level=lv, person=p, k=k))
    elif args.phase == "model":
        for m in ("nano", "flux", "seedream") + (("nanopro",) if args.with_pro else ()):
            for p in ps:
                for k in range(args.n or 4):
                    jobs.append(dict(model=m, direction=args.direction, level=args.level, person=p, k=k))
    elif args.phase == "couple":
        for m in args.models.split(","):
            for i, scene in enumerate(prompts.COUPLE_SCENES):
                jobs.append(dict(model=m, direction=args.direction, level=args.level, person="casal", k=i, scene=scene))
    elif args.phase == "pivot":
        for p in ps:
            for k in range(args.n or 2):
                jobs.append(dict(model=args.model, direction=args.direction, level=3, person=p, k=k))
    else:  # avulso
        targets = [args.person] if args.person else ps
        for p in targets:
            for k in range(args.n or 1):
                jobs.append(dict(model=args.model, direction=args.direction, level=args.level, person=p, k=k))
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["direction", "model", "couple", "pivot"])
    ap.add_argument("--provider", choices=["fal", "direct"], default="fal")
    ap.add_argument("--model", choices=MODELS, default="nano")
    ap.add_argument("--direction", choices=list(prompts.DIRECTIONS), default="A")
    ap.add_argument("--level", type=int, choices=[1, 2, 3], default=2)
    ap.add_argument("--person")
    ap.add_argument("--n", type=int)
    ap.add_argument("--models", default="nano,flux,seedream", help="fase couple: modelos, separados por vírgula")
    ap.add_argument("--with-pro", action="store_true", help="inclui Nano Banana Pro na fase model (só --provider direct)")
    ap.add_argument("--upload", action="store_true", help="fal: subir fotos ao CDN em vez de data URIs")
    ap.add_argument("--cap", type=float, default=15.0, help="teto de gasto acumulado em USD")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()
    ps = people()
    jobs = plan(args)
    price = PRICE_FAL if args.provider == "fal" else PRICE_DIRECT
    n_in = {p: 3 for p in ps}
    n_in["casal"] = 6
    for j in jobs:
        if args.provider == "fal" and j["model"] not in PRICE_FAL:
            sys.exit(f"{j['model']} não existe no provedor fal; use --provider direct")
    est = sum(price[j["model"]](n_in[j["person"]]) for j in jobs)
    already = spent()
    print(f"{len(jobs)} imagens via {args.provider}, estimativa US$ {est:.2f}; já gasto US$ {already:.2f}; teto US$ {args.cap:.2f}")
    if already + est > args.cap:
        sys.exit("Acima do teto. Suba --cap conscientemente ou reduza --n.")
    if args.dry_run:
        for j in jobs:
            print("  ", j)
        return
    if args.provider == "fal" and not os.environ.get("FAL_KEY"):
        sys.exit("FAL_KEY ausente: preencha .env a partir de .env.example")

    refs_cache = {p: photo_bytes(p) for p in ps}
    for j in jobs:
        tag = f"{j['direction']}{j['level']}"
        dest = OUT / tag / j["model"]
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / f"{j['person']}-{j['k']}.png"
        if path.exists():
            print(f"  pulando {path.relative_to(HERE)} (já existe)")
            continue
        if j["person"] == "casal":
            prompt = prompts.couple_prompt(j["direction"], j["level"], j["scene"])
            refs = refs_cache[ps[0]] + refs_cache[ps[1]]
        else:
            prompt = prompts.character_sheet_prompt(j["direction"], j["level"])
            refs = refs_cache[j["person"]]
        print(f"  {j['model']:9s} {tag} {j['person']}-{j['k']} ...", end="", flush=True)
        try:
            img, meta = generate(args.provider, j["model"], prompt, refs, seed=1000 + j["k"], upload=args.upload)
        except Exception as e:  # noqa: BLE001
            print(f" FALHOU: {type(e).__name__}: {e}")
            record({**j, "provider": args.provider, "path": None, "error": f"{type(e).__name__}: {e}", "cost_usd": 0, "ts": time.time()})
            continue
        path.write_bytes(img)
        row = {**j, "provider": args.provider, "path": str(path.relative_to(HERE)), "prompt": prompt, "ts": time.time(), **meta}
        record(row)
        print(f" ok  {meta['latency_s']}s  US$ {meta['cost_usd']:.3f}")
    print(f"Total gasto até agora: US$ {spent():.2f}. Gere a folha: uv run contact_sheet.py")


if __name__ == "__main__":
    main()
