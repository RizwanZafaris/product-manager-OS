# Fintech

This is a pointer card, and that is deliberate. Fintech is the one domain whose full pack already exists in this repository as [the regulated module](../../modules/regulated/README.md), the material that seeded the whole OS. Duplicating its content here would create a second copy that drifts from the verified one, which is exactly the failure the module's byte-exact policy exists to prevent. So this card orients and routes; it teaches nothing the module already owns.

## Where to go

- **[modules/regulated/README.md](../../modules/regulated/README.md)** explains when the overlay activates (any product where a supervisor can ask for the document trail: licensed payment flows, credit decisions, KYC or screening steps, stored value) and how it binds at Gate 2 and Gate 5.
- **[skills/reg-gap-check/SKILL.md](../../skills/reg-gap-check/SKILL.md)** runs the challenge in advance: eleven regulatory domains checked against a spec, findings ranked by severity, owners and closing evidence named. Run it before any money-touching PRD reaches engineering.
- **[templates/operate/compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md)** captures the data-protection side and carries the legal sign-off.
- The regulated PRD template and its worked example live inside the module as byte-exact copies; use them as the module's own README directs, never edited in place.

## What the module covers, and does not

The module's verified citations map to two instruments only: the CBUAE guidance note on consumer protection and AI/ML adoption by licensed financial institutions (issued February 11, 2026) and the EU AI Act's Annex IV technical documentation fields, each read against primary text on a dated pass. Every other regime, PSD2 and its successors, US money-transmitter licensing, card scheme rulebooks, MAS or FCA guidance, is deliberately out of scope until its primary text has been read and cited. The reg-gap-check skill still names those domains and tells you what evidence would close each gap; it just refuses to invent the regulator's words. If you work fintech, that refusal is the single most protective habit this repository can give you.

## The one orientation the card adds

Fintech's questions are the same questions every domain card asks, with the stakes moved: the gatekeepers hold licenses over your business rather than listings, the metrics carry audit consequences rather than dashboard consequences, and an unverified claim in a document is not a quality problem but a supervisory finding waiting for its date. When another domain card on this shelf shares your product (an AI feature in a wallet, a checkout in a marketplace), read both cards, and let the regulated module win every conflict.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays: the regulated overlay fires, and usually the AI overlay with it), DESIGN-3 (where PII lives becomes a residency and regulator question), and DELIVER-6 (regulated overlay drift is checked before launch, not after).

**Templates this bends:** none directly; it activates [modules/regulated](../../modules/regulated/README.md) at Gates 2 and 5 via [os/STAGE-GATES.md](../../os/STAGE-GATES.md), and the module takes it from there.
