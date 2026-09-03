---
layer: frameworks
stage: PLANNING
gate: 6
feeds: ["templates/planning/north-star-metric.md", "templates/planning/okrs.md", "templates/operate/metrics-review.md"]
method: "knowledge/north-star-metric.md"
aliases: ["North Star Input Tree", "north-star-input-tree"]
---
# North Star Input Tree

Based on the ideas of Sean Ellis and the growth community, codified in Amplitude's North Star Playbook by John Cutler and colleagues (2019). Explained here in this repository's own words.

## What it is for

The [north star card](../../knowledge/north-star-metric.md) argues for one metric that expresses delivered customer value, fed by a few inputs teams can move. This worksheet is where that choice is made on paper and tested. It answers two questions: which single number would fall if customers quietly stopped benefiting, and which three to five dials, each owned by one person, provably feed it. The tree is a set of causal claims. Writing them down is what lets a later metrics review grade them instead of admiring them.

## Run it when

- Before an OKR cycle, so every key result ladders to one definition of value
- When a PRD names a success metric and nobody can say which input it feeds
- After a metrics review where the inputs moved and the north star did not
- When two teams are optimizing numbers that fight each other (sign-ups against activation quality)

**Skip it when:** nothing is instrumented. A tree drawn before a single event is logged is a slogan with boxes around it; write the analytics instrumentation spec first, then name the metric it makes measurable.

## Inputs you need first

- The value the product claims to create, from `templates/planning/vision.md` and `templates/planning/product-strategy.md`
- The event taxonomy in the [analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), section 2, so "computable today" is a fact, not a hope
- The latest [metrics review](../../templates/operate/metrics-review.md), for baselines and data confidence
- The OKR sheet in flight, so the tree does not contradict it

## The worksheet

### Step 1: score the candidate north stars

Scale per check: 0 fails, 1 partly, 2 clearly. A candidate under 8 of 10 does not become the north star.

| Candidate (unit, period) | Value, not volume: a customer got what they came for | Falls within a quarter if value stops | One team cannot game it alone | Leads revenue rather than being revenue | Computable today from a named source | Total of 10 |
|---|---|---|---|---|---|---|
| [metric] | | | | | | |

### Step 2: the inputs

Three to five rows. The causal claim must read "when this rises, the north star rises because [mechanism]". Lead means the input moves weeks before the north star; lag means it confirms afterwards.

| Input (unit, period) | Causal claim | Lead or lag | Owner (one name) | Current (date) | Moves within a quarter? | Source |
|---|---|---|---|---|---|---|
| | | | | | yes / no | |

Rules: exactly one owner per row ("growth" is nobody on a Tuesday); at least three rows answer yes to moving within a quarter; at most one lag row.

### Step 3: sanity checks

| Check | Pass condition | Result |
|---|---|---|
| Value not vanity | The north star scored 2 on "falls within a quarter" | pass / fail |
| Moves within a quarter | Three or more inputs answered yes | |
| No single metric hides a leak | For every input, the way it could rise while customers get less is written down, with the guardrail that would catch it | |
| Coverage | Breadth (how many), frequency (how often), depth (how much), efficiency (how easily) each appear in an input, or the omission is explained | |
| Not arithmetic | Nobody has claimed the inputs sum to the north star; the tree is causal | |

### Step 4: guardrails

| Input it guards | Guardrail metric | Floor or ceiling | Who halts work |
|---|---|---|---|
| | | | |

## Reading the result

A candidate at 10 with passing inputs goes straight into the north star sheet. A best candidate at 8 or 9 is adopted with the failing check named as a known weakness and a fix date; the usual weakness is instrumentation. Under 8, the most common repair is the unit: "reports created" fails value-not-volume, "reports approved first time" passes. An input that cannot move within a quarter is a lag metric; keep at most one, and it never becomes a key result. An input for which nobody can name a leak is a vanity metric in disguise; find the leak or drop the row.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, which drafts a report from receipts, checks policy, and routes it for approval.

Candidates: "reports submitted per week" scored 6 (a report bounced back for rework still counts, so it fails value-not-volume). "Reports approved on first submission per week" scored 9, losing a point on computability because approval events live in the finance system and the join to copilot-drafted reports is a two-week instrumentation task, dated and owned.

| Input | Causal claim | Lead or lag | Owner | Current | Moves in a quarter? |
|---|---|---|---|---|---|
| Share of reports started in the copilot | More drafts go through policy checks before a manager sees them | lead | onboarding PM | 41% | yes |
| Receipt-to-line match rate at draft time | Fewer unmatched lines means fewer manager edits and bounces | lead | ML lead | 83% | yes |
| Policy pre-check pass rate before submission | Violations caught before submission never become rejections | lead | policy PM | 76% | yes |
| Median manager approval time (hours) | Reports approved inside the week count in the week | lead | workflow PM | 31 | yes |
| Employees submitting per month | Breadth: more of the company is on the tree at all | lag | customer success lead | 2,900 | no |

Leak named for row 3: the pass rate could rise because policy rules were loosened. Guardrail: post-approval corrections by accounts payable, ceiling 3%, halt called by the finance controller. Sanity checks: all pass once the instrumentation task lands.

## The trap

The org-chart tree. Each department gets one input so nobody feels left out, the causal claim column fills with "contributes to", and the sheet looks complete. Test it: could you predict next month's north star from this month's inputs, even roughly? If not, you have a dashboard with a hierarchy drawn on it, not a tree, and the metrics review will grade five claims that were never claims. Cut the inputs until each one has a mechanism a skeptic could argue with.

## Feeds

- [North star sheet](../../templates/planning/north-star-metric.md), sections 1 to 3, which carries the adopted metric, inputs, and guardrails
- [OKRs](../../templates/planning/okrs.md): every key result traces to an input row
- [Metrics review](../../templates/operate/metrics-review.md), section 2, where the causal claims are graded
- [Analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md), section 1, for any input marked not computable
- [Metrics dictionary](../../templates/operate/metrics-dictionary.md), one row per input, driven by the [metrics-tree skill](../../skills/metrics-tree/SKILL.md)
- PLANNING track; the tree is on trial at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Worked fill: [examples/ledgerline-north-star-tree.md](../../examples/ledgerline-north-star-tree.md)
- Method background: [north star metric](../../knowledge/north-star-metric.md)
