---
layer: templates
stage: DELIVER
gate: 5
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Release Readiness", "release-readiness"]
---
# Release Readiness: [product or feature name]

**Stage:** DELIVER (this file IS [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [launch-readiness](../../skills/launch-readiness/SKILL.md)

<!-- This is the go or no-go working document and the launch checklist in one place.
     The gate passes when every box below is honestly checkable, not when the meeting
     ends. A box you cannot check goes to the known-issues table with an owner, or it
     stops the release. Ticking a box to be polite moves the failure to production.

     Two rules about when this file is filled, because both are broken often
     and neither is recoverable afterwards. Fill it BEFORE the release, not
     during: a gate held after a flag was flipped is a record, not a decision.
     And fill it as you go through DELIVER rather than the night before, so
     the meeting reviews evidence instead of collecting it.

     Section 9 lists the ways this gate passes while the release is not ready.
     Read it once before the first go or no-go you chair. -->

**Release:** [version or milestone] · **Target date:** [YYYY-MM-DD]
**Decider:** [one named person] · **Decision:** GO / NO-GO / GO WITH CONDITIONS
**Decision date:** [YYYY-MM-DD] · **Held before any production rollout:** yes / no

## 1. Features

<!-- The second box is the one that catches real problems. Scope cut quietly
     during BUILD is the most common reason a release ships and does not move
     the metric it was justified by: the cut thing was the mechanism. List the
     cuts and check them against the PRD's objectives before ticking. -->

- [ ] Everything in the PRD's launch scope is built, and nothing extra shipped unreviewed
- [ ] Scope cuts since sign-off are listed here: [list, or "none"]
- [ ] Acceptance criteria all pass (Gate 4 evidence: [link or location])

## 2. Tests

<!-- "Ran and passed" is two claims, and the second is usually the one asked
     about. A suite that ran with failures triaged as known is not a pass; it
     is a known-issues row, and it belongs in section 3 with an owner. -->

- [ ] Every blocking level in the [testing strategy](testing-strategy.md) ran and passed
- [ ] The [edge-case register](edge-cases.md) has no open rows
- [ ] [UAT](uat-plan.md) is signed off, conditions listed below if any
- [ ] For AI features: eval thresholds met per the [eval spec](../ai/eval-spec.md), and the [red-team review](../ai/red-team-review.md) is closed

## 3. Known issues shipping with this release

<!-- An empty table on a real product is a red flag, not a green one. Every
     release of any size ships something known and imperfect; a blank table
     means the issues exist and are not written down, which is the same state
     with worse recall.

     "Why it is acceptable to ship" is the column that does the work. If it
     cannot be written in one sentence a support agent would accept, the issue
     is not acceptable, it is unexamined. -->

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| | | | | | |

## 4. Rollback

<!-- The trigger is agreed in advance because nobody agrees a rollback
     threshold during an incident: at that moment everyone is arguing about
     whether this is bad enough, and the arguing is the cost. A number decided
     while calm is what turns that into a reading.

     Tested means executed, in an environment, on a date, by someone who
     wrote down how long it took. A procedure that exists as a document has
     not been tested. -->

- [ ] Rollback procedure exists and was tested on [environment], on [YYYY-MM-DD]
- Rollback trigger, agreed in advance: [the condition that forces rollback, a number where possible]
- Rollback owner: [name] · Time to roll back: [n minutes]
- Data written between release and rollback: [what happens to it]

## 5. Operations and monitoring

<!-- The question this section is really asking: if this release breaks at
     three in the morning, does the person paged know it is this release, and
     can they see which part? A dashboard that shows system health but not
     this feature's behaviour will be green through the whole incident. -->

- [ ] Dashboards and alerts for this release are live (see [observability](../architecture/observability.md))
- [ ] [Failure scenarios](failure-scenarios.md) reviewed with the on-call owner
- [ ] The [operational readiness review](../operate/operational-readiness-review.md) is complete

## 6. Communications

<!-- Support is first in this table deliberately. They meet the release before
     anyone else does, and a support team that learns about a change from a
     ticket is the most reliable way to turn a small defect into a bad week. -->

| Audience | What they get | Owner | Sent |
|---|---|---|---|
| Support team | [briefing, known issues, escalation path] | | |
| Internal stakeholders | [release note] | | |
| Customers | [announcement or changelog, or "silent release"] | | |

## 7. Regulated overlay

<!-- Answer this even when the answer is no, and write the reason. A blank
     here reads as "not applicable" to the next reader and as "not considered"
     to an auditor, and only one of those is survivable. -->

- [ ] Does this release touch a product that contains an AI or machine-learning feature and has a financial or data regulator applying to it? If yes, the regulated module was run via the [reg-gap-check skill](../../skills/reg-gap-check/SKILL.md) and the [compliance impact assessment](../operate/compliance-impact-assessment.md) is signed. Both halves are required by the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); a regulated release with no model in it records what the regulatory owner used instead. If no, write why: [reason]

## 8. Sign-offs per function

<!-- A sign-off is a name, not a team. "Engineering" cannot be paged, cannot
     be asked what it meant, and cannot be found six months later.

     A conditional sign-off is a real and useful answer, and it is only worth
     anything if the condition is written in the row. A condition agreed aloud
     is a condition nobody will meet. -->

| Function | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| Product | | | | |
| Engineering | | | | |
| QA | | | | |
| Design | | | | |
| Support | | | | |
| Data | | | | |
| Legal / Compliance (if section 7 is yes) | | | | |

## 9. How this gate fails while looking like it passed

<!-- Every row below has happened at a real go or no-go. They are listed
     because in each case the document looked complete: the failure is not a
     missing section, it is a filled one that means nothing. Read this before
     chairing, not afterwards. -->

| Failure mode | What it looks like in the room | The rule that stops it |
|---|---|---|
| Rubber-stamp under date pressure | "We are fine, ship it", five times in five minutes, and nobody opens the runbook | Go criterion by criterion, pass or fail, recorded live rather than written up later |
| Empty known-issues table | A blank table presented as a clean result, with the real risks in direct messages | Do not accept the gate until the table is populated with severity, owner and mitigation |
| Rollback nobody tested | "We have a rollback plan" on a slide, no rehearsal, no timing | Require a rehearsal in a real environment, recently, with the elapsed time recorded |
| Sign-off by team, not person | "Engineering approves", written by whoever had the document open | Named sign-offs with role and date. A team cannot be paged or asked what it meant |
| Conditions agreed aloud | Everyone nods at "we will fix X first", and nothing is written | Conditions go in the sign-off row before the meeting ends, or the verdict is not conditional |
| Green dashboard, wrong metric | Every tile green while latency has tripled and the error budget is spent | Name the indicators tied to this release's user-visible behaviour, not only system uptime |
| Decider owns the ship date | The person holding the vote also owns the revenue number it affects | Declare it. Split the role for this gate, or record that the conflict was accepted and by whom |
| Gate held after the release | The meeting is on Friday, the flag was flipped on Tuesday, notes to be backfilled | The gate is held before any production rollout. There is no retroactive sign-off |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- A conditional go, which is the verdict people find hardest to write down
     properly. Delete it once this file holds a real release. -->

**Release:** *v2.4, receipt auto-extraction* · **Decision:** *GO WITH CONDITIONS* · **Decider:** *R. Ali, product lead*

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| *1* | *Extraction fails on receipts photographed in low light, and falls back to manual entry without telling the user why* | *medium* | *The fallback is correct and loses no data. The silence is confusing, not harmful, and affects a minority of submissions* | *S. Kaur* | *2026-06-12* |
| *2* | *Support runbook does not cover the fallback path* | *high* | *Not acceptable to ship. This is a condition, not a known issue* | *Support lead* | *before rollout* |

*Conditions recorded in the sign-off row: support runbook published and the support team briefed, both before the flag is enabled for any customer. Rollback trigger agreed in advance: manual-entry fallback rate above the pre-launch baseline for two consecutive hours, called by the on-call engineer without further discussion.*

The second row is the point. It was raised as a known issue and it is not one: nothing about it is acceptable to ship, so it became a written condition with a deadline before rollout. Known issues and conditions get confused constantly, and the difference is whether the release may proceed while it is open.

## Exit gate

<!-- Checkable by someone who was not in the meeting, which is the test of
     whether the gate is a gate. Each box is a fact about this file. -->

Gate 5 is green when:

- [ ] Every checklist box above is checked, or its exception sits in the known-issues table with an owner and a date
- [ ] The known-issues table is not empty, or the emptiness is explained
- [ ] Every known issue distinguishes itself from a condition: an issue may ship open, a condition may not
- [ ] The rollback trigger is a condition a dashboard can show, not a feeling, and the procedure was executed on a dated environment
- [ ] Every sign-off row has a name and a date, and every conditional verdict has its condition written in the row
- [ ] The decider recorded GO, NO-GO, or GO WITH CONDITIONS, with conditions in writing
- [ ] This gate was held before any production rollout, and the header says so
- [ ] Section 7 is answered even where the answer is no, with the reason written

Signed: [decider name], [role], [YYYY-MM-DD]
