---
layer: os
stage: DEFINE
gate: 2
feeds: ["os/maps/design.md", "skills/conductor/questions/define.md"]
method: ""
aliases: ["DEFINE"]
---
# DEFINE: map of content

Stage 2 of the six in [OPERATING-LOOP.md](../OPERATING-LOOP.md). Turn the validated problem into requirements someone can build, test, and sign. The stage ends at Gate 2 in [STAGE-GATES.md](../STAGE-GATES.md).

This file is a hub node. Its job is to give the graph one place per stage to fan out from, so the vault reads as six clusters instead of one hairball. It is curated by hand, not generated: see [maps/README.md](README.md) for the maintenance rule.

## The gate this stage ends at

| Gate | Closes | What it demands, in one line |
|---|---|---|
| Gate 2: requirements signed off | DEFINE | Every criterion able to fail on a threshold, every assumption registered with a validate-by date, and the sponsor's signature on the business case itself, not only on the gate form. |

Pick the artifact weight before you open anything here: [WHICH-DOCUMENT.md](../WHICH-DOCUMENT.md). The gate asks the same questions at every weight and answers them in fewer words, never in fewer answers.

## Templates this stage owns

| Template | What it is for |
|---|---|
| [one-pager.md](../../templates/definition/one-pager.md) | The light weight: problem, proposal, scope, one metric with a guardrail, up to three criteria |
| [brd.md](../../templates/definition/brd.md) | Business objectives, scope, constraints, the return logic, and the sponsor's signature block |
| [prd.md](../../templates/definition/prd.md) | Background, objectives, stories, scope, success metrics, launch criteria |
| [frd.md](../../templates/definition/frd.md) | Functional requirements with traceability back to PRD items |
| [nfr.md](../../templates/definition/nfr.md) | Latency, availability, scale, security, accessibility, retention, each a number or a named owner |
| [business-rules.md](../../templates/definition/business-rules.md) | Rule, trigger, source of truth, exceptions, test traceability |
| [assumptions-register.md](../../templates/definition/assumptions-register.md) | Confidence, validation method, validate-by date; the most skipped artifact in the field |
| [acceptance-criteria.md](../../templates/definition/acceptance-criteria.md) | Given, when, then, with edge and negative cases and thresholds that can report a failure |
| [prfaq.md](../../templates/definition/prfaq.md) | Working backwards from the release announcement, with the hostile questions kept in |
| [design-brief.md](../../templates/definition/design-brief.md) | The product and design agreement: problem, constraints, success, deliverables, review dates |

Overlays attach here rather than later. The AI overlay turns model behavior into rows in [eval-spec.md](../../templates/ai/eval-spec.md) plus [guardrails.md](../../templates/ai/guardrails.md) and [hallucination-controls.md](../../templates/ai/hallucination-controls.md). The regulated overlay answers its preconditions before requirements freeze, routed through [reg-gap-check](../../skills/reg-gap-check/SKILL.md) into [modules/regulated/README.md](../../modules/regulated/README.md); nothing under that module is edited here.

## Frameworks the methods come from

| Worksheet | What you run it for | Originator, in one line |
|---|---|---|
| [rice-scoring-sheet.md](../../frameworks/prioritization/rice-scoring-sheet.md) | Score scope with the arithmetic visible and mandates in their own lane | Sean McBride described RICE while at Intercom (2016) |
| [moscow.md](../../frameworks/prioritization/moscow.md) | Negotiate scope against a fixed date, with a cap on musts | Dai Clegg introduced the must, should, could, would split (1994) |
| [wsjf-cost-of-delay.md](../../frameworks/prioritization/wsjf-cost-of-delay.md) | Sequence a fixed set so short valuable work goes first | Don Reinertsen, The Principles of Product Development Flow (2009) |
| [weighted-decision-matrix.md](../../frameworks/prioritization/weighted-decision-matrix.md) | Choose between options on weighted criteria, then test the winner | After Stuart Pugh's controlled convergence method (1981) |
| [user-story-map.md](../../frameworks/prioritization/user-story-map.md) | Arrange stories along the journey so a release is a working slice | Jeff Patton, from 2005 and the 2014 book |
| [impact-mapping.md](../../frameworks/prioritization/impact-mapping.md) | Trace every deliverable to an actor whose behavior must change | Gojko Adzic, Impact Mapping (2012) |
| [decision-doors.md](../../frameworks/prioritization/decision-doors.md) | Classify a decision by reversibility to set the process it deserves | Jeff Bezos, in the 2015 Amazon shareholder letter |
| [estimation-sheet.md](../../frameworks/execution/estimation-sheet.md) | Produce a range with a reference class instead of one confident number | PERT's three-point form (1958), with Cohn and Flyvbjerg on the human bias |

