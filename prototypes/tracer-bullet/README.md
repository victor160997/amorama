# Protótipo: tracer bullet (um Final Video de ponta a ponta)

**Descartável.** Responde ao ticket [Tracer bullet: um Final Video completo de ponta a ponta (≤ US$ 30)](https://github.com/victor160997/amorama/issues/9). Vive no branch `prototype/tracer-bullet` (nascido de `prototype/house-style`, de onde reaproveita `prompts.py`); só a decisão volta para `main`.

Pergunta: dá para gerar, à mão, um Final Video inteiro para um Couple real, com semelhança aceita pelo painel cego e custo dentro das faixas do gate? Critério completo em [Critério de aceite do tracer bullet e do gate](https://github.com/victor160997/amorama/issues/7).

| Arquivo | Etapa |
|---|---|
| `script.py` | Story → Script via Claude API (saída estruturada) |
| `scenes.py` | Script + Character Sheets aprovadas → Scenes (Kling O3 Standard no fal.ai; keyframe e Seedance como alternativas) |
| `assemble.py` | Scenes + legendas + música → `out/final.mp4` (ffmpeg embutido, sem instalar nada) |
| `report.py` | custo e latência por etapa, extrapolação para 6 Scenes + 1 Regeneration |
| `common.py` | caminhos, `.env`, livro-caixa `out/runs.jsonl`, teto de US$ 30 |

**O repositório é público.** `in/` (Story, Fichas, música), `out/` (Script, Scenes, Final Video, livro-caixa) e `.env` estão no `.gitignore` e nunca são commitados. Só as notas e os números vão para o ticket.

## Entradas (só o fundador pode fornecer)

- `in/story.txt`: a Story, escrita como um Couple cliente escreveria.
- `in/sheets/<pessoa>.png`: as duas Character Sheets com Approval, copiadas de `out/A2/flux/` do protótipo de House Style. A ordem alfabética dos nomes define `@Element1` e `@Element2`.
- `in/music.mp3`: uma faixa royalty-free.
- `.env` com `ANTHROPIC_API_KEY` (a `FAL_KEY` é lida do `.env` do protótipo de House Style).

## Ordem (stage-gate: nenhum centavo em vídeo antes do painel aprovar as Fichas)

```bash
cd prototypes/tracer-bullet
# 1. Approval das Fichas pelo Couple, depois painel cego de 3 pessoas (2 de 3 acertam as duas).
# 2. Script
uv run script.py --scenes 4 --seconds 8      # leia out/script.json
# 3. Scenes
uv run scenes.py --scene 1 --dry-run         # confere prompt e custo
uv run scenes.py --scene 1                   # fumaça: uma Scene, assista
uv run scenes.py                             # as outras
uv run scenes.py --scene 3 --regen           # a 1 Regeneration orçada
# 4. Montagem
uv run assemble.py
# 5. Números
python3 report.py
```

Se a identidade quebrar no modo padrão (`r2v`, Fichas como *elements*): `uv run scenes.py --scene N --regen --mode keyframe` (FLUX compõe um still do casal e o vídeo só anima); se o Kling falhar ou recusar: `--mode keyframe --video seedance`.

## Painel cego (3 pessoas próximas do casal)

Registrar as respostas literais no ticket, sem as imagens.

1. **Fichas** (antes de qualquer Scene): mostrar as duas Character Sheets sem contexto. "Quem são essas duas pessoas?" Aceite: 2 de 3 acertam as duas.
2. **Final Video** (depois da montagem), por Scene: "Os dois continuam sendo as mesmas pessoas das imagens?" (4 de 4); "Viu algo deformado ou estranho?" (no máximo 1 Scene); com a Story em mãos, "que momento do texto é esta Scene?" (3 de 4).
3. **Casal**: "Este vídeo conta a nossa história?" (sim ou não).
4. **Fora do gate**: reação de 2 ou 3 casais de fora ("pagariam R$ X?"), só registrada.
