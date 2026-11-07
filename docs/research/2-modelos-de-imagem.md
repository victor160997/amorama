# Pesquisa: modelos de imagem para semelhança e consistência de personagem

- **Ticket:** [Pesquisa: modelos de imagem para semelhança e consistência de personagem](https://github.com/victor160997/amorama/issues/2) (filho do mapa wayfinder)
- **Data da pesquisa:** 2026-11-07. Todos os preços e limites abaixo foram lidos nas páginas oficiais nessa data; modelos de imagem mudam de preço e de nome com frequência, então reverifique antes de comprometer orçamento.
- **Fontes:** só páginas primárias (docs e preços dos fornecedores, páginas de modelo no fal.ai e no Replicate, arquivos de licença no Hugging Face/GitHub). Cada afirmação traz a URL onde foi vista. O que não foi possível confirmar em fonte primária está marcado **[não verificado]**.

## Resumo e recomendação

Para gerar **Character Sheets** com semelhança facial a partir de 2+ fotos e reutilizá-las como referência em várias **Scenes** no **House Style**, a categoria que vence hoje é a de **modelos nativos de edição com múltiplas referências** (passa-se as fotos e um prompt; sem treino, sem adapter). Eles aceitam de 10 a 16 imagens de referência, documentam consistência de personagem, custam US$ 0,03–0,05 por imagem e, nos três casos escolhidos, documentam duas ou mais pessoas distintas na mesma imagem.

Candidatos para o teste comparativo de ~US$ 15 (mesmas fotos, mesmo prompt de House Style):

| # | Modelo | Via | Custo/imagem (1K) | Por que |
|---|---|---|---|---|
| 1 | **Nano Banana 2.1** (`gemini-nano-banana-2.1`, Google) | Gemini API direto (ou fal.ai / Replicate) | **US$ 0,0336** direto e Replicate; US$ 0,040 no fal.ai | Único com limite documentado pelo fornecedor de **até 4 personagens consistentes** por imagem e 14 referências; mais barato dos três; "person generation: supported". |
| 2 | **FLUX 3 Image** (Black Forest Labs) | BFL API direto ou fal.ai (US$ 0,048); Replicate US$ 0,024 | **US$ 0,048** (tier 1K) | Até 10 referências sem cobrança extra; docs mostram exemplo de "casal" e de pessoas de duas imagens compostas juntas; licença comercial plena via API. |
| 3 | **Seedream 5.0 Pro** (ByteDance) | Replicate (US$ 0,045) ou BytePlus ModelArk direto (US$ 0,045 + US$ 0,003 por imagem de entrada extra) | **US$ 0,045** (≤1.5K) | Única família com afirmação oficial explícita de **fusão de rostos de várias pessoas** em uma cena preservando a identidade de cada uma; 10 referências. |

Controle opcional (sobra orçamento): **Qwen-Image-Edit-2511** (Alibaba, Apache 2.0, US$ 0,03/imagem no fal.ai e Replicate), o único candidato de pesos abertos com licença comercial sem ressalvas e com afirmação explícita de "fusão de duas pessoas em uma foto de grupo". Não entrou no trio porque trabalha melhor com 1–3 imagens de entrada, o que limita o uso direto de 2+ fotos por pessoa.

O que foi **descartado** e por quê está na seção "Descartados". Em resumo: adapters de FaceID (PuLID, InstantID, IP-Adapter FaceID, PhotoMaker, InfiniteYou) dependem de modelos InsightFace **não comerciais** e só suportam um rosto; LoRA por pessoa custa US$ 2–6,40 de treino por pessoa por Order e a combinação de dois LoRAs não tem comportamento documentado; GPT Image 2.5/2.6 não publica preço por imagem e a própria documentação avisa que pode falhar em consistência de personagem recorrente; Runway Gen-4 Image treina com os inputs do cliente fora do plano Enterprise e exige "Powered by Runway"; Ideogram Character aceita 1 referência e 1 personagem.

## Critérios usados

Derivados da pergunta do ticket e do GLOSSARY:

1. **Semelhança** do Character Sheet com a pessoa a partir de 2+ fotos (zero-shot, sem treino por Order).
2. **Consistência** da identidade quando o Character Sheet aprovado vira referência de várias Scenes.
3. **Duas identidades distintas** na mesma imagem (o Couple sempre tem exatamente duas pessoas).
4. **Custo por imagem** e **latência** (relevante para Regeneration e para o Concierge Mode).
5. **Licença de uso comercial** dos outputs, e cláusulas sobre fotos de pessoas reais.
6. **Acesso via API** (fal.ai, Replicate ou direto).

## Panorama: quatro mecanismos de referência de identidade

| Mecanismo | Como funciona | Estado em 2026-11 | Veredito para Amorama |
|---|---|---|---|
| **Edição nativa multi-referência** | O modelo recebe N fotos + prompt e gera/edita preservando o que é "sujeito" | Padrão da indústria: Google Nano Banana 2.x/Pro, BFL FLUX 3 Image / FLUX.2, ByteDance Seedream 4.x/5.x, Alibaba Qwen-Image-Edit, OpenAI GPT Image 2.x | **Escolhido.** Zero-shot, barato, aceita várias pessoas. |
| **Adapters de rosto (IP-Adapter FaceID, InstantID, PuLID, PhotoMaker, InfiniteYou)** | Um encoder facial (InsightFace) injeta a identidade num modelo base SD/FLUX | Vários endpoints descontinuados no fal.ai; base SDXL/FLUX.1 | **Descartado.** Pesos InsightFace são "non-commercial research only"; um rosto por imagem. |
| **Fine-tune LoRA por pessoa** | Treina-se um LoRA com 10–20 fotos; inferência com o LoRA carregado | fal.ai (FLUX.1: US$ 2/treino; FLUX.2 dev: US$ 6,40/1000 passos), Replicate (~US$ 1,46–2/treino) | **Plano B.** Caro e lento por Order (dois treinos); mistura de dois LoRAs sem documentação de qualidade. |
| **Modelos de "personagem" com referência única** | Uma imagem define o personagem (Ideogram Character, Runway Gen-4 References) | Vivos, mas 1–3 referências | **Descartado** para Character Sheet; Ideogram 4.5 (5 refs) poderia voltar como alternativa se o trio falhar. |

## Fichas dos candidatos

### 1. Nano Banana 2.1 — `gemini-nano-banana-2.1` (Google)

- **Status:** lançado 2026-10-06 (GA no Vertex), recomendado pela Google como padrão para novos projetos; `gemini-3.1-flash-image` (Nano Banana 2) é o antecessor estável e `gemini-2.5-flash-image` é legado com desligamento em 2027-03-15. Fontes: https://aistudio.google.com/docs/models · https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/nano-banana-2-1 · https://aistudio.google.com/docs/pricing
- **Mecanismo:** edição nativa multi-referência. "Multi-image fusion supports up to 14 reference images, with character consistency for up to 4 characters and object fidelity for up to 10 objects." Fonte: https://aistudio.google.com/docs/models/gemini-nano-banana-2.1 e https://aistudio.google.com/docs/image-generation (seção Limitations: "support character resemblance of up to 4 characters").
- **Duas pessoas distintas:** sim, limite documentado de 4 personagens. É o único dos candidatos com número oficial.
- **Custo (1K = 1024²):**
  - Gemini API direto: saída de imagem US$ 30/1M tokens; "1120 tokens … equivalent to **$0.0336 per image**" (1K), US$ 0,0504 (2K), US$ 0,113 (4K). Batch: metade. Entrada US$ 1,50/1M tokens. Fonte: https://aistudio.google.com/docs/pricing
  - Vertex AI: mesmos valores efetivos. Fonte: https://cloud.google.com/model-garden/pricing
  - fal.ai (`google/nano-banana-2.1` e `/edit`): cobrança por token, "representative costs" US$ 0,040 (1K), US$ 0,059 (2K), US$ 0,134 (4K); edição com duas entradas 1K ≈ US$ 0,044; "each input image adds about $0.002". Fonte: https://fal.ai/models/google/nano-banana-2.1/edit
  - Replicate (`google/nano-banana-2.1`): US$ 0,0336 (1K), US$ 0,0504 (2K), US$ 0,1134 (4K). Fonte: https://replicate.com/google/nano-banana-2.1
- **Latência:** nenhum número oficial; a Google diz apenas "Flash-level speed". **[não verificado]**. Para referência, o irmão Nano Banana 2 Lite anuncia "sub-2 second" (https://aistudio.google.com/docs/models/gemini-3.1-flash-lite-image).
- **Licença / pessoas reais:** Gemini API Terms (vigência 2026-03-23): a Google não reivindica propriedade do conteúdo gerado; uso é para fins profissionais/comerciais; em serviços pagos os prompts não são usados para treinar. Fonte: https://aistudio.google.com/docs/terms. A Generative AI Prohibited Use Policy proíbe personificação enganosa e violação de privacidade, sem proibir fotos de pessoas reais como referência. Fonte: https://policies.google.com/terms/generative-ai/use-policy. Docs: "Make sure you have the necessary rights to any images you upload"; **todas as imagens carregam marca d'água invisível SynthID** e credenciais C2PA. Fonte: https://aistudio.google.com/docs/image-generation. Filtros de segurança incluem categorias "Celebrity" e "People/Face"; no Vertex há `personGeneration` (ALLOW_ADULT etc.) e `prominentPeople`. Fonte: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-responsible-ai
- **Alternativa cara na mesma família:** Nano Banana Pro (`gemini-3-pro-image`), US$ 0,134/imagem (1K/2K) direto, US$ 0,15 no fal.ai/Replicate; "up to 5 character images" e "consistency and resemblance of up to 5 people". Fontes: https://aistudio.google.com/docs/pricing · https://blog.google/innovation-and-ai/products/nano-banana-pro/. Vale como "teto de qualidade" no teste se o 2.1 decepcionar na semelhança.

### 2. FLUX 3 Image (Black Forest Labs)

- **Status:** lançado 2026-10-01, "single endpoint for generation and editing … up to ten references"; a BFL marca FLUX.1 Kontext como "legacy editing model". Fontes: https://docs.bfl.ai/release-notes.md · https://docs.bfl.ai/api-reference/models/edit-or-create-an-image-with-flux1-kontext-[pro].md
- **Mecanismo:** edição nativa multi-referência, "takes 1 to 10 entries in `images`". Guia de multi-referência: "keep a character consistent across variations"; papel "Subject = a person, animal, or character to keep recognizable"; exemplo "Place the couple from image 2 at the table in image 4". Fontes: https://docs.bfl.ai/guides/prompting_editing_multi_reference.md · https://docs.bfl.ai/flux_3/flux3_image_generate.md · https://docs.bfl.ai/flux_3/flux3_image_layout.md
- **Duas pessoas distintas:** sim, qualitativamente (exemplos de casal e de "people from image 1 and image 2 posing together" no guia de composição do FLUX.2: https://docs.bfl.ai/guides/usecases_editing_multi_image_compositing). Sem número máximo de personagens documentado.
- **Custo:** por tier de resolução, referências não cobradas.
  - BFL API direto: 768² US$ 0,041; **1K US$ 0,048**; 1.5K US$ 0,07; 2K US$ 0,10; 4K US$ 0,607. Fonte: https://bfl.ai/pricing (regras de arredondamento: https://docs.bfl.ai/quick_start/pricing.md)
  - fal.ai (`fal-ai/flux-3-image` e `/edit`): "A 1K (1 MP) image costs $0.048". Fonte: https://fal.ai/models/fal-ai/flux-3-image/edit
  - Replicate (`black-forest-labs/flux-3-image`): US$ 0,0205 (768), **US$ 0,024 (1K)**, US$ 0,035 (1.5K), US$ 0,05 (2K), US$ 0,3035 (4K), cerca de metade da tabela da BFL. Fonte: https://replicate.com/black-forest-labs/flux-3-image. A razão da diferença não foi encontrada **[não verificado]**; vale testar no Replicate e confirmar a cobrança real.
- **Latência:** sem número oficial **[não verificado]**; schema avisa "4k can take several minutes". Para comparação, FLUX.1 Kontext [pro] anuncia 5–6 s (https://docs.bfl.ai/kontext/kontext_overview.md).
- **Licença / pessoas reais:** API inclui direitos comerciais plenos: "all usage includes full commercial rights with no separate license" (https://help.bfl.ai/articles/9272590838-self-serve-dev-license-overview-pricing); Developer ToS §3(b) "you own all right, title, and interest in and to Output" (https://bfl.ai/legal/developer-terms-of-service). **Atenção operacional:** o mesmo ToS proíbe "Upload images of individuals … without their consent" (§6(j)), imagens de menores de 18 (§6(k)) e exige "informed, documented consent" da pessoa retratada cobrindo o uso e a distribuição do output (§9(a)). Para Amorama isso significa um consentimento explícito do Couple no fluxo do Order, registrado. Usage Policy: https://bfl.ai/legal/usage-policy
- **Alternativas na mesma família:** FLUX.2 [pro] (US$ 0,03 primeiro MP + US$ 0,015 por MP de referência; até 8 referências via API; guia de consistência de personagem com exemplo de casal: https://docs.bfl.ai/guides/usecases_editing_character_consistency.md; preço https://bfl.ai/pricing) e FLUX.2 [klein] 4B (Apache 2.0, US$ 0,014, mas só 4 referências e sem afirmação de identidade). FLUX 3 Image Klein (pesos abertos, US$ 0,009/1K direto) está sob a "FLUX Kommunity License", comercial só para receita anual < US$ 5M (https://huggingface.co/black-forest-labs/flux-3-image-klein/blob/main/LICENSE.md); ainda não está no fal.ai nem no Replicate.

### 3. Seedream 5.0 Pro (ByteDance)

- **Status:** lançado 2026-07-08. A família tem 4.0 (US$ 0,03), 4.5 (US$ 0,04), 5.0 Lite (US$ 0,035), 5.0 Flash (US$ 0,018–0,027) e 5.0 Pro. Fonte: https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro
- **Mecanismo:** edição nativa multi-referência, até 10 imagens de entrada. A única afirmação oficial explícita de identidade multi-pessoa de toda a pesquisa: a fusão "extracts each person's facial features and combines them into a single scene in specified positions" (exemplo com 6 entradas e 5 pessoas). Fonte: blog acima. Replicate: referências "keep a character, product, or style consistent across generations" e "blend multiple subjects into one scene". Fonte: https://replicate.com/bytedance/seedream-5-pro
- **Duas pessoas distintas:** sim, explícito.
- **Custo:**
  - Replicate (`bytedance/seedream-5-pro`): **1K US$ 0,045**; 2K US$ 0,09. Fonte: https://replicate.com/bytedance/seedream-5-pro
  - BytePlus ModelArk direto (`dola-seedream-5-0-pro-260628`): US$ 0,045/imagem (≤1.5K), US$ 0,09 acima; primeira imagem de entrada grátis, "From the second image: $0.003"; imagens barradas pela moderação não são cobradas. Fonte: https://ai.byteplus.com/ark/region:ap-southeast-1/docs/model-pricing
  - fal.ai (`bytedance/seedream/v5/pro/edit`): "Tentative pricing is $0.0675 + $(0.0045 x number of additional input images)" (≤1536²), o dobro acima. Fonte: https://fal.ai/models/bytedance/seedream/v5/pro/edit. Mais caro que Replicate/BytePlus; preferir Replicate no teste.
- **Latência:** o exemplo em destaque no Replicate registra 177 s (2K) — amostra única, não benchmark **[não verificado como típico]**. Seedream 4.5 no fal.ai anuncia "~60 seconds"; Seedream 4 ≈ 14 s (https://replicate.com/blog/compare-image-editing-models). Se a latência do Pro for impeditiva, o substituto é **Seedream 5.0 Lite** (US$ 0,035, 10–14 referências, "complex scenes featuring multiple characters": https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite).
- **Licença / pessoas reais:** modelo fechado. No fal.ai: "Commercial use permitted under partner agreement"; no Replicate os Terms §5.1 cedem ao cliente todo direito sobre o output, inclusive comercial, sujeito aos termos do modelo (https://replicate.com/terms). Os "General Terms for AI Services" da BytePlus não puderam ser lidos (página renderizada em JS) **[não verificado]**; o Customer Code of Conduct da ModelArk exige que plataformas que usam ativos de pessoas reais "review and retain authorization" (https://docs.byteplus.com/en/docs/ModelArk/2353368). Parâmetros: `watermark` (marca visível "AI-generated", padrão true na API BytePlus — desligar) e `enable_safety_checker` (padrão true). Fonte: https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api

### Controle opcional: Qwen-Image-Edit-2511 (Alibaba)

- **Mecanismo:** multi-referência, "works best with 1 to 3 input images"; "character consistency has been significantly improved"; "high-fidelity fusion of two separate person images into a coherent group shot". Fontes: https://huggingface.co/Qwen/Qwen-Image-Edit-2511 · https://replicate.com/qwen/qwen-image-edit-2511
- **Custo:** US$ 0,03 por megapixel no fal.ai (`fal-ai/qwen-image-edit-2511`) e US$ 0,03 por imagem no Replicate. Fontes: https://fal.ai/models/fal-ai/qwen-image-edit-2511 · https://replicate.com/qwen/qwen-image-edit-2511
- **Latência:** exemplo no Replicate 4,5 s.
- **Licença:** pesos **Apache 2.0** (https://github.com/QwenLM/Qwen-Image/blob/main/LICENSE), portanto comercial e auto-hospedável. Atenção: os sucessores Qwen-Image-2.1 e 3.0 **não** são Apache (Qwen Research License, não comercial: https://huggingface.co/Qwen/Qwen-Image-2.1/blob/main/LICENSE).
- **Por que é controle e não titular:** o limite prático de 3 entradas obriga a um fluxo em dois passos (Character Sheet por pessoa a partir de 2–3 fotos; depois Scene a partir dos 2 Character Sheets). Esse fluxo é exatamente o de Amorama, então o modelo pode se sair bem; mas os três titulares fazem isso e ainda aceitam as fotos originais junto.

## Descartados (e por quê)

| Modelo / abordagem | Motivo principal | Fonte |
|---|---|---|
| **GPT Image 2.5 / 2.6 Sunburst e Flare** (OpenAI) | Até 16 referências e fidelidade alta sempre ativa, mas (a) preço por imagem não publicado para 2.5/2.6 (só calculadora interativa; no Replicate, 2.6 Sunburst sai US$ 0,05 low / US$ 0,09 medium / US$ 0,128 high); (b) a própria documentação avisa que o modelo "may occasionally struggle to maintain visual consistency for recurring characters"; (c) `gpt-image-1` foi desligado em 2026-10-23 e 1.5/mini são desligados em 2026-12-01. Fica como 4º opcional se houver orçamento. | https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/docs/pricing · https://developers.openai.com/api/docs/deprecations · https://replicate.com/openai/gpt-image-2.6-sunburst |
| **Runway Gen-4 Image / Turbo** | Barato (US$ 0,02–0,08) e até 3 referências com @tags, mas os Terms (2026-10-23) dizem que "Inputs and Outputs may be used by the Company to train" fora do Enterprise e exigem "Powered by Runway" visível no app. Fotos íntimas de um Couple não devem alimentar treino de terceiros. | https://docs.dev.runwayml.com/guides/pricing/ · https://runway.com/terms-and-conditions · https://dev.runwayml.com/learn/commercial-use |
| **Ideogram Character / Ideogram 4.5** | Character: 1 referência, 1 personagem, US$ 0,10–0,20. 4.5: até 5 referências e US$ 0,06 (medium), comercial OK, mas nenhuma página afirma consistência de dois personagens; API Agreement exige identificar o output como gerado pelo modelo ("Powered by Ideogram"). | https://developer.ideogram.ai/api-reference/api-reference/generate-v3 · https://ideogram.ai/models/4.5/ · https://ideogram.ai/legal/api-tos/ |
| **PuLID, InstantID, IP-Adapter FaceID, PhotoMaker V2, InfiniteYou** | Todos dependem de modelos faciais InsightFace, cujo model zoo diz "ALL models are available for non-commercial research purposes only"; IP-Adapter FaceID e InfiniteYou são explicitamente não comerciais; InstantID e InfiniteYou usam só o maior rosto; nenhum endpoint vivo expõe duas identidades. Vários estão descontinuados no fal.ai. | https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md · https://huggingface.co/h94/IP-Adapter-FaceID · https://github.com/instantX-research/InstantID · https://huggingface.co/ByteDance/InfiniteYou · https://fal.ai/models/fal-ai/flux-pulid |
| **LoRA por pessoa** (FLUX.1/FLUX.2) | Treino: fal.ai US$ 2/treino (FLUX.1, 1000 passos), US$ 2,40 (portrait trainer), US$ 6,40 (FLUX.2 dev), US$ 4,30 (FLUX.2 klein 9B); Replicate ≈ US$ 1,46–2 e ~2 min. Inferência US$ 0,021–0,035/MP. Dois LoRAs podem ser combinados (fal `loras` até 3 no FLUX.2; Replicate `extra_lora`), mas nenhuma plataforma documenta qualidade/vazamento de identidade entre duas pessoas **[não verificado]**. Por Order: 2 treinos ≈ US$ 4–13 contra ≈ US$ 0,10 no zero-shot. Fica como plano B se o zero-shot não atingir semelhança aceitável. Base FLUX.1/2 [dev] é não comercial, mas outputs gerados no fal.ai/Replicate são liberados para uso comercial segundo as próprias plataformas. | https://fal.ai/models/fal-ai/flux-lora-fast-training · https://fal.ai/models/fal-ai/flux-2-trainer · https://fal.ai/models/fal-ai/flux-2/lora · https://replicate.com/docs/get-started/fine-tune-with-flux · https://replicate.com/black-forest-labs/flux-dev-lora · https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md |
| **Gemini 2.5 Flash Image (Nano Banana original)** | Legado; só 3 imagens de entrada; "Person generation: Not supported" no Vertex; desligamento em 2027-03-15. | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image |
| **FLUX.1 Kontext [pro]/[max]** | Marcados "legacy" pela BFL; multi-referência "experimental" com até 4 imagens. | https://docs.bfl.ai/api-reference/models/edit-or-create-an-image-with-flux1-kontext-[pro].md |

## Notas transversais de licença

- **Plataformas:** no Replicate, os Terms (2026-04-01) §5.1 cedem ao cliente o output, inclusive para uso comercial, sujeito aos termos do modelo (https://replicate.com/terms). No fal.ai, os Terms (2026-09-08) não atribuem o output expressamente; a permissão comercial se apoia no selo "Commercial use" de cada página de modelo e os "Third-Party Materials" podem ter termos próprios (https://fal.ai/terms). A AUP do fal.ai proíbe usar "another person's name, image, voice, or other likeness without their consent" (https://fal.ai/legal/acceptable-use-policy). Em ambos, **a licença do modelo governa**.
- **Consentimento:** BFL (Developer ToS §6(j), §9(a)), Alibaba Model Studio (Product Terms 4.48.1(b)), BytePlus (Code of Conduct §2.6), Runway e Ideogram exigem consentimento das pessoas retratadas. Amorama precisa de um aceite explícito do Couple (ambos adultos, fotos próprias) registrado no Order. Isso deve virar requisito do fluxo de upload, independentemente do modelo escolhido.
- **Marca d'água:** Google aplica SynthID invisível em tudo; Seedream tem marca visível opcional (desligar via `watermark=false`); OpenAI aplica C2PA. Nenhuma impede uso comercial.
- **Treinamento com dados do cliente:** Google (serviços pagos), Ideogram e Replicate declaram não treinar com inputs/outputs; Runway declara que pode. **[não verificado]** para BytePlus/Seedream (termos não legíveis).

## Plano de teste comparativo (~US$ 15)

**Objetivo:** escolher o modelo que gera o Character Sheet e as imagens-chave de Scene (stills de referência). A geração de vídeo das Scenes a partir dessas imagens é outro ticket.

**Entradas fixas (iguais para todos os modelos):**
- 2 casais voluntários da equipe (adultos, com consentimento por escrito), 3 fotos por pessoa: rosto frontal, 3/4 e corpo inteiro, luz natural, sem óculos escuros. Total 12 fotos.
- 1 prompt de House Style (abaixo), 4 descrições de Scene com poses/enquadramentos distintos (ex.: os dois sentados num café rindo; caminhando de mãos dadas na praia ao pôr do sol; dançando na sala; plano médio com um sussurrando no ouvido do outro), em 9:16.
- Resolução 1K em todos (para igualar custo e tempo).

**Prompt base de House Style (sem nomes de estúdio):**

> "Stylized 3D animated character render in a warm, cinematic family-film look: soft rounded facial features, slightly enlarged expressive eyes, smooth subsurface skin, simplified clean clothing folds, gentle rim light, pastel color palette, shallow depth of field, 9:16 portrait. Keep the exact facial structure, skin tone, hair style and color, eye shape, and body proportions of the person in the reference photos so that friends would recognize them."

Para Scenes com os dois: acrescentar "Use the two reference images as two different people; do not blend their faces; person A on the left, person B on the right" e a descrição da Scene.

**Fases e volume por modelo (30 imagens cada):**

| Fase | O que gera | Imagens/modelo |
|---|---|---|
| A. Character Sheet | Por pessoa: 3 fotos → 4 gerações (seeds/variações) com o prompt de House Style | 4 pessoas × 4 = 16 |
| B. Scene com duas identidades | Por casal: os 2 melhores Character Sheets da fase A (+ opcionalmente as fotos) → 4 Scenes | 2 casais × 4 = 8 |
| C. Regeneration | Pedir 3 edições sobre uma Scene da fase B (trocar roupa, mudar expressão, mudar fundo) em um casal, e 3 no outro | 6 |

**Orçamento estimado (1K):**

| Modelo | Via | 30 imagens |
|---|---|---|
| Nano Banana 2.1 | Gemini API direto (US$ 0,0336) | ≈ US$ 1,01 (fal.ai ≈ US$ 1,30) |
| FLUX 3 Image | BFL/fal.ai (US$ 0,048) | ≈ US$ 1,44 (Replicate ≈ US$ 0,72) |
| Seedream 5.0 Pro | Replicate (US$ 0,045) | ≈ US$ 1,35 |
| **Subtotal trio** | | **≈ US$ 3,80** |
| Opcional: Qwen-Image-Edit-2511 | fal.ai/Replicate (US$ 0,03) | ≈ US$ 0,90 |
| Opcional: Nano Banana Pro só nas fases A+B (24 img) como teto de qualidade | Gemini API (US$ 0,134) | ≈ US$ 3,22 |
| Reserva para iteração de prompt, refações e falhas | | ≈ US$ 5,00 |
| **Total** | | **≈ US$ 13–14**, dentro dos US$ 15 |

**Critérios de comparação (avaliação cega, escala 1–5, três avaliadores: as duas pessoas retratadas + 1 pessoa neutra que conhece o casal):**

1. **Semelhança** do Character Sheet: "você reconheceria essa pessoa?" (critério eliminatório: média < 3 descarta o modelo).
2. **Estabilidade** da identidade nas 4 Scenes: o mesmo rosto em todas? Variação de formato de rosto, nariz, cabelo.
3. **Integridade de duas identidades:** zero mistura ou troca de traços entre as duas pessoas (contar ocorrências; qualquer troca é falha grave).
4. **Aderência ao House Style:** o look 3D é consistente entre pessoas e Scenes, sem cair em fotorrealismo.
5. **Artefatos:** mãos, olhos, dentes, texto espúrio, marca d'água visível.
6. **Operacional (medido, não opinado):** latência p50 e p95 de cada chamada; taxa de recusa/bloqueio de moderação; custo real cobrado vs. tabela.

**Regra de decisão:** maior média ponderada (semelhança 35%, estabilidade 25%, duas identidades 20%, House Style 15%, artefatos 5%) entre os que passam o eliminatório; empate técnico (< 0,3 ponto) decide pelo menor custo e depois pela menor latência p95. Registrar o resultado como decisão no mapa, com as imagens geradas linkadas em um bucket privado (não no repositório; fotos de pessoas reais).

**Métrica automática opcional:** similaridade de embeddings faciais (ArcFace/InsightFace) entre foto e Character Sheet pode complementar a avaliação humana, mas só para uso interno de avaliação: os pesos InsightFace são "non-commercial research only" e não podem entrar no produto.

## O que não foi possível verificar (e vale checar no teste)

- Latência típica de Nano Banana 2.1, FLUX 3 Image e Seedream 5.0 Pro: nenhum fornecedor publica número; medir na fase A.
- Por que o Replicate cobra cerca de metade da tabela BFL no FLUX 3 Image; confirmar na fatura.
- Termos de uso comercial da BytePlus para a API paga do Seedream (páginas em JS não legíveis); se o Seedream vencer, ler os termos no console antes de contratar.
- fal.ai: definição formal do selo "Commercial use" (não existe página de docs; só o selo por modelo).
- Se a Gemini Developer API expõe `person_generation` / `prominent_people` (só encontrado na referência REST do Vertex).

## Fontes consultadas (todas em 2026-11-07)

Google: https://aistudio.google.com/docs/pricing · https://aistudio.google.com/docs/image-generation · https://aistudio.google.com/docs/models/gemini-nano-banana-2.1 · https://aistudio.google.com/docs/terms · https://policies.google.com/terms/generative-ai/use-policy · https://cloud.google.com/model-garden/pricing · https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/nano-banana-2-1 · https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-responsible-ai · https://fal.ai/models/google/nano-banana-2.1/edit · https://replicate.com/google/nano-banana-2.1 · https://blog.google/innovation-and-ai/products/nano-banana-pro/

Black Forest Labs: https://bfl.ai/pricing · https://docs.bfl.ai/quick_start/pricing.md · https://docs.bfl.ai/release-notes.md · https://docs.bfl.ai/flux_3/flux3_image_generate.md · https://docs.bfl.ai/guides/prompting_editing_multi_reference.md · https://docs.bfl.ai/guides/usecases_editing_character_consistency.md · https://docs.bfl.ai/guides/usecases_editing_multi_image_compositing · https://bfl.ai/legal/developer-terms-of-service · https://bfl.ai/legal/usage-policy · https://help.bfl.ai/articles/9272590838-self-serve-dev-license-overview-pricing · https://fal.ai/models/fal-ai/flux-3-image/edit · https://replicate.com/black-forest-labs/flux-3-image · https://huggingface.co/black-forest-labs/flux-3-image-klein/blob/main/LICENSE.md · https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md

ByteDance Seedream: https://ai.byteplus.com/ark/region:ap-southeast-1/docs/model-pricing · https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api · https://docs.byteplus.com/en/docs/ModelArk/2353368 · https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro · https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite · https://replicate.com/bytedance/seedream-5-pro · https://fal.ai/models/bytedance/seedream/v5/pro/edit · https://fal.ai/models/fal-ai/bytedance/seedream/v4.5/edit · https://replicate.com/blog/compare-image-editing-models

Alibaba Qwen: https://github.com/QwenLM/Qwen-Image · https://github.com/QwenLM/Qwen-Image/blob/main/LICENSE · https://huggingface.co/Qwen/Qwen-Image-Edit-2511 · https://huggingface.co/Qwen/Qwen-Image-2.1/blob/main/LICENSE · https://fal.ai/models/fal-ai/qwen-image-edit-2511 · https://replicate.com/qwen/qwen-image-edit-2511 · https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service-v-3-8-0

OpenAI: https://developers.openai.com/api/docs/pricing · https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/docs/api-reference/images/createEdit · https://developers.openai.com/api/docs/deprecations · https://developers.openai.com/api/docs/guides/image-prompting · https://replicate.com/openai/gpt-image-2.6-sunburst · https://fal.ai/models/openai/gpt-image-2.5/flare/edit

Runway: https://docs.dev.runwayml.com/guides/pricing/ · https://docs.dev.runwayml.com/guides/models/ · https://raw.githubusercontent.com/runwayml/sdk-node/main/src/resources/text-to-image.ts · https://runway.com/terms-and-conditions · https://dev.runwayml.com/learn/commercial-use

Ideogram: https://developer.ideogram.ai/api-reference/api-reference/generate-v3 · https://developer.ideogram.ai/api-reference/images/generate/ideogram-4-5 · https://ideogram.ai/models/4.5/ · https://ideogram.ai/legal/api-tos/ · https://fal.ai/models/fal-ai/ideogram/character/api

Adapters e LoRA: https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md · https://huggingface.co/h94/IP-Adapter-FaceID · https://github.com/instantX-research/InstantID · https://huggingface.co/ByteDance/InfiniteYou · https://fal.ai/models/fal-ai/flux-pulid · https://replicate.com/zsxkib/instant-id · https://fal.ai/models/fal-ai/flux-lora-fast-training · https://fal.ai/models/fal-ai/flux-2-trainer · https://fal.ai/models/fal-ai/flux-2/lora · https://replicate.com/docs/get-started/fine-tune-with-flux · https://replicate.com/black-forest-labs/flux-dev-lora

Plataformas: https://fal.ai/terms · https://fal.ai/legal/acceptable-use-policy · https://replicate.com/terms
