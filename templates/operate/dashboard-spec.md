---
layer: templates
stage: OPERATE
gate: 6
feeds: []
method: ""
aliases: ["Dashboard Spec", "dashboard-spec"]
---
# Dashboard Spec: [dashboard name]

Stage: OPERATE, feeds [Gate 6: outcomes verified](../../os/STAGE-GATES.md); specified in DESIGN so the dashboard exists on launch day
Knowledge: [HEART metrics worksheet](../../frameworks/metrics/heart-metrics.md)
Skill: [metrics-tree](../../skills/metrics-tree/SKILL.md); the [analyst agent](../../agents/analyst-agent.md) reads the result in the metrics review

> **Delete any section you do not need.** One dashboard per audience and per set of questions. A dashboard for everyone answers nothing, and the fix is a second spec, not a second page of tiles. Never leave a heading standing over white space.

<!-- The spec a builder can implement without asking: who looks at it, what
     questions it must answer, which metric id each tile shows, where each tile
     drills to, and what alerts. No metric is defined here. Every tile cites an id
     from the metrics dictionary, so the dashboard can never disagree with the
     review.

     Neighbours: the metrics dictionary (metrics-dictionary.md) defines every metric
     this spec cites; the instrumentation spec
     (../delivery/analytics-instrumentation-spec.md) owns the events; the metrics
     review (metrics-review.md) is the reading, not the screen; the observability
     template (../architecture/observability.md) owns system health dashboards.

     Fill first: the audience and questions in section 1, the tiles in section 3,
     and the alerts in section 5. -->

**Owner:** [name] · **Builder:** [name] · **Audience:** [one role group] · **Tool:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Built / Verified
**Dictionary version:** [date of the metrics-dictionary.md copy this spec cites]

## 1. Audience and questions

<!-- Every tile traces to a question row, and every question names the decision
     its answer changes. A tile that answers no question is decoration, and
     decoration is what people read when the real number is inconvenient. -->

| # | Audience (role) | Question they arrive with | Decision the answer changes | How often they look |
|---|---|---|---|---|
| Q1 | | | | |
| Q2 | | | | |

## 2. Layout

<!-- Top row: the north star and its guardrail, with target lines. Second row:
     the input metrics that explain the top row. Below: diagnostics and segments.
     A reader should get the headline in the first row and the reason in the
     second; nothing in the top row should surprise the metrics review. -->

- **Row 1:** [north star tile, guardrail tile]
- **Row 2:** [input metric tiles, in the order of the lineage table]
- **Row 3 and below:** [diagnostic tiles, segment views]
- **Filters available on every tile:** [date range, segment ids from the dictionary]

## 3. Tiles

<!-- One row per tile. Comparison is what turns a number into a signal: against a
     target, a prior period, or a segment. Targets are ILLUSTRATIVE until agreed
     and labeled so on the tile. The italic row is ILLUSTRATIVE. -->

| Tile | Question # | Metric id | Visual (number / trend / funnel / cohort table / distribution) | Grain and window | Comparison (target / prior period / segment) | Segments available | Owner |
|---|---|---|---|---|---|---|---|
| T-1 | | | | | | | |
| *T-3* | *Q2* | *M-004* | *trend, 12 weeks* | *weekly, trailing 12 weeks* | *target line at 80 percent (ILLUSTRATIVE) and prior 12 weeks* | *by client platform, by account size* | *[name]* |

## 4. Drill paths

<!-- Where a reader goes when a tile looks wrong. Every path ends in a view that
     exists and carries the filters the reader already set, or the drill is a
     restart. -->

| From tile | To (view or report) | What it explains | Filters carried |
|---|---|---|---|
| | | | |

## 5. Alerting

<!-- Thresholds are fields, agreed with the metric owner, never invented here. An
     alert with no first action is noise with a bell, and noise trains people to
     mute the channel the real alert will use. Suppression names the known gaps
     and data lags that would otherwise page someone about a pipeline. -->

| Metric id | Condition (threshold and direction) | Window | Who is told | Channel | First action (runbook or review) | Suppressed when |
|---|---|---|---|---|---|---|
| | [n or [n] percent, agreed with owner on [date]] | | | | | [data more than [n] hours behind; known gap G-[n]] |

## 6. Freshness and known gaps

<!-- The dictionary's refresh and gaps, shown on the tile, so a reader never has
     to ask whether the number is stale or partial. -->

| Tile | Source refresh and latency | Shown on the tile as | Known gaps annotated (dictionary gap ids) |
|---|---|---|---|
| | | [e.g. "as of [date, time]"] | |

## 7. Verification

<!-- Built becomes verified when each tile's value has been reproduced by hand
     from the dictionary formula on one day, and every difference is explained.
     Do this once at build and again after any dictionary change log entry. -->

| Tile | Dictionary value on [date] | Dashboard value | Match (yes / no) | Explanation if no |
|---|---|---|---|---|
| | | | | |

---

## Exit gate (feeds Gate 6: outcomes verified)

Done when every box is honestly ticked. The verified dashboard is the screen the [metrics review](metrics-review.md) reads for [Gate 6](../../os/STAGE-GATES.md); its tiles cite [metrics-dictionary.md](metrics-dictionary.md) and nothing else.

- [ ] Every tile cites a metric id from the dictionary, and no metric is defined here
- [ ] Every tile traces to a question, and every question names a decision
- [ ] The audience is one role group; a second audience got a second spec
- [ ] Every drill path ends in a view that exists and carries filters
- [ ] Every alert has a threshold agreed with the metric owner, a window, a channel, and a first action
- [ ] Freshness and known gaps show on the tiles that have them
- [ ] Every tile's value was reproduced from the dictionary formula once, with differences explained
- [ ] The ILLUSTRATIVE row has been deleted
- [ ] Signed by [name], [date]
