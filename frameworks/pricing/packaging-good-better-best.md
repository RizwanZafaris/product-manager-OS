---
layer: frameworks
stage: PLANNING
gate: 5
feeds: ["templates/planning/pricing-packaging.md", "templates/planning/positioning.md", "templates/delivery/launch-comms-plan.md"]
method: "knowledge/INDEX.md"
aliases: ["Good-better-best packaging", "packaging-good-better-best"]
---
# Good-better-best packaging

The good-better-best pattern is common usage in pricing practice rather than one author's invention; the reference here is Rafi Mohammed's article The Good-Better-Best Approach to Pricing (Harvard Business Review, 2018). Explained here in this repository's own words.

## What it is for

Three tiers let one product serve three willingness-to-pay levels without three products. Good is a real offer for the price-sensitive segment; better is where most customers should land; best carries the capabilities a demanding segment will pay for and anchors the other two. The work is not naming the tiers. It is choosing the value metric (the unit you charge by, which should scale with the value delivered), placing fences (the things that separate one tier from the next and that a customer accepts as fair), and writing the migration rules before existing customers learn there is a new price list. This sheet holds those checks in that order. It improves the packaging decision in the pricing document and the launch decision that depends on it.

## Run it when

- A single price is leaving revenue on the table at the top and adoption on the floor at the bottom.
- A van Westendorp read produced non-overlapping ranges per segment.
- A new capability (policy engine, audit trail, SSO) needs a home that is not "everyone gets it".

**Skip it when:** you have one segment and one job. Three tiers for one kind of customer are a decision tax on every deal; price the product once and revisit when a second segment shows up in win-loss.

## Inputs you need first

- Segments with evidence, from [positioning](../../templates/planning/positioning.md) section 4.
- A price range per segment from [van Westendorp](van-westendorp.md) and a plateau per tier from [Gabor-Granger](gabor-granger.md).
- The capability list classified by a [Kano survey](../discovery/kano-survey.md): must-be capabilities cannot fence a tier.
- The current customer base by plan, with the features each plan actually uses.

## The worksheet

### 1. Value metric

| Candidate unit | Scales with delivered value? | Easy to count and to predict? | Buyer accepts it? | Evidence | Pick |
|---|---|---|---|---|---|
| | yes / partly / no | yes / partly / no | yes / partly / no | [interviews, invoices, or "assumption"] | |

**Decision rule:** pick the unit with no "no" in the first three columns; where two qualify, pick the one buyers already budget in.

### 2. Tiers

| Tier | Segment | Included | Fences at the boundary above | Price (from the ladder) | Upgrade trigger | Cannibalization risk |
|---|---|---|---|---|---|---|
| Good | | | | | [what runs out or appears] | |
| Better | | | | | | |
| Best | | | | | | |

### 3. Fences

| Fence | Type (feature / usage / seat / support) | Boundary | Why the customer accepts it | How it gets gamed |
|---|---|---|---|---|
| | | good to better / better to best | | |

### 4. Tier-design checklist

- [ ] Every tier names a segment and an upgrade trigger
- [ ] Good could be sold alone without embarrassment; it is a product, not a demo
- [ ] Every must-be capability is in Good
- [ ] No boundary uses more than two fence types
- [ ] Best contains at least one capability the demanding segment cannot do without
- [ ] The price steps fit the Gabor-Granger plateaus, not a round-number habit
- [ ] The tier names describe the customer, not the price

### 5. Migration rules

| Existing plan | Maps to | Price change | Grandfathered until | Notice sent by | Exception approver |
|---|---|---|---|---|---|
| | | | [date or renewal count] | [date] | [role] |

**Decision rule:** no customer loses a capability in use without a path to keep it; every price increase gets a stated notice period and a grandfather term; exceptions go through one approver and into the decision log.

## Reading the result

If the fence table is empty at a boundary, the two tiers are one tier with two prices, and sales will always sell the cheaper. If Good fails the sold-alone test, you have built a decoy, and the segment it was meant for will churn loudly and review you on the way out. If Best has nothing a demanding buyer needs, it is an anchor with no buyers, which is fine only if you meant it. Migration is where packaging fails in public: run the mapping against the real customer list before announcing, and count the customers who lose something.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Value metric: active filer per month (a filer who submits at least one report), chosen over seats because value tracks reports, not logins.

| Tier | Segment | Included | Fence above | Price |
|---|---|---|---|---|
| Filer (Good) | teams under 50 filers | capture, card match, submit, status | feature | 8 |
| Team (Better) | mid-market finance teams | adds policy pre-check, approver queue, two ERP connectors | feature plus support | 12 |
| Finance (Best) | firms with audit requirements | adds audit trail, SSO, custom policy rules, named support | none above | 18 |

Migration: customers on the legacy per-seat plan map to Team at their current spend for two renewal cycles; notice 90 days before the first affected renewal; the pricing owner approves exceptions and logs them. The mapping run found 11 accounts using the audit export on the legacy plan; they get Finance at the Team price until their second renewal.

## The trap

The Good tier that is a demo. Someone strips Good until it embarrasses the buyer into Better, the conversion looks good for a quarter, and then the small-team segment that Good was for leaves reviews about the bait. Good has to be a product a satisfied customer could stay on for years. The second failure is the seat fence under shared logins: customers game it, the metric stops tracking value, and finance and sales argue about a number that means nothing. A fence has to be something the customer would rather pay for than work around.

## Feeds

- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 1 (value metric), section 3 (tiers and packaging), section 5 (discount rules)
- [Positioning](../../templates/planning/positioning.md): section 4 (customers who care most), one tier per segment named there
- [Launch comms plan](../../templates/delivery/launch-comms-plan.md): the migration notices
- [Decision log](../../templates/execution/decision-log.md): every migration exception
- PLANNING track, feeding [Gate 5: release readiness green](../../os/STAGE-GATES.md)
- Method background: [knowledge index](../../knowledge/INDEX.md); the [pricing-packaging skill](../../skills/pricing-packaging/SKILL.md) drives the tier design