Knowledge behind the methods: [rice-prioritization.md](../../knowledge/rice-prioritization.md), [amazon-pr-faq.md](../../knowledge/amazon-pr-faq.md), [shape-up.md](../../knowledge/shape-up.md). The full index is [knowledge/README.md](../../knowledge/README.md).

## Skills that drive it

| Skill | Use when |
|---|---|
| [write-prd](../../skills/write-prd/SKILL.md) | The requirements stack needs writing, sized first against the weight ladder |
| [ai-prd](../../skills/ai-prd/SKILL.md) | The implementer is a model, so the criteria have to be eval rows |
| [spec-review](../../skills/spec-review/SKILL.md) | A draft needs every untestable adjective found before a human reads it |
| [story-writer](../../skills/story-writer/SKILL.md) | A signed PRD has to become epics, stories, and runnable criteria |
| [decision-memo](../../skills/decision-memo/SKILL.md) | A scope or option decision is stuck in threads and needs one decider |
| [reg-gap-check](../../skills/reg-gap-check/SKILL.md) | Money movement, cards, wallets, lending, crypto, or customer data are in scope |

## Agents that lead it

Per [agents/TEAM.md](../../agents/TEAM.md), section 1.

| Role | Who |
|---|---|
| Lead | [drafting-agent](../../agents/drafting-agent.md) |
| Supporting | [research-agent](../../agents/research-agent.md), [acceptance-agent](../../agents/acceptance-agent.md) for criteria that can fail, [estimator-agent](../../agents/estimator-agent.md) for the first sizing, [validation-agent](../../agents/validation-agent.md) |
| Humans who sign Gate 2 | Product owner, engineering lead, business sponsor, and the regulatory owner where a regulator applies |

No agent signs a gate, and no agent invents a number or a name.

## Where this sits in the loop

Entry is a signed Gate 1 plus a logged weight decision. Exit feeds [design.md](design.md). The interview path through the same stage is [skills/conductor/questions/define.md](../../skills/conductor/questions/define.md).

## Graph links

Wikilinks below are additive: they exist so the Obsidian graph draws the edges. GitHub does not render them, and every file named here is already a normal link above.

- Loop and gates: [[os/OPERATING-LOOP.md]] · [[os/STAGE-GATES.md]] · [[os/WHICH-DOCUMENT.md]] · [[os/PRODUCT-WORKSPACE.md]]
- Neighbor hubs: [[os/maps/discover.md]] · [[os/maps/design.md]] · [[os/maps/README.md]]
- Templates: [[templates/definition/one-pager.md]] · [[templates/definition/brd.md]] · [[templates/definition/prd.md]] · [[templates/definition/frd.md]] · [[templates/definition/nfr.md]] · [[templates/definition/business-rules.md]] · [[templates/definition/assumptions-register.md]] · [[templates/definition/acceptance-criteria.md]] · [[templates/definition/prfaq.md]] · [[templates/definition/design-brief.md]]
- Overlay templates: [[templates/ai/eval-spec.md]] · [[templates/ai/guardrails.md]] · [[templates/ai/hallucination-controls.md]] · [[modules/regulated/README.md]]
- Frameworks: [[frameworks/prioritization/rice-scoring-sheet.md]] · [[frameworks/prioritization/moscow.md]] · [[frameworks/prioritization/wsjf-cost-of-delay.md]] · [[frameworks/prioritization/weighted-decision-matrix.md]] · [[frameworks/prioritization/user-story-map.md]] · [[frameworks/prioritization/impact-mapping.md]] · [[frameworks/prioritization/decision-doors.md]] · [[frameworks/execution/estimation-sheet.md]]
- Knowledge: [[knowledge/rice-prioritization.md]] · [[knowledge/amazon-pr-faq.md]] · [[knowledge/shape-up.md]] · [[knowledge/README.md]]
- Skills: [[skills/write-prd/SKILL.md]] · [[skills/ai-prd/SKILL.md]] · [[skills/spec-review/SKILL.md]] · [[skills/story-writer/SKILL.md]] · [[skills/decision-memo/SKILL.md]] · [[skills/reg-gap-check/SKILL.md]] · [[skills/conductor/questions/define.md]]
- Agents: [[agents/TEAM.md]] · [[agents/drafting-agent.md]] · [[agents/research-agent.md]] · [[agents/acceptance-agent.md]] · [[agents/estimator-agent.md]] · [[agents/validation-agent.md]]
