# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=1.0", "pydantic>=2"]
# ///
"""PROTÓTIPO. Story -> Script (4 Scenes) via Claude API, com saída estruturada.

  uv run script.py                 # lê in/story.txt, grava out/script.json
  uv run script.py --scenes 4 --seconds 8

Depois de gerar, LEIA out/script.json. Editar à mão é permitido no concierge; anote no ticket se editou.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

import anthropic
from pydantic import BaseModel, Field

from common import IN, OUT, load_env, people, record

MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 4.00 / 1e6, 20.00 / 1e6  # USD por token (tabela Opus 5.5)


class Scene(BaseModel):
    n: int
    story_moment: str = Field(description="Trecho ou momento da Story que esta Scene mostra, em PT-BR, 1 frase")
    visual_prompt: str = Field(description="Prompt em inglês para o modelo de vídeo")
    subtitle: str = Field(description="Legenda em PT-BR")


class Script(BaseModel):
    title: str
    scenes: list[Scene]


SYSTEM = """You turn a couple's own written story into the Script of a short vertical animated video.

The video is {n} Scenes of about {seconds} seconds each, shown in order with one subtitle line per Scene and background music. There is no narration and no dialogue audio, so each Scene has to read on its own as a moving image.

How the Scenes get made, which shapes what a good visual_prompt looks like: an image-to-video model receives one approved reference image per person and your visual_prompt. It refers to the two people only through the literal tokens @Element1 ({p1}) and @Element2 ({p2}). The harness appends the visual style and the identity rules afterwards, so leave style, rendering and "keep their faces" instructions out; your job is content.

The risk this video lives or dies on is likeness: the two characters must stay recognizably the same two people in every Scene. Video models lose identity when faces are small, turned away, occluded, or when a lot happens at once. So each visual_prompt should describe:
- one simple, continuous action that fits in {seconds} seconds (no cuts, no time jumps, no sequence of events);
- both people in frame, in a medium or medium-close shot, faces visible to the camera for most of the Scene;
- one concrete setting with a few specific details taken from the Story, and the time of day or light;
- one slow camera move at most (slow push-in, gentle orbit, or static).
Always write "@Element1" and "@Element2" instead of names or descriptions of the people; never describe their face, hair, skin or body, because the reference images carry that. Clothing may be mentioned only when the Story makes it matter (a wedding, a beach). Avoid readable text, signs, screens, logos, crowds, children, pets, and other characters with visible faces: the product has exactly two people on screen.

Choose the {n} moments that the couple would most want to see again, in the order they happened, so that someone who knows them recognises their story. Stay faithful to what the Story says: do not invent events, places or details it does not support. If the Story is thin, prefer a quiet, true moment over an invented dramatic one.

Each subtitle is one line in Brazilian Portuguese, at most 12 words, in the couple's own voice and tone (first person plural when it fits), without emojis or hashtags. Together the subtitles should read as a tiny version of their story. story_moment is one sentence in Portuguese saying which part of the Story the Scene shows. title is a short Portuguese title for the video. Write every visual_prompt in English, 40 to 90 words."""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenes", type=int, default=4)
    ap.add_argument("--seconds", type=int, default=8)
    args = ap.parse_args()

    load_env()
    story_path = IN / "story.txt"
    if not story_path.exists() or not story_path.read_text().strip():
        sys.exit(f"Escreva a Story do casal em {story_path}")
    story = story_path.read_text().strip()
    p1, p2 = people()

    client = anthropic.Anthropic()
    t0 = time.time()
    resp = client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        output_config={"effort": "high"},
        system=SYSTEM.format(n=args.scenes, seconds=args.seconds, p1=p1, p2=p2),
        messages=[{"role": "user", "content": f"The couple's Story, exactly as they wrote it:\n\n<story>\n{story}\n</story>"}],
        output_format=Script,
    )
    latency = round(time.time() - t0, 1)
    if resp.stop_reason == "refusal":
        sys.exit(f"Claude recusou a Story: {resp.stop_details}")
    script = resp.parsed_output
    if script is None or len(script.scenes) != args.scenes:
        sys.exit(f"Script inválido (stop_reason={resp.stop_reason}): {resp.content}")

    cost = resp.usage.input_tokens * PRICE_IN + resp.usage.output_tokens * PRICE_OUT
    OUT.mkdir(exist_ok=True)
    (OUT / "script.json").write_text(json.dumps({**script.model_dump(), "seconds": args.seconds}, ensure_ascii=False, indent=2))
    record("script", model=MODEL, latency_s=latency, cost_usd=round(cost, 4),
           in_tokens=resp.usage.input_tokens, out_tokens=resp.usage.output_tokens, story_chars=len(story))
    print(f"ok  {latency}s  US$ {cost:.3f}  -> out/script.json\n")
    print(script.title)
    for s in script.scenes:
        print(f"\n[{s.n}] {s.story_moment}\n    legenda: {s.subtitle}\n    prompt:  {s.visual_prompt}")


if __name__ == "__main__":
    main()
