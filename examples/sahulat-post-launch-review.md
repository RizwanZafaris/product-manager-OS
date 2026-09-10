# Post-Launch Review: Sahulat Bill Pay

Fills [templates/operate/post-launch-review.md](../templates/operate/post-launch-review.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the Sahulat journey rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Launch date:** 2026-07-06 · **Review date:** 2026-08-21 · **Status:** Reviewed; feeds Gate 6 attempt 1 (PIVOT, decision D8), signed 2026-08-28, a week after this review
**Inputs:** the [Sahulat journey](sahulat-journey.md) data sheet, its DELIVER and OPERATE timeline · the [one-pager](sahulat-one-pager.md) sections 4 and 7 · launch dashboard LD-1 (M1, M3, N47, N48 daily)

## 1. Launch facts

- What shipped, one sentence: USSD and app bill lookup and payment for a Ravi Power electricity bill or a Chenab Gas bill, funded from wallet balance or a same-visit agent cash-in, with a saved bill reference, a reminder SMS three days before a saved bill's due date, an SMS payment reference, and a status message when a session drops mid-payment (SAHULAT-S1, S2, S3, S5, S6, S8, S9, S10, S11, all nine Rel-1 stories; 9 of the squad's 28 engineer-weeks went to the balance-first slice, S5, S10 and S11, N54); Mehran Water (SAHULAT-S7) was dropped from Rel-1 by decision D5 after three of ten test bills failed reference validation.
- The one launch metric, from the north star sheet's guardrail table, the instrument this product uses in place of a separate GTM plan: M3, USSD bill-pay session completion. Stop condition set then: must not fall below 90 percent, halt-caller Zainab Qureshi.
- Rollout shape as it actually happened: staged per decision D6, 600 pilot agents in the Lahore district on 2026-07-06. A bill-peak day on 2026-07-08 produced the first float stockouts (N52), and a USSD timeout spike on 2026-07-09 took M3 to 87 percent for the week (N46). Zainab Qureshi paused the planned nationwide step for four days under decision D7 on 2026-07-10 while the timeout fix shipped; the fix landed 2026-07-14, the same day the daily reconciliation caught and explained the one unexplained trust-account break in the window (N48). Gate 5's CONDITIONAL GO condition, the agent float top-up hotline, went live 2026-07-17, and the nationwide step followed on 2026-07-24. The review window set at Gate 5 (N55, launch plus six weeks) closed 2026-08-17; this review was held four days later, on day 46 after launch, later than this template's usual two-to-six-week window by design, not drift.

## 2. Goal vs actual

All figures below are ILLUSTRATIVE, from the Sahulat data sheet; targets are quoted unchanged from the [one-pager](sahulat-one-pager.md) section 4, the DEFINE-stage document (Gate 2 attempt 2, amended 2026-05-21 under D5) that Gate 5 relied on.

| Metric | Target at Gate 5 (quoted from doc) | Actual at review | Delta | Data confidence |
|---|---|---|---|---|
| Gate 1 success signal (quoted from `gates/gate-1-attempt-2.md`, 2026-02-27) | "a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month" | Open: Sara Lodhi; the data sheet has no query for this outcome-level signal | Open | Open |
| M1: bills paid per month (N42) | "40,000 bills paid in the four weeks to 2026-08-16" | 31,200 bills, four weeks to 2026-08-16, core ledger query M1 | -8,800 bills, 78 percent of target | measured |
| M2: share of bill payments funded from a balance held more than 48 hours, the balance-first hypothesis (N43) | "50 percent of bill payments, same four-week window" | 9 percent, query FP-01; 78 percent were instead funded by a cash-in within two hours of the payment (N44) | -41 points, 18 percent of target | measured |
| Guardrail M3: USSD bill-pay session completion (N46) | "Must not fall below 90 percent" | Week 1: 87 percent, a breach; at review: 92 percent | Week 1: 3 points below the floor; D7 paused the nationwide step 4 days; 2 points clear at review | measured |
| Guardrail M4: pass-through share, a cash-in fully cashed out within 48 hours (N10, N11) | "Must not rise above 61 percent" | 58 percent, four weeks to 2026-08-16, query PT-01 | -3 points; guardrail held | measured |

