# JTBD Spec: Sahulat Bill Pay

Fills [templates/discovery/jtbd-spec.md](../templates/discovery/jtbd-spec.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan run by a fictional licensed electronic-money institution, the people, agents, customers, billers, bank, aggregator and telco are fiction, and every number is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig · **Date:** 2026-02-17 · **Interviews behind this spec:** 14 sessions (INT-001 to INT-014, N17), linked in [the research plan](sahulat-user-research-plan.md) and recorded in [the interview notes](sahulat-interview-notes.md)

## 1. Job statement

- **When** the month closes and the electricity, gas and water bills arrive with due dates that land on weekends as often as weekdays
- **I want to** settle each bill before its due date without a trip to a branch or a shop and without paying a surcharge for a weekend cutoff
- **so I can** keep the household's accounts clean and stop losing time and money on errands that should not exist

| Field | Answer |
|---|---|
| Job performer | Shazia, P1, the household bill-runner; she executes the job even where a male head of household holds the account (P1 cites INT-001, 002, 004, 005, 007, 008) |
| Frequency and trigger | Three bills a month per household in the sample, electricity, gas and water (N22); the paper bill arriving with its due date is the trigger (T1) |
| How they measure success | The bill is paid before its due date and no late surcharge appears on the next bill (E1, INT-004 at 02:10; Gate 1 attempt 2's outcome signal, restated in [the one-pager](sahulat-one-pager.md)) |
| Evidence | E1 and E2 from INT-004; themes T1, T2 and T5 from [the research plan](sahulat-user-research-plan.md) section 6; cost facts N18 to N20 from [the interview notes](sahulat-interview-notes.md) |

## 2. Tools hired today

| Tool hired today | What it does well | Where it fails the job | Evidence |
|---|---|---|---|
| A trip to a bank branch (4 of 8 customers) | Accepted everywhere, and the teller stamps a slip that counts as proof | A round trip of a median 70 minutes plus PKR 60 transport per trip (N20); shut when a due date falls on a Saturday or Sunday, which happened to 3 of 8 most recent bills (N24) | N63, N20, N24; E1 |
| A bill shop across the road (4 of 8 customers) | Open after hours and on weekends, so a Sunday due date is still payable | Charges an estimated PKR 30 to 50 per bill (N21), and the fee does not buy certainty about posting timing | N63, N21; E1 ("the shop man charged me fifty") |
| Doing nothing until the due date passes, then paying the surcharge | Zero effort at the moment of decision | Five of eight customers paid a late surcharge in the last three months, a median of PKR 200 per bill shown in four of those five (N18, N19) | N18, N19; E1 |
| Cash-in at an agent counter, then walk to a shop or branch to pay | The cash-in itself is instant and local | Money leaves the wallet the same day (T2, six of eight moved it out within two days, N26), so the wallet never becomes the payment channel; the customer makes a second trip anyway | T2, N26; E2 ("I only put money in the phone when I need to send it that day") |
| An agent keys the bill on the customer's handset or his own (observed post-launch) | Removes the trip entirely; median 6 minutes at the counter (CN13) | Was unpriced and unsanctioned in Rel-1 (commission v7 paid PKR 0, N68); the customer hands over her PIN (E6) and asks for a paper slip the system does not produce (N60) | N45, CN13, E6, N60, N68 |

## 3. Forces on the switch

| Force | What we heard | Evidence |
|---|---|---|
| Push of the current struggle | The surcharge that lands because the bank was shut on a Sunday due date, and the PKR 50 the shop took anyway (E1); the blind repeat dial after a session drops mid-payment, waiting ten minutes for a status message that never comes (E4) | E1, INT-004 at 02:10; E4, INT-007 at 21:15; T4, T5 |
| Pull of the new way | Customers asked whether Sahulat could do the bill: 412 helpline calls tagged BILL-ASK in four weeks (N13), against a feature that did not exist; agents field the same question daily and refer customers away (E3) | N13; E3, INT-011 at 06:50; T3 |
| Anxiety about the new | "The screen went off in the middle and I did not know if the money went" (E4): fear of paying twice, or of losing the money into nothing, is the dominant worry about moving the payment onto the wallet | E4, INT-007 at 21:15; T4 |
| Habit of the old | The trip is already built around the bill cycle: 6 of 8 customers pay on the due date itself (N25), and the bill-shop relationship absorbs the weekend case, so there is no felt gap to fill on a weekday | N25; T1; E1 |

A switch happens when push plus pull outweigh anxiety plus habit. Here push (surcharge, fee, lost time) and pull (412 asking calls) are strong, but anxiety (did the money move?) is the binding force, which is why AC-7, AC-8 and AC-10 carry the dropped-session and duplicate cases rather than the happy path.

## 4. Barriers to progress

| Barrier | Type | Severity | Evidence |
|---|---|---|---|
| No product existed to pay a bill from the wallet; the feature was absent while demand showed up in 412 calls | capability | blocks the job | N13; D1 |
| Money enters the wallet for a purpose and leaves the same day, so there is no balance to pay from at the moment the bill is due | access | degrades it | T2, N26; E2 |
| Fear that a dropped USSD session has already debited the wallet, producing a blind redial and a possible double payment | anxiety | blocks the job | E4, T4; R2 |
| Weekend and after-hours due dates reproduce the surcharge on any rail that posts next working day | switching cost | degrades it | N24, N25, N35; E1; D3 |
| Agent float runs out on bill-peak days (the 5th to the 10th carry 44 percent of payments), so the same-visit cash-in and pay fails at the counter | access | degrades it | N57, N52; R1 |
| Agents were paid PKR 0 for an agent-performed bill in commission v7, so the assistance customers actually wanted carried no incentive | switching cost | annoyance | N68; DEP-4 |

## 5. So what

| Field | Answer |
|---|---|
| The underserved part of the job | The moment between the bill arriving and the money leaving the wallet. Today's hires fail hardest where the due date lands outside banking hours (push, E1) and where the customer cannot trust that a payment posted (anxiety, E4). The balance-first design bet assumed the funding step was the gap; the evidence says the funding step is solved by the cash-in the customer already makes, and the unsolved step is the trust that the payment landed before the surcharge window closes |
| Feeds | [The problem framing](sahulat-problem-framing.md) (Gate 1 roll-up), [the personas](sahulat-personas.md) (P1 Shazia, P2 Rafiq, P3 Kamran labelled ASSUMPTION), and [the opportunity assessment](sahulat-opportunity-assessment.md) |
| Open questions for the next interviews | Whether a customer would accept an SMS reference as proof in place of a stamped slip (AS-2, tested later); whether she would confirm an agent-keyed payment on her own phone without handing over her PIN (AS-3, E6 shows the PIN being shared today); what an agent charges informally for doing the bill himself (pass-2 finding CN17, PKR 20, E8) |

## Exit gate

This spec is fit to build on when:

- [x] The job statement names situation, motivation, and outcome without naming any product. Section 1's When/I want to/so I can carries no product word; the job is settling a bill before its due date without a trip or a surcharge
- [x] At least one real interview stands behind it. Fourteen sessions, INT-001 to INT-014 (N17), with verbatims E1 through E5 cited throughout
- [x] Tools hired today include the non-product alternatives. Section 2 lists the bank branch, the bill shop, doing nothing and paying the surcharge, and the agent keying the bill on his own handset
- [x] All four forces carry entries grounded in what customers said. Each row in section 3 cites an E-note or a theme, not a hope; the anxiety row is the one customers volunteered unprompted (E4)
- [x] Barriers are typed and rated, ready to become requirements or GTM work. Section 4 types all six rows and rates severity; the capability and anxiety rows became acceptance criteria (AC-7, AC-8, AC-10), the access and switching-cost rows became GTM work (the float hotline, the commission schedule)
- [x] The underserved part of the job is stated and feeds a named next artifact. Section 5 names the trust-before-due-date moment and routes to the problem framing, the personas and the opportunity assessment

Signed: Faisal Mirza, Chief Executive and sponsor, 2026-02-27
