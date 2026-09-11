# Incident Postmortem: HG-INC-14, the rehearsal that ate the settlement file

Fills [templates/operate/incident-postmortem.md](../templates/operate/incident-postmortem.md). Part of the [Harbourgate journey](harbourgate-journey.md): a fictional mid-market retailer replacing a nine-year-old checkout with a single-provider payment service, Quay. Everything here is invented: Harbourgate, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date and log line is ILLUSTRATIVE, drawn from the journey's data sheet and identifier table, never to be copied as a target. See the [examples index](README.md).

**Incident owner (writes this doc):** Bea Lindqvist, Senior Engineer, Payments · **Facilitator (runs the review):** Noor Haddad, QA Lead
**Incident date:** 2026-06-15 · **Review date:** 2026-06-17 · **Status:** actions verified

## 1. Facts, severity, and timeline

- One-sentence summary: a scheduled job left running in the pre-production environment read and deleted the live Marlowe settlement file two days after the rehearsal it was built for was aborted, and finance's daily close ran nearly six hours late with nobody paged.
- Severity: 3 of 4 on Harbourgate's scale · Duration from first impact to full resolution: 5 hours 40 minutes (N41)
- Detected by: an employee noticed, not an alert; a finance analyst saw the Marlowe reconciliation dashboard sitting empty at the start of the working day. That absence of an alert is itself a finding, addressed below as cause 4.
- Systems and features involved: the pre-production rehearsal environment (cutover rehearsal 1), the shared Marlowe SFTP settlement drop (I-6), the production ingestion job, and finance's daily reconciliation close

This incident sits two days downstream of a different failure. Rehearsal 1, run on 2026-06-13 against D-019's one-weekend cutover plan, aborted at 9 hours 10 minutes when 1,529 of 1,742 lines in a real Marlowe settlement file would not match Quay's reconciliation (N37). The rehearsal's own abort did not touch the scheduling layer, and its ingestion job, still enabled and still holding the only credentials Marlowe issues, ran again on its normal daily schedule.

| Time (with zone, Europe/London) | What happened | Source (log, alert, chat link) |
|---|---|---|
| 06:30 | Marlowe's real settlement file for the weekend lands on the shared SFTP drop, on schedule (N33) | Provider file specification; SFTP transfer log |
| 07:00 | The pre-production ingestion job, left enabled since rehearsal 1's abort on 2026-06-13, polls the shared drop, downloads the file, and deletes it on read as its normal success behaviour | Pre-production job run log |
| 08:10 | A finance analyst finds the Marlowe reconciliation dashboard empty for the day and posts in the #finance-ops channel | #finance-ops channel |
| (time not recorded) | Bea Lindqvist traces the read to the pre-production job's credentials and opens a ticket with Marlowe support requesting a re-send | Ticket MRL-88213 |
| 2 h 10 min after the ticket (N69) | Marlowe support responds, within their 4-hour queue SLA, confirms the original file, and reissues it to the drop | Ticket MRL-88213 |
| 12:40 | The reissued file is ingested through the production path; finance completes the daily close | Finance close log |

The incident record does not show when the pre-production schedule was disabled, or whether it was disabled at all before 2026-06-15's run. The systematic fix, disabling every pre-production schedule as part of any future abort, is corrective action A5, added to the checklist on 2026-06-19 (section 5); A2's split of the SFTP drop by environment, verified 2026-06-26, removed the job's reach to the production drop regardless of its schedule.

## 2. Customer and business impact

- Users or accounts affected: none directly. No customer-facing payment failed: no cohort had shifted onto Quay by 2026-06-15, the first cohort (Marlowe, 5%) did not begin until 2026-07-13, so every order still authorised and captured through checkout-pay's existing Kestrel, Marlowe and Tidewater integrations, unaffected by a failure inside a pre-production environment. The impact fell entirely on Harbourgate's own finance operation.
- What they experienced, in their terms: nothing visible to a shopper. Internally, finance operations worked from an empty Marlowe reconciliation view for most of a morning and could not confirm the day's Marlowe settlement position until early afternoon.
- Business impact: the daily close ran 5 hours 40 minutes late; 5,190 settlement lines and £332,000 in settled value were reconciled late (N42). No SLA credit applied, because the delay fell inside a provider relationship rather than a customer contract. Rehearsal 1's verify failure also cost the cancelled 2026-06-27 cutover weekend (D-020), booked under N43 as a cost of D-019's failed hypothesis, not of this incident.
- Commitments breached: none against a customer or Kestrel. Marlowe's own 4-hour support response commitment (N69) was met, at 2 hours 10 minutes. The reconciliation tolerance in N35 (£50 per provider per day) was not itself breached, since the reissued file matched once it arrived; what breached was the timing of the close, not its accuracy.

