# Risk Matrix: Lantern Admin Console rollout

Fills [frameworks/execution/risk-matrix.md](../frameworks/execution/risk-matrix.md). Everything here is invented: Northstar Works, the Lantern Admin Console, and all people, dates, scores and amounts are ILLUSTRATIVE. The initiative and scoring are fictional and show the worksheet method rather than a real risk assessment.

**Owner:** Priya Nair, product manager · **Sponsor:** Mateo Ruiz, chief operating officer · **Date:** 2026-10-06

**Context, ILLUSTRATIVE:** Northstar Works is a fictional software company. Lantern Admin Console is a fictional internal product that gives support managers one place to review account access requests. Priya Nair is the product manager, Mateo Ruiz is the sponsor, and the named owners below are fictional team members. The initiative horizon is the twelve weeks before the pilot launch.

## What it is for

This worksheet scores the risks for the Lantern Admin Console pilot on one shared set of 1 to 5 likelihood and impact scales. It answers which risks need action before the pilot, which need Mateo's direct attention, and which can be accepted.

The scoring method is based on the probability and impact matrix as codified in the US military system-safety standard MIL-STD-882 (1969) and later in ISO 31000 (2009), explained here in the repository's own words. This is a standalone assessment because this initiative has no existing risk register using these scales.

## Run it when

- The pilot plan has been drafted and its material uncertainties need owners.
- The sponsor needs a clear threshold for personal escalation.
- The team needs to distinguish a likely delivery nuisance from a less likely but severe failure.
- The team has enough evidence to give each risk a written likelihood and impact basis.

**Skip it when:** the initiative is already covered by a risk register using a different scoring method. Running both methods would give the same event two scores and create a reconciliation problem.

## Inputs you need first

- The Lantern Admin Console pilot plan and its twelve-week horizon.
- The sponsor's stated appetite: Mateo Ruiz must be told personally about scores above 9.
- The premortem output, which identified the event rows below.
- Evidence for each likelihood and impact basis, including prior team experience, pilot research and delivery constraints.

## The worksheet

### Step 1: the scales

Likelihood is scored within the twelve-week pilot horizon.

| Likelihood | Definition used for Lantern |
|---|---|
| 1, rare | No precedent in this team's history |
| 2, unlikely | Has happened to teams like ours, not to us |
| 3, possible | Has happened to us in the last two years |
| 4, likely | Has happened to us in the last year, or early signs are already visible |
| 5, almost certain | A precondition is already true |

Impact is the worst credible outcome, using the highest of time, customers and commitments.

| Impact | Definition used for Lantern |
|---|---|
| 1, minor | Under a week of one team's time and no customer notices |
| 2, moderate | A sprint slips or a few customers notice, nothing breached |
| 3, significant | A milestone slips by more than a month, a customer commitment is breached, or there is a compliance finding |
| 4, major | A gate cannot pass this quarter, or revenue or a regulatory deadline is at risk |
| 5, severe | The initiative fails or the company faces a reportable incident |

Score arithmetic is:

**Likelihood x impact = score**

The possible range is:

**1 x 1 = 1** through **5 x 5 = 25**

| Likelihood, then impact | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 5 | 5 | 10 | 15 | 20 | 25 |
| 4 | 4 | 8 | 12 | 16 | 20 |
| 3 | 3 | 6 | 9 | 12 | 15 |
| 2 | 2 | 4 | 6 | 8 | 10 |
| 1 | 1 | 2 | 3 | 4 | 5 |

### Step 2: the bands and appetite lines

| Band | Score | What it requires | Review |
|---|---:|---|---|
| Low | 1 to 4 | Accept, signed by name in the register | Quarterly |
| Medium | 5 to 9 | A mitigation plan with a date | Monthly |
| High | 10 to 15 | A named owner, a trigger, and an active mitigation | Weekly |
| Critical | 16 to 25 | All of the above, plus escalation to the sponsor and a line on the next gate's agenda | Weekly, and at every status report |

