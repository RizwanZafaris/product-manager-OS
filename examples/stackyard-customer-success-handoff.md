# Customer Success Handoff: Stackyard scheduled cycle counts

Fills [templates/operate/customer-success-handoff.md](../templates/operate/customer-success-handoff.md). Everything here is invented for this standalone example: Stackyard is a fictional stock-count product for warehouses and parts distributors, Millbrook Systems its fictional vendor, and every account, person, number and date is ILLUSTRATIVE, not drawn from any real company or customer. There is no journey or data sheet behind it. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**Product owner:** Mateo Rinaldi, Product Manager · **Release:** Stackyard 7.0, scheduled cycle counts · **Launch date:** 2026-11-17 (wave 1), 2026-11-24 (wave 2)
**Receiving customer success lead:** Ruth Okafor, Director of Customer Success · **Receiving support lead:** Hollis Brandt, Support Lead · **Handoff meeting held:** 2026-11-03, two days before the Gate 5 meeting
**Health score status:** validated on the 2026-07-14 back-test, run on mid-market and enterprise accounts scored together over eight quarters, 31 non-renewals among 262 renewal events (ILLUSTRATIVE), which clears the [customer health score](../frameworks/metrics/customer-health-score.md) floor of 30; unvalidated for self-serve, whose usage was not tracked per account before 2026-05, so no back-test window exists yet and self-serve accounts are not banded in section 4
**Launch facts source:** the Stackyard 7.0 copy of the [launch comms plan](../templates/delivery/launch-comms-plan.md), section 1, owned by Mateo Rinaldi

## 1. What changed for customers

| # | Change | Who sees it (segment, plan, rollout wave) | What the customer must do differently | Removed or moved, and when | Reaches them on |
|---|---|---|---|---|---|
| C1 | Cycle counts can be scheduled in the app by zone and frequency, and close with a variance report | All segments; enterprise and mid-market in wave 1, self-serve in wave 2 | Set up a schedule once per site, about 10 minutes per site (ILLUSTRATIVE, from beta timings) | Nothing removed | 2026-11-17 and 2026-11-24 |
| C2 | The CSV count-list import is retired; recurring imports move to schedules or to the counts API | All segments | Move any recurring CSV import to a schedule, or to the API endpoint for ERP-driven lists | The CSV import screen and endpoint stop working on 2027-01-17 | Notice 2026-11-17; removal 2027-01-17 |
| C3 | The variance report moves from Reports to the count itself | All segments | Nothing; the old link redirects | Old location redirects until 2027-03-01 | 2026-11-17 |
| C4 | Counts are assigned to handheld app users by zone | Mid-market and enterprise accounts with handheld licences | Assign zones to counters once | Nothing removed | 2026-11-17 |

No cancel, downgrade or consent flow is touched by this release, so no choice symmetry audit was required.

## 2. Adoption plan per segment

| Segment | Accounts | Adoption event (the action that counts) | Target share and date | Motion | Owner | How we know (metric id) |
|---|---|---|---|---|---|---|
| Self-serve Starter | 410 | First scheduled count completed, closed with its variance report | 40 percent of accounts by 2026-12-31 (ILLUSTRATIVE) | In-app guide on the Counts page, three-email sequence | Ines Halloran, Lifecycle Marketing | M-CC-ADOPT-SS |
| Mid-market, pooled CSM | 120 | Same event | 60 percent of accounts by 2026-12-31 (ILLUSTRATIVE) | Two live webinars, CSM follow-up email to non-adopters after two weeks | Dara Quist, CS Manager, mid-market | M-CC-ADOPT-MM |
| Enterprise, named CSM | 18 | Same event, at every site the account counts | 15 of 18 accounts by 2027-01-10, a week before C2 lands (ILLUSTRATIVE) | One admin enablement session per account | Tomas Ellery, CS Manager, enterprise | M-CC-ADOPT-ENT |

The adoption event is the beta's working choice, not a measured one. [OPEN: Part 1 of the [activation and churn diagnosis](../frameworks/metrics/activation-churn-diagnosis.md) cannot run until a post-launch cohort is eight weeks old; check "first scheduled count completed" against week-8 retention by 2027-01-31. Owner: Priya Varma, Product Analyst.]

**Accounts that need a hands-on session before the change reaches them:** the 7 enterprise accounts (ILLUSTRATIVE) whose CSV imports are driven by a script or an integration rather than by a person, listed by Tomas Ellery from the import logs on 2026-10-30, because C2 breaks their process silently on 2027-01-17 whatever they do in the app.

## 3. Health-score signals this launch moves

