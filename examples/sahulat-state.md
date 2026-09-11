# STATE: Sahulat Bill Pay

Fills [templates/execution/state.md](../templates/execution/state.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-03-25 · **Status:** Written at Gate 2 attempt 2 (SIGNED); read first by any runtime resuming this product, and at every gate in [STAGE-GATES](../os/STAGE-GATES.md)

## Position

Stage: DEFINE
Gate attempts: Gate 1 attempt 1 on 2026-02-20 MORE DISCOVERY; Gate 1 attempt 2 on 2026-02-27 GO; Gate 2 attempt 1 on 2026-03-18 RETURNED for adjectives; Gate 2 attempt 2 on 2026-03-25 SIGNED
Next question: DESIGN-1, how bill pay is integrated and what happens when an approved payment's fulfilment fails afterward
Overlays active: AI: no; regulated: yes (State Bank of Pakistan EMI Regulations, Amna Rasheed as regulatory owner), decided at 2026-03-05, logged as D2
Domain: [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) and [payments acquiring](../knowledge/domains/payments-acquiring.md)

## Accepted answers

| ID | Question (short) | Answer (one line) | Evidence class | Landed in |
|---|---|---|---|---|
| A1 | Is bill pay worth discovery effort over a keep-balance cashback promotion? | Yes; discovery opens on bill pay, not on a promotion (D1, Faisal Mirza, 2026-01-16) | verified | sahulat-opportunity-assessment.md section 9, decision log D1 |
| A2 | What artifact weight does a regulator-in-scope call for? | One-pager with user stories and acceptance criteria attached, not the full BRD/PRD/FRD stack (D2, Hira Baig, 2026-03-05, over Amna Rasheed's objection; resolution carried as DEP-3) | single-source | sahulat-one-pager.md, sahulat-user-stories.md, sahulat-acceptance-criteria.md |
| A3 | Who is the product for? | P1 Shazia, the household bill-runner, on six sessions, and P2 Rafiq, the corner-shop agent, on six; P3 Kamran carries the ASSUMPTION label on two sessions only | verified (P1, P2); contested (P3) | sahulat-personas.md |
| A4 | What problem sentence did Gate 1 accept? | A bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month (the outcome signal O1, rewritten from usage at Gate 1 attempt 2) | verified | gates/gate-1-attempt-2.md, sahulat-one-pager.md section 4 |
| A5 | How will we know it worked? | M1: 40,000 bills paid per month; M2: 50 percent of bill payments funded from a balance held more than 48 hours; guardrails M3 (USSD completion floor 90 percent) and M4 (pass-through share must not rise above 61 percent) | target | sahulat-one-pager.md section 4 |
| A6 | What is the Rel-1 customer fee? | PKR 0 per bill (D4, Faisal Mirza, 2026-03-20) | decided | decision log D4, sahulat-one-pager.md section 5 |
| A7 | Which aggregator rail do we integrate? | Not yet answered; deferred to DESIGN-1. No term sheet yet at this snapshot | unverified | none yet |

## Open challenges

| ID | Answer offered | Why not accepted | Pushes used (n of 2) | Parked to |
|---|---|---|---|---|
| C1 | "Promptly" as a criterion threshold (AC-3 SMS confirmation) | No digit in it; Gate 2 attempt 1 returned the whole packet for adjectives | 2 of 2 | Resolved at Gate 2 attempt 2: AC-3 now reads "within 60 seconds" (N56) |
| C2 | "The session should recover gracefully" as a guardrail | No digit in it; same return reason as C1 | 2 of 2 | Resolved at Gate 2 attempt 2: AC-8 status SMS within 2 minutes, AC-10 duplicate blocked within 24-hour window (N56) |
| C3 | Full BRD/PRD/FRD stack because a regulator is in scope (Amna Rasheed's objection to D2) | Hira Baig decided one-pager weight with compliance memo as DEP-3; objection recorded in the decision log, not overturned | 1 of 2 | sahulat-decision-log.md D2; DEP-3 needed by 2026-05-29 |
| C4 | Kamran as a design persona justifying balance-first work | Only two sessions (INT-003, INT-006) behind him; labelled ASSUMPTION at creation but designed for anyway; the vision's non-goal requires three of eight or more holding a balance, which N26 (2 of 8) does not clear | 1 of 2 | sahulat-personas.md P3; risk R6 (scored 2 x 5 at premortem); M2 target set where the bet has to be true so the review can falsify it |

*Push rule:* Each open challenge allows a maximum of 2 pushes. A push is a re-submission of the answer to the gate or reviewer after modification. When 2 of 2 are used without resolution, the item is parked to a named artifact or dependency. When resolved before the limit, the remaining count reflects the actual submissions made.

## Evidence ledger

| E# | Claim | Verbatim quote | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| E1 | Weekend due dates produce surcharges even when the customer tries to pay | "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." | INT-004 (C-04), interview notes section 8 | 2026-02-02 | 2026-02-16 | measured, shown |
| E2 | Customers do not hold a balance between transactions | "I only put money in the phone when I need to send it that day. Why would I leave it there?" | INT-004 (C-04), interview notes section 8 | 2026-02-02 | 2026-02-16 | measured, told |
| E3 | Agents field bill questions daily and refer customers to a shop | "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." | INT-011 (A-03), research plan | 2026-02-04 to 2026-02-13 | 2026-02-16 | measured, told |
| E4 | A dropped USSD session produces a blind repeat dial | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." | INT-007 (C-07), research plan section 5 | 2026-02-06 | 2026-02-16 | measured, told |
| E5 | One customer holds a salary balance in the wallet | "I keep two or three thousand in it because my salary comes there." | INT-003 (C-03), personas P3 behaviors | 2026-01-29 | 2026-02-17 | measured, told; single-source under P3 |
| E6 | Pass-through rate at baseline | "61 percent of cash-ins were fully cashed out again within 48 hours" | Core ledger, query PT-01, Q4 2025 | 2025-12-31 | 2026-01-12 | measured |
| E7 | Helpline demand signal | "412 agent-helpline calls in four weeks asking whether Sahulat could pay a utility bill" | Agent helpline, tag BILL-ASK | 2026-01-09 | 2026-01-12 | measured |

## Journal

2026-01-12, Hira Baig, trigger identified (N13, N10 side by side), no artifacts touched
2026-01-15, Hira Baig, opportunity assessment written, riskiest assumption named, sahulat-opportunity-assessment.md
2026-01-16, Hira Baig, D1 logged, decision log
2026-01-19, Hira Baig, research plan status Planned, sahulat-user-research-plan.md
2026-01-26 to 2026-02-13, Hira Baig and Usman Javed, INT-001 to INT-014 conducted, guide revised v1 to v2 (leading question cut), sahulat-interview-guide.md, sahulat-interview-notes.md
2026-02-16, Hira Baig, synthesis day, problem framing and empathy map, sahulat-problem-framing.md
2026-02-17, Hira Baig, personas P1 P2 P3 (ASSUMPTION), sahulat-personas.md
2026-02-20, Hira Baig, Gate 1 attempt 1 MORE DISCOVERY, gates/gate-1-attempt-1.md
2026-02-27, Hira Baig, Gate 1 attempt 2 GO signed, gates/gate-1-attempt-2.md
2026-03-02, Hira Baig, vision written, sahulat-vision.md
2026-03-04, Hira Baig, north star sheet written, sahulat-north-star-metric.md
2026-03-05, Hira Baig, D2 logged (artifact weight override), decision log
2026-03-09, Hira Baig, one-pager drafted, sahulat-one-pager.md
2026-03-11, Hira Baig, user stories drafted, sahulat-user-stories.md
2026-03-13, Hira Baig, acceptance criteria drafted, sahulat-acceptance-criteria.md
2026-03-18, Hira Baig, Gate 2 attempt 1 RETURNED for adjectives, gates/gate-2-attempt-1.md
2026-03-20, Hira Baig, D4 logged (customer fee PKR 0), decision log
2026-03-25, Hira Baig, Gate 2 attempt 2 SIGNED, gates/gate-2-attempt-2.md, this file created

---

## Exit gate walk (feeds Gate 3: design reviewed and accepted)

This state file is fit to hand to DESIGN when:

- [x] Stage is stated and matches the last gate outcome. DEFINE, after Gate 2 attempt 2 SIGNED on 2026-03-25
- [x] Every accepted answer names where it landed in the workspace. All seven rows in Accepted answers carry a path plus section
- [x] Every open challenge names why it is not yet closed and who owns closing it. Four rows in Open challenges, each with a push count and a parking place
- [x] The evidence ledger holds verbatim quotes, not paraphrases, for load-bearing claims. Seven rows, all in quotation marks, all traceable to a session id or a query id
- [x] The journal has one line per session since the product began. Fifteen lines from 2026-01-12 to 2026-03-25
- [ ] The next question is named with a bank id and is genuinely unanswered. DESIGN-1 is named; the integration choice remains open. This row stays unticked until the premortem and ADRs are written. Note since this snapshot: the Darya term sheet arrived 2026-03-30
- [x] Overlays are declared with a decision date and a log reference. Regulated: yes, decided 2026-03-05, logged as D2; AI: no

Signed: Hira Baig, Product Manager, 2026-03-25
