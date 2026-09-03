---
layer: os
stage: DESIGN
gate: 3
feeds: ["os/maps/build.md", "skills/conductor/questions/design.md"]
method: ""
aliases: ["DESIGN"]
---
# DESIGN: map of content

Stage 3 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Decide how it will be built and what could go wrong, before anything is built. The stage ends at Gate 3 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 3: architecture and risks reviewed | DESIGN | One rejected alternative recorded with its tradeoff, every integration and every high risk owned by a person rather than a team, and alert thresholds set before any code exists. |

## Templates this stage owns

| Template | What it is for |
|---|---|
| [system-design.md](../../templates/architecture/system-design.md) | Goals, non-goals, components, the alternatives considered and their tradeoffs |
| [solution-architecture.md](../../templates/architecture/solution-architecture.md) | Context, capability map, integration points, the build or buy rationale |
| [adr.md](../../templates/architecture/adr.md) | One numbered record per decision; reversals supersede and never edit |
| [data-model.md](../../templates/architecture/data-model.md) | Entities, keys, the data dictionary, PII classified with retention per class |
| [api-contract.md](../../templates/architecture/api-contract.md) | Endpoint, schema, auth, errors, versioning |
| [sequence-diagram.md](../../templates/architecture/sequence-diagram.md) | The synchronous, asynchronous, and error paths drawn rather than described |
| [integrations.md](../../templates/architecture/integrations.md) | System, protocol, auth, SLA, owner, and the failure behavior a user would see |
| [security-architecture.md](../../templates/architecture/security-architecture.md) | The threat walk per component, with a mitigation owner per finding |
| [observability.md](../../templates/architecture/observability.md) | SLOs, alert thresholds, dashboard owner, the synthetic failure check |
| [privacy-impact-assessment.md](../../templates/architecture/privacy-impact-assessment.md) | Data inventory, lawful basis, risks and mitigations, the sign-off line |
| [accessibility-checklist.md](../../templates/architecture/accessibility-checklist.md) | Conformance level set once, then checks by component with evidence |
| [stakeholder-map.md](../../templates/execution/stakeholder-map.md) | Interest, influence, cadence, concerns, and who is needed at which gate |
| [risk-register.md](../../templates/execution/risk-register.md) | Likelihood, impact, score, mitigation, a named owner, a review date |
| [decision-log.md](../../templates/execution/decision-log.md) | Numbered decisions with options, rationale, and the decider |
| [dependency-register.md](../../templates/execution/dependency-register.md) | Other teams' dates, reviewed weekly from this gate onward |
| [state.md](../../templates/execution/state.md) | The per-product memory a Conductor run appends to |

The AI overlay adds least-access checks to [agent-architecture.md](../../templates/ai/agent-architecture.md) and an owner plus a test per rail in [guardrails.md](../../templates/ai/guardrails.md), with a hostile read through [red-team-review.md](../../templates/ai/red-team-review.md) before the gate.

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [premortem-worksheet.md](../../frameworks/execution/premortem-worksheet.md) | Assume the failure happened and write down why, while it is cheap | Gary Klein described the premortem in Harvard Business Review (2007) |
| [risk-matrix.md](../../frameworks/execution/risk-matrix.md) | Score likelihood against impact on defined scales, with an appetite line | The defense standard MIL-STD-882 (1969) and later ISO 31000; no single author |
| [raci.md](../../frameworks/execution/raci.md) | Put one accountable name on every decision | Responsibility charting, in general management practice from the 1970s |
| [stakeholder-power-interest.md](../../frameworks/execution/stakeholder-power-interest.md) | Spend engagement time where it changes the outcome | Aubrey Mendelow's power and interest grid (1991) |
| [build-buy-partner.md](../../frameworks/strategy/build-buy-partner.md) | Score the four options on core, time, cost, control, and exit | After Coase on the boundary of the firm (1937) and Williamson's later work |
| [team-topologies-assessment.md](../../frameworks/assessment/team-topologies-assessment.md) | Name which shape each team actually operates as, and what the gap costs | Matthew Skelton and Manuel Pais, Team Topologies (2019) |
| [tech-debt-assessment.md](../../frameworks/assessment/tech-debt-assessment.md) | Price each compromise per quarter and once, then decide | Ward Cunningham's 1992 debt metaphor, with Martin Fowler's 2009 quadrant |
| [fmea.md](../../frameworks/execution/fmea.md) | Walk the design function by function and enumerate the failure modes nobody thought to name | The US military standard MIL-P-1629 (1949), taken up by NASA and later Ford |

