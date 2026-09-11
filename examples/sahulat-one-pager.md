# One-Pager: Sahulat Bill Pay

Fills [templates/definition/one-pager.md](../templates/definition/one-pager.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig · **Date:** 2026-03-09 · **Status:** Approved at Gate 2 attempt 2, 2026-03-25 (attempt 1 on 2026-03-18 was RETURNED for adjectives); amended 2026-05-21 per decision D5; annotated after Gate 5 (2026-07-01) and the post-launch review (2026-08-21), annotations marked as such
**Reviewers who must not be surprised:** Faisal Mirza, Zainab Qureshi, Amna Rasheed

## 1. Problem

Shazia, Sahulat's household bill-runner, pays her Ravi Power electricity bill and Chenab Gas bill in person, near the due date, at a bank branch or a bill shop charging an estimated PKR 30 to 50 (N21), and when a due date lands on a weekend the branch is shut and the surcharge posts anyway: "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill" (E1, INT-004, 2026-02-02). Five of eight customers interviewed paid a late surcharge in the last three months, and 61 percent of cash-ins are fully cashed out within 48 hours rather than waiting for a bill (N10): "I only put money in the phone when I need to send it that day. Why would I leave it there?" (E2, INT-004, 2026-02-02). About 246,000 wallets show a Shazia-type bill-week cash-in pattern (N64, estimate, query BP-01). See [the Sahulat problem framing](sahulat-problem-framing.md), the discovery source of truth.

## 2. Proposal

Shazia dials Sahulat's USSD short code, looks up her Ravi Power or Chenab Gas bill by the reference number on the paper, and sees the amount and due date without the paper in hand. She pays it, from wallet balance or in the same counter visit where she cashes in with Rafiq, her agent, and gets an SMS with a payment reference within a minute of paying, the proof she currently gets from a shop's slip. BillBridge posts to the biller within 30 minutes, and if posting fails the debit is reversed within 24 hours (AC-9). After a dropped session, an SMS within 2 minutes tells her whether money moved, and redialing resumes the same attempt, so a second attempt never becomes a second payment. Nothing else about the wallet changes: cash-in, cash-out and transfer are untouched.

## 3. Scope

| # | In scope, one line each | Priority | Story or ticket |
|---|---|---|---|
| 1 | Look up a Ravi Power electricity bill by the reference number printed on the paper bill, over USSD | Must | SAHULAT-S1 |
| 2 | Pay the bill from wallet balance and receive an SMS with a payment reference | Must | SAHULAT-S2 |
| 3 | Cash in at an agent counter and pay the bill in the same visit | Must | SAHULAT-S3 |
| 4 | Pay a Chenab Gas bill through the same flow | Must | SAHULAT-S6 |
| 5 | After a USSD session drops mid-payment, tell the customer by SMS within 2 minutes whether money moved, and resume the same attempt on the next dial | Must | SAHULAT-S8 |
| 6 | Let a support agent look a bill payment up by reference on the first call | Should | SAHULAT-S9 |
| 7 | Save a bill reference after paying, so next month's lookup skips re-entry (balance-first) | Should | SAHULAT-S5 |
| 8 | Offer the same lookup-and-pay flow on the smartphone app (balance-first) | Should | SAHULAT-S10 |
| 9 | Send a reminder SMS three days before a saved bill's due date (balance-first) | Should | SAHULAT-S11 |

At Gate 2 attempt 2 this table also carried paying a Mehran Water bill (SAHULAT-S7). Decision D5 dropped it on 2026-05-21, after three of ten test bills failed Mehran Water's reference validation, and the affected criterion was re-reviewed against this gate rather than absorbed quietly; see section 5.

## 4. How we will know it worked

The outcome signal Gate 1 attempt 2 set on 2026-02-27, carried unchanged (the user stories label it O1): a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month. M1 and M2 are how this document tests it.

Targets below are ILLUSTRATIVE, agreed with the metric owner named in each row; baselines are measured where stated, since this document predates launch and only M4's baseline reflects data collected before Rel-1.

| Metric | Baseline | Target | Measured where | Owner |
|---|---|---|---|---|
| M1: bills paid per month | 0 bills a month; the feature does not exist yet | 40,000 bills paid in the four weeks ending launch plus six weeks (N42) | Core ledger, query BL-01 | Hira Baig |
| M2: share of bill payments funded from a balance held more than 48 hours, the balance-first hypothesis | 0 percent; the feature does not exist yet | 50 percent of bill payments, same four-week window | Core ledger, query FP-01 | Hira Baig |
| Guardrail: USSD bill-pay session completion (M3) | Not yet measured; no bill-pay session exists yet | Must not fall below 90 percent | Falak Telecom USSD gateway logs | Zainab Qureshi (halt-caller) |
| Guardrail: pass-through share, cash-in fully cashed out within 48 hours (M4) | 61 percent, measured, Q4 2025, query PT-01 | Must not rise above 61 percent | Core ledger, query PT-01 | Hira Baig (halt-caller) |

Annotation, 2026-07-01: Gate 5 set the review window as launch plus six weeks, closing 2026-08-17 (N55); M1 and M2 are measured over the last four full weeks inside it, 2026-07-20 to 2026-08-16.

M2 is the balance-first assumption written as a number so it can fail: if fewer than half of bill payments are funded from a balance held more than two days, the design bet behind SAHULAT-S5, S10 and S11 does not hold. Fifty percent is double what the sample shows: 2 of 8 held a balance for more than two days (N26), and 6 of 8 moved money out the same day (T2). The target is set where the design bet has to be true, so the review can falsify it; a target the sample already cleared would prove nothing. If M2 is under 50 percent at review, the balance-first work (SAHULAT-S5, S10, S11) stops. Decider Faisal Mirza at Gate 6. That work draws against the squad's full BUILD capacity of 28 engineer-weeks (N8, estimate, noted at this amendment).

[The vision](sahulat-vision.md)'s non-goal against designing a flow that only pays off if customers hold a balance conditions that work on a later DISCOVER pass finding three of eight or more customers holding a balance, a bar N26 (2 of 8) does not clear. This document commits SAHULAT-S5, S10 and S11 as shoulds, not musts, against that unmet bar: M2 is the mechanism that makes the bet falsifiable rather than assumed, and the work stops at Gate 6 if the sample still does not support it. The gap between the vision's stated condition and scoping the work as should-priority ahead of it was not reconciled at sign-off; it is recorded here at this amendment rather than left silent.

## 5. Not doing

Paying a Mehran Water bill in Rel-1 (SAHULAT-S7). In scope at Gate 2 attempt 2; decision D5 dropped it on 2026-05-21 after three of ten test bills failed Mehran Water's reference validation. Returns once the biller's reference format passes the test suite Ravi Power and Chenab Gas cleared.

Charging the customer a fee to pay a bill. Faisal Mirza's early framing leaned toward revenue on top of the payment; decision D4 on 2026-03-20 set the Rel-1 customer fee at PKR 0, because a new fee at the counter would blunt the value of removing a trip and a surcharge on the day it launches. Revisit once adoption is proven.

Building the smartphone app as the lead channel, a non-goal carried from [the vision](sahulat-vision.md). Most Sahulat customers reach the wallet over USSD on a feature phone, not the app, so USSD carries the walking skeleton and the app flow (SAHULAT-S10) ships as a should, not the primary surface. Reopens once the app becomes the majority channel for active bill-pay usage, sustained across two consecutive quarters.

Integrating through Darya Bank's BillLink rail instead of BillBridge, the same bank-rail non-goal [the vision](sahulat-vision.md) carries in section 5. Darya's catalogue and API were more ready and would have shipped roughly nine weeks sooner, but its 15:00 weekday settlement cutoff would have posted a Sunday-due bill the next working day, reproducing the surcharge this feature exists to remove, and its 60 percent revenue share left Sahulat PKR 4 a bill against PKR 7 through BillBridge. Given up: nine weeks and a 210-biller catalogue against BillBridge's 160. Decision D3 on 2026-04-03 chose BillBridge instead; D3 postdates this document's original sign-off and is folded in at the 2026-05-21 amendment. Reopens if Darya's cutoff moves past 20:00, seven days a week.

Any merchant-facing QR code or point-of-sale acceptance, a non-goal carried from [the vision](sahulat-vision.md). This feature pays a fixed household biller, not a merchant at a till; merchant acquiring is out of the product's current horizon there.

## 6. Acceptance

All thresholds below are ILLUSTRATIVE, agreed at Gate 2 attempt 2.

| # | Given, when, then | Owner |
|---|---|---|
| AC-1 | Given a customer dials the USSD short code and enters a valid Ravi Power reference number, when Sahulat queries BillBridge, then the amount and due date return within 8 seconds at the 95th percentile | Zainab Qureshi |
| AC-3 | Given a looked-up Ravi Power bill and a wallet balance at or above the amount due, when the customer confirms payment, then the wallet debits once, BillBridge is called, and an SMS carrying the payment reference arrives within 60 seconds | Zainab Qureshi |
| AC-8 | Given a USSD session drops before the debit call is made, when the customer dials again, then Sahulat resumes the same attempt against its idempotency key rather than starting a new one, and a status SMS arrives within 2 minutes either way | Zainab Qureshi |

The full pass-or-fail contract, AC-1 through AC-13, including the duplicate-payment block, the tier-limit refusal, and the 24-hour reversal when a biller posting fails after debit, is in [the Sahulat acceptance criteria](sahulat-acceptance-criteria.md). AC-8's resume half was later accepted as the Gate 4 miss (2026-06-10).

## 7. Risks and open questions

All likelihood and impact scores below are ILLUSTRATIVE, on a 1-to-5 scale, from the DESIGN-stage premortem.

| # | Risk or question | Owner | Needed by |
|---|---|---|---|
| 1 | Does bill pay need the full BRD/FRD stack rather than one-pager weight, given a regulator is in scope? Amna Rasheed's objection to decision D2, filed in the decision log | Amna Rasheed | 2026-05-29, a compliance memo confirming bill pay sits within the licence's permitted activities (DEP-3) |
| 2 | R1: agent float runs out on a bill-peak day, so the same-visit cash-in and pay fails at the counter (likelihood 4 of 5, impact 4 of 5) | Tariq Sohail | Open: Tariq Sohail, before the nationwide rollout step; the calendar date was not yet fixed at this amendment |
| 3 | R2: a USSD session times out mid-payment and the customer pays twice (likelihood 4 of 5, impact 4 of 5); AC-7, AC-8 and AC-10 are the answer | Zainab Qureshi | Gate 4, targeted for 2026-06-10 |
| 4 | R3: BillBridge posts late to a biller and a surcharge lands despite the payment (likelihood 2 of 5, impact 4 of 5); AC-9's 24-hour reversal is the answer | Hira Baig | Gate 4, targeted for 2026-06-10, when AC-9 is verified |
| 5 | R4: a trust-account reconciliation break from an aggregator retry (likelihood 3 of 5, impact 3 of 5) | Bilal Hasan | Gate 4, targeted for 2026-06-10 |
| 6 | R5: Falak Telecom delays the USSD short-code menu change past UAT (likelihood 3 of 5, impact 3 of 5) | Zainab Qureshi | 2026-06-14, dependency DEP-2 |
| 7 | R6: customers do not hold a balance, so paying from balance is used by few (likelihood 2 of 5, impact 5 of 5); this is M2's hypothesis restated as a risk | Hira Baig | Open: Hira Baig, fixed once Gate 5 sets the post-launch review window |

Rows 2 through 7 are the DESIGN-stage premortem's six risks, dated 2026-04-08, folded into this table at the 2026-05-21 amendment so a reader of the signed one-pager sees the risk picture the team carried into BUILD. Row 7 is flagged, not filed quietly: a likelihood of 2 of 5 rests on the same two interviews, INT-003 and INT-006, that Kamran's persona rests on, and M2's target exists precisely because that confidence is untested. Flagged at this amendment but not re-scored, and no balance-first story was paused pending the review. Annotation, 2026-08-21: that inaction is what the post-launch review names.

---

## How this one-pager fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Solution before problem | The proposal appears first, with the need compressed into a clause | The problem block comes first, and names no solution |
| Unfalsifiable success | The same hypothesis behind M2, "customers will value paying from balance," is unfalsifiable as written; no review window could fail it | One metric, one target number, one date; here, M2: 50 percent of bill payments funded from a balance held more than 48 hours, in the four weeks ending launch plus six weeks |
| Nothing excluded | Only the chosen approach appears, and scope is unbounded by omission | The not-doing list carries at least two real items somebody wanted |
| No decider | It closes with "let us discuss" or "team to align" | One name, one role, and the date by which they decide |
| The problem is never sized | No estimate of how many, how often, or what it costs | Size it, cite the source, and say how rough the number is |
| A pitch, not a decision | Heavy on benefit, silent on cost, risk and reversal | Costs, risks and a kill criterion appear on the same page |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] The problem cites evidence with a source ID rather than asserting it. Section 1 cites E1 and E2 by interview id and date.
- [x] One outcome metric and one guardrail metric, each with a baseline and an owner. Section 4 carries M1 and M2 as outcomes and M3 and M4 as guardrails, each with a baseline, a target and an owner.
- [x] The not-doing list is written and the reviewers have read it. Section 5 lists five items. Three were on the list at Gate 2 attempt 2, signed 2026-03-25 by Hira Baig, Zainab Qureshi, Faisal Mirza and Amna Rasheed. Water (D5) and the Darya rail (D3) were added at the 2026-05-21 amendment, which Faisal Mirza, Zainab Qureshi and Amna Rasheed re-reviewed.
- [x] Every must has an acceptance criterion that can fail. SAHULAT-S1, S2, S3, S6 and S8 are the Rel-1 musts, each with a testable criterion in the AC-1 to AC-13 contract; three headline rows are sampled in section 6.
- [ ] Every risk and open question has an owner and a date. Rows 2 and 7 (R1 and R6) carry an owner but a marked-Open date, since Gate 5 had not yet set the nationwide-rollout and review-window dates at this amendment; every other row carries both.
- [ ] It still fits on one page, or it has been promoted to prd.md. No: about 1,970 words after the 2026-05-21 amendment and the post-Gate-5 annotations. Gate 2 accepted the one-pager weight under decision D2, over Amna Rasheed's objection, but that decision was about document weight, not page count. Not promoted to prd.md. Open: Hira Baig decides trim vs promote.

Signed at Gate 2 attempt 2, 2026-03-25: Hira Baig, product owner; Zainab Qureshi, engineering lead; Faisal Mirza, sponsor; Amna Rasheed, regulatory owner (per STAGE-GATES: regulated, no model), signed with her D2 objection noted. The 2026-05-21 amendment under D5 was re-reviewed by the same three reviewers named above rather than re-signed at a new gate attempt, since it removed scope rather than adding it.
