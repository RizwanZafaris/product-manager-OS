---
name: metrics-tree
description: Build the chain from a north star metric to its input metrics, to one definition per metric, to a dashboard specification someone can read in a minute. Use when a product has no agreed north star or the one it has fails the vanity test, when two teams report the same metric with different numbers, before OKRs or an instrumentation spec are written, or when a dashboard has decayed into a wall of tiles. Takes the value statement, what is instrumented, the analytics platform, and the audiences; returns the north star sheet, the input tree, the metrics dictionary rows, and the dashboard spec.
---

# Metrics Tree: from north star to a dashboard someone can read

Metrics fail as a slogan and a wall. The north star is named before anything measures it, the inputs have no owners and no causal claim, every team computes "active" its own way, and the dashboard has forty tiles that answer no question anyone asked. This skill builds the tree from the top, defines each metric once, and specifies a dashboard around the questions its audience actually brings.

## Files this skill drives

- [../../templates/planning/north-star-metric.md](../../templates/planning/north-star-metric.md), the metric, the input tree, the guardrails, the cadence
- [../../templates/operate/metrics-dictionary.md](../../templates/operate/metrics-dictionary.md), one row per metric
- [../../templates/operate/dashboard-spec.md](../../templates/operate/dashboard-spec.md), one per audience
- Worksheets: [../../frameworks/metrics/north-star-input-tree.md](../../frameworks/metrics/north-star-input-tree.md), [../../frameworks/metrics/aarrr-funnel.md](../../frameworks/metrics/aarrr-funnel.md) (McClure, 2007), [../../frameworks/metrics/heart-metrics.md](../../frameworks/metrics/heart-metrics.md) (Rodden, Hutchinson, and Fu at Google, 2010)
- [../../templates/delivery/analytics-instrumentation-spec.md](../../templates/delivery/analytics-instrumentation-spec.md), where every formula's events come from
- [../../templates/planning/okrs.md](../../templates/planning/okrs.md) and [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md), which trace to the tree and read from it
- Method background: [../../knowledge/north-star-metric.md](../../knowledge/north-star-metric.md), the HEART and AARRR entries in [../../knowledge/INDEX.md](../../knowledge/INDEX.md)
- [../../agents/analyst-agent.md](../../agents/analyst-agent.md) runs this method under its own rules in an agent runtime

## When to use

- No agreed north star, or the current one only ever goes up
- Two teams quote the same metric with different numbers
- Before OKRs are set, so key results ladder to one definition of value
- Before the instrumentation spec is written, so events serve metrics instead of the other way round
- Before a dashboard is built, or when the existing one has decayed
- After a Gate 6 where the inputs moved and the north star did not

## Inputs

The value the product delivers and to whom, from the vision or strategy document. The product's stage. What is instrumented today: the instrumentation spec or the warehouse tables. The analytics platform. The metrics people already quote, with where each number comes from. The dashboard audiences and the decisions each one makes.

Ask one question before anything else: if every customer silently stopped benefiting tomorrow, which number would fall within the quarter. Ask for current values from the source system, never from memory. If nothing is instrumented, the knowledge card's rule applies: do not name the north star yet, write the instrumentation spec inputs first, and come back.

## Workflow

### 1. Choose the north star and write its vanity test

Candidates come from delivered value, not revenue; revenue is a lagging result of value delivered earlier. Five tests, all in writing: it falls within a quarter if value stops; it leads rather than lags; a team can move it within a quarter; no single team can game it alone; a named source system computes it. Decision rule: a candidate that fails any test is replaced, and "not yet instrumented" fails the last one.

### 2. Build the input tree

Three to five inputs, each a dial one team can move, with the causal claim to the north star written down, one owner by name, a lead or lag classification, and a current value with its source and date. Use the AARRR funnel to locate where customers leak between acquisition, activation, retention, referral, and revenue; the leaking stage usually holds the input with the most headroom. Use HEART to choose the experience-level inputs: for happiness, engagement, adoption, retention, and task success, write the goal, then the signal, then the metric. Three sanity checks from the worksheet: value not vanity, moves within a quarter, and no single metric hides a leak, meaning the tree covers acquisition through retention. Decision rule: an input with no stated mechanism is dropped; an input owned by two teams is split or reassigned.

### 3. Set the guardrails

The metrics allowed to veto a north star win: quality, trust, cost to serve, support load. Each with a floor or ceiling, a named halt-caller, and the bad win it prevents. Floors come from the current value in the source system and the owner's stated tolerance, never from a round number.

### 4. Define every metric once

One dictionary row per metric: id, name, definition in words, formula, unit, period, the numerator and denominator events from the instrumentation spec, source system, owner, refresh, known gaps, and the segment cuts allowed. Decision rule: when two teams compute the same name differently, one definition wins and the other metric is renamed; a metric whose formula cannot be written from named events is not a metric yet, it is a request to the instrumentation spec.

### 5. Specify the dashboard

Per audience: the three to five questions it answers, the tiles with their dictionary ids and cuts, the drill path from north star to input to segment to event, the alerts with thresholds taken from the guardrails and who is paged, the refresh, the owner. Decision rule: a tile that answers none of the listed questions is cut; one dashboard per audience, never one per stakeholder.

### 6. Wire the tree into the loop

Every key result and every PRD success metric traces to a tree node, or the mismatch is logged on the north star sheet. Targets come from the OKR sheet; where none exists the cell reads [OPEN: owner] rather than a plausible number. Schedule the review cadence with a named runner, and point the metrics review at the tree.

## Output format

1. North star block: metric with unit and period, the value it expresses, the vanity test in writing, source system, current value with date
2. Input tree: | Input | Causal claim | Lead / lag | Owner | Current (source, date) | Target (OKR sheet, or [OPEN: owner]) |
3. Guardrails: | Metric | Floor or ceiling | Halt-caller | Bad win prevented |
4. Dictionary rows, one per metric named above
5. Dashboard spec per audience: the questions, then | Tile | Metric id | Cut | Drill path | Alert |, owner, refresh
6. Trace table: | KR or PRD metric | Tree node, or "mismatch, logged" |

## Failure modes this skill guards against

- A north star that only ever goes up
- Revenue named as the north star, so the tree steers by the rearview mirror
- Inputs with no owner or no causal claim, metrics that happened to be on a dashboard
- Definitions that differ by team, so every review starts with an argument about the number
- Numbers quoted from memory instead of from the source system
- A tree with no retention node, so growth hides churn
- Targets invented to fill a cell
- A dashboard built from every metric anyone asked for
- Instrumentation specified after build, so launch week reports nothing

## Exit gate

The tree feeds the PLANNING track in [../../os/OPERATING-LOOP.md](../../os/OPERATING-LOOP.md) and is what Gate 6 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) reads. Do not report it done until the north star sheet's exit gate passes, every dashboard tile carries a dictionary id, and every number in the output has a source system and a date.
