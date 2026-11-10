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

## Resultado (2026-11-09)

Casal fundador, Story real de 192 caracteres. Imagens e vídeos não estão no repositório; só os números.

| Etapa | Chamadas | Latência | Custo |
|---|---|---|---|
| Script (`claude-opus-5-5`, saída estruturada, sem edição manual) | 1 | 17 s | US$ 0,03 |
| Scenes (Kling O3 Standard reference-to-video, 8 s, 9:16, Fichas como *elements*) | 4 ok + 1 erro de payload | 191 a 203 s cada (inferência ~188 s) | US$ 2,69 |
| Regenerations | 0 | | |
| Montagem (ffmpeg, 32 s, 1080×1920, música, legendas) | 1 | 48 s | 0 |
| **Total** | | | **US$ 2,72** de 30 |

- Painel cego de 3: **3 de 3** reconheceram as duas Fichas; no Final Video, "mesmas pessoas" nas 4 Scenes, nenhum artefato apontado. Casal: "conta a nossa história? sim, está perfeito". Reação de fora: "pagariam R$ 100, mas por mais tempo de vídeo talvez" (32 s pareceu curto para esse preço).
- Extrapolação para 6 Scenes + 1 Regeneration: **US$ 4,88** (faixa go, ≤ US$ 8). Latência projetada após a Approval: 6 Scenes em paralelo ≈ 4,5 min; em série ≈ 21 min.
- Saída nativa do Kling O3 Standard: **720×1280 a 24 fps**, reescalada para 1080p na montagem.
- O Kling manteve a **roupa das Fichas** em todas as Scenes, ignorando "roupa de praia" no prompt: bom para consistência, e o Script não deve pedir troca de roupa.
- Payload do `reference-to-video`: cada elemento exige `frontal_image_url` **e** `reference_image_urls` (a mesma Ficha nos dois funciona). Data URIs aceitas.

## Rodada 2 (2026-11-09): Story narrativa + 1 Regeneration

Responde ao ticket [Tracer bullet 2: Story narrativa + 1 Regeneration (≤ US$ 5)](https://github.com/victor160997/amorama/issues/19). Rodada isolada da primeira: Story em `in/tb2/story.txt`, saídas e livro-caixa em `out/tb2/`, mesmas Character Sheets.

```bash
export TB_RUN=tb2 TB_CAP=5
uv run script.py --scenes 2 --seconds 8
uv run scenes.py                      # 2 Scenes
uv run scenes.py --scene 1 --regen    # a Regeneration, mesmo prompt e mesmas Fichas
python3 report.py
```

| Etapa | Chamadas | Latência | Custo |
|---|---|---|---|
| Script (`claude-opus-5-5`, sem edição manual) | 1 | 12 s | US$ 0,03 |
| Scenes (Kling O3 Standard reference-to-video, 8 s) | 2 | 215 e 220 s | US$ 1,34 |
| Regeneration da Scene 1 (mesmo prompt) | 1 | 197 s | US$ 0,67 |
| **Total** | | | **US$ 2,04** de 5 |

- Story narrativa de 4 parágrafos (598 caracteres). O Script escolheu o primeiro beijo (na fila de uma boate, à noite) e um passeio de bondinho; só a Scene 1 tem contato físico. Dança e abraço seguem sem teste.
- **Identidade e roupa seguram no beijo**: rosto, cabelo, barba, vestido, colar e camiseta iguais às Fichas nos 3 clipes, sem troca de identidade nem de cor de roupa. Casal: "mesmas pessoas, sem troca de identidade ou roupa".
- **A Regeneration mantém as pessoas, mas é outra tomada**: os dois trocam de lado, o cenário muda, ficam de perfil o tempo todo e **o beijo pedido no prompt não acontece** (a legenda fala em beijo). O casal ainda assim disse que combina com as outras Scenes e que ficaria satisfeito.
- A Scene original também desviou do prompt: o beijo acontece no início e no fim (pedido só no fim) e o cenário saiu pôr do sol ao ar livre, não noite na porta de uma boate.
