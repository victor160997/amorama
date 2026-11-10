# /// script
# requires-python = ">=3.11"
# dependencies = ["static-ffmpeg>=2.5", "pillow>=10"]
# ///
"""PROTÓTIPO. Tira de 6 quadros por Scene para a conferência Scene × legenda do concierge.

  uv run strips.py              # todas as Scenes em uso (out/scenes/scene-<n>.mp4)
  uv run strips.py --scene 3    # só a Scene 3 (depois de um Retake)

Grava out/tmp/strip-<n>.png (6 quadros lado a lado, com a legenda embaixo). Nada disso entra no git.
"""

from __future__ import annotations

import argparse
import json
import subprocess

from PIL import Image, ImageDraw
from static_ffmpeg import run as _sff

from common import OUT

FFMPEG, _ = _sff.get_or_fetch_platform_executables_else_raise()
FRAMES, FRAME_W = 6, 320


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", type=int)
    args = ap.parse_args()
    script = json.loads((OUT / "script.json").read_text())
    seconds = int(script["seconds"])
    tmp = OUT / "tmp"
    tmp.mkdir(exist_ok=True)
    for s in script["scenes"]:
        n = s["n"]
        clip = OUT / "scenes" / f"scene-{n}.mp4"
        if args.scene not in (None, n) or not clip.exists():
            continue
        frames = []
        for i in range(FRAMES):
            t = 0.3 + i * (seconds - 0.6) / (FRAMES - 1)
            f = tmp / f"f-{n}-{i}.png"
            subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(clip), "-frames:v", "1",
                            "-vf", f"scale={FRAME_W}:-2", str(f)], check=True)
            frames.append(Image.open(f).convert("RGB"))
        h = frames[0].height
        strip = Image.new("RGB", (FRAME_W * FRAMES, h + 40), "black")
        for i, im in enumerate(frames):
            strip.paste(im, (i * FRAME_W, 0))
        ImageDraw.Draw(strip).text((10, h + 12), f"Scene {n}: {s['subtitle']}", fill="white")
        dest = tmp / f"strip-{n}.png"
        strip.save(dest)
        for i in range(FRAMES):
            (tmp / f"f-{n}-{i}.png").unlink()
        print(dest)


if __name__ == "__main__":
    main()
