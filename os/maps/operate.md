---
layer: os
stage: OPERATE
gate: 6
feeds: ["os/maps/discover.md", "skills/conductor/questions/operate.md"]
method: ""
aliases: ["OPERATE"]
---
# OPERATE: map of content

Stage 6 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Run it, measure it, and let the numbers decide what happens next. The stage ends at Gate 6 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 6: outcomes verified | OPERATE, then loops to DISCOVER | The Gate 1 signal measured with its source system stated, the input metrics read beside the headline, and one of persist, pivot, or sunset with its consequence scheduled. |

## Templates this stage owns

| Template | What it is for |
|---|---|
| [operational-readiness-review.md](../../templates/operate/operational-readiness-review.md) | Runbooks, on-call, backup and recovery, blast radius |
| [metrics-review.md](../../templates/operate/metrics-review.md) | Outcome against target per key result, input movement, the decision |
| [metrics-dictionary.md](../../templates/operate/metrics-dictionary.md) | One row per reported metric: definition, formula, source, owner, refresh |
| [dashboard-spec.md](../../templates/operate/dashboard-spec.md) | Audience, the questions it answers, tiles, drill paths, alerting |
| [post-launch-review.md](../../templates/operate/post-launch-review.md) | Goal against actual, once per launch |
| [experiment-brief.md](../../templates/operate/experiment-brief.md) | Hypothesis, primary metric, variants, exposure, the decision rule |
| [incident-postmortem.md](../../templates/operate/incident-postmortem.md) | Blameless timeline, quantified impact, causes in systems language |
| [feedback-program.md](../../templates/operate/feedback-program.md) | A standing program tied to a decision, with exit criteria |
| [win-loss-review.md](../../templates/operate/win-loss-review.md) | Why it was won or lost, in the buyer's words |
| [qbr-board-update.md](../../templates/operate/qbr-board-update.md) | Metrics against goal, risks and asks, the decisions needed |
| [compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md) | Applicable rules, data categories, retention, the sign-off |
| [sunset-eol-plan.md](../../templates/operate/sunset-eol-plan.md) | The Gate 6 sunset outcome with dates, migration path, and an owner |
| [growth-plan.md](../../templates/planning/growth-plan.md) | The input-metric bet, the cheapest test of it, the counter-metric, the kill condition |
| [okrs.md](../../templates/planning/okrs.md) | Owned on the planning cadence, scored number against number here |

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [north-star-input-tree.md](../../frameworks/metrics/north-star-input-tree.md) | Break one value metric into inputs a team can move, with owners | Sean Ellis's north star framing, laid out in Amplitude's playbook (2019) |
| [aarrr-funnel.md](../../frameworks/metrics/aarrr-funnel.md) | Define each stage by its event and find where the funnel leaks | Dave McClure's startup metrics talk (2007) |
| [heart-metrics.md](../../frameworks/metrics/heart-metrics.md) | Pick UX metrics through goals and signals, not through what is easy to log | Rodden, Hutchinson, and Fu at Google (2010) |
| [growth-loops.md](../../frameworks/metrics/growth-loops.md) | Draw the loop where output becomes the next input, and do its arithmetic | Brian Balfour and Casey Winters at Reforge, from 2018 onward |
| [cohort-retention.md](../../frameworks/metrics/cohort-retention.md) | Read whether the curve flattens, and avoid the standard misreads | Cohort reading in the lean tradition, after Eric Ries (2011) |
| [unit-economics.md](../../frameworks/metrics/unit-economics.md) | Work margin, acquisition cost, lifetime value, and payback honestly | The SaaS treatment popularized by David Skok (2013) |
| [dora-four-keys.md](../../frameworks/metrics/dora-four-keys.md) | Read delivery health beside the product numbers | Nicole Forsgren, Jez Humble, and Gene Kim, Accelerate (2018) |
| [five-whys-fishbone.md](../../frameworks/execution/five-whys-fishbone.md) | Get from an incident symptom to a cause somebody can change | Taiichi Ohno's practice at Toyota, with Kaoru Ishikawa's cause diagram (1960s) |
| [causal-loop-diagram.md](../../frameworks/systems/causal-loop-diagram.md) | Explain a flat number structurally and locate the constraint | Jay Forrester's system dynamics (1961); the loop notation spread through Senge (1990) |
| [product-operating-model-assessment.md](../../frameworks/assessment/product-operating-model-assessment.md) | Score whether the organization can execute the plan it wrote | Marty Cagan and colleagues, Transformed (2024) |
| [leverage-points.md](../../frameworks/systems/leverage-points.md) | Place each intervention on the rung it acts at, after a delivered quarter moved nothing | Donella Meadows, Leverage Points (1999) |
| [space-framework.md](../../frameworks/metrics/space-framework.md) | Build a productivity slate across five dimensions instead of quoting one number | Forsgren, Storey, and colleagues in ACM Queue (2021) |
| [westrum-culture-typology.md](../../frameworks/assessment/westrum-culture-typology.md) | Score how bad news travels, before you trust a review or a status colour | Ron Westrum in Quality and Safety in Health Care (2004) |