Two qualifiers this table alone would hide. First, 24,600 wallets paid at least one bill, 5.8 percent of the 422,000 wallets active in the trailing 30 days at review (N53 against N3); M1's shortfall is a reach problem, not only a hypothesis one. Second, the board's key result is scored on its own metric, 30-day active wallets: 422,000 at review (N3) against the 520,000 target (N4), up from 410,000 in December 2025 (N2), still 98,000 short. Separately, the north star (M5) rose from 96,000 wallets in December 2025 (N14) to 118,000 at review (N15), a gain of 22,000; about a third of that gain was already in the pre-launch trend (N16, estimate, Sara Lodhi's slope from January to June 2026, low to medium confidence), so at most two-thirds of the 22,000 is plausibly this launch's. This review does not credit the whole 22,000 to bill pay, and does not credit any of it toward the 520,000 key result, which is scored above on its own metric.

## 3. What worked, what did not

- Worked: the M3 guardrail recovered from an 87 percent week-1 breach to 92 percent at review, after the timeout fix and D7's four-day pause (N46), on dashboard LD-1.
- Worked: the M4 guardrail held, pass-through falling from 61 to 58 percent (N10, N11), the direction the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) card asks this number to move.
- Worked: UAT closed three severity-1 defects before launch, 2026-06-15 to 2026-06-24 (N51).
- Worked: the rollback rehearsal ran clean in nine minutes in pre-production, 2026-06-22 (N50); it was not invoked during the window, but it was ready.
- Worked: Gate 5's CONDITIONAL GO condition, the float top-up hotline, closed on the date set, 2026-07-17 (Gate 5 attempt 1 condition, per the timeline).
- Did not: M1 missed by 8,800 bills (N42), and M2 missed badly, 9 percent against 50 (N43), the balance-first hypothesis this product was designed around.
- Did not: week 1 carried an operational cost the target sheet never priced: 61 duplicate-payment tickets against 3 by week 6, 11 on-call pages against 1, and 2 incidents in the window (N47, N49).
- Did not: 38 of the 600 pilot agents reported a float stockout on a bill-peak day inside launch week, 2026-07-08 (N52); the launch itself fell inside the 5th-to-10th bill-peak window (N57), before the hotline meant to prevent it existed.
- Did not: 9 of the squad's 28 engineer-weeks (N54) and PKR 480,000 of launch SMS (N41) went to the balance-first funding path this review found used by 9 percent of payments (N43).
- Would do differently next launch: name the process step that permitted the miss, not only the miscalibration downstream of it. Rel-1 scope, including the balance-first stories SAHULAT-S5, S10 and S11, was signed at Gate 2 on 2026-03-25, before the research plan's own falsification rule was checked against it: fewer than three of eight balance-keepers should have kept those stories out of Rel-1, and two of eight kept a balance (N26). The DESIGN premortem then compounded that gap on 2026-04-08, scoring R6 at likelihood 2 of 5 on the same two interviews, INT-003 and INT-006, that persona P3, Kamran, rests on and that carried no validate-by date, while 6 of 8 customer sessions described money leaving the wallet the day it arrived (theme T2). Gate 2 signing scope against the plan's own rule is what section 5 has to answer for first; the premortem score is what made the miss worse.

## 4. Customer feedback

All counts below are ILLUSTRATIVE, from the data sheet's support-system tags and agent debrief notes.

| Source (tickets / interviews / reviews / sales) | Theme | Count | One verbatim quote |
|---|---|---|---|
| Pilot agent debriefs, 2026-07-27 | Customers ask for a paper slip; an SMS reference does not read as proof | Raised in 5 of 6 pilot agent debriefs (N60) | "They still ask me for a chit before they leave the counter. An SMS is not something they can show their landlord." (agent debrief, 2026-07-27, N60) |
| Support tickets, tag DUP-PAY | Fear that a dropped session paid twice | 61 tickets week 1, 3 week 6 (N47) | "It says paid on my phone twice. Please check before you take the money again." (support ticket, tag DUP-PAY, week 1, N47) |
| Agent helpline, tag FLOAT-OUT | Agent's e-money float ran out, so the cash-in could not be credited and the bill could not be paid in the same visit | 38 of 600 pilot agents, 2026-07-08 (N52) | "Customers bring cash for the bill but my float was finished by noon." (agent helpline, tag FLOAT-OUT, 2026-07-08, N52) |
| Support tickets | Requests to add Mehran Water, dropped from Rel-1 by decision D5 | 6 tickets in six weeks (N59) | "Can I pay my water bill here too, or only electricity and gas?" (support ticket, N59) |

The feedback we expected but did not get: almost nothing about the reminder SMS or saving a bill reference, the pieces of SAHULAT-S11 and S5 the balance-first design leaned on hardest. Feedback clustered on the counter instead: float, a paper receipt, a missing biller. Read beside section 5's field observation, that absence is itself a finding: customers are not experiencing this feature at the reminder SMS or the saved-reference step, the way the design assumed they would.

## 5. Premortem reconciliation

All likelihood and impact scores below are ILLUSTRATIVE, on a 1-to-5 scale, from the DESIGN-stage premortem of 2026-04-08.

