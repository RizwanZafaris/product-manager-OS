---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["templates/planning/roadmap.md", "templates/planning/okrs.md", "templates/execution/dependency-register.md"]
method: "knowledge/shape-up.md"
aliases: ["Now, Next, Later roadmap", "now-next-later"]
---
# Now, Next, Later roadmap

Based on the ideas of Janna Bastow, from her roadmapping work at ProdPad (2012 onward). Explained here in this repository's own words.

## What it is for

A roadmap sorted by confidence instead of by date. Certainty decays with distance, so the precision of what you publish has to decay with it: Now is committed and dated, Next is shaped and likely, Later is a direction that may never ship. This answers the question a roadmap is actually asked, "what are you working on and how sure are you," without manufacturing dates that get quoted back as promises. It is the shape of the [roadmap template](../../templates/planning/roadmap.md); this sheet is the sorting step that decides which column each item has earned.

## Run it when

- A ranked list exists (from the [RICE sheet](rice-scoring-sheet.md) or [WSJF](wsjf-cost-of-delay.md)) and it needs a form that sales, support, and executives can read without turning it into a contract.
- A dated roadmap keeps being quoted back at you six months later.
- Priorities move faster than quarters and the published roadmap is always stale.

**Skip it when:** every item has a hard external date. A migration cutover or a regulatory program is a calendar with a critical path, and a confidence column adds nothing to it; use the [dependency register](../../templates/execution/dependency-register.md) and a dated plan.

## Inputs you need first

- The ranked backlog with its scores and confidence levels.
- The objective each item serves, from the [OKR sheet](../../templates/planning/okrs.md); an item that serves none is a pet project with a row.
- Dependency status per item, from the dependency register.
- Capacity for the Now horizon, at the 80 percent rule from the [roadmap builder](../../skills/roadmap-builder/SKILL.md).
- The current parked and killed list.

## The worksheet

### Step 1: the entry tests

| Column | What it means | Entry test (all must hold) | Precision allowed |
|---|---|---|---|
| Now | Committed, in flight or next up | Confidence at or above 70 percent; every dependency resolved or dated; capacity reserved within the 80 percent line; outcome named | Month or sprint |
| Next | Shaped, planned, not started | Problem evidenced (Gate 1 passed, or an [evidence note](../../templates/discovery/evidence-note.md)); solution shaped enough to size; confidence 50 to 70 percent | Quarter |
| Later | A direction, not a feature | Problem named, with evidence that it exists; a strategy bet it serves; no solution committed | None: theme and problem only |
| Parked or killed | Deliberately not doing | A written reason and a date | Not applicable |

Confidence is the RICE confidence adjusted for dependency state: an item at 80 percent with an unbuilt dependency is not at 80 percent.

### Step 2: sort

| Initiative | Column | Outcome it serves (objective ref) | Confidence | Evidence for the confidence | Dependency status | Precision written as | Promotion or demotion signal |
|---|---|---|---|---|---|---|---|
| [item] | [Now / Next / Later / Parked] | [O1 KR2] | [percent] | [data, analogy, or opinion; source] | [resolved / dated / open] | [month / quarter / none] | [what evidence moves it] |

### Step 3: the movement rules

| Move | Trigger | Who records it, where |
|---|---|---|
| Later to Next | The promotion signal in the row has been observed and a solution is shaped | Owner, in the roadmap change log |
| Next to Now | Sized, dependencies dated, confidence at or above 70 percent, capacity free | Owner, after the capacity check |
| Now to Next | A dependency slipped or confidence fell below 70 percent; say so before anyone notices | Owner, same week, with a note to whoever was counting on it |
| Anywhere to Parked or Killed | The evidence changed, or the strategy did | Owner, with the reason, in the parked and killed table |

Size rule: Now holds what fits within 80 percent of capacity for its horizon; Next holds about the same again; Later is unbounded, but every theme traces to a bet in the [product strategy](../../templates/planning/product-strategy.md).

### Mapping to the roadmap template

| This sheet | Roadmap template section |
|---|---|
| Now rows | Now table: initiative, outcome, target period, confidence, dependencies, status |
| Next rows | Next table, with the quarter and the shaping status |
| Later rows | Later table: theme, problem, earliest entry to Next, promotion signal |
| Parked and killed rows | Parked and killed table, with the reason |
| Every move | Change log |

## Reading the result

Count the rows per column. An empty Later means there is no strategy behind the roadmap, only a queue. A Now longer than capacity is a promise list, and the promises furthest down are already broken. A Next row with no evidence in its confidence column is a wish with a quarter attached. Then read Later aloud: if a salesperson could quote a feature name and a date from it, rewrite the row as a theme.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot, one planning cycle, every number invented.

| Initiative | Column | Outcome | Confidence | Evidence | Dependency | Signal |
|---|---|---|---|---|---|---|
| Receipt auto-extraction v1 | Now, next month | O1: first-submission approval up | 85 percent | Pilot data on 400 receipts | Storage upgrade, dated | |
| Filer review-before-submit screen | Now, next sprint | O1 | 90 percent | Shipped pattern elsewhere in the product | None | |
| Policy category suggestion | Next, following quarter | O1 | 60 percent | Opinion plus interview quotes; discovery task open | Policy export from finance, open | Discovery shows category mismatch is the top bounce cause |
| Reviewer bulk approve | Next | O2: reviewer hours down | 65 percent | Reviewer interviews | Drafted reports must exist | Extraction v1 in use on half of reports |
| Reviewers stop doing mechanical checks | Later | O2 | none written | Time logs from finance | | Bulk approve ships and reviewer hours move |
| Filing on behalf of another employee | Later | O3: assistants covered | none written | Three enterprise accounts asked | | Assistant workflow research done |
| Mileage from calendar entries | Parked | | | Low reach on the RICE sheet | | Revisit if travel volume doubles |

## The trap

A date leaks into Later. A salesperson asks when the assistant workflow ships, the PM writes "Q3" into the Later row to be helpful, the deal closes on it, and the roadmap has become a contract nobody signed. The only honest answers to "when" for a Later item are a theme with its promotion signal, or a real commitment: move it to Now, take the capacity, and date it. A date in Later is precision decaying in the wrong direction, and it is how a confidence roadmap turns back into the Gantt chart it replaced.

## Feeds

- [Roadmap](../../templates/planning/roadmap.md): the Now, Next, Later, and Parked and killed tables, section by section as mapped above
- [OKRs](../../templates/planning/okrs.md): every Now and Next row names an objective there
- [Dependency register](../../templates/execution/dependency-register.md): the dated dependencies that let an item enter Now
- The PLANNING track of the [operating loop](../../os/OPERATING-LOOP.md), through the sequencing step of the [roadmap builder](../../skills/roadmap-builder/SKILL.md)
- Method background: the roadmap template's preamble, and appetite over estimate in [Shape Up](../../knowledge/shape-up.md)
