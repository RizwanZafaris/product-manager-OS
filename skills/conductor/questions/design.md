---
layer: skills
stage: DESIGN
gate: 3
feeds: []
method: ""
aliases: ["DESIGN bank"]
---
# DESIGN bank

Stage: DESIGN, feeds Gate 3 (architecture and risks reviewed) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md).
Working handoffs: [../../../agents/drafting-agent.md](../../../agents/drafting-agent.md) in the Architect role for the `templates/architecture/` set; [../../program-premortem/SKILL.md](../../program-premortem/SKILL.md) for the failure pass.
Applies: the premortem method, Gary Klein's entry in [../../../knowledge/README.md](../../../knowledge/README.md), assume the failure has happened, then explain it while being right is still cheap. The Conductor names this method aloud when DESIGN-4 runs.
Format and ladder: [README.md](README.md).

### DESIGN-1: the rejected alternative

Ask: What alternative was seriously considered and rejected, and what tradeoff decided it?
Wrong costs: A design with no rejected alternative has not been designed yet; it has been transcribed.
Evidence class: 2, the tradeoff written as an ADR.
Cross-examine when: the alternative is a strawman nobody would have built. Move: banned openers, then: what would a competent team choosing it have been optimizing for?
Accept when: a real alternative, the tradeoff that decided against it, and the consequence accepted by deciding.
Lands in: `architecture/adr.md` (one ADR per decision, suffix names the decision), and STATE.md accepted answers.

### DESIGN-2: integrations

Ask: For every integration, who owns it, under what SLA, and what happens when it fails?
Wrong costs: "We will figure it out" at design time becomes an incident owned by whoever is on call.
Evidence class: 3, the counterparty's commitment in writing, or the gap named per integration.
Cross-examine when: the failure behavior is retry-and-hope, or the owner is a team, not a person. Move: category to name.
Accept when: every integration row carries owner, SLA, and failure behavior, and no row says it will be worked out later.
Lands in: `architecture/integrations.md` sections 1 and 3, and STATE.md accepted answers.

### DESIGN-3: where PII lives

Ask: Where does personally identifiable information live, and what is the retention per data class?
Wrong costs: Retention decided after launch is retention decided by whoever gets the deletion request.
Evidence class: 2, the data model with classes marked and retention stated.
Cross-examine when: "we do not really store PII" arrives without a walked data model. Move: interest to behavior, walk the model field by field.
Accept when: every data class marked, retention stated per class, and the deletion path named.
Lands in: `architecture/data-model.md` and `architecture/security-architecture.md`, and STATE.md accepted answers.

### DESIGN-4: the premortem

Ask: It is six months from now and this product failed: why?
Wrong costs: Teams reliably know how their project will fail and reliably are not asked.
Evidence class: 5, filed as owned risks; the deliverable is the register row, not certainty.
Cross-examine when: the first answer is generic (ran late, lost focus) or the second answer repeats the first. Move: banned openers; this question is always asked twice, and the second answer must differ from the first.
Accept when: two distinct failure causes, each landed in the risk register with a likelihood, an impact, and a named owner. Then hand off to [../../program-premortem/SKILL.md](../../program-premortem/SKILL.md) for the full twelve-mode pass; its PRESENT findings join the same register.
Lands in: `execution/risk-register.md` section 2, and STATE.md accepted answers.

### DESIGN-5: who we wait on

Ask: Which teams does this product wait on, by what date, and who is the escalation contact?
Wrong costs: The dependency discovered at integration time is owned by a team that never agreed to your date.
Evidence class: 3, the dependency in the other team's committed plan, not only in yours.
Cross-examine when: "they know about it". Move: interest to behavior, is it in their plan with a date, and can you point at it?
Accept when: every dependency has a needed-by date, an escalation contact, and evidence of the counterparty's commitment or an honest register row saying it is unconfirmed.
Lands in: `execution/dependency-register.md` sections 1 and 2, and STATE.md accepted answers.

### DESIGN-6: seeing it misbehave

Ask: How will you see this misbehaving before users tell you?
Wrong costs: Without SLOs and alerts named now, the monitoring plan is the support queue.
Evidence class: 2, SLOs, alert thresholds, and a dashboard owner written down before code exists.
Cross-examine when: the answer is "standard monitoring" or a tool name with no thresholds. Move: naked numbers.
Accept when: SLOs with numbers, alert thresholds, and one named dashboard owner.
Lands in: `architecture/observability.md` sections 1, 4, and 5, and STATE.md accepted answers.

### DESIGN-7: AI overlay, least access

Ask: What is the least access each agent needs, and does every guardrail have an owner and a test?
Wrong costs: An over-permissioned agent is a breach with a project plan; an untested guardrail is a diagram.
Evidence class: 2, the permission table and the guardrail table, each row owned and tested.
Cross-examine when: any agent holds access "for flexibility", or any guardrail's test is a design review. Move: interest to behavior, show the test that exercised it.
Accept when: every agent's access is the minimum its task needs, and every guardrail row names an owner and a test. Skip this entry with a cited source when STATE.md says the AI overlay is not active.
Lands in: filled copies of `templates/ai/agent-architecture.md` and `templates/ai/guardrails.md` in the workspace, and STATE.md accepted answers.

## Forced pair

On "advance anyway": DESIGN-4, then DESIGN-5. The unasked premortem and the unconfirmed dependency are the two failures Gate 3's own skip warning names.

## Gate 3 rendering

| Gate 3 checklist line | Evidenced by |
|---|---|
| At least one rejected alternative recorded as an ADR | DESIGN-1 |
| Every integration names owner, protocol, SLA, failure behavior | DESIGN-2 |
| Data model classifies PII with retention per class | DESIGN-3 |
| Security walk per component with mitigation owners | DESIGN-3, plus the Architect-role handoff against `architecture/security-architecture.md` |
| Observability names SLOs, thresholds, dashboard owner | DESIGN-6 |
| A premortem ran and the risk register absorbed it | DESIGN-4, plus the program-premortem handoff |
| High risks have named owners and review dates | DESIGN-4 |
| Dependency register complete with escalation contacts | DESIGN-5 |
| AI overlay: least access, guardrails owned and tested | DESIGN-7 |
