# Dependency Register: Quay (Harbourgate Payment Modernisation)

Fills [templates/execution/dependency-register.md](../templates/execution/dependency-register.md). Part of the [Harbourgate journey](harbourgate-journey.md): a fictional mid-market retailer replacing a nine-year-old checkout with a single-provider payment service, Quay. Everything here is invented: Harbourgate, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date and status is ILLUSTRATIVE, drawn from the journey's data sheet and identifier table, never to be copied as a target. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), first filled 2026-04-10 ahead of the gate, governed weekly through DELIVER
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [program-premortem](../skills/program-premortem/SKILL.md)

**Initiative:** Quay (checkout-pay replacement) · **Register owner:** Ife Adeyemi, Product Manager · **Review cadence:** weekly, Thursday engineering sync
**Last reviewed:** 2026-10-16

## 1. The register

| # | Dependency (deliverable, not a team name) | Owning team | Their named contact | Needed by (our date) | Their committed date | Status | Escalation contact (their manager or ours) |
|---|---|---|---|---|---|---|---|
| DEP-1 | Kestrel terminal SDK certified for the kiosk PIN pad model | Kestrel | Dani Ferreira | 2026-07-20 | 2026-07-10 | delivered 2026-07-09 | Tomasz Wierzbicki (Engineering Lead) |
| DEP-2 | Marlowe sandbox settlement files, so reconciliation can be tested against something other than production (N33: Marlowe's file arrives daily at 06:30 with weekend settlements folded into Monday's file, which is why testing only against production data was risky) | Marlowe merchant support | ticket queue only, no named contact | 2026-06-05 | never committed; requested 2026-04-20 | should have read at risk from 2026-06-05; recorded at risk 2026-06-16; withdrawn 2026-07-03, need removed by ADR-0004 | Bea Lindqvist, escalated to Tomasz Wierzbicki from 2026-06-16 |
| DEP-3 | Finance daily-close runbook updated for dual-path reconciliation | Finance operations | Priya Raman | 2026-07-10 | 2026-07-08 | delivered 2026-07-08 | Rohan Iyer (CFO) |
| DEP-4 | Reporting migrated off the legacy table shape (mitigates R5: a change to the legacy table shape breaking reporting, finance reconciliation or the order-history page) | Data engineering | Grace Mbeki | 2027-02-27 | 2027-02-27 | in progress | Tomasz Wierzbicki (Engineering Lead) |
| DEP-5 | Kiosk firmware update scheduled across 61 shops (closes R12 on delivery) | Store operations | Lena Baptiste | 2026-08-01 | 2026-07-28 | delivered 2026-07-30 | Tomasz Wierzbicki (Engineering Lead) |
| DEP-6 | Fraud rules engine re-pointed at the new decline event stream | Fraud and risk | Saoirse Whelan | 2026-07-13 | 2026-07-06 | delivered 2026-07-06 | Tomasz Wierzbicki (Engineering Lead) |
| DEP-7 | PCI DSS scope re-assessment booked for after the sunset | InfoSec, with the external assessor | Hamid Qureshi | 2026-12-15 | 2026-11-20 | in progress | Rohan Iyer (budget owner for the assessor) |
| DEP-8 | Termination notices to Marlowe and Tidewater for 2026-12-15 | Legal | Anneliese Vogt | 2026-09-15 | 2026-09-14 | delivered 2026-09-14 | Rohan Iyer (CFO, contract sponsor) |

DEP-2's contact column reads "ticket queue only, no named contact" because that is what Marlowe's merchant support actually offered, not a placeholder awaiting a name. The row stayed unnamed for its whole life, from being requested on 2026-04-20 to being withdrawn on 2026-07-03, including the eight weeks it sat at requested before escalation, which is the condition section 4's failure table warns against. "Withdrawn" is not in the fixed status vocabulary below; it is a declared deviation, used once, for the one row whose need disappeared rather than being met.

## 2. Escalation ladder

1. Slip detected at weekly review: register owner (Ife Adeyemi) contacts the named contact within one working day. Where there is no named contact, as on DEP-2 throughout its life, the register owner contacts the internal owner of the relationship instead (Bea Lindqvist for Marlowe) and records that no external escalation path exists.
2. No recovery plan within `<n>` working days: escalate to the escalation contact on the row.
3. Still unresolved and the needed-by date is inside `<n>` weeks: raise at the monthly sponsor sync with Rohan Iyer present, and the dependency becomes a risk register row with a mitigation.

Rung 1's "one working day" reproduces the template's own fixed wording and needs no data-sheet citation. Rungs 2 and 3 keep the template's `<n>` placeholders rather than a filled number, because no data-sheet row states a working-day or week count for this ladder; setting them is a decision for the register owner and the escalation contacts, not a number this document may invent. The 4-week age trigger in A6 (section 4) is different: that count is a journey fact, drawn from corrective action A6 in the data sheet, and is cited there.

