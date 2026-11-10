"""PROTÓTIPO. Peças comuns do tracer bullet: caminhos, .env, livro-caixa (runs.jsonl) e teto de gasto."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
# TB_RUN=tb2 isola uma segunda rodada: Story em in/tb2/story.txt, saídas e livro-caixa em out/tb2/.
# As Character Sheets (in/sheets/) são as mesmas em todas as rodadas.
RUN = os.environ.get("TB_RUN", "")
SHEETS = HERE / "in" / "sheets"
IN = HERE / "in" / RUN  # story.txt, music.mp3 (nunca no git)
OUT = HERE / "out" / RUN  # script.json, scenes/, final.mp4, runs.jsonl (nunca no git)
RUNS = OUT / "runs.jsonl"
HOUSE_STYLE = HERE.parent / "house-style"  # prompts.py versionado (este branch nasce de prototype/house-style)
# Fotos, Fichas geradas e .env do House Style vivem (fora do git) no worktree daquele protótipo.
HOUSE_STYLE_LOCAL = HERE.parents[2] / "prototype-house-style" / "prototypes" / "house-style"

CAP_USD = float(os.environ.get("TB_CAP", "30"))  # teto do ticket (tracer bullet 2: TB_CAP=5)


def load_env() -> None:
    """Lê .env daqui e, na falta, o do protótipo de House Style (mesma FAL_KEY)."""
    for env in (HERE / ".env", HOUSE_STYLE / ".env", HOUSE_STYLE_LOCAL / ".env"):
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if v.strip():
                        os.environ.setdefault(k.strip(), v.strip().strip('"'))


def rows() -> list[dict]:
    if not RUNS.exists():
        return []
    return [json.loads(l) for l in RUNS.read_text().splitlines() if l.strip()]


def spent() -> float:
    return sum(r.get("cost_usd", 0) or 0 for r in rows())


def record(stage: str, **row) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with RUNS.open("a") as f:
        f.write(json.dumps({"stage": stage, "ts": time.time(), **row}, ensure_ascii=False) + "\n")


def guard(estimate: float, cap: float = CAP_USD) -> None:
    already = spent()
    print(f"estimativa US$ {estimate:.2f}; já gasto US$ {already:.2f}; teto US$ {cap:.2f}")
    if already + estimate > cap:
        sys.exit("Acima do teto do tracer bullet. Pare e reavalie.")


def people() -> list[str]:
    """Ordem fixa: pessoa 1 = @Element1, pessoa 2 = @Element2."""
    sheets = sorted(p.stem for p in SHEETS.glob("*.png"))
    if len(sheets) != 2:
        sys.exit(f"Esperava exatamente 2 Character Sheets aprovadas em {SHEETS}, achei {sheets}")
    return sheets
