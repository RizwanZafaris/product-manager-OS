# Post-Launch Review: Sahulat Bill Pay

Fills [templates/operate/post-launch-review.md](../templates/operate/post-launch-review.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the Sahulat journey rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Launch date:** 2026-07-06 · **Review date:** 2026-08-21 · **Status:** Reviewed; feeds Gate 6 attempt 1 (PIVOT, decision D8), signed 2026-08-28, a week after this review
**Inputs:** the [Sahulat journey](sahulat-journey.md) data sheet, its DELIVER and OPERATE timeline · the [one-pager](sahulat-one-pager.md) sections 4 and 7 · launch dashboard LD-1 (M1, M3, N47, N48 daily)

## 1. Launch facts

- What shipped, one sentence: USSD bill lookup and payment for a Ravi Power electricity bill or a Chenab Gas bill, funded from wallet balance or a same-visit agent cash-in, with an SMS payment reference and a status message when a session drops mid-payment (SAHULAT-S1, S2, S3, S6, S8, S9); Mehran Water (SAHULAT-S7) was dropped from Rel-1 by decision D5 after three of ten test bills failed reference validation.
- The one launch metric, from the north star sheet's guardrail table, the instrument this product uses in place of a separate GTM plan: M3, USSD bill-pay session completion. Stop condition set then: must not fall below 90 percent, halt-caller Zainab Qureshi.
- Rollout shape as it actually happened: staged per decision D6, 600 pilot agents in the Lahore district on 2026-07-06. A bill-peak day on 2026-07-08 produced the first float stockouts (N52), and a USSD timeout spike on 2026-07-09 took M3 to 87 percent for the week (N46). Zainab Qureshi paused the planned nationwide step for four days under decision D7 on 2026-07-10 while the timeout fix shipped; the fix landed 2026-07-14, the same day the daily reconciliation caught and explained the one unexplained trust-account break in the window (N48). Gate 5's CONDITIONAL GO condition, the agent float top-up hotline, went live 2026-07-17, and the nationwide step followed on 2026-07-24. The review window set at Gate 5 (N55, launch plus six weeks) closed 2026-08-17; this review was held four days later.

## 2. Goal vs actual

All figures below are ILLUSTRATIVE, from the Sahulat data sheet; targets are quoted unchanged from the [one-pager](sahulat-one-pager.md) section 4, the DEFINE-stage document (Gate 2 attempt 2, amended 2026-05-21 under D5) that Gate 5 relied on without restating.

| Metric | Target at Gate 5 (quoted from doc) | Actual at review | Delta | Data confidence |
|---|---|---|---|---|
| M1: bills paid per month (N42) | "40,000 bills paid in the four weeks to 2026-08-16" | 31,200 bills, four weeks to 2026-08-16, core ledger query M1 | -8,800 bills, 78 percent of target | measured |
| M2: share of bill payments funded from a balance held more than 48 hours, the balance-first hypothesis (N43) | "50 percent of bill payments, same four-week window" | 9 percent, query FP-01; 78 percent were instead funded by a cash-in within two hours of the payment (N44) | -41 points, 18 percent of target | measured |
| Guardrail M3: USSD bill-pay session completion (N46) | "Must not fall below 90 percent" | Week 1: 87 percent, a breach; at review: 92 percent | Breached 4 days under D7, then 2 points clear | measured |
| Guardrail M4: pass-through share, a cash-in fully cashed out within 48 hours (N10, N11) | "Must not rise above 61 percent" | 58 percent, four weeks to 2026-08-16, query PT-01 | -3 points; guardrail held | measured |

Two qualifiers this table alone would hide. First, 24,600 wallets paid at least one bill, 5.8 percent of the 422,000 wallets active in the trailing 30 days at review (N53 against N3); M1's shortfall is a reach problem, not only a hypothesis one. Second, the north star (M5) rose from 96,000 wallets in December 2025 (N14) to 118,000 at review (N15), a gain of 22,000 against the board's 520,000 key result (N4); about a third of that gain was already in the pre-launch trend (N16, Sara Lodhi's slope, January to June 2026), so at most two-thirds, roughly 15,000 wallets, is plausibly this launch's. This review does not credit the whole 22,000 to bill pay.

## 3. What worked, what did not

- Worked: the M3 guardrail recovered from an 87 percent week-1 breach to 92 percent at review, after the timeout fix and D7's four-day pause (N46), on dashboard LD-1.
- Worked: the M4 guardrail held, pass-through falling from 61 to 58 percent (N10, N11), the direction the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) card asks this number to move.
- Worked: UAT closed three severity-1 defects before launch (N51), and the rollback rehearsal ran clean in nine minutes (N50); neither was needed in anger during the window, but both were ready.
- Worked: Gate 5's CONDITIONAL GO condition, the float top-up hotline, closed on the date set, 2026-07-17.
- Did not: M1 missed by 8,800 bills (N42), and M2 missed badly, 9 percent against 50 (N43), the balance-first hypothesis this product was designed around.
- Did not: week 1 carried an operational cost the target sheet never priced: 61 duplicate-payment tickets against 3 by week 6, 11 on-call pages against 1, and 2 incidents in the window (N47, N49).
- Did not: 38 of the 600 pilot agents reported a float stockout on the one bill-peak day inside launch week, 2026-07-08 (N52), before the hotline meant to prevent it existed.
- Would do differently next launch: score a risk against the evidence's actual reach, not the persona it protects. R6 was scored likelihood 2 of 5 on the same two interviews, INT-003 and INT-006, that persona P3, Kamran, rests on, while 6 of 8 customer sessions described money leaving the wallet the day it arrived (theme T2); the risk arrived at more than twice its scored likelihood, and that miscalibration is what section 5 has to answer for.

## 4. Customer feedback

All counts below are ILLUSTRATIVE, from the data sheet's support-system tags and agent debrief notes.

| Source (tickets / interviews / reviews / sales) | Theme | Count | One verbatim quote |
|---|---|---|---|
| Pilot agent debriefs, 2026-07-27 | Customers ask for a paper slip; an SMS reference does not read as proof | Raised in 5 of 6 pilot agent debriefs (N60) | "They still ask me for a chit before they leave the counter. An SMS is not something they can show their landlord." |
| Support tickets, tag DUP-PAY | Fear that a dropped session paid twice | 61 tickets week 1, 3 week 6 (N47) | "It says paid on my phone twice. Please check before you take the money again." |
| Agent helpline, tag FLOAT-OUT | Agent had no cash to complete a same-visit cash-in and bill payment | 38 of 600 pilot agents, 2026-07-08 (N52) | "The agent said the machine shows I can pay, but he has no cash to give me. Come back tomorrow." |
| Support tickets | Requests to add Mehran Water, dropped from Rel-1 by decision D5 | 6 tickets in six weeks (N59) | "Can I pay my water bill here too, or only electricity and gas?" |

The feedback we expected but did not get: almost nothing about the reminder SMS or saving a bill reference, the pieces of SAHULAT-S11 and S5 the balance-first design leaned on hardest. Feedback clustered on the counter instead: float, a paper receipt, a missing biller. Read beside section 5's field observation, that absence is itself a finding: customers are not experiencing this feature at the reminder screen the design assumed they would use.

## 5. Premortem reconciliation

All likelihood and impact scores below are ILLUSTRATIVE, on a 1-to-5 scale, from the DESIGN-stage premortem of 2026-04-08.

| Failure mode | Predicted? | Arrived? | What we change because of it |
|---|---|---|---|
| R1: agent float runs out on a bill-peak day, so the same-visit cash-in fails at the counter (4x4, owner Tariq Sohail) | yes | yes: 38 of 600 pilot agents on 2026-07-08 (N52) | The hotline arrived nine days after this risk first landed, not before it. Open: Tariq Sohail owns whether it needs its own response-time guardrail before the next bill-peak run, the 5th to 10th of the month (N57). |
| R2: a USSD session times out mid-payment and the customer pays twice (4x4, owner Zainab Qureshi) | yes | yes: M3 at 87 percent, 61 duplicate tickets in week 1 (N46, N47), the AC-8 resume-half gap Gate 4 had accepted as a miss coming due | Fix shipped 2026-07-14; tickets fell to 3 by week 6. Nothing further owed; D7's pause is why this did not compound at nationwide scale. |
| R3: BillBridge posts late to a biller and a surcharge lands despite the payment (2x4, owner Hira Baig); AC-9's 24-hour reversal answers the [payments acquiring](../knowledge/domains/payments-acquiring.md) card's question about fulfilment failing after approval | yes | no: zero confirmed cases; four tickets alleged a late posting, none matched to a post outside BillBridge's 30-minute SLA once checked | Nothing structural. The four unconfirmed tickets close as inconclusive rather than fold into a count that overstates this risk. |
| R4: a trust-account reconciliation break from an aggregator retry (3x3, owner Bilal Hasan) | yes | yes, once: PKR 12,300 unexplained on 2026-07-14, traced within the day to a BillBridge retry posting twice (N48) | Nothing structural; the zero-break guardrail held every other day, and same-day tracing is the design working, not a gap. |
| R5: Falak Telecom delays the USSD menu change past UAT (3x3, owner Zainab Qureshi) | yes | no: DEP-2 landed five days late, 2026-06-19 against a 2026-06-14 need-by, but inside the UAT window (2026-06-15 to 2026-06-24) | Nothing for this launch. The next pass's DESIGN stage should still name Falak Telecom's lead time as a watch item; one pass inside UAT's slack is not proof the margin holds twice. |
| R6: customers do not hold a balance, so few pay from one (2x5, owner Hira Baig); M2's hypothesis restated as a risk | yes, scored low | yes, worse than scored: 9 percent against 50 (N43) | The scoring is the lesson, not only the miss. The room believed in Kamran; the wider sample already said otherwise, including the line requoted here from six and a half months earlier: "I only put money in the phone when I need to send it that day. Why would I leave it there?" (E2, INT-004, 2026-02-02). D8 pivots away from the design this risk was scored against. |
| Not predicted: agent-assisted bill pay, the agent performing the lookup and payment on the customer's phone or their own handset | no | yes: 41 of 53 observed payments across 12 counters, 2026-08-11 and 2026-08-12 (N45) | This is the shape D8 pivots toward, the design target for DISCOVER opening 2026-09-07, and the reason section 6 moves an agent-facing story up the list and opens a commission line agents have gone six weeks without. |

## 6. Follow-ups

| Item | Lands in (linked doc or ticket) | Owner | Date |
|---|---|---|---|
| Commission schedule v8, a bill-pay assistance line (PKR 5 per bill proposed, N39) paying agents for assistance the current schedule does not recognize | dependency register, DEP-4 v8 | Bilal Hasan | 2026-09-30 |
| Float top-up hotline response-time guardrail, given R1 arrived at pilot scale before the hotline was live | risk register, R1 | Tariq Sohail | Open: Tariq Sohail, no date fixed |
| Reframe the next DISCOVER pass around Rafiq, persona P2 the agent, not Kamran, persona P3 the assumption R6 disproved | product README, next DISCOVER pass | Hira Baig | 2026-09-07 |
| Move SAHULAT-S4, the agent-handset payment confirmation, from a Rel-2 should toward the next pass's walking skeleton, following N45 | user stories, next revision | Hira Baig | 2026-09-07 |
| Close the four unconfirmed R3 late-posting tickets against BillBridge's own log before filing them inconclusive | decision log, risk register R4 | Hira Baig | Open: Hira Baig, no date fixed |
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

- [ ] Every target in section 2 is quoted from a Gate 5 era document. Quoted verbatim, but honestly from the one-pager (Gate 2 attempt 2, amended 2026-05-21): Gate 5 attempt 1 relied on those targets without restating them in a document of its own, so no document authored at Gate 5 itself carries these numbers.
- [x] Worked and did-not lists both have entries with evidence, covering product and process. Section 3 carries four worked items and three did-not items, each with a cited row id, and covers the metrics and the process around UAT, rollback and the hotline condition.
- [x] The premortem table has a row for every arrived failure, predicted or not. Section 5 carries R1 through R6 plus the unpredicted agent-assisted row N45 surfaced.
- [x] Every follow-up has left this file for an owned destination. All six rows in section 6 name an owner and a destination register; two carry an open date rather than a fixed one, and both still name who owns closing it.
- [x] The recurring metrics review cadence is scheduled, with its first date set. Section 6's last row: 2026-09-21, owner Hira Baig.

Signed: Faisal Mirza, Chief Executive and sponsor, 2026-08-21. Hira Baig, product owner, presented the findings above. Gate 6 itself is a separate, later event: attempt 1 on 2026-08-28 records decision D8, PIVOT to agent-assisted bill pay, in `gates/gate-6-attempt-1.md` in the product workspace, built on this review rather than repeating it.