DEP-2 never reached rung 3 through the ladder itself; nobody raised it, because until 2026-06-16 nothing in the register forced the question. Risk register row R3 already existed, opened at the 2026-04-09 premortem at score 4 with the mitigation "read the production drop with the keep flag," eleven days before DEP-2 was even requested from Marlowe (2026-04-20); rehearsal 1 proved that mitigation wrong, and R3 was re-scored to 9 on 2026-06-15. A separate row, R14, came from security finding F2 (the SFTP drop shared by pre-production and production), not from DEP-2, and was added to the register only after HG-INC-14. DEP-2 itself reached rung 1 only on 2026-06-16, about four weeks after the 4-week rule, had it existed, would have fired at the 2026-05-21 review; that rule, A6, was not added until three days later, on 2026-06-19 (see section 4).

## 3. Reverse dependencies

| Deliverable we owe | To team | Their needed-by | Our committed date | Status |
|---|---|---|---|---|
| Legacy payment table shape written unchanged from Quay (ADR-0002), so the order-history page and reporting keep working | Order service and order-history page (I-10) | ongoing, from Quay's first live order | 2026-05-06 (D-011, percentage ramp with shadow comparison begins) | on track; the shape stays until removal 2027-03-31 (N65, DEP-4) |
| Decline event stream carrying provider, reason class and trace id (AC-4), so fraud rules can be re-pointed at it | Fraud and risk (I-9) | 2026-07-06, to meet DEP-6 | before 2026-07-06, evidenced by DEP-6 delivering against it on 2026-07-06 | delivered; DEP-6 closed on time against it |
| Nightly reconciliation export to the finance ERP (I-11), covering both paths through the drain | Finance operations | 2026-07-08, to meet DEP-3 | 2026-07-03 (ADR-0004 built, straddle set classified) | delivered; underpins the daily close DEP-3 depends on |

## 4. Weekly review notes

