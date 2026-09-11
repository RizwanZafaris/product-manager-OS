---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Human Approval Gates", "human-approval-gates"]
---
# Human Approval Gates: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 3 (architecture and risks reviewed) and Gate 5 (release readiness)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- An approval gate holds an action until a named human role says yes. Three failure
     modes to design out: the gate that auto-approves on silence, the approver who is
     a team name rather than a role with a rota, and the approval that leaves no
     record. For regulated products the escalation rows in
     ../../modules/regulated/README.md apply on top of this table. -->

**Feature:** [one sentence]
**Gates owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Gate table

| # | Trigger condition (specific, testable) | Action held | Approver role (role, not person; person on rota) | Channel and SLA | On timeout | Test |
|---|---|---|---|---|---|---|
| 1 | [e.g. any irreversible action: payment, send, deletion, filing] | [the action] | [role] | [queue or channel, n minutes] | deny and notify | [test ID] |
| 2 | [e.g. output value above threshold n] | [release of the output] | [role] | [channel, SLA] | deny and notify | [test ID] |
| 3 | An agent proposes a tool call inside the live conversation (file write, code execution, an external API call) | The tool call, shown to the user with its parameters before it runs | The user in the conversation, in-line | Synchronous, blocks the turn until answered | deny, tool call not made | [test ID] |
| 4 | A design agent with write access to design files proposes a change (for example, a Penpot MCP integration editing a shared file, paraphrased as the pattern, not a specific vendor's exact behaviour) | The write to the shared design file | Design lead, or the named owner of that file | [channel, SLA] | deny and notify | [test ID] |
| 5 | [add] | | | | | |

<!-- On timeout the default is deny. If a gate must fail open for operational reasons,
     write the reason, the risk owner's name, and the compensating control in section 3.
     A silent fail-open is how "human in the loop" becomes a legend. -->

## 2. Audit log requirement

Every gate decision writes a record with, at minimum:

- Request ID, timestamp, triggering condition matched
- The held action's full parameters as presented to the approver
- Approver identity, decision, decision time, and free-text reason if denied
- Model version and prompt version that produced the request
- Retention period for these records: [n, per applicable requirement]
- Where the log lives and who can read it: [location, access rule]
- Data classes the record carries, with their PII class from ../architecture/data-model.md, and which fields are masked, excluded, or stored as a reference to the unchanged original payload, per ../architecture/observability.md section 2; what the approver saw must stay reconstructable

## 3. Exceptions and fail-open register

| Gate # | Why it fails open | Compensating control | Risk owner | Review date |
|---|---|---|---|---|
| [none is the right answer until proven otherwise] | | | | |
| *Example: an automation that posts a channel reply to a routine, low-stakes question (ILLUSTRATIVE)* | *A queue-blocking approval on every reply would defeat the automation's purpose; the volume makes a human-in-the-loop gate impractical at this trigger* | *Replies are logged and sampled for review after the fact; any reply flagged by the sampling or by a recipient escalates to a real gate on the next occurrence of that pattern* | *[name]* | *[date]* |

## Worked micro-example

Gate: any outbound message composed by the assistant. Trigger: message ready to send. Approver role: duty ops reviewer, weekday rota of three. Channel: review queue, 30 minute SLA ILLUSTRATIVE. On timeout: message is not sent, requester notified, case reopens next shift. Log: full message body, approver, decision, model and prompt version. The message that never went out on a Friday night is the control working, not the control failing.

## Exit gate

- [ ] Every trigger condition is testable, not a vibe ("sensitive" is a vibe; "amount over n" is a trigger)
- [ ] Every approver is a role with a rota, and the rota exists
- [ ] Every timeout behavior is deny, or the fail-open is in section 3 with an owner
- [ ] The audit record fields are implemented, not aspirational; someone has read one
- [ ] The audit record's data classes are classified and its PII handling is stated
