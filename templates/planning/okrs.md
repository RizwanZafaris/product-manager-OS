---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: "knowledge/okrs.md"
aliases: ["OKR Sheet"]
---
# OKR Sheet: [product or team name], [period]

**Stage:** PLANNING track (feeds every stage of the [operating loop](../../os/OPERATING-LOOP.md))
**Knowledge:** [OKRs](../../knowledge/okrs.md)
**Skill:** [okr-critic](../../skills/okr-critic/SKILL.md); [roadmap-builder](../../skills/roadmap-builder/SKILL.md) for the quarter they sit in

<!-- The method here is Andy Grove's, as popularized by John Doerr in Measure What
     Matters, encoded in this repo's own words; the knowledge card linked above
     carries the fuller treatment and the classic trap.

     That trap, key results that are tasks, is the one this sheet is built to catch.
     The test for every KR: could you score it without asking the team what they did?
     "Ship the new onboarding flow" fails that test. "New users reaching first value
     within one day rises from 30% to 55%" passes. Shipping is an activity; a key
     result is a change in the world.

     Three to five key results per objective. Baseline is mandatory: a target without
     a baseline is a wish with a number on it. -->

**Owner:** [name] · **Period:** [quarter or cycle] · **Scoring cadence:** [e.g. check-in every 2 weeks, final score in the last week]
**Grading scale:** 0.0 to 1.0 at period end; around 0.7 on ambitious KRs is healthy, 1.0 across the board means the targets were sandbagged

## Objective 1: [qualitative, memorable, time-bound statement of what better looks like]

<!-- One sentence a team member could repeat without reading it. If it needs
     the key results underneath to be understood, it is not an objective yet. -->


| # | Key result (an outcome, not a task) | Baseline | Target | Current | Score | Owner |
|---|---|---|---|---|---|---|
| KR1 | | | | | | |
| KR2 | | | | | | |
| KR3 | | | | | | |
| *ex* | *weekly active teams using auto-extraction (ILLUSTRATIVE)* | *0* | *40* | *12* | *0.3* | *[name]* |

**Commitment type per KR:** [mark each as committed (1.0 expected) or aspirational (0.7 is success), because grading them the same punishes ambition]

## Objective 2: [statement]

<!-- Same bar. Delete this block if the period has one objective, which is
     usually the stronger choice. -->


| # | Key result | Baseline | Target | Current | Score | Owner |
|---|---|---|---|---|---|---|
| KR1 | | | | | | |
| KR2 | | | | | | |
| KR3 | | | | | | |

## Guardrails

<!-- What must not degrade while chasing the objectives. These are monitored, not scored. -->

| Guardrail metric | Floor or ceiling | Watched by |
|---|---|---|
| | | |

## Check-in log

<!-- The section that decides whether these were OKRs or decoration. A set
     looked at twice, at planning and at scoring, cannot change a decision in
     between, which was the only reason to write it. -->


| Date | KR movements since last check-in | Confidence change | Action taken |
|---|---|---|---|
| | | | |

## End-of-period scoring

<!-- Score against the baseline recorded at planning, not against what the
     number turned out to be. A target edited during the period is a target
     that scored itself. -->


- Scored on: [YYYY-MM-DD] · Scored by: [name, with the team present]
- KRs that scored below 0.3, and the one-line diagnosis for each: [list]
- What carries into next period, and what is dropped: [list]
- Feed the results into the [metrics review](../operate/metrics-review.md) for Gate 6

## How this OKR set fails

<!-- Each row produces a set that is scored at quarter end and taught the team
     nothing. The first is the most common by a wide margin. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Key results are tasks | "Ship the dashboard", "run the webinar", ticked at completion | A key result is an outcome with a number. A launch is how, not whether |
| The objective is a metric | "Increase revenue" as the objective, with the metric repeated beneath | The objective says what better looks like. The key results measure it |
| Sandbagged | Everything scores full marks and nothing changed | If every set scores full marks, the targets were forecasts, not stretches |
| Too many | Five objectives and a dozen key results nobody can recall | Few enough that the team can say them from memory, or they are not operating |
| No baseline | "Engagement up", with no starting number, argued about at scoring | Baseline and target are written at planning, dated, and not edited afterwards |

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


This sheet is fit to run the period on when:

- [ ] Every objective is qualitative and time-bound; every KR is quantitative
- [ ] Every KR passes the "score it without asking what the team did" test
- [ ] Every KR has a baseline, a target, and a named owner
- [ ] Each KR is marked committed or aspirational
- [ ] Guardrails are listed, so the objectives cannot be gamed silently
- [ ] The scoring cadence has calendar entries, not intentions

Signed: [name], [role], [YYYY-MM-DD]
