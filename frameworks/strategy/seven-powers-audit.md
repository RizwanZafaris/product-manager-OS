---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/product-strategy.md", "templates/discovery/competitive-analysis.md", "templates/planning/pricing-packaging.md"]
method: "knowledge/INDEX.md"
aliases: ["Seven Powers audit", "seven-powers-audit"]
---
# Seven Powers audit

Based on the ideas of Hamilton Helmer, from 7 Powers: The Foundations of Business Strategy (2016). Explained here in this repository's own words.

## What it is for

A feature lead is not an advantage. An advantage is something a capable, well-funded rival cannot or will not take away. Helmer's test has two halves: a power delivers a benefit (a price you can charge or a cost you avoid) and rests on a barrier (a reason the rival does not neutralize it). Seven mechanisms pass that test. The audit walks all seven, scores benefit and barrier separately, and forces one honest conclusion: which power, if any, the product has today, and which one it could build. It improves the "why it holds" line in the strategy, the line most strategies leave to adjectives.

## Run it when

- The strategy's differentiation section says "better UX" or "AI-native"
- Before a pricing decision that assumes customers will not defect
- When a rival ships your headline feature and the team wants to know how much it matters
- When leadership asks whether an internal tool could be sold, before anyone sizes the market
- At each annual strategy refresh, because powers arrive and decay with the product's stage

**Skip it when:** the product has no external customers and nobody is proposing to find any. An internal tool competes with a vendor's licence, not for a market; the [build, buy, partner](build-buy-partner.md) sheet answers that question in an hour, and seven zeros here answer nothing.

## Inputs you need first

- Competitive analysis, sections 4 and 5: what rivals actually have, dated
- Unit cost and price facts from the [pricing and packaging](../../templates/planning/pricing-packaging.md) sheet, or the internal cost to run
- Retention or churn evidence, if any, from the [metrics review](../../templates/operate/metrics-review.md)
- Contracts and exclusive arrangements: what the company holds that others cannot buy

## The worksheet

<!-- Scores: 0 none, 1 plausible with evidence pending, 2 demonstrated with linked evidence. Score benefit and barrier separately; a benefit with no barrier is a head start, not a power. The stage column is Helmer's observation that powers become available at different points in a product's life; it tells you where to look, not what to claim. -->

| Power | Mechanism, in one line | Typical stage | Benefit for us (specific) | Barrier (why a capable rival does not copy) | Evidence | Benefit 0 to 2 | Barrier 0 to 2 | Verdict |
|---|---|---|---|---|---|---|---|---|
| Scale economies | Unit cost falls with volume, so the leader can underprice | Takeoff | | | | | | |
| Network economies | Each user makes the product worth more to the next | Takeoff | | | | | | |
| Counter-positioning | Our model would damage the incumbent's business if copied, so they hesitate | Origination | | | | | | |
| Switching costs | Leaving costs the customer more than staying | Takeoff | | | | | | |
| Branding | Buyers pay more for the name on otherwise identical goods | Stability | | | | | | |
| Cornered resource | We hold an asset others cannot obtain at any price | Origination | | | | | | |
| Process power | An embedded way of working that takes years to replicate | Stability | | | | | | |

**Decision rule:** a power exists only when benefit and barrier both score 2. Both at 1 is a candidate: name the path from 1 to 2. Anything else is 0 and gets written as "none". Claim at most two powers; a sheet that claims four has confused benefits with barriers.

**Conclusion (mandatory, one line):** [the power we have, or "none yet; candidate: [power]; path: [what makes the barrier real]"]

## Reading the result

- **One demonstrated power.** Write it into the strategy's "why it holds" line and price against it. Protect it in the roadmap before adding features.
- **A candidate only.** The strategy is a plan to build a barrier. Sequence the moves that turn the 1 into a 2 and give them a metric.
- **None.** Honest and common. The strategy is execution speed, and the [risk register](../../templates/execution/risk-register.md) gets a row: "a funded rival matches the product within [period]".
- **Benefit 2, barrier 0 anywhere.** That is the feature you are about to lose. Assume a copy within two release cycles and decide now whether to defend it or move on.

## ILLUSTRATIVE example

Invented. Ledgerline's finance lead asked whether the internal expense copilot could be sold to other mid-market firms; the audit answers what power Ledgerline would hold in that market.

| Power | Benefit | Barrier | Scores | Verdict |
|---|---|---|---|---|
| Counter-positioning | Drafting with the policy line and the filer as author removes the resubmission loop that vendor tools sell services around | Nothing stops a vendor adding a policy line to its draft; their services revenue is not large enough to make them hesitate | 1 / 0 | None |
| Cornered resource | A category-to-policy mapping learned from reviewer corrections | The mapping is specific to Ledgerline's own policy; a buyer's would start from zero | 1 / 0 | None |
| Switching costs | A customer's correction history would accumulate | It exports in one click; a day of work to leave | 1 / 0 | None |
| The other four | No installed base, no brand, no scale, no process worth naming | | 0 / 0 | None |

Conclusion: no power, and no candidate. If the copilot is ever sold, it competes on execution speed alone, and the business case has to say so rather than lean on "our AI is better".

## The trap

Barrier confused with lead. The barrier column fills with "we are a year ahead", "our model is better", or "we know the policy". None of those stops a rival; they describe how long the copy takes. The sheet then reports two or three powers for a product a funded rival could match in a year, and the pricing built on it assumes retention the product has not earned. Test every barrier entry with one question: if a rival with twice our budget did exactly this tomorrow, what stops them? If the answer is a duration, score the barrier 0.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 3 (how we win), the "why it holds" line
- [Competitive analysis](../../templates/discovery/competitive-analysis.md): section 5 (axes) and section 6 ("where we are genuinely behind")
- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 4, competitive benchmark
- [Business case](../../templates/planning/business-case.md): the defensibility line under its options, when productization is the question
- [Risk register](../../templates/execution/risk-register.md): the "benefit without barrier" rows
- PLANNING track
- Method background: [knowledge index](../../knowledge/INDEX.md), 7 Powers entry
