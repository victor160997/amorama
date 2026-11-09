# House Style do Amorama: guia de prompt (protótipo v0.1)

> **PROTÓTIPO.** Este guia existe para ser testado contra imagens reais e depois reduzido a uma única direção.
> Ticket: [House Style: guia de prompt do estilo 3D e protótipo de Character Sheets](https://github.com/victor160997/amorama/issues/8).
> Fonte canônica dos textos de prompt: `prompts.py` neste diretório (o harness lê de lá). Este arquivo explica o porquê.

O **House Style** é o único look de animação 3D em que toda Character Sheet e toda Scene são renderizadas. O Casal não escolhe. Este guia propõe **três direções deliberadamente diferentes** para o fundador reagir, mais um **dial de caricatura** independente da direção. O teste escolhe uma direção e um nível; o resto é descartado.

Regras fixas, válidas para qualquer direção:

- Nunca citar estúdios, filmes ou franquias nos prompts. O estilo é descrito pelas características (luz, material, proporção, paleta).
- Prompts em inglês (os modelos respondem melhor); o guia em PT-BR.
- A semelhança é eliminatória. Estilização acontece em **material, luz e paleta** antes de acontecer em **anatomia**. Só o dial de caricatura mexe em anatomia.

## 1. O que é uma Character Sheet (proposta a confirmar com o fundador)

Uma imagem por pessoa, 9:16, 1K. Ela tem duas funções: ser o que o Casal aprova e ser a referência de identidade que o modelo de vídeo recebe para cada Scene. As duas funções pedem a mesma coisa: rosto grande, nítido, sem distração.

| Elemento | Decisão proposta | Por quê |
|---|---|---|
| Enquadramento | Da cintura para cima, vista 3/4 virada para a câmera, linha dos olhos no terço superior | Rosto grande o bastante para julgar semelhança; o 3/4 mostra nariz e queixo melhor que o frontal |
| Expressão | Sorriso leve, olhar para a câmera | Neutro o bastante para servir de referência em qualquer Scene |
| Mãos | Naturais, relaxadas | Fase 0: o modelo ignorou "fora do quadro" e fez mãos boas em 12 de 12; proibir só gastava prompt |
| Fundo | Gradiente liso na cor da direção, sem cenário | Nada compete com o rosto; o modelo de vídeo não herda cenário errado |
| Roupa | A mesma das fotos de referência, simplificada | Fase 0: o modelo copia a roupa sozinho e isso ajuda o reconhecimento ("é o vestido dela") |
| Fotos de entrada | 3 por pessoa: frontal, 3/4 e corpo inteiro, luz natural, sem óculos escuros | Mesmo conjunto para todos os modelos |

Alternativa descartada por enquanto: "ficha" com 3 vistas (frente, perfil, corpo inteiro) numa só imagem. Dá mais informação ao modelo de vídeo, mas divide a resolução do rosto por três e complica a Approval. Volta se a consistência entre Scenes falhar no tracer bullet.

## 2. Bloco de fidelidade (igual em todas as direções)

Entra em todo prompt de Character Sheet, antes do estilo. É o que protege a semelhança:

> Keep this person's exact identity from the reference photos: face shape and jawline, nose, lips, eye shape and eye color, eyebrows, skin tone, hair color, texture, length and style, facial hair, glasses if present, visible marks, and body build. Friends must recognize them instantly. Do not beautify, slim, change age, lighten or darken the skin, or add or remove glasses.

## 3. Bloco "evitar" (igual em todas as direções)

Os três modelos aceitam só prompt positivo, então o "evitar" é escrito como instrução:

> No text, captions, logos or watermarks. No photorealistic skin pores or uncanny realism. No extra fingers or limbs. Single person only, no one else in frame.

Para imagens com o casal (fase B), acrescentar:

> Two different people: the person from the first reference set on the left, the person from the second on the right. Never blend or swap their facial features, hair or skin tone.

## 4. As três direções

As três são "animação 3D", mas discordam em material, luz, proporção e paleta. Variantes que só mudassem de cor não ensinariam nada.

### Direção A: Cinema caloroso

Um filme de animação 3D de longa-metragem, visto em tela grande. Pele macia com luz atravessando (subsurface), olhos um pouco maiores e muito vivos, cabelo em mechas volumosas, luz de cinema.

| Slot | Conteúdo |
|---|---|
| Iluminação | Key suave e grande de um lado, rim light quente atrás do cabelo, leve névoa volumétrica, profundidade de campo rasa |
| Proporções | Quase reais (cabeça 1:7); traços arredondados, olhos +10 a 15% |
| Textura | Pele lisa com subsurface, sem poros; cabelo em mechas esculpidas; tecido com dobras simplificadas |
| Paleta | Pastéis quentes: pêssego, creme, terracota suave, com um frio (azul-petróleo) de contraste |
| Enquadramento | O da Character Sheet (seção 1), fundo gradiente creme → pêssego |
| Evitar | Realismo fotográfico, pele plástica brilhante, iluminação chapada |

Aposta: a direção com mais chance de passar no painel cego, porque quase não mexe na anatomia. Risco: parecer "genérico de IA".

### Direção B: Miniatura artesanal

Bonecos de stop-motion em um set de miniatura. Materiais foscos que parecem feitos à mão (massa de modelar, feltro, madeira pintada), pequenas imperfeições, lente tilt-shift que denuncia a escala.

| Slot | Conteúdo |
|---|---|
| Iluminação | Luz prática de tungstênio quente, sombras suaves de softbox, foco raso tipo tilt-shift (bordas desfocadas) |
| Proporções | Levemente compactadas (cabeça 1:5), mãos grossas e simplificadas, pescoço curto |
| Textura | Pele fosca com microtextura de massa de modelar; roupa em feltro e lã com trama visível; cabelo em placas esculpidas |
| Paleta | Terrosa e dessaturada: mostarda, verde-oliva, tijolo, creme, com um acento saturado por imagem |
| Enquadramento | O da Character Sheet, fundo de papel-cartão liso em tom terroso |
| Evitar | Brilho plástico, superfícies perfeitas, luz fria de estúdio |

Aposta: a mais memorável e a mais difícil de confundir com "vídeo de IA"; combina com a ideia de presente feito à mão. Risco: a textura de massa pode comer os traços finos e derrubar a semelhança.

### Direção C: Boneco colecionável

Figura de vinil de colecionador fotografada em estúdio. Superfícies lisas e levemente brilhantes, cabeça grande, traços simplificados, fundo infinito de cor sólida, nitidez de foto de produto.

| Slot | Conteúdo |
|---|---|
| Iluminação | Estúdio limpo: luz frontal difusa, reflexo especular pequeno nos olhos e na pele, sombra de contato suave no chão |
| Proporções | Cabeça grande (1:4), corpo curto, olhos grandes, boca e nariz simplificados |
| Textura | Vinil liso semi-brilhante, roupa em peça única sem dobras, cabelo em bloco esculpido |
| Paleta | Saturada e alegre: fundo sólido em pastel saturado (menta, lavanda, amarelo-manteiga), roupa em cores planas |
| Enquadramento | O da Character Sheet, cintura para cima (fase 0: "corpo inteiro" encolheu o rosto) |
| Evitar | Textura de pele realista, luz dramática, cenário |

Aposta: o mais "produto", ótimo em thumbnail e no celular. Já nasce no nível 3 do dial; serve de prova de que a caricatura preserva o reconhecimento. Risco: parecer brinquedo infantil para um presente romântico.

## 5. Dial de caricatura (independente da direção)

O ticket de critério de aceite pede uma **variante mais caricata pronta como pivot (a)**. Em vez de uma quarta direção, o dial é um slot que entra em qualquer direção:

| Nível | Nome | Texto do slot | Quando usar |
|---|---|---|---|
| 1 | Fiel | "Realistic human proportions; stylization only in materials, lighting and color, not in anatomy." | Se a semelhança no nível 2 ficar no limite |
| 2 | Estilizado (padrão) | "Gently stylized proportions: head about 10% larger, eyes about 15% larger, softened and rounded features, otherwise true to the person." | Padrão das direções A e B |
| 3 | Caricato (pivot a) | "Caricature proportions: head about 1/4 of body height, large expressive eyes, exaggerate this person's three most distinctive features (for example nose, chin, eyebrows, hairline) while keeping them unmistakably recognizable." | Pivot (a) do gate; padrão da direção C |

Hipótese a testar: o nível 3 pode **melhorar** o reconhecimento (caricatura amplifica o que distingue) ao custo de ser menos lisonjeiro. O painel decide.

## 6. Como o prompt é montado

```
[CHARACTER SHEET FRAMING]  seção 1
[FIDELITY]                 seção 2
[DIRECTION A|B|C]          seção 4: material, luz, paleta, fundo
[STYLIZATION LEVEL 1|2|3]  seção 5
[AVOID]                    seção 3
```

Ordem importa pouco nos modelos atuais, mas o bloco de fidelidade vem antes do estilo porque, quando há conflito, queremos que a identidade ganhe.

## 7. Plano de teste (dentro de ~US$ 15, 1K em tudo)

Provedor do protótipo: **fal.ai** (decisão de 2026-11-08, créditos já existentes). Preços fal.ai de 2026-11-07: Nano Banana 2.1 ≈ US$ 0,046 com 3 fotos de entrada, FLUX 3 Image US$ 0,048, Seedream 5.0 Pro ≈ US$ 0,077 com 3 entradas. Em produção, Gemini direto e Replicate baixam isso em 15 a 50%.

| Fase | Pergunta | Modelos | Imagens | Custo estimado |
|---|---|---|---|---|
| 0. Direção | Qual das três direções o fundador quer? | Nano Banana 2.1 (o mais barato) | 3 direções × 2 pessoas × 2 gerações = 12 | ≈ US$ 0,55 |
| A. Modelo | Qual modelo preserva melhor a semelhança na direção escolhida? | Nano Banana 2.1, FLUX 3 Image, Seedream 5.0 Pro | 3 × 2 pessoas × 4 gerações = 24 | ≈ US$ 1,40 |
| B. Casal | Os dois juntos sem mistura de traços? | Os 3 | 3 × 3 stills de casal = 9 | ≈ US$ 0,60 |
| C. Pivot (a) | O nível 3 reconhece melhor ou pior? | Modelo vencedor | 2 pessoas × 2 gerações = 4 | ≈ US$ 0,30 |
| Opcional | Teto de qualidade: Nano Banana Pro na fase A | Nano Banana Pro | 8 | ≈ US$ 1,20 |
| Reserva | Iterar prompt, refazer falhas | | | ≈ US$ 5 |
| **Total** | | | ≈ 57 a 65 imagens | **≈ US$ 3 a 9**, teto US$ 15 |

Avaliação: nota cega 1–5 por imagem em semelhança (eliminatória: média < 3 descarta), aderência ao House Style e artefatos; na fase B, contagem de misturas/trocas de traços (qualquer uma é falha grave). Latência e custo real medidos pelo harness, não opinados. Regra de decisão herdada da pesquisa de modelos de imagem: semelhança 35%, estabilidade 25%, duas identidades 20%, House Style 15%, artefatos 5%.

## 8. Resultados

### Fase 0 (2026-11-08): direção

Nano Banana 2.1 via fal.ai, 12 imagens, US$ 0,55, 12 a 26 s por imagem. Notas de semelhança do casal (1 a 5):

| Direção | Notas | Média | Veredito |
|---|---|---|---|
| A Cinema caloroso (nível 2) | 5, 4, 5, 4 | 4,5 | **Escolhida** |
| B Miniatura artesanal (nível 2) | 3, 2, 2, 2 | 2,25 | Reprovada (corte 3): a textura de massinha come os traços |
| C Boneco colecionável (nível 3) | 1, 1, 1, 1 | 1,0 | Reprovada: caricatura + vinil perdem a pessoa |

Observações de estilo: as duas gerações de cada pessoa saíram quase idênticas em A e B (boa estabilidade); único artefato foi poeira flutuante numa imagem de B; em C uma geração saiu de corpo inteiro. O modelo copiou a roupa das fotos em todas e ignorou "mãos fora do quadro" sem prejuízo; o guia foi ajustado (seção 1).

Alerta para o pivot (a): o nível 3 em C tirou 1 em tudo. A fase C testa o nível 3 na direção A para separar o efeito da caricatura do efeito do vinil.


### Fase A (2026-11-08): modelo

Direção A nível 2, 4 gerações por pessoa e por modelo, via fal.ai. Notas de semelhança (1 a 5) de um avaliador em modo cego, as mesmas 8 imagens do Nano Banana incluem as 4 da fase 0 rejulgadas lado a lado:

| Modelo | Marcelle | Victor | Média | Inferência mediana / p95 | Custo 8 img | Veredito |
|---|---|---|---|---|---|---|
| **FLUX 3 Image** | 5, 3, 4, 4 | 4, 5, 5, 5 | **4,38** | 26 s / 28 s | US$ 0,38 | **Escolhido** |
| Seedream 5.0 Pro | 5, 4, 2, 5 | 4, 4, 4, 3 | 3,88 | 42 s / 104 s | US$ 0,61 | Reserva |
| Nano Banana 2.1 | 5, 1, 2, 3 | 2, 2, 3, 2 | 2,50 | 19 s / 24 s | US$ 0,37 | Reprovado (corte 3) |

Leitura de estilo: Nano Banana é o mais estilizado e o melhor enquadramento de Ficha, mas perdeu a pessoa; FLUX estiliza menos (render semirrealista) e desvia o fundo para gradiente multicolor, mas preserva o rosto; Seedream faz rosto menor e poses demais. Duas imagens do Nano Banana que tiraram 5 na fase 0 tiraram 5 e 2 na fase A: a nota depende do que está ao lado. O painel cego de 3 pessoas do gate rejulga tudo no tracer bullet.

### Fase B (2026-11-08): casal

3 stills (café, praia, dança) em FLUX e Seedream, 6 imagens, US$ 0,41. **Zero misturas ou trocas de traços** em ambos. Roupa da Marcelle mudou de cor na cena da dança nos dois modelos. FLUX quase abandona a estilização em cena de casal (semirrealismo); Seedream segura melhor. Como as Scenes do produto vêm do modelo de vídeo a partir das Fichas, e não destes stills, o efeito real fica para o tracer bullet.

### Fase C (2026-11-08): pivot (a)

Nível 3 na direção A, FLUX, 4 imagens, US$ 0,19. **O FLUX ignorou a caricatura**: saída igual ao nível 2 com olhos um pouco maiores; uma imagem ganhou um piercing inexistente. Conclusão: o pivot (a) do gate não existe por prompt no FLUX. Se o painel reprovar a semelhança no tracer bullet, pivot (a) = Seedream 5.0 Pro nível 3 (não testado), senão ir direto ao pivot (b).

## 9. Decisão

- **House Style v1 = direção A (Cinema caloroso), nível 2**, prompt de `prompts.py` (`character_sheet_prompt("A", 2)`). Direções B e C descartadas. O look real do v0 é o que o FLUX produz com esse prompt: estilização mais leve que a descrita, fundo em gradiente pastel. Reforçar o prompt para mais estilização é ajuste do tracer bullet, não decisão deste ticket.
- **Character Sheet** = uma imagem 9:16 1K por pessoa, 3/4, cintura para cima, roupa das fotos, fundo liso (seção 1).
- **Modelo de imagem = FLUX 3 Image**, reserva Seedream 5.0 Pro; Nano Banana 2.1 reprovado em semelhança.
- **Provedor**: fal.ai no protótipo e no tracer bullet (créditos existentes). Produção: BFL direto ou Replicate (metade do preço no Replicate; ToS da BFL exige consentimento documentado da pessoa retratada, já previsto no fluxo).
- **Custo medido** por Character Sheet no fal.ai: US$ 0,048 (FLUX); 2 Fichas + 1 Regeração ≈ US$ 0,15 por Order.
- **Total gasto neste ticket**: US$ 2,34 de US$ 15 (42 imagens + 1 fumaça). Sobram ≈ US$ 12,66 do envelope de imagem, que podem reforçar o tracer bullet.

## 10. O que este protótipo não decide

- Formato do Script e das legendas (névoa do mapa).
- Como a Character Sheet vira referência no modelo de vídeo (tracer bullet).
- Música e montagem (tracer bullet).
