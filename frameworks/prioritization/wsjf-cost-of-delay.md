# WSJF and cost of delay

Based on the ideas of Donald Reinertsen, from The Principles of Product Development Flow (2009), in the form popularized by the Scaled Agile Framework. Explained here in this repository's own words.

## What it is for

One team, one queue, several items that will all be built eventually: the only question is order, and the wrong order has a price. Every week an item waits, its value leaks: revenue not earned, a deadline closer, a risk still open. WSJF (weighted shortest job first) puts a number on that leak, the cost of delay, and divides it by how long the item takes. Short, valuable items go first, because they stop leaking soonest and clear the queue for the rest. It answers "what first," not "what at all"; selection belongs to the [RICE sheet](rice-scoring-sheet.md).

## Run it when

- A ranked list has survived RICE and the team needs the order it will actually work in.
- Some items lose value with time (a seasonal window, a contract date, a competitor's launch) and others do not, and the debate ignores the difference.
- One large item is blocking three small ones and nobody will say so.

**Skip it when:** the question is whether to build an item at all. WSJF assumes everything on the sheet gets built and only orders it; run it on a wish list and the smallest wish always wins.

## Inputs you need first

- The short list that will be built, from the RICE sheet or the roadmap's Next table.
- Duration for each item in one unit (weeks of team time), from the people who would do the work.
- What each item is worth and to whom, from the [OKR sheet](../../templates/planning/okrs.md) and the [product strategy](../../templates/planning/product-strategy.md).
- Dates that make value decay: contract commitments, mandates, and the [dependency register](../../templates/execution/dependency-register.md).
- Risks an item retires, from the [risk register](../../templates/execution/risk-register.md).

## The worksheet

### Step 1: score cost of delay, one column at a time

Cost of delay has three components, each scored on the same relative scale: 1, 2, 3, 5, 8, 13, 20. The smallest item in a column gets a 1; every other item is scored relative to it. Score a whole column across every item before starting the next column. Scoring one item across all columns is how every sponsor gives their own item a 20 three times.

| Component | Question it answers |
|---|---|
| User or business value | How much does this move the period's metric or a customer's outcome, relative to the others? |
| Time criticality | How fast does the value decay? Is there a fixed date after which it is worth much less? Does waiting change what has to be built? |
| Risk reduction or opportunity enablement | What risk does this retire, or what future work does it unlock, that the others do not? |

### Step 2: divide by duration

CoD = value + time criticality + risk reduction. WSJF = CoD / duration. Duration is on the same relative scale, or in weeks of team time if every item has a real estimate; use one or the other for the whole sheet.

| # | Item | Value | Time criticality | Risk or enablement | CoD (sum) | Duration | Arithmetic | WSJF |
|---|---|---|---|---|---|---|---|---|
| 1 | [item] | [1 to 20] | [1 to 20] | [1 to 20] | [sum] | [1 to 20, or weeks] | [CoD / duration] | [result] |

### Step 3: the split test

For the item with the largest duration, write the thinnest slice that delivers most of its value and score the slice as its own row. A split often produces the highest WSJF on the sheet.

| Large item | Slice | Slice CoD | Slice duration | Slice WSJF |
|---|---|---|---|---|
| [item] | [what ships first] | | | |

### The relative-scale warning

The numbers mean nothing outside this sheet. A 13 here is not a 13 on another team's sheet, so never compare or add WSJF across teams or quarters. The scale also compresses extremes: an item fifty times more valuable than the smallest still scores 20. When you can put currency on cost of delay (revenue per week lost, penalty per week late), use money per week and real durations; the arithmetic is identical and the argument is shorter.

## Reading the result

Sequence by WSJF, highest first. Ties go to the shorter duration. A valuable item at the bottom of the list is usually a large one; split it before accepting the order. The ranking is a snapshot: re-score when a duration changes or a date moves, and record any reorder in the [decision log](../../templates/execution/decision-log.md) with the reason. If time criticality dominates every row, you are looking at a deadline calendar, not a queue; pin those items and run the sheet on the rest.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot team, one quarter's queue, every number invented. Duration in weeks of team time.

| # | Item | Value | Time | Risk | CoD | Duration | Arithmetic | WSJF |
|---|---|---|---|---|---|---|---|---|
| 1 | Receipt auto-extraction, all receipt types | 13 | 3 | 5 | 21 | 8 | 21 / 8 | 2.6 |
| 2 | Policy category suggestion (finance refreshes categories at fiscal year start) | 8 | 8 | 3 | 19 | 5 | 19 / 5 | 3.8 |
| 3 | Reviewer bulk approve | 5 | 2 | 1 | 8 | 2 | 8 / 2 | 4.0 |
| 4 | Extraction eval harness | 1 | 3 | 13 | 17 | 3 | 17 / 3 | 5.7 |

Order: 4, 3, 2, 1. The most valuable item goes last, which is the sheet doing its job: eight weeks of the quarter spent on it first would delay everything else. Split test: "extraction for printed receipts in one currency" has CoD 15 and duration 3, WSJF 5.0, and moves to second place. The eval harness leads because it retires the risk that all of row 1 is built on unmeasured accuracy.

## The trap

Scoring by item instead of by column. The sponsor of the extraction work scores value 20, time criticality 20, risk 20, because that is what a sponsor does; the next sponsor matches it; CoD becomes a count of who was in the room, and the only column left with any variance is duration, so the sheet quietly turns into "smallest first" with a decimal point. The second version is duration gaming: halve the estimate and the score doubles, which is why duration comes from the people doing the work and is written down before the value columns are scored.

## Feeds

- [Roadmap](../../templates/planning/roadmap.md): the order of the Now table and the entry order of Next
- [Dependency register](../../templates/execution/dependency-register.md): any item pulled forward by time criticality names its date there
- [Decision log](../../templates/execution/decision-log.md): the sequence decision and every reorder
- The sequencing step of the [roadmap builder](../../skills/roadmap-builder/SKILL.md), on the PLANNING track of the [operating loop](../../os/OPERATING-LOOP.md)
- Select before you sequence: [RICE scoring sheet](rice-scoring-sheet.md)
- Method background: the WSJF entry in the [knowledge index](../../knowledge/INDEX.md)
