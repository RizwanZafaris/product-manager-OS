---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["frameworks/strategy/business-model-canvas.md", "frameworks/strategy/lean-canvas.md", "frameworks/strategy/positioning-canvas.md"]
method: "knowledge/INDEX.md"
aliases: ["Value proposition canvas", "value-proposition-canvas"]
---
# Value proposition canvas

Based on the ideas of Alexander Osterwalder, Yves Pigneur, Gregory Bernarda, and Alan Smith, from Value Proposition Design (2014). Explained here in this repository's own words.

## What it is for

The canvas zooms into the two blocks of the business model canvas most likely to be wrong: customer segments and value propositions. Two halves face each other. The customer profile lists what a segment is trying to get done (jobs: functional, social, emotional), what stands in the way (pains), and what a good outcome looks like (gains). The value map lists what you offer (products and services), what removes a pain (relievers), and what produces a gain (gain creators). Fit is not a feeling; it is a line from a ranked pain or gain to the value-map item that addresses it, backed by evidence a customer agrees, not the team's confidence that it should. The canvas improves one decision: whether to build the thing you are about to build, or learn more about the job first.

## Run it when

- A candidate solution or feature exists and needs testing against real jobs, pains, and gains before engineering time is committed
- [Personas](../../templates/discovery/personas.md) or a [JTBD spec](../../templates/discovery/jtbd-spec.md) exist with evidence, and the open question is what to build for them
- A value proposition line is being drafted for [positioning](positioning-canvas.md) or [pricing](../../templates/planning/pricing-packaging.md) and needs checking against what customers actually rank highest
- Sales or support keeps hearing the same objection and nobody has mapped it to a named pain

**Skip it when:** no job map or interview evidence exists yet for the segment. The canvas ranks jobs, pains, and gains; ranking a blank page produces a confident-looking guess. Run the [JTBD job map](../discovery/jtbd-job-map.md) or the [Mom Test interviews](../discovery/mom-test-interview-guide.md) first.

## Inputs you need first

- Evidence on the customer side: a job map, JTBD spec, interview evidence notes, or a filled empathy map
- A candidate value map: the product, feature, or service under test, however early
- The segment definition, precise enough that two people would profile the same person
- Existing objections or churn reasons, if any, from support or sales notes

## The worksheet

### Part 1: customer profile

<!-- Rank 1 to 3. Jobs: 1 low importance, 2 useful, 3 must be addressed to win the choice. Pains: 1 mild irritant, 2 costs time or money, 3 blocks the job or is why they would leave. Gains: 1 nice to have, 2 expected, 3 would win the choice outright. Rank from evidence, not from what the team wants to be true. -->

| # | Category (job / pain / gain) | Sub-type (functional / social / emotional; leave blank for pains and gains) | What it is, in the customer's words | Rank 1 to 3 | Evidence |
|---|---|---|---|---|---|
| 1 | Job | | | | |
| 2 | Job | | | | |
| 3 | Pain | n/a | | | |
| 4 | Pain | n/a | | | |
| 5 | Gain | n/a | | | |
| 6 | Gain | n/a | | | |

### Part 2: value map

| # | Category (product/service / pain reliever / gain creator) | What we offer | Which Part 1 item it addresses | Evidence it works, not a feature description |
|---|---|---|---|---|
| 1 | Product/service | | | |
| 2 | Pain reliever | | [item #] | |
| 3 | Gain creator | | [item #] | |

### Part 3: the fit test

<!-- Fit is scored only for Part 1 items ranked 3. A rank-3 item with no linked row, or a linked row with no evidence beyond the team's belief, is not fit. -->

| Part 1 item (rank 3 only) | Linked value map item | Fit status: on paper / evidenced / none |
|---|---|---|
| | | |

**Decision rule:** count the rank-3 rows and apply Osterwalder's three levels in order, never out of sequence. Problem-solution fit: the map addresses the profile on paper. Product-market fit: the market responds, evidenced by real usage or willingness to pay. Business-model fit: the economics work, checked in the [business model canvas](business-model-canvas.md). Do not claim the second level from the first, or the third from the second.

## Reading the result

- **Every rank-3 job, pain, and gain has an evidenced link.** Problem-solution fit holds; move to a real test of demand before claiming product-market fit.
- **A rank-3 item has no linked value map row.** The roadmap is about to ship something the segment cares about less than what it is ignoring. Reprioritize the value map before the roadmap, not after.
- **A value map item links to nothing in Part 1.** A feature in search of a job. Cut it or find the job; do not keep it because it already shipped.
- **Most links read "on paper."** Normal this early. The canvas has stated the hypothesis, not proved it. Take the rank-3 rows into the next round of interviews.

## ILLUSTRATIVE example

Invented, Ledgerline's expense copilot, filers as the profiled segment.

Jobs: get reimbursed without a second submission (functional, rank 3); not be the report finance flags every month (social, rank 2). Pains: a rejected report means redoing the whole form from a receipt pile (rank 3); the policy document is long and out of date (rank 2). Gains: knowing before submit whether a line will be questioned (rank 3).

Value map: a pain reliever showing the policy line next to each category, so a mismatch is visible before submit, addressing pain 1 and gain 1; a gain creator, single-tap accept for lines with no flag, addressing job 1.

Fit test: job 1 (rank 3) links to the gain creator, evidenced by six pilot filers whose first-submission approval rose against their own prior reports. Pain 1 (rank 3) links to the pain reliever, evidenced the same way. Gain 1 also links to the pain reliever, but on paper only: no filer was asked whether seeing the policy line changed their confidence before submit, so that link stays marked on paper until the next interview round.

## The trap

Filling the value map first, then reverse-engineering a profile that fits it. The solution already exists, so pains and gains get written in its vocabulary, "no real-time policy check" as a pain, before anyone confirmed a filer thinks in those terms, and the fit test passes because both halves were written by the same person on the same afternoon. The tell: a Part 1 item whose wording matches a Part 2 feature name almost exactly. Profile the customer from interview transcripts, in their words, before opening the value map; if the two halves sound like the same author, they are.

## Feeds

- [Business model canvas](business-model-canvas.md): the value propositions and customer segments blocks, sharpened before its check B
- [Lean canvas](lean-canvas.md): the problem and unique value proposition boxes
- [Positioning canvas](positioning-canvas.md): Part 3 (value) draws on the evidenced relievers and creators here
- [Personas](../../templates/discovery/personas.md): pains and workarounds, and goals and success
- [Assumptions register](../../templates/definition/assumptions-register.md): every link marked "on paper," confidence low
- DISCOVER, ahead of Gate 1
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
