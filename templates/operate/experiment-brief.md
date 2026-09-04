---
layer: templates
stage: OPERATE
gate: 6
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Experiment Brief", "experiment-brief"]
---
# Experiment Brief: [experiment short name]

**Stage:** OPERATE (this file feeds [Gate 6: outcomes verified, learn or sunset](../../os/STAGE-GATES.md))
**Knowledge:** [Knowledge index, Lean Startup entry](../../knowledge/INDEX.md)
**Skill:** [experiment-designer](../../skills/experiment-designer/SKILL.md)

<!-- One experiment, one page, decided before it runs. The underlying discipline is
     Eric Ries's validated learning, restated in this repository's own words: the
     unit of progress is what the experiment taught, not what it shipped, and an
     experiment only teaches if the decision rule was written while everyone was
     still ignorant of the result. A rule written after the data arrives is a
     rationalization with a timestamp.

     This brief pairs with the [growth plan](../planning/growth-plan.md), which
     picks the bet; this file specifies the test. Results land in the
     [metrics review](metrics-review.md). If the product contains a model, the AI
     overlay's eval spec still applies; this brief does not replace it. -->

**Owner:** [name] · **Status:** [drafted / running / decided] · **Last updated:** [YYYY-MM-DD]

## 1. Hypothesis

<!-- Falsifiable, with the mechanism stated. "We believe X will move Y because Z"
     forces the causal claim into daylight, where the retro can examine it. -->

- **We believe that** [the change]
- **will move** [the target metric]
- **because** [the mechanism, the reason a customer behaves differently]
- **Evidence this is worth testing:** [linked; the growth plan bet, a synthesis theme, a support pattern]

## 2. Target metric and guardrail

<!-- One primary metric. Two primary metrics means the result can always be
     read as a win, and it will be. Guardrails are the metrics you are not
     trying to move and would stop for, with a floor written as a number. -->


| Field | Answer |
|---|---|
| Target metric | [one metric, with unit and period] |
| Tree link | [the north star input it feeds, per the [north star sheet](../planning/north-star-metric.md)] |
| Baseline | [current value, dated] |
| Minimum detectable effect we care about | [the smallest lift that would justify shipping] |
| Guardrail metric and floor | [what must not degrade, and by how much before we stop] |

## 3. Variants

<!-- Describe what the user experiences, not what was built. A variant a
     reader cannot picture cannot be reasoned about later, and the person
     reading this in six months is deciding whether to rerun it. -->


| Variant | What the user experiences | Allocation |
|---|---|---|
| Control | [current behavior] | [share] |
| A | | [share] |
| *B (ILLUSTRATIVE)* | *checkout survey moved to post-receipt* | *25 percent* |

## 4. Sample size and duration

<!-- Sized before launch, because "we will run it until it looks done" is how
     peeking becomes policy. If nobody on the team can size the sample, that is a
     named dependency, not a section to skip. -->

| Field | Answer |
|---|---|
| Sample needed | [n per variant, and the arithmetic or tool behind it] |
| Expected duration | [period at current traffic; if it exceeds an honest ceiling, shrink the question] |
| Start / end dates | [YYYY-MM-DD to YYYY-MM-DD] |
| Unit of assignment | [user / account / session, and why] |

## 5. Decision rule

<!-- The section that makes this a brief instead of a diary. Three outcomes, each
     with a pre-committed action and the person who executes it. -->

| Outcome | Rule (written before launch) | Action | Owner |
|---|---|---|---|
| Ship | [target moved by at least [threshold] with guardrail intact] | | |
| Iterate | [directional signal but below threshold: what specifically changes next] | | |
| Kill | [no signal, or guardrail breached] | [and the learning is still written up] | |

**Decided on [YYYY-MM-DD]:** [result, decision taken, link to the metrics review entry]

## How this experiment fails

<!-- Every row here produces a result that will be quoted in a decision
     meeting and should not be. The common thread is that the rule was decided
     after the data arrived, which is the one thing an experiment exists to
     prevent. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| A variant, not a hypothesis | The brief names the change but not the behaviour it predicts | State the expected effect and its direction before launch |
| Peeking and stopping early | Checking daily and calling it the first time it looks significant | Fix the sample size and the analysis date in advance, and hold to them |
| Never powered | A detectable effect picked to suit the schedule, then "no effect" reported | Compute the minimum detectable effect from the baseline and the traffic first |
| No guardrails | The primary metric improves while something else quietly gets worse | Name guardrails with floors, and check them before declaring a result |
| No decision rule | "We will look at the numbers and discuss" | Write ship, kill and extend criteria before the first user sees a variant |
| The loser ships anyway | The variant underperformed and was merged regardless | Tie the ship decision to the rule written above, or record that it was overridden and by whom |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


This brief is fit to launch when:

- [ ] The hypothesis names a mechanism, not just a direction
- [ ] Exactly one target metric is named, tied to the north star tree, with a dated baseline
- [ ] A guardrail exists with a numeric floor and a stop behavior
- [ ] Sample size and duration were computed before launch, arithmetic shown
- [ ] All three decision outcomes have pre-committed rules, actions, and owners
- [ ] The kill outcome ends in a written learning, not a quiet burial

Signed: [name], [role], [YYYY-MM-DD]