| Failure mode | Predicted? | Arrived? | What we change because of it |
|---|---|---|---|
| R1: agent float runs out on bill-peak days, so the same-visit cash-in fails at the counter (4x4, owner Tariq Sohail) | yes | yes: 38 of 600 pilot agents on 2026-07-08 (N52) | The hotline arrived nine days after this risk first landed, not before it. Open: Tariq Sohail owns whether it needs its own response-time guardrail before the next bill-peak run, the 5th to 10th of the month (N57); the August 5th-to-10th peak, the first at nationwide scale, has no FLOAT-OUT reading in this review. |
| R2: a USSD session times out mid-payment and the customer pays twice (4x4, owner Zainab Qureshi) | yes | yes: M3 at 87 percent, 61 duplicate tickets in week 1 (N46, N47), the AC-8 resume-half gap Gate 4 had accepted as a miss coming due | Fix shipped 2026-07-14; tickets fell to 3 by week 6, and D7's pause is why this did not compound at nationwide scale. Still owed: the AC-8 resume-on-next-dial half, the Gate 4 miss deferred to Rel-2 with Zainab Qureshi as owner, is the root cause of both R2 and D7 and has not yet shipped. |
| R3: BillBridge posts late to a biller and a surcharge lands despite the payment (2x4, owner Hira Baig); AC-9's 24-hour reversal answers the [payments acquiring](../knowledge/domains/payments-acquiring.md) card's question about fulfilment failing after approval | yes | no: zero confirmed cases; four tickets alleged a late posting and are not yet checked against BillBridge's log (unverified) | Nothing structural so far. The four unconfirmed tickets stay open against BillBridge's log rather than folding into a count that overstates this risk; see the follow-up in section 6. |
| R4: a trust-account reconciliation break from an aggregator retry (3x3, owner Bilal Hasan) | yes | yes, once: PKR 12,300 unexplained on 2026-07-14, traced within the day to a BillBridge retry posting twice (N48) | Nothing structural in the guardrail itself; the zero-break floor held every other day and same-day tracing is the design working. Follow-up: confirm with BillBridge that its retries are idempotent, so a retry cannot post twice again; owner Bilal Hasan. |
| R5: Falak Telecom delays the USSD menu change past UAT (3x3, owner Zainab Qureshi) | yes | no: DEP-2 landed five days late, 2026-06-19 against a 2026-06-14 need-by, but inside the UAT window (2026-06-15 to 2026-06-24) | Nothing for this launch. The next pass's DESIGN stage should still name Falak Telecom's lead time as a watch item; one pass inside UAT's slack is not proof the margin holds twice. |
| R6: customers do not hold a balance, so paying from balance is used by few (2x5, owner Hira Baig); M2's hypothesis restated as a risk | yes, scored low | yes, worse than scored: 9 percent against 50 (N43) | The scoring is the lesson, but Gate 2 is the step that let it happen. Rel-1 scope, with SAHULAT-S5, S10 and S11 in it, was signed at Gate 2 on 2026-03-25, before the research plan's own falsification rule, fewer than three of eight balance-keepers keeps the balance-first stories out of Rel-1, was checked against it; two of eight kept a balance (N26). The DESIGN premortem then compounded that gap on 2026-04-08, scoring R6 at likelihood 2 of 5 against P3, Kamran, whose label also carried no validate-by date. The room believed in Kamran anyway; the wider sample already said otherwise, including the line requoted here from six and a half months earlier: "I only put money in the phone when I need to send it that day. Why would I leave it there?" (E2, INT-004, 2026-02-02). Process change: Gate 2 must check the research plan's falsification results against any proposed scope before signing it, and a premortem score resting on an ASSUMPTION-labelled persona must cite its session count and any pre-registered falsification result before the score is accepted. This review recommends PIVOT away from the design this risk was scored against; Gate 6 decided D8 on 2026-08-28. |
| Not predicted: agent-assisted bill pay, the agent performing the lookup and payment on the customer's phone or their own handset | no, though RQ3's open remainder (whether an agent would rather perform the payment was not asked) and E3 pointed at it | yes: 41 of 53 observed payments across 12 counters, 2026-08-11 and 2026-08-12 (N45, measured, observed, small sample: 12 counters, two days; the next DISCOVER pass should test this at wider scale) | This is the shape this review recommends and Gate 6 decided as D8 on 2026-08-28: the design target for DISCOVER opening 2026-09-07, and the reason section 6 moves an agent-facing story up the list and opens a commission line agents have gone six weeks without. |
| Not predicted: customers ask agents for a paper slip; an SMS reference does not read as proof | no | yes: raised in 5 of 6 pilot agent debriefs, 2026-07-27 (N60) | Undercuts the assumption that the wallet alone is the record and the receipt. Follow-up: a printable or agent-handset receipt for the next DISCOVER pass; owner Hira Baig or Tariq Sohail. |

