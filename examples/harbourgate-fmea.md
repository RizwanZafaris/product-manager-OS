# Harbourgate FMEA: settlement ingestion and reconciliation

Fills [frameworks/execution/fmea.md](../frameworks/execution/fmea.md).

Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, pound and identifier is ILLUSTRATIVE. It is drawn from the [Harbourgate journey](harbourgate-journey.md) and the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), and is not a benchmark or target.

**Owner:** Bea Lindqvist, Senior Engineer, payments · **Facilitator:** Noor Haddad (HC39) · **Run:** 2026-06-22 · **Re-run:** 2026-06-29 · **Status:** Re-run complete, row 7 added after rehearsal 2

## What it is for

This FMEA walks settlement ingestion and reconciliation under cutover plan v2. It covers both the legacy and Quay paths during the drain, including file arrival, file consumption, straddle classification, refunds, tolerance checks and the ERP export.

The team screened on severity first and did not rank by RPN. The wrong-rail legacy refund is High because its severity is 5, even though its RPN is 45. RPN is retained as a tiebreak only within an action-priority band.

The first sheet did not include the voided-authorisation double count. Rehearsal 2 found it on 2026-06-27, and row 7 was added on the re-run on 2026-06-29. The FMEA S, O and D scales are not register scores. As recorded in reconciliation note 3, the register uses different likelihood and impact scales.

## Run it when

This run was required before Gate 5 because the flow moves money and writes to finance's systems of record. It was run on 2026-06-22 under cutover plan v2 and re-run on 2026-06-29 after rehearsal 2.

The re-run was triggered by a failure mode not present on the first sheet: a voided authorisation counted twice.

## Inputs you need first

- Settlement file timing from N33
- The £50 reconciliation tolerance from N35
- The straddle drain target from N36
- Rehearsal 1 evidence from N37
- Rehearsal 2 evidence from N38
- Business rules BR-002 and BR-003
- Corrective actions A1 to A4
- ADR-0004
- The incident and coverage context in the [Harbourgate journey](harbourgate-journey.md)
- The FMEA evidence row HC39 in the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md)

## The worksheet

### Step 1: the three scales

Severity, the worst credible effect of this failure mode on a user, a customer, or the business:

| S | Meaning |
|---|---|
| 1 | Cosmetic. Somebody notices and nothing changes |
| 2 | One person loses time or redoes work. No external effect |
| 3 | A team absorbs manual rework, or a customer complains and is made whole |
| 4 | A commitment is missed, a period close slips, or a customer escalates formally |
| 5 | Money moves wrongly, a contract or regulation is breached, or personal data leaks |

Occurrence, how often this cause produces this failure mode within the initiative's horizon:

| O | Meaning |
|---|---|
| 1 | No precedent here or in systems like it |
| 2 | Has happened to teams like ours, not to us |
| 3 | Has happened to us in the last two years |
| 4 | Happens in a normal month, or a precondition is already true |
| 5 | Happens most weeks and is treated as normal |

Detection, and note the inversion: a **low** number is good, because it means something catches the failure early.

| D | Meaning |
|---|---|
| 1 | An automatic control blocks the failure before it leaves the system, every time |
| 2 | An automatic check flags it and a human must clear the flag before it proceeds |
| 3 | A routine human review would probably catch it before it reaches anyone outside |
| 4 | Found downstream: at the close, in a reconciliation, or in an audit |
| 5 | Nothing looks for it. You learn from a complaint, or you never learn |

These scales are local to this FMEA. They are not restated as Harbourgate risk-register scores.

### Step 2: how the rows get ranked, and the method that is deprecated

Risk priority number is calculated as:

**RPN = S x O x D**

The team retained the arithmetic but did not rank by RPN. Severity screening came first:

1. Read every severity-5 row before any other row.
2. Read every severity-4 row next.
3. Assign action priority from the table.
4. Use RPN only as a tiebreak within an action-priority band.

| S | Condition on O and D | Action priority |
|---|---|---|
| 5 | any O, any D | High |
| 4 | O of 3 or more, or D of 4 or more | High |
| 4 | O of 2 or less and D of 3 or less | Medium |
| 3 | O of 4 or more, or (O of 3 and D of 4 or more) | High |
| 3 | O of 3 and D of 3 or less, or O of 2 or less and D of 4 or more | Medium |
| 3 | O of 2 or less and D of 3 or less | Low |
| 2 | O of 4 or more and D of 4 or more | Medium |
| 2 | anything else | Low |
| 1 | any O, any D | Low |

What each band obliges:

| Action priority | Obligation |
|---|---|
| High | An action with an owner and a date before the gate, or a written reason for accepting it, signed by the sponsor |
| Medium | An action with an owner, or a recorded acceptance in the risk register's accepted section |
| Low | Action optional. Record that you looked and chose not to act |

