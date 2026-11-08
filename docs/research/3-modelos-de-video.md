# Pesquisa: modelos imagem→vídeo para as Scenes do Final Video

Resolve a issue [#3](https://github.com/victor160997/amorama/issues/3). Data da coleta: **2026-11-07**. Todos os preços são oficiais (páginas de preço/docs dos vendors e dos agregadores fal.ai e Replicate), em USD, lidos nessa data; cada número tem a URL de origem. Onde um fato não pôde ser confirmado em fonte primária, está marcado como **não verificado**.

## Pergunta

Entre os modelos imagem→vídeo acessíveis via API hoje, qual combinação de custo por Scene (5–10 s, 9:16), latência, fidelidade ao frame/personagem de referência e disponibilidade via agregador (fal.ai / Replicate) melhor atende um Final Video de 4–6 Scenes? Recomendar 1 primário e 1 fallback para o tracer bullet de ≤ US$ 30 (4 Scenes de ~5 s + 1 Regeneration).

## Resposta curta

- **Primário: Kling O3 Standard via fal.ai** (`fal-ai/kling-video/o3/standard/reference-to-video` para gerar a Scene direto das duas Character Sheets como *elements*; `fal-ai/kling-video/o3/standard/image-to-video` quando houver um keyframe da Scene). **US$ 0,084/s sem áudio → US$ 0,42 por Scene de 5 s, US$ 0,84 por 10 s.** 9:16 explícito, start+end frame, *elements* com imagem frontal + 1–3 referências por personagem, licença comercial explícita nos termos da API da Kling. Latência observada no fal: ~94 s para 5 s.
- **Fallback: Seedance 1.5 Pro via fal.ai ou Replicate** (`fal-ai/bytedance/seedance/v1.5/pro/image-to-video` / `bytedance/seedance-1.5-pro`). **US$ 0,13 por Scene de 5 s a 720p sem áudio (US$ 0,29 a 1080p).** Vendor diferente (ByteDance), start+end frame, parâmetro `aspect_ratio: 9:16`, mesmo preço nos dois agregadores. Sem multi-referência: exige um keyframe da Scene como imagem inicial.
- **Final Video de 6 Scenes + 1 Regeneration (7 clipes):** primário **US$ 2,94** (5 s) / **US$ 5,88** (10 s) sem áudio; fallback **US$ 0,91** (5 s, 720p) / **US$ 2,03** (5 s, 1080p) / **US$ 4,06** (10 s, 1080p). Tracer bullet (5 clipes de 5 s): **US$ 2,10** no primário, **US$ 0,65–1,45** no fallback. O orçamento de US$ 30 cobre o vídeo com folga; o que sobra é para Character Sheets e keyframes.
- **Latência:** nenhum vendor publica SLA. Observações únicas nas páginas oficiais: Kling O3 Standard ~94 s/5 s (fal), Kling 2.5 Turbo Pro 156 s/5 s (Replicate), Seedance 1.5 Pro 60 s/5 s (Replicate). Seis Scenes em série ficam em ~10–16 min; em paralelo (a fila do fal aceita múltiplas requisições), ~2–5 min. Ambos cabem na meta de Final Video < 20 min após a Approval.

## O que mudou no mercado (importa para o desenho)

Estas mudanças invalidam parte da lista da issue (Runway Gen-4, Veo via Gemini API, Sora):

| Fato | Fonte |
|---|---|
| **OpenAI Sora 2 / Sora 2 Pro e a Videos API foram desligados em 2026-09-24**, "sem API substituta". Páginas no fal e Replicate retornam 404. | https://developers.openai.com/api/docs/deprecations · https://developers.openai.com/api/docs/guides/video-generation |
| **Veo saiu da Gemini API** (veo-3.1-* desligados em 2026-10-22; substituto sugerido: `gemini-omni-1.2-flash`). Veo 3.1 GA só na Google Cloud "Gemini Enterprise Agent Platform" (ex-Vertex), região `us-central1`. | https://aistudio.google.com/docs/deprecations · https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate |
| **fal.ai remove todos os endpoints Veo 3.1 em 2026-11-17** ("Move to a supported model before then"). | https://fal.ai/models/fal-ai/veo3.1/image-to-video · https://fal.ai/models/fal-ai/veo3.1/fast/image-to-video |
| **Runway não está no fal.ai** (busca `keywords=runway` retorna 0); está no Replicate (`runwayml/gen-4.5`, `runwayml/gen4-turbo`). Gen-4 (não turbo) não existe na API; `gen4_aleph`/`gen3a_turbo` desligados em 2026-07-30. Os modelos de vídeo da Runway **não têm multi-referência de personagem nem end frame** (`promptImage` máx. 1, `position: first`). | https://docs.dev.runwayml.com/openapi.json · https://docs.dev.runwayml.com/guides/models/ · https://replicate.com/runwayml |
| Kling: API direta reorganizada (modelo na URL, sem `mode std/pro`; qualidade via `settings.resolution`). Linha atual: 2.5 Turbo, 2.6, O1, 3.0/3.0 Omni/3.0 Turbo, O3, 4.0 (GA 2026-10-28), 4.0 Flash (2026-11-04). 2.1 saiu do mapa e está marcado *deprecated* no fal. | https://kling.ai/document-api/guides/capability-map/video.md · https://fal.ai/models/fal-ai/kling-video/v2.1/pro/image-to-video |
| Seedance: linha 2.5 / 2.0 / 2.0 Fast / 2.0 Mini / 1.5 Pro / 1.0 Pro / 1.0 Pro Fast. **Seedance 2.x não aceita imagens/vídeos de referência com rostos humanos reais** sem verificação da pessoa. | https://docs.byteplus.com/en/docs/modelark/video-generation-tutorial · https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide |
| MiniMax: linha atual "H3"; Hailuo 02/2.3 listados como *legacy* (ainda precificados). Luma: só Ray 3.2 na API; Ray 2 removido do fal (404). | https://platform.minimax.io/docs/guides/models-intro · https://lumalabs.ai/api/pricing |

## Tabela comparativa (clipe 9:16, preço oficial, sem áudio salvo indicação)

Legenda: **5 s / 10 s** = custo de um clipe nessa duração na resolução indicada. "Segue imagem" = o endpoint não tem parâmetro de aspect ratio e herda o da imagem inicial (uma Character Sheet/keyframe 9:16 gera 9:16). Latências são **observações únicas** publicadas nas páginas oficiais, não SLA.

| Modelo (endpoint) | Onde | Preço oficial | 5 s | 10 s | Durações | 9:16 | Referência de personagem | Áudio | Rostos reais / moderação | Licença comercial | Latência publicada |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kling O3 Standard** `fal-ai/kling-video/o3/standard/reference-to-video` e `.../image-to-video` | fal; Runway Dev (`klingO3_*`); direto (`/omni-video`) | US$ 0,084/s sem áudio; 0,112/s com áudio ([fal](https://fal.ai/models/fal-ai/kling-video/o3/standard/reference-to-video); direto 720p 0,084 / 1080p 0,112 [Kling](https://kling.ai/document-api/pricing/base/video.md)) | **0,42** | **0,84** | 3–15 s | `aspect_ratio` 16:9/9:16/1:1 no R2V; I2V segue imagem | start + end frame; **elements** (frontal + 1–3 refs por personagem); até 7 refs+elements, 4 com vídeo ([doc](https://kling.ai/document-api/api/video/3-0-omni/elements.md)) | opcional | sem filtro de rosto documentado na API; ToS exige consentimento/direitos de imagem ([Kling](https://kling.ai/docs/user-policy)); fal `enable_safety_checker` | **API Kling §6.4: "uso comercial não é restrito"** ([termos](https://kling.ai/document-api/guides/protocols/paid-service.md)); badge *Commercial use* no fal | **~94 s para 5 s** (Std) vs ~318 s (Pro) ([fal](https://fal.ai/models/fal-ai/kling-video/o3/standard/image-to-video)) |
| Kling O1 `kwaivgi/kling-o1` / `fal-ai/kling-video/o1/reference-to-video` | Replicate (std 0,084/s); fal (0,112/s); direto | [Replicate](https://replicate.com/kwaivgi/kling-o1) · [fal](https://fal.ai/models/fal-ai/kling-video/o1/reference-to-video) | 0,42 (Replicate) / 0,56 (fal) | 0,84 / 1,12 | 5/10 (3–10 c/ vídeo) | sim (R2V) | start + end; elements ≤ 7 | não | idem Kling | idem Kling | 141 s exemplo (Replicate) |
| **Kling 2.5 Turbo Pro** `fal-ai/kling-video/v2.5-turbo/pro/image-to-video` / `kwaivgi/kling-v2.5-turbo-pro` | fal, Replicate, Runway Dev, direto | US$ 0,07/s ([fal](https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video) · [Replicate](https://replicate.com/kwaivgi/kling-v2.5-turbo-pro)); direto 720p 0,042 / 1080p 0,07 | **0,35** | **0,70** | 5/10 | segue imagem | start + end frame (direto: end frame só em 1080p); **sem multi-referência** | não | idem Kling | idem Kling | 156 s para 5 s (Replicate, exemplo) |
| Kling 2.6 Pro `fal-ai/kling-video/v2.6/pro/image-to-video` / `kwaivgi/kling-v2.6` | fal, Replicate, direto | 0,07/s sem áudio; 0,14/s áudio nativo ([fal](https://fal.ai/models/fal-ai/kling-video/v2.6/pro/image-to-video)) | 0,35 | 0,70 | 5/10 | segue imagem | start + end (fal); sem multi-ref | nativo (1080p) | idem | idem | 131 s (Replicate) |
| Kling 3.0 / 4.0 | fal, Replicate, direto | 3.0 Std 0,084–0,126/s; 4.0 0,157/s 720p, 0,235/s 1080p ([Kling](https://kling.ai/document-api/pricing/base/video.md) · [fal](https://fal.ai/models/kling/v4/image-to-video)) | 0,42–0,79 | 0,84–1,57 | 3–15 / 3–30 | sim | elements, multi-keyframe (4.0: até 10 imagens) | sim | idem | idem | 182–532 s (Replicate) |
| **Seedance 1.5 Pro** `fal-ai/bytedance/seedance/v1.5/pro/image-to-video` / `bytedance/seedance-1.5-pro` | fal, Replicate, BytePlus (`seedance-1-5-pro-251215`) | 720p 0,026/s sem áudio, 0,052 c/ áudio; 1080p 0,06 / 0,12 ([Replicate](https://replicate.com/bytedance/seedance-1.5-pro)); fal: US$ 1,20/1M tokens sem áudio, 2,40 com ([fal](https://fal.ai/models/fal-ai/bytedance/seedance/v1.5/pro/image-to-video)); BytePlus idem ([pricing](https://docs.byteplus.com/en/docs/modelark/model-pricing)) | **0,13 (720p) / 0,29 (1080p)** | 0,26 / 0,58 | 4–12 s | `aspect_ratio` incl. 9:16 | start + end frame; **sem multi-referência** | opcional (`generate_audio`) | bloqueio de rostos reais documentado só para 2.x; 1.x não coberto (não verificado) | badge *Commercial use* (fal); Replicate §5.1; termos BytePlus **não verificados** | 60 s para 5 s (Replicate, exemplo) |
| Seedance 1.0 Pro | fal, Replicate, BytePlus | Replicate 0,06/s 720p, 0,15/s 1080p ([Replicate](https://replicate.com/bytedance/seedance-1-pro)); fal 2,50/1M tokens ≈ 0,27 (720p 5 s) | 0,27–0,30 / 0,61–0,75 | 0,54–0,60 / 1,22–1,50 | 2–12 | sim | start + end | não | idem | idem | 55 s (Replicate) |
| Seedance 2.0 Fast / 2.5 (reference-to-video) | fal, Replicate, BytePlus | fal 0,2419/s 720p (2.0 Fast); 2.5 US 0,473/s 720p ([fal](https://fal.ai/models/bytedance/seedance-2.0/fast/image-to-video)); Replicate 2.0 Fast 0,15/s, 2.5 0,2312/s ([Replicate](https://replicate.com/bytedance/seedance-2.5)). **Preços divergem entre agregadores** | 0,75–1,21 (720p) | 1,50–2,42 | 4–15 / 4–30 | sim | R2V com até 9 (2.0) / 30 (2.5) imagens | sim, sem custo extra | **rejeita refs com rostos reais** sem verificação ([BytePlus](https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide)) | idem | 89–224 s (Replicate) |
| Veo 3.1 Fast `fal-ai/veo3.1/fast/*` / `google/veo-3.1-fast` / `veo-3.1-fast-generate-001` | fal (**até 17/11/2026**), Replicate, Google Cloud Agent Platform | 0,10/s sem áudio, 0,15 c/ áudio ([fal](https://fal.ai/models/fal-ai/veo3.1/fast/image-to-video) · [Replicate](https://replicate.com/google/veo-3.1-fast)); direto 720p 0,08/0,10, 1080p 0,10/0,12 ([Google](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing)) | **só 4/6/8 s**: 4 s = 0,40 | 8 s = 0,80 | 4/6/8 | `aspect_ratio` 9:16 | first + last frame; "ingredients" (`reference_images` ≤ 3; no Replicate só 16:9/8 s; schema do Fast sem o campo) | sim | `personGeneration` `allow_adult`/`disallow`; filtro de celebridades e crianças ([Google](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines)) | Google Cloud terms; C2PA | 62 s para 8 s (Replicate) |
| Veo 3.1 | idem | 0,20/s sem áudio, 0,40 c/ áudio | 4 s = 0,80 | 8 s = 1,60 | 4/6/8 | sim | idem + 4K | sim | idem | idem | 102 s / 8 s |
| Runway Gen-4 Turbo `gen4_turbo` / `runwayml/gen4-turbo` | direto, Replicate (**não no fal**) | 5 créditos/s = US$ 0,05/s ([Runway](https://docs.dev.runwayml.com/guides/pricing/) · [Replicate](https://replicate.com/runwayml/gen4-turbo)) | **0,25** | 0,50 | 2–10 s (int) | `720:1280` | **só primeiro frame; sem end frame, sem refs** | não | `publicFigureThreshold auto/low`; moderação cobra crédito ([Runway](https://docs.dev.runwayml.com/api-details/moderation/)) | ToU §4.4 "não restringe uso comercial"; exige "Powered by Runway" ([ToU](https://runway.com/terms-of-use)) | 25 s para 5 s (Replicate) |
| Runway Gen-4.5 | direto, Replicate | 12 créditos/s = 0,12/s | 0,60 | 1,20 | 2–10 | 720p apenas | só primeiro frame | não | idem | idem | 229 s / 10 s |
| Wan 2.6 i2v flash `wan-video/wan2.6-i2v-flash` / `wan2.6-i2v-flash` | Replicate, DashScope (não no fal) | Replicate 720p 0,05/s, 1080p 0,075 ([Replicate](https://replicate.com/wan-video/wan2.6-i2v-flash)); direto 720p 0,05 c/ áudio, 0,025 sem ([Alibaba](https://www.alibabacloud.com/help/en/model-studio/wan2-6-i2v-flash)) | 0,25 | 0,50 | 5/10/15 | segue imagem | só start frame | sim | moderação genérica (`IPInfringementSuspect`) | Service Agreement §7.5: IP do output é do usuário (texto só em chinês) | 50 s (Replicate); "1–5 min" (Alibaba) |
| Wan 2.7 i2v / r2v | fal, Replicate, DashScope | 0,10/s 720p, 0,15 1080p ([fal](https://fal.ai/models/fal-ai/wan/v2.7/image-to-video)) | 0,50 | 1,00 | 2–15 | r2v: 16:9/9:16/… | start + end; r2v ≤ 5 refs | sim | idem | idem | 225 s i2v, 750 s r2v (Replicate) |
| MiniMax Hailuo 2.3 Std | fal, Replicate, direto | US$ 0,28 por 6 s, 0,56 por 10 s (768p) ([MiniMax](https://platform.minimax.io/docs/pricing) · [fal](https://fal.ai/models/fal-ai/minimax/hailuo-2.3/standard/image-to-video)) | **só 6/10 s**: 6 s = 0,28 | 0,56 | 6/10 | segue imagem | só start frame | não | sem política de rosto publicada | termos da API MiniMax **não verificados** (página JS) | 97 s (Replicate) |
| MiniMax H3-Max (reference-to-video) | fal, direto | 768p 0,08/s (promo 0,056 até 15/11/2026); 1080p 0,16 ([fal](https://fal.ai/models/minimax/h3-max/reference-to-video)) | 0,40 (768p) | 0,80 | 5–15 | `aspect_ratio` 9:16 | até 4 refs quadradas (12 arquivos) | nativo | idem | idem | não publicada |
| Vidu Q2 reference-to-video `fal-ai/vidu/q2/reference-to-video` | fal (Replicate só Q3) | 720p **US$ 0,30 por vídeo** (1–8 s); 1080p 0,20 + 0,10/s ([fal](https://fal.ai/models/fal-ai/vidu/q2/reference-to-video)) | 0,30 | 8 s = 0,30 (máx.) | 1–8 | 16:9/9:16/1:1 | até 7 imagens de referência | só BGM (4 s) | moderação de "public figures" ([Vidu](https://platform.vidu.com/docs/terms-and-policies/content-moderation)) | "We don't restrict your use for commercial purposes" ([Vidu](https://platform.vidu.com/docs/terms-and-policies/terms-of-use)) | não publicada |
| Luma Ray 3.2 | Replicate, fal (`luma/agent/ray/v3.2`), direto | 720p US$ 0,30 / 5 s; 1080p 1,20 / 5 s ([Luma](https://lumalabs.ai/api/pricing)) | 0,30 (720p) | **10 s não suporta start_frame** | 5/10 | 9:16 (1080p vertical "ainda não disponível") | start + end (só 5 s); keyframes | não | ToS: rotular output com pessoas como IA | output do cliente, mas só com assinatura ativa | "bem abaixo de 2 min" para 5 s/720p ([Luma](https://docs.agents.lumalabs.ai/guides/videos/generation)) |
| LTX 2.5 Fast | Replicate (0,03/s 720p), fal (0,09/s) | [Replicate](https://replicate.com/lightricks/ltx-2.5-fast) · [fal](https://fal.ai/models/lightricks/ltx-2.5/image-to-video/fast). **3× de diferença entre agregadores** | 0,15 (Replicate) | 0,30 | 2–20 (fal: ≥ 6) | 16:9/9:16 | start + end | sim | NSFW policy | licença própria LTX | 34 s (Replicate) |
| Sora 2 | — | **descontinuado 2026-09-24** ([OpenAI](https://developers.openai.com/api/docs/deprecations)) | — | — | — | — | — | — | bloqueava rostos reais na entrada | — | — |

Observações sobre a tabela:

- **Áudio não é necessário** para o Final Video (música e legendas entram na montagem), então o custo relevante é sempre o "sem áudio". Em Kling 2.6/3.x/O3 e Seedance 1.5 o áudio dobra ou quase dobra o preço.
- fal e Replicate cobram o mesmo valor para Kling 2.5 Turbo Pro, Kling 2.6, Veo 3.1 e Seedance 1.5 Pro: a troca de agregador é neutra em custo para esses. Para Seedance 2.x e LTX os preços divergem bastante.
- fal: falhas HTTP ≥ 500 não são cobradas; fila e cold start são grátis ([docs](https://fal.ai/docs/model-apis/pricing)). Replicate: "if a run fails, we don't charge you" ([docs](https://replicate.com/docs/topics/billing)). Runway: geração **moderada cobra crédito**.
- A página `fal.ai/pricing` diverge das páginas dos modelos em vários casos (Kling 3.0, PixVerse, Seedance 2.0 Fast). Tratamos a frase de preço na página do modelo como a vigente.

## Fidelidade ao personagem: o que as fontes primárias permitem afirmar

Nenhuma página oficial publica métrica de consistência de identidade; isso só pode ser medido no tracer bullet. O que é verificável é **que mecanismo cada API oferece**:

| Mecanismo | Quem oferece | Implicação para Amorama |
|---|---|---|
| Só primeiro frame | Runway Gen-4 Turbo/4.5, Hailuo 2.3, Wan 2.6 flash, Seedance 1.0 Pro Fast | Exige um **keyframe da Scene** (imagem com o Couple já composto) gerado antes; o vídeo só anima essa imagem. Identidade depende 100% do keyframe. |
| Primeiro + último frame | Kling 2.5 Turbo/2.6/O3/3.0/4.0, Seedance 1.0 Pro/1.5 Pro/2.x, Veo 3.1, Wan 2.7, Luma, LTX, Hailuo 02 | Permite "ancorar" a Scene nas duas pontas e encadear Scenes com continuidade. |
| Multi-imagem de personagem (*elements* / ingredients / reference-to-video) | **Kling O1/O3/3.0 Omni/4.0** (frontal + 1–3 refs por personagem, até 7), Veo 3.1 (≤ 3, com restrições de ratio/duração), Vidu Q2/Q3 (≤ 7), Seedance 2.x (≤ 9/30, **rejeita rostos reais**), Wan 2.7 r2v (≤ 5), H3-Max (≤ 4) | Permite passar **as duas Character Sheets diretamente** e descrever a Scene no prompt, sem keyframe intermediário. É o caminho mais curto do Script à Scene. |

Dado que a Approval do Couple é sobre as Character Sheets, o mecanismo de *elements* é o que melhor liga "o que foi aprovado" a "o que aparece no vídeo". Kling O3 Standard é o único da shortlist que combina *elements*, start/end frame, 9:16 explícito e preço < US$ 0,50 por Scene de 5 s.

## Rostos reais

Os insumos da etapa de vídeo são Character Sheets no House Style (renders 3D), não fotos. Ainda assim:

- **Seedance 2.x** recusa referências com rosto humano real sem verificação da pessoa; pode gerar falsos positivos em renders realistas. 1.x não tem a restrição documentada.
- **Veo 3.1** bloqueia celebridades e crianças por padrão (`personGeneration: allow_adult`); **Runway** tem `publicFigureThreshold` e cobra gerações moderadas; **fal** proíbe uso de imagem de terceiros sem consentimento ([AUP](https://fal.ai/legal/acceptable-use-policy)); **Kling** exige consentimento e direitos de imagem nos termos.
- Em todos os casos o Couple fornece as próprias fotos e consente, então o risco é de **moderação falso-positiva**, não de violação de política. Falso-positivo = Regeneration; por isso fal/Replicate (que não cobram falha) são preferíveis ao Runway direto para esse cenário.

## Licença comercial (resumo)

| Caminho | Base |
|---|---|
| fal.ai | Badge *Commercial use* em todos os endpoints da shortlist; ToS (2026-09-08) não reivindica IP sobre o output, uso "por conta e risco do cliente" ([ToS](https://www.fal.ai/legal/terms-of-service) · [FAQ](https://fal.ai/docs/documentation/model-apis/faq)) |
| Replicate | Termos §5.1: cede ao usuário todo direito sobre o output, incl. uso comercial, "sujeito aos termos de terceiros" do modelo ([terms](https://replicate.com/terms)) |
| Kling (direto) | API Paid Service Terms §6.3–6.4: IP do output é do usuário; uso comercial não restrito ([termos](https://kling.ai/document-api/guides/protocols/paid-service.md)) |
| ByteDance/BytePlus | **não verificado** em fonte primária (termos deferem ao "model service agreement") |
| Runway | Não restringe uso comercial, mas exige atribuição "Powered by Runway" em apps voltados a usuários finais e usa inputs/outputs para treino ([ToU](https://runway.com/terms-of-use)) |
| Google (Agent Platform) | Google Cloud terms; output com Content Credentials (C2PA) |
| Luma | Output pertence ao cliente, só com assinatura ativa ([ToS](https://lumalabs.ai/legal/tos)) |

## Recomendação para o tracer bullet

**Primário: Kling O3 Standard no fal.ai**

- Endpoints: `fal-ai/kling-video/o3/standard/reference-to-video` (duas Character Sheets como `elements`, `aspect_ratio: "9:16"`, `duration: 5`, `generate_audio: false`) e `fal-ai/kling-video/o3/standard/image-to-video` (quando houver keyframe + `end_image_url`).
- Custo: **US$ 0,42 por Scene de 5 s; US$ 0,84 por 10 s.** Tracer bullet (4 Scenes + 1 Regeneration): **US$ 2,10**.
- Latência observada: ~94 s por clipe de 5 s. Seis Scenes em série ≈ 9–10 min; em paralelo ≈ 2–3 min.
- Troca de modelo sem reescrever código: mesmo schema de `elements` em `fal-ai/kling-video/o1/reference-to-video` (US$ 0,112/s), `o3/pro` (US$ 0,112/s), `kling/v4/reference-to-video` (US$ 0,157/s); no Replicate, `kwaivgi/kling-o1` (US$ 0,084/s) e `kwaivgi/kling-v3-omni-video`.
- Por que não Kling 2.5 Turbo Pro (US$ 0,35)? É US$ 0,07 mais barato e muito mais usado, mas não aceita *elements*: exigiria um keyframe por Scene. Fica como alternativa se os *elements* não entregarem consistência no teste.

**Fallback: Seedance 1.5 Pro (fal.ai ou Replicate, mesmo preço)**

- Endpoints: `fal-ai/bytedance/seedance/v1.5/pro/image-to-video` ou `bytedance/seedance-1.5-pro` com `aspect_ratio: "9:16"`, `resolution: "1080p"`, `generate_audio: false`, `image_url` + `end_image_url` opcional.
- Custo: **US$ 0,13 (720p) / 0,29 (1080p) por Scene de 5 s; 0,26 / 0,58 por 10 s.** Tracer bullet: US$ 0,65–1,45.
- Vendor independente da Kling (cobre indisponibilidade), start+end frame, latência observada ~60 s/5 s. Sem multi-referência: usa o fluxo keyframe → vídeo. Modelos 1.x não têm o bloqueio de rosto real da linha 2.x.

**Descartados e por quê:** Veo 3.1 (sai do fal em 10 dias, sem duração de 5/10 s, só via Google Cloud `us-central1`); Runway (não está no fal, sem end frame nem refs, 720p apenas, cobra moderação, atribuição obrigatória); Sora 2 (descontinuado); Seedance 2.x (2–3× o custo e bloqueio de rosto real); Hailuo 2.3 (só 6/10 s, só start frame); Luma Ray 3.2 (10 s sem start frame, 9:16 1080p indisponível); Vidu Q2 (barato e com 7 refs, mas máximo 8 s, só no fal, latência não publicada; candidato a 2º fallback se Seedance falhar); H3-Max (novo demais, preço promocional).

## Custo projetado do Final Video (6 Scenes + 1 Regeneration = 7 clipes, sem áudio)

| Cenário | 5 s por Scene | 10 s por Scene |
|---|---|---|
| Primário Kling O3 Standard (fal) | **US$ 2,94** | **US$ 5,88** |
| Primário com áudio nativo (se quisermos testar) | US$ 3,92 | US$ 7,84 |
| Fallback Seedance 1.5 Pro 720p | US$ 0,91 | US$ 1,82 |
| Fallback Seedance 1.5 Pro 1080p | US$ 2,03 | US$ 4,06 |
| Alternativa Kling 2.5 Turbo Pro | US$ 2,45 | US$ 4,90 |

Mesmo o pior caso (O3 Standard, 10 s, áudio) fica em US$ 7,84 por Final Video só de vídeo. O orçamento de US$ 30 do tracer bullet é dominado por outras etapas (Character Sheets, keyframes, Regenerations de imagem), não pelo vídeo.

## Lacunas (não verificáveis em fonte primária hoje)

1. Nenhum vendor publica latência típica ou SLA; os números acima são exemplos únicos nas páginas oficiais.
2. Qualidade/consistência de identidade entre Scenes: só mensurável no tracer bullet.
3. Resolução de saída do Kling 2.5 Turbo Pro e O1 não é declarada nas páginas do fal/Replicate (direto: 720p ou 1080p por `settings.resolution`; o preço US$ 0,07/s dos agregadores coincide com o tier 1080p do direto).
4. Termos comerciais da BytePlus (Seedance direto) e da API MiniMax (página só em JS).
5. Veo 3.1: número máximo de imagens de referência na fonte oficial (Replicate diz 3); SynthID não aparece mais nas páginas atuais (só C2PA).
6. Preço dos pacotes mínimos da API direta da Kling (renderizado client-side); o fal cobra pay-as-you-go, o que elimina essa barreira.

## Fontes consultadas (principais)

- fal.ai: páginas dos modelos listados acima; https://fal.ai/pricing ; https://fal.ai/docs/model-apis/pricing ; https://www.fal.ai/legal/terms-of-service ; https://fal.ai/legal/acceptable-use-policy
- Replicate: páginas dos modelos listados acima; https://replicate.com/terms ; https://replicate.com/docs/topics/billing ; https://replicate.com/docs/topics/models/official-models
- Kling: https://kling.ai/document-api/pricing/base/video.md ; https://kling.ai/document-api/guides/capability-map/video.md ; https://kling.ai/document-api/api/video/3-0-omni/elements.md ; https://kling.ai/document-api/api/video/2-5-turbo/image-to-video.md ; https://kling.ai/document-api/guides/protocols/paid-service.md
- Google: https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing ; https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate ; https://aistudio.google.com/docs/deprecations ; https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines
- Runway: https://docs.dev.runwayml.com/guides/pricing/ ; https://docs.dev.runwayml.com/openapi.json ; https://docs.dev.runwayml.com/api-details/moderation/ ; https://runway.com/terms-of-use
- ByteDance: https://docs.byteplus.com/en/docs/modelark/model-pricing ; https://docs.byteplus.com/en/docs/modelark/video-generation-tutorial ; https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide
- MiniMax: https://platform.minimax.io/docs/pricing ; https://platform.minimax.io/docs/api-reference/video-generation-v2-create
- Alibaba: https://www.alibabacloud.com/help/en/model-studio/video-generation ; https://www.alibabacloud.com/help/en/model-studio/wan2-6-i2v-flash ; https://www.alibabacloud.com/help/en/model-studio/image-to-video-api-reference
- Vidu: https://platform.vidu.com/docs/overview/pricing ; https://platform.vidu.com/docs/terms-and-policies/terms-of-use
- Luma: https://lumalabs.ai/api/pricing ; https://docs.agents.lumalabs.ai/guides/videos/generation ; https://lumalabs.ai/legal/tos
- OpenAI: https://developers.openai.com/api/docs/deprecations ; https://developers.openai.com/api/docs/guides/video-generation
