---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Multi-Agent Workflow", "multi-agent-workflow"]
---
# Multi-Agent Workflow: [workflow name]

Stage: AI overlay, active whenever two or more agents cooperate on one task; feeds Gate 3 (architecture and risks reviewed)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- agent-architecture.md says who the agents are and what they may touch. This
     document says how they cooperate: the handoff order, the state they share, when a
     human is pulled in, and what makes the whole thing stop. A multi-agent system
     without written termination rules is a bill with no ceiling. -->

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

- Where it lives: [store, path, or channel]
- Schema: [fields, or link to the schema file]
- Who may write which fields: [per-agent write map; two writers to one field needs a merge rule, written here]
- What a human sees when inspecting a run in flight: [view, location]

## 3. Escalation to a human

- Conditions that force escalation: [confidence below n / agents disagree / step SLA exceeded / cost cap approached / add]
- Escalates to (role with a rota, not a name): [role]
- What the human receives: [the run state, the disagreement, the recommended action]
- Approval-gated actions inside the workflow route through the filled human-approval-gates.md, not through an agent's own judgment

## 4. Termination

<!-- Three ways every run ends, all written down. -->

- Success: [the condition that means done, checkable by code]
- Failure: [conditions that end the run as failed, and what the requester is told]
- Budget stop: the run halts when it hits any of the caps in section 5, preserving state for human review, never silently retrying past a cap

## 5. Cost cap

- Per-run token or spend ceiling: [n, ILLUSTRATIVE until agreed with [name]]
- Per-day ceiling for the whole workflow: [n]
- Max steps per run (loop guard): [n]
- Max retries per step: [n]
- At any ceiling: [halt and escalate / degrade to the cheap tier per ../../routing/README.md; state which]
- Who reads the spend report, on what cadence: [name, cadence]

## Worked micro-example

A two-agent research-and-draft flow: step 1, researcher gathers sources and writes a findings file (its only write permission); step 2, drafter reads findings and fills one template; step 3, validator checks required fields and either terminates with success or bounces once to the drafter; a second bounce escalates to the duty editor. Caps: 40 steps, one retry per step, per-run spend ceiling ILLUSTRATIVE. Every run ends in one of three written ways.

## Exit gate

- [ ] Every handoff is numbered with a payload format and a malformed-payload behavior
- [ ] Every shared-state field has exactly one writer, or a written merge rule
- [ ] Escalation conditions are testable and route to a role with a rota
- [ ] All three termination paths are written, including the budget stop
- [ ] Every cap has a number and a named reader of the spend report
