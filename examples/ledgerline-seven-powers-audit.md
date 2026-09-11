# Seven Powers audit: Ledgerline Expense Copilot

Fills [frameworks/strategy/seven-powers-audit.md](../frameworks/strategy/seven-powers-audit.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, and every figure are fiction built for this repository and are not benchmarks or claims about any real product.

**Owner:** Maya Chen, Product Manager · **Date:** 2026-10-28 · **Status:** Audited, no power demonstrated; one candidate

## What it is for

This audit tests whether the Ledgerline Expense Copilot has an advantage that a capable, well-funded rival cannot or will not take away. It separates the benefit from the barrier, rather than treating a useful feature or an integration as a power.

The commercial trigger was the pricing decision that would assume Business-plan customers would not defect to Cinderwick. The Q3 win-loss batch recorded 31 lost Business-plan deals, 9 naming receipt capture as the primary reason, and 7 of those 9 choosing Cinderwick. That evidence creates a reason to test defensibility, not a reason to claim it.

The audit uses the seven mechanisms associated with Hamilton Helmer's *7 Powers: The Foundations of Business Strategy* (2016), explained here in the repository's own words.

## Run it when

- Before a pricing decision that assumes customers will not defect to Cinderwick
- When a rival has a credible receipt-capture offer
- When the team wants to distinguish Ledgerline's platform data from a feature that a stand-alone vendor could copy
- When the strategy needs an honest "why it holds" line
- At a later strategy refresh, if the approval-rate tile turns the candidate into a demonstrated barrier

**Skip it when:** there are no external customers and nobody is proposing to find any. That is not the state here: Ledgerline has 6,400 Business accounts, and the pricing question is explicitly customer-facing.

## Inputs you need first

- The [Ledgerline journey data sheet](ledgerline-journey.md), especially N26, N37 and the shared identifier for LEDGERLINE-S5
- The [Ledgerline coverage sheet](ledgerline-coverage-sheet.md), especially LC9, which records this audit's scores and conclusion
- Evidence about the alternative: 7 of the 9 lost Business-plan deals that named receipt capture chose Cinderwick, from N37
- Evidence about the owned asset: the approval flow and approval events of the 6,400 Business accounts, from N26
- Evidence about the proposed path to a barrier: LEDGERLINE-S5, the customer-facing approval-rate tile
- The distinction between a benefit and a barrier: a useful approval-rate view is not yet a power unless its data access and customer value create a barrier a rival cannot neutralize

## The worksheet

| Power | Mechanism, in one line | Typical stage | Benefit for us (specific) | Barrier (why a capable rival does not copy) | Evidence | Benefit 0 to 2 | Barrier 0 to 2 | Verdict |
|---|---|---|---|---|---|---:|---:|---|
| Scale economies | Unit cost falls with volume, so the leader can underprice | Takeoff | Ledgerline has 6,400 Business accounts, but the audit has no evidence that customer-scale receipt capture lowers Ledgerline's unit cost below Cinderwick's quoted $8 per seat per month. | No demonstrated cost curve, volume contract, or cost advantage that a capable rival could not match. | [N26 and N13 in the journey](ledgerline-journey.md) | 0 | 0 | None |
| Network economies | Each user makes the product worth more to the next | Takeoff | The approval-rate tile could make an account's own workflow more useful to its admins and reviewers, but no cross-account or user-to-user value has been demonstrated. | One account's approval events do not yet make the product more valuable to another account, and no network effect is evidenced. | [N26 and LEDGERLINE-S5 in the journey](ledgerline-journey.md), [LC9 in the coverage sheet](ledgerline-coverage-sheet.md) | 0 | 0 | None |
| Counter-positioning | Our model would damage the incumbent's business if copied, so they hesitate | Origination | Ledgerline can place the copilot inside the platform that Business accounts already run, while Cinderwick is a stand-alone receipt-capture vendor. | Cinderwick can add a comparable platform connection or approval-rate view without a demonstrated conflict with its existing business model. The difference is a positioning lead, not a barrier. | [N26, N37 and N13 in the journey](ledgerline-journey.md) | 1 | 0 | None |
| Switching costs | Leaving costs the customer more than staying | Takeoff | Approval history and approval events could become useful to an account's finance reviewers if the copilot becomes part of the approval workflow. | No evidence shows that leaving would make the customer lose an accumulated asset or incur a material migration cost. The candidate is not yet a switching-cost power. | [N35 and N37 in the journey](ledgerline-journey.md), [LC9 in the coverage sheet](ledgerline-coverage-sheet.md) | 1 | 0 | None |
| Branding | Buyers pay more for the name on otherwise identical goods | Stability | Ledgerline already owns the platform relationship with 6,400 Business accounts, which may support trust in an add-on. | The audit has no evidence that buyers pay more for the Ledgerline name or prefer it to Cinderwick for otherwise identical receipt capture. | [N26 and N37 in the journey](ledgerline-journey.md) | 0 | 0 | None |
| Cornered resource | We hold an asset others cannot obtain at any price | Origination | Ledgerline holds the approval flow and approval events of the 6,400 Business accounts. A customer-facing approval-rate tile could turn that platform-held data into a product benefit that a stand-alone vendor cannot see. | The asset is a candidate barrier only. The approval-rate tile, LEDGERLINE-S5, must make the account's own approval performance visible and useful in the workflow. Until that path is used and its customer value is demonstrated, a capable rival may still compete on the surrounding receipt-capture job. | [N26 and LEDGERLINE-S5 in the journey](ledgerline-journey.md), [LC9 in the coverage sheet](ledgerline-coverage-sheet.md) | 1 | 1 | Candidate |
| Process power | An embedded way of working that takes years to replicate | Stability | Ledgerline's approval flow can connect drafting to review and approval events inside the existing platform workflow. | The audit has no evidence that the way of working has been embedded for long enough, or is difficult enough to learn, to stop a capable rival from copying the workflow. | [N26 and LEDGERLINE-S5 in the journey](ledgerline-journey.md), [LC9 in the coverage sheet](ledgerline-coverage-sheet.md) | 0 | 0 | None |

**Score check:** the only candidate is cornered resource at benefit 1 and barrier 1. Every other row fails the two-score test: scale \(0 / 0\), network \(0 / 0\), counter-positioning \(1 / 0\), switching costs \(1 / 0\), branding \(0 / 0\), and process power \(0 / 0\).

**Decision rule:** a power exists only when benefit and barrier both score 2. Both at 1 is a candidate, so the cornered-resource row requires a path from 1 to 2. No row scores 2 / 2, and this audit claims no demonstrated power.

**Conclusion (mandatory, one line):** none yet; candidate: cornered resource; path: use the approval-rate tile (LEDGERLINE-S5) to make the approval flow and approval events of the 6,400 Business accounts a customer-visible benefit that a stand-alone vendor cannot see, then demonstrate that this creates a durable barrier

## Reading the result

- **No demonstrated power.** The Ledgerline Expense Copilot should not be priced on an assumption that customers will stay because Ledgerline has a power. The strategy is execution speed and product value until the candidate is tested.
- **One candidate.** The strategy can build toward a cornered resource, but the asset alone is not enough. LEDGERLINE-S5 is the path to test: show an account admin the account's first-submission approval rate before and after activation.
- **The candidate's metric.** The relevant product path is the approval-rate tile, not the existence of the underlying events. The tile must make the platform-held data useful to the customer in a way a stand-alone vendor cannot reproduce.
- **Competitive implication.** Cinderwick remains a credible alternative. The audit therefore does not support a premium based on defensibility, even though Ledgerline may have a distribution and data-access lead.
- **Strategy implication.** Keep the "why it holds" line conditional: Ledgerline may hold a cornered resource in the approval flow and approval events, but it has not yet demonstrated the barrier.
- **Pricing implication.** The pricing decision should not claim that the candidate is a power. The Q3 evidence is 31 lost Business-plan deals, 9 naming receipt capture as the primary reason, and 7 of those 9 choosing Cinderwick. That is evidence of competitive pressure, not evidence of retention.
- **Next audit condition.** Re-run this worksheet after LEDGERLINE-S5 has evidence that the approval-rate view changes customer behaviour or creates a loss that a stand-alone vendor cannot avoid. Until then, the verdict remains none yet.

## ILLUSTRATIVE example

Ledgerline's candidate is narrower than "we have the platform" or "our UX is better":

| Test | Result |
|---|---|
| Benefit | The approval flow and approval events of 6,400 Business accounts could support an account-specific approval-rate view. |
| Barrier | A stand-alone vendor cannot see those platform-held approval events. |
| Current score | 1 benefit / 1 barrier, so candidate, not power. |
| Path | LEDGERLINE-S5, the approval-rate tile, must turn the private platform data into a durable customer benefit. |
| Honest conclusion | None yet. |

The candidate does not reuse the stand-alone Ledgerline example from the blank worksheet. It is about the Ledgerline product's customer-facing add-on and its existing platform-held approval data.

## The trap

The trap here would be treating access to Ledgerline's platform as a finished power. The 6,400 Business accounts and their approval events are a potentially valuable resource, but the audit does not yet show that customers value the resulting tile enough to stay, pay, or accept a switching cost.

A capable rival could copy a drafting feature, an approval-rate display, or a platform integration unless the underlying account approval data creates a durable difference. The barrier score therefore stays at 1 until LEDGERLINE-S5 demonstrates that difference.

The audit also avoids converting the Cinderwick comparison into a power claim. Cinderwick is quoted at $8 per seat per month, and 7 of 9 lost deals naming receipt capture chose it. Ledgerline's position inside the platform may help distribution, but distribution is not automatically counter-positioning, branding, scale, or process power.

## Feeds

- [Product strategy](../templates/planning/product-strategy.md): section 3, the "why it holds" line, kept conditional until the candidate reaches 2 / 2
- [Competitive analysis](../templates/discovery/competitive-analysis.md): the Cinderwick comparison and the evidence that 7 of 9 relevant lost deals chose Cinderwick
- [Pricing and packaging](../templates/planning/pricing-packaging.md): do not price as though a demonstrated power already exists
- [Risk register](../templates/execution/risk-register.md): record the risk that a capable rival matches the product before the candidate becomes a barrier
- [Ledgerline journey data sheet](ledgerline-journey.md): N13, N26, N35, N37 and LEDGERLINE-S5
- [Ledgerline coverage sheet](ledgerline-coverage-sheet.md): LC9, the dated Seven Powers scores and conclusion
- PLANNING track
- Method background: [knowledge index](../knowledge/INDEX.md), Seven Powers entry
