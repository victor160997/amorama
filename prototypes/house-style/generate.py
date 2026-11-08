# /// script
# requires-python = ">=3.11"
# dependencies = ["google-genai>=2.3", "replicate>=1.0", "pillow>=10"]
# ///
"""PROTÓTIPO. Gera Character Sheets (e stills de casal) com 3 modelos para comparar o House Style.

Uso (dentro de prototypes/house-style/, com .env preenchido):

  uv run generate.py --phase direction                 # fase 0: 3 direções, só Nano Banana 2.1
  uv run generate.py --phase model --direction A       # fase A: 3 modelos na direção escolhida
  uv run generate.py --phase couple --direction A      # fase B: stills de casal nos 3 modelos
  uv run generate.py --phase pivot --direction A --model nano   # fase C: nível 3 no vencedor
  uv run generate.py --model flux --direction B --level 2 --n 1 --person ana   # chamada avulsa

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
from pathlib import Path

from PIL import Image

import prompts

HERE = Path(__file__).parent
PHOTOS = HERE / "photos"
OUT = HERE / "out"
RUNS = OUT / "runs.jsonl"

# Preços de tabela (USD por imagem 1K), pesquisa de 2026-11-07. Nano Banana é calculado
# pelos tokens reais quando a API devolve usage; isto é só a estimativa prévia.
PRICE = {
    "nano": 0.0336 + 0.004,  # saída 1120 tokens + ~2.5K tokens de entrada (3 fotos)
    "nanopro": 0.134 + 0.004,
    "flux": 0.024,  # Replicate; tabela BFL seria 0,048
    "seedream": 0.045,
}
GEMINI_IN_PER_TOKEN = 1.50 / 1_000_000
GEMINI_OUT_PER_TOKEN = 30.0 / 1_000_000
GEMINI_PRO_OUT_PER_TOKEN = 120.0 / 1_000_000  # 0,134 USD / 1120 tokens

MODEL_IDS = {
    "nano": "gemini-nano-banana-2.1",
    "nanopro": "gemini-3-pro-image",
    "flux": "black-forest-labs/flux-3-image",
    "seedream": "bytedance/seedream-5-pro",
}


def load_env() -> None:
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def people() -> list[str]:
    if not PHOTOS.exists():
        sys.exit(f"Crie {PHOTOS}/<pessoa>/ com 3 fotos por pessoa.")
    ps = sorted(p.name for p in PHOTOS.iterdir() if p.is_dir() and not p.name.startswith("_"))
    if len(ps) != 2:
        sys.exit(f"Esperava exatamente 2 pastas em {PHOTOS}, achei {ps}")
    return ps


def photo_bytes(person: str, max_side: int = 1536) -> list[tuple[bytes, str]]:
    """Fotos da pessoa redimensionadas em memória (menos tokens, upload menor)."""
    files = sorted(
        f for f in (PHOTOS / person).iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"}
    )
    if not files:
        sys.exit(f"Nenhuma foto em {PHOTOS / person}")
    out = []
    for f in files:
        im = Image.open(f)
        im = im.convert("RGB")
        im.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=90)
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


# ---------- chamadas ----------


def call_gemini(model_key: str, prompt: str, refs: list[tuple[bytes, str]]) -> tuple[bytes, dict]:
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = MODEL_IDS[model_key]
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
        # Fallback: Interactions API (forma oficialmente documentada para nano-banana-2.1).
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
        f.name = f"ref{i}.jpg"  # o cliente usa o nome ao fazer upload
    if model_key == "flux":
        inp = {"prompt": prompt, "images": files, "aspect_ratio": "9:16", "resolution": "1k",
               "output_format": "png", "grounding": False}
    else:
        inp = {"prompt": prompt, "image_input": files, "aspect_ratio": "9:16", "size": "1K",
               "output_format": "png"}
    pred = replicate.predictions.create(model=MODEL_IDS[model_key], input=inp)
    pred.wait()
    pred.reload()
    if pred.status != "succeeded":
        raise RuntimeError(f"{pred.status}: {pred.error}")
    out = pred.output
    first = out[0] if isinstance(out, list) else out
    data = first.read() if hasattr(first, "read") else __import__("urllib.request").request.urlopen(first).read()
    return data, {"api": "replicate", "predict_time_s": (pred.metrics or {}).get("predict_time"),
                  "cost_usd": PRICE[model_key]}


def generate(model_key: str, prompt: str, refs: list[tuple[bytes, str]]) -> tuple[bytes, dict]:
    t0 = time.time()
    if model_key in ("nano", "nanopro"):
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
        for m in ("nano", "flux", "seedream"):
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
    ap.add_argument("--model", choices=list(MODEL_IDS), default="nano")
    ap.add_argument("--direction", choices=list(prompts.DIRECTIONS), default="A")
    ap.add_argument("--level", type=int, choices=[1, 2, 3], default=2)
    ap.add_argument("--person")
    ap.add_argument("--n", type=int)
    ap.add_argument("--with-pro", action="store_true", help="inclui Nano Banana Pro na fase model")
    ap.add_argument("--cap", type=float, default=15.0, help="teto de gasto acumulado em USD")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()
    jobs = plan(args)
    est = sum(PRICE[j["model"]] for j in jobs)
    already = spent()
    print(f"{len(jobs)} imagens, estimativa US$ {est:.2f}; já gasto US$ {already:.2f}; teto US$ {args.cap:.2f}")
    if already + est > args.cap:
        sys.exit("Acima do teto. Suba --cap conscientemente ou reduza --n.")
    if args.dry_run:
        for j in jobs:
            print("  ", j)
        return

    ps = people()
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
            img, meta = generate(j["model"], prompt, refs)
        except Exception as e:  # noqa: BLE001
            print(f" FALHOU: {type(e).__name__}: {e}")
            record({**j, "path": None, "error": f"{type(e).__name__}: {e}", "cost_usd": 0, "ts": time.time()})
            continue
        path.write_bytes(img)
        row = {**j, "path": str(path.relative_to(HERE)), "prompt": prompt, "ts": time.time(), **meta}
        record(row)
        print(f" ok  {meta['latency_s']}s  US$ {meta['cost_usd']:.3f}")
    print(f"Total gasto até agora: US$ {spent():.2f}. Gere a folha: uv run contact_sheet.py")


if __name__ == "__main__":
    main()
