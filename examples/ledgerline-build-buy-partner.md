# Build, buy, partner, or wait

Fills [frameworks/strategy/build-buy-partner.md](../frameworks/strategy/build-buy-partner.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its product, its options and every score are fiction built to show the worksheet method, not to recommend a real decision.

**Owner:** Priya Nair, Engineering Lead · **Date:** 2026-12-22 · **Status:** Build selected for ADR-008

## What it is for

This worksheet scores the drafted-report meter for the Ledgerline Expense Copilot. The component is narrow enough for one team to own: count drafted reports on the product side and feed the monthly count into the billing system's invoice run.

The decision is between four options:

- **Build:** a product-side counter feeding the billing system's invoice run, as proposed by ADR-008.
- **Buy:** a new third-party metering vendor.
- **Partner:** count drafts from the model vendor's usage report. The known gap is that the vendor bills one line per period, not per account, which weakens account-level control for M-009.
- **Wait:** use the billing platform's general usage module when it is available, not before Q2 2027.

The [journey data sheet](ledgerline-journey.md) records N87, DEP4, M-009 and ADR-008. The [coverage sheet](ledgerline-coverage-sheet.md) records LC14 and LC15, including the scores, weights and option inputs.

## Run it when

- A component enters the roadmap and the team must decide whether to write it or wire up another system.
- A dependency or architecture decision changes the available options.
- A component's evolution stage and movement need to become an implementation decision.
- A partnership or vendor option is proposed and the team needs to price control and exit cost, not only implementation cost.

This run is appropriate because ADR-008 proposes a new product-side usage meter, DEP4 is open, and the billing platform's general usage module is not expected before Q2 2027.

## Inputs you need first

| Input | Ledgerline evidence | Use in this worksheet |
|---|---|---|
| Component definition | Drafted-report meter: product-side count feeding the billing system's invoice run | Defines the build option |
| Evolution evidence | Three document-extraction APIs checked on 2026-12-18, all metered; three metered-billing vendors checked on 2026-12-18 | The component is not treated as an unproven category |
| Build estimate | N87: 1 person-month, $10,000 at the engineering cost rate, needed by 2027-01-08; DEP4 is open | Inputs for build timing and cost |
| Buy input | LC15: about 2% of billed usage revenue, about 3 weeks of integration, and a new vendor DPA | Inputs for the buy option |
| Partner input | LC14: the model vendor's usage report bills one line per period, not per account, creating a known M-009 gap | Inputs for control and exit scoring |
| Wait input | LC15: the billing platform's usage module is not expected before Q2 2027 | Input for time to value |

The horizon for the cost row is **12 months**, as stated in LC14. The scoring is an estimate recorded on 2026-12-22. The build estimate is from N87, and the option timing and commercial assumptions are from LC15.

## The worksheet

### Part 1: score each option

Higher is better for every criterion. Each score is from 1 to 5. The weights sum to 10:

- Strategic core: 2
- Time to value: 3
- Total cost over 12 months: 2
- Control: 2
- Exit cost: 1

The scores below are the LC14 scores. Each weighted cell shows the score multiplied by its weight.

| Criterion | Weight (sums to 10) | Build | Buy | Partner | Wait |
|---|---:|---:|---:|---:|---:|
| Strategic core | 2 | 3, 3 x 2 = 6 | 1, 1 x 2 = 2 | 1, 1 x 2 = 2 | 1, 1 x 2 = 2 |
| Time to value | 3 | 5, 5 x 3 = 15 | 2, 2 x 3 = 6 | 1, 1 x 3 = 3 | 1, 1 x 3 = 3 |
| Total cost (horizon: 12 months) | 2 | 4, 4 x 2 = 8 | 2, 2 x 2 = 4 | 5, 5 x 2 = 10 | 5, 5 x 2 = 10 |
| Control | 2 | 5, 5 x 2 = 10 | 2, 2 x 2 = 4 | 1, 1 x 2 = 2 | 4, 4 x 2 = 8 |
| Exit cost | 1 | 4, 4 x 1 = 4 | 2, 2 x 1 = 2 | 3, 3 x 1 = 3 | 5, 5 x 1 = 5 |
| **Weighted total** | **10** | **6 + 15 + 8 + 10 + 4 = 43** | **2 + 6 + 4 + 4 + 2 = 18** | **2 + 3 + 10 + 2 + 3 = 20** | **2 + 3 + 10 + 8 + 5 = 28** |

#### Score rationale

| Criterion | Build | Buy | Partner | Wait |
|---|---|---|---|---|
| Strategic core | 3: the meter supports the proposed usage metric and ADR-008, but the drafted-report meter is not itself the product's customer-facing differentiation | 1: a new metering vendor provides a generic capability | 1: the model vendor's usage report provides a generic usage record rather than a Ledgerline-owned capability | 1: the general billing usage module is a platform capability rather than a product differentiator |
| Time to value | 5: N87 estimates 1 person-month and DEP4 is needed by 2027-01-08 | 2: LC15 includes about 3 weeks of integration and a new vendor DPA | 1: the team depends on the model vendor's reporting shape and its one-line-per-period billing | 1: the billing platform's usage module is not expected before Q2 2027 |
| Total cost over 12 months | 4: N87 estimates 1 person-month at $10,000 | 2: LC15 assumes about 2% of billed usage revenue, plus integration and a new vendor DPA | 5: the existing model-vendor usage report avoids a new metering vendor cost | 5: waiting avoids a new build or vendor cost during the stated horizon |
| Control | 5: the product owns the drafted-report count and can feed the billing invoice run through ADR-008 | 2: a vendor can change terms, reporting or pricing on its terms | 1: the model vendor reports one line per period, not per account, leaving the M-009 gap | 4: the billing platform is more controllable than a model vendor or new metering vendor, but the module is not yet available |
| Exit cost | 4: the product-side counter can be replaced or adjusted without adopting a new vendor's reporting contract | 2: exit includes vendor, integration and DPA work | 3: exit requires replacing the vendor report as the source for usage | 5: waiting defers commitment and leaves no new vendor or integration to unwind |

**Arithmetic:** the weighted score for each cell is the criterion score multiplied by its weight. The totals are:

- Build: `3 x 2 + 5 x 3 + 4 x 2 + 5 x 2 + 4 x 1 = 6 + 15 + 8 + 10 + 4 = 43`
- Buy: `1 x 2 + 2 x 3 + 2 x 2 + 2 x 2 + 2 x 1 = 2 + 6 + 4 + 4 + 2 = 18`
- Partner: `1 x 2 + 1 x 3 + 5 x 2 + 1 x 2 + 3 x 1 = 2 + 3 + 10 + 2 + 3 = 20`
- Wait: `1 x 2 + 1 x 3 + 5 x 2 + 4 x 2 + 5 x 1 = 2 + 3 + 10 + 8 + 5 = 28`

Build leads with **43**. Wait is second with **28**, Partner is third with **20**, and Buy is fourth with **18**.

### Part 2: the tie-breaker

**Decision rule:** the highest weighted total wins. Build scores 43, which is 15 points above Wait at 28.

1. **The strategic-core veto.** The veto is not needed. Build's strategic-core score is 3, not 4 or 5.
2. **The exit-cost tiebreak.** The tiebreak is not needed because the leader does not have a close call within two points. The 15-point lead is conclusive.
3. **Decision.** Build the product-side drafted-report meter proposed by ADR-008. It is the selected option for DEP4.

The result is **Build**, with no tie-break needed. The component will count drafted reports on the product side and feed the count into the billing system's invoice run. N87 estimates 1 person-month and $10,000 at the engineering cost rate, and DEP4 is needed by 2027-01-08.

## Reading the result

- **One option leads by more than two points, no veto in play.** Build leads Wait by 15 points, so the decision is Build.
- **The strategic-core veto fires.** It does not fire. Build's strategic-core score is 3.
- **Wait wins.** It does not win. Wait scores 28, below Build's 43. The wait trigger remains the billing platform's general usage module becoming available, which LC15 says is not expected before Q2 2027.
- **Every option scores under 3 on strategic core.** Buy, Partner and Wait score 1, while Build scores 3. The component is still a strategy and architecture decision because the choice determines how Ledgerline measures the customer value metric, controls account-level billing and handles the M-009 known gap.

The selected option is therefore:

| Decision field | Result |
|---|---|
| Component | Drafted-report meter |
| Selected option | Build |
| Implementation shape | Product-side counter feeding the billing system's invoice run |
| Weighted score | 43 |
| Next dependency | DEP4, usage meter counted per account and billed in arrears |
| Needed by | 2027-01-08 |
| Related ADR | ADR-008, proposed 2026-12-22 |
| Horizon scored | 12 months |
| Unresolved input | M-009 remains a guardrail, with the model-vendor usage report's per-period, not per-account, gap retained as a reason not to select Partner |

## ILLUSTRATIVE example

This completed worksheet is the Ledgerline example. The decision is to build the drafted-report meter, not to buy a new metering vendor, partner through the model vendor's usage report, or wait for the billing platform's general usage module.

The arithmetic is:

`Build = 3 x 2 + 5 x 3 + 4 x 2 + 5 x 2 + 4 x 1 = 43`

`Wait = 1 x 2 + 1 x 3 + 5 x 2 + 4 x 2 + 5 x 1 = 28`

`Partner = 1 x 2 + 1 x 3 + 5 x 2 + 1 x 2 + 3 x 1 = 20`

`Buy = 1 x 2 + 2 x 3 + 2 x 2 + 2 x 2 + 2 x 1 = 18`

Build leads Wait by:

`43 - 28 = 15 points`

Because the lead is more than two points and Build does not score 4 or 5 on strategic core, neither tie-break rule changes the result. Priya Nair selects Build for ADR-008 and DEP4.

## The trap

The main trap is treating the cheapest or most available usage source as equivalent to an account-level drafted-report meter.

Partner scores 20 because the existing model-vendor usage report has a low total-cost score, but it scores 1 for control. The vendor bills one line per period, not per account, which leaves the M-009 known gap. That makes the source unsuitable for the account-level count needed by the proposed usage price.

Wait scores 28 because it avoids immediate implementation cost and has good eventual exit cost, but its time-to-value score is 1. LC15 says the billing platform's general usage module is not expected before Q2 2027. Waiting would leave DEP4 open while EXP-2 depends on the usage meter.

Buy scores 18 because a new metering vendor adds about 2% of billed usage revenue, about 3 weeks of integration and a new vendor DPA, as recorded in LC15. Its lower total is not only a price comparison. It also reflects reduced control and a higher exit cost.

The build score is not a claim that the meter is strategically differentiating on its own. Its advantage comes from delivering the required usage metric within the stated horizon while preserving product-side control over the count and the billing handoff.

## Feeds

- [Wardley map](ledgerline-wardley-map.md): the component's stage and movement support the build decision for a small product-side meter.
- [Solution architecture](../templates/architecture/solution-architecture.md) and [integrations register](../templates/architecture/integrations.md): ADR-008 and DEP4 become architecture and integration rows.
- [Decision memo](../templates/planning/decision-memo.md) and [decision log](../templates/execution/decision-log.md): record the scored options, the 43 to 28 result, the absence of a tie-break and the dated decision.
- [Risk register](../templates/execution/risk-register.md): retain M-009's known gap and assign any exit-cost concern to an owner.
- [Weighted decision matrix](../frameworks/prioritization/weighted-decision-matrix.md): the related Ledgerline worksheet records the earlier value-metric choice that this meter enables.
- DESIGN stage, feeds Gate 3.
- Method background: the worksheet is based on Ronald Coase, from "The Nature of the Firm", Economica (1937), and Oliver Williamson's transaction-cost economics, from Markets and Hierarchies (1975). Partner and wait are added here to the make-or-buy binary.
