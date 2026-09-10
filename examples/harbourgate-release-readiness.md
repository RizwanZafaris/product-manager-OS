# Release Readiness: Quay payment service, Marlowe cohort 1

Fills [templates/delivery/release-readiness.md](../templates/delivery/release-readiness.md). Part of the [Harbourgate journey](harbourgate-journey.md): a fictional mid-market retailer replacing a nine-year-old checkout with a single-provider payment service, Quay. Everything here is invented: Harbourgate, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date and threshold is ILLUSTRATIVE, drawn from the journey's data sheet and identifier table, never to be copied as a target. See the [examples index](README.md).

**Stage:** DELIVER (this file IS [Gate 5: release readiness green](../os/STAGE-GATES.md), attempt 2)
**Knowledge:** [knowledge index](../knowledge/INDEX.md)
**Skill:** [launch-readiness](../skills/launch-readiness/SKILL.md)

**Release:** Quay, Marlowe cohorts, starting with cohort 1 (D-021 phased shift: 5% of Marlowe's web and app orders route through Quay and Kestrel hosted fields at cohort 1; Marlowe stops carrying them) · **Target date:** 2026-07-13
**Decider:** Ife Adeyemi, Product Manager · **Decision:** GO WITH CONDITIONS
**Decision date:** 2026-07-08 · **Held before any production rollout:** yes for this release, five days before the first order in cohort 1 (2026-07-13, N71). The D-011 shadow ramp (2026-05-06 to 2026-05-21) ran live traffic before any Gate 5 attempt and was stopped by D-017; this gate is the first to put Quay in production as the system of record.
**Gate 6 review window (chosen now, before the data exists):** 2026-09-07 + 4 weeks, to 2026-10-05 (N67)

This is Gate 5's second attempt. Attempt 1, on 2026-06-16, was NO-GO: the rollback line was unknown and the reconciliation line had already failed, three days after rehearsal 1 aborted (2026-06-13) at 9 hours 10 minutes, unable to pass verify because there is no instant at which a provider has nothing in flight, and one day before its still-enabled ingestion job consumed the production Marlowe file (HG-INC-14, 2026-06-15). Between the two attempts the plan changed under D-021 from D-019's one-weekend freeze-move-switch to a phased traffic shift with a legacy drain, and two further rehearsals ran clean or clean enough to fix. This document is attempt 2, not attempt 1 rewritten: it decides go or no-go for Marlowe's cohorts (5%, 50%, 100% of that provider's traffic, N46), each step advancing on the migration cutover plan's verify-phase exit criteria, not for the Tidewater or Kestrel-legacy cohorts that follow at Gate 5 attempts 3 and 4. Cohort 1, at 5%, is the first production exposure and carries the conditions below.

| Gate 5 attempt | Date | Outcome |
|---|---|---|
| 1 | 2026-06-16 | NO-GO: rollback line unknown, reconciliation line failed, after rehearsal 1 |
| 2 | 2026-07-08 | GO WITH CONDITIONS for the Marlowe cohorts (cohort 1 first), this document |
| 3 | 2026-07-29 | Later attempt, recorded 2026-08-26: GO for the Tidewater store cohorts (separate document) |
| 4 | 2026-08-26 | Later attempt, recorded 2026-08-26: GO for the Kestrel legacy connector cohorts (separate document) |

## 1. Features

