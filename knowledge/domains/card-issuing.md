---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Card issuing", "issuer processing", "card programme management", "card-issuing"]
---
# Card issuing

Issuing is the other side of the four-party model from acquiring: the issuer authorises transactions against a cardholder's account and carries obligations, most notably first-party dispute handling, that an acquirer never sees. The single most consequential fact for a PM here is that most fintechs issuing cards do not hold the banking licence themselves. They operate under a sponsor bank's bank identification number, and the sponsor bank carries the ultimate regulatory responsibility even though the fintech built the product and owns the roadmap. That means the network's rules and the sponsor's risk appetite outrank your own backlog every time they conflict, and disputes and tokenisation are where the real operating cost of the business actually hides, not in the plastic or the app. Card networks govern authorisation, tokenisation for wallets, and the issuer-side dispute process on fixed timelines the product cannot renegotiate. Credit, debit, and prepaid are legally distinct products with different regulatory regimes, error-resolution duties, and disclosure requirements, even when the app screen looks identical to the cardholder holding any of the three.

## Questions a PM must ask

1. Are we the issuer of record, or a programme manager operating under a sponsor bank's licence, and which decisions in this feature actually require the sponsor's sign-off before shipping?
2. Is this card credit, debit, or prepaid, and does the dispute-resolution and disclosure regime built into the product actually match which one it legally is?
3. When a cardholder disputes a transaction, what is the regulatory timeline for provisional credit and final resolution, and does the workflow hit it, not just the marketing claim of an instant dispute?
4. What happens when a network token in a phone wallet and the physical card's number diverge, for example after a reissue, and does the product re-provision the token or leave the wallet silently broken?
5. What is the fraud and credit-loss liability split between us, the sponsor bank, and the network, and does our own risk appetite actually match what we are on the hook for?
6. Does the cardholder-facing app make clear which entity is actually their bank of record for deposit-insurance and dispute purposes, since confusion here is a support-cost and compliance problem at once?
7. For a credit product, what does the underwriting decision rely on, and can it be explained to the sponsor bank's model risk function in terms they will accept? See [lending-credit](lending-credit.md) for the underwriting question in full, and [modules/regulated/README.md](../../modules/regulated/README.md) when a model drives it.
8. What is the programme's spend limit, velocity control, and exposure cap, and who at the sponsor bank monitors it in real time rather than after the fact?

## Gatekeepers

- **The sponsor or issuing bank.** Holds the bank identification number and the banking licence, approves the programme agreement, sets risk limits, and can suspend the entire card programme, not just one feature, if its controls are judged inadequate.
- **The card networks**, Visa, Mastercard, and regional schemes. License the number range, set authorisation and tokenisation rules, and run the issuer-side dispute process on fixed timelines.
- **The banking regulator supervising the sponsor.** The sponsor's own primary federal or national supervisor in the US, or the equivalent central bank licensing regime for banks and e-money issuers elsewhere.
- **Consumer protection regulators on dispute and disclosure.** The US CFPB oversees Regulation E for debit and prepaid disputes and Regulation Z for credit; most jurisdictions carry an equivalent error-resolution and disclosure regime a card product cannot contract around.
- **Programme risk and underwriting**, internal or the sponsor bank's own. Sets credit limits, velocity rules, and exposure caps; a growth feature that raises limits without this sign-off is exactly the failure sponsor banks exist to prevent.
- **Wallet providers, Apple, Google, and Samsung, via their own provisioning rules.** Not a regulator, but a gatekeeper in practice, able to suspend a number range's wallet provisioning on a fraud pattern the issuer does not control.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Authorisation approval rate | Issuer risk posture and cardholder experience | Rises by loosening velocity or fraud rules, moving loss from a visible decline to invisible fraud that surfaces later |
| Dispute resolution time versus the regulatory deadline | Compliance and trust | An average sits comfortably inside the deadline while a long tail of complex disputes blows through it, and the tail is what an examiner reads |
| First-party fraud rate, a cardholder disputing a transaction they authorised | A real and growing loss category | Often bundled into "fraud" with genuine third-party fraud, hiding that the fix, better authorisation evidence, is different from a better fraud model |
| Programme exposure versus the sponsor bank's limit | Risk headroom | A point-in-time reading can look fine the day before a velocity spike breaches it intraday |
| Card activation rate | Programme launch health | A card activated by one verification swipe and never used again scores identically to genuine engagement |
| Issuer-side chargeback win rate | Dispute quality | A "win" can mean the network's default timeline simply expired in the cardholder's favor, not that evidence was reviewed |
| Token provisioning success rate | Wallet reach | Says nothing about whether the token still authorises correctly after a card reissue, which is where wallets silently break |
| Net credit losses as a share of receivables | Portfolio health | Lags underwriting decisions by months, so a loose underwriting period reports as healthy until the loss curve catches up |
| Time to card issuance | Onboarding friction | Improves by deferring identity checks that then surface as post-issuance freezes, a worse failure than a slower approval would have been |
| Sponsor bank audit findings open past due date | Partnership health | A small open count can still include the one finding severe enough to trigger a programme suspension; severity, not count, is what matters |

## Reading

- **Regulation E and Regulation Z (US).** The model error-resolution and dispute-timeline regimes for debit and prepaid, and for credit respectively; read them even outside the US as a benchmark for what a fair dispute process guarantees.
- **Visa and Mastercard issuer-side operating rules** on authorisation, tokenisation, and disputes. Read the issuer chapters specifically; acquirer-facing summaries miss the timelines that bind a programme manager.
- **US enforcement actions against sponsor banks over bank-fintech partnership oversight.** Read the recurring pattern, inadequate ongoing monitoring of the fintech partner, rather than any single case, and verify specific names and dates before relying.
- **EMVCo's tokenisation specifications**, underlying Visa Token Service and Mastercard's equivalent, the technical standard behind wallet provisioning.
- **State Bank of Pakistan's regulations for electronic money institutions.** A non-US model for who may issue stored-value instruments and how customer funds must be safeguarded (verify current specifics before relying).
- **The EU's e-money directive framework.** The European model for e-money issuer licensing and safeguarding, useful as a contrast to a sponsor-bank model built on a single bank's own licence.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays, since a card programme is financial regulation by definition and a model-driven decision inside it stacks the AI overlay on top), DESIGN-2 (integrations, since the sponsor bank, network, and wallet providers can each unilaterally stop the programme), DELIVER-6 (regulated overlay drift, since sponsor terms and network rules can change between sign-off and launch), and OPERATE-4 (cost to run, where dispute volume and programme exposure are the operational load unique to issuing).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (sponsor bank, network, and wallets each named with owner and failure behavior), [eval-spec](../../templates/ai/eval-spec.md) (subgroup performance and drift are the acceptance criteria when a model drives underwriting or fraud scoring), [release-readiness](../../templates/delivery/release-readiness.md) (a programme launch or limit change carries the sponsor bank's sign-off as its own line), and [risk-register](../../templates/execution/risk-register.md) (programme exposure and sponsor-relationship risk as standing entries, not one-off risks).
