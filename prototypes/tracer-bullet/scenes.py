# /// script
# requires-python = ">=3.11"
# dependencies = ["fal-client>=0.5", "pillow>=10"]
# ///
"""PROTÓTIPO. Gera as Scenes a partir de out/script.json e das Character Sheets aprovadas (in/sheets/).

  uv run scenes.py --scene 1 --dry-run     # mostra o prompt final e o custo, sem gastar
  uv run scenes.py --scene 1               # fumaça: só a Scene 1 (olhe antes de gerar o resto)
  uv run scenes.py                         # todas as Scenes que ainda não existem
  uv run scenes.py --scene 3 --regen       # Regeneration da Scene 3 (a anterior é preservada)

Modos (--mode):
  r2v       Kling O3 Standard reference-to-video: as duas Fichas entram como elements (padrão).
  keyframe  FLUX 3 Image compõe um still do casal na Scene; o vídeo só anima esse still.
            Com --video kling usa Kling O3 image-to-video; com --video seedance usa o fallback.

Saídas: out/scenes/scene-<n>.mp4 (a tentativa em uso), out/scenes/scene-<n>.try<k>.mp4 (todas),
out/runs.jsonl (latência, custo, prompt, modo). Nada disso entra no git.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

from common import HOUSE_STYLE, OUT, SHEETS, guard, load_env, people, record, rows

sys.path.insert(0, str(HOUSE_STYLE))
import prompts  # noqa: E402  (House Style v1: direção A, nível 2)

KLING_R2V = "fal-ai/kling-video/o3/standard/reference-to-video"
KLING_I2V = "fal-ai/kling-video/o3/standard/image-to-video"
SEEDANCE_I2V = "fal-ai/bytedance/seedance/v1.5/pro/image-to-video"
FLUX_EDIT = "fal-ai/flux-3-image/edit"

KLING_PER_S = 0.084  # USD/s sem áudio (página do modelo no fal, 2026-11-08)
FLUX_PER_IMAGE = 0.048


def seedance_cost(seconds: int, w: int = 1080, h: int = 1920, fps: int = 24) -> float:
    return (h * w * fps * seconds / 1024) * 1.20 / 1e6  # US$ 1,20 por 1M tokens de vídeo, sem áudio


# O Script só descreve conteúdo. Estilo e identidade são do harness, iguais em toda Scene.
_style = prompts.DIRECTIONS["A"]["text"].split(" Background:")[0]  # sem o fundo liso da Ficha
VIDEO_STYLE = (
    f"{_style} {prompts.LEVELS[2]['text']} "
    "The whole scene, including the setting and props, is rendered in this same stylized 3D animated look, "
    "never live-action or photorealistic."
)
IDENTITY = (
    "@Element1 and @Element2 are two different people. Keep each one's face, hair, skin tone and build exactly "
    "as in their reference image for the entire shot; never blend or swap their features. Exactly two people in frame."
)
AVOID = "No text, captions, subtitles, logos or watermarks. No extra fingers or limbs. No cuts."


def video_prompt(visual_prompt: str) -> str:
    return " ".join([visual_prompt.strip(), IDENTITY, VIDEO_STYLE, AVOID])


def data_uri(path: Path, max_side: int = 1360) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def sheet_urls(upload: bool) -> list[str]:
    """Por padrão data URIs (nada fica no CDN do fal). --upload sobe ao CDN se o endpoint recusar."""
    import fal_client

    paths = [SHEETS / f"{p}.png" for p in people()]
    if upload:
        return [fal_client.upload_file(str(p)) for p in paths]
    return [data_uri(p) for p in paths]


def fal_run(endpoint: str, arguments: dict) -> tuple[dict, dict]:
    import fal_client

    metrics: dict = {}

    def on_update(ev):
        if isinstance(ev, fal_client.Completed):
            metrics.update(ev.metrics or {})

    t0 = time.time()
    result = fal_client.subscribe(endpoint, arguments=arguments, with_logs=True, on_queue_update=on_update)
    return result, {"latency_s": round(time.time() - t0, 1), "inference_s": metrics.get("inference_time")}


def fetch(url: str) -> bytes:
    if url.startswith("data:"):
        return base64.b64decode(url.split(",", 1)[1])
    return urllib.request.urlopen(url).read()


def strip_uris(arguments: dict) -> dict:
    """Para o runs.jsonl: nunca gravar imagens em base64."""
    def clean(v):
        if isinstance(v, str) and v.startswith("data:"):
            return "<data-uri>"
        if isinstance(v, list):
            return [clean(x) for x in v]
        if isinstance(v, dict):
            return {k: clean(x) for k, x in v.items()}
        return v
    return clean(arguments)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", type=int, help="só esta Scene (1-based)")
    ap.add_argument("--regen", action="store_true", help="Regeneration: gera de novo mesmo que já exista")
    ap.add_argument("--mode", choices=["r2v", "keyframe"], default="r2v")
    ap.add_argument("--video", choices=["kling", "seedance"], default="kling")
    ap.add_argument("--upload", action="store_true", help="sobe as Fichas ao CDN do fal em vez de data URIs")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.video == "seedance" and args.mode != "keyframe":
        sys.exit("Seedance 1.5 Pro não aceita elements: use --mode keyframe --video seedance")

    load_env()
    script = json.loads((OUT / "script.json").read_text())
    seconds = int(script["seconds"])
    scenes = [s for s in script["scenes"] if args.scene in (None, s["n"])]
    dest = OUT / "scenes"
    dest.mkdir(parents=True, exist_ok=True)
    todo = [s for s in scenes if args.regen or not (dest / f"scene-{s['n']}.mp4").exists()]
    if not todo:
        sys.exit("Nada a gerar (as Scenes já existem; use --regen para uma Regeneration).")

    per_video = seedance_cost(seconds) if args.video == "seedance" else KLING_PER_S * seconds
    per_scene = per_video + (FLUX_PER_IMAGE if args.mode == "keyframe" else 0)
    print(f"{len(todo)} Scene(s), {seconds}s, modo {args.mode}/{args.video}, US$ {per_scene:.3f} cada")
    guard(per_scene * len(todo))
    if args.dry_run:
        for s in todo:
            print(f"\n[{s['n']}] {video_prompt(s['visual_prompt'])}")
        return

    sheets = sheet_urls(args.upload)
    for s in todo:
        n = s["n"]
        k = sum(1 for r in rows() if r["stage"] == "scene" and r.get("scene") == n and not r.get("error"))
        prompt = video_prompt(s["visual_prompt"])
        base = {"scene": n, "attempt": k, "regeneration": k > 0, "mode": args.mode, "video": args.video, "seconds": seconds}
        print(f"  Scene {n} tentativa {k} ...", end="", flush=True)
        try:
            keyframe_url = None
            if args.mode == "keyframe":
                kf_prompt = " ".join([
                    s["visual_prompt"].replace("@Element1", "the person in the first image").replace("@Element2", "the person in the second image"),
                    "9:16 vertical.", prompts.COUPLE_RULE.replace("reference set", "image"),
                    VIDEO_STYLE, "No text, captions, logos or watermarks. Exactly two people in frame.",
                ])
                kf_args = {"prompt": kf_prompt, "image_urls": sheets, "aspect_ratio": "9:16", "resolution": "1k", "output_format": "png"}
                res, m = fal_run(FLUX_EDIT, kf_args)
                kf = fetch(res["images"][0]["url"])
                kf_path = dest / f"scene-{n}.try{k}.keyframe.png"
                kf_path.write_bytes(kf)
                record("keyframe", **base, endpoint=FLUX_EDIT, cost_usd=FLUX_PER_IMAGE, prompt=kf_prompt, path=str(kf_path.relative_to(OUT.parent)), **m)
                keyframe_url = data_uri(kf_path)

            if args.mode == "r2v":
                endpoint = KLING_R2V
                vargs = {"prompt": prompt, "elements": [{"frontal_image_url": u, "reference_image_urls": [u]} for u in sheets],
                         "duration": str(seconds), "aspect_ratio": "9:16", "generate_audio": False}
            elif args.video == "kling":
                endpoint = KLING_I2V
                vargs = {"prompt": prompt.replace("@Element1", "the first person").replace("@Element2", "the second person"),
                         "image_url": keyframe_url, "duration": str(seconds), "generate_audio": False}
            else:
                endpoint = SEEDANCE_I2V
                vargs = {"prompt": prompt.replace("@Element1", "the first person").replace("@Element2", "the second person"),
                         "image_url": keyframe_url, "aspect_ratio": "9:16", "resolution": "1080p",
                         "duration": str(seconds), "generate_audio": False}
            res, m = fal_run(endpoint, vargs)
            video = fetch(res["video"]["url"])
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {str(e)[:300]}"  # o fal ecoa o payload (base64) nos erros
            print(f" FALHOU: {err}")
            record("scene", **base, error=err, cost_usd=0)
            continue
        path = dest / f"scene-{n}.try{k}.mp4"
        path.write_bytes(video)
        shutil.copyfile(path, dest / f"scene-{n}.mp4")  # a tentativa mais recente é a que a montagem usa
        record("scene", **base, endpoint=endpoint, cost_usd=round(per_video, 4), prompt=prompt,
               arguments=strip_uris(vargs), path=str(path.relative_to(OUT.parent)), **m)
        print(f" ok  {m['latency_s']}s  US$ {per_video:.2f}  -> {path.relative_to(OUT.parent)}")
    print("Assista cada Scene antes de seguir. Livro-caixa: uv run report.py")


if __name__ == "__main__":
    main()