The FMEA did not use RPN to put the wrong-rail refund below another row. Its calculation is **5 x 3 x 3 = 45**, but its severity of 5 makes it High.

### Step 3: the analysis sheet

| # | Step or function | Failure mode (what the system does) | Effect (on whom, and what they lose) | S | Cause (why it does that) | O | Current control, named | D | RPN (deprecated, tiebreak only) | Action priority |
|---|---|---|---|---:|---|---:|---|---:|---:|---|
| 1 | Receive the daily settlement file | Treats the expected file as present when no file has landed at 06:30 | Finance cannot complete the daily close on time, and the missing settlement remains undiscovered until downstream work | 4 | No settlement-file-absent alert existed before A3 | 3 | None before A3 | 5 | 4 x 3 x 5 = 60 | High |
| 2 | Ingest the settlement file | A non-production job reads and consumes the production file | The production reconciliation loses its input, and finance's close is delayed | 4 | Pre-production shares the production SFTP drop and the job deletes the file on successful read | 3 | None before A2 and A4 | 5 | 4 x 3 x 5 = 60 | High |
| 3 | Match settlement lines across both paths | Leaves a line authorised on one path and settled on another unmatched | Finance carries unmatched money into the close and must perform manual reconciliation | 4 | Settlement lags authorisation, refunds can lag by months, and there is no classified straddle set | 4 | Reconciliation tolerance in BR-003, but no straddle classification before ADR-0004 | 4 | 4 x 4 x 4 = 64 | High |
| 4 | Route a refund for a legacy-authorised order | Sends the refund down the wrong rail | The customer does not receive the expected refund, and finance must correct a money-moving error | 5 | Refund routing does not consistently use the original authorisation rail | 3 | BR-002; rehearsal 2 found and fixed the legacy-refund 422 path | 3 | 5 x 3 x 3 = 45 | High |
| 5 | Compare settled value with captured value | Allows a provider's settled value to differ from captured value by more than £50 without blocking close | Finance closes with an unresolved value difference and must reopen the close | 4 | A provider-level tolerance breach is not reconciled before close | 2 | BR-003 blocks finance close above £50 | 1 | 4 x 2 x 1 = 8 | Medium |
| 6 | Export reconciled results to the finance ERP | The ERP export fails | Finance cannot use the reconciled result in the ERP and must repeat or complete the export manually | 4 | The nightly ERP export fails after reconciliation has completed | 2 | None named in this FMEA | 3 | 4 x 2 x 3 = 24 | Medium |
| 7 | Count voided authorisations in reconciliation | Counts a voided authorisation twice | Finance sees an incorrect count and must correct the reconciliation before close | 4 | The void event and the authorisation record are both included in the count | 3 | Rehearsal 2 found the issue on 2026-06-27; fix before rehearsal 3 | 4 | 4 x 3 x 4 = 48 | High |

**Re-run note:** Row 7 was absent from the 2026-06-22 sheet. It was added on 2026-06-29 after rehearsal 2. Its initial calculation is **4 x 3 x 4 = 48**.

### Step 4: the action sheet

Actions were selected for every High row. Row 5 remains covered by BR-003 and was not given a new action on this sheet. Row 6 remains a Medium item and requires either an owner or recorded acceptance in the risk register's accepted section. No new action identifier for the ERP export is present in HC39, so this sheet does not invent one.

| # | Action | Type (prevent / detect / reduce the effect) | Owner (one role) | By when | S after | O after | D after | Action priority after | Register row |
|---|---|---|---|---|---:|---:|---:|---|---|
| 1 | A3, page at 07:45 when no settlement file has landed since 06:30 | detect | Bea Lindqvist | 2026-07-09 | 4 | 3 | 2 | High | A3 |
| 2 | A2, separate SFTP drops so pre-production credentials cannot read the production drop, and A4, make the production ingestion job exit non-zero on "no file" | prevent and detect | Bea Lindqvist | 2026-06-26 | 4 | 1 | 2 | Medium | A2, A4 |
| 3 | ADR-0004, reconcile both paths from one ledger, match on either reference, and classify the straddle set; BR-003 detects a remaining value difference | prevent and detect | Bea Lindqvist | 2026-07-03 | 4 | 2 | 2 | Medium | ADR-0004 |
| 4 | Enforce BR-002 routing to the original provider for legacy-authorised refunds, and retain the rehearsal 2 fix for the 422 path | prevent | Bea Lindqvist | 2026-06-27 | 5 | not restated | not restated | High on severity alone | BR-002 |
| 5 | No new action selected. BR-003 blocks finance close when settled value differs from captured value by more than £50 | detect | Priya Raman | while BR-003 is active | 4 | 2 | 1 | Medium | BR-003 |
| 6 | No new action identifier supplied by the data sheet. Record the ERP export failure in the risk register accepted section with an owner | reduce the effect | Priya Raman | before Gate 5 | 4 | 2 | 3 | Medium | risk register accepted section |
| 7 | Add the voided-authorisation count case to the reconciliation tests and pass it before rehearsal 3 | prevent and detect | Bea Lindqvist | before 2026-07-04 | 4 | 1 | 2 | Medium | rehearsal 3 evidence |

