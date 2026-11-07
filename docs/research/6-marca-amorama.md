# Pesquisa: disponibilidade da marca "Amorama" (INPI, WIPO, domínios)

- **Ticket:** [#6](https://github.com/victor160997/amorama/issues/6)
- **Data da consulta:** 2026-11-07 (todas as buscas foram feitas neste dia; INPI carimbou os resultados com 07/11/2026 18:38–18:45, horário de Brasília)
- **Pergunta:** Existe registro ou pedido de marca "Amorama" (ou colidente) no INPI nas classes relevantes (41 entretenimento/produção de vídeo, 42 SaaS, eventualmente 9 e 35) e na base global da WIPO? Os domínios amorama.com / .com.br / .app estão livres? Recomendação: seguir, registrar já, ou sinal de alerta.

## Resumo

| Frente | Resultado | Fonte primária |
|---|---|---|
| INPI, busca exata "amorama" | **Nenhum resultado** | busca.inpi.gov.br (Pesquisa Básica, tipo Exata) |
| INPI, busca radical "amorama" | 57 processos; **1 colidente direto em vigor: "AMORAMA AROMAS", NCL 35** (titular pessoa física); nenhum nas classes 9, 41, 42 | busca.inpi.gov.br (Pesquisa Básica, tipo Radical) |
| INPI, variantes amoramma / amo rama / amo-rama / amoramas | Nenhum resultado novo além dos já listados | busca.inpi.gov.br |
| WIPO Global Brand Database / Madrid Monitor | **Não foi possível consultar** (desafio anti-bot ALTCHA; Madrid Monitor proíbe consulta automatizada). TMview (EUIPO) também bloqueou o acesso | branddb.wipo.int, www3.wipo.int/madrid/monitor |
| amorama.com | **Registrado** desde 2008-08-11 via Corsearch Domains (registrador de proteção de marca); redireciona para adorama.com (loja Adorama, EUA) | rdap.verisign.com |
| amorama.com.br | **Registrado** desde 2021-10-30 por pessoa física (Antonio Carlos Catani Neto); aponta para loja Shopify que responde "Store unavailable" | rdap.registro.br |
| amorama.app | **Registrado** em 2026-09-23 via Cloudflare; **site ativo em PT-BR vendendo "livro do casal" digital para aniversário de namoro/casamento**, operado por TEMQT Sistemas (CNPJ 21.993.101/0001-80, Salvador/BA) | pubapi.registry.google (RDAP), https://amorama.app |
| Web (empresas/apps "Amorama") | Nenhum app ou empresa indexado com o nome exato além de: associação portuguesa de pais (Amadora, PT) e o próprio amorama.app (ainda não indexado) | buscas web, ver seção 5 |

**Veredito curto:** sinal de alerta amarelo. Não há impedimento registral nas classes 41/42 no INPI (a única marca "Amorama" em vigor é "AMORAMA AROMAS", classe 35, de outro segmento), mas (a) os três domínios óbvios estão tomados e (b) já existe um produto brasileiro chamado **Amorama** em **amorama.app**, lançado há ~6 semanas, no **mesmo nicho** (presente digital personalizado para casais a partir de fotos e texto). Se esse site não for do próprio time, é colisão direta de marca de fato (uso anterior, art. 129 §1º da LPI, direito de precedência) e o nome deve ser repensado antes de qualquer investimento em marca. Ver seção 6.

---

## 1. INPI (busca.inpi.gov.br)

### 1.1 Método

A busca pública do INPI exige sessão (cookie JSESSIONID). Sem sessão o servlet devolve "Banco de Marcas inacessível momentaneamente. Erro: java.sql.SQLException: Null SQL statement". Fluxo que funcionou:

1. `GET https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login` (cria a sessão anônima)
2. `GET https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_classe_basica.jsp` (formulário "Pesquisa Básica")
3. `POST https://busca.inpi.gov.br/pePI/servlet/MarcasServletController` com `Action=searchMarca`, `tipoPesquisa=BY_MARCA_CLASSIF_BASICA`, `marca=<termo>`, `buscaExata=sim|nao`, `classeInter=` (vazio = todas as classes), `registerPerPage=100`.

Observações de método:
- O INPI aplica WAF/limite de taxa: requisições paralelas na mesma sessão devolveram HTTP 403; as buscas foram repetidas sequencialmente, cada uma em sessão nova, e todas retornaram HTTP 200.
- A página de detalhe de cada processo (`Action=detail&CodPedido=...`) devolveu uma página de erro do WAF (30 KB, sem dados) em todas as tentativas; os dados abaixo vêm da **tabela de resultados** (número, prioridade, marca, situação, titular, classe), que o INPI exibe diretamente.
- A busca "Radical" do INPI é fonética/aproximada, não substring: a mesma lista de 57 processos saiu para "amorama", "amo rama" e "amo-rama".
- Não há URL permanente de resultado (é POST com sessão). Para reproduzir: https://busca.inpi.gov.br/pePI/ → Marca → Pesquisa Básica → marca = `amorama`, tipo Radical, classe em branco.

### 1.2 Busca exata "amorama" (todas as classes)

> RESULTADO DA PESQUISA (07/11/2026 às 18:38:13) Marca: amorama - Nenhum resultado foi encontrado para a sua pesquisa.

Repetida às 18:45:40 em sessão nova, mesmo resultado. **Não existe pedido nem registro da marca nominativa exata "AMORAMA" no INPI.**

### 1.3 Busca radical "amorama" (todas as classes) — 57 processos

Processos cuja marca contém o radical "amorama"/"amoram" ou é foneticamente próxima. Os relevantes para colisão:

| Processo | Prioridade | Marca | Situação (07/11/2026) | Titular | Classe NCL |
|---|---|---|---|---|---|
| **933696620** | 29/02/2024 | **AMORAMA AROMAS** | **Registro de marca em vigor** | SOLANGE ANDREA BOHN | **35** |
| 939820110 | 02/07/2025 | AMORAMAR | Aguardando exame de mérito | FERNANDO LUIZ GOMES FILHO | 43 |
| 914583840 | 26/04/2018 | Lamorama | Registro de marca em vigor | TARCILA DE ALMEIDA MARCAL AVELAR | 25 |
| 909843864 | 17/08/2015 | AMORAMATTE | Pedido definitivamente arquivado | MANUELA ROCHA | 25 |
| 904555100 | 27/02/2012 | Amoramais Comunicação | Pedido definitivamente arquivado | AMORAMAIS EDIÇÃO MARKETING E COMUNICAÇÃO LTDA | 35 |
| 813282659 | 13/02/1987 | GLAMORAMA | Arquivado | FINAX IMOVEIS E ASSESSORIA S/C LTDA | 40:10 (classificação antiga) |

Os outros 51 processos são "AMORA ..." (Amora Makeup, Amora Maria, Amora Macaron, Amora Magazine, Amora maker etc.), "AMOR A ..." / "AMOR À MASSA", "AMOR AMAZÔNIA", "AA AMOR AMADO", "POR AMOR A MALAWI", "Puro Amor Amamentação" e 14 pedidos da "Associação Beneficente Reviver Help Deus é Amor Amando e Cuidando" — distantes grafica e semanticamente, em classes de alimentos, cosméticos, vestuário, serviços beneficentes. Não afetam 41/42.

Leitura por classe de interesse:
- **Classe 41 (entretenimento, produção de vídeo/animação): nenhum processo.**
- **Classe 42 (SaaS, software): nenhum processo.**
- **Classe 9 (software baixável): nenhum processo.**
- **Classe 35 (publicidade, comércio): "AMORAMA AROMAS" em vigor** (reg. 29/02/2024). Segmento de aromas/perfumaria; afinidade mercadológica baixa com vídeo animado para casais, mas é o mesmo núcleo distintivo "AMORAMA" e pode ser citado em exame se o pedido do time incluir classe 35 (ex.: "serviços de comércio eletrônico", "publicidade"). Risco de oposição: baixo a moderado, só se houver pedido em 35.
- "AMORAMAR" (classe 43, alimentação/hospedagem), pendente desde 07/2025: afinidade nula com 41/42.

### 1.4 Variantes

| Termo | Tipo | Resultado |
|---|---|---|
| amoramma | Radical | Nenhum resultado (18:44:48) |
| amo rama | Radical | Mesmos 57 processos de "amorama" |
| amo-rama | Radical | Mesmos 57 processos de "amorama" |
| amoramas | Radical | 4 processos, todos "AMOR À MASSA"/"MORAMASSA" (classes 30 e 32), irrelevantes |

Não foram encontradas marcas "Amorama's" ou "Amoramas" próprias. **Nenhuma variante colide nas classes 9, 41 ou 42.**

## 2. WIPO Global Brand Database e Madrid Monitor

- **branddb.wipo.int**: toda requisição (incluindo `https://branddb.wipo.int/en/quicksearch?by=brandName&v=amorama` e o antigo endpoint `branddb/jsp/select.jsp`) devolve uma página com desafio anti-bot **ALTCHA** antes de liberar a aplicação; sem resolver o desafio em navegador não há dados. **Não foi possível consultar a base global por esta via.**
- **Madrid Monitor** (`https://www3.wipo.int/madrid/monitor/en/`): a página de ajuda informa que não há API pública e que os termos de uso proíbem consulta automatizada; a interface é renderizada por JavaScript. **Não consultado.**
- **TMview (EUIPO, `tmdn.org`)**, tentado como alternativa que agrega INPI-BR e dezenas de escritórios: o WAF devolveu "Request Rejected" tanto via curl quanto via fetch. **Não consultado.**

Como a questão principal (Brasil) foi respondida direto na fonte primária (INPI), a lacuna é apenas internacional. Sinal secundário (fraco, não primário): buscas web em agregadores de marcas dos EUA (Justia, Markinton, TrademarkDir) não retornaram nenhuma marca "AMORAMA"; os resultados são todos "AMORA" (Unilever, classe 30; Amora International; Amora LLC etc.) e "ADORAMA" (Adorama Inc.). Fontes: https://trademark.justia.com/owners/adorama-inc-623539, https://markinton.com/trademark/amora-87233424, https://trademarkdir.com/owner/amora-international-ltd.

**Pendência:** fazer a busca manual em https://branddb.wipo.int/en/quicksearch?by=brandName&v=amorama (filtro: designação BR e, se o produto for internacional, US/EM) em um navegador. Leva ~2 minutos. Se o nome for mantido, vale fazer antes do depósito.

## 3. Domínios

WHOIS via CLI não estava disponível no ambiente; usou-se **RDAP** (protocolo oficial sucessor do WHOIS, servido pelos próprios registros) mais DNS e HTTP.

### 3.1 amorama.com — registrado (desde 2008)

Fonte: https://rdap.verisign.com/com/v1/domain/amorama.com (consultado 2026-11-07)

- Registrador: **Corsearch Domains LLC** (IANA 642), empresa de proteção de marcas/anti-typosquatting.
- Registro: 2008-08-11; expiração: 2027-08-11; última alteração: 2026-07-11.
- Status: clientDeleteProhibited, clientTransferProhibited (travado pelo registrador).
- DNS: resolve para 5.22.145.121; `http://amorama.com/` redireciona para `https://www.adorama.com/?clickref=...&utm_medium=affiliate` (Adorama, varejista de fotografia dos EUA), atrás de proteção anti-bot DataDome.

Interpretação: domínio defensivo da Adorama (typo de "adorama"). Praticamente indisponível para compra; abordagem de compra tende a ser ignorada ou cara.

### 3.2 amorama.com.br — registrado (desde 2021)

Fonte: https://rdap.registro.br/domain/amorama.com.br (consultado 2026-11-07); equivalente à consulta WHOIS em https://registro.br/tecnologia/ferramentas/whois/?search=amorama.com.br

- Titular: **Antonio Carlos Catani Neto** (pessoa física, CPF parcialmente mascarado), contato administrativo handle ACCNE102.
- Registro: 2021-10-30; última alteração: 2022-06-07; DNSSEC assinado (DS registrado em 2025-02-21, ou seja, o domínio segue sendo mantido).
- DNS: `amorama.com.br` → 23.227.38.65 e `www.amorama.com.br` → `shops.myshopify.com` (Shopify). `https://amorama.com.br/` devolve HTTP 404 "Store unavailable" (loja Shopify desativada ou nunca publicada).

Interpretação: domínio parado nas mãos de pessoa física há 5 anos, sem uso ativo. É o único dos três com chance realista de aquisição por negociação direta (o RDAP expõe e-mail do contato administrativo). Nenhum registro de marca associado foi encontrado no INPI com esse titular.

### 3.3 amorama.app — registrado (2026-09-23) e EM USO no mesmo nicho

Fonte RDAP: https://pubapi.registry.google/rdap/domain/amorama.app (registro .app é da Google Registry; consultado 2026-11-07)

- Registrador: **Cloudflare, Inc.** (IANA 1910). Registro: **2026-09-23**; expiração: 2027-09-23. Status: clientTransferProhibited. NS: algin/melody.ns.cloudflare.com.

Fonte do conteúdo: https://amorama.app/ (HTTP 200, 102 KB, consultado 2026-11-07)

- `<title>`: "Amorama — livro do casal para aniversário de namoro e de casamento".
- Meta description: "Monte antes de pagar, em 10 minutos, um livro com as fotos e as palavras de vocês. A partir de R$ 29, só no fim. Entregue o QR na mão ou mande o link lacrado."
- Produto: livro digital do casal montado a partir de 3–6 "momentos" (fotos + dedicatórias), entregue por QR code/link privado, com contador de dias, quadro A4 imprimível, cards para redes sociais, opcional de áudio e música. Planos R$ 29 e R$ 39, pagamento único via Mercado Pago (Pix/cartão), garantia de 14 dias. O site diz que "o capítulo ilustrado, que usa IA para o dia sem foto, entra depois do lançamento".
- Operador declarado no rodapé: **"A Amorama é operada pela TEMQT Sistemas · CNPJ 21.993.101/0001-80"**; contato `contato@amorama.app`; Instagram https://www.instagram.com/amorama.app/ (não foi possível ler o perfil: o Instagram bloqueia acesso sem login).
- CNPJ 21.993.101/0001-80 (fonte: https://brasilapi.com.br/api/cnpj/v1/21993101000180, que espelha a Receita Federal): razão social **JEAN DANIEL SAMPAIO SILVA TEMQT SISTEMAS**, nome fantasia TEMQT SISTEMAS, ativa desde 2015-03-05, Salvador/BA, CNAE "Suporte técnico, manutenção e outros serviços em tecnologia da informação".

Interpretação: é um produto brasileiro, em português, com o nome exato "Amorama", vendendo presente digital personalizado para casais a partir de fotos e texto do casal — o mesmo público, a mesma ocasião (aniversário de namoro/casamento) e um formato adjacente ao vídeo animado descrito no GLOSSARY.md deste repositório. O domínio tem seis semanas e o site ainda não está indexado em buscadores (nenhum hit para "amorama.app" ou "TEMQT" nas buscas da seção 5).

**Atenção:** a proximidade do conceito (fotos + história do casal → presente digital, com "capítulo ilustrado por IA" prometido) sugere que **pode ser a landing page do próprio time** deste repositório, ou de alguém muito próximo. Isso precisa ser confirmado pelo dono do projeto antes de qualquer decisão. Se for do time: os achados de domínio viram "já temos o .app" e a recomendação muda (ver seção 6). Se **não** for do time: é o achado mais grave desta pesquisa.

## 4. Síntese sobre colisão (visão leiga, não é parecer jurídico)

- No INPI, para as classes 41 e 42 (e 9), o caminho está livre: nenhum pedido ou registro com "Amorama" ou variante.
- "AMORAMA AROMAS" (classe 35, em vigor desde 2024) é o único registro com o mesmo núcleo. Afinidade de mercado baixa; só pesa se o pedido incluir classe 35.
- O Brasil adota o sistema atributivo (quem deposita primeiro leva), mas a Lei 9.279/96, art. 129 §1º, dá **direito de precedência** a quem, de boa-fé, já usava no país há pelo menos 6 meses marca idêntica ou semelhante para produto/serviço idêntico, semelhante ou afim. Se a Amorama de amorama.app for de terceiro e estiver em uso desde ~09/2026, ela completa 6 meses em ~03/2027 e passa a poder opor esse direito a um depósito do time. Fonte da regra: http://www.planalto.gov.br/ccivil_03/leis/l9279.htm (art. 129).
- Também vale o inverso: se o time depositar primeiro, é o terceiro quem terá de brigar; mas a convivência de dois "Amorama" para casais no Brasil, com o terceiro já segurando o .app e o Instagram @amorama.app, gera confusão de mercado independentemente do registro.

## 5. Buscas web por empresas/apps "Amorama" (2026-11-07)

Consultas: `"Amorama" empresa OR app OR marca`; `"Amorama" trademark OR brand OR company`; `"amorama.com.br" OR "Amorama Aromas" OR "amorama.com"`; `Amorama aromas Brasil loja OR instagram OR shopify`; `"Amorama" app casais OR couples OR vídeo OR animação`; `"amorama.app" OR "Amorama" TEMQT`.

Resultados com o nome exato:
- **Amorama – Associação de Pais e Amigos das Crianças Deficientes Profundos**, Amadora, Portugal (ONG; portal de contratação pública): https://anogov.com/ap-amorama/faces/app/dashboard.jsp. Sem relação de mercado.
- Nenhum app em lojas (App Store/Google Play), nenhuma empresa, nenhuma marca estrangeira chamada "Amorama" apareceu. O ruído é todo "Amora" (app de companhia por IA e app de casais, https://play.google.com/store/apps/details?id=com.amorasoulmate ; https://mwm.ai/apps/amora/6753182194), "Adorama" (loja de fotografia, dona de amorama.com) e "Amaro" (moda).
- amorama.app e "Amorama Aromas" **não** estão indexados em nenhum buscador consultado: só foram encontrados por RDAP/DNS e INPI, respectivamente.

Nicho (para contexto competitivo, não colisão de nome): LovePanda (https://lovepanda.co/) vende "retrospectiva do casal" animada a partir de fotos e música por link/QR; Dentro da História vende e-book personalizado de casal. Nenhum usa nome parecido.

## 6. Recomendação

**Sinal de alerta (amarelo forte), condicionado a uma pergunta de 1 minuto para o dono do projeto: amorama.app / TEMQT Sistemas é do time?**

**Caso A — amorama.app NÃO é do time:**
- Trocar o nome antes de investir em marca, domínio e identidade. Há um concorrente brasileiro de mesmo nome, mesmo público, mesma ocasião de compra, com o .app e o @amorama.app em uso; os dois outros domínios óbvios estão tomados (um por brand protection da Adorama, outro parado desde 2021). Registrar "Amorama" em 41/42 seria juridicamente possível hoje, mas compraria uma disputa (precedência do art. 129 §1º a partir de ~03/2027) e confusão de mercado desde o dia 1.
- Não bloqueia a spec: o nome segue provisório no código/docs, como o ticket já previa.

**Caso B — amorama.app É do time (ou de sócio):**
- Caminho livre no INPI para 41 e 42: **depositar agora** a marca nominativa "AMORAMA" (ou mista, com logo) nas classes **41** (produção de vídeo/animação, entretenimento) e **42** (SaaS), e avaliar **9** (app baixável) se houver app. Evitar incluir a classe 35 ou redigir a especificação de 35 longe de "aromas/perfumaria" para não esbarrar em "AMORAMA AROMAS" (933696620). Valores por classe (pedido + concessão, com desconto para ME/EPP/MEI/pessoa física) estão na tabela de retribuições do INPI: https://www.gov.br/inpi/pt-br/servicos/tabelas-de-retribuicao (não verificada nesta pesquisa). Depositar cedo fixa a prioridade antes que terceiros (ex.: dono de amorama.com.br) se movam.
- Antes do depósito, fazer a busca manual na WIPO (seção 2, 2 minutos) e, se possível, uma busca de anterioridade com agente de PI para checar marcas figurativas e fonéticas que a Pesquisa Básica não cobre.
- Domínios: manter o .app; tentar negociar **amorama.com.br** com o titular (parado, pessoa física, e-mail no RDAP); desistir do **.com** (defensivo da Adorama).

Em ambos os casos, não é necessário renomear nada no repositório agora.

## Fontes consultadas (todas em 2026-11-07)

- INPI, Consulta à Base de Dados — Marcas: https://busca.inpi.gov.br/pePI/ (Pesquisa Básica: `https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_classe_basica.jsp`; servlet `https://busca.inpi.gov.br/pePI/servlet/MarcasServletController`)
- WIPO Global Brand Database: https://branddb.wipo.int/en/quicksearch?by=brandName&v=amorama (bloqueado por ALTCHA)
- WIPO Madrid Monitor: https://www3.wipo.int/madrid/monitor/en/ (sem API pública; JS)
- EUIPO TMview: https://www.tmdn.org/tmview/ (WAF "Request Rejected")
- RDAP .com (Verisign): https://rdap.verisign.com/com/v1/domain/amorama.com
- RDAP .br (Registro.br): https://rdap.registro.br/domain/amorama.com.br
- RDAP .app (Google Registry): https://pubapi.registry.google/rdap/domain/amorama.app (bootstrap IANA: https://data.iana.org/rdap/dns.json)
- Site: https://amorama.app/ ; Instagram declarado: https://www.instagram.com/amorama.app/
- CNPJ 21.993.101/0001-80: https://brasilapi.com.br/api/cnpj/v1/21993101000180
- Lei 9.279/96 (LPI), art. 129: http://www.planalto.gov.br/ccivil_03/leis/l9279.htm
- Buscas web citadas na seção 5 (Justia, Markinton, TrademarkDir, Google Play, anogov.com, lovepanda.co)