## 6. Follow-ups

| Item | Lands in (linked doc or ticket) | Owner | Date |
|---|---|---|---|
| Commission schedule v8, a bill-pay assistance line (PKR 5 per bill proposed, N39) paying agents for assistance the current schedule does not recognize | dependency register, DEP-4 v8 | Bilal Hasan | 2026-09-30 |
| Float top-up hotline response-time guardrail, given R1 arrived at pilot scale before the hotline was live | risk register, R1 | Tariq Sohail | 2026-09-05 |
| Reframe the next DISCOVER pass around Rafiq, persona P2 the agent, not Kamran, persona P3 the assumption R6 disproved | product README, next DISCOVER pass | Hira Baig | 2026-09-07 |
| Move SAHULAT-S4, the agent-handset payment confirmation, from a Rel-2 should toward the next pass's walking skeleton, following N45 | user stories, next revision | Hira Baig | 2026-09-07 |
| Close the four unconfirmed R3 late-posting tickets against BillBridge's own log before filing them inconclusive | risk register, R3, plus the support tickets alleging late posting (ids not on the data sheet) | Hira Baig | 2026-08-28 |
| AC-8 resume-on-next-dial half, the deferred Gate 4 miss and root cause of R2 and D7 | acceptance criteria; Rel-2 backlog | Zainab Qureshi | Open: Zainab Qureshi, no date fixed |
| Confirm with BillBridge that its retries are idempotent, so a retry cannot post twice again | risk register, R4 | Bilal Hasan | Open: Bilal Hasan, no date fixed |
| Printable or agent-handset receipt for the paper-slip finding (N60) | user stories, next revision | Hira Baig or Tariq Sohail | 2026-09-07 |
| First recurring metrics review, the cadence instrument this one-time review hands off to | metrics-review.md, north star sheet cadence | Hira Baig | 2026-09-21 |

## How this review fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Only the wins are reviewed | Every section reports something that went well | Name at least one thing that came in under its target, or the review is not finished |
| The target moved after the fact | "What we really wanted was a smaller number", said afterwards | The target and the definition of success are locked before launch and quoted here unchanged |
| Everything is attributed to the launch | Any movement in the period is credited to the release | State what the metric would plausibly have done anyway, and say how confident you are |
| Nothing is decided | The document ends in thanks and a list of observations | Close with named owners, dated actions, and a date to re-check |
| Held too late to remember | Six weeks after launch, and nobody can recall what shipped | Hold it within about two weeks of the launch window closing |
| Blame lands on a person | The review names who missed rather than what allowed the miss | Name the step in the process that permitted it, and the change to that step |

## Exit gate

This review is done when:

- [x] Every target in section 2 is quoted from a Gate 5 era document. Quoted verbatim from the one-pager (Gate 2 attempt 2, amended 2026-05-21 under D5), a document already in force when Gate 5 attempt 1 ran on 2026-07-01 and unchanged since; that amendment date, six weeks ahead of Gate 5, is what makes it a Gate 5 era document and satisfies this box. This review does not separately verify whether `gates/gate-5-attempt-1.md` itself restates M1 to M4; the one-pager quoted above is the source of record either way.
- [x] Worked and did-not lists both have entries with evidence, covering product and process. Section 3 carries five worked items and four did-not items, each with a cited row id, and covers the metrics and the process around UAT, rollback and the hotline condition.
- [x] The premortem table has a row for every arrived failure, predicted or not. Section 5 carries R1 through R6 plus the unpredicted agent-assisted row (N45) and the unpredicted paper-slip row (N60).
- [x] Every follow-up has left this file for an owned destination. All nine rows in section 6 name an owner and a destination register; two carry an open date rather than a fixed one, and each still names who owns closing it.
- [x] The recurring metrics review cadence is scheduled, with its first date set. Section 6's last row: 2026-09-21, owner Hira Baig.

*Amendment, 2026-08-28: every reference to D8 above records this review's recommendation, endorsed by Gate 6 attempt 1 as PIVOT that day, a week after this review was held and signed.*

Signed: Faisal Mirza, Chief Executive and sponsor, 2026-08-21. Hira Baig, product owner, presented the findings above. Gate 6 itself is a separate, later event: attempt 1 on 2026-08-28 records decision D8, PIVOT to agent-assisted bill pay, in `gates/gate-6-attempt-1.md` in the product workspace, built on this review rather than repeating it.
