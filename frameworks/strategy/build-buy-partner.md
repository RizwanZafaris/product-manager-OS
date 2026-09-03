---
layer: frameworks
stage: DESIGN
gate: 3
feeds: ["frameworks/strategy/wardley-map.md", "templates/architecture/solution-architecture.md", "templates/architecture/integrations.md"]
method: "knowledge/INDEX.md"
aliases: ["Build, buy, partner, or wait", "build-buy-partner"]
---
# Build, buy, partner, or wait

Based on the ideas of Ronald Coase, from "The Nature of the Firm", Economica (1937), and of Oliver Williamson's transaction-cost economics, from Markets and Hierarchies (1975). Explained here in this repository's own words, with partner and wait added as the two options a strict make-or-buy binary leaves out.

## What it is for

Coase asked why a firm makes some things itself and buys others through the market; his answer was the cost of the transaction, not the price tag alone. This worksheet turns that question into a score for one component: build it, buy a vendor's version, partner with someone who already has it, or wait, because the market has not settled yet. Five criteria carry the decision: strategic core, time to value, total cost over a stated horizon, control, and exit cost, each scored 1 to 5 below. A component gets one row, scored the same way twice, months apart, instead of re-argued from feeling each time it comes up.

## Run it when

- A new component enters the roadmap and engineering asks whether to write it or wire up a vendor
- A vendor contract is up for renewal and building it now costs less than it did last time
- The [Wardley map](wardley-map.md) has placed a component's evolution stage and the team needs to turn that stage into an actual decision
- A partnership is proposed and nobody has priced what walking away from it costs later

**Skip it when:** the [Wardley map](wardley-map.md) already places the component at commodity, several metered vendors, no claim on strategic core. That case is buy or rent in one line; scoring five criteria on a component nobody thinks is a differentiator is theater with a total at the bottom.

## Inputs you need first

- The component definition, narrow enough that one team could own the decision
- Evolution stage and movement from the Wardley map, if one has been run
- Vendor and partner terms that are real: price, contract length, data rights, from the [integrations register](../../templates/architecture/integrations.md) or a vendor scan
- An honest build estimate from engineering: effort, and what it displaces on the roadmap

## The worksheet

### Part 1: score each option

<!-- Score 1 to 5, higher always better, so totals compare directly across options. Strategic core: 5, this is what customers pick us for; 1, a commodity any vendor sells the same way. Time to value: 5, usable inside the horizon's first slice; 1, nothing usable until the whole thing is done. Total cost, over the stated horizon: 5, lowest total cost; 1, highest. Control: 5, we set the roadmap, own the data, can change vendors at will; 1, a vendor can deprecate, reprice, or use our data on its terms. Exit cost: 5, cheap and fast to unwind; 1, locked in by data, contract, or retraining. -->

| Criterion | Weight (sums to 10) | Build | Buy | Partner | Wait |
|---|---|---|---|---|---|
| Strategic core | | | | | |
| Time to value | | | | | |
| Total cost (horizon: [state it]) | | | | | |
| Control | | | | | |
| Exit cost | | | | | |
| Weighted total | | | | | |

**Arithmetic:** each cell's weighted score is score times weight; the total per option is the sum down its column. State the horizon before anyone scores the cost row, or the column compares different bets wearing the same label.

### Part 2: the tie-breaker

**Decision rule:** the highest weighted total wins. Two rules break a close call, in this order.

1. **The strategic-core veto.** If build scores 4 or 5 on strategic core, it wins any total within two points of the leader: a differentiator rented from a vendor stops being one the day a competitor rents it too.
2. **The exit-cost tiebreak.** Otherwise, the higher exit-cost score wins; a close call is a bet you are more likely to unwind. If exit cost also ties, prefer partner over buy over build over wait, each step deferring commitment one notch further.

A tie broken by neither rule means the criteria were scored too coarsely; rescore the two leaders rather than defaulting to seniority in the room.

## Reading the result

- **One option leads by more than two points, no veto in play.** Decide it, and write the losing options' scores into the [decision memo](../../templates/planning/decision-memo.md) so the call can be revisited on facts, not memory.
- **The strategic-core veto fires.** Build, even where the total favors another option on cost or time to value; log the gap as the price of the differentiator, not grounds to reverse the call quietly later.
- **Wait wins.** Name the trigger that ends the wait: a stage change on the Wardley map, a vendor's price move, a date. A wait with no trigger is a decision deferred forever, not one that was made.
- **Every option scores under 3 on strategic core.** The component was never a strategy question. Buy the cheapest option that clears total cost and control, and spend this sheet's time on a component that matters.

## ILLUSTRATIVE example

Invented, Ledgerline's expense copilot. Component: policy logic for multiple entities and currencies, needed only once Ledgerline expands past its single-entity pilot. Weights out of 10: strategic core 3, time to value 2, total cost 2, control 2, exit cost 1. Horizon: two years.

| Criterion | Build | Buy | Partner | Wait |
|---|---|---|---|---|
| Strategic core | 4 | 2 | 3 | 2 |
| Time to value | 2 | 4 | 3 | 1 |
| Total cost | 2 | 4 | 3 | 5 |
| Control | 5 | 2 | 3 | 5 |
| Exit cost | 3 | 2 | 2 | 5 |
| Weighted total | 33 | 28 | 29 | 33 |

Build and wait tie at 33. The strategic-core veto fires: build's score of 4 is evidence-backed, citing the same attribute the [positioning canvas](positioning-canvas.md) example names as unique, so build wins outright over the instinct to defer anything not urgent this quarter. Decision: fund a small build now, ahead of the entity expansion, rather than license the vendor's module later under deadline pressure.

## The trap

Strategic core inflated to win the veto. Any team that wants to build scores its component 4 or 5 regardless of whether a customer would notice the difference, because the veto rule hands build the win the moment that box is checked. The tell: a strategic-core score with no evidence column, a confident number for a component nobody has shown a customer cares about at the attribute level, the test the [positioning canvas](positioning-canvas.md) or the [Seven Powers audit](seven-powers-audit.md) already run. Require that score to cite one of those two sheets before it can trigger the veto; an uncited 4 or 5 is a wish, not a differentiator.

## Feeds

- [Wardley map](wardley-map.md): stage and movement feed the time-to-value and total-cost scores directly
- [Solution architecture](../../templates/architecture/solution-architecture.md) and the [integrations register](../../templates/architecture/integrations.md): the chosen option becomes a row
- [Decision memo](../../templates/planning/decision-memo.md) and the [decision log](../../templates/execution/decision-log.md): the scored options, the tie-breaker used, and the dated decision
- [Risk register](../../templates/execution/risk-register.md): any exit-cost score of 1 or 2 gets a named owner
- General-purpose version of this scoring method: [weighted decision matrix](../prioritization/weighted-decision-matrix.md)
- DESIGN stage, feeds Gate 3
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