Knowledge behind the methods: [north-star-metric.md](../../knowledge/north-star-metric.md), [okrs.md](../../knowledge/okrs.md), [high-output-management.md](../../knowledge/high-output-management.md). The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [product-analyst](../../skills/product-analyst/SKILL.md) | Gate 6 needs metric evidence a reader can trace to a source |
| [metrics-tree](../../skills/metrics-tree/SKILL.md) | There is no agreed north star, or the tree has no metric definitions under it |
| [experiment-designer](../../skills/experiment-designer/SKILL.md) | A growth bet needs a hypothesis, guardrails, and a stop rule |
| [postmortem-facilitator](../../skills/postmortem-facilitator/SKILL.md) | An incident needs a blameless review with corrective actions that get verified |
| [feedback-synthesis](../../skills/feedback-synthesis/SKILL.md) | Post-launch feedback has to become weighted themes for the next pass |
| [okr-critic](../../skills/okr-critic/SKILL.md) | Key results read as tasks and cannot be scored |
| [stakeholder-update](../../skills/stakeholder-update/SKILL.md) | The QBR or board read needs the decisions on the first page |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [analyst-agent](../../agents/analyst-agent.md) |
| Supporting | [growth-agent](../../agents/growth-agent.md), [research-agent](../../agents/research-agent.md) for the why behind a number, [drafting-agent](../../agents/drafting-agent.md), [validation-agent](../../agents/validation-agent.md) |
| Humans who sign Gate 6 | Product owner and sponsor |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry is a signed Gate 5, live in production, with the instrumentation emitting. Exit is the loop closing: persist, pivot, or sunset, each of which returns to [discover.md](discover.md) with what was learned. The interview path through the same stage is [skills/conductor/questions/operate.md](../../skills/conductor/questions/operate.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/deliver.md]] · [[os/maps/discover.md]] · [[os/maps/README.md]]
- Templates: [[templates/operate/operational-readiness-review.md]] · [[templates/operate/metrics-review.md]] · [[templates/operate/metrics-dictionary.md]] · [[templates/operate/dashboard-spec.md]] · [[templates/operate/post-launch-review.md]] · [[templates/operate/experiment-brief.md]] · [[templates/operate/incident-postmortem.md]] · [[templates/operate/feedback-program.md]] · [[templates/operate/win-loss-review.md]] · [[templates/operate/qbr-board-update.md]] · [[templates/operate/compliance-impact-assessment.md]] · [[templates/operate/sunset-eol-plan.md]] · [[templates/planning/growth-plan.md]] · [[templates/planning/okrs.md]]
- Frameworks: [[frameworks/metrics/north-star-input-tree.md]] · [[frameworks/metrics/aarrr-funnel.md]] · [[frameworks/metrics/heart-metrics.md]] · [[frameworks/metrics/growth-loops.md]] · [[frameworks/metrics/cohort-retention.md]] · [[frameworks/metrics/unit-economics.md]] · [[frameworks/metrics/dora-four-keys.md]] · [[frameworks/execution/five-whys-fishbone.md]] · [[frameworks/systems/causal-loop-diagram.md]] · [[frameworks/assessment/product-operating-model-assessment.md]] · [[frameworks/systems/leverage-points.md]] · [[frameworks/metrics/space-framework.md]] · [[frameworks/assessment/westrum-culture-typology.md]]
- Knowledge: [[knowledge/north-star-metric.md]] · [[knowledge/okrs.md]] · [[knowledge/high-output-management.md]] · [[knowledge/README.md]]
- Skills: [[skills/product-analyst/SKILL.md]] · [[skills/metrics-tree/SKILL.md]] · [[skills/experiment-designer/SKILL.md]] · [[skills/postmortem-facilitator/SKILL.md]] · [[skills/feedback-synthesis/SKILL.md]] · [[skills/okr-critic/SKILL.md]] · [[skills/stakeholder-update/SKILL.md]] · [[skills/conductor/questions/operate.md]]
- Agents: [[agents/TEAM.md]] · [[agents/analyst-agent.md]] · [[agents/growth-agent.md]] · [[agents/research-agent.md]] · [[agents/drafting-agent.md]] · [[agents/validation-agent.md]]
