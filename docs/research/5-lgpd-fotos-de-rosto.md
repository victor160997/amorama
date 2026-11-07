# Pesquisa #5: LGPD aplicada a fotos de rosto, consentimento de terceiros e retenção

- Ticket: [#5](https://github.com/victor160997/amorama/issues/5)
- Data da pesquisa: 2026-11-07
- Escopo: o que a LGPD (Lei 13.709/2018), as resoluções e guias da ANPD e as políticas dos provedores de API exigem de um serviço que recebe fotos de rosto de duas pessoas (o Couple), enviadas por uma delas, para gerar Character Sheets, Scenes e um Final Video, usando APIs de geração hospedadas fora do Brasil.
- Postura inicial a validar: checkbox único afirmando que as duas pessoas consentiram e são maiores; fotos apagadas 30 dias após a entrega; Final Video guardado 90 dias; fotos nunca usadas para treinar modelos.
- Isto é pesquisa jurídica de produto, não parecer de advogado. Os pontos marcados como **decisão** precisam de validação com advogado antes do lançamento pago.

## TL;DR

1. **Classificação.** A ANPD trata todo dado biométrico como sensível (art. 5º, II; art. 11) e, em fiscalização recente, usou a definição do Decreto 10.046/2019: "características biológicas e comportamentais mensuráveis [...] que podem ser coletadas para reconhecimento automatizado, tais como [...] o formato da face". A LGPD não tem a ressalva do GDPR de que foto só é biometria quando processada para identificação única, e a ANPD ainda não publicou regra sobre isso (tomada de subsídios de 2025, norma prevista para 2026). Uma foto de rosto que passa por um modelo que extrai e reproduz a fisionomia é, no mínimo, um caso de fronteira. **Decisão recomendada: tratar as fotos como dado sensível.** O custo é pequeno (consentimento específico e destacado) e o risco da outra leitura é alto (base legal nula, multa de até 2% do faturamento).
2. **Base legal.** Para dado sensível, execução de contrato (art. 7º, V) e legítimo interesse (art. 7º, IX) **não existem** como hipóteses: o art. 11 só admite consentimento "específico e destacado" (art. 11, I) ou hipóteses de dispensa que não se aplicam a um produto de entretenimento. Logo a base para as fotos é **consentimento do titular, específico e destacado, por pessoa**. Execução de contrato cobre o resto do Order (e-mail, pagamento, Story, Order Link) para quem contrata.
3. **Segunda pessoa.** Consentimento é "manifestação [...] pela qual o titular concorda" (art. 5º, XII) e o ônus de provar que foi obtido é do controlador (art. 8º, § 2º). O checkbox do uploader dizendo que o parceiro concordou não é consentimento do parceiro; é só uma declaração contratual que ajuda em regresso civil. **Decisão recomendada: coletar consentimento individual da segunda pessoa, com o próprio link dela (modelo "Partner Link"), antes de gerar a Character Sheet dela.** O checkbox do uploader continua existindo, como garantia contratual complementar e para o período entre upload e consentimento do parceiro.
4. **Menores.** O Couple é definido como dois adultos; maioridade aos 18 (CC art. 5º). Consentimento de menor de 16 é inválido e entre 16 e 18 exige assistência; o art. 14 da LGPD exige melhor interesse e consentimento de um dos pais quando criança (< 12). O ECA Digital (Lei 15.211/2025, em vigor desde 17/03/2026) só alcança serviços direcionados a ou de "acesso provável" por crianças e adolescentes, com três requisitos cumulativos; um produto de casal, pago, sem feed social, dificilmente se enquadra, mas o teste deve ficar documentado. **Decisão: 18+ declarado nos termos, bloqueio por moderação de fotos que aparentem menores (os próprios provedores já bloqueiam), sem fluxo infantil nenhum.**
5. **Retenção.** A LGPD manda eliminar ao fim do tratamento (arts. 15 e 16), sem prazo numérico. Os números propostos são defensáveis se forem justificados pela finalidade: as fotos são necessárias até a Approval e as Regenerations; depois da entrega, só uma janela curta de suporte justifica retê-las. **Decisão recomendada: fotos apagadas na entrega do Final Video, com janela máxima de 30 dias só se houver pedido de Regeneration pós-entrega; Final Video por 90 dias para download, depois eliminado; metadados do Order (sem fotos) pelo prazo fiscal/consumerista.** 30 dias para as fotos é o teto, não o padrão. O que faz a diferença é o que acontece **nos provedores**: fal.ai guarda inputs/outputs por 90 dias por padrão a menos que você desligue; Replicate apaga em 1 hora; Runway não documenta; Vertex AI só loga prompts sinalizados por abuso (até 90 dias); Anthropic apaga em 30 dias.
6. **Treinamento.** "Nunca" é fácil de prometer no Amorama e difícil de garantir no fornecedor: Runway (Termos de Uso self-serve, §4.4) reserva o direito de treinar com inputs e outputs; fal.ai self-serve pode usar "Usage Data" derivada; Gemini API no tier gratuito treina com os dados. Só Vertex AI, Anthropic API e fal.ai/Runway em plano enterprise têm compromisso contratual de não treinar. **Decisão: só usar provedores/planos com cláusula de não treinamento.**
7. **Transferência internacional.** Exige base legal **mais** um mecanismo do art. 33 (Resolução CD/ANPD 19/2024, art. 9º). EUA não têm decisão de adequação (só a União Europeia/EEE, Resolução 32/2026). Mecanismos viáveis: (a) cláusulas-padrão da ANPD no contrato com o importador (Anexo II da Res. 19/2024, texto não alterável, obrigatório desde 23/08/2025) ou (b) consentimento específico e em destaque para a transferência, com informação prévia do caráter internacional (art. 33, VIII). **Dos cinco provedores, só o Google Cloud (Vertex AI) incorpora as cláusulas-padrão da ANPD por padrão via DPA ("BR SCCs", 21/08/2025).** fal.ai, Replicate, Runway e Anthropic (DPA) não mencionam Brasil nem LGPD; com eles o mecanismo seria o consentimento do art. 33, VIII (frágil, revogável) ou um aditivo com as cláusulas da ANPD negociado caso a caso. Além disso, a Res. 19/2024, art. 17, § 2º, obriga a publicar na Política de Privacidade, em português, um documento com forma, duração, finalidade, país de destino e responsáveis pela transferência.
8. **Termos e Política.** Lista completa na seção 10. O essencial: consentimento destacado (cláusula separada, art. 8º, § 1º) por pessoa, finalidade descrita (gerar Character Sheets, Scenes e Final Video no House Style), informação da transferência internacional com países de destino, prazos de retenção numéricos, canal de exercício de direitos (art. 18), declaração 18+, proibição de fotos de terceiros sem consentimento, licença de uso do Final Video e disclaimer de conteúdo sintético.

## 1. As fotos são dado biométrico/sensível?

### O que a lei diz

- LGPD art. 5º, II: "dado pessoal sensível: dado pessoal sobre origem racial ou étnica, convicção religiosa, opinião política, filiação a sindicato ou a organização de caráter religioso, filosófico ou político, dado referente à saúde ou à vida sexual, dado genético ou **biométrico**, quando vinculado a uma pessoa natural". ([planalto.gov.br, Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm))
- LGPD art. 11, § 1º: "Aplica-se o disposto neste artigo a qualquer tratamento de dados pessoais que revele dados pessoais sensíveis e que possa causar dano ao titular, ressalvado o disposto em legislação específica." (mesma fonte)
- A LGPD **não define** "dado biométrico". O GDPR (art. 4(14) e considerando 51) restringe biometria a dados resultantes de "tratamento técnico específico" que permita identificação única, e diz expressamente que fotografias só são biométricas nesse caso. A LGPD não copiou essa ressalva.

### O que a ANPD diz

- Nota Técnica nº 4/2026/CPDP/CGF/SFI/ANPD (fiscalização do reconhecimento facial nas escolas do Paraná), itens 5.4.1 e 5.25: "Os atributos biométricos de determinada pessoa natural, conforme definição do art. 2º, II, do Decreto nº 10.046/2019, podem ser definidos como as características biológicas e comportamentais mensuráveis da pessoa natural que podem ser coletadas para reconhecimento automatizado, tais como a palma da mão, as digitais dos dedos, a retina ou a íris dos olhos, **o formato da face**, a voz e a maneira de andar. Os atributos biométricos dos indivíduos, por definição legal, constituem dados pessoais sensíveis". E: "os dados pessoais biométricos são considerados como dados pessoais sensíveis, requerendo hipótese de tratamento necessariamente baseada no art. 11 da LGPD." ([gov.br/anpd, PDF](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos/nota_tecnica_4_versao_publica-educacao_parana.pdf/@@display-file/file))
- A mesma nota (5.4.4) descreve a análise técnica de biometria facial como "detecção (descobrir e localizar faces nas imagens e vídeos), a classificação (categorizar o indivíduo por meio de atributos como gênero, etnia, raça, idade...), a verificação (...)" etc. Ou seja, para a ANPD o que torna a face "biometria" é a análise automatizada dos atributos, não a identificação em cadastro.
- Tomada de Subsídios sobre dados biométricos (02/06 a 02/07/2025, item 5 da Agenda Regulatória 2025-2026): a ANPD descreve biometria como "categoria sensível de dados pessoais, conforme a Lei Geral de Proteção de Dados Pessoais (LGPD)" e lista "reconhecimento facial" entre os exemplos; a norma final é esperada para 2026 e ainda não saiu. ([gov.br/anpd, notícia de 02/06/2025](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-abre-tomada-de-subsidios-sobre-tratamento-de-dados-biometricos))
- Radar Tecnológico vol. 2, "Biometria e Reconhecimento Facial" (24/06/2024): estudo não vinculante que reafirma biometria como dado sensível e distingue detecção, identificação e classificação de faces. Não localizei o PDF no portal durante a pesquisa; a referência consta de documento oficial da própria tomada de subsídios.

### Aplicação ao Amorama

O pipeline recebe fotos de rosto, um modelo extrai os traços fisionômicos e os reproduz em uma Character Sheet estilizada, depois nas Scenes. Não há identificação ("quem é essa pessoa?") nem autenticação. Há, porém, análise automatizada de atributos faciais e produção de uma representação derivada da fisionomia. Pela definição que a ANPD usou (Decreto 10.046/2019), "formato da face coletado para reconhecimento automatizado" é biometria; a ressalva europeia sobre fotografias não existe na LGPD; e a regulação específica está em aberto.

Além disso, mesmo na leitura mais branda (foto = dado pessoal comum), a foto de rosto **revela** origem racial ou étnica e pode revelar saúde ou religião (art. 11, § 1º), e o tratamento é intrinsecamente ligado ao direito de imagem (CC art. 20), que a Resolução CD/ANPD 2/2022 cita como exemplo de dano relevante.

**Conclusão:** tratar como dado sensível. Consequências práticas:

- base legal do art. 11 (ver seção 2);
- cláusula 11 das cláusulas-padrão (salvaguardas adicionais para dados sensíveis) nas transferências;
- o Amorama provavelmente faz "tratamento de alto risco" na Res. CD/ANPD 2/2022 (critério específico: dados sensíveis; critério geral: pode "afetar significativamente interesses e direitos fundamentais", cujo § 2º cita "violação [...] ao direito à imagem"). Se for alto risco, perde as flexibilizações para agentes de pequeno porte (prazos em dobro, dispensa de encarregado). Tratar como se não tivesse as flexibilizações é o caminho seguro. ([DOU, Res. CD/ANPD 2/2022, arts. 3º e 4º](https://in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-2-de-27-de-janeiro-de-2022-376562019))

## 2. Base legal: consentimento vs execução de contrato

### Texto

- Art. 7º, I (consentimento), V ("quando necessário para a execução de contrato ou de procedimentos preliminares relacionados a contrato do qual seja parte o titular, a pedido do titular dos dados") e IX (legítimo interesse) valem só para dados **não sensíveis**.
- Art. 11: "O tratamento de dados pessoais sensíveis somente poderá ocorrer nas seguintes hipóteses: I - quando o titular ou seu responsável legal consentir, de forma específica e destacada, para finalidades específicas; II - sem fornecimento de consentimento do titular, nas hipóteses em que for indispensável para: a) cumprimento de obrigação legal [...] b) políticas públicas [...] c) estudos por órgão de pesquisa [...] d) exercício regular de direitos [...] e) proteção da vida [...] f) tutela da saúde [...] g) garantia da prevenção à fraude e à segurança do titular, nos processos de identificação e autenticação de cadastro em sistemas eletrônicos".
- Guia Orientativo da ANPD sobre Legítimo Interesse (v1.0, fev/2024), p. 8: "se trata de uma hipótese legal não aplicável ao tratamento de dados pessoais sensíveis, haja vista a sua previsão apenas no art. 7º da LGPD, não tendo sido reproduzida no art. 11. Assim, caso o tratamento envolva dados pessoais sensíveis, o controlador deve verificar se existe outra hipótese legal que ampare a realização do tratamento, entre as previstas no art. 11". ([gov.br/anpd, guia](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse))
- Requisitos do consentimento: art. 5º, XII ("manifestação livre, informada e inequívoca pela qual o titular concorda com o tratamento de seus dados pessoais para uma finalidade determinada"); art. 8º, § 1º ("Caso o consentimento seja fornecido por escrito, esse deverá constar de cláusula destacada das demais cláusulas contratuais"); § 2º ("Cabe ao controlador o ônus da prova de que o consentimento foi obtido em conformidade com o disposto nesta Lei"); § 4º ("autorizações genéricas para o tratamento de dados pessoais serão nulas"); § 5º (revogável a qualquer momento, "por procedimento gratuito e facilitado"); art. 9º, § 1º (consentimento nulo se a informação prestada for enganosa).

### Decisão

| Dado | Titular | Base legal | Observações |
|---|---|---|---|
| Fotos de rosto, Character Sheets, Scenes e Final Video (contêm a fisionomia) | cada pessoa do Couple | art. 11, I: consentimento específico e destacado, **um por pessoa** | finalidade enumerada: gerar Character Sheets, Scenes e o Final Video do Order no House Style; mais o consentimento de transferência internacional (art. 33, VIII) se não houver cláusulas-padrão com o provedor |
| E-mail, dados de pagamento, Order Link, Story | quem contrata | art. 7º, V (execução de contrato) | Story pode conter dados sensíveis do casal (religião, saúde); cobrir no mesmo consentimento |
| Dados do parceiro no Story (nome, fatos) | parceiro | art. 7º, IX (legítimo interesse) com teste de balanceamento documentado, ou o mesmo consentimento individual | o consentimento individual resolve os dois de uma vez |
| Logs de acesso | ambos | art. 7º, II (obrigação legal: Marco Civil art. 15, 6 meses) | ver seção 6 |

Por que não "execução de contrato" para as fotos mesmo que não fossem sensíveis: a segunda pessoa não é parte do contrato ("contrato do qual seja parte o titular, a pedido do titular"), então a base só cobriria o uploader. E por que não "legítimo interesse": além de não valer para dado sensível, o guia da ANPD exige necessidade, legítima expectativa e teste de balanceamento; a expectativa de alguém cuja foto foi enviada por outra pessoa para virar personagem 3D não é óbvia.

Risco a aceitar conscientemente: consentimento é revogável (art. 8º, § 5º; art. 18, IX). Se um dos dois revogar depois da entrega, o Amorama deve parar de tratar e eliminar o que tem (art. 15, III; art. 16), sem reembolso obrigatório pela LGPD, mas com a relação de consumo a considerar. Os termos devem dizer isso.

## 3. A segunda pessoa (não é o uploader)

### Problema

O consentimento do art. 11, I é ato pessoal do titular; o art. 8º, § 2º põe no controlador o ônus de provar que foi obtido. Um checkbox marcado pelo uploader prova a declaração do uploader, não a vontade do parceiro. Em paralelo, o Código Civil, art. 20, permite proibir "a utilização da imagem de uma pessoa" para fins comerciais sem autorização, e a Súmula 403 do STJ diz: "Independe de prova do prejuízo a indenização pela publicação não autorizada de imagem de pessoa com fins econômicos ou comerciais". ([planalto.gov.br, CC](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm); [STJ, Súmula 403](https://arquivocidadao.stj.jus.br/index.php/sumula-403))

O cenário de risco concreto: ex-parceiro(a) ou pessoa que nunca soube do pedido descobre o Final Video. Nesse caso o Amorama é controlador e responde (art. 42), com direito de regresso contra o uploader.

### Opções

| Opção | Como | Prova de consentimento do parceiro | Atrito | Veredito |
|---|---|---|---|---|
| A. Checkbox único do uploader ("declaro que nós dois consentimos e somos maiores") | só no formulário de upload | nenhuma: é declaração de terceiro | zero | insuficiente sozinho; manter como garantia contratual |
| B. Partner Link: o uploader informa e-mail/WhatsApp do parceiro; o parceiro recebe link próprio, vê as fotos dele que foram enviadas e dá consentimento destacado | segundo link secreto, no mesmo padrão do Order Link | registro individual (timestamp, IP, texto aceito, versão) | médio: um passo a mais, mas também vira momento de "surpresa" controlada ou de Approval conjunta | **recomendado** |
| C. Approval das Character Sheets pelos dois | exige que os dois acessem o Order Link e aprovem | prova forte, mas tardia: as fotos já foram tratadas e transferidas para gerar as Character Sheets | médio | boa como camada adicional, não substitui B porque o consentimento tem que ser prévio |
| D. Fluxo "presente surpresa": uploader consente pelos dois e o parceiro só consente depois | — | inexistente até a entrega | zero | incompatível com art. 11, I; não oferecer em v0 |

Desenho recomendado para B:

1. Upload: uploader dá o próprio consentimento destacado e informa o contato do parceiro. Checkbox contratual: "confirmo que as fotos são minhas e de [nome], que [nome] sabe deste pedido e que somos maiores de 18 anos".
2. Nada do parceiro é enviado a provedor externo até o consentimento do parceiro. Em Concierge Mode isso é um passo manual no checklist do operador. As fotos do parceiro ficam em quarentena cifrada; se o consentimento não vier em N dias (por exemplo 7), são eliminadas e o Order é cancelado/reembolsado conforme os termos.
3. Partner Link mostra: quem pediu, para que (texto curto com a finalidade), quais fotos dele foram enviadas, para onde vão (país dos provedores), por quanto tempo ficam, como revogar. Botão de consentimento destacado e botão de recusa (que elimina as fotos dele e avisa o uploader).
4. Registro: id do Order, pessoa, versão do texto, timestamp, IP/user-agent, hash das fotos consentidas.
5. Approval das Character Sheets pode ser do uploader sozinho (produto) ou dos dois (mais seguro); o Final Video fica disponível pelo Order Link para ambos.

Se o produto insistir num fluxo surpresa, a única mitigação séria é gerar primeiro apenas a Character Sheet do uploader e exigir o consentimento do parceiro antes de qualquer tratamento da foto dele; não há atalho legal para tratar dado sensível de alguém sem o consentimento dessa pessoa.

## 4. Menores de idade

- Maioridade civil aos 18 (CC art. 5º); menores de 16 são absolutamente incapazes e entre 16 e 18 relativamente incapazes (CC arts. 3º e 4º). Consentimento de dado sensível dado por menor de 16 é nulo; entre 16 e 18 exige assistência dos pais.
- LGPD art. 14: tratamento de dados de crianças e adolescentes "deverá ser realizado em seu melhor interesse"; para crianças, "consentimento específico e em destaque dado por pelo menos um dos pais ou pelo responsável legal" (§ 1º), com "todos os esforços razoáveis para verificar" que foi o responsável (§ 5º). Enunciado CD/ANPD 1/2023 (DOU 24/05/2023): "O tratamento de dados pessoais de crianças e adolescentes poderá ser realizado com base nas hipóteses legais previstas no art. 7º ou no art. 11 da LGPD, desde que observado e prevalecente o seu melhor interesse, a ser avaliado no caso concreto, nos termos do art. 14 da Lei." ([gov.br/anpd, PDF](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-divulga-enunciado-sobre-o-tratamento-de-dados-pessoais-de-criancas-e-adolescentes/Enunciado1ANPD.pdf/@@display-file/file))
- ECA Digital (Lei 15.211/2025, em vigor em 17/03/2026, art. 41-A): aplica-se a "todo produto ou serviço de tecnologia da informação direcionado a crianças e a adolescentes no País ou de acesso provável por eles". "Acesso provável" exige três requisitos cumulativos (art. 1º, parágrafo único): probabilidade de uso e atratividade; facilidade de acesso; e "significativo grau de risco à privacidade, à segurança ou ao desenvolvimento biopsicossocial". Onde se aplica, veda autodeclaração de idade (art. 9º, § 1º) e exige verificação confiável. ([planalto.gov.br, Lei 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm))
- Guia Orientativo da ANPD sobre o escopo do ECA Digital (out/2026), p. 30-34: "um determinado produto ou serviço de tecnologia da informação não será caracterizado como de 'acesso provável' por crianças e adolescentes se apenas um ou dois dos requisitos estiverem presentes"; o guia lista categorias com presunção legal de acesso provável (redes sociais, lojas de apps, jogos, provedores de conteúdo adulto, "sistemas capazes de geração de conteúdo e interação com usuários a partir de instruções em linguagem natural", etc.) e recomenda documentar o "teste de acesso provável". ([gov.br/anpd, PDF](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-fornecedores-de-produtos-ou-servicos-de-tecnologia-da-informacao.pdf/@@display-file/file))
- Atenção: a categoria presumida "sistemas capazes de geração de conteúdo [...] a partir de instruções em linguagem natural" (Decreto 12.880/2026) é próxima do que o Amorama faz com a Story. O argumento para afastar a presunção é que o Amorama não expõe um gerador livre ao usuário: o Couple escreve uma Story, e a geração roda em Concierge Mode dentro de um Script fixo, sem interação em linguagem natural com o modelo. Isso precisa estar escrito no teste de acesso provável.
- Provedores: Veo rejeita por padrão a geração de crianças (`personGeneration` padrão `allow_adult`; filtro de criança só liberado com allowlist); Runway proíbe "Characters based on the face or voice of a person under the age of 18"; fal.ai exige 18+ para usuários e End Users; Gemini API exige 18+ e proíbe direcionar a menores. Ou seja, mesmo que o Amorama quisesse, o pipeline falharia com menores.

**Decisão:** o Amorama é serviço para adultos (dois adultos, sem crianças no v0, conforme GLOSSARY). Medidas: (i) declaração 18+ nos termos e no consentimento de cada pessoa; (ii) moderação de upload que rejeite fotos que aparentem menores (classificador de idade aparente ou revisão humana em Concierge Mode), com registro da rejeição; (iii) teste de acesso provável do ECA Digital documentado (sem design infantil, pago, sem feed público, sem interação livre com o modelo); (iv) nenhum fluxo com pais/responsáveis, porque o produto não aceita menores em nenhuma hipótese. Reavaliar se o produto algum dia incluir filhos na Scene.

## 5. Direitos do titular e eliminação

- Art. 18: confirmação, acesso, correção, anonimização/bloqueio/eliminação de dados desnecessários (IV), portabilidade, "eliminação dos dados pessoais tratados com o consentimento do titular, exceto nas hipóteses previstas no art. 16" (VI), informação sobre compartilhamento (VII), revogação (IX). § 5º: atendimento "sem custos", nos prazos do regulamento; § 6º: o controlador deve informar "de maneira imediata" aos agentes com quem compartilhou os dados, para que repitam a eliminação, "exceto nos casos em que esta comunicação seja comprovadamente impossível ou implique esforço desproporcional".
- Art. 19: declaração simplificada imediata ou declaração completa em até 15 dias. Res. CD/ANPD 2/2022, art. 15: pequeno porte pode dar a simplificada em até 15 dias.
- Cláusulas-padrão (Res. 19/2024, Anexo II, cláusula 15.3): prazo de 15 dias para atender pedidos relativos a dados transferidos.
- Prático: os dois titulares devem poder exercer direitos **separadamente**, inclusive o parceiro contra o Order do uploader. A eliminação de um implica eliminar Character Sheet, Scenes e Final Video (contêm a fisionomia dele) e acionar a eliminação nos provedores (fal.ai tem endpoint de delete; Replicate já apagou em 1 h; Runway e Vertex não documentam delete por API para o fluxo normal; Anthropic apaga em 30 dias).

## 6. Retenção defensável

### Regras

- Art. 15: término do tratamento quando a finalidade foi alcançada ou os dados deixaram de ser necessários (I), fim do período (II), revogação (III), determinação da ANPD (IV). Art. 16: "Os dados pessoais serão eliminados após o término de seu tratamento, no âmbito e nos limites técnicos das atividades, autorizada a conservação para": obrigação legal (I), pesquisa (II), transferência a terceiro (III), uso exclusivo do controlador anonimizado (IV).
- Art. 6º, III (necessidade: "limitação do tratamento ao mínimo necessário"). Res. 19/2024, art. 9º, parágrafo único: a transferência "deverá se limitar ao mínimo necessário".
- Marco Civil (Lei 12.965/2014), art. 15: provedor de aplicações com fins econômicos deve guardar "registros de acesso a aplicações de internet" por 6 meses, sob sigilo. Isso são logs de acesso, não fotos. ([planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm))
- Res. CD/ANPD 15/2024, art. 10: registro de incidentes de segurança por no mínimo 5 anos.
- Res. 19/2024, cláusulas-padrão, cláusula 2: o contrato com o importador deve declarar "Período de armazenamento dos dados".

### Tabela recomendada

| Dado | Finalidade | Prazo proposto | Justificativa |
|---|---|---|---|
| Fotos de origem (uploader e parceiro) | gerar Character Sheets e Scenes, inclusive Regenerations | até a entrega do Final Video; eliminação em até 7 dias após a entrega; **30 dias é o teto** só quando houver Regeneration pós-entrega aberta | depois da entrega a finalidade acabou (art. 15, I); 30 dias "por padrão" é difícil de justificar se não há mais geração a fazer |
| Fotos do parceiro antes do consentimento dele | quarentena | 7 dias, depois eliminadas se não houver consentimento | sem base legal ainda; quanto menos tempo, melhor |
| Character Sheets e Scenes | montar o Final Video e Regenerations | mesmo prazo das fotos | contêm a fisionomia |
| Final Video | entrega/download pelo Order Link; suporte | 90 dias após a entrega, depois eliminado | a janela de reclamação do consumidor por serviço durável é 90 dias (CDC art. 26, II); o Couple pode baixar nesse período; mais que isso vira armazenamento sem finalidade |
| Registro de consentimento (texto, versão, timestamp, IP, hash das fotos) | prova (art. 8º, § 2º) | 5 anos após a eliminação dos dados | prescrição geral de pretensões reparatórias; sem a foto em si |
| Dados do Order (e-mail, pagamento, Story) | contrato, fiscal | 5 anos | obrigação fiscal/contábil (art. 16, I) |
| Logs de acesso | Marco Civil art. 15 | 6 meses | obrigação legal |
| Prompts e outputs nos provedores | geração | ver seção 8; configurar o mínimo que cada um permite | o Amorama responde pelo que fica lá (art. 42; cláusula 20 das cláusulas-padrão) |

Observação sobre "fotos apagadas 30 dias após a entrega": vale como teto comunicado ao usuário ("em até 30 dias"), mas a política interna deve apagar na entrega mais a janela de Regeneration. Se o produto quiser oferecer "refazer o vídeo depois", isso exige novo consentimento ou consentimento que já preveja a retenção pelo prazo da garantia, dito com clareza.

Treinamento: a promessa "nunca usamos suas fotos para treinar modelos" é compatível com o art. 7º, § 7º / art. 6º, I (finalidade) e deve constar dos termos. Qualquer melhoria do House Style com material real do Couple seria nova finalidade e exigiria novo consentimento específico (art. 8º, § 4º). A promessa só é verdadeira se os provedores também não treinarem (seção 8).

## 7. Transferência internacional

### Regras

- LGPD art. 33: a transferência só é permitida para países com proteção adequada (I), com garantias comprovadas pelo controlador na forma de cláusulas contratuais específicas, cláusulas-padrão, normas corporativas globais ou selos/certificados (II), ou nas demais hipóteses, entre elas "quando o titular tiver fornecido o seu consentimento específico e em destaque para a transferência, com informação prévia sobre o caráter internacional da operação, distinguindo claramente esta de outras finalidades" (VIII) e "quando necessário para atender as hipóteses previstas nos incisos II, V e VI do art. 7º" (IX).
- Resolução CD/ANPD 19/2024 (DOU 23/08/2024), Anexo I, art. 9º: a transferência só pode ocorrer "amparada em: I - uma das hipóteses legais previstas no art. 7º ou no art. 11 da LGPD; e II - um dos seguintes mecanismos válidos": decisão de adequação (a); cláusulas-padrão, normas corporativas globais ou cláusulas específicas (b); ou as hipóteses do art. 33, II, "d", e III a IX (c). ([in.gov.br, Res. 19/2024](https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-19-de-23-de-agosto-de-2024-580095396))
- Art. 3º, III-V: "transferência" é transmitir, compartilhar ou disponibilizar acesso a outro agente de tratamento; "coleta internacional" (agente no exterior coletando direto do titular) não é transferência (art. 6º). Enviar fotos de um servidor do Amorama para a API de um provedor nos EUA é transferência internacional.
- Art. 16: a validade com cláusulas-padrão "pressupõe a adoção integral e sem alteração do texto disponibilizado no Anexo II, mediante instrumento contratual firmado entre o exportador e o importador"; as cláusulas podem integrar um contrato mais amplo via aditivo (§ 1º, II), e nada no contrato pode contrariá-las (§ 2º).
- Resolução art. 2º, parágrafo único: prazo de 12 meses para incorporar as cláusulas-padrão (vencido em 23/08/2025).
- Art. 17, § 2º: o controlador "deverá ainda publicar em sua página na Internet documento contendo informações em língua portuguesa, em linguagem simples, clara, precisa e acessível sobre a realização da transferência internacional de dados, incluindo, pelo menos": forma, duração e finalidade específica; país de destino; identificação e contatos do controlador; uso compartilhado e finalidade; responsabilidades dos agentes e medidas de segurança; direitos do titular e canal, inclusive o direito de peticionar à ANPD. Pode estar integrado à Política de Privacidade, "de forma destacada" (§ 3º). § 1º: íntegra das cláusulas ao titular em 15 dias, se pedido.
- Anexo II, cláusulas relevantes: 2 (descrição da transferência, categorias de dados, período de armazenamento); 3 e 18 (transferências posteriores, isto é, subprocessadores do importador); 11 (dados sensíveis: salvaguardas adicionais); 13 (exportador garante que coletou legalmente); 14 (transparência); 15 (direitos, 15 dias); 16 (incidente em 3 dias úteis); 20 (eliminação ao fim do tratamento); 21 (medidas de segurança descritas na Seção III); 22 (importador declara que leis locais não o impedem de cumprir); 24 (foro brasileiro).
- Decisões de adequação: só a União Europeia/EEE, por Resolução nº 32/2026 (DOU 26/01/2026); EUA, Reino Unido, Singapura etc. não têm. ([in.gov.br, Res. 32/2026](https://www.in.gov.br/web/dou/-/resolucao-n-32-de-26-de-janeiro-de-2026-683334547); [gov.br/anpd, página de transferência internacional](https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados))

### Aplicação

Todos os provedores candidatos processam nos EUA (ou em local não garantido). Caminhos:

1. **Cláusulas-padrão da ANPD no contrato com o provedor.** Único mecanismo contratual robusto. Google Cloud já incorpora: o Cloud Data Processing Addendum, Apêndice 3, define "LGPD" e "BR SCCs", e a página [cloud.google.com/sccs/br-c2p](https://cloud.google.com/sccs/br-c2p) (21/08/2025) reproduz o Anexo II em inglês, com Google como "Importer/processor" e o cliente como "Exporter / Controller", Opção A de transferência posterior e o exportador designado para as cláusulas 14-16. Nenhum dos outros quatro menciona Brasil ou LGPD na documentação pública (ver seção 8). Com eles, seria preciso pedir um aditivo com o Anexo II (plano enterprise) e não há garantia de aceitação.
2. **Consentimento específico e em destaque para a transferência (art. 33, VIII).** Como a base das fotos já é consentimento, acrescentar o consentimento de transferência no mesmo passo é natural: texto separado dizendo que as fotos serão enviadas a provedores nos EUA (nomeá-los), para a finalidade de geração, pelo prazo X, e que lá o nível de proteção é contratual. Fragilidades: revogável; não dispensa o Amorama de responder pelo que o importador fizer; e a ANPD trata a dispensa de consentimento como exceção. É o mecanismo possível para fal.ai/Replicate/Runway/Anthropic hoje.
3. **Art. 33, IX (necessidade para executar o contrato).** Cobre só o contratante e só se a transferência for necessária ao contrato, e a hipótese de base para dado sensível é o art. 11, não o art. 7º, V; não apostar nisso para as fotos.

**Decisão recomendada:** (a) usar Vertex AI (BR SCCs já incorporadas) como provedor de geração de vídeo; (b) para qualquer outro provedor que receba fotos, exigir aditivo com o Anexo II ou, enquanto não houver, apoiar a transferência no consentimento do art. 33, VIII, registrado por pessoa; (c) não enviar fotos ao Claude: só a Story, que já é dado pessoal mas não sensível por natureza, e também aí preferir DPA com cláusulas da ANPD ou o consentimento do art. 33, VIII; (d) publicar a seção de transferência internacional na Política de Privacidade com os campos do art. 17, § 2º; (e) preencher a cláusula 2 (categorias: "imagens faciais; dados sensíveis (biométricos)"; período: o mínimo configurado no provedor) e a Seção III (medidas de segurança) no contrato com cada importador.

## 8. Provedores: o que os documentos deles dizem (verificado em 2026-11-07)

Resumo do levantamento de documentação pública de cada provedor. "Não menciona" quer dizer que o termo não aparece nos documentos públicos consultados; pode haver cláusula em contrato enterprise.

| Provedor | Treina com inputs da API? | Retenção de inputs/outputs | Papel / DPA / Brasil | Política de uso (rostos, menores) | Subprocessadores |
|---|---|---|---|---|---|
| **fal.ai** ([privacy](https://fal.ai/privacy) 22/07/2026, [terms](https://fal.ai/terms) 08/09/2026, [DPA](https://fal.ai/legal/data-processing-addendum) 31/07/2026, [AUP](https://fal.ai/legal/acceptable-use-policy), [retenção](https://fal.ai/docs/documentation/model-apis/media-expiration)) | Self-serve: sem promessa explícita; fal é dona de "Usage Data" (anonimizada/agregada, "derived from Customer Input") e pode usá-la para desenvolver "AI models"; DPA §1.7.2 permite "Deidentified Data to improve the Services". Enterprise: "We never train our models on our enterprise customers' data" | "Request inputs and outputs are stored in the platform for 90 days by default"; header `X-Fal-Store-IO: 0` desliga o histórico; `X-Fal-Object-Lifecycle-Preference` controla expiração de arquivos no CDN; API para deletar payloads; ZDR só via vendas | Processor (DPA, EU SCCs Módulo 2, UK IDTA); servidores "United States and other countries"; **não menciona Brasil/LGPD** | Proíbe usar "name, image, voice, or other likeness without their consent", deepfakes, sexualização sem consentimento, CSAM; **AUP §7.1(vi) proíbe fazer upload de "Biometric data (such as facial recognition data...)"** (precisa de leitura jurídica: pode alcançar fotos de rosto); exige 18+ para usuários e End Users | lista em trust.fal.ai/subprocessors (não legível por fetch); modelos de terceiros "may apply their own safeguards" |
| **Replicate** ([privacy](https://replicate.com/privacy) 01/04/2026, [terms](https://replicate.com/terms) 01/04/2026, [retenção](https://replicate.com/docs/topics/predictions/data-retention)) | Sem declaração; licença para prover o serviço; "Resultant Data" agregada pode melhorar o serviço | API: "all input parameters, output values, output files, and logs are automatically removed after an hour, by default"; predições via web ficam indefinidamente; sem delete por API documentado; sem ZDR | Diz ser "processor" ou "service provider"; **sem DPA público, sem regiões, sem Brasil/LGPD**; enterprise "contact sales" | Proíbe nudez não consentida, impersonation, exploração infantil; termos de alguns modelos (Ideogram, Flux-Dev) proíbem upload de pessoas sem consentimento / "biometric processing" | não lista; "does not control [...] how the Marketplace Models use your Content" |
| **Runway** ([privacy](https://runway.com/privacy-policy) 23/10/2026, [terms](https://runway.com/terms-of-use) 23/10/2026, [enterprise terms](https://runway.com/enterprise-terms) 01/06/2026, [DPA PDF](https://runway.com/customer-data-processing-addendum.pdf) ago/2026, [usage policy](https://runway.com/safety/usage-policy) 06/03/2026, [subprocessadores](https://runway.com/customer-subprocessors/)) | **Termos de Uso §4.4: "Inputs and Outputs may be used by the Company to train and improve its AI models"**, licença perpétua, sem opt-out. Só os Enterprise Terms (§5.2) vedam treinamento. Não está claro sob qual dos dois uma chave de API self-serve cai | "no obligation to store any of Your Content"; retenção "as long as necessary"; enterprise: exportação 30 dias pós-término; sem delete por API nem ZDR documentados | Processor no DPA (EU SCCs, UK IDTA); AWS e GCP nos EUA; DPA lista como titulares "Individuals depicted in images, videos" e como dado sensível "facial image data"; **não menciona Brasil/LGPD** | Proíbe uso de imagem de outra pessoa sem permissão, NCII, impersonation, "Characters based on the face or voice of a person under the age of 18"; moderação automática em toda requisição da API; usuários 13+ | 30 subprocessadores, vários "Output generation (conditional)": OpenAI, Black Forest Labs, Kling (Singapura), Byteplus (Singapura), fal, Ideogram, Meta, Google; Anthropic e Hive para moderação |
| **Google Veo via Gemini API / AI Studio** ([terms](https://aistudio.google.com/docs/terms) 23/03/2026, [usage policies](https://aistudio.google.com/docs/usage-policies)) | Tier gratuito: usa conteúdo para "improve, and develop Google products [...] and machine learning technologies", com revisão humana; **"Do not submit sensitive, confidential, or personal information to the Unpaid Services"**. Tier pago: não treina | Pago: logs de prompts e respostas por 55 dias para abuso; sem ZDR | Pago: DPA de processor; dados "stored transiently or cached in any country"; sem residência; **não menciona Brasil/LGPD** | Exige 18+; a página de vídeo diz que "Veo 3.1 Preview in the Gemini API has been shut down" (22/10/2026) e aponta para Gemini Omni, que "does not support" upload/edição de imagens de "certain recognizable people" e bloqueia menores em EEE/UK/CH; SynthID em todos os vídeos | não publicado nessas páginas |
| **Google Veo via Vertex AI** ([data governance](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance), [abuse monitoring](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/abuse-monitoring), [Cloud DPA](https://cloud.google.com/terms/data-processing-addendum), [BR SCCs C2P](https://cloud.google.com/sccs/br-c2p), [residência](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency), [Veo image-to-video](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-an-image), [Responsible AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/responsible-ai-and-usage-guidelines), [Prohibited Use Policy](https://policies.google.com/terms/generative-ai/use-policy) 17/12/2024) | "Google won't use your data to train or fine-tune any AI/ML models without your prior permission or instruction" | Prompts só são logados quando sinalizados por abuso, "up to 90 days", com revisão humana possível; output de Veo vai para bucket do cliente (`storageUri`) ou volta na resposta; ZDR por pedido à conta | Processor (Cloud DPA, 23/10/2025); **Apêndice 3 tem seção Brasil com "BR SCCs" = cláusulas-padrão da ANPD, incorporadas automaticamente quando há "BR Restricted Transfers"**; Veo 3.1 roda em `us-central1`; southamerica-east1 não tem Veo | `personGeneration`: `allow_adult` (padrão) ou `disallow`; filtro de criança rejeita geração de menores salvo allowlist; filtro de celebridade; proíbe NCII, impersonation enganosa, conteúdo sexual explícito, biometria sem consentimento legal; SynthID + C2PA | lista em cloud.google.com/terms/subprocessors (não legível por fetch) |
| **Anthropic Claude API** ([commercial terms](https://www.anthropic.com/legal/commercial-terms) 17/06/2025, [DPA](https://www.anthropic.com/legal/data-processing-addendum) 24/02/2025, [retenção comercial](https://privacy.claude.com/en/articles/7996866) 01/07/2026, [ZDR e modelos cobertos](https://support.claude.com/en/articles/15425695) 01/09/2026, [residência](https://platform.claude.com/docs/en/manage-claude/data-residency), [AUP](https://www.anthropic.com/legal/aup)) | "Anthropic may not train models on Customer Content from Services" | Inputs/outputs apagados "within 30 days"; conteúdo sinalizado até 2 anos; ZDR por organização via vendas, mas os "Covered Models" (Fable 5/5.1, Mythos 5/5.1) "require 30-day data retention; ZDR is therefore not available" | Processor; EU SCCs Módulos 2/3, UK e Swiss addenda; `inference_geo` "global" ou "us"; **DPA não menciona LGPD** (a Política de Privacidade de consumidor cita SCCs aprovadas pela ANPD, mas não é o instrumento da API) | Proíbe impersonation enganosa, NCII, CSAM, "biometric or neural data (including facial recognition)" e rastreamento sem consentimento | lista em trust.anthropic.com/subprocessors (não legível por fetch) |

Conclusões para o pipeline:

- **Vertex AI** é o único com (i) não treinamento contratual, (ii) cláusulas-padrão da ANPD já no DPA e (iii) controles explícitos de pessoas/menores. Custo: processamento nos EUA (não há Veo em São Paulo) e abuse logging de prompts sinalizados.
- **fal.ai** só é viável com `X-Fal-Store-IO: 0`, lifecycle curto no CDN, delete por API após cada Order, plano com cláusula de não treinamento, e depois de esclarecer com eles o §7.1(vi) do AUP (upload de "biometric data"), porque na leitura literal fotos de rosto para gerar likeness podem violar o AUP.
- **Replicate** tem a melhor retenção padrão (1 h), mas nenhum DPA público, nenhuma menção a transferência internacional e repasse opaco a donos de modelos; só com DPA enterprise que inclua o Anexo II.
- **Runway** self-serve é incompatível com "nunca treinamos com suas fotos" (Termos §4.4) e tem cadeia longa de subprocessadores que recebem inputs; só em Enterprise Terms.
- **Gemini API** tier gratuito está fora de cogitação (treina e pede para não enviar dado pessoal); o tier pago é aceitável para texto, mas para vídeo com pessoas a própria Google desligou Veo na Gemini API e restringe pessoas reconhecíveis no sucessor.
- **Claude** deve receber só a Story e o Script, nunca as fotos; mesmo assim incluir a transferência da Story na seção de transferência internacional.

## 9. Segurança, incidentes e governança

- Art. 46 (medidas técnicas e administrativas) e § 2º (privacy by design); art. 47 (sigilo mesmo após o término); art. 37 (registro das operações); art. 38 (relatório de impacto, que a ANPD pode pedir); art. 42 (responsabilidade do controlador e do operador).
- Res. CD/ANPD 15/2024 (incidentes): comunicação à ANPD e aos titulares em 3 dias úteis quando o incidente "possa acarretar risco ou dano relevante" e envolva, entre outros critérios, "dados pessoais sensíveis" ou "dados de crianças, de adolescentes ou de idosos" (art. 5º); prazo em dobro para pequeno porte (art. 6º, § 8º), salvo se for alto risco; registro de incidentes por 5 anos (art. 10). Fotos de rosto vazadas são incidente comunicável por definição. ([texto da resolução, legisweb](https://www.legisweb.com.br/legislacao/?id=458235); DOU 26/04/2024)
- Res. CD/ANPD 2/2022: pequeno porte dispensa encarregado (art. 11), mas exige canal de comunicação com o titular (§ 1º); registro simplificado (art. 9º); política de segurança simplificada (art. 13). Como o Amorama provavelmente é alto risco (seção 1), planejar como se as flexibilizações não valessem: nomear encarregado (é "boa prática" para dosimetria, art. 11, § 2º), manter ROPA, escrever RIPD curto.
- Cadeia de operadores: os provedores são operadores (art. 5º, VII; art. 39) e seus subprocessadores são suboperadores; o guia da ANPD recomenda contrato que fixe "objeto, a duração, a natureza e a finalidade do tratamento dos dados, os tipos de dados pessoais envolvidos e os direitos e obrigações" e ciência ao controlador sobre suboperadores. ([gov.br/anpd, Guia de Agentes de Tratamento v2.0](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado))
- Direito penal relevante para moderação: CP art. 216-B, parágrafo único (montagem para incluir pessoa em cena de nudez/sexo); art. 218-C, cuja pena passou a 4 a 10 anos pela Lei 15.280/2025 ([planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15280.htm)); Lei 15.123/2025 (agravante de IA na violência psicológica contra a mulher, CP art. 147-B). O Amorama não gera nada disso por design (Script fixo, House Style, sem prompt livre), mas a moderação deve bloquear Story e fotos com conteúdo sexual e qualquer tentativa de usar pessoa pública.

## 10. Checklist para o ticket de termos e moderação

### A. Consentimento e fluxo

- [ ] Consentimento destacado **por pessoa** (art. 8º, § 1º; art. 11, I), em tela própria, não embutido no aceite dos termos. Texto nomeia a finalidade (gerar Character Sheets, Scenes e Final Video deste Order no House Style), os dados (fotos de rosto, consideradas dado sensível), os destinatários (provedores, por nome e país), os prazos e o canal de revogação.
- [ ] Segundo consentimento destacado, separado, para a **transferência internacional** (art. 33, VIII), usado quando o provedor não tiver as cláusulas-padrão da ANPD no contrato.
- [ ] **Partner Link**: nenhuma foto do parceiro sai do Amorama antes do consentimento dele; quarentena cifrada com expiração (7 dias); recusa elimina as fotos e avisa o uploader.
- [ ] Checkbox contratual do uploader: fotos próprias e do parceiro; parceiro ciente; ambos 18+; responsabilidade por falsidade e direito de regresso.
- [ ] Declaração 18+ de cada pessoa no respectivo consentimento.
- [ ] Registro de consentimento: Order, pessoa, versão do texto, timestamp, IP/user-agent, hash das fotos; guardado 5 anos após a eliminação dos dados.
- [ ] Revogação em um clique pelo Order Link ou Partner Link; efeito: parar geração, eliminar fotos/Character Sheets/Scenes/Final Video daquela pessoa, acionar delete nos provedores, confirmar por e-mail.
- [ ] Aviso de alteração de política com destaque (art. 8º, § 6º) e novo consentimento se mudar finalidade, destinatários ou prazos.

### B. Termos de Uso

- [ ] Serviço exclusivo para maiores de 18 anos; Couple = duas pessoas adultas; proibido enviar fotos de menores, de terceiros sem consentimento ou de pessoas públicas.
- [ ] Descrição do que é gerado (likeness estilizada, não fotorrealista) e de que o resultado é conteúdo sintético; o Amorama pode marcar o Final Video como gerado por IA (SynthID/C2PA já vêm do Veo).
- [ ] Licença: o Couple recebe o Final Video para uso pessoal; o Amorama não usa fotos, Character Sheets, Scenes ou Final Video para marketing, portfólio ou treinamento sem consentimento específico separado.
- [ ] Regenerations, prazos de entrega e o que acontece se um dos dois revogar ou recusar (cancelamento, política de reembolso).
- [ ] Moderação: direito de recusar Order por conteúdo sexual, violento, com menores, pessoas públicas ou indícios de falta de consentimento; sem reembolso em caso de violação dolosa (validar com advogado consumerista).
- [ ] Foro e lei brasileira; canal de atendimento; prazo de resposta.

### C. Política de Privacidade (arts. 9º e 18; Res. 19/2024, art. 17, § 2º)

- [ ] Identificação e contato do controlador e do encarregado (ou canal equivalente).
- [ ] Dados tratados por categoria, com as fotos marcadas como dado sensível; finalidade específica de cada um; base legal de cada um (tabela da seção 2).
- [ ] Seção destacada "Transferência internacional": forma, duração e finalidade; **países de destino** (EUA e os que cada provedor declarar); provedores nomeados; mecanismo (cláusulas-padrão da ANPD ou consentimento); responsabilidades e medidas de segurança; direitos e canal; direito de peticionar à ANPD; como pedir a íntegra das cláusulas (15 dias).
- [ ] Prazos de retenção numéricos (tabela da seção 6), incluindo o que fica nos provedores.
- [ ] Promessa de não treinamento, com a ressalva honesta de que só se usam provedores com compromisso contratual equivalente.
- [ ] Direitos do art. 18 enumerados, como exercer, prazo (15 dias), gratuidade, possibilidade de recusa de consentimento e consequências (art. 18, VIII), exercício separado por cada pessoa do Couple.
- [ ] Compartilhamento: lista de operadores (provedores de geração, e-mail, pagamento, hospedagem) e seus países.
- [ ] Incidentes: compromisso de comunicar titulares e ANPD nos prazos da Res. 15/2024.
- [ ] Cookies/analytics conforme o Guia de Cookies da ANPD, se houver.
- [ ] Versão e data; histórico de alterações.

### D. Configurações técnicas e contratuais por provedor

- [ ] Vertex AI: projeto com Cloud DPA aceito (BR SCCs ativas); `personGeneration = allow_adult` (nunca `allow_all`); output para bucket próprio em região controlada com lifecycle curto; request-response logging desligado; pedir ZDR à conta; anotar `us-central1` como país de destino.
- [ ] fal.ai (se usado): plano com cláusula de não treinamento; `X-Fal-Store-IO: 0` em toda requisição; `X-Fal-Object-Lifecycle-Preference` com expiração de horas; delete de payloads e arquivos CDN ao fechar o Order; esclarecimento escrito sobre AUP §7.1(vi); aditivo com Anexo II da Res. 19/2024.
- [ ] Replicate (se usado): só via API (1 h de retenção), nunca pelo painel web; DPA enterprise com Anexo II; checar termos do modelo específico quanto a upload de pessoas.
- [ ] Runway (se usado): só sob Enterprise Terms (§5.2 veda treinamento) com DPA; revisar quais subprocessadores de "output generation" o modelo escolhido aciona; `contentModeration` padrão.
- [ ] Anthropic: só Story/Script, nunca fotos; `inference_geo = "us"` para fixar país de destino; pedir aditivo LGPD ou cobrir pelo consentimento do art. 33, VIII; registrar que a retenção é 30 dias e que ZDR não vale para os modelos cobertos.
- [ ] Para cada importador: preencher cláusula 2 (categorias, período de armazenamento) e Seção III (medidas de segurança) quando houver cláusulas-padrão; anotar transferências posteriores (cláusula 3/18) a partir da lista de subprocessadores.
- [ ] Nunca usar tiers gratuitos/"unpaid" de nenhum provedor com dados do Couple.

### E. Moderação de entrada e saída

- [ ] Fotos: rejeitar menores aparentes, nudez, mais de uma pessoa por foto quando não for o Couple, pessoas públicas; registrar motivo da rejeição sem guardar a foto.
- [ ] Story/Script: filtro para conteúdo sexual explícito, violência, ódio, menção a terceiros identificáveis fora do Couple; Script gerado só a partir de templates do House Style.
- [ ] Saída: revisão humana (Concierge Mode) de Character Sheets e Scenes antes da Approval; bloquear qualquer Scene que fuja do House Style para fotorrealismo.
- [ ] Canal de denúncia na página pública do Order Link ("não autorizei o uso da minha imagem"), com remoção em até 24 h e eliminação total.

### F. Governança interna

- [ ] ROPA (registro simplificado, modelo da ANPD) cobrindo o fluxo fotos → provedores → entrega.
- [ ] RIPD curto (art. 38) justificando a classificação como sensível, as bases, a transferência e a retenção.
- [ ] Teste de "acesso provável" do ECA Digital documentado.
- [ ] Plano de resposta a incidentes com prazo de 3 dias úteis e registro de 5 anos.
- [ ] Logs de acesso por 6 meses (Marco Civil art. 15), separados das fotos.
- [ ] Encarregado nomeado e publicado (mesmo que dispensável).
- [ ] Revisar esta pesquisa quando a ANPD publicar a norma de dados biométricos (prevista para 2026).

## Fontes (acessadas em 2026-11-07)

Lei e regulação:

- Lei 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Código Civil, arts. 3º-5º, 11, 20, 21: https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
- Marco Civil da Internet, art. 15: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm
- Lei 15.211/2025 (ECA Digital): https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm
- Lei 15.280/2025 (penas dos crimes sexuais, art. 218-C): https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15280.htm
- Resolução CD/ANPD 19/2024 (transferência internacional e cláusulas-padrão): https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-19-de-23-de-agosto-de-2024-580095396
- Resolução ANPD 32/2026 (adequação da União Europeia): https://www.in.gov.br/web/dou/-/resolucao-n-32-de-26-de-janeiro-de-2026-683334547
- Página da ANPD sobre transferência internacional: https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados
- Resolução CD/ANPD 2/2022 (agentes de pequeno porte): https://in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-2-de-27-de-janeiro-de-2022-376562019
- Resolução CD/ANPD 15/2024 (incidentes): https://www.legisweb.com.br/legislacao/?id=458235
- Enunciado CD/ANPD 1/2023: https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-divulga-enunciado-sobre-o-tratamento-de-dados-pessoais-de-criancas-e-adolescentes/Enunciado1ANPD.pdf/@@display-file/file
- Nota Técnica 4/2026 ANPD (reconhecimento facial, escolas do Paraná): https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos/nota_tecnica_4_versao_publica-educacao_parana.pdf/@@display-file/file
- Tomada de subsídios sobre dados biométricos (ANPD, 02/06/2025): https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-abre-tomada-de-subsidios-sobre-tratamento-de-dados-biometricos
- Guia Orientativo Legítimo Interesse (ANPD, 2024): https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse
- Guia Orientativo Agentes de Tratamento e Encarregado v2.0 (ANPD, 2022): https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado
- Guia Orientativo ECA Digital: escopo e obrigações gerais (ANPD, out/2026): https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-fornecedores-de-produtos-ou-servicos-de-tecnologia-da-informacao.pdf/@@display-file/file
- Guia de Segurança da Informação para agentes de pequeno porte e modelo de ROPA (ANPD): https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte
- Súmula 403 do STJ: https://arquivocidadao.stj.jus.br/index.php/sumula-403

Provedores: URLs na tabela da seção 8.

Limitações: as páginas de subprocessadores de fal.ai, Google Cloud e Anthropic são renderizadas em JS e não puderam ser lidas; o PDF do Radar Tecnológico vol. 2 não foi localizado no portal da ANPD; o texto completo da Nota Técnica da ANPD com o resultado da tomada de subsídios de biometria (dez/2025) não foi consultado. A norma da ANPD sobre biometria, prevista para 2026, pode alterar a seção 1.
