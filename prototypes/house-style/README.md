# Protótipo: House Style e Character Sheets

**Descartável.** Responde ao ticket [House Style: guia de prompt do estilo 3D e protótipo de Character Sheets](https://github.com/victor160997/amorama/issues/8). Vive no branch `prototype/house-style`; só a decisão volta para `main`.

- `HOUSE-STYLE.md`: o guia (3 direções + dial de caricatura + plano de teste).
- `prompts.py`: os textos de prompt que o harness usa. `python prompts.py A 2` imprime um.
- `generate.py`: gera as imagens nos modelos candidatos e registra latência e custo.
- `contact_sheet.py`: monta `out/index.html` para comparar e dar notas, com modo cego.

## Antes de rodar (só o fundador pode fazer)

1. **Contas e chaves.** Google AI Studio (Nano Banana 2.1, pré-pago) e Replicate (FLUX 3 Image e Seedream 5.0 Pro). Copie `.env.example` para `.env` e preencha. O `.env` está no `.gitignore`.
2. **Fotos.** `photos/<nome>/` para cada pessoa do casal, 3 fotos: frontal, 3/4, corpo inteiro, luz natural, sem óculos escuros. Exatamente duas pastas. **O repositório é público: `photos/` e `out/` estão no `.gitignore` e não podem ser commitados nunca.**
3. **Consentimento.** Os termos da BFL (FLUX) exigem consentimento documentado da pessoa retratada, e a pesquisa de LGPD pede o mesmo. Guarde uma mensagem escrita do seu par autorizando o teste, fora do repositório.
4. `uv` instalado (já está nesta máquina).

## Rodar

```bash
cd prototypes/house-style
uv run generate.py --phase direction --dry-run   # confere plano e custo sem gastar
uv run generate.py --phase direction             # fase 0: 12 imagens, ~US$ 0,45
uv run contact_sheet.py && xdg-open out/index.html
# escolhida a direção (ex.: A):
uv run generate.py --phase model --direction A   # fase A: 24 imagens, ~US$ 0,85
uv run generate.py --phase couple --direction A  # fase B: 9 imagens, ~US$ 0,35
uv run generate.py --phase pivot --direction A --model nano   # fase C: nível 3 no vencedor
```

`generate.py` recusa rodar se o gasto acumulado em `out/runs.jsonl` mais a estimativa passar de US$ 15 (`--cap`). Imagens já geradas não são refeitas; apague o arquivo para regenerar.

## Avaliar

Abra `out/index.html?blind=1` para cada avaliador (nomes de modelo escondidos, colunas embaralhadas por linha). Nota 1–5 de semelhança por imagem; "Exportar notas" copia um JSON. Cole os JSONs no comentário de resolução do ticket, sem as imagens.
