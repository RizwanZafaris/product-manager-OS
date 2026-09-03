---
layer: os
stage: DELIVER
gate: 5
feeds: ["os/maps/operate.md", "skills/conductor/questions/deliver.md"]
method: ""
aliases: ["DELIVER"]
---
# DELIVER: map of content

Stage 5 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Ship it on purpose, with a way back. The stage ends at Gate 5 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 5: release readiness green | DELIVER | UAT exit criteria met with real users or named proxies, a rollback actually performed with its elapsed time recorded, and one signature per function rather than one for the group. |

## Templates this stage owns

| Template | What it is for |
|---|---|
| [uat-plan.md](../../templates/delivery/uat-plan.md) | Scope, entry and exit criteria, testers, defect severity agreed before testing |
| [release-readiness.md](../../templates/delivery/release-readiness.md) | The go or no-go sheet: features, tests, known issues, rollback, comms, sign-offs |
| [migration-cutover-plan.md](../../templates/delivery/migration-cutover-plan.md) | Phases, the rehearsal, the point of no return, reconciliation |
| [support-runbook.md](../../templates/delivery/support-runbook.md) | What an agent opens with a customer on the line |
| [launch-comms-plan.md](../../templates/delivery/launch-comms-plan.md) | Audiences, channels, timeline, and the rollback message |
| [customer-comms.md](../../templates/delivery/customer-comms.md) | The messages themselves, with the approval chain beside each |
| [release-notes.md](../../templates/delivery/release-notes.md) | One change set written three times: customer, internal, support |
| [sla-slo-definition.md](../../templates/delivery/sla-slo-definition.md) | Indicators, objectives, and the agreement kept apart |
| [sales-enablement-one-pager.md](../../templates/delivery/sales-enablement-one-pager.md) | Derived from positioning: pains, proof, objections, demo path |
| [gtm-plan.md](../../templates/planning/gtm-plan.md) | First cohort and channel with evidence the channel reaches them, and a stop condition |
| [positioning.md](../../templates/planning/positioning.md) | Alternatives forward to a category, never a tagline backward |

The AI overlay verifies guardrails live in the release candidate and tests the kill switch rather than designing it. The regulated overlay re-checks here that what was promised at DEFINE is true of the artifact that ships, routed through [reg-gap-check](../../skills/reg-gap-check/SKILL.md) into [modules/regulated/README.md](../../modules/regulated/README.md).

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [positioning-canvas.md](../../frameworks/strategy/positioning-canvas.md) | Work from competitive alternatives to a market category | April Dunford, Obviously Awesome (2019) |
| [packaging-good-better-best.md](../../frameworks/pricing/packaging-good-better-best.md) | Choose the value metric, set fences, write migration rules first | Common commercial practice, with Rafi Mohammed's treatment (2018) |
| [raci.md](../../frameworks/execution/raci.md) | Put one accountable name on each launch task and each comms approval | Responsibility charting, in general management practice from the 1970s |
| [risk-matrix.md](../../frameworks/execution/risk-matrix.md) | Score the known issues you are choosing to ship with | The defense standard MIL-STD-882 (1969) and later ISO 31000; no single author |
| [premortem-worksheet.md](../../frameworks/execution/premortem-worksheet.md) | Re-run the failure question against the cutover, not the design | Gary Klein described the premortem in Harvard Business Review (2007) |

Knowledge behind the methods: [crossing-the-chasm.md](../../knowledge/crossing-the-chasm.md) for the beachhead before the broadcast. The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [launch-readiness](../../skills/launch-readiness/SKILL.md) | Gate 5 needs walking item by item into a go, no-go, or conditional go |
| [gtm-launch-planner](../../skills/gtm-launch-planner/SKILL.md) | The launch needs tiering, a first cohort, channels, and comms drafted early |
| [pricing-packaging](../../skills/pricing-packaging/SKILL.md) | The release changes price, tiers, or fences |
| [stakeholder-update](../../skills/stakeholder-update/SKILL.md) | Executives need the situation, complication, and the decision they owe you |
| [reg-gap-check](../../skills/reg-gap-check/SKILL.md) | The overlay answers from Gate 2 have to be re-verified against what ships |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [release-manager-agent](../../agents/release-manager-agent.md) |
| Supporting | [pmm-agent](../../agents/pmm-agent.md) for narrative and enablement, [acceptance-agent](../../agents/acceptance-agent.md) for UAT evidence, [red-team-agent](../../agents/red-team-agent.md), [validation-agent](../../agents/validation-agent.md) |
| Humans who sign Gate 5 | Release owner, product owner, operations or support lead, and the regulatory owner where a regulator applies |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry is a signed Gate 4 and a release candidate a non-engineer can open. Exit feeds [operate.md](operate.md), and the Gate 6 review window is chosen here, before the numbers exist. The interview path through the same stage is [skills/conductor/questions/deliver.md](../../skills/conductor/questions/deliver.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/build.md]] · [[os/maps/operate.md]] · [[os/maps/README.md]]
- Templates: [[templates/delivery/uat-plan.md]] · [[templates/delivery/release-readiness.md]] · [[templates/delivery/migration-cutover-plan.md]] · [[templates/delivery/support-runbook.md]] · [[templates/delivery/launch-comms-plan.md]] · [[templates/delivery/customer-comms.md]] · [[templates/delivery/release-notes.md]] · [[templates/delivery/sla-slo-definition.md]] · [[templates/delivery/sales-enablement-one-pager.md]] · [[templates/planning/gtm-plan.md]] · [[templates/planning/positioning.md]]
- Overlay routes: [[modules/regulated/README.md]] · [[templates/ai/guardrails.md]]
- Frameworks: [[frameworks/strategy/positioning-canvas.md]] · [[frameworks/pricing/packaging-good-better-best.md]] · [[frameworks/execution/raci.md]] · [[frameworks/execution/risk-matrix.md]] · [[frameworks/execution/premortem-worksheet.md]]
- Knowledge: [[knowledge/crossing-the-chasm.md]] · [[knowledge/README.md]]
- Skills: [[skills/launch-readiness/SKILL.md]] · [[skills/gtm-launch-planner/SKILL.md]] · [[skills/pricing-packaging/SKILL.md]] · [[skills/stakeholder-update/SKILL.md]] · [[skills/reg-gap-check/SKILL.md]] · [[skills/conductor/questions/deliver.md]]
- Agents: [[agents/TEAM.md]] · [[agents/release-manager-agent.md]] · [[agents/pmm-agent.md]] · [[agents/acceptance-agent.md]] · [[agents/red-team-agent.md]] · [[agents/validation-agent.md]]