| Signal (id from the health score) | Expected direction and size | Mechanism | For how long | What CS does about it | Re-back-test needed? |
|---|---|---|---|---|---|
| H2 core-action trend (counts closed per active seat per week) | Down 10 to 25 percent for two to three weeks (ILLUSTRATIVE, from the beta) | Accounts pause CSV imports while they build schedules | Until 2026-12-15 | Suppress the Falling flag for accounts whose H2 drop starts within 7 days of their wave date; read every suppressed account on 2026-12-15 | Yes, scheduled 2027-02-15: a scheduled count and an imported count both count as the core action now, and they run at different frequencies |
| H3 support friction | Up, about one extra ticket per account in the first three weeks (ILLUSTRATIVE) | Setup questions | Until 2026-12-08 | Exclude tickets tagged cycle-count-setup at severity S3 or S4 from H3 until the end date; S1 and S2 tickets still count | No; the signal's definition does not change |
| H1 seat activation | Up slightly for accounts with handheld counters | Zone assignment brings counters into the app | Lasting | No change | Covered by the 2027-02-15 back-test |
| H5 sentiment | No change expected | | | No change | No |

## 4. Renewal-risk accounts

**Window:** renewals between 2026-11-17 and 2027-03-31

| Account | Segment | Renewal date | Band and score (as of date) | Why at risk from this launch | Play | CS owner | Play starts by |
|---|---|---|---|---|---|---|---|
| Pellow Distribution | Enterprise | 2026-12-31 | Amber, 58, 2026-11-02 | Nightly CSV imports from its ERP for 12 sites; C2 removes that path 17 days after renewal | Migration session with a Millbrook solutions engineer to move the ERP feed to the counts API before renewal | Tomas Ellery | 2026-11-10 |
| Garnet Cold Store | Mid-market | 2027-01-31 | Red, 36, 2026-11-02 | Already at risk: the executive sponsor left in September. The launch adds setup work at both sites | Executive call with the new operations director, then a guided schedule setup | Dara Quist | 2026-11-12 |
| Ashby Trade Supplies | Mid-market | 2027-02-28 | Amber, 47, 2026-11-02 | Builds count lists in spreadsheets and imports them weekly; C2 | Webinar seat plus a one-to-one setup call | Dara Quist | 2026-11-24 |
| Northcote Spares | Enterprise | 2027-03-15 | Green, 74, 2026-11-02 | Imports through a third-party integration, the fictional Bayline Connect, that uses the CSV endpoint; it breaks on 2027-01-17 whatever the band says | API migration notes to the integration partner; extended CSV access to 2027-03-31 if the partner slips, approved by Ruth Okafor | Tomas Ellery | 2026-11-17 |
| [OPEN: self-serve accounts renewing in the window whose CSV imports are scheduled by a script. Support operations to pull the list from import logs by 2026-11-20. Owner: Ines Halloran] | Self-serve | | Not banded (score unvalidated for this segment) | C2 | Targeted email with the API guide, then a support callback offer | No account owner; Ines Halloran owns the email | 2026-11-24 |

## 5. Self-serve and help-centre content plan

| Content | Question it answers, in the customer's words | Format | Linked from (surface) | Owner | Published by |
|---|---|---|---|---|---|
| KB-1 Set up a recurring count | Runbook S-1: "I can't find where to import my count list" | Article and in-app tip | Banner on the old import screen; the Counts page | Lena Marsh, Support Content | 2026-11-14 |
| KB-2 Import files are no longer accepted | Runbook S-2: "my import file keeps getting rejected" | Article | The import error message from 2027-01-17 | Lena Marsh | 2027-01-10 |
| KB-3 Counts assigned by zone | Runbook S-3: "a counter got a count I never gave them" | Article | Zone assignment screen | Lena Marsh | 2026-11-14 |
| KB-4 Where the variance report went | Runbook S-4: "where is my variance report" | In-app tip | The old report link's redirect | Ines Halloran | 2026-11-17 |
| KB-5 Schedule your first count | The first-run question, from beta sessions | Three-minute video | Step 1 of the in-app guide | Ines Halloran | 2026-11-17 |

Waiver: German and Dutch versions of KB-1 to KB-3 publish on 2026-12-05, after wave 2. Waived by Hollis Brandt, Support Lead, on 2026-11-03, because the 9 accounts (ILLUSTRATIVE) using those locales are mid-market, and Dara Quist's team will walk each through setup in person.

- **Deflection rate definition:** self-served sessions resolved without a ticket / (those sessions + tickets), on topics tagged cycle-count, over 2026-11-17 to 2027-01-31
- **A self-served session means:** a help-centre article view or an in-app help open on a cycle-count topic, counted once per user per topic per day; the support bot is not live for this topic, so bot conversations are not counted
- **"Resolved without a ticket" means:** a help-centre or in-app help session on a cycle-count topic with no ticket from the same user on a cycle-count topic within 7 days; a reopened ticket counts as a ticket
- **Baseline:** 46.0 percent (ILLUSTRATIVE), from the CSV import topic over the third quarter of 2026: 1,150 sessions resolved without a ticket and 1,350 tickets, so 1,150 / (1,150 + 1,350) = 46.0 percent · **Target:** 55 percent (ILLUSTRATIVE) by 2027-01-31
- **Counter-metrics:** CSAT on cycle-count tickets at or above the third-quarter support-wide 80 percent (ILLUSTRATIVE), on the 1 to 5 scale with 4 and 5 counted as satisfied; repeat-contact rate, same user and topic within 14 days, at or below 12 percent (ILLUSTRATIVE)