Knowledge behind the methods: [cagan-product-teams.md](../../knowledge/cagan-product-teams.md) for the feasibility and viability risks, and [domains/ai-products.md](../../knowledge/domains/ai-products.md) when a model sits inside the product. The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [program-premortem](../../skills/program-premortem/SKILL.md) | The plan is approaching Gate 3 or a cutover and status feels fine to everyone |
| [spec-review](../../skills/spec-review/SKILL.md) | The NFR set or the business rules still read as prose |
| [decision-memo](../../skills/decision-memo/SKILL.md) | An architecture option needs one decider, a door type, and the dissent on record |
| [escalation](../../skills/escalation/SKILL.md) | A dependency owner has not agreed to the date in your register |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [architect-agent](../../agents/architect-agent.md) |
| Supporting | [estimator-agent](../../agents/estimator-agent.md) for option cost, [red-team-agent](../../agents/red-team-agent.md) before the gate, [drafting-agent](../../agents/drafting-agent.md), [validation-agent](../../agents/validation-agent.md) |
| Humans who sign Gate 3 | Architect or senior engineer, product owner, security reviewer |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry is a signed Gate 2 with the requirement set frozen enough that an architect can be wrong about it. Exit feeds [build.md](build.md). The interview path through the same stage is [skills/conductor/questions/design.md](../../skills/conductor/questions/design.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/define.md]] · [[os/maps/build.md]] · [[os/maps/README.md]]
- Templates: [[templates/architecture/system-design.md]] · [[templates/architecture/solution-architecture.md]] · [[templates/architecture/adr.md]] · [[templates/architecture/data-model.md]] · [[templates/architecture/api-contract.md]] · [[templates/architecture/sequence-diagram.md]] · [[templates/architecture/integrations.md]] · [[templates/architecture/security-architecture.md]] · [[templates/architecture/observability.md]] · [[templates/architecture/privacy-impact-assessment.md]] · [[templates/architecture/accessibility-checklist.md]] · [[templates/execution/stakeholder-map.md]] · [[templates/execution/risk-register.md]] · [[templates/execution/decision-log.md]] · [[templates/execution/dependency-register.md]] · [[templates/execution/state.md]]
- Overlay templates: [[templates/ai/agent-architecture.md]] · [[templates/ai/guardrails.md]] · [[templates/ai/red-team-review.md]]
- Frameworks: [[frameworks/execution/premortem-worksheet.md]] · [[frameworks/execution/risk-matrix.md]] · [[frameworks/execution/raci.md]] · [[frameworks/execution/stakeholder-power-interest.md]] · [[frameworks/strategy/build-buy-partner.md]] · [[frameworks/assessment/team-topologies-assessment.md]] · [[frameworks/assessment/tech-debt-assessment.md]] · [[frameworks/execution/fmea.md]]
- Knowledge: [[knowledge/cagan-product-teams.md]] · [[knowledge/domains/ai-products.md]] · [[knowledge/README.md]]
- Skills: [[skills/program-premortem/SKILL.md]] · [[skills/spec-review/SKILL.md]] · [[skills/decision-memo/SKILL.md]] · [[skills/escalation/SKILL.md]] · [[skills/conductor/questions/design.md]]
- Agents: [[agents/TEAM.md]] · [[agents/architect-agent.md]] · [[agents/estimator-agent.md]] · [[agents/red-team-agent.md]] · [[agents/drafting-agent.md]] · [[agents/validation-agent.md]]