- [x] Everything in the PRD's launch scope for cohort 1 is built, and nothing extra shipped unreviewed: HARBOURGATE-S1 (pay by card, web and app), S3 (decline with reason class and one retry), S4 (per-provider routing flag with two-person change), S5 (refund to the originating provider), S6 (settlement ingestion and reconciliation), S7 (legacy table shape written unchanged), S8 (decline event stream), S10 (step-up authentication), S11 (capture on dispatch, void on fulfilment failure). S2 and S9 (kiosk payment and kiosk fallback) are Tidewater's stories and are not in this cohort's scope; S12 (settlement-file-absent alert) is condition C1 below, not yet shipped at sign-off.
- [x] Scope cuts since sign-off: none. The guest checkout redesign was out of scope from the PRD itself, not cut afterward, and the order-history page keeps reading the legacy table shape unchanged under ADR-0002.
- [x] Acceptance criteria all pass (Gate 4 evidence: load test of 2026-06-05, N23 and N24, and Gate 4 attempt 2, met 2026-06-09). AC-3 is a live criterion, not a one-time pass: verified at each cohort's dwell exit per N16 and N47, and protected by the N17 rollback trigger; the Marlowe baseline it is measured against is an estimate (N14). Two criteria moved after Gate 4 and are evidenced separately: AC-8 was amended 2026-07-03 when ADR-0004 introduced the classified straddle set, verified by rehearsal 3 passing AC-8 cleanly on 2026-07-04 (N39); rehearsal 2 (2026-06-27) exercised the straddle-set logic before it was formally merged and stands as A1's first verification of it, not as evidence the amended criterion passes. AC-13, the settlement-file-absent alert, was added 2026-06-19 and is tracked as condition C1 (A3 / AC-13), not yet met at this sign-off.

## 2. Tests

- [x] Every blocking level ran and passed, with the honest exception named: unit and integration suites passed at Gate 4 attempt 2 (2026-06-09); rehearsal 1 (2026-06-13, N37) did not pass, aborted at 9 h 10 min with 1,529 of 1,742 Marlowe settlement lines unmatched, and caused HG-INC-14; rehearsal 2 (2026-06-27, N38) found and fixed two issues (legacy refunds returning 422, voided authorisations double-counted); rehearsal 3 (2026-07-04, N39) ran clean; the rollback rehearsal (N40) timed a flag flip at 3 min 50 s and a restore at 22 minutes, both 2026-07-04.
- [ ] No open rows against a blocking defect for cohort 1's scope: not literally true, exceptions carried to section 3. A2 closed 2026-06-26: pre-production credentials can no longer read the production settlement drop, verified by a failed read attempt, which closes the root cause behind HG-INC-14. Three items remain open and are carried to section 3 as known issues rather than closed silently: the decline reason-class mapping (N62), the straddle set's first live settlement cycle, and Marlowe's support model (N69).
- [x] UAT: signed off by Noor Haddad, QA Lead, against rehearsal 3's clean run and the rollback timing; no condition attached.
- [ ] For AI features: N/A. Quay contains no AI or machine-learning feature; see section 7.

