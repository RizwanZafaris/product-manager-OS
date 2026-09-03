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

| Field | Answer |
|---|---|
| Target metric | [one metric, with unit and period] |
| Tree link | [the north star input it feeds, per the [north star sheet](../planning/north-star-metric.md)] |
| Baseline | [current value, dated] |
| Minimum detectable effect we care about | [the smallest lift that would justify shipping] |
| Guardrail metric and floor | [what must not degrade, and by how much before we stop] |

## 3. Variants

| Variant | What the user experiences | Allocation |
|---|---|---|
| Control | [current behavior] | [share] |
| A | | [share] |
| *B* | *checkout survey moved to post-receipt* | *25 percent* |

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

## Exit gate

This brief is fit to launch when:

- [ ] The hypothesis names a mechanism, not just a direction
- [ ] Exactly one target metric is named, tied to the north star tree, with a dated baseline
- [ ] A guardrail exists with a numeric floor and a stop behavior
- [ ] Sample size and duration were computed before launch, arithmetic shown
- [ ] All three decision outcomes have pre-committed rules, actions, and owners
- [ ] The kill outcome ends in a written learning, not a quiet burial

Signed: [name], [role], [YYYY-MM-DD]