Arithmetic for the after states:

- Row 1: **4 x 3 x 2 = 24**. It remains High because S is 4 and O is 3.
- Row 2: **4 x 1 x 2 = 8**. It moves to Medium because S is 4, O is 1 and D is 2.
- Row 3: **4 x 2 x 2 = 16**. It moves to Medium because S is 4, O is 2 and D is 2.
- Row 4: S remains **5**, so the action priority remains High on severity alone. The after O and D values are not restated in HC39.
- Row 7: **4 x 1 x 2 = 8**. It moves to Medium because S is 4, O is 1 and D is 2.

## ILLUSTRATIVE example

This is the filled Harbourgate example for settlement ingestion and reconciliation. Every number, date, pound and identifier above is ILLUSTRATIVE and comes from the Harbourgate data sheets.

The ordering decision is visible in the first four rows:

1. Row 4 is read first because **S = 5**, despite an RPN of 45.
2. Rows 1, 2 and 3 are read next because each has **S = 4**.
3. Row 3 has the largest RPN among the severity-4 rows, **64**, but that number did not make it more important than row 1 or row 2.
4. Row 7 is a re-run addition, not evidence that the first sheet was complete.

## Reading the result

The severity-5 row is a design decision. A legacy-authorised refund must remain on the original rail under BR-002. It is not made acceptable merely because its RPN is lower than row 3's.

The incident evidence changed the sheet in two ways. A1 and ADR-0004 address the straddle cause, while A2, A3 and A4 address the production file-consumption and missing-file causes from HG-INC-14. Rehearsal 2 then exposed the voided-authorisation count failure, which was added as row 7 instead of being described as if it had been known on 2026-06-22.

The action types are mixed:

- A3 improves detection of an absent file.
- A2 prevents environment cross-reading.
- A4 detects an invalid no-file production run.
- ADR-0004 prevents unmatched straddle lines by changing the reconciliation design.
- BR-002 prevents a refund from taking the wrong rail.
- The row 7 test prevents and detects double counting.

The sheet does not claim that an action reduced severity where the data does not support that claim. The wrong-rail refund remains S5.

## Where the output lands

- High rows go to the [Harbourgate journey](harbourgate-journey.md) evidence for Gate 5 by name.
- A1 and ADR-0004 feed the cutover reconciliation design.
- A2, A3 and A4 feed operational readiness and the incident corrective-action record.
- BR-002 and BR-003 remain the named controls for refund routing and the £50 finance-close tolerance.
- Row 7's fix is evidenced by rehearsal 3 on 2026-07-04.
- The source record for the FMEA run and re-run is HC39 in the [Harbourgate coverage sheet](harbourgate-coverage-sheet.md).

## Re-run trigger

Re-run when settlement ingestion or reconciliation gains or loses a step, when a provider or ERP integration changes, or after an incident or rehearsal finds a failure mode not already present.

This run was re-run on 2026-06-29 because rehearsal 2 on 2026-06-27 found the voided-authorisation double count. Rehearsal 3 on 2026-07-04 then provided the next verification point.

## The trap

The first sheet looked complete because it covered absent files, unsafe file consumption, straddle lines, refunds, tolerance breaches and ERP export. It was not complete: rehearsal 2 exposed a counting failure in the reconciliation itself.

A second trap would have been to rank the rows by RPN. That would have placed the wrong-rail refund, at 45, below the absent-file row at 60 and the straddle row at 64. Severity-first screening keeps the money-moving failure visible.

A third trap would have been to restate the FMEA scores as register scores. HC39 and reconciliation note 3 make clear that FMEA S, O and D are a separate instrument from the register's likelihood and impact scoring.

## Feeds

- [Harbourgate journey](harbourgate-journey.md), for N33 to N36, BR-002, BR-003, A1 to A4 and ADR-0004
- [Harbourgate coverage sheet](harbourgate-coverage-sheet.md), HC39 and reconciliation note 3
- [Harbourgate incident postmortem](harbourgate-incident-postmortem.md), for HG-INC-14 and A1 to A6
- [Harbourgate migration cutover plan](harbourgate-migration-cutover-plan.md), for the settlement and drain controls
- [Harbourgate operational readiness review](harbourgate-operational-readiness-review.md), for the detection controls used during operation
- Risk register, for the Medium row acceptance required for the ERP export failure

**Exit gate:** Bea Lindqvist signed the completed FMEA and Noor Haddad witnessed the re-run on 2026-06-29. The sheet is ready for Gate 5 review.