## 3. Contributing causes

Under D-020, this postmortem covers both rehearsal 1's failure and the file deletion it led to: rehearsal 1's verify failure is cause 1's consequence, and the abort path that left the job running is cause 5.

| # | Contributing cause (systems language) | Why it was possible | Category |
|---|---|---|---|
| 1 | Reconciliation had no way to classify a line that straddled the cutover: authorised on one path, settled after the other had taken over | Quay's reconciliation logic was built for a clean handover, not for a settlement lag of up to three days and refunds lagging months, so it either matched a line or rejected it, with nothing in between; the resulting verify failure aborted rehearsal 1, and the abort path (cause 5) left the ingestion job running for two days until it consumed the production file | design |
| 2 | The dependency for a Marlowe sandbox settlement file sat at "requested" for eight weeks with no automatic escalation, so the rehearsal had no safe substitute for the real file | The dependency register (DEP-2) tracked status but nothing compared its age against a threshold; a stale row and a fresh one looked the same | process |
| 3 | Pre-production and production shared one SFTP drop and one set of Marlowe credentials, so a pre-production job could read, and delete, the live file | The drop predates BUILD: the STRIDE walk of 2026-04-08, in DESIGN, already found it shared between pre-production and production, on the assumption that Marlowe's single-credential model meant a single environment; this was finding F2, scored 4, and sent to backlog item HG-812 rather than the risk register, so nobody scheduled the fix before rehearsal 1 needed it | tooling |
| 4 | The pre-production job deleted the source file on read as its normal success behaviour, and no alert existed for a missing settlement file | The job was written against the happy path, before a rehearsal environment shared the drop with production; a missing-file page was never in scope because until rehearsal 1, nothing had ever made the file go missing. A2's later split of the SFTP drop by environment makes the delete-on-read behaviour moot for production, since a pre-production job can no longer reach the production file at all; the production ingestion job's separate gap, treating an empty poll as success rather than paging, is closed by A4 | alerting |
| 5 | The rehearsal's abort checklist stopped the rehearsal but did not disable the pre-production environment's own job schedule | The checklist from D-019's plan covered rolling back the migration steps, not the scheduling layer underneath them, because nobody had modelled an abort that left infrastructure running unattended for two calendar days | process |

Cause 1 is R9 (lines authorised on the legacy path and settled after a shift go unmatched, added 2026-06-16), mitigated by ADR-0004's straddle-set logic and open until the last drain. Cause 2 is the register's own history: [harbourgate-dependency-register.md](harbourgate-dependency-register.md) shows DEP-2 requested on 2026-04-20 and still open on 2026-06-11, more than three weeks past the four-week threshold that A6 later added (dependency register, section 4). Cause 2 is also risk R3 (Marlowe issues no sandbox files, so reconciliation is tested against production), raised at a score of 4 with the mitigation "read the production drop with the keep flag," a mitigation this incident shows was the risk, not the fix; R3 was re-scored the day this incident occurred and closed 2026-07-03, once ADR-0004 removed the need for a sandbox file (A1). Cause 3 is finding F2 in [harbourgate-security-architecture.md](harbourgate-security-architecture.md), and it is also risk R14: scored at the STRIDE walk, routed to a backlog item instead of the risk register, added to the register only after it had already occurred (2026-06-16, the day after this incident), scored at 9, and closed 2026-06-26 once the SFTP drop was split (A2).

## 4. What worked

- Finance's own vigilance closed most of the detection gap the missing alert left open: a person noticed an empty dashboard within roughly an hour of the file disappearing, well inside a working morning, even with nothing paging anyone.
- Bea Lindqvist's standing relationship with Marlowe's merchant support meant the re-send ticket went in quickly once the read was traced, and Marlowe answered well inside their own SLA (N69: 2 hours 10 minutes into a 4-hour window) rather than at its edge.
- Because no cohort had shifted onto Quay by 2026-06-15, every order still ran on its original provider rail through checkout-pay, so no order failed and no customer saw anything. The blast radius stayed inside a back-office process precisely because the finance close is not on the checkout path.
- The job's own run log carried enough detail, timestamp, credentials used, file name read, to trace root cause the same morning, which is why this postmortem could be written from logs and chat rather than from memory two days later.
- Rehearsal 1 found, in pre-production and at no customer cost, the straddle-line reconciliation failure that D-019's one-weekend plan would otherwise have met on a live cutover weekend (N37): the rehearsal that fails is the one worth running.

