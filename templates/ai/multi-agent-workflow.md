---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Multi-Agent Workflow", "multi-agent-workflow"]
---
# Multi-Agent Workflow: [workflow name]

Stage: AI overlay, active whenever two or more agents cooperate on one task; feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [AI products](../../knowledge/domains/ai-products.md)
Skill: [AI PRD skill](../../skills/ai-prd/SKILL.md)
Filled example: [Ledgerline Expense Copilot Receipt Draft](../../examples/ledgerline-multi-agent-workflow.md)

<!-- [agent-architecture.md](agent-architecture.md) says who the agents are and what
     they may touch. This document says how they cooperate: the handoff order, the
     state they share, when a human is pulled in, and what makes the whole thing
     stop. A multi-agent system without written termination rules is a bill with no
     ceiling. -->

**Workflow:** [one sentence: input in, outcome out]
**Workflow owner:** [name] · **Document date:** [YYYY-MM-DD]
**Agents involved:** [list, each one a roster row in the filled agent-architecture.md]

## 1. Handoff sequence

<!-- Number every step. Each handoff names what is passed, in what format, and what the
     receiver does if the payload is malformed. "It sends the results along" is where
     multi-agent systems go to die. -->

| Step | From | To | Payload (format, required fields) | On malformed payload |
|---|---|---|---|---|
| 1 | [entry point] | [agent A] | [e.g. request JSON: id, text, requester] | [reject with reason, log] |
| 2 | [agent A] | [agent B] | [e.g. classification + confidence] | [route to human queue] |
| 3 | [add until the happy path and every branch are numbered] | | | |

## 2. Shared state

<!-- Shared state is the only thing every agent in the workflow can see at once, so
     a field with no declared owner is where two agents silently disagree. A trap:
     leaving the schema as "whatever the last agent wrote", because that is not a
     schema, it is a race. This fails when the human view names a dashboard that
     was never built; a run in flight that nobody can inspect is not actually
     observable. Never let two agents write the same field without the merge rule
     stated here. -->

- Where it lives: [store, path, or channel]
- Schema: [fields, or link to the schema file]
- Who may write which fields: [per-agent write map; two writers to one field needs a merge rule, written here]
- What a human sees when inspecting a run in flight: [view, location]

## 3. Escalation to a human

<!-- Escalation exists so a stuck or disagreeing run reaches a person before it
     burns budget or ships a bad output. A trap: writing a condition only a human
     would notice by reading logs, like "seems off", instead of a number a monitor
     can check. This fails when the escalation role is a named individual instead
     of a rota, because the workflow then stops the day that person is out. Do not
     let an agent decide for itself that a situation does not need escalation; that
     call belongs to the conditions listed here. -->

- Conditions that force escalation: [confidence below n / agents disagree / step SLA exceeded / cost cap approached / add]
- Escalates to (role with a rota, not a name): [role]
- What the human receives: [the run state, the disagreement, the recommended action]
- Approval-gated actions inside the workflow route through the filled [human-approval-gates.md](human-approval-gates.md), not through an agent's own judgment

## 4. Termination

<!-- Three ways every run ends, all written down. -->

- Success: [the condition that means done, checkable by code]
- Failure: [conditions that end the run as failed, and what the requester is told]
- Budget stop: the run halts when it hits any of the caps in section 5, preserving state for human review, never silently retrying past a cap

## 5. Cost cap

<!-- Every cap here turns a runaway loop into a bounded, budgeted event instead of
     an open-ended bill. A trap: setting the per-run ceiling and leaving the
     per-day ceiling blank, because a workflow that respects one cap can still run
     often enough to blow through the other. This fails when every ceiling
     escalates to a human with no cheaper degrade path, so an ordinary volume
     spike pages someone instead of costing a little more. Never leave a cap as a
     round guess; derive it from the worked micro-example below or a measured
     baseline, and name who actually reads the spend report. -->

| Cap | Value |
|---|---|
| Per-run token or spend ceiling | [n, ILLUSTRATIVE until agreed with [name]] |
| Per-day ceiling for the whole workflow | [n] |
| Max steps per run (loop guard) | [n] |
| Max retries per step | [n] |
| At any ceiling | [halt and escalate / degrade to the cheap tier per ../../routing/README.md; state which] |
| Who reads the spend report, on what cadence | [name, cadence] |

## Worked micro-example

A two-agent research-and-draft flow: step 1, researcher gathers sources and writes a findings file (its only write permission); step 2, drafter reads findings and fills one template; step 3, validator checks required fields and either terminates with success or bounces once to the drafter; a second bounce escalates to the duty editor. Caps: 40 steps, one retry per step, per-run spend ceiling ILLUSTRATIVE. Every run ends in one of three written ways.

## Exit gate

- [ ] Every handoff is numbered with a payload format and a malformed-payload behavior
- [ ] Every shared-state field has exactly one writer, or a written merge rule
- [ ] Escalation conditions are testable and route to a role with a rota
- [ ] All three termination paths are written, including the budget stop
- [ ] Every cap has a number and a named reader of the spend report
