---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: ["skills/reg-gap-check/SKILL.md", "templates/operate/compliance-impact-assessment.md"]
method: ""
aliases: ["Fintech"]
---
# Fintech

This is a pointer card, and that is deliberate. Fintech is the one domain whose full pack already exists in this repository as [the regulated module](../../modules/regulated/README.md), the material that seeded the whole OS. Duplicating its content here would create a second copy that drifts from the verified one, which is exactly the failure the module's byte-exact policy exists to prevent. So this card orients and routes; it teaches nothing the module already owns.

## Where to go

The sub-sector packs that this pointer used to lack now exist beside it. Read the one whose licence and rail are yours: [core banking](core-banking.md), [transaction banking](transaction-banking.md), [remittances](remittances.md), [payments acquiring](payments-acquiring.md), [card issuing](card-issuing.md), [lending and credit](lending-credit.md), [embedded finance and BaaS](embedded-finance-baas.md), [wealth and investing](wealth-investing.md), [capital markets](capital-markets.md), [insurance](insurance.md), [crypto and digital assets](crypto-digital-assets.md), [RegTech, AML and KYC](regtech-aml-kyc.md), [mobile money and wallets](mobile-money-wallets.md), and [Islamic finance](islamic-finance.md). This card still owns one thing: when the product contains a model that decides, the regulated module applies on top of whichever sector card you read.

- **[modules/regulated/README.md](../../modules/regulated/README.md)** names the canonical source and how the overlay binds at Gate 2 and Gate 5. That README retains the broader "operates under a regulator" wording (any product where a supervisor can ask for the document trail: licensed payment flows, credit decisions, KYC or screening steps, stored value); the narrowed rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md) governs, and the overlay fires only when the product also contains an AI or machine-learning feature.
- **[skills/reg-gap-check/SKILL.md](../../skills/reg-gap-check/SKILL.md)** runs the challenge in advance: eleven regulatory domains checked against a spec, findings ranked by severity, owners and closing evidence named. Run it before any money-touching PRD reaches engineering.
- **[templates/operate/compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md)** captures the data-protection side and carries the legal sign-off.
- The regulated PRD template and its worked example live inside the module as byte-exact copies; use them as the module's own README directs, never edited in place.

## What the module covers, and does not

The module's verified citations map to two instruments only: the CBUAE guidance note on consumer protection and AI/ML adoption by licensed financial institutions (issued February 11, 2026) and the EU AI Act's Annex IV technical documentation fields, each read against primary text on a dated pass. Every other regime, PSD2 and its successors, US money-transmitter licensing, card scheme rulebooks, MAS or FCA guidance, is deliberately out of scope until its primary text has been read and cited. The reg-gap-check skill still names those domains and tells you what evidence would close each gap; it just refuses to invent the regulator's words. If you work fintech, that refusal is the single most protective habit this repository can give you.

## The one orientation the card adds

Fintech's questions are the same questions every domain card asks, with the stakes moved: the gatekeepers hold licenses over your business rather than listings, the metrics carry audit consequences rather than dashboard consequences, and an unverified claim in a document is not a quality problem but a supervisory finding waiting for its date. When another domain card on this shelf shares your product (an AI feature in a wallet, a checkout in a marketplace), read both cards, and let the regulated module win every conflict.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays: the AI overlay fires whenever a model is in the product; the regulated overlay fires only when both halves are yes, and a regulator-only yes routes to reg-gap-check instead), DESIGN-3 (where PII lives becomes a residency and regulator question), and DELIVER-6 (regulated overlay drift is checked before launch, not after).

**Templates this bends:** none directly; where a model is in the product, it activates [modules/regulated](../../modules/regulated/README.md) at Gates 2 and 5 via [os/STAGE-GATES.md](../../os/STAGE-GATES.md), and the module takes it from there.

**Filled in this repo:** no filled example fills a template from inside modules/regulated (byte-exact, and this card deliberately does not duplicate it) and no PRD example in this repository carries a run reg-gap-check output. The nearest filled artifact is [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md), which fills the one template this card names outside the module, [templates/operate/compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md); read its section 2 (applicable regulations, obligations triggered, evidence holder, owner) for table shape, since its actual regime is PCI DSS and UK GDPR on a payments checkout, not a financial-services licence or either instrument the regulated module currently cites. None of the fourteen financial-services sub-sector cards this pointer routes to has a filled example of its own yet either.

**Worked example (ILLUSTRATIVE):** one row of section 2 of a compliance-impact-assessment, written the way a wallet or lending PRD would need it, citing the one instrument this repository's regulated module currently verifies against:

| Regulation or regime | Applies because | Obligations triggered | Evidence and holder | Owner |
|---|---|---|---|---|
| CBUAE guidance note on consumer protection and AI/ML adoption by licensed financial institutions (issued February 11, 2026) | The product's credit-decisioning feature is a model that decides about a person, at a UAE-licensed financial institution (ILLUSTRATIVE product; the regulation and its issue date are real, quoted as this repository's own module names them) | Technical documentation trail, an explainability record a customer can be given on request, and a named accountable executive per the guidance note | The regulated module's PRD overlay, run through [skills/reg-gap-check/SKILL.md](../../skills/reg-gap-check/SKILL.md); evidence held by the accountable executive named there | [OPEN: named per product, per modules/regulated/README.md] |

The row stops at what the module has actually verified against primary text; a real product would run reg-gap-check itself rather than have this card assert a finding, which is the refusal the card calls its single most protective habit.
