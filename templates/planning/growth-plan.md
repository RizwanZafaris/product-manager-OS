---
layer: templates
stage: OPERATE
gate: 6
feeds: []
method: "knowledge/north-star-metric.md"
aliases: ["Growth Plan", "growth-plan"]
---
# Growth Plan: [product name]

**Stage:** OPERATE (this file feeds [Gate 6: outcomes verified](../../os/STAGE-GATES.md))
**Knowledge:** [north star metric](../../knowledge/north-star-metric.md)
**Skill:** [growth agent](../../agents/growth-agent.md); [experiment-designer](../../skills/experiment-designer/SKILL.md) for each experiment it ranks

<!-- A growth plan is one bet at a time, made in public, with the evidence attached.
     The frame is the north star model as popularized by Sean Ellis and codified in
     Amplitude's playbook, restated in this repository's own words: one metric that
     expresses delivered value, fed by a small tree of input metrics teams can
     actually move. Growth work is choosing the input with the most headroom and
     running the cheapest experiment that could move it. The knowledge card linked
     above carries the fuller treatment and the vanity-metric trap.

     Two disciplines this file enforces. Every experiment names a counter-metric,
     because most growth mechanisms have a failure mode that looks like success for
     a while: activation pumped by lowering the bar, referrals pumped by nagging.
     And the kill condition is written before the experiment starts, because after
     it starts, everyone involved is invested in not seeing it. -->

**Owner:** [name] · **Period:** [quarter or cycle] · **Last updated:** [YYYY-MM-DD]
**Linked metrics review:** [filled copy of metrics-review.md](../operate/metrics-review.md) · **Linked OKR sheet:** [okrs.md copy for this product]

## 1. Where the metric tree stands

<!-- Numbers come from the metrics review, not re-derived here. If the two files
     disagree, the review wins and this table is corrected. -->

| Metric | Role | Current | Trend over [period] | Source system |
|---|---|---|---|---|
| | North star | | | |
| | Input | | | |
| | Input | | | |

## 2. The next growth bet

<!-- One bet. A plan with three simultaneous bets is a wish list wearing a plan's
     clothes, and when something moves, nobody knows which bet moved it. -->

- **Input metric chosen:** [one metric from the tree above]
- **Why this one:** [the headroom: how far below its plausible ceiling it sits, and what says so]
- **What the last metrics review said about it:** [one line, with the review date]

## 3. The loop or channel behind the metric

<!-- Name the mechanism that feeds the chosen metric and where it leaks. A metric
     with no mechanism behind it cannot be moved on purpose, only wished at. -->

- **Mechanism:** [the loop or channel: e.g. invited teammate activates, activated team invites the next]
- **Where it leaks today:** [the step where the numbers fall off, with the number]
- **Evidence:** [the funnel query, cohort table, or interview set that shows the leak, linked or filed]

## 4. The cheapest experiment

<!-- Cheapest that could plausibly move the metric, not the most impressive. State
     what the experiment is worth before anyone estimates what it takes; if the
     estimate exceeds the worth, shrink the experiment, not the honesty. -->

| Hypothesis (must be falsifiable) | Design | Cost (people-days + spend) | Duration | Success threshold | Owner |
|---|---|---|---|---|---|
| | | | | [number, agreed before start] | |

## 5. Counter-metric

| Metric | Damage it detects | Threshold that stops the experiment | Source system |
|---|---|---|---|
| | | | |

## 6. Kill condition

- **Ends at:** [the date or the threshold, whichever comes first]
- **Who decides:** [name]
- **Decision lands in:** [decision log](../execution/decision-log.md) entry, plus a ledger row below

## Experiment ledger

<!-- Append-only. A ledger with no failed rows is either a very young plan or an
     edited one, and edited ledgers teach nothing. -->

| # | Experiment | Dates | Result (number vs threshold) | Decision (scale / iterate / kill) | Logged at |
|---|---|---|---|---|---|
| | | | | | |

## Exit gate

This plan is fit to run when:

- [ ] The bet is a single input metric, and the tree linking it to the north star is written in section 1
- [ ] The mechanism behind the metric is named, with the leak located and evidenced
- [ ] The hypothesis can fail, with a numeric success threshold agreed before the experiment starts
- [ ] Cost and duration are stated, and the experiment is the cheapest that could plausibly move the metric
- [ ] A counter-metric is named with a stopping threshold and a source system
- [ ] The kill condition names a date or a threshold and a decider, before the start
- [ ] Every finished experiment has a ledger row and a decision-log entry, failures included

Signed: [name], [role], [YYYY-MM-DD]
