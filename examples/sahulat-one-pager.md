# One-Pager: Sahulat Bill Pay

Fills [templates/definition/one-pager.md](../templates/definition/one-pager.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, Hira Baig its only fictional product manager, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the Sahulat journey rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig · **Date:** 2026-03-09 · **Status:** Approved at Gate 2 attempt 2, 2026-03-25 (attempt 1 on 2026-03-18 was RETURNED for adjectives); amended 2026-05-21 per decision D5
**Reviewers who must not be surprised:** Faisal Mirza, Zainab Qureshi, Amna Rasheed

## 1. Problem

Shazia, Sahulat's household bill-runner, pays her Ravi Power electricity bill and Chenab Gas bill in person, near the due date, at a bank branch or a bill shop charging PKR 30 to 50, because nothing in the wallet looks a bill up or pays one. When a due date lands on a weekend the branch is shut and the surcharge posts anyway: "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill" (E1, INT-004, 2026-02-02). Five of eight customers interviewed paid a late surcharge in the last three months, and 61 percent of cash-ins are fully cashed out within 48 hours, so money entering Sahulat leaves the day it arrives rather than waiting for a bill: "I only put money in the phone when I need to send it that day. Why would I leave it there?" (E2, INT-004, 2026-02-02). The evidence base and the Gate 1 GO are in [the Sahulat journey](sahulat-journey.md).

## 2. Proposal

Shazia dials Sahulat's USSD short code, looks up her Ravi Power or Chenab Gas bill by the reference number on the paper, and sees the amount and due date without the paper in hand. She pays it, from wallet balance or in the same counter visit where she cashes in with Rafiq, her agent, and gets an SMS carrying a payment reference the moment the bill posts, the proof she currently gets from a shop's slip. A dropped USSD session tells her, before she redials, whether the money moved, so a second attempt never becomes a second payment. Nothing else about the wallet changes: cash-in, cash-out and transfer are untouched.

## 3. Scope

| # | In scope, one line each | Story or ticket |
|---|---|---|
| 1 | Look up an electricity or gas bill by the reference number printed on the paper bill, over USSD | SAHULAT-S1 |
| 2 | Pay the bill from wallet balance and receive an SMS with a payment reference | SAHULAT-S2 |
| 3 | Cash in at an agent counter and pay the bill in the same visit | SAHULAT-S3 |
| 4 | Pay a Chenab Gas bill through the same flow | SAHULAT-S6 |
| 5 | Tell the customer, before a dropped session ends, whether the payment went through | SAHULAT-S8 |
| 6 | Let a support agent look a bill payment up by reference on the first call | SAHULAT-S9 |
| 7 | Save a bill reference after paying, so next month's lookup skips re-entry | SAHULAT-S5 |
| 8 | Offer the same lookup-and-pay flow on the smartphone app | SAHULAT-S10 |
| 9 | Send a reminder SMS three days before a saved bill's due date | SAHULAT-S11 |

At Gate 2 attempt 2 this table also carried paying a Mehran Water bill (SAHULAT-S7). Decision D5 dropped it on 2026-05-21, after three of ten test bills failed Mehran Water's reference validation, and the affected criterion was re-signed against this gate rather than absorbed quietly; see section 5.

## 4. How we will know it worked

All figures below are ILLUSTRATIVE target figures, agreed with the metric owner named in each row; none is a measured actual, since this document predates launch.

| Metric | Baseline | Target | Measured where | Owner |
|---|---|---|---|---|
| M1: bills paid per month | 0 bills a month; the feature does not exist yet | 40,000 bills paid in the four weeks to 2026-08-16 | Core ledger, query M1 | Hira Baig |
| M2: share of bill payments funded from a balance held more than 48 hours, the balance-first hypothesis | 0 percent; the feature does not exist yet | 50 percent of bill payments, same four-week window | Core ledger, query FP-01 | Hira Baig |
| Guardrail: USSD bill-pay session completion (M3) | Not yet measured; no bill-pay session exists yet | Must not fall below 90 percent | Falak Telecom USSD gateway logs, dashboard LD-1 | Zainab Qureshi (halt-caller) |
| Guardrail: pass-through share, cash-in fully cashed out within 48 hours (M4) | 61 percent, measured, Q4 2025, query PT-01 | Must not rise above 61 percent | Core ledger, query PT-01 | Hira Baig (halt-caller) |

M2 is the balance-first assumption written as a number so it can fail: if fewer than half of bill payments are funded from a balance held more than two days, the design bet behind SAHULAT-S5, S10 and S11 does not hold. Fifty percent, not a hundred, because Kamran, the persona this bet stands on, is drawn from two interviews out of eight and is labelled an assumption in the personas document; a target only a near-universal habit could clear would be unfalsifiable in the other direction.

## 5. Not doing

Paying a Mehran Water bill in Rel-1 (SAHULAT-S7). In scope at Gate 2 attempt 2; decision D5 dropped it on 2026-05-21 after three of ten test bills failed Mehran Water's reference validation. Returns once the biller's reference format passes the test suite Ravi Power and Chenab Gas cleared.

Charging the customer a fee to pay a bill. Faisal Mirza's early framing leaned toward revenue on top of the payment; decision D4 on 2026-03-20 set the Rel-1 customer fee at PKR 0, because a new fee at the counter would blunt the value of removing a trip and a surcharge on the day it launches. Revisit once adoption is proven.

Building the smartphone app as the lead channel. Most Sahulat customers reach the wallet over USSD on a feature phone, not the app, so USSD carries the walking skeleton and the app flow (SAHULAT-S10) ships as a should, not the primary surface. App-first would build the wrong product well for most of the base.

Integrating through Darya Bank's BillLink rail instead of BillBridge. Darya's catalogue and API were more ready and would have shipped roughly nine weeks sooner, but its 15:00 weekday settlement cutoff would have posted a Sunday-due bill the next working day, reproducing the surcharge this feature exists to remove. Decision D3 on 2026-04-03 chose BillBridge instead; D3 postdates this document's original sign-off and is folded in at the 2026-05-21 amendment. Reopens if Darya's cutoff moves past 20:00, seven days a week.

Any merchant-facing QR code or point-of-sale acceptance. This feature pays a fixed household biller, not a merchant at a till; merchant acquiring is a non-goal of the product's current horizon.

## 6. Acceptance

All thresholds below are ILLUSTRATIVE, agreed at Gate 2 attempt 2.

| # | Given, when, then | Owner |
|---|---|---|
| AC-1 | Given a customer dials the USSD short code and enters a valid Ravi Power reference number, when Sahulat queries BillBridge, then the amount and due date return within 8 seconds at the 95th percentile | Zainab Qureshi |
| AC-3 | Given a looked-up bill and sufficient wallet balance, when the customer confirms payment, then the balance debits, the bill posts, and an SMS carrying a payment reference arrives within 60 seconds | Zainab Qureshi |
| AC-8 | Given a USSD session drops before the debit is confirmed, when the customer dials again, then Sahulat resumes the same attempt against its idempotency key rather than starting a new one, and a status SMS arrives within 2 minutes either way | Zainab Qureshi |

The full pass-or-fail contract, AC-1 through AC-13, including the duplicate-payment block, the tier-limit refusal, and the 24-hour reversal when a biller posting fails after debit, is indexed in [the Sahulat journey's shared identifiers](sahulat-journey.md#shared-identifiers).

## 7. Risks and open questions

All likelihood and impact scores below are ILLUSTRATIVE, on a 1-to-5 scale, from the DESIGN-stage premortem.

| # | Risk or question | Owner | Needed by |
|---|---|---|---|
| 1 | Does bill pay need the full BRD and PRD stack rather than one-pager weight, given a regulator is in scope? Amna Rasheed's objection to decision D2, filed in the decision log | Amna Rasheed | 2026-05-29, a compliance memo confirming bill pay sits within the licence's permitted activities |
| 2 | R1: agent float runs out on a bill-peak day, so the same-visit cash-in and pay fails at the counter (likelihood 4 of 5, impact 4 of 5) | Tariq Sohail | Open: Tariq Sohail, before the nationwide rollout step; the calendar date was not yet fixed at this amendment |
| 3 | R2: a USSD session times out mid-payment and the customer pays twice (likelihood 4 of 5, impact 4 of 5); AC-7, AC-8 and AC-10 are the answer | Zainab Qureshi | Gate 4, targeted for 2026-06-10 |
| 4 | R3: BillBridge posts late to a biller and a surcharge lands despite the payment (likelihood 2 of 5, impact 4 of 5); AC-9's 24-hour reversal is the answer | Hira Baig | Before launch |
| 5 | R4: a trust-account reconciliation break from an aggregator retry (likelihood 3 of 5, impact 3 of 5) | Bilal Hasan | Gate 4, targeted for 2026-06-10 |
| 6 | R5: Falak Telecom delays the USSD short-code menu change past UAT (likelihood 3 of 5, impact 3 of 5) | Zainab Qureshi | 2026-06-14, dependency DEP-2 |
| 7 | R6: customers do not hold a balance, so paying from balance is used by few (likelihood 2 of 5, impact 5 of 5); this is M2's hypothesis restated as a risk | Hira Baig | Open: Hira Baig, fixed once Gate 5 sets the post-launch review window |

Rows 2 through 7 are the DESIGN-stage premortem's six risks, dated 2026-04-08, folded into this table at the 2026-05-21 amendment so a reader of the signed one-pager sees the risk picture the team carried into BUILD. Row 7 is flagged, not filed quietly: a likelihood of 2 of 5 rests on the same two interviews, INT-003 and INT-006, that Kamran's persona rests on, and M2's target exists precisely because that confidence is untested.

---

## How this one-pager fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Solution before problem | The proposal appears first, with the need compressed into a clause | The problem block comes first, and names no solution |
| Unfalsifiable success | "Improve the experience", "increase engagement" | One metric, one target number, one date |
| Nothing excluded | Only the chosen approach appears, and scope is unbounded by omission | The not-doing list carries at least two real items somebody wanted |
| No decider | It closes with "let us discuss" or "team to align" | One name, one role, and the date by which they decide |
| The problem is never sized | No estimate of how many, how often, or what it costs | Size it, cite the source, and say how rough the number is |
| A pitch, not a decision | Heavy on benefit, silent on cost, risk and reversal | Costs, risks and a kill criterion appear on the same page |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] The problem cites evidence with a source ID rather than asserting it. Section 1 cites E1 and E2 by interview id and date.
- [x] One outcome metric and one guardrail metric, each with a baseline and an owner. Section 4 carries M1 and M2 as outcomes and M3 and M4 as guardrails, each with a baseline, a target and an owner.
- [x] The not-doing list is written and the reviewers have read it. Section 5 lists five items reviewers wanted; Faisal Mirza, Zainab Qureshi and Amna Rasheed signed Gate 2 attempt 2.
- [x] Every must has an acceptance criterion that can fail. SAHULAT-S1, S2, S3, S6 and S8 are the Rel-1 musts, each with a testable criterion in the AC-1 to AC-13 contract; three headline rows are sampled in section 6.
- [ ] Every risk and open question has an owner and a date. Rows 2 and 7 (R1 and R6) carry an owner but a marked-Open date, since Gate 5 had not yet set the nationwide-rollout and review-window dates at this amendment; every other row carries both.
- [x] It still fits on one page, or it has been promoted to prd.md. Gate 2 accepted the one-pager weight under decision D2, over Amna Rasheed's objection; not promoted to prd.md.

Signed at Gate 2 attempt 2, 2026-03-25: Hira Baig, product owner; Faisal Mirza, sponsor. The 2026-05-21 amendment under D5 was re-reviewed by the same three reviewers named above rather than re-signed at a new gate attempt, since it removed scope rather than adding it.
