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
| 3 | [add] | | | | | |

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

## 3. Exceptions and fail-open register

| Gate # | Why it fails open | Compensating control | Risk owner | Review date |
|---|---|---|---|---|
| [none is the right answer until proven otherwise] | | | | |

## Worked micro-example

Gate: any outbound message composed by the assistant. Trigger: message ready to send. Approver role: duty ops reviewer, weekday rota of three. Channel: review queue, 30 minute SLA ILLUSTRATIVE. On timeout: message is not sent, requester notified, case reopens next shift. Log: full message body, approver, decision, model and prompt version. The message that never went out on a Friday night is the control working, not the control failing.

## Exit gate

- [ ] Every trigger condition is testable, not a vibe ("sensitive" is a vibe; "amount over n" is a trigger)
- [ ] Every approver is a role with a rota, and the rota exists
- [ ] Every timeout behavior is deny, or the fail-open is in section 3 with an owner
- [ ] The audit record fields are implemented, not aspirational; someone has read one
