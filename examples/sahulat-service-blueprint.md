# Service Blueprint: Sahulat Agent-Assisted Bill Pay

Fills [templates/discovery/service-blueprint.md](../templates/discovery/service-blueprint.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Rafiq and the customer are fictional, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheets in [the Sahulat journey](sahulat-journey.md) and [the Sahulat coverage sheet](sahulat-coverage-sheet.md) rather than from any real wallet, agent network or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-09-08 · **Status:** Drafted 2026-09-08 from the counter observation and pilot debriefs; the pass-2 agent interview quotes (E6, E7) and the fix-candidates section (§5) were added after INT-015 to INT-020 (2026-09-10 to 2026-09-12) and the 2026-09-18 design sprint
**Evidence base:** Usman Javed's field observation at 12 agent counters, 2026-08-11 and 2026-08-12 (N45, CN13); the pass-2 agent interviews INT-015 to INT-020, 2026-09-10 to 2026-09-12 (CN14 to CN17, E6, E7); the pilot agent debriefs of 2026-07-27 (N60)

## 1. Scenario, trigger, and scope

**Scenario:** Rafiq, the corner-shop agent (persona P2 in [sahulat-personas.md](sahulat-personas.md), sourced from INT-009 to INT-014 and INT-015 to INT-020), pays a household's electricity or gas bill on the customer's own phone while she stands at his counter.
**Trigger:** A customer arrives at Rafiq's counter holding a paper bill, or naming the biller, and asks him to pay it; the observation notes record this as the dominant pattern rather than the customer paying it herself (N45: 41 of 53 assisted payments across 12 counters).
**Scope statement:** this blueprint covers from the customer stating which bill she needs paid through the customer leaving the counter holding proof of payment, and nothing after: it stops before the daily trust-account reconciliation closes, which is recorded here only as the backstage step that checks the day's work, not as part of the customer's scenario.

## 2. The blueprint

Written from N45, CN13, E6 and E7 and the pilot debriefs (N60), not from the Rel-1 design that assumed a customer paying from her own held balance. Every vendor Sahulat depends on for this scenario is named in the support column: Falak Telecom (USSD gateway and SMS), BillBridge (bill aggregator), the billers themselves (Ravi Power, Chenab Gas), and Sutlej Bank Limited, Sahulat's settlement bank named in [the coverage sheet](sahulat-coverage-sheet.md).

| # | User action | Frontstage (what the user sees) | Backstage (people and actions out of sight) | Support systems and vendors |
|---|---|---|---|---|
| 1 | Customer tells Rafiq which bill needs paying (Ravi Power or Chenab Gas) and hands him the paper bill, or reads out the reference number printed on it | Customer speaks the biller's name and hands over paper, or reads a number aloud | Rafiq listens and, where the paper is missing, asks for the reference from memory or a saved chit | None |
| 2 | Rafiq dials Sahulat's USSD short code on his agent handset and looks up the bill by reference | Customer watches Rafiq's screen or waits while he works his own phone | Rafiq keys the reference into the USSD menu | Falak Telecom's USSD gateway (N66: 180-second session ceiling) |
| 3 | The bill amount and due date come back; Rafiq reads them out and the customer confirms | Customer hears the amount and due date spoken back to her | Rafiq checks the amount against what the customer expects to owe | BillBridge, whose catalogue the lookup queries |
| 4 | Rafiq checks whether his own agent float covers crediting a same-visit cash-in for the bill amount | Customer waits; this step is invisible to her unless it fails | Rafiq mentally or physically checks his float balance; on 38 of 600 pilot agents this check failed on the 2026-07-08 bill-peak day (N52) | Sahulat's agent float ledger; Tariq Sohail's network operations |
| 5 | Customer hands Rafiq cash for the bill amount | Cash changes hands at the counter | Rafiq treats the cash as a same-visit cash-in, crediting the customer's wallet before paying out of it (AC-5) | None beyond the wallet itself |
| 6 | Rafiq keys the bill payment against the customer's own wallet; the wallet requires a PIN to authorize the debit | Customer is asked for her PIN, or Rafiq keys the transaction and she supplies the PIN to him directly: "She gave me her PIN so I could do the bill. I do not like knowing it, but the queue was long" (E6, INT-016, 2026-09-10, 12:20) | The two-phase debit state machine (ADR-2) starts, holding an idempotency key against wallet, reference and bill month, the guard against the duplicate-payment tickets a dropped session or a shared PIN can otherwise produce (N47: 61 in week 1, 3 in week 6) | Sahulat's core ledger and USSD gateway |
| 7 | The debit posts and Sahulat submits the payment to BillBridge for the biller | Nothing new to the customer at this instant; she is still standing at the counter | BillBridge posts to the biller within 30 minutes, seven days a week, per its rate-card SLA (N36); settlement to the biller follows T+1 through Sutlej Bank Limited | BillBridge; Sutlej Bank Limited; Ravi Power or Chenab Gas as the receiving biller |
| 8 | A confirmation SMS with a payment reference arrives on the customer's phone | Customer receives the SMS on her own handset | Falak Telecom's SMS gateway delivers the message Sahulat queued at posting | Falak Telecom |
| 9 | Customer asks for something to hold beyond the SMS | 17 of 41 assisted payments in the observation included this ask (N45, CN13); Rafiq answers from habit, not from a designed feature: "I write the SMS number on a chit and stamp it. They show the chit, not the phone" (E7, INT-018, 2026-09-11, 08:40) | Rafiq writes the SMS reference on a paper chit by hand and stamps it; no system prints or logs this document | None; this step exists entirely outside Sahulat's systems |
| 10 | Customer leaves the counter | Customer walks away holding her phone with the SMS, and often the hand-written chit | Median 6 minutes elapsed at the counter from the customer's ask (row 1) to the confirmation SMS (row 8), across the 41 observed payments (CN13) | None |
| 11 | Sahulat's daily reconciliation checks the day's BillBridge postings against the trust-account sub-ledger, after the counter closes | Invisible to the customer; included because it is where a posting error at row 7 would first surface | Bilal Hasan's team runs the reconciliation; a BillBridge retry posting twice produced one unexplained break of PKR 12,300 on 2026-07-14, traced and explained within the day (N48) | BillBridge; Sutlej Bank Limited; Sahulat's trust-account sub-ledger (ADR-3) |

## 3. Failure points at the line of visibility

| # | Blueprint step | What fails or drops | Owner of the fix conversation | Evidence |
|---|---|---|---|---|
| F1 | Step 6, PIN authorization | The customer hands her PIN to Rafiq so he can key the debit, defeating the control that the PIN is meant to hold; happened in 24 of 41 observed assisted payments | Amna Rasheed, head of compliance and regulatory affairs | CN13 (24 of 41); E6, INT-016, 2026-09-10 |
| F2 | Step 9, proof beyond the SMS | No designed artifact exists once the customer asks for something to hold; Rafiq's hand-written, stamped chit is invented at the counter and unrecorded anywhere in Sahulat's systems, and pilot agent debriefs raised the same ask independently | Tariq Sohail, head of agent network | N60 (raised in 5 of 6 pilot agent debriefs, 2026-07-27); CN13 (17 of 41); E7, INT-018, 2026-09-11 |
| F3 | Step 4, agent float | Rafiq cannot credit the same-visit cash-in when his float is out on a bill-peak day, so the payment does not happen at the counter it was tried at | Hira Baig, Product Manager | N52 (38 of 600 pilot agents on the 2026-07-08 bill-peak day); N57 (bill-peak days carry 44 percent of monthly bill payments) |

## 4. Time and waits

| Blueprint step | Elapsed time | Of which waiting | What the user is waiting on | Evidence |
|---|---|---|---|---|
| Step 2, USSD lookup | Within the 8-second p95 threshold agreed at Gate 2 | Open: not separately measured in the field observation | The USSD gateway's response | N56 (acceptance threshold); N66 (180-second session ceiling) |
| Steps 5 to 8, cash handed over through confirmation SMS | Median 6 minutes at the counter | Open: the observation notes recorded only the total, not a wait-versus-processing split | BillBridge posting and the SMS gateway, standing at the counter the whole time | CN13 |
| Step 7, BillBridge posting | Up to 30 minutes by SLA, seven days a week | Not observed to reach this ceiling in the counter sample; the 6-minute median in the row above suggests most postings clear faster than the SLA | The biller-side posting behind the confirmation SMS | N36 |

## 5. Fix candidates

Routed to the pass-2 problem framing, which has not yet been drafted from this blueprint. The blank is [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md); the coverage sheet's timeline opened the assumption map the day before this file, on 2026-09-07, and schedules the design sprint after it, 2026-09-14 to 2026-09-18, but has not yet scheduled a pass-2 problem framing. Owner of that gap: Hira Baig.

| Candidate | Blueprint step(s) | Who feels it and how often | Route |
|---|---|---|---|
| Agent-initiated payment with the customer confirming on her own phone, so the PIN never has to change hands | Step 6 (F1) | Every customer asked for her PIN at the counter; 24 of 41 in the observed sample (CN13) | Pass-2 problem framing, Open; already the subject of assumption AS-3 and sprint question SQ1 per the coverage sheet |
| A printed or stamped slip issued by the system at the point of payment, replacing Rafiq's hand-written chit | Step 9 (F2) | 17 of 41 observed payments, and independently in 5 of 6 pilot agent debriefs | Pass-2 problem framing, Open; already the subject of sprint question SQ2, left unclear at the 2026-09-18 design sprint per the coverage sheet |
| A float replenishment path for agents ahead of the 5th-to-10th bill-peak window, distinct from the existing float top-up hotline that answers a stock-out already happened | Step 4 (F3) | 38 of 600 pilot agents on one observed bill-peak day; 44 percent of monthly bill payments fall in that window | Pass-2 problem framing, Open |

## Exit gate (feeds Gate 1: problem worth solving)

- [x] One scenario, one persona, and an explicit scope statement, held to eight to twelve user actions: Rafiq and the customer, 10 rows from the customer's ask to her leaving the counter, plus row 11 as the backstage exception the scope statement names
- [x] Every row drawn from cited evidence, not the official process diagram: every row cites N45, CN13, N60, N36, N47, N52, N56, N66, ADR-2, ADR-3, AC-5 or E6 or E7
- [x] Every vendor in the support row is named: Falak Telecom, BillBridge, Ravi Power, Chenab Gas, Sutlej Bank Limited
- [x] Every failure point has a named owner for the fix conversation: Amna Rasheed (F1), Tariq Sohail (F2), Hira Baig (F3)
- [x] Time and wait annotations exist for the painful steps, with evidence: steps 2, 5 to 8, and 7 carry timing from N56, CN13 and N36; two rows are honestly marked Open rather than a guessed split
- [ ] Every fix candidate is routed: problem framing, owning team, or not now: all three are routed to the pass-2 problem framing, which is itself still Open, so this box cannot be checked until that file exists

Signed: Hira Baig, Product Manager, 2026-09-08; the fix-candidates section (Section 5) was updated after the 2026-09-18 design sprint, per the Status line above, and was not re-signed at a new date since it adds routing rather than changing the blueprint itself.
