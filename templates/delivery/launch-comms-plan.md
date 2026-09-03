# Launch Comms Plan: [product or feature name]

**Stage:** DELIVER (feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md); expands section 6 of [release-readiness.md](release-readiness.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [gtm-launch-planner](../../skills/gtm-launch-planner/SKILL.md)

<!-- The release checklist has one communications table. This file is that table
     grown up, for launches where more than two audiences have to hear different
     things at different times. If the release-readiness table covers it, delete
     this file and say so; a comms plan for a silent release is theater.

     Two rules carry the document. First, one set of launch facts, written once in
     section 1, that every message derives from; the moment support and sales tell
     different stories, the launch has a defect no dashboard shows. Second, the
     rollback message is written now, while everyone is calm. For message structure,
     Barbara Minto's situation-complication-resolution spine (indexed in the
     knowledge layer) is the shape that survives an executive skim. -->

**Owner:** [name] · **Launch date:** [YYYY-MM-DD] · **Last updated:** [YYYY-MM-DD]
**GTM plan:** [filled copy of ../planning/gtm-plan.md] · **Release:** [version or milestone]

## 1. Launch facts, written once

<!-- Every message in section 2 derives from these lines. Change them here, then
     re-derive; never patch a single channel. -->

- What is shipping, in one sentence a customer would recognize: [sentence]
- When: [date and time, with timezone] · Rollout shape: [all at once / staged: how]
- Who gets it first: [cohort from the GTM plan]
- What changes for existing users: [the honest answer, including anything taken away]
- What does NOT change: [the reassurance line, if one is needed]

## 2. Audiences and messages

<!-- One row per audience that needs a different message, not a different copy of
     the same one. "What they must do" is the field that earns the row; a message
     with no action is a candidate for deletion. The italic row shows a completed entry. -->

| Audience | What they need to know | What they must do | Message owner | Sign-off by |
|---|---|---|---|---|
| | | | | |
| *support team* | *new flow, top 3 expected questions, known issue #2* | *use the new macro; escalate billing cases to [name]* | *[name]* | *support lead* |

## 3. Channel and timeline

<!-- Work backward from launch. T-0 is launch day; internal audiences hear before
     external ones, support before everyone. -->

| When (T-n days) | Channel | Audience | Artifact (draft linked) | Owner | Sent |
|---|---|---|---|---|---|
| | | | | | |

## 4. Support and field readiness

- [ ] Support briefed, with the known-issues table from release-readiness in hand
- [ ] FAQ drafted from the hardest real questions, not the easiest: [link]
- [ ] Escalation path named: [who, for what severity, reachable how]
- [ ] Sales or account teams (if any) have the one-pager and the pricing answer

## 5. Rollback comms, pre-written

<!-- If the rollback trigger in release-readiness fires, these go out with names
     already on them. Writing this after the trigger fires costs an hour you will
     not have. -->

- Holding statement (external, sendable within [n] minutes): [two sentences, drafted now]
- Internal notice: [channel, owner, drafted now]
- Who approves sending: [name] · Who sends: [name]
- If customer data was affected: [the additional obligations, and who confirms them; see ../operate/compliance-impact-assessment.md if a regulator is in scope]

## 6. After launch

- Day-1 report: [what number, from the launch dashboard, sent by whom to whom]
- Week-1 summary: [owner, audience]
- Feedback route: [where customer reactions are collected, feeding ../operate/post-launch-review.md]

## Exit gate

This plan is done when:

- [ ] Section 1 is filled and every message in section 3 links to a draft derived from it
- [ ] Every audience row has an action, an owner, and a sign-off name
- [ ] Support is briefed before any external message is scheduled
- [ ] The rollback holding statement exists and its approver is named

Signed: [name], [role], [YYYY-MM-DD]
