# Pricing and Packaging: [product name]

**Stage:** PLANNING track (feeds every stage of the [operating loop](../../os/OPERATING-LOOP.md), most directly Gate 5 readiness)
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [pricing-packaging](../../skills/pricing-packaging/SKILL.md)

<!-- Pricing is a product decision that ships like a feature and reverses like a
     migration, so it gets a document, an owner, and a review date like everything
     else in this tree. The anchor concept is the value metric: the unit you charge
     by should scale with the value the customer receives, which is why it should
     rhyme with the [north star sheet](north-star-metric.md). Charging by seat when
     value scales by volume taxes adoption; charging by volume when value is flat
     invites bill shock.

     This file records the decision and its reasoning. It does not do the research;
     willingness-to-pay evidence comes from discovery and lands in the evidence
     column, or the row admits it is a guess. -->

**Owner:** [name, the one person who can approve a price change] · **Last updated:** [YYYY-MM-DD]
**Positioning doc:** [this product's positioning](positioning.md), which sets the category's pricing assumptions

## 1. Value metric

| Field | Answer |
|---|---|
| Unit we charge by | [seats, orders, volume, flat, etc.] |
| How it tracks delivered value | [one sentence; if it does not track value, say what it tracks instead and why] |
| North star tie | [the tree metric this unit rhymes with, or "mismatch, accepted because [reason]"] |
| Evidence customers accept this unit | [interviews, competitor norms, pilot invoices, linked; or "assumption"] |

## 2. Pricing model

<!-- The shape before the numbers: subscription, usage, tiered, flat, freemium, or a
     hybrid. Name the model, the reason, and the failure mode you are accepting,
     because every model has one. -->

- **Model:** [shape]
- **Why this model for this buyer:** [how the section 4 buyer prefers to buy, evidence-linked]
- **Failure mode accepted:** [e.g. usage models make revenue seasonal; freemium funds non-buyers]

## 3. Tiers and packaging

<!-- Each tier is aimed at a named segment and answers one upgrade question: what
     runs out, or what appears, that moves a customer up. A tier without a named
     segment is a price point looking for a justification. -->

| Tier | Price | Aimed at | What is included | What moves them to the next tier |
|---|---|---|---|---|
| | [amount / period] | | | |
| *Team, $290 per month* | *$290/mo* | *ops teams of 5 to 20* | *core workflow, 3 integrations* | *audit log and SSO appear in the tier above* |

## 4. Competitive benchmark

<!-- Where the alternatives from the positioning doc sit, so the price lands in a
     context, not a vacuum. Include the non-product alternative: the spreadsheet is
     priced at zero plus someone's Tuesdays. -->

| Alternative | Their unit | Their price | Where we sit relative, and why that is defensible |
|---|---|---|---|
| | | [dated, sourced] | |

## 5. Discount rules

<!-- Written before the first negotiation, because mid-deal is where pricing
     integrity goes to die. Anything outside these rules requires the owner's
     sign-off, logged in the [decision log](../execution/decision-log.md). -->

| Situation | Maximum discount | Approver | Expires |
|---|---|---|---|
| | [number, with unit] | [name or role] | [date or condition] |

## 6. Review

- **Review cadence:** [e.g. every two quarters, and at each Gate 6]
- **What triggers an off-cycle review:** [win-loss pattern, competitor move, value-metric drift]
- **Next review:** [date, owner]

A price change worth testing before committing runs as a pricing experiment through [experiment-brief.md](../operate/experiment-brief.md), decision rule and all, before it lands in section 2.

## Exit gate

This pricing is fit to publish when:

- [ ] The value metric is stated, tied to the north star tree or the mismatch is accepted in writing
- [ ] The model names its accepted failure mode
- [ ] Every tier aims at a named segment and names its upgrade trigger
- [ ] The benchmark includes the customer's real alternative, dated and sourced
- [ ] Discount rules exist, with named approvers, before the first negotiation
- [ ] One owner is named who can approve changes, and a review date is on a calendar

Signed: [name], [role], [YYYY-MM-DD]
