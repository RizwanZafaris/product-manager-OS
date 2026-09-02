# Customer Comms: [product, release, or event name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md); reused in OPERATE for incidents and maintenance
Knowledge: [Knowledge index, SCR entry](../../knowledge/INDEX.md)
Skill: [gtm-launch-planner](../../skills/gtm-launch-planner/SKILL.md)

> **Delete any section you do not need.** A silent release needs no message; say so in [release-readiness.md](release-readiness.md) section 6 and delete this file. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- This file holds the messages themselves, per channel, with the approval
     chain each one passed through. Who hears when is launch-comms-plan.md; the
     facts every message derives from are release-notes.md section 1, or, for an
     incident, the timeline in ../operate/incident-postmortem.md. Each message
     follows Barbara Minto's situation, complication, resolution spine (SCR,
     1978, indexed in the knowledge layer): what is true, what changed, what we
     are doing and what you should do. Fill the facts block and the approval
     chain first; drafts written before the chain is agreed get rewritten by
     whoever was left out. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Facts every message derives from

<!-- Copy, do not retype. Change a fact here, then re-derive every message;
     never patch one channel. -->

| Field | Value |
|---|---|
| Event type | [launch / change / deprecation / maintenance / incident / cutover freeze] |
| What is true for the customer, in one sentence | [sentence] |
| What they must do, if anything | [action, deadline; or "nothing"] |
| When | [dates, times, timezone] |
| Who is affected | [segment, plan, region; or "all"] |
| Source document | [release-notes.md, migration-cutover-plan.md, or postmortem id] |

## 2. Approval chain

<!-- One row per message. Legal or compliance is named when personal data,
     money, or a regulator is touched; "consulted" without a name is not an
     approval. -->

| Message | Drafted by | Reviewed by (support, product, legal or compliance where needed) | Approved by | Approved on |
|---|---|---|---|---|
| In-app | | | | |
| Email | | | | |
| Status page | | | | |

## 3. In-app message

<!-- Short. The customer is in the middle of something. Name the trigger that
     shows it, who sees it, and when it stops showing. -->

- Trigger and placement: [page or moment; banner, modal, or inline]
- Audience rule: [segment or flag]
- Shows from: [date] · Stops: [date or condition]
- Text: [the message, in the customer's words, with one action link]
- Dismissal and frequency: [once, per session, until acted on]

## 4. Email

<!-- The subject line states the change, not the excitement. One action per
     email. If the reader must do nothing, say that in the first line and keep
     it short. -->

- Segment and list source: [where the recipient list comes from, who pulls it, checked against unsubscribes]
- Send time: [date, time, timezone; after support is briefed]
- Subject: [line]
- Body:

> [Situation: what is true today. Complication: what is changing and when. Resolution: what we are doing and what you should do, with one link.]

- Reply-to and where replies are triaged: [address, owner]

## 5. Status page

<!-- For incidents, maintenance, and cutover freezes. Written now, while calm.
     The update cadence is a promise; keep it or say why not. -->

| Stage | Text (drafted now) | Posted by | Update cadence |
|---|---|---|---|
| Scheduled or investigating | [text] | | [every n minutes until resolved] |
| Identified or in progress | [text] | | |
| Monitoring | [text] | | |
| Resolved | [text, including whether a postmortem will be published] | | |

## 6. Holding statement and rollback wording

<!-- If the rollback trigger in release-readiness.md fires, this goes out with
     names already on it. Two sentences, no root cause claims before the
     postmortem. -->

- Holding statement: [two sentences]
- Approved by: [name] · Sent by: [name] · Sendable within: [agreed time]
- If customer data was affected: [additional obligations and who confirms them; route to ../operate/compliance-impact-assessment.md where a regulator is in scope]

## 7. Support brief

- Support has the messages, the FAQ, and the macro ids before any send: [yes, date, by whom]
- Expected inbound and the answer: [top three questions, from support-runbook.md]
- Feedback route: [where replies and reactions are collected; feeds ../operate/post-launch-review.md]

## Exit gate (feeds Gate 5: release readiness green)

Approved messages satisfy the "comms are drafted and approved" line at [Gate 5](../../os/STAGE-GATES.md) and fill section 3 of [launch-comms-plan.md](launch-comms-plan.md) with linked drafts.

- [ ] Section 1 is filled and every message can be traced to it line by line
- [ ] Every message has a named approver and a date, with legal or compliance named where data, money, or a regulator is touched
- [ ] Every message states what the customer must do, or says plainly that nothing is required
- [ ] The status page texts and the holding statement exist before the event, not after
- [ ] Support is briefed before any external send is scheduled
- [ ] Signed by [name], [date]