## 6. Support macros and escalation path

| Macro id | Situation it is sent in | Approved wording (customer comms draft or macro tool) | Written or rewritten by (queue owner) | Last reviewed |
|---|---|---|---|---|
| M-CC-01 | Customer asks where the CSV import went, after 2027-01-17 | Customer comms draft CC-EMAIL-3, in the macro tool | Femi Adeyemi, tier 1 queue owner | 2026-11-02 |
| M-CC-02 | Customer asks how to schedule a count | Links KB-1 and KB-5 | Femi Adeyemi | 2026-11-02 |
| M-CC-03 | A counter received a count nobody assigned to them | Links KB-3; asks for the zone name and site | Femi Adeyemi | 2026-11-02 |
| M-CC-04 | Customer asks for more time before the CSV import is retired | Routes to the account owner; promises no date | Femi Adeyemi | 2026-11-02 |

- **Technical escalation:** per the Stackyard 7.0 copy of the [support runbook](../templates/delivery/support-runbook.md), section 4, severity ids from the [testing strategy](../templates/delivery/testing-strategy.md) ladder
- **Product contact for "bug or design choice" questions:** Mateo Rinaldi, the cycle-counts product channel, weekdays 09:00 to 17:00 UK time
- **Commercial or contract questions caused by the change:** the account owner; extended CSV access is approved only by Ruth Okafor, and only to 2027-03-31
- **When a renewal-risk account escalates:** the section 4 CS owner is told within 4 working hours by the support lead on shift

## 7. Feedback loop back to product

- **Where it lands:** evidence notes tagged cycle-count-2026-11, written by the support lead on shift and synthesised with everything else through the [feedback-synthesis](../skills/feedback-synthesis/SKILL.md) skill
- **Who reads it, how often:** Mateo Rinaldi, at a Tuesday triage every week to 2026-12-29, then in the monthly metrics review
- **What makes product act:** 10 or more tickets on one runbook symptom row in a week (ILLUSTRATIVE); any section 4 account naming the launch as a reason; any churn coded to C2 in the churn tally
- **How CS and support hear back:** a section in the weekly CS digest, "what changed because of what you sent", owned by Mateo Rinaldi
- **Standing program, if any:** none; the 12-account beta panel (ILLUSTRATIVE) closed at launch and its members moved to their normal CS owners

## 8. How this handoff fails

Checked at the 2026-11-03 handoff meeting against the template's table:

| Failure | Checked how in this handoff |
|---|---|
| Handoff by forwarded release note | Both receiving leads attended; the meeting date is in the header and precedes Gate 5 |
| Adoption target is "usage" | Every segment has an event, a dated target and a metric id; the event itself is flagged OPEN in section 2 |
| Save plays on accounts that are only switching over | H2 and H3 suppression windows have end dates |
| Real risk hidden inside the suppression window | Every suppressed account is read on 2026-12-15, and Ruth Okafor owns that read |
| The CRM red list relabelled as launch risk | Every section 4 row names a section 1 change; Garnet Cold Store's row says plainly the risk predates the launch |
| Deflection bought by hiding the contact route | The contact button stays on every KB article; CSAT and repeat contacts sit beside the target |
| Help content in product vocabulary | Every KB item maps to a runbook symptom row; Hollis Brandt reviewed all five |
| A feedback loop with no reader | Mateo Rinaldi holds the Tuesday slot to 2026-12-29 |

## Exit gate

Feeds [Gate 5: release readiness green](../os/STAGE-GATES.md) through the support row of section 6 of the Stackyard 7.0 copy of [release readiness](../templates/delivery/release-readiness.md), alongside its launch comms plan.

- [x] Every section 1 row says what the customer must do differently and what is removed or moved, with a date
- [x] Every section 2 segment has an adoption event that is an action, a target share with a date, an owner, and a metric id (the event's validation is an OPEN item due 2027-01-31)
- [x] Every section 3 signal has an expected direction, an end date for any suppression, and a yes or no on re-back-testing
- [ ] Section 4 covers every account renewing in the stated window that is red, amber, or losing a workflow, each with a CS owner and a start date, and the header states whether the health score is validated (Not yet: the self-serve script-import accounts are an OPEN row due 2026-11-20. Carried into release readiness as a condition with that date, owner Ines Halloran)
- [x] The deflection rate is written with its formula, what counts as a session, its window, its not-deflected rule, a baseline, a target, and at least one counter-metric
- [x] Every macro links approved wording and names the queue owner who wrote or rewrote it
- [x] The escalation routes name people, and the technical route matches the support runbook's section 4
- [x] The feedback loop names a reader, a cadence, a trigger for product action, and how CS hears back
- [x] Both receiving leads are named in the header and the handoff meeting date is before the Gate 5 meeting

Signed: Mateo Rinaldi, Product Manager, 2026-11-04
