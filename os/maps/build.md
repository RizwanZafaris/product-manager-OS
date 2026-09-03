---
layer: os
stage: BUILD
gate: 4
feeds: ["os/maps/deliver.md", "skills/conductor/questions/build.md"]
method: ""
aliases: ["BUILD"]
---
# BUILD: map of content

Stage 4 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Build to the spec, and keep the spec honest as reality pushes back. The stage ends at Gate 4 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 4: acceptance criteria met | BUILD | Every Gate 2 criterion demonstrated or listed as a miss with an owner and a decision, no undecided edge-case row, and failure scenarios exercised rather than described. |

## Templates this stage owns

| Template | What it is for |
|---|---|
| [testing-strategy.md](../../templates/delivery/testing-strategy.md) | Test levels, coverage targets, environments, entry and exit criteria |
| [edge-cases.md](../../templates/delivery/edge-cases.md) | Case, trigger, expected behavior, linked test; no row left undecided |
| [failure-scenarios.md](../../templates/delivery/failure-scenarios.md) | Blast radius, detection, recovery, and the data-loss risk |
| [analytics-instrumentation-spec.md](../../templates/delivery/analytics-instrumentation-spec.md) | Event taxonomy and owners, written before build so Gate 6 has a baseline |
| [acceptance-criteria.md](../../templates/definition/acceptance-criteria.md) | Owned at DEFINE, verified here case by case against the running product |
| [decision-log.md](../../templates/execution/decision-log.md) | Where a scope change goes instead of being absorbed silently |
| [change-request.md](../../templates/execution/change-request.md) | One change to a signed baseline, with the approvers named |
| [tech-debt-register.md](../../templates/execution/tech-debt-register.md) | What the shortcut costs per quarter and what removing it costs once |
| [status-report.md](../../templates/execution/status-report.md) | The weekly written record, where amber carries a date and red carries a decision |
| [retrospective.md](../../templates/execution/retrospective.md) | The previous cycle's actions checked first, then two or three new ones with owners |

The AI overlay runs the eval sets in [eval-spec.md](../../templates/ai/eval-spec.md) against the version that will ship, and the breaks from [red-team-review.md](../../templates/ai/red-team-review.md) earn permanent eval rows.

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [estimation-sheet.md](../../frameworks/execution/estimation-sheet.md) | Re-forecast in ranges when the first sizing meets the code | PERT's three-point form (1958), with Cohn and Flyvbjerg on the human bias |
| [five-whys-fishbone.md](../../frameworks/execution/five-whys-fishbone.md) | Get from a defect symptom to a cause somebody can change | Taiichi Ohno's practice at Toyota, with Kaoru Ishikawa's cause diagram (1960s) |
| [retrospective-formats.md](../../frameworks/execution/retrospective-formats.md) | Pick the format that fits the week and leave with owned actions | Norman Kerth (2001), then Derby and Larsen (2006) |
| [dora-four-keys.md](../../frameworks/metrics/dora-four-keys.md) | Read delivery health without turning velocity into a target | Nicole Forsgren, Jez Humble, and Gene Kim, Accelerate (2018) |
| [risk-matrix.md](../../frameworks/execution/risk-matrix.md) | Re-score the risks the build just changed | The defense standard MIL-STD-882 (1969) and later ISO 31000; no single author |
| [theory-of-constraints.md](../../frameworks/execution/theory-of-constraints.md) | Name the one station setting the pace of the line, when cycle time climbed and every function reports itself busy | Eliyahu Goldratt, taught as a factory novel in The Goal (1984) |

Knowledge behind the methods: [shape-up.md](../../knowledge/shape-up.md) for appetite and the scope hammer, and [cagan-product-teams.md](../../knowledge/cagan-product-teams.md) for what an empowered team is accountable for. The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [story-writer](../../skills/story-writer/SKILL.md) | Stories or criteria have drifted from what the team is actually building |
| [spec-review](../../skills/spec-review/SKILL.md) | A criterion has stopped parsing against the product and needs to be found |
| [product-review](../../skills/product-review/SKILL.md) | The weekly walk has decayed into status theater |
| [escalation](../../skills/escalation/SKILL.md) | A decision has missed its needed-by date or two owners have deadlocked |
| [decision-memo](../../skills/decision-memo/SKILL.md) | A scope change needs options priced and one decider on the record |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [acceptance-agent](../../agents/acceptance-agent.md) |
| Supporting | [drafting-agent](../../agents/drafting-agent.md), [validation-agent](../../agents/validation-agent.md), [estimator-agent](../../agents/estimator-agent.md) to re-forecast |
| Humans who sign Gate 4 | Engineering lead, QA owner, product owner |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry is a signed Gate 3 plus the instrumentation spec where the PRD names metrics. Exit feeds [deliver.md](deliver.md); a wrong requirement sends you back to Gate 2 explicitly, never silently. The interview path through the same stage is [skills/conductor/questions/build.md](../../skills/conductor/questions/build.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/design.md]] · [[os/maps/deliver.md]] · [[os/maps/README.md]]
- Templates: [[templates/delivery/testing-strategy.md]] · [[templates/delivery/edge-cases.md]] · [[templates/delivery/failure-scenarios.md]] · [[templates/delivery/analytics-instrumentation-spec.md]] · [[templates/definition/acceptance-criteria.md]] · [[templates/execution/decision-log.md]] · [[templates/execution/change-request.md]] · [[templates/execution/tech-debt-register.md]] · [[templates/execution/status-report.md]] · [[templates/execution/retrospective.md]]
- Overlay templates: [[templates/ai/eval-spec.md]] · [[templates/ai/red-team-review.md]]
- Frameworks: [[frameworks/execution/estimation-sheet.md]] · [[frameworks/execution/five-whys-fishbone.md]] · [[frameworks/execution/retrospective-formats.md]] · [[frameworks/metrics/dora-four-keys.md]] · [[frameworks/execution/risk-matrix.md]] · [[frameworks/execution/theory-of-constraints.md]]
- Knowledge: [[knowledge/shape-up.md]] · [[knowledge/cagan-product-teams.md]] · [[knowledge/README.md]]
- Skills: [[skills/story-writer/SKILL.md]] · [[skills/spec-review/SKILL.md]] · [[skills/product-review/SKILL.md]] · [[skills/escalation/SKILL.md]] · [[skills/decision-memo/SKILL.md]] · [[skills/conductor/questions/build.md]]
- Agents: [[agents/TEAM.md]] · [[agents/acceptance-agent.md]] · [[agents/drafting-agent.md]] · [[agents/validation-agent.md]] · [[agents/estimator-agent.md]]