## 3. Known issues shipping with this release

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| 1 | Decline events carry provider, reason class and trace id (AC-4 is met), but 6% of Kestrel declines classify to reason class "other" rather than a specific reason at this gate (N62) | low | AC-4's letter is met on every decline; "other" is a taxonomy gap, not a missing field, and support already has provider and trace id to work a ticket | Bea Lindqvist | 2026-08-14, the mapping fix already scheduled (N62) |
| 2 | ADR-0004's classified straddle set, which lets reconciliation match a line authorised on one path and settled on the other, has been exercised in rehearsal (rehearsal 2, A1) but not yet against a live production settlement cycle | medium | Cohort 1 is 5% of Marlowe's orders; the first live settlement cycle including cohort 1 orders is expected 2026-07-14 (N33, Kestrel's file lands daily 06:30 for the previous day), reviewed at the cohort 1 dwell exit on 2026-07-16 and must fall within the £50 tolerance Priya Raman signed (N35); the legacy path keeps serving refunds and its own settlement file through the drain, so nothing depends on the straddle set alone | Bea Lindqvist, reviewed at the cohort 1 dwell exit | 2026-07-16, dwell exit review; escalates to a rollback trigger review if it fails |
| 3 | Marlowe support is a ticket queue with a 4-hour response commitment and no named contact or phone escalation (N69); it responded in 2 h 10 min during HG-INC-14 but that was for an incident already understood internally | low | A rollback needs no cooperation from Marlowe: the flag flip (N40) runs entirely inside Quay, and cohort 1 caps exposure at 5% of that provider's volume | Tomasz Wierzbicki, monitor only, no fix exists to buy | reviewed at every cohort dwell exit, next 2026-07-16 |

## 4. Rollback

- [x] Rollback procedure exists and was tested on pre-production, on 2026-07-04 (N40)
- Rollback trigger, agreed in advance: cohort decline rate above baseline plus 2 percentage points over a rolling 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes; on-call may call it without further discussion (N17)
- Rollback owner: Tomasz Wierzbicki, Engineering Lead, cutover lead with authority to abort · Time to roll back: 3 minutes 50 seconds, flag flip to legacy (N40); full restore after the flag is removed takes 22 minutes, not needed for a mid-cohort rollback
- Data written between release and rollback: the legacy path is never frozen under D-021, so it keeps ingesting its own settlement file and serving its own refunds for the whole drain. Orders authorised on Quay before a rollback are kept on Quay's ledger and reconciled through the straddle set (ADR-0004); nothing is replayed onto the legacy path. A rollback stops new orders from reaching Quay; it does not touch orders Quay has already authorised (matches the migration cutover plan v2, section 4).

## 5. Operations and monitoring

- [x] Dashboards and alerts for this release are live (see [observability requirements](harbourgate-observability.md)): the Quay operations dashboard, owned by Bea Lindqvist, shows all four SLOs with budget remaining and the health of I-1, I-4 and I-6. Two of the three paging alerts on that document existed at Gate 3; the settlement-file-absent alert is condition C1 and is not yet live at this sign-off.
- [x] Failure scenarios reviewed with the on-call owner: reviewed with Tomasz Wierzbicki and the on-call rota, using HG-INC-14 as the worked case and the synthetic failure check of 2026-07-02 (N72), which paged at 07:46 and closed its runbook in 11 minutes, as the proof the review had something real to point at rather than a hypothetical.
- [x] The operational readiness review is complete, with two items carried forward as conditions rather than closed quietly: C1 (settlement-file-absent alert live) and C2 (finance daily-close runbook published, support briefed), both below. The runbook gap behind C2 was first raised as a known issue, then moved here as a condition because support cannot work a dual-path reconciliation ticket without it; the release may not proceed to cohort 1 while it is open.

**Conditions on this GO, with owner and date:**

| Condition | Owner | Due | Status at sign-off |
|---|---|---|---|
| C1 (A3 / AC-13): settlement-file-absent alert live in production, paging by 07:45 when a provider's file has not landed | Bea Lindqvist | 2026-07-09 | open at sign-off; the release may not proceed to cohort 1 without it |
| C2: finance daily-close runbook (DEP-3, delivered by finance 2026-07-08) published to support, and the support team briefed on the dual-path reconciliation it describes | Priya Raman, Callum Fraser | 2026-07-10 | open at sign-off; the release may not proceed to cohort 1 without it |

**Addendum, 2026-07-13.** Both conditions closed before cohort 1 began: C1 live 2026-07-09 (N34), verified by the live page of 2026-07-10 (A3); C2's runbook published to support and the support team briefed 2026-07-10. Cohort 1 started 2026-07-13, four and three days respectively after the two conditions closed.

## 6. Communications

| Audience | What they get | Owner | Sent |
|---|---|---|---|
| Support team | Briefing on the dual-path reconciliation, the three known issues in section 3, and the escalation path to Bea Lindqvist for a Quay-side problem or Tomasz Wierzbicki for a rollback call | Callum Fraser | 2026-07-10 (condition C2) |
| Internal stakeholders | Release note to the cast: engineering, finance operations, fraud and risk, data engineering, legal | Ife Adeyemi | 2026-07-08 |
| Customers | Silent release. The 5% of orders the flag would have routed to Marlowe (by order-id hash, N46) now take card details in Kestrel hosted fields rather than Harbourgate's own form, and the card number no longer reaches Harbourgate's servers (AC-1) | Ife Adeyemi | not applicable, silent |

## 7. Regulated overlay

- [x] Does this release touch a product that contains an AI or machine-learning feature and has a financial or data regulator applying to it? No. Quay's routing, decline classification and reconciliation logic is deterministic: it contains no model, so neither AI-specific instrument in the regulated module applies and this gate does not tick the overlay's gate lines. Four regimes apply to Quay regardless: PCI DSS, the card scheme rules and the market's strong customer authentication requirement through Harbourgate's acquiring contracts and its handling of cardholder data (S10 step-up, BR-005, N57 is in cohort 1 scope), and UK GDPR by statute, not through those contracts. Hamid Qureshi, Information Security Lead, is the regulatory owner in the AI overlay's place; reg-gap-check was run on 2026-07-01 for that reason and this gate's sign-off table (section 8) carries his dated re-check. The gap mapping sits in the [compliance impact assessment](harbourgate-compliance-impact-assessment.md), which carries three gaps (G1 to G3), states that no DPIA is required, and was signed by Anneliese Vogt and Hamid Qureshi on 2026-07-06, two days before this gate. Of the three gaps, G1 (Tidewater's data-processing clause) is Tidewater-only and does not block Marlowe cohort 1; it is due 2026-07-31, before the first Tidewater cohort, and does not block Marlowe. G2 closed 2026-05-08. G3 (PCI scope reduction not yet evidenced by an assessor, DEP-7) is a post-sunset item and does not block this release either.

## 8. Sign-offs per function

| Function | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| Product | Ife Adeyemi | GO WITH CONDITIONS | C1 and C2 (section 5). Conflict of interest, see note below the table | 2026-07-08 |
| Engineering | Tomasz Wierzbicki | GO WITH CONDITIONS | C1: settlement-file-absent alert live before rollout | 2026-07-08 |
| QA | Noor Haddad | GO | Rehearsal 3 clean (N39); rollback flag flip timed 3 min 50 s, within the 30-minute RTO (N29), rehearsed in pre-production (N40) | 2026-07-08 |
| Design | Ines Castellanos | GO | Reviewed the Kestrel hosted-fields card entry against the current checkout, 2026-07-08. The guest checkout redesign stays out of scope, unaffected by this release | 2026-07-08 |
| Support | Callum Fraser | GO WITH CONDITIONS | C2: finance daily-close runbook published and support briefed before rollout | 2026-07-08 |
| Data | Grace Mbeki | GO | Legacy table shape written unchanged under ADR-0002; reporting is unaffected until DEP-4 migrates it off that shape, due 2027-02-27 | 2026-07-08 |
| Finance | Priya Raman | GO WITH CONDITIONS | C2: finance daily-close runbook published and support briefed; reconciliation within the £50 tolerance (N35) at rehearsal 3 | 2026-07-08 |
| Legal / Compliance | Anneliese Vogt | N/A to this gate | Section 7's AI trigger does not apply, so this row is not required by the template's own condition. The compliance sign-off for PCI DSS, scheme rules, the strong customer authentication requirement (S10, BR-005, N57) and UK GDPR is recorded on the compliance impact assessment | 2026-07-06 |
| Regulatory owner | Hamid Qureshi | GO | Confirms the compliance impact assessment's PCI DSS, scheme rule, strong customer authentication (S10, BR-005, N57) and UK GDPR mapping still holds for Marlowe cohort 1; G1 and G3 do not block this cohort (section 7) | 2026-07-08 |
| Sponsor | Rohan Iyer | N/A to this gate | Accepts Product's decider conflict of interest for this gate (see note below the table) | 2026-07-08 |

Note on the Product row's conflict: Ife Adeyemi, as decider, also owns the completion date that Rohan Iyer, the sponsor, tracks against budget. The conflict is not split for this gate; it is recorded here, and Rohan Iyer accepted it on 2026-07-08, at this gate, in the Sponsor row above. The mitigation in force at this gate is Tomasz Wierzbicki's independent Accountable authority to abort a cohort mid-window (stakeholder map) and the N17 rollback trigger, which lets on-call call a rollback without asking the decider.

## 9. How this gate fails while looking like it passed

Attempt 1 of this gate, twenty-two days earlier (2026-06-16), failed on one of these rows for real (rollback) and on the reconciliation line in section 2, which is why attempt 2 reads them literally rather than as a checklist to nod through.

| Failure mode | What it looked like on attempt 1, and what changed for attempt 2 | The rule that stops it |
|---|---|---|
| Rubber-stamp under date pressure | Attempt 1 was not rubber-stamped: it returned NO-GO in the room, on the day, rather than being waved through toward the 2026-06-27 cutover it was reviewing | Go criterion by criterion, pass or fail, recorded live |
| Empty known-issues table | Section 3 holds three rows, none of them cosmetic: a taxonomy gap, an unverified-at-scale reconciliation path, and a support model with no phone line | Do not accept the gate until the table is populated with severity, owner and mitigation |
| Rollback nobody tested | This is the row attempt 1 failed on. At attempt 1 there was no timed rollback; N40's 3 minute 50 second flag flip exists because attempt 1's NO-GO demanded it before attempt 2 could be scheduled | Require a rehearsal in a real environment, recently, with the elapsed time recorded |
| Sign-off by team, not person | Every row in section 8 carries one name; Product's row names the conflict rather than hiding behind "the team agreed" | Named sign-offs with role and date |
| Conditions agreed aloud | C1 and C2 are written rows with owners and due dates in section 5, not a verbal "we'll sort the alert before launch" | Conditions go in the sign-off row before the meeting ends, or the verdict is not conditional |
| Green dashboard, wrong metric | The dashboard's fourth SLO (every decline carries provider, reason class and trace id) exists specifically because Marlowe logged no declines at all before Quay; a dashboard that only showed uptime would have stayed green through that gap | Name the indicators tied to this release's user-visible behaviour, not only system uptime |
| Decider owns the ship date | True here, and declared rather than concealed: Ife Adeyemi decides this gate and also owns the completion date Rohan Iyer tracks. It is recorded in section 8 rather than split, with Rohan Iyer's own Sponsor row naming his acceptance of the conflict at this gate (2026-07-08), and the independent check this gate does not otherwise have is Tomasz Wierzbicki's separate authority to abort a cohort mid-window plus the N17 rollback trigger, not a later, unrelated decision | Declare it. Split the role for this gate, or record that the conflict was accepted and by whom |
| Gate held after the release | This gate is dated 2026-07-08; cohort 1's first order is 2026-07-13, five days later (N71). The header states the gap in days rather than leaving the reader to infer it, and also owns the earlier D-011 shadow ramp (2026-05-06 to 2026-05-21) as production exposure that predates any Gate 5 attempt, so it is not mistaken for a retroactive sign-off of this gate | The gate is held before any production rollout for the release it authorises. There is no retroactive sign-off |

## Exit gate

- [x] Every checklist box above is checked, or its exception sits in the known-issues table with an owner and a date: sections 1, 4, 5 and 7 checked; in section 2 the edge-case box is unticked with its exceptions in section 3, and the AI box is N/A; section 3 holds the three open exceptions
- [x] The known-issues table is not empty: three rows in section 3, none of them a placeholder
- [x] Every known issue distinguishes itself from a condition: the three rows in section 3 may ship open; C1 and C2 in section 5 may not; closure recorded in the addendum
- [x] The rollback trigger is a condition a dashboard can show, not a feeling: N17's two thresholds, both readable off the Quay operations dashboard; the procedure was executed in pre-production on 2026-07-04 with the elapsed time recorded (N40)
- [x] Every sign-off row has a name and a date, and every conditional verdict has its condition written in the row: ten rows in section 8, four conditional (Product, Engineering, Support, Finance), each naming C1 or C2
- [x] The decider recorded GO, NO-GO, or GO WITH CONDITIONS, with conditions in writing: GO WITH CONDITIONS, C1 and C2, both in section 5
- [x] This gate was held before any production rollout, and the header says so: signed 2026-07-08, cohort 1 begins 2026-07-13, five days later
- [x] Section 7 is answered even where the answer is no, with the reason written: no AI or machine-learning feature; PCI DSS, scheme rules, the strong customer authentication requirement and UK GDPR handled through reg-gap-check and the compliance impact assessment instead, with Hamid Qureshi named as regulatory owner

Signed: Ife Adeyemi, Product Manager, 2026-07-08. See the [Harbourgate journey](harbourgate-journey.md) for the rehearsal that failed, the incident it caused, and the two later Gate 5 attempts this document's shape carried forward to the Tidewater and Kestrel-legacy cohorts.