## 5. Corrective actions

| ID | Action | Addresses cause # | Owner | Due date | Verification method | Status |
|---|---|---|---|---|---|---|
| A1 | Build ADR-0004: reconcile settlement for both paths from one ledger, matching on either reference, with a classified straddle set for lines that cross the cutover | 1 | Bea Lindqvist | 2026-07-03 | Rehearsal 3 passing the amended AC-8, 2026-07-04 (N39); straddle logic first exercised in rehearsal 2 (N38) | verified |
| A2 | Give pre-production its own SFTP drop; pre-production credentials cannot read the production drop | 3 | Hamid Qureshi | 2026-06-26 | A deliberate read attempt from pre-production against the production drop, run 2026-06-26, failed as designed | verified |
| A3 | Add a page at 07:45 if no settlement file has landed since the scheduled 06:30 arrival, for each provider on a day its file is due (N34) | 4 | Bea Lindqvist | 2026-07-09 | Synthetic failure check (N72): Marlowe file withheld in pre-production on 2026-07-02, page fired, runbook closed in 11 minutes; live in production from 2026-07-09, verified by the live page of 2026-07-10 | verified |
| A4 | Make the production ingestion job exit non-zero on "no file", instead of treating an empty poll as success | 4 | Bea Lindqvist | 2026-06-26 | Failing-file test added to CI | verified |
| A5 | Add "disable every pre-production schedule" to the rehearsal abort checklist | 5 | Tomasz Wierzbicki | 2026-06-19 | Exercised at the rehearsal 2 abort drill; schedules confirmed disabled before the drill closed | verified |
| A6 | A dependency sitting at "requested" for more than 4 weeks is escalated automatically at the weekly dependency review | 2 | Ife Adeyemi | 2026-06-19 | Confirmed against the dependency register's review log at the first regular review after it was added, 2026-07-02 (no row at requested past 4 weeks) | verified |

A3 pages when a file never arrives; A4, which stops the production job from treating an empty poll as success, is what would have caught 2026-06-15's actual failure, a file that arrived and was then consumed by the pre-production job before production ever read it.

All six actions verified before the first Marlowe cohort shipped under the reshaped plan. Cutover plan v2 carries A3 through N72 in its phase 0 pre-checks, A1 through ADR-0004 in section 5 (reconciliation), A5 in section 4 (the abort rule), and A2 and A4 in section 3 (the rehearsal gaps and the fixes before rehearsal 2); A6 does not appear there.

## Exit gate

- [x] The timeline is built from recorded sources, with detection and resolution both timestamped: section 1, 06:30 to 12:40, each row sourced to a log, a ticket or a chat channel.
- [x] Impact is quantified, or the reason it cannot be is stated: section 2 states the 5 hours 40 minutes, 5,190 lines and £332,000 from N42, and states plainly that no customer-facing impact occurred rather than inventing one.
- [x] No cause row contains a person's name: section 3's five rows use "a pre-production job," "the ingestion job," "the rehearsal's abort checklist," never a name; "a finance analyst" names a role in section 1's detection note, not a section 3 cause row. Names appear only in sections 1, 4 and 5 where the template calls for who did what, not why the system failed.
- [x] Every cause row has at least one corrective action, and every action has an owner, a due date, and a verification method: causes 1 to 5 map to the six actions in section 5, with cause 4 carrying two.
- [x] Verified actions that change how the service is run are copied into section 6 of [operational-readiness-review.md](../templates/operate/operational-readiness-review.md): this journey fills no operational-readiness-review.md, so the checks derived from this incident are carried instead by release readiness section 5 and cutover plan v2's phase 0. At Gate 5 attempt 2, condition C1 is A3. Condition C2 is publishing DEP-3's finance daily-close runbook (delivered 2026-07-08) to support and briefing the support team, met 2026-07-10: a pre-existing dependency, logged after D-021 (2026-06-18), that this incident made urgent rather than an action this postmortem produced.
- [x] The review happened out loud with the responders in the room, not by document circulation alone: 2026-06-17, facilitated by Noor Haddad, with Bea Lindqvist, Tomasz Wierzbicki, Ife Adeyemi and the finance analyst who detected the incident present. Hamid Qureshi, owner of A2, was not a responder on the day.

Signed: Bea Lindqvist, Senior Engineer, Payments and Incident Owner, 2026-07-10 (the date the last corrective action, the settlement-file-absent alert, was verified live in production).

Back to the [Harbourgate journey](harbourgate-journey.md).
