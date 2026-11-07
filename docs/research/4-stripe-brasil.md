# Pesquisa #4 — Stripe Brasil: Pix + cartão nacional + internacional

- **Ticket:** [#4](https://github.com/victor160997/amorama/issues/4)
- **Data da consulta:** 2026-11-07 (todas as taxas e regras abaixo foram lidas nas páginas oficiais nessa data)
- **Fontes:** somente primárias — `docs.stripe.com`, `stripe.com/br/pricing`, `support.stripe.com`. Cada afirmação traz o link da página que a sustenta.
- **Contexto:** CNPJ brasileiro vende um produto digital (Final Video) por R$ 80–200, pago antes da geração, com reembolso garantido se o Couple nunca der a Approval dos Character Sheets. O fluxo é sem login: o Couple acompanha o Order pelo Order Link (URL secreta por e-mail).

## Resposta curta

1. **Taxas (preço padrão, Brasil, 2026-11-07):** cartão nacional **3,99% + R$ 0,39**; cartão internacional **+2%** sobre o nacional (e, se houver conversão, o cliente paga a conversão via Adaptive Pricing, a partir de 2%); **Pix 1,19%** (hoje *somente por convite* para empresas sediadas no Brasil); boleto R$ 3,45; contestação R$ 55. Tarifas já incluem impostos indiretos; Stripe não emite NFS-e.
2. **Pix:** confirmação imediata, QR expira em 4 h por padrão (60 s a 14 dias), webhook `payment_intent.succeeded` / `checkout.session.async_payment_succeeded`. Reembolso total ou parcial em até **90 dias**, cai em minutos, **não pode ser cancelado** e **é rejeitado se o saldo disponível da conta Stripe não cobrir o valor** (ao contrário do cartão, que fica pendente).
3. **Cartão nacional:** Visa, Mastercard (+ Amex, Elo e outras bandeiras locais segundo a página de suporte). **Parcelamento não existe na documentação da Stripe para o Brasil** (só México, Japão e Mastercard Installments). Repasse do cartão nacional só **30 dias corridos** depois da transação — o pior prazo de todos.
4. **Cartão internacional:** aceito em BRL com +2%. Contas Stripe Brasil têm **restrição de câmbio/cross-border**: pagamentos que envolvam conversão de moeda são recusados; Visa/Mastercard emitidos fora do Brasil cobrados em BRL passam. Repasse em 5 dias. **Stripe Tax não está disponível para empresa sediada no Brasil.**
5. **Checkout vs Payment Element:** para o fluxo sem login com Order Link, usar **Checkout Session (página hospedada)** em `mode=payment`, `customer_creation=if_required`, `client_reference_id=<order_id>`, `success_url` com `{CHECKOUT_SESSION_ID}` apontando de volta ao Order Link, e cumprir via webhook. Payment Element só se a página de pagamento precisar ser visualmente "dentro" do site; nesse caso ainda assim com a Checkout Sessions API (`ui_mode=elements`), não com Payment Intents.
6. **Caveats do fluxo "pagamento antecipado + reembolso garantido":** reembolso não devolve a tarifa da Stripe (R$ 6,38 perdidos num Order de R$ 150 no cartão); reembolso de Pix precisa de saldo disponível; cartão só vira saldo disponível em 30 dias, Pix em 2; janela de contestação do cartão é ~120 dias e a Stripe a conta a partir da **data do serviço**, não do pagamento; Pix tem contestação via MED sem direito a defesa.

---

## 1. Tabela de taxas oficial (Brasil, preço padrão)

Fonte principal: [stripe.com/br/pricing](https://stripe.com/br/pricing) e [stripe.com/br/pricing/local-payment-methods](https://stripe.com/br/pricing/local-payment-methods), lidas em 2026-11-07.

| Item | Tarifa | Observação / fonte |
| --- | --- | --- |
| Cartão nacional (emitido no BR) | **3,99% + R$ 0,39** por transação | "por transação realizada para cartões nacionais" — [pricing](https://stripe.com/br/pricing) |
| Cartão internacional | **+ 2%** sobre o valor da transação | aplicado "após conversão para a moeda local" — [pricing](https://stripe.com/br/pricing) |
| Conversão de moeda | Adaptive Pricing: **cliente** paga a partir de 2% (docs: 2–4%); empresa paga 0% | [pricing](https://stripe.com/br/pricing), [Adaptive Pricing](https://docs.stripe.com/payments/currencies/localize-prices/adaptive-pricing) |
| Pix | **1,19%** por Pix pago, sem parte fixa | "Para empresas sediadas no Brasil, no momento, o Pix é apenas para convidados." — [local-payment-methods](https://stripe.com/br/pricing/local-payment-methods) |
| Boleto | **R$ 3,45** por boleto pago | [local-payment-methods](https://stripe.com/br/pricing/local-payment-methods) |
| Contestação recebida | **R$ 55,00** | não devolvida mesmo se ganhar — [pricing](https://stripe.com/br/pricing), [how-disputes-work](https://docs.stripe.com/disputes/how-disputes-work) |
| Refutação manual de contestação | R$ 55,00 | devolvida se ganhar — [pricing](https://stripe.com/br/pricing) |
| Smart Disputes | 30% do valor contestado, só se ganhar | [pricing](https://stripe.com/br/pricing) |
| 3D Secure | incluído no preço padrão; standalone R$ 0,60/tentativa | [pricing](https://stripe.com/br/pricing) |
| Reembolso | sem tarifa para emitir; **tarifa original não é devolvida** | [pricing](https://stripe.com/br/pricing), [refunds](https://docs.stripe.com/refunds) |
| Repasse (payout) normal | sem tarifa | [payouts](https://docs.stripe.com/payouts) |
| Impostos sobre as tarifas | "Stripe fees are inclusive of all such indirect taxes" | sem NFS-e desde maio/2022; relatório em Financial Reports — [support](https://support.stripe.com/questions/taxes-on-stripe-fees-for-brazil-based-businesses) |

**Custo por Order no preço padrão (ilustrativo):**

| Valor do Order | Pix (1,19%) | Cartão nacional (3,99% + 0,39) | Cartão internacional em BRL (5,99% + 0,39) |
| --- | --- | --- | --- |
| R$ 80 | R$ 0,95 | R$ 3,58 | R$ 5,18 |
| R$ 150 | R$ 1,79 | R$ 6,38 | R$ 9,38 |
| R$ 200 | R$ 2,38 | R$ 8,37 | R$ 12,37 |

Esses valores são o que se perde num reembolso integral, porque a Stripe não devolve a tarifa de processamento ([refunds](https://docs.stripe.com/refunds): "As tarifas de processamento da Stripe referentes à transação original não são devolvidas").

Valor mínimo de cobrança em BRL: R$ 0,50 ([currencies](https://docs.stripe.com/currencies)). Irrelevante para R$ 80–200.

---

## 2. Pix

Fonte: [docs.stripe.com/payments/pix](https://docs.stripe.com/payments/pix) e [accept-a-payment](https://docs.stripe.com/payments/pix/accept-a-payment?payment-ui=checkout).

### Disponibilidade

- Empresas no Brasil aceitam Pix com liquidação em BRL. **Pix Automático (recorrente) não está disponível para empresas domiciliadas no Brasil** — irrelevante para Amorama (pagamento único).
- **Convite:** a página de preços diz que, para empresas sediadas no Brasil, "no momento, o Pix é apenas para convidados". A doc manda verificar elegibilidade em *Configurações › Formas de pagamento* do Dashboard. **Isso é um risco de onboarding: não assumir que Pix estará ligado no dia 1.**
- MCCs proibidos (farmácia, apostas, cripto, serviços médicos etc.) não afetam vídeo personalizado.
- Limites: mínimo R$ 0,50; máximo padrão por pagamento = equivalente a US$ 3.000 em BRL. Confortável para R$ 80–200.
- Moeda de apresentação: **só `brl`**. Em Checkout, "Os preços de todos os itens precisam usar a moeda `brl`".

### Fluxo e prazo de confirmação

- Cliente escolhe Pix → recebe QR code / "copia e cola" → aprova no app do banco → **"Payment confirmation timing: Immediate"**.
- A página de checkout fica aberta; o app do banco não redireciona de volta. Checkout/Elements redirecionam para a `return_url`/`success_url` quando o intent chega a estado final.
- No **Payment Element / API direta**, `stripe.confirmPixPayment` exibe o QR; com `handleActions: false` você recebe `next_action.pix_display_qr_code` com `data` (string EMV), `image_url_png`, `image_url_svg`, `expires_at` e `hosted_instructions_url`.
- Campos coletados no formulário: nome, e-mail e `tax_id` (CPF/CNPJ). A doc diz que o governo exige CPF/CNPJ "ao realizar transações internacionais"; em sandbox o Checkout pede `000.000.000-00`.
- **Descrição no extrato:** Pix ignora `statement_descriptor`; o cliente vê **Ebanx** (parceiro da Stripe) como recebedor. O nome da empresa aparece no campo `identifier`. Vale avisar o Couple na tela de pagamento.
- Recibos: por padrão o parceiro Ebanx envia recibo por e-mail; dá para desligar em *Configurações › E-mails*.

### Expiração

- `payment_method_options[pix][expires_after_seconds]`: **60 a 1.209.600 s (14 dias)**; **padrão 14.400 s (4 h)** após a confirmação do PaymentIntent. Alternativa `expires_at` (timestamp absoluto); não pode usar os dois.
- Cliente não consegue pagar depois do vencimento. Após expirar, confirmar o PaymentIntent com outra forma ou cancelar.
- A doc recomenda **confiar no evento `payment_intent.payment_failed`** para saber que expirou, não no timestamp.
- Em Checkout hospedado, a própria Checkout Session expira em **24 h** por padrão (`expires_at` entre 30 min e 24 h) — ver §8.

### Webhooks

- API direta / Payment Element: `payment_intent.succeeded` (chega "imediatamente após o Pix ser pago" em produção), `payment_intent.payment_failed` (expirou).
- Checkout: `checkout.session.completed` quando o cliente conclui a sessão; para formas com notificação postergada, `checkout.session.async_payment_succeeded` / `checkout.session.async_payment_failed`. O guia de [fulfillment](https://docs.stripe.com/checkout/fulfillment?ui=full-page) diz que **webhooks são obrigatórios** e que a função de fulfillment deve ser idempotente e checar `payment_status != 'unpaid'`.
- Sandbox: e-mails especiais (`succeed_immediately@…`, `expire_immediately@…`, `fill_never@…`) simulam cada cenário.

### Reembolso de Pix

- **Total e parcial suportados.** Janela: **90 dias** após o pagamento original. Processamento: "Usually within a few minutes", mas "não há um tempo máximo garantido".
- **Não é possível cancelar reembolsos de Pix.**
- Vai para a conta bancária usada no pagamento original.
- Um `Refund` com status inicial de sucesso "não comprova, por si só, que o valor foi creditado"; verificar o status antes de dizer ao Couple que o dinheiro voltou.
- **Saldo:** [refunds](https://docs.stripe.com/refunds) — "Se o saldo disponível não for suficiente para cobrir o valor do reembolso, a Stripe mantém o reembolso como pendente para transações com cartão (**reembolsos para outros tipos de forma de pagamento são rejeitados**)". Ou seja, reembolso de Pix falha se o saldo disponível estiver baixo. Mitigação: recarga (*top-up*) na conta Stripe ou manter volume.

### Contestações (MED)

- Pix aceita contestação só em casos limitados (fraude, invasão de conta) via Mecanismo Especial de Devolução. **Não é possível contestar nem enviar evidência**; a decisão do parceiro é final e a Stripe debita os fundos. Evento `charge.dispute.created`.

### Liquidação

- "Settlement timing: Up to 2 business days (T+2)" ([pix](https://docs.stripe.com/payments/pix)); a página de suporte de repasses diz **2 dias** para Pix ([support](https://support.stripe.com/questions/brazil-specific-payout-schedule-and-payment-availability)).

---

## 3. Cartão nacional

### Bandeiras

- [currencies](https://docs.stripe.com/currencies): "Em Brasil, você pode aceitar: Visa, Mastercard."
- [support — Accepted payment methods in Brazil](https://support.stripe.com/questions/accepted-payment-methods-in-brazil) lista além disso "Amex, Elo, Hipercard, AVS, Correios and other local schemes", débito local (BR), débito internacional (não-BR), Google/Apple Pay. (A tabela da página tem colunas desalinhadas; Visa/Mastercard crédito são os únicos inequívocos. Hipercard foi descontinuado pela bandeira em 2025; tratar a lista como "confirmar no Dashboard".)
- Débito: a página de suporte lista "Local debit cards (BR)" como aceitos.

### Parcelamento

- [docs.stripe.com/payments/installments](https://docs.stripe.com/payments/installments) lista **apenas** Mastercard Installments, México (*meses sin intereses*) e Japão. **Não há documentação de parcelamento para contas no Brasil.** Buscas em `support.stripe.com` também não retornam nada oficial.
- **Conclusão para o produto:** não contar com "3x sem juros" via Stripe. Para R$ 80–200 isso tem impacto baixo — o valor está abaixo do patamar típico de parcelamento — mas é uma desvantagem competitiva frente a adquirentes nacionais se o preço subir. Se parcelamento virar requisito, é motivo para reavaliar o provedor, não para gambiarra.

### Taxas e contestações

- 3,99% + R$ 0,39 (§1). 3DS incluído.
- Contestação: R$ 55 debitados na abertura, não devolvidos. Janela típica do portador: **120 dias**; resposta do vendedor em 7–21 dias; ciclo total 2–3 meses ([how-disputes-work](https://docs.stripe.com/disputes/how-disputes-work)). Ponto crítico para Amorama: "quando um cliente paga por um evento ou serviço futuro …, **a janela de contestação começa na data do evento, não na data de pagamento**". Um Order pago hoje e entregue em 10 dias tem janela de contestação contando da entrega.
- Reembolso emitido logo após a cobrança (até ~2 h) pode sair como *anulação* (reversal), que não aparece no extrato do cliente.

### Repasse

- **30 dias corridos** para cartão nacional (§6).

---

## 4. Cartão internacional e venda para fora do Brasil

### Hoje (cliente estrangeiro pagando um CNPJ brasileiro)

- Tarifa: nacional **+ 2%** = 5,99% + R$ 0,39 quando cobrado em BRL.
- [support — Transaction declined – Stripe Brazil accounts](https://support.stripe.com/questions/transaction-declined-stripe-brazil-accounts): "Cross-border payments and foreign exchange (FX) activity are restricted for Stripe Brazil merchant accounts." Pagamentos que envolvem "cross-border flows, international offsettings, or currency conversions" são recusados com a mensagem "The transaction could not be completed due to restrictions on cross border and foreign exchange payments…". **A restrição não se aplica a Visa e Mastercard emitidos fora do Brasil cobrados por uma conta Stripe Brasil** — ou seja, um cartão americano pagando em **BRL** funciona; o banco do cliente faz a conversão e pode cobrar spread dele.
- [currencies](https://docs.stripe.com/currencies), seção "Países com controle cambial": remessas de/para o Brasil só por canais autorizados. Na prática, **a conta Stripe Brasil liquida em BRL** e não deve ser tratada como conta multimoeda.
- Repasse de cartão internacional: **5 dias** (vs 30 do nacional) ([support](https://support.stripe.com/questions/brazil-specific-payout-schedule-and-payment-availability)).
- Pix não é opção para cliente fora do Brasil (cliente precisa estar no BR).

### Adaptive Pricing (apresentar em moeda local do cliente)

- Converte automaticamente o preço para a moeda do cliente em Checkout/Payment Links/Elements com Checkout Sessions; **não funciona com Elements + Payment Intents**. Empresa paga 0%; cliente paga 2–4% embutido no câmbio. Reembolso devolve na moeda do cliente pela **mesma taxa** da compra ([adaptive-pricing](https://docs.stripe.com/payments/currencies/localize-prices/adaptive-pricing)).
- A doc não lista países de conta elegíveis/excluídos; o Dashboard (*Settings › Adaptive Pricing*) é a fonte. Dada a restrição de FX acima, **há risco real de não estar disponível para contas BR** — item em névoa (§10).

### Stripe Tax

- [tax/supported-countries](https://docs.stripe.com/tax/supported-countries): **Brasil não aparece na tabela**, nem como "your business location" nem como "your customer location". Portanto um CNPJ brasileiro **não pode usar Stripe Tax** para calcular IVA/GST de clientes na UE, Reino Unido etc. Vender produto digital para fora exigiria resolver imposto de consumo por conta própria (ou via marketplace/merchant of record).

### O que muda de verdade ao vender para fora

1. Moeda de apresentação continua sendo BRL salvo se Adaptive Pricing estiver habilitado para a conta — confirmar no Dashboard.
2. Sem Stripe Tax; obrigações de IVA/GST ficam manuais.
3. Pix sai do cardápio; só cartão (+2%).
4. Disputas em moeda convertida podem vir com valor diferente do original (câmbio no dia da disputa) ([how-disputes-work](https://docs.stripe.com/disputes/how-disputes-work)).
5. Alternativa estrutural, se o mercado externo crescer: entidade fora do Brasil com conta Stripe própria — fora do escopo deste ticket.

---

## 5. Reembolsos (regras gerais + Pix)

Fonte: [docs.stripe.com/refunds](https://docs.stripe.com/refunds).

| Regra | Cartão | Pix |
| --- | --- | --- |
| Total / parcial | ✓ / ✓ (vários parciais até o total) | ✓ / ✓ |
| Tarifa original devolvida | **Não** | **Não** |
| Tarifa para reembolsar | Não (preço padrão) | Não |
| Prazo para o cliente ver | 5–10 dias úteis (ou anulação imediata se logo após a cobrança) | minutos, sem máximo garantido |
| Janela para emitir | Doc não fixa limite para cartão | **90 dias** |
| Saldo disponível insuficiente | fica **pendente** até haver saldo | **rejeitado** |
| Cancelar reembolso | só alguns, pelo Dashboard, por pouco tempo | **não** |
| Falha de reembolso | `refund.failed`, fundos voltam em até 30 dias; precisa de alternativa manual | idem |
| Destino | sempre a forma de pagamento original | conta bancária original |

Outros pontos:

- Reembolso usa **saldo disponível, não pendente**. Como o cartão nacional só fica disponível após 30 dias (§6), uma empresa nova que reembolsa Pix no primeiro mês pode não ter saldo — a doc permite **recarga** (*top-up*) para cobrir.
- Eventos a escutar: `refund.created` (mínimo recomendado), `refund.updated`, `refund.failed`, `charge.refunded`.
- Enquanto uma contestação está aberta, **não dá para reembolsar fora do processo de contestação**.
- Para fluxos com muito reembolso logo após a cobrança, a doc sugere **autorização e captura manuais** (cancelar antes de capturar não custa tarifa). **Não serve para Pix** (sem captura manual) e, para cartão, a autorização vale só alguns dias — não cobre o ciclo de Approval de Amorama se ele passar disso. Fica registrado como opção para cartão se a Approval acontecer em até ~7 dias; ver §9.

---

## 6. Repasses (payouts) no Brasil

Fontes: [docs.stripe.com/payouts](https://docs.stripe.com/payouts), [support — Brazil-specific payout schedule](https://support.stripe.com/questions/brazil-specific-payout-schedule-and-payment-availability), [support — Supported bank accounts in Brazil](https://support.stripe.com/questions/supported-bank-accounts-in-brazil).

- **Sempre automáticos e diários** ("Brasil e Índia: os repasses são sempre automáticos e diários"). Semanais/mensais não existem; **repasse manual não está disponível no Brasil**.
- Disponibilidade dos fundos, em **dias corridos** após o processamento:
  - **30 dias** — cartão nacional (emitido no BR)
  - **5 dias** — cartão internacional
  - **2 dias** — Pix, boleto e pré-pago nacional
- Fim de semana: cai no próximo dia útil. Mínimo de repasse R$ 0,01.
- Primeiro repasse pode demorar mais ("até 30 dias em países como o Brasil").
- Instant Payouts: a doc não menciona Brasil; tratar como indisponível.
- Conta bancária: **conta corrente em BRL, no mesmo CNPJ da conta Stripe** ("including ME and MEI accounts"); divergência faz o repasse falhar. Banco precisa ser instituição domiciliada (lista Nuclea) e constar nas listas Visa/Mastercard Brasil. Bancos digitais (Nubank, Inter, C6…) têm formatos de agência documentados.
- Recebíveis de cartão são reportados aos sistemas de registro (lei brasileira) e podem ser negociados/onerados; o Dashboard mostra o detalhe ([support — card receivables](https://support.stripe.com/questions/payouts-in-brazil-card-receivables)).

**Implicação de caixa para Amorama:** um Order de R$ 150 no cartão nacional vira dinheiro em conta em ~30 dias; via Pix em ~2 dias. Como a geração precisa pagar APIs antes disso, o Pix não é só mais barato — é o que financia a operação. Vale incentivar Pix na tela de pagamento.

---

## 7. Onboarding do CNPJ

Fontes: [support — Brazil-specific information to open a Stripe account](https://support.stripe.com/questions/brazil-specific-information-to-open-a-stripe-account), [support — 2026 updates to Brazil verification requirements](https://support.stripe.com/questions/2026-updates-to-brazil-verification-requirements).

Necessário para pessoa jurídica:

- **CNPJ ativo na Receita Federal** (a Stripe verifica; CNPJ suspenso/baixado/pendente gera restrições). Cada conta fica presa a um único CNPJ; **CNPJ e tipo de empresa não podem ser alterados após verificação**.
- Razão social igual à do CNPJ; endereço comercial **no Brasil**, verificado com documento da entidade.
- Site (ou link de app store/rede social) e telefone de suporte.
- **Representante legal** com CPF, residente no Brasil, que seja administrador ou procurador; precisa de ID + selfie segurando o documento ("proof of life") e documento de autorização (contrato social / procuração). Idade mínima 18.
- **UBOs**: todo sócio com ≥ 25% ou controle significativo — nome, CPF, nascimento, endereço, percentual.
- **Capacidade financeira** (faixa de faturamento mensal): nova empresa / < R$ 5 mil / 5–30 mil / 30–400 mil / > 400 mil.
- Conta corrente BRL no mesmo CNPJ (§6).
- Prazos: após a Stripe pedir informação, "typically, you have 28 days from the due date to provide updated information before payouts are paused"; pagamentos pausam 90 dias após o vencimento.
- Desde 1º/jul/2026 a Receita emite CNPJ alfanumérico; informar exatamente como emitido ([support](https://support.stripe.com/questions/brazil-cnpj-new-alphanumeric-format-support)).
- Impostos: tarifas já incluem tributos indiretos; não há NFS-e das tarifas, só relatório no Dashboard ([support](https://support.stripe.com/questions/taxes-on-stripe-fees-for-brazil-based-businesses)).
- **Pix depende de convite** (§2) — pedir habilitação logo após a ativação da conta.

---

## 8. Stripe Checkout vs Payment Element para o fluxo sem login

Fontes: [online-payments](https://docs.stripe.com/payments/online-payments) (comparação oficial), [how-checkout-works](https://docs.stripe.com/payments/checkout/how-checkout-works?payment-ui=stripe-hosted), [guest-customers](https://docs.stripe.com/payments/checkout/guest-customers), [fulfillment](https://docs.stripe.com/checkout/fulfillment?ui=full-page), [payment-element](https://docs.stripe.com/payments/payment-element), [API Checkout Sessions](https://docs.stripe.com/api/checkout/sessions/create).

### O que a Stripe recomenda

- "Recomendamos a API Checkout Sessions para a maioria das integrações." Payment Intents só para quem quer "controle total … e recriar essas funcionalidades por conta própria" — exige "muito mais código e manutenção contínua".
- O **Payment Element** hoje também é oferecido em cima da Checkout Sessions API (`ui_mode=elements`); a doc do Payment Element diz explicitamente para não usar Payment Intents "a menos que o usuário solicite explicitamente".
- Pix e cartão são suportados em todas as UIs relevantes: página hospedada, formulário incorporado, Payment Element ([pix — produtos](https://docs.stripe.com/payments/pix)).

### Recomendação para Amorama

**Checkout Session hospedada (ou `embedded_page`), `mode=payment`.** Motivos ligados ao fluxo sem login:

| Necessidade do Order Link | Como o Checkout resolve |
| --- | --- |
| Sem conta/login | `customer_creation=if_required` → nenhum `Customer` criado; dados ficam em `customer_details` e o Dashboard agrupa como *guest customer*. |
| Amarrar pagamento ao Order | `client_reference_id=<order_id>` (≤ 200 chars) + `metadata` + `payment_intent_data.metadata`. |
| Voltar ao Order Link após pagar | `success_url=https://…/pedido/<token>?session_id={CHECKOUT_SESSION_ID}`; `cancel_url` de volta ao Order Link. |
| Saber que pagou mesmo se o Couple fechar a aba | webhook `checkout.session.completed` + `checkout.session.async_payment_succeeded`/`failed`; fulfillment idempotente checando `payment_status`. |
| Pix com QR, expiração e e-mail de lembrete | Pix nativo no Checkout; `payment_method_options[pix][expires_after_seconds]`; e-mail de lembrete com QR habilitável no Dashboard. |
| PT-BR | `locale=pt-BR`. |
| Sessão não ficar aberta para sempre | `expires_at` entre 30 min e 24 h (padrão 24 h); evento `checkout.session.expired` para marcar o Order como "aguardando pagamento" de novo. |
| Reembolso garantido | reembolso pelo `payment_intent` da sessão (API `refunds`), total ou parcial. |
| PCI, 3DS, CAPTCHA, erros traduzidos, Link, Apple/Google Pay | nativos. |

**Detalhe importante com Pix no Checkout:** `expires_after_seconds` do Pix é contado a partir da confirmação do PaymentIntent, e a Checkout Session em si expira em até 24 h. Para não deixar um QR "vivo" por 4 h depois de o Couple abandonar, alinhar o `expires_after_seconds` (p.ex. 30–60 min) e tratar `payment_intent.payment_failed` como "Pix expirou — gerar outro".

**Quando usar Payment Element em vez disso:** só se o produto exigir que o formulário de pagamento fique dentro da página do Order Link com layout próprio. Mesmo assim, usar `ui_mode=elements` da Checkout Sessions API, que mantém Adaptive Pricing, webhooks do ciclo completo e expiração automática; Payment Intents puros perdem tudo isso e precisam de `return_url` + verificação manual do status na volta.

---

## 9. Caveats do fluxo "pagamento antecipado + reembolso garantido"

1. **Custo irrecuperável do reembolso.** Tarifa não volta: R$ 0,95–2,38 (Pix) ou R$ 3,58–8,37 (cartão nacional) por Order reembolsado. Modelar como custo de aquisição falhado.
2. **Reembolso de Pix exige saldo disponível, senão é rejeitado.** Nos primeiros 30 dias (cartão ainda pendente) o saldo disponível vem quase só de Pix (D+2). Manter reserva via *top-up* ou aceitar que um reembolso pode precisar de reemissão.
3. **Prazo de 90 dias para reembolsar Pix.** O fluxo de Approval + regenerações precisa fechar bem antes disso. Definir prazo máximo de Approval (p.ex. 30 dias) e reembolsar automaticamente ao expirar.
4. **Reembolso de Pix é irreversível** e o `Refund` "succeeded" não prova crédito na conta do Couple. Mensagem ao Couple: "reembolso enviado", não "recebido".
5. **Contestação de cartão conta a partir da entrega do serviço**, com ciclo de 2–3 meses e R$ 55 não devolvidos. Guardar evidência: Story, fotos enviadas, registro de Approval (timestamp, IP, token do Order Link), downloads do Final Video.
6. **Contestação de Pix (MED) não tem defesa.** Casos raros (fraude/invasão), mas a Stripe debita e pronto.
7. **Alternativa para cartão: autorizar sem capturar.** Reduz custo de "reembolso" a zero quando o Couple não aprova, mas (a) não existe para Pix e (b) a autorização de cartão dura dias, não semanas — só funciona se a Approval for rápida. Não adotar sem prototipar; registrado como opção.
8. **Caixa.** Cartão nacional D+30 vs Pix D+2 — ver §6. Pix deve ser o padrão sugerido na tela.
9. **Pix por convite.** Se a conta não for habilitada, o MVP fica só com cartão (3,99% + R$ 0,39, D+30). Pedir habilitação durante o onboarding e ter esse cenário no plano.
10. **Extrato do Pix mostra Ebanx**, não Amorama. Avisar na tela para reduzir "não reconheço essa cobrança".
11. **Sem parcelamento.** Aceitável na faixa R$ 80–200; limitação se o preço subir.
12. **Internacional:** funciona só em BRL com +2%; sem Stripe Tax; Adaptive Pricing a confirmar. Não prometer "venda para fora" sem validar no Dashboard.

---

## 10. Névoa (não confirmado em fonte primária)

- Se **Adaptive Pricing** está habilitável para contas sediadas no Brasil (a doc lista BR só como mercado de *cliente*; a restrição de FX das contas BR sugere que não). Verificar em *Dashboard › Settings › Adaptive Pricing*.
- Lista exata de **bandeiras nacionais** (Elo/Amex) realmente habilitadas na conta — a página de suporte é ambígua; conferir em *Payment methods* após ativação.
- Prazo para **habilitação do Pix** por convite e critérios.
- Se **Instant Payouts** existem para BR (doc silencia; presumir não).
- Limite de tempo para **reembolso de cartão** — a doc da Stripe não fixa; bandeiras têm regras próprias.
- Duração exata da **autorização sem captura** para cartões no Brasil (doc genérica fala em dias; não confirmado para BR).

---

## Fontes consultadas (2026-11-07)

Preços
- https://stripe.com/br/pricing
- https://stripe.com/br/pricing/local-payment-methods

Pix
- https://docs.stripe.com/payments/pix
- https://docs.stripe.com/payments/pix/accept-a-payment?payment-ui=checkout
- https://docs.stripe.com/payments/pix/accept-a-payment?payment-ui=direct-api

Cartões, parcelamento, moedas
- https://docs.stripe.com/payments/installments
- https://docs.stripe.com/currencies
- https://docs.stripe.com/payments/currencies/settlement-payouts
- https://docs.stripe.com/payments/currencies/localize-prices/adaptive-pricing?payment-ui=stripe-hosted
- https://support.stripe.com/questions/adaptive-pricing
- https://support.stripe.com/questions/accepted-payment-methods-in-brazil
- https://support.stripe.com/questions/transaction-declined-stripe-brazil-accounts
- https://support.stripe.com/questions/in-which-currencies-can-i-charge-my-customers

Reembolsos e contestações
- https://docs.stripe.com/refunds
- https://docs.stripe.com/disputes/how-disputes-work

Repasses
- https://docs.stripe.com/payouts
- https://support.stripe.com/questions/brazil-specific-payout-schedule-and-payment-availability
- https://support.stripe.com/questions/supported-bank-accounts-in-brazil
- https://support.stripe.com/questions/payouts-in-brazil-card-receivables

Onboarding e impostos
- https://support.stripe.com/questions/brazil-specific-information-to-open-a-stripe-account
- https://support.stripe.com/questions/2026-updates-to-brazil-verification-requirements
- https://support.stripe.com/questions/brazil-cnpj-new-alphanumeric-format-support
- https://support.stripe.com/questions/taxes-on-stripe-fees-for-brazil-based-businesses

Stripe Tax
- https://docs.stripe.com/tax/supported-countries

Checkout vs Elements
- https://docs.stripe.com/payments/online-payments
- https://docs.stripe.com/payments/checkout/how-checkout-works?payment-ui=stripe-hosted
- https://docs.stripe.com/payments/checkout/guest-customers
- https://docs.stripe.com/checkout/fulfillment?ui=full-page
- https://docs.stripe.com/payments/payment-element
- https://docs.stripe.com/api/checkout/sessions/create

Boleto (só para a tabela de taxas)
- https://docs.stripe.com/payments/boleto
