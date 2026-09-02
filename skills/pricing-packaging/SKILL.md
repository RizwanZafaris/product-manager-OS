---
name: pricing-packaging
description: Design the willingness-to-pay research, the tiers, and the migration rules for a price or packaging change, and land the decision in the pricing and packaging template. Use when a new product or tier needs its first price, when features move between tiers or the value metric changes, when win-loss keeps naming price, or when a price change is about to reach existing customers. Takes the positioning, the value metric candidate, billing and usage data, and dated competitor prices; returns a research design, findings with their caveats, a tier table, migration rules, and the decision log entry.
---

# Pricing and Packaging: a price you can defend, tiers with a reason, a migration nobody regrets

Pricing fails in three familiar ways. The price is copied from the leader. The tiers are the feature list cut in three. An untested change reaches existing customers as a bill, and the churn arrives before the revenue. This skill runs the research that fits the question, designs tiers around segments and a value metric, and writes the migration rules before the first invoice moves.

## Files this skill drives

- [../../templates/planning/pricing-packaging.md](../../templates/planning/pricing-packaging.md), every section
- Worksheets: [../../frameworks/pricing/van-westendorp.md](../../frameworks/pricing/van-westendorp.md) (van Westendorp, 1976), [../../frameworks/pricing/gabor-granger.md](../../frameworks/pricing/gabor-granger.md) (Gabor and Granger, 1966), [../../frameworks/pricing/packaging-good-better-best.md](../../frameworks/pricing/packaging-good-better-best.md) (common practice; Sawhney, Harvard Business Review, 2018, as the reference)
- [../../templates/operate/experiment-brief.md](../../templates/operate/experiment-brief.md), for a price test before commitment, designed with [../../skills/experiment-designer/SKILL.md](../../skills/experiment-designer/SKILL.md)
- [../../templates/definition/assumptions-register.md](../../templates/definition/assumptions-register.md), one row per guess inside the price
- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where the price decision and every exception to the discount rules land
- Read first: [../../templates/planning/positioning.md](../../templates/planning/positioning.md) for the segment and the category's price assumptions, [../../templates/planning/north-star-metric.md](../../templates/planning/north-star-metric.md) for the value metric tie
- Method background: [../../knowledge/roles/pmm-boundary.md](../../knowledge/roles/pmm-boundary.md), which makes pricing a shared call with one named owner

## When to use

- A first price for a new product, tier, or add-on
- A repackaging: a feature moves between tiers, a tier is added, or the value metric changes
- Win-loss names price in enough losses that the pattern beats the anecdotes, or discounting has drifted from the written rules
- Leadership asks for a price increase and wants to know what it costs in customers
- Before Gate 5, for any release that changes what a customer pays

## Inputs

The positioning: segment, alternatives, category. The value metric candidate from the north star tree. The current price list and the discount reality from billing. The customer base by tier with its usage distribution, from billing and product analytics. Competitor prices, dated and sourced, from [../../skills/competitive-intel/SKILL.md](../../skills/competitive-intel/SKILL.md). Cost to serve per unit, from finance. The one person who can approve a price change.

Ask for what is missing: the single question the research must answer (an acceptable range for a new offer, or the revenue-maximizing point among candidate prices), how many respondents from the best-fit segment can be reached, and whether existing customers are in scope. No cost-to-serve figure means the price floor is unknown, and that is an assumption row, not a detail.

## Workflow

### 1. Fix the value metric before any number

The unit you charge by must scale with the value the customer receives, which is why it should rhyme with the north star tree. Decision rule: a unit that taxes adoption (charging per seat when value scales with volume) or invites bill shock (charging per volume when value is flat) is rejected here, before research, because no survey fixes a wrong unit.

### 2. Choose the research design

Van Westendorp when the offer is new, there is no price anchor, and the question is the acceptable range: four questions per respondent (too cheap, a bargain, getting expensive, too expensive), plotted as cumulative curves. Gabor and Granger when candidate price points exist and the question is the demand curve and the revenue-maximizing point: a ladder of would-you-buy at each price. Both need respondents from the best-fit segment, read per segment, and both overstate what people will actually pay. The respondent floor per segment comes from the worksheet. Decision rule: below that floor, run willingness-to-pay interviews and a pilot invoice test instead of a survey that will be quoted as if it were representative.

### 3. Field, read, and cross-check

Field the questions through `templates/discovery/survey-design.md`, with the bias checks it carries. Read the result by the worksheet's rule. Then cross-check against three anchors: pilot invoices actually paid, the dated competitor benchmark including the non-product alternative, and the cost-to-serve floor. A price under the floor is a decision someone signs, not a finding.

### 4. Design the tiers

Good, better, best. Each tier aims at a named segment and answers one upgrade question: what runs out, or what appears, that moves a customer up. Fences are feature, usage, seat, or support, and the value metric is the same across tiers. Decision rule: a capability gated to the top tier must be one that only the top segment's job needs; a fence built to extract rather than to fit is the row the win-loss review will quote back.

### 5. Write the migration rules

Map every existing customer to a new tier from billing data and compute the distribution of bill changes; the revenue impact is a range from that distribution, not a guess. Set the treatment per cohort: grandfathered for a stated period, price-protected, or moved with notice. Rule: no bill moves without a notice date, a path, and a support macro. Any cohort losing a capability it uses gets a named decision in the decision log.

### 6. Test when reversible, then publish

A change that can be exposed to a slice of new customers runs as a price test through the experiment brief, with conversion, churn, and support volume as guardrails. Write the discount rules before the first negotiation, with approvers and expiry. Fill the pricing template, log the decision, and set the review cadence and the off-cycle triggers.

## Output format

1. Value metric block: unit, how it tracks value, north star tie, evidence or "assumption"
2. Research design: method, why this one, segment, respondent count and its source, questions, the read rule
3. Findings: acceptable range or demand curve summary with the overstatement caveat, and the three cross-checks
4. Tier table: | Tier | Aimed at | Value metric level | Fenced (feature / usage / seat / support) | Upgrade trigger | Price (from findings, or [OPEN: owner]) |
5. Migration table: | Existing cohort | Count (billing) | Bill change range | Treatment | Notice date | Support macro |
6. Discount rules, the decision log entry, the review date, and the assumption rows

## Failure modes this skill guards against

- The leader's price, copied, with the leader's segment never checked
- Tiers cut from the feature list instead of built from segments
- A value metric that taxes the behavior the product exists to grow
- Stated willingness to pay read as paid willingness to pay
- A sample too small to segment, then quoted for every segment
- A migration with no bill-change distribution, discovered as churn
- Discounts invented mid-deal, with no approver and no expiry
- A price test with no guardrail on churn or support
- A price set with cost to serve unknown

## Exit gate

The decision feeds the pricing template's exit gate and Gate 5 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md), where a published price is part of release readiness. Do not report it done until the value metric is tied or the mismatch is accepted in writing, every tier names its segment and trigger, the migration table covers every existing customer, and the decision is logged with one named owner.
