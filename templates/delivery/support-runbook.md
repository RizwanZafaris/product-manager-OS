# Support Runbook: [product or feature name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md); maintained through OPERATE
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [release-manager-agent](../../agents/release-manager-agent.md)

> **Delete any section you do not need.** A change with no new customer-visible behavior needs one row in the known-issues table of an existing runbook, not a new file. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- This is the document a support agent opens with a customer on the line. It
     starts from what the customer says, not from what the system does. The
     engineering runbooks (restart, failover, restore) are listed in
     ../operate/operational-readiness-review.md section 2; how the system breaks
     and recovers is failure-scenarios.md; the wording support may send is
     customer-comms.md. This file joins them from the customer's side: symptom,
     diagnosis, workaround, escalation. Fill the symptom table and the
     escalation table first; the rest can grow after launch. New rows arrive
     from ../operate/incident-postmortem.md corrective actions and from the
     support section of release-notes.md. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Support lead who reviewed it:** [name] · **Next review:** [YYYY-MM-DD]

## 1. What this feature does, for a responder

<!-- One block a new support agent can act on. Name the surfaces, the identifier
     a customer can read out, and where the corresponding record lives. -->

- What it does, in one sentence: [sentence]
- Surfaces it appears on: [web, mobile, email, API, integration]
- Identifier to ask the customer for: [what it is called on screen, where they find it]
- Where that identifier is looked up: [admin tool, log search, dashboard, with the link]
- Who has it: [segments, plans, cohorts if the rollout is staged]

## 2. Symptoms

<!-- One row per thing a customer would say, in their words. "Likely cause" is
     the usual one, not the only one; the first check is what separates the
     causes. The italic row is an invented example on the expense copilot. -->

| # | Symptom, as the customer reports it | Likely cause | First check | Workaround or answer | Escalate if |
|---|---|---|---|---|---|
| | | | | | |
| *S-1* | *"the copilot filled in the wrong merchant on my receipt"* | *low-confidence extraction accepted without review* | *open the receipt record; check the confidence flag* | *edit the merchant field; say honestly that the correction does not retrain anything* | *more than [n] reports from one customer in a day* |

## 3. Diagnosis steps

<!-- Numbered steps per symptom class, each ending in a decision: resolved,
     workaround applied, or escalate with the evidence below. Collect the
     evidence before escalating; an escalation without it comes straight back. -->

### Symptom class: [name]

1. [step: what to open, what to look at]
2. [step: what distinguishes cause A from cause B]
3. [decision: resolve with X / apply workaround Y / escalate with the evidence table]

**Evidence to collect before escalating**

| Item | Where to find it | Why engineering needs it |
|---|---|---|
| [record id, timestamp with timezone, screenshot, app version, steps to reproduce] | | |

## 4. Escalation

<!-- Severity definitions belong to your org; copy them here so nobody looks
     them up mid-call. Response expectations are fields agreed with the team
     that will be paged, never assumed. Names, not teams. -->

| Severity | Definition for this feature | Escalate to (name) | How (channel, pager) | Expected first response | What to include |
|---|---|---|---|---|---|
| Sev 1 | [e.g. no customer can submit] | | | [agreed time] | [section 3 evidence plus customer count] |
| Sev 2 | | | | [agreed time] | |
| Sev 3 | | | | [agreed time] | |

**After hours:** [what changes, who is reachable]
**Product owner for "bug or design choice" questions:** [name, channel]

## 5. Known issues

<!-- Copied from the readiness document at launch, then maintained here. An
     issue with no fix date is a permanent limitation and should say so; move it
     to section 1 as a fact about the feature. -->

| Id | Issue | Who is affected | Workaround | Approved wording (macro id or customer-comms.md link) | Fix owner | Fix date | Source |
|---|---|---|---|---|---|---|---|
| KI-1 | | | | | | | [release-notes.md section 4 / postmortem id] |

## 6. What support may and may not say

<!-- The lines that keep a hard call from becoming a commitment the team cannot
     keep. Wording lives in customer-comms.md; this section is the boundary. -->

- May confirm: [what is safe to state as fact]
- May offer: [workarounds, credits within a stated authority, escalation]
- May not promise: [fix dates not in section 5, refunds above authority, root causes not yet confirmed]
- Anything involving personal data or a regulator: [route to name; see ../architecture/privacy-impact-assessment.md and ../operate/compliance-impact-assessment.md]

## 7. Maintenance

- Reviewed after every incident touching this feature: [yes, by name]
- Rows added from postmortems since launch: [count, with ids]
- Retired rows: [ids and dates, so the history stays visible]

## Exit gate (feeds Gate 5: release readiness green)

A reviewed runbook satisfies the "runbook for it exists" line at [Gate 5](../../os/STAGE-GATES.md) and the support row in section 6 of [release-readiness.md](release-readiness.md).

- [ ] Every symptom row is written in the customer's words and ends in a workaround or an escalation rule
- [ ] Every diagnosis path ends in a decision, and the evidence list exists
- [ ] Every escalation row names a person, a channel, and an agreed response expectation
- [ ] Every known issue from the readiness document is here with a workaround and approved wording
- [ ] The support lead has read it and is named above
- [ ] A next review date is set
- [ ] Signed by [name], [date]
