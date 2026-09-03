---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/product-strategy.md", "templates/planning/growth-plan.md", "templates/planning/roadmap.md"]
method: ""
aliases: ["Ansoff matrix", "ansoff-matrix"]
---
# Ansoff matrix

Based on the ideas of H. Igor Ansoff, from "Strategies for Diversification", Harvard Business Review (1957). Explained here in this repository's own words.

## What it is for

Every growth move combines a product (existing or new) with a market (existing or new). That gives four cells: market penetration (same product, same market, more of it), product development (new product for the market you have), market development (the product you have, taken to a market you do not), and diversification (new product, new market). The matrix rests on one observation: risk rises with distance from the cell you are in, because each step away replaces knowledge with assumption. The worksheet places each candidate move in its cell, records what you actually know about the market side and the product side, and sets the evidence bar before funding accordingly.

## Run it when

- A roadmap or growth plan mixes moves of very different risk and prices them all as "a quarter"
- Someone proposes a new user group and calls it "the same product, so low risk"
- The core has stalled and diversification is suddenly attractive
- When the [product strategy](../../templates/planning/product-strategy.md) where-to-play table needs a risk band per bet

**Skip it when:** every candidate move sits in the penetration cell. Sequencing more of the same is a [RICE](../../knowledge/rice-prioritization.md) question, and the matrix will only tell you what you knew.

## Inputs you need first

- The candidate moves, from the [growth plan](../../templates/planning/growth-plan.md) section 2 or the roadmap's Next and Later columns
- Market evidence for any "new market" claim: discovery document, personas, win-loss reviews
- Capability evidence for any "new product" claim: what has shipped and been measured
- The current cell, proven by usage and retention rather than by ambition

## The worksheet

<!-- "New market" means a user group whose buyer, buying process, or job differs from the one you serve today, even if the product is unchanged. "New product" means a capability you have not shipped and measured. Risk band by cell: penetration 1, product development 2, market development 3, diversification 4. -->

| Move | Product: existing or new (why) | Market: existing or new (why) | Cell | Risk band 1 to 4 | What we know about the market (evidence) | What we know about the product (evidence) | Evidence required before funding | Share of period capacity |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

**Evidence bars by band.** Band 1: a measured baseline and a target. Band 2: validated problem evidence from existing users (interviews or tickets) and a prototype test. Band 3: five or more conversations with the new group, one named alternative they use today, and a channel you can prove reaches them. Band 4: a separate [business case](../../templates/planning/business-case.md) with its own Gate 1, and a beachhead defined per [Crossing the Chasm](../../knowledge/crossing-the-chasm.md).

**Decision rule.** No move is funded above its evidence bar. While the core is unproven (adoption not yet at target, the success signal not yet moving), band 3 and 4 moves together take a small, stated share of capacity, and never the strongest engineer. A band 4 move funded because the core is stalling is a bet made when the company can least afford to lose it; size it like one.

## Reading the result

- **Most capacity in bands 1 and 2.** Healthy for a product before scale. Sequence band 1 by RICE, band 2 by the growth plan's cheapest experiment.
- **A band 3 move labelled band 1.** The commonest misfile; see the trap. Re-place it and find the five conversations.
- **A band 4 move in the Now column.** Pull it back to a business case with a gate. If the core cannot spare the capacity, it cannot spare the distraction either.
- **Nothing above band 1.** The roadmap is maintenance. Fine for a period, not for a strategy; revisit the vision's why-now.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Current cell: the internal copilot, used by Ledgerline's own filers who travel a few times a quarter.

| Move | Cell | Band | Evidence held | Evidence required | Capacity |
|---|---|---|---|---|---|
| Raise adoption from half of eligible reports toward all of them, without a mandate | Penetration | 1 | Adoption measured weekly since launch | A target and a nudge experiment | 30 percent |
| Card-feed reconciliation and mileage for the same filers | Product development | 2 | Nine tickets and four interviews asking for it | Prototype test with six filers | 25 percent |
| The copilot for executive assistants filing on behalf of others | Market development | 3 | Parked at discovery as a distinct workflow; one interview | Five assistant interviews, the alternative they use, a rollout path through their managers | 10 percent, discovery only |
| Sell the copilot to other mid-market firms | Diversification | 4 | The finance lead's enthusiasm and one peer's interest at a conference | A business case with its own Gate 1, a market sizing, a beachhead | 0 this period |

Reading: the assistants move was proposed as "penetration, same product"; the user, the accountability rules, and the workflow all differ, so it is band 3 and funds discovery only. Selling the copilot is band 4 whatever the demo looks like.

## The trap

The same-product fallacy. A new user group gets filed as penetration because the code does not change, so the move is funded at band 1 with no evidence about the group. Ledgerline's version: the assistants who file for executives were treated as more filers, and the pilot found they file in batches, from forwarded receipts, under someone else's policy exceptions; the draft flow fit none of it and the quarter went to rework. The cell is set by the user and the job, never by the codebase, and a group whose workflow you have not watched is a new market.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 2 (where to play), the risk band per bet
- [Growth plan](../../templates/planning/growth-plan.md): section 2 (the next growth bet) and section 4 (the cheapest experiment)
- [Roadmap](../../templates/planning/roadmap.md): Next and Later carry the band; band 4 moves sit in Parked until a business case exists
- [Business case](../../templates/planning/business-case.md): required for any band 4 move
- PLANNING track
- Method background: [Crossing the Chasm](../../knowledge/crossing-the-chasm.md) for the beachhead rule; no Ansoff card exists, see the [knowledge index](../../knowledge/INDEX.md)
