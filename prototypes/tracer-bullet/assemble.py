# /// script
# requires-python = ">=3.11"
# dependencies = ["static-ffmpeg>=2.5", "pillow>=10"]
# ///
"""PROTÓTIPO. Monta o Final Video: Scenes em ordem + legendas + música -> out/final.mp4 (9:16, 1080x1920).

  uv run assemble.py                 # usa out/scenes/scene-<n>.mp4, out/script.json, in/music.*
  uv run assemble.py --no-music      # só para conferir vídeo e legendas

As legendas são desenhadas com Pillow e sobrepostas (não depende de libass nem de fontes do sistema).
No fim confere o critério de montagem (pass/fail técnico) e grava a latência no livro-caixa.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from static_ffmpeg import run as _sff

from common import IN, OUT, record

W, H, FPS = 1080, 1920, 30
FONTS = [IN / "font.ttf", Path("/mnt/c/Windows/Fonts/segoeuib.ttf"), Path("/mnt/c/Windows/Fonts/arialbd.ttf"),
         Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]

FFMPEG, FFPROBE = _sff.get_or_fetch_platform_executables_else_raise()


def probe(path: Path) -> dict:
    out = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def subtitle_png(text: str, dest: Path, size: int = 62, max_w: int = 900, center_y: float = 0.74) -> None:
    """Uma ou duas linhas, branco com contorno escuro, fora da faixa que Reels/TikTok cobrem embaixo."""
    font = ImageFont.truetype(str(next(f for f in FONTS if f.exists())), size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    block = "\n".join(lines)
    xy = (W / 2, H * center_y)
    kw = dict(font=font, anchor="mm", align="center", spacing=14)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).multiline_text(xy, block, fill=(0, 0, 0, 200), stroke_width=10, stroke_fill=(0, 0, 0, 200), **kw)
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(img).multiline_text(xy, block, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(20, 20, 20, 255), **kw)
    img.save(dest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--music-volume", type=float, default=0.8)
    args = ap.parse_args()

    script = json.loads((OUT / "script.json").read_text())
    scenes = script["scenes"]
    clips = [OUT / "scenes" / f"scene-{s['n']}.mp4" for s in scenes]
    missing = [c.name for c in clips if not c.exists()]
    if missing:
        sys.exit(f"Faltam Scenes: {missing}")
    music = None if args.no_music else next((p for p in sorted(IN.glob("music.*"))), None)
    if not args.no_music and music is None:
        sys.exit(f"Coloque a faixa em {IN}/music.mp3 (ou use --no-music)")

    t0 = time.time()
    tmp = OUT / "tmp"
    tmp.mkdir(exist_ok=True)
    durs, native = [], []
    for c in clips:
        p = probe(c)
        v = next(s for s in p["streams"] if s["codec_type"] == "video")
        durs.append(float(p["format"]["duration"]))
        native.append(f"{v['width']}x{v['height']}@{v.get('r_frame_rate')}")
    total = sum(durs)

    cmd = [FFMPEG, "-y", "-v", "error"]
    for c in clips:
        cmd += ["-i", str(c)]
    for i, s in enumerate(scenes):
        png = tmp / f"sub-{s['n']}.png"
        subtitle_png(s["subtitle"], png)
        cmd += ["-loop", "1", "-t", f"{durs[i]:.3f}", "-i", str(png)]
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(music)]

    n = len(clips)
    fc = []
    for i in range(n):
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1[v{i}]")
        # legenda entra e sai com fade curto dentro da Scene
        fc.append(f"[{n + i}:v]format=rgba,fade=in:st=0.3:d=0.4:alpha=1,fade=out:st={max(durs[i] - 0.6, 0):.3f}:d=0.4:alpha=1[s{i}]")
        fc.append(f"[v{i}][s{i}]overlay=0:0:shortest=1[o{i}]")
    fc.append("".join(f"[o{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,fade=in:st=0:d=0.5,fade=out:st={total - 0.8:.3f}:d=0.8,format=yuv420p[vout]")
    maps = ["-map", "[vout]"]
    if music:
        fc.append(f"[{2 * n}:a]atrim=0:{total:.3f},afade=in:st=0:d=0.8,afade=out:st={total - 1.5:.3f}:d=1.5,volume={args.music_volume}[aout]")
        maps += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    final = OUT / "final.mp4"
    cmd += ["-filter_complex", ";".join(fc), *maps, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-r", str(FPS), "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)]
    subprocess.run(cmd, check=True)
    latency = round(time.time() - t0, 1)

    p = probe(final)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in p["streams"])
    dur = float(p["format"]["duration"])
    checks = {
        "MP4 9:16 1080x1920": (v["width"], v["height"]) == (W, H),
        f"duração ~{len(scenes) * int(script['seconds'])} s": abs(dur - len(scenes) * int(script["seconds"])) <= 3,
        "tem música": has_audio,
        "Scenes em ordem": True,  # por construção (ordem do Script)
    }
    record("assemble", latency_s=latency, cost_usd=0, duration_s=round(dur, 2), native=native,
           size_mb=round(final.stat().st_size / 1e6, 1), checks=checks)
    print(f"ok  {latency}s  -> out/final.mp4  ({dur:.1f}s, {final.stat().st_size / 1e6:.1f} MB)")
    print(f"resolução nativa das Scenes: {sorted(set(native))} (reescaladas para {W}x{H})")
    for k, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}")
    print("  ?     legendas legíveis no celular: confira assistindo no aparelho")


if __name__ == "__main__":
    main()