| Date | Rows that changed status | Escalations opened or closed |
|---|---|---|
| 2026-04-10 (opened at Gate 3, before the first Thursday review) | Register opened at Gate 3; DEP-1, DEP-4 and DEP-5 logged at committed, each against the committed date the owning team gave (section 1). Their needed-by dates shown in section 1 were re-baselined to plan v2 after D-021 (2026-06-18); the dates logged at this opening matched the schedule assumed at Gate 3 (completion 2026-06-30, N44), and were re-baselined to plan v1 (D-019, 2026-06-02) and then to plan v2 (D-021, 2026-06-18) | none |
| 2026-04-16 | No change to DEP-1, DEP-5; DEP-4 moved from committed to in progress; DEP-2 not yet requested | none |
| 2026-04-23 | DEP-2 logged at requested (asked of Marlowe 2026-04-20, no committed date offered); its needed-by of 2026-06-05 was set to leave time before the rehearsal and cutover then planned for June | none |
| 2026-05-21 | DEP-2 still requested, 4 weeks elapsed, no named contact and no committed date | none opened; the ladder's rung 3 existed but nothing in the register yet triggered it automatically |
| 2026-06-11 | DEP-2 still requested, 7 weeks elapsed; its needed-by of 2026-06-05 had already passed with no committed date, which the template's own arithmetic should have read as at risk. In hindsight, once D-019 set Marlowe's cutover for 2026-06-27 and 28 (N70), DEP-2 was still the only route to a non-production file for rehearsal 1 on 2026-06-13 (N37), then two days away | none |
| 2026-06-16 (ad hoc, called after Gate 5 attempt 1's NO-GO, outside the weekly cadence) | Rehearsal 1 (2026-06-13) failed its verify phase against production-shaped Marlowe data, and HG-INC-14 (2026-06-15) followed; the review named DEP-2's eight weeks at requested as a contributing gap, R9 and R14 were added to the risk register, and R3, open since the 2026-04-09 premortem and re-scored to 9 on 2026-06-15, was recorded here; Gate 5 attempt 1 returned NO-GO | escalation opened: DEP-2 to Bea Lindqvist, then Tomasz Wierzbicki |
| 2026-06-19 (ad hoc, the corrective action's own due date, outside the weekly cadence) | Corrective action A6 added from the postmortem: a dependency at requested for more than 4 weeks is escalated automatically at the weekly review, owner Ife Adeyemi | none open; A6 not yet verified against a live review |
| 2026-07-02 | A6 verified for the first time at a regular review: no row at requested past 4 weeks. DEP-3 and DEP-6 logged at committed, their needed-by dates set against plan v2 (D-021, 2026-06-18) | none open |
| 2026-07-03 (ad hoc, the day the need was actually removed) | DEP-2 withdrawn: ADR-0004 reconciles both paths from one ledger with a classified straddle set, using D-021's phased cohorts to verify reconciliation against real settlement files at 5% exposure and A2's separated SFTP drops to keep pre-production off the production drop, removing the need for Marlowe sandbox files entirely | escalation on DEP-2 closed |
| 2026-07-09 | DEP-1 delivered 2026-07-09; DEP-3 delivered 2026-07-08; DEP-6 recorded delivered 2026-07-06 | none open |
| 2026-07-30 | DEP-5 delivered 2026-07-30, two days past its committed date of 2026-07-28 but still two days inside the 2026-08-01 needed-by; the slip triggered rung 1 and closed without an at-risk flag; R12 (kiosk firmware update) closed on delivery | none open |
| 2026-08-13 | DEP-4 tracking against its committed date; no change | none open |
| 2026-08-27 | DEP-4 tracking against its committed date; no change; DEP-8 logged at committed (needed by 2026-09-15, committed 2026-09-14) | none open |
| 2026-09-17 | DEP-8 delivered 2026-09-14; DEP-7 logged at committed following D-023 (2026-09-14), which fixed the 2026-12-15 sunset date; DEP-7's committed date of 2026-11-20 confirmed with the external assessor | none open |
| 2026-10-15 | DEP-4 and DEP-7 remain in progress, both tracking against their committed dates | none open |

## How this register fails

| Failure mode | What it looked like on this register | The rule that stopped it |
|---|---|---|
| A verbal yes recorded as committed | Marlowe never gave DEP-2 a date at all, so it could not be mis-recorded as committed; it sat honestly at requested for eight weeks, which was itself the warning nobody acted on | Committed means on their plan with their date. DEP-2's row never claimed more than it had |
| No named human | DEP-2's contact column reads "ticket queue only" for its entire life | The rule asks for a name. Where none exists, the register says so in plain words rather than inventing one, and routes escalation internally instead |
| At risk is felt, not computed | Before 2026-06-16, nobody compared DEP-2's requested-since date against a threshold, and nobody noticed its needed-by date of 2026-06-05 had already passed with no committed date, which the template's own arithmetic would have read as at risk | A6 fixed the age signal: 4 weeks at requested escalates automatically, verified against the review log from 2026-07-02 |
| Escalation avoided | DEP-2 reached rung 1 only after an incident forced the question, not from the weekly review catching it | The ladder is now triggered by the register itself (A6), not by someone deciding the moment feels right |
| Reverse dependencies left as a courtesy blank | Early drafts of this register tracked only what Quay needed from others, before reverse dependencies were added | Section 3 states what Quay owes the order-history page, fraud and finance, each with our own committed date, so those teams can hold the register to the same standard |

## Exit gate

- [x] Every dependency names a deliverable, a human contact, and an escalation contact: passed from 2026-07-03, when DEP-2 was withdrawn; before that date this box failed on DEP-2. DEP-1, DEP-3 to DEP-8 name a human contact in section 1 throughout. DEP-2 alone never had one: its contact is explicitly "no named contact" rather than left blank, with an internal escalation contact (Bea Lindqvist, then Tomasz Wierzbicki) named beside it for its whole life, but that internal contact does not satisfy the box on its own.
- [x] Every row shows both our needed-by date and their committed date: all eight rows in section 1.
- [x] No row claims committed without the work on the owning team's own plan: DEP-2 is marked "never committed; requested" for the whole period it had no date from Marlowe.
- [x] Every at-risk or blocked row has a corresponding risk register entry: DEP-2 fed risk R3, open since the 2026-04-09 premortem and re-scored to 9 on 2026-06-15, closed 2026-07-03 once ADR-0004 removed the need for sandbox files (harbourgate-risk-register.md). R14, from security finding F2 (the SFTP drop shared by pre-production and production), is a separate cause of the same incident, not DEP-2's own risk entry; it closed 2026-06-26 once A2 separated the environments' drops.
- [x] Reverse dependencies are filled in, not left as a courtesy blank: section 3 names what Quay owes the order-history page, the fraud team and finance, each with an our-committed date and a status.
- [x] The weekly review has an entry from the current or previous week: 2026-10-15, within the week of this journey's index date, 2026-10-16.
- [x] The example row has been deleted: section 1 holds only DEP-1 to DEP-8.

Reviewed and current as of 2026-10-16: Ife Adeyemi, Product Manager and register owner. Open: DEP-4 (reporting off the legacy table shape, due 2027-02-27) and DEP-7 (PCI scope re-assessment, assessor booked 2026-11-20 against the 2026-12-15 need) remain in progress and carry into the journey's sunset plan (harbourgate-sunset-eol-plan.md).
