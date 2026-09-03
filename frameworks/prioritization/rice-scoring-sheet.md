---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/roadmap.md", "templates/execution/decision-log.md", "templates/execution/dependency-register.md"]
method: "knowledge/rice-prioritization.md"
aliases: ["RICE scoring sheet", "rice-scoring-sheet"]
---
# RICE scoring sheet

Based on the ideas of Sean McBride, from the Intercom blog post introducing RICE (2016); the ICE section follows Sean Ellis's growth practice (2017). Explained here in this repository's own words.

## What it is for

A backlog with more candidates than capacity needs an order, and the order needs a reason that survives the sponsor of the item that lost. RICE makes each item's supporters write down four beliefs (reach, impact, confidence, effort) and turns them into one comparable number. The number is the receipt; the product is the argument you had to have to produce it, which shows which items rest on measurement and which on adrenaline. The [roadmap builder](../../skills/roadmap-builder/SKILL.md) fills this form at its scoring step; the [knowledge card](../../knowledge/rice-prioritization.md) covers why the method exists and how it lies.

## Run it when

- More than five comparable candidates compete for capacity that fits fewer, and the ordering debate has gone around twice.
- Two sponsors call their items equally urgent and neither has said what "urgent" moves.
- You need to say no in writing, with the inputs visible, so the no holds after you leave the room.

**Skip it when:** the list is short and the first two items are obvious; scoring then spends a week confirming what everyone knew, and the losers learn to distrust the sheet rather than the ranking.

## Inputs you need first

- The metric this period is judged on, from the [OKR sheet](../../templates/planning/okrs.md); impact is scored against it, not general goodness.
- A normalized backlog: one row per item, with type, requesting stakeholder, and the outcome it claims.
- A reach source: a count per period from the [metrics review](../../templates/operate/metrics-review.md) or an [evidence note](../../templates/discovery/evidence-note.md), never a share of an imagined market.
- Effort in person-months from the people who would do the work, including compliance, migration, and operational readiness.
- Hard external dates, from contracts or the [dependency register](../../templates/execution/dependency-register.md), for the mandate lane.

## The worksheet

**Step 1: declare the reach unit.** One unit for the whole sheet; filers and reports are not comparable, because one filer files many reports.

| Reach unit and period | Metric impact is scored against | Scored by, on |
|---|---|---|
| [reports per quarter] | [KR reference] | [role], [YYYY-MM-DD] |

**Step 2: the scales.** Impact, per person reached, against that metric: 3 massive (moves it on its own), 2 high, 1 medium, 0.5 low, 0.25 minimal; coarse on purpose, because a finer scale claims precision the inputs lack. Effort is whole person-months across every discipline, minimum 0.5; score a range at its top.

| Confidence | Rule |
|---|---|
| 100 percent | Data: measured on this product, this user base, this period, or in a shipped experiment |
| 80 percent | Analogy: measured somewhere comparable, with a written reason it transfers |
| 50 percent | Opinion: believed, not measured |
| Below 50 | Do not score; open a discovery task |

**Step 3: score.** RICE = (Reach x Impact x Confidence) / Effort, confidence as a decimal. The arithmetic column is not optional.

| Item | Reach | Impact | Confidence | Effort (pm) | Arithmetic | RICE | Evidence |
|---|---|---|---|---|---|---|---|
| [item] | [count] | [3 to 0.25] | [1.0 / 0.8 / 0.5] | [pm] | [R x I x C / E] | [result] | [source, date] |

**Step 4: the mandate lane, outside the ranking.** Compliance items, contract commitments, and scheme rules are never scored. They take capacity first, pinned to the quarter their date demands; the ranked list fills what remains, up to 80 percent of stated capacity.

| Mandate | Source and hard date | Cost of missing it | Effort (pm) | Quarter pinned |
|---|---|---|---|---|
| [item] | [contract clause, YYYY-MM-DD] | [what happens] | [pm] | [Qn] |

**ICE, for fast triage.** ICE = Impact x Confidence x Ease, each 1 to 10, ease being the inverse of effort. Sort raw intake with it in an hour, drop the bottom, and graduate anything that will take a build slot to RICE; never mix the two scores in one ranking.

| Item | Impact | Confidence | Ease | ICE | Keep for RICE? |
|---|---|---|---|---|---|
| [item] | [1 to 10] | [1 to 10] | [1 to 10] | [I x C x E] | [yes / no, why] |

## Reading the result

Scores are buckets, not ranks. Two scores within about 20 percent of each other are a tie, because the inputs carry wider error than the gap; settle ties by judgment in the open and log them in the [decision log](../../templates/execution/decision-log.md) with the options that lost. A row at 50 percent confidence gets a discovery task, not a build slot, however high it scores. The ranked list fills capacity only after the mandate lane has taken its share. Walk each sponsor through their row before publishing; new evidence changes a score, seniority does not.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot, one quarter, every number invented. Reach unit: expense reports per quarter, against the KR "first-submission approval rate".

| Item | Reach | I | C | E | Arithmetic | RICE |
|---|---|---|---|---|---|---|
| Receipt auto-extraction | 6,000 | 2 | 0.8 | 4 | 6,000 x 2 x 0.8 / 4 | 2,400 |
| Reviewer bulk approve | 4,000 | 0.5 | 1.0 | 1 | 4,000 x 0.5 x 1.0 / 1 | 2,000 |
| Policy category suggestion | 6,000 | 1 | 0.5 | 2 | 6,000 x 1 x 0.5 / 2 | 1,500 |

The first two rows tie by the bucket rule; extraction goes first because bulk approve needs drafted reports to exist, and the log says so. The third row is opinion-level, so it gets a two-week discovery task on category mismatch instead of a slot. Mandate lane: the enterprise contract's data-residency clause (receipt images in-region by a fixed date, 1 pm) is pinned to the quarter and never enters the ranking.

## The trap

Reach unit drift. Halfway through the sheet someone scores their item in filers, because that is the number they have, while the next item is scored in reports. A filer files around ten reports a quarter, so the reports item wins tenfold, and the ranking is decided by a bookkeeping accident. The quieter drift: a mandate wanders into the ranked table "so we can see it against the others," scores low against the KR, and a revenue feature beats a contract deadline on paper. Steps 1 and 4 exist for these two failures; a sheet that skips either has produced numbers, not a decision.

## Feeds

- [Roadmap](../../templates/planning/roadmap.md): the ranked list fills Now and Next; mandates carry their date
- [Decision log](../../templates/execution/decision-log.md): every tie-break, with the options that lost
- [Dependency register](../../templates/execution/dependency-register.md): pinned mandates and reordering dependencies
- The PLANNING track of the [operating loop](../../os/OPERATING-LOOP.md), via the [roadmap builder](../../skills/roadmap-builder/SKILL.md)
- Then sequence with [WSJF](wsjf-cost-of-delay.md); scope a fixed date with [MoSCoW](moscow.md)
- A filled copy: [Ledgerline RICE scoring](../../examples/ledgerline-rice-scoring.md)
- Method background: [RICE prioritization](../../knowledge/rice-prioritization.md); ICE in the [knowledge index](../../knowledge/INDEX.md)
