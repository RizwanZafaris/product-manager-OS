---
name: launch-readiness
description: Run the Gate 5 release readiness checklist item by item against the delivery documents and the release candidate, and produce a go, no-go, or conditional go with every condition named, owned, and dated. Use when a release is inside two weeks of its target date, when a readiness document is being filled for the first time, when a launch slipped and the checklist needs re-running, or when someone wants to ship on a feeling. Takes the release readiness document, UAT results, rollback evidence, comms drafts, and the runbook; returns the item-by-item verdict table and the decision packet for the gate chair.
---

# Launch Readiness: go, no-go, or conditions with names on them

Launches fail at the gate in one recognizable way: the checklist is ticked from memory, the rollback exists on paper, and support learns about the release from a customer. This skill walks Gate 5 one item at a time, demands evidence in the release candidate for each, and turns "mostly ready" into a conditional go whose conditions each have an owner and a close-by date, or into the no-go it actually is.

## Files this skill drives

- [../../templates/delivery/release-readiness.md](../../templates/delivery/release-readiness.md), the working document and the checklist in one place
- Gate 5 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md), whose eight items this skill walks in order
- Reads, as evidence: [../../templates/delivery/uat-plan.md](../../templates/delivery/uat-plan.md), [../../templates/delivery/testing-strategy.md](../../templates/delivery/testing-strategy.md), [../../templates/delivery/edge-cases.md](../../templates/delivery/edge-cases.md), [../../templates/delivery/failure-scenarios.md](../../templates/delivery/failure-scenarios.md), [../../templates/delivery/launch-comms-plan.md](../../templates/delivery/launch-comms-plan.md), [../../templates/operate/operational-readiness-review.md](../../templates/operate/operational-readiness-review.md)
- Overlays: [../../templates/ai/guardrails.md](../../templates/ai/guardrails.md) for model features; the [reg-gap-check skill](../reg-gap-check/SKILL.md) and [../../templates/operate/compliance-impact-assessment.md](../../templates/operate/compliance-impact-assessment.md) for regulated products
- Records: [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md) for the decision, [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md) for accepted known issues

## When to use

- Two weeks before a target date, as the first full run, and again at the gate itself
- After a slip, because evidence that was true a month ago may not be
- When a function wants to sign "with reservations" and nobody has written the reservations down
- Before any AI feature or regulated release, where the overlay items are mandatory

## Inputs

The filled release readiness document (drafts accepted; the gaps are the point), UAT results, the rollback rehearsal record, comms drafts per audience, and the on-call runbook. Ask for these when missing: the named decider who can say no-go; the Gate 4 misses carried forward and their decisions; the environment and date of the rollback rehearsal; the severity-1 defect list; and, for regulated products, the section 0 answers from Gate 2. Decision rule: if the pre-read was not circulated 48 hours ahead, reschedule the gate rather than walk the room through the document.

## Workflow

### 1. Confirm the frame

Decider named; sign-off owners named per function (a name, not a team); pre-read circulated; every claim to be shown in the release candidate, not on slides. Missing any of these, the gate does not open.

### 2. Walk the eight items

For each Gate 5 item, record the evidence seen, the verdict (pass, condition, or fail), and, for a condition, the owner and the close-by date:

1. **UAT exit criteria met**, with real users or named proxies, and every severity-1 defect closed. Evidence: the signed UAT plan and the defect list. Rule: an open severity-1 is a fail, not a condition.
2. **Rollback performed in pre-production**, with the time to roll back recorded. Evidence: the rehearsal record with date and environment. Rule: a rollback that was designed but never run is a fail; the rehearsal is the cheapest hour of the launch.
3. **Known issues listed**, each with a workaround or an accepted-risk sign-off. Evidence: the known-issues table. Rule: an empty table on a real product is a question, not a pass.
4. **Comms drafted and approved** for support, sales or field teams, and customers where applicable. Evidence: the drafts and the approver's name. Rule: unbriefed support is a condition whose close-by date falls before the release, never after.
5. **On-call knows, and the runbook exists.** Evidence: the runbook link and the on-call acknowledgment. Rule: a runbook nobody on call has read is a condition owned by the on-call lead.
6. **Every function signed its own line**: engineering, product, QA, support, and any others the readiness document names. Rule: a blank line is a no-go from that function until it is filled.
7. **AI overlay**, when a model ships: guardrails verified live in the release candidate, and the kill switch tested. Rule: a kill switch that was designed but never tested is a fail.
8. **Regulated overlay**: the Gate 2 section 0 answers are still true of the artifact that ships; any drift is written up and re-signed by the regulatory owner. Rule: drift without a re-signature is a fail.

### 3. Check the rollback trigger

The trigger is a condition a dashboard can show (an error rate, a latency, a failed reconciliation count), with an owner and the time to roll back. A trigger written as a feeling ("if things look bad") is a condition owned by the release owner, closed before release.

### 4. Decide

Apply the rules in order. Any fail: NO-GO, with the fails listed and the re-run date set. No fails and one or more conditions: CONDITIONAL GO, valid only while every condition has an owner and a close-by date; a condition missing either converts the verdict to NO-GO. No fails and no conditions: GO. The decider records the decision and the one-paragraph reason on the readiness document and on the gate form.

### 5. Record and follow through

Decision log entry with the decider named. Accepted known issues become risk register rows with the signer as risk owner. Each condition gets a check on its close-by date; an open condition at that check is a launch stop, not a re-date.

## Output format

1. Item table: | # | Gate 5 item | Evidence seen | Verdict (pass / condition / fail) | Condition owner | Close-by date |
2. Rollback line: trigger, owner, time to roll back, rehearsal date and environment
3. Decision: GO / NO-GO / CONDITIONAL GO, the decider's name, the reason paragraph, and for a conditional go the numbered conditions with owners and dates
4. Sign-off table copied from the readiness document, every row named and dated
5. The decision log entry and any risk register rows

## Failure modes this skill guards against

- **The checklist ticked from memory.** Every item needs evidence you can point at, shown in the release candidate.
- **Rollback on paper.** The industry's incident write-ups repeat this line; the rehearsal is not optional.
- **The conditional go with no owners.** A no-go wearing a smile; the conversion rule above removes it.
- **Support learns from customers.** Comms to support close before release, not after.
- **Team names on sign-off lines.** "Engineering" cannot be paged; a person can.
- **Overlay items skipped as not applicable, with no reason.** Write the reason, or run the overlay.
- **Re-dating conditions.** An open condition at its close-by date stops the launch.

## Exit gate

This skill runs Gate 5 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md), closing DELIVER and feeding OPERATE. It is done when the readiness document's exit gate boxes are honestly checkable, the decision is recorded with the decider's name, and every condition has an owner and a date.
