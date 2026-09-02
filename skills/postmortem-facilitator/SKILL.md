---
name: postmortem-facilitator
description: Facilitate a blameless incident postmortem: reconstruct the timeline from recorded sources, quantify impact, run five whys and a fishbone to reach causes the team can change, and leave with corrective actions that have owners, dates, and verification. Use when an incident qualifies for review under your severity policy, when a postmortem draft reads as a list of what people did wrong, when the same class of incident has recurred, or when a launch review found an operational failure it cannot explain. Takes the incident channel, alerts, logs, and the responder list; returns the filled incident postmortem template and the verified-action rows for the operational readiness review.
---

# Postmortem Facilitator: the same incident, made impossible

A postmortem fails when it finds a person. The room learns that showing up to an incident earns a paragraph with your name in it, the next incident's responders hide what they saw, and the document starts collecting fiction. This skill runs the review so that every cause is something the team can change, every action has a verification a reviewer can check, and the responders leave wanting to be in the next room.

## Files this skill drives

- [../../templates/operate/incident-postmortem.md](../../templates/operate/incident-postmortem.md), the document the review fills
- [../../frameworks/execution/five-whys-fishbone.md](../../frameworks/execution/five-whys-fishbone.md), the two cause-analysis worksheets
- [../../templates/operate/operational-readiness-review.md](../../templates/operate/operational-readiness-review.md), section 6, where verified actions that change how the service runs are copied
- [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md), which absorbs any cause the team decides not to fix, as an accepted risk with an owner
- Method background: the blameless discipline restates, in this repository's own words, the postmortem culture described in Google's SRE writing (2016) and Amazon's Correction of Error practice; five whys (Taiichi Ohno, Toyota Production System, 1978); the fishbone diagram (Kaoru Ishikawa, 1960s)

## When to use

- An incident met the severity bar in your policy, or breached a customer commitment
- A draft postmortem exists and reads as a list of who did what wrong
- The same class of incident has happened twice
- A post-launch review found operational pain nobody can explain

## Inputs

The incident channel or thread, the alert history, deploy and change logs, and the list of responders. Ask for these when missing: the severity definition used (the review needs the org's scale, not an adjective); the customer-facing impact source (a query, a support queue count, a dashboard); the on-call runbook that was in force; and a facilitator who was not a responder. Decision rule: the incident owner writes the document and a different person runs the review. A responder facilitating their own incident is the first blameless rule broken.

## Workflow

### 1. Set the rules out loud

Open the review with the two rules: everyone acted reasonably on the information they had, and the object of study is the system that handed them that information. No cause row will carry a person's name; roles ("the on-call engineer") are acceptable. State that the review is for learning and that the document is not a performance input. Say this every time, not only the first time.

### 2. Reconstruct the timeline from sources

Build the timeline before the meeting, from logs, alerts, and chat timestamps, never from memory. Each row: time with zone, what happened (an observation, not an interpretation), and the source link. Mark the four anchors: first impact, detection, mitigation, full resolution. Decision rule: a gap in the timeline longer than the time-to-detect target is itself a finding; ask what was happening and who knew. "We should have caught it" goes to the causes section, never into the timeline.

### 3. Quantify the impact

Users or accounts affected and how they were counted; what they experienced, in their words; business impact with numbers where they exist; commitments breached. Every number is labeled ILLUSTRATIVE or traced to the query that produced it. If the impact cannot be quantified, write why, and the inability becomes a corrective action about instrumentation.

### 4. Find the conditions, not the trigger

Run the five whys on the trigger until the answer is something the team can change: a pipeline stage, an alert threshold, a permission, a runbook, a design choice. Decision rule: stop when the next "why" leaves the team's control (a vendor's roadmap, human attention) and record the last controllable condition instead. Then run the fishbone across categories (process, tooling, alerting, documentation, design) to find the conditions the whys missed. An incident is almost never one cause; add rows until the incident could not have happened without each one. Ask "why was this possible", never "why did you do that".

### 5. Name what worked

At least one row. The runbook that held, the kill switch that killed, the escalation that was fast. These are behaviors to keep funding, and a review that lists only failures teaches responders that showing up earns criticism.

### 6. Write corrective actions with verification

One action per cause row, minimum. Each: the concrete change, the cause number, an owner by name, a due date, a verification method, a status. Decision rule: "be more careful" and "add a training" are not actions; an alert that fires in a drill, a canary stage in CI, and a removed permission are. The verification says how a reviewer will confirm the action landed. A cause the team decides not to fix goes to the risk register as an accepted risk with an owner and a review date, never silently dropped.

### 7. Close the loop

Track actions to verified. Copy verified actions that change how the service runs into section 6 of the operational readiness review. Schedule a check thirty days out; an open action at that check is escalated, not re-dated.

## Output format

1. The filled incident postmortem template: summary, severity, timeline table with sources, impact, cause table in systems language, what worked, actions table
2. The five whys chain and the fishbone, attached from the worksheet
3. Action tracker: | Action | Cause # | Owner | Due | Verification | Status | Copied to ORR section 6 (yes / no) |
4. Risk register rows for causes accepted rather than fixed

## Failure modes this skill guards against

- **The named cause.** A person in a cause row; the next incident's evidence goes missing.
- **Timeline from memory.** Reconstructed times that flatter the response. Sources only.
- **Stopping at the trigger.** "The deploy broke it" is where the analysis starts, not where it ends.
- **The uncontrollable root cause.** "Human error" as a finding. Keep asking until the answer is something the team can change.
- **Actions without verification.** "Improve monitoring" with no drill to prove it. An unverified action is the next incident's cause row.
- **The document-only review.** Circulated, never discussed; the responders never heard what worked.
- **Action decay.** Twelve open actions in the tracker three months later. The thirty-day check escalates rather than re-dates.

## Exit gate

The postmortem feeds Gate 6 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md), where operational load is reviewed, and its verified actions feed [../../templates/operate/operational-readiness-review.md](../../templates/operate/operational-readiness-review.md). Do not report it done until the template's exit gate boxes are honestly checkable, the review happened out loud with the responders present, and every action has an owner, a date, and a verification method.