Mateo Ruiz set these appetite lines for the initiative:

- Any risk with impact 5 is treated as Critical regardless of its multiplication result.
- Mateo Ruiz is told personally about every score above 9, meaning scores of 10 through 25.
- Security and compliance rows move up one band. No security or compliance row appears in this scoring sheet.
- The top-band rule requires a named owner and an observable trigger. A review date alone is not a trigger.

The appetite rule changes row 3 from High by arithmetic to Critical by impact:

**2 x 5 = 10, normally High, impact 5 moves it to Critical**

### Step 3: the scoring sheet

| # | Risk (event) | Category | L | Basis for L | I | Basis for I | Score | Band after appetite | Owner | Trigger | Response (mitigate / accept / transfer / avoid) | Review date |
|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|
| 1 | The identity-provider import fails during the pilot and access requests cannot be reviewed | Feasibility | 4 | Early test runs showed intermittent import failures, so an early signal is already visible | 3 | A milestone could slip by more than a month while the team restores the review flow | 4 x 3 = 12 | High | Elena Park, engineering lead | Import failure rate above 2 percent in any 30-minute period | Mitigate: add retry handling, a manual queue and an on-call owner | 2026-10-13 |
| 2 | Support managers do not use the console because the review flow is slower than their current process | Usability | 3 | A similar internal workflow was abandoned by our team within the last two years | 3 | The pilot milestone could slip by more than a month if usage is too low to validate the workflow | 3 x 3 = 9 | Medium | Jonah Bell, research lead | Fewer than 6 of 10 invited managers complete a review in the first pilot week | Mitigate: observe five sessions, remove the slowest step and retest before pilot expansion | 2026-10-20 |
| 3 | The console recommends approval for an access request that should be rejected | Value | 2 | This has happened to teams like ours, but not to our team | 5 | A wrong approval could create a reportable incident and cause the initiative to fail | 2 x 5 = 10 | Critical, by the impact-5 line | Elena Park, engineering lead | Any test case with a known rejection reason receives an approval recommendation | Avoid: require an explicit human decision and block recommendation-based approval until evaluation passes | 2026-10-09 |
| 4 | The engineer who owns the access-policy integration becomes unavailable | Feasibility | 2 | Similar teams have experienced this, but our team has not | 3 | The integration milestone could slip by more than a month | 2 x 3 = 6 | Medium | Elena Park, engineering lead | The owner is unavailable for 5 working days or more, or a handoff is incomplete | Mitigate: document the integration and pair a second engineer before pilot build | 2026-10-27 |
| 5 | Pilot participants do not represent the range of account-access requests seen by support | Value | 2 | Similar discovery efforts have had narrow participant samples, but this team has not had this failure | 2 | A few customers could notice a weak workflow, but no commitment would be breached | 2 x 2 = 4 | Low | Jonah Bell, research lead | Fewer than 3 request types appear in the first 20 pilot cases | Accept: record the sampling gap and review it quarterly; add a participant only if the trigger fires | 2026-12-15 |

**Residual scoring after the planned response**

Residual scores show what the mitigation is expected to leave behind. The arithmetic uses the same 1 to 5 scales, and the residual score is not a second method.

| # | Planned response | Residual L | Residual I | Residual arithmetic | Residual score | Residual band after appetite | What the residual means |
|---:|---|---:|---|---|---:|---|---|
| 1 | Retry handling, a manual queue and an on-call owner | 2 | 3 | 2 x 3 = 6 | 6 | Medium | An outage could still delay the milestone, but the manual queue limits the interruption |
| 2 | Observe sessions, remove the slowest step and retest | 2 | 3 | 2 x 3 = 6 | 6 | Medium | Low usage remains possible, but the team will have evidence before expansion |
| 3 | Human decision required and recommendation-based approval blocked | 1 | 4 | 1 x 4 = 4 | 4 | Low | A recommendation can still be wrong, but it cannot approve the request by itself |
| 4 | Integration documentation and a paired engineer | 1 | 3 | 1 x 3 = 3 | 3 | Low | A short absence should no longer delay the integration by more than a week |
| 5 | Accept the sampling gap and monitor request types | 2 | 2 | 2 x 2 = 4 | 4 | Low | The sample can still be narrow, but the trigger identifies the gap early |

## Reading the result

One of the five initial rows is in the Critical band and one is in the High band:

**2 rows in the top two bands / 5 total rows = 40 percent**

That is more than a fifth of the rows, so the plan needs another DESIGN review before the pilot is approved. The immediate action is to resolve row 3, then confirm that row 1's manual queue is usable.

The most urgent row is row 3. Its arithmetic score is 10:

**2 x 5 = 10**

The impact-5 appetite line makes it Critical, even though the multiplication result would otherwise place it in High. The sponsor, Mateo Ruiz, must be told personally, and the row belongs on the next gate agenda.

After mitigation, row 3 becomes:

**1 x 4 = 4, Low**

That residual is acceptable only because the response removes automatic approval and keeps a human decision in the flow.

No residual score is above 9:

**0 residual rows above 9 / 5 total rows = 0 percent**

The team should still run a premortem after the design changes, because the initial assessment had two rows in the top two bands, and rule one above sends the plan back to DESIGN before the residual scores can be trusted. The residual score of 0 is not itself a decoration signal; it is only the projected result of mitigations that have not yet been completed.

## ILLUSTRATIVE example

The Lantern Admin Console rows show five different outcomes from the same 1 to 5 method.

- Row 1 is High because the likelihood is 4 and the impact is 3: **4 x 3 = 12**.
- Row 2 is Medium because the likelihood is 3 and the impact is 3: **3 x 3 = 9**.
- Row 3 is Critical because the likelihood is 2 and the impact is 5: **2 x 5 = 10**, then the impact-5 line applies.
- Row 4 is Medium because the likelihood is 2 and the impact is 3: **2 x 3 = 6**.
- Row 5 is Low because the likelihood is 2 and the impact is 2: **2 x 2 = 4**.

The sponsor's appetite changes the treatment of row 3. Without the impact-5 line, its score of 10 would be High. With the line, the severe worst credible outcome requires Critical treatment and personal sponsor escalation.

The residual arithmetic shows the intended mitigation effect:

- Row 1 changes from **4 x 3 = 12** to **2 x 3 = 6**.
- Row 2 changes from **3 x 3 = 9** to **2 x 3 = 6**.
- Row 3 changes from **2 x 5 = 10** to **1 x 4 = 4**.
- Row 4 changes from **2 x 3 = 6** to **1 x 3 = 3**.
- Row 5 remains **2 x 2 = 4**, because the team chose acceptance rather than an active mitigation.

## The trap

Multiplication can hide the tail. A risk with likelihood 2 and impact 5 scores 10, while a risk with likelihood 4 and impact 3 scores 12. Without the impact-5 line, the severe event would look less urgent than the more likely delivery problem.

The impact-5 line fixes that distortion for this initiative. Row 3 is treated as Critical because its worst credible outcome is severe, not because its average outcome is likely.

The other trap is scoring without evidence. Row 1 has likelihood 4 because early test failures are already visible. Row 5 has likelihood 2 because similar teams have had narrow samples, but this team has not experienced the failure. The basis columns make those judgments reviewable.

A trigger is an observable signal that the event is starting to happen. For row 3, a test case receiving an approval recommendation despite a known rejection reason is a trigger. The next review date is not a trigger.

## Feeds

- [Risk register](../templates/execution/risk-register.md), if the initiative later adopts a register using these same scales
- [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), where the Critical row and its owner, trigger and review date are presented
- [Premortem worksheet](../frameworks/execution/premortem-worksheet.md), which supplied the event rows
- [Status report](../templates/execution/status-report.md), where row 3 is reported until its residual score is accepted
- Method background: [Cagan's four risks](../knowledge/cagan-product-teams.md)
