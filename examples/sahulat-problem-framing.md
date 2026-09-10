# Problem Framing: Sahulat Bill Pay

Fills [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md). Everything here is invented: Sahulat is a fictional mobile-money wallet run by a fictional Pakistani electronic money institution, every person, quote, call count and PKR figure is invented to agree with the rest of the [Sahulat journey](sahulat-journey.md), and none of it describes any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-02-16 · **Status:** Funded, 2026-02-27 (Gate 1 attempt 2 GO); framed 2026-02-16; revised after Gate 1 attempt 1 was returned on 2026-02-20

## 1. Situation

Sahulat Digital runs a mobile-money wallet with 1,900,000 registered wallets and 3,200 active agents as of 2025-12-31. Most customers reach it over a USSD short code on a feature phone or through an agent behind a counter rather than through a smartphone app, and cash moving into a wallet has always run well ahead of any use of that money once it is there: 61 percent of cash-ins were fully cashed out again within 48 hours in the quarter ending 2025-12-31, a pattern the team already knew going into 2026 and treats as ordinary. Households in this customer base pay recurring utility bills, most commonly electricity and gas, each due on a fixed date printed on a paper bill, and today none of those bills touches the wallet at any point.

## 2. Complication

In the four weeks to 2026-01-09, the agent helpline logged 412 calls tagged as customers asking whether Sahulat could pay an electricity or gas bill, a feature that did not exist, and set beside the 61 percent cash-out pattern, the two numbers pointed at the same fact from two directions: money enters the wallet and leaves again with nothing keeping it there, and the board's 2026 key result of 520,000 30-day active wallets, against 410,000 active at the end of 2025, had nothing in the product roadmap that would close that gap. Faisal Mirza's own first instinct was a cashback promotion for customers who kept a balance; D1, on 2026-01-16, sent Hira Baig into discovery on the bill itself instead, because the promotion rested on an assumption, that customers will keep a balance in order to pay from it, nobody had tested yet.

## 3. Problem statement

> A household that pays its utility bills in cash needs a way to settle a monthly electricity or gas bill by its due date without a dedicated trip during business hours, because missing that window adds a surcharge to the next bill, but today every way it pays, a bank branch or a bill shop, requires being there during its opening hours, so it makes the trip itself or pays someone to make it, which costs the household about 14 hours a year and, depending on which of those costs it incurs, roughly PKR 720 (transport alone) to PKR 3,320 (transport, plus a surcharge, plus a shop fee at the top of its range) a year in cash (N27).

## 4. Evidence

| # | Evidence item | Type (interview / ticket / metric / observation) | Source or ID | Strength (strong / weak) |
|---|---|---|---|---|
| E1 | "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." | interview | INT-004 (C-04), 2026-02-02, 02:10 | weak (n=1 session; corroborated by 3 of 8 sample due dates falling on a weekend) |
| E2 | "I only put money in the phone when I need to send it that day. Why would I leave it there?" | interview | INT-004 (C-04), 2026-02-02, 18:35 | weak (n=1 session; consistent with theme T2 in the research plan, seen in 6 of 8 customer sessions) |
| E3 | "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." | interview | INT-011 (A-03), 2026-02-04, 06:50 | weak (n=1 agent; the referral pattern is corroborated by T3 across all six agent sessions, but the six-or-seven-a-day count itself is untallied) |
| E4 | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." | interview | INT-007 (C-07), 2026-02-06, 21:15 | weak (n=1 session; channel-reliability context, not counted toward the arithmetic below) |
| 5 | 412 calls in the four weeks to 2026-01-09 tagged as customers asking whether Sahulat could pay an electricity or gas bill | ticket | agent helpline, tag BILL-ASK (N13) | strong (own system) |
| 6 | 61 percent of cash-ins fully cashed out again within 48 hours, quarter ending 2025-12-31 | metric | core ledger, query PT-01 (N10) | strong (own system) |

Fourteen research sessions, eight customers and six agents, ran 2026-01-26 to 2026-02-13, and this document is their synthesis. Rows 5 and 6 are Sahulat's own system data and are strong for that reason; rows E1 to E4 are single-session quotes from that round and are weak. Sections 5 and 6 below are not all drawn from the same fourteen sessions: the household table under section 5 tallies the interview sample, the business table draws on the core ledger, the commission schedule and the board OKR sheet, and section 6's segment count comes from query BP-01 on the ledger, not from an interview count.

## 5. Cost of inaction

**To the user:** a household in the interview sample pays this cost every month a bill is due, in time it always spends and cash it spends only when a payment fails or is handed to someone else (ILLUSTRATIVE, estimate; arithmetic worked here, N27).

| Component | Amount | Basis |
|---|---|---|
| Trips to pay bills | 14 hours a year (12 trips a year x 70 minutes a trip) | median trip length across 8 customer sessions; 12 trips assumes one trip a month carries all three bills (N27) |
| Transport | PKR 720 a year (12 x PKR 60 a trip) | median transport cost across 8 customer sessions |
| Late surcharges | PKR 800 a year, for the 5 of 8 households in the sample who paid one (about 4 occurrences x PKR 200) | 4 of the 5 surcharge bills were shown, not only described; the "about 4 times a year" figure is extrapolated from a three-month window (N18) |
| Fee to a bill shop | PKR 1,080 to PKR 1,800 a year, for the 4 of 8 households in the sample who pay a shop to do it (3 bills x PKR 30 to 50 a bill x 12 months) | estimate, told: the PKR 30 to 50 range comes from the six agent sessions (N21); one customer session, INT-004, separately names PKR 50 for a shop-paid bill (E1) |

The 14 hours and PKR 720 in transport apply to every household in the sample; the surcharge row and the shop-fee row apply to different, partly overlapping halves of it. A household that both pays a surcharge and uses a shop is exposed to roughly PKR 2,600 (PKR 720 + PKR 800 + PKR 1,080) to PKR 3,320 (PKR 720 + PKR 800 + PKR 1,800) a year in cash on top of the 14 hours, the sum of the three rows above; a household that does neither still loses the 14 hours and PKR 720.

**To the business:** the same 61 percent pattern that triggered this inquiry has a monthly cost the business already pays, whether or not it ever builds bill pay (ILLUSTRATIVE, estimate; arithmetic worked here, N28).

| Component | Amount | Basis |
|---|---|---|
| Pass-through cycles a month | 701,500 (1,150,000 cash-ins x 61 percent) | core ledger, December 2025, query PT-01 |
| Agent commission paid on money that never stays | about PKR 24.6 million a month (701,500 x PKR 35, the PKR 15 cash-in and PKR 20 cash-out commission combined) | commission schedule v6, 2025-10-01 |
| Board key-result gap | 110,000 wallets (520,000 target for 2026-12-31 minus 410,000 active at 2025-12-31) with nothing in the roadmap to close it | board OKR sheet, December 2025 |

The PKR 24.6 million a month is commission the business already pays for cash that touches the wallet and is fully cashed out again within 48 hours (N10); it is not a projection of what bill pay would earn, only what today's pattern already costs. Bill pay would not remove the cash-in half of this: a bill paid from a same-visit cash-in still earns the PKR 15 cash-in commission, so at most the PKR 20 cash-out commission on cycles that end in a bill payment is avoidable, and this figure bounds the addressable cost from above, not the amount bill pay would actually recover.

**Trajectory:** asserted as stable, not measured as stable, and on its own not self-correcting. Only one quarter of query PT-01 exists at this writing (N10, the quarter ending 2025-12-31), so there is no ledger trend behind "stable"; prior-quarter PT-01 readings are Open: Sara Lodhi. What the fourteen sessions do show is a reason the pattern would not correct itself even if it were trending: money enters for a purpose and leaves again the same day in 6 of 8 customer sessions (theme T2), and the sessions that contradict it, INT-003 and INT-006 (N26), are two sessions, not a trend. If anything the channel these households already use is about to get more expensive: Falak Telecom's tariff notice of 2025-12-18 raises the USSD session rate from PKR 0.40 to PKR 0.65, a 62.5 percent increase (N62), effective 2026-10-01, a cost that lands on every session and every retry on the channel these households already use, which does not create this problem but does not fade it either.

## 6. Who feels it and how often

| Segment | How many | Frequency of the pain | Severity (blocks work / slows work / annoys) |
|---|---|---|---|
| Households with a wallet whose cash-in pattern matches a bill-paying customer | about 246,000 wallets (a proxy: wallets with a cash-in on the 5th to the 10th of the month in 2 of the last 3 months, query BP-01, ILLUSTRATIVE estimate) | 3 bills a month per household in the interview sample, electricity, gas and water; one trip a month carries all three (N27) | slows a task every household already has to do, and turns into a real cash loss whenever the trip fails to land before the due date |
| Agents fielding bill questions they cannot resolve | 3,200 active agents; the helpline's 412 calls in the four weeks to 2026-01-09 are customer demand reaching agents (tag BILL-ASK), not a count of agents in pain | multiple times a day per agent, by one agent's own account (E3) | slows work: sends business the agent could have kept to a competing shop, unpaid |

## 7. Constraints on any resolution

Any resolution must sit inside the scope of activities permitted under Sahulat Digital's electronic money institution licence, granted under the State Bank of Pakistan's EMI Regulations; a flow that involves settling money to a biller, not only moving it between wallets, may need its own compliance filing before launch, which is why Amna Rasheed, head of compliance, is a party to this decision even though bill pay does not exist yet as a feature. Customers reached through the agent network and the USSD channel sit across more than one wallet tier under the EMI Regulations' own tiered due-diligence rules for basic and enhanced wallets, the risk-based tiering the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) sector card describes; a resolution that assumed every customer already held the wallet's higher tier would exclude the same low-balance, cash-based households this problem describes, so no resolution may treat a tier upgrade as a precondition, and the tier limit itself is Open: Amna Rasheed. This document does not consider what happens once a bill payment is approved and its posting to a biller fails afterward; that question belongs to whichever resolution DESIGN produces, and the [payments acquiring](../knowledge/domains/payments-acquiring.md) sector card is the reference for it at that point, not this one. The company has one product manager and nine engineers in total; any commitment past Gate 1 competes with whatever else those nine engineers already carry, a capacity constraint this document does not attempt to size. The board's 2026 key result of 520,000 30-day active wallets by 2026-12-31 is a fixed year-end deadline that bounds how long DEFINE and DESIGN can run if this problem is funded. Open: Faisal Mirza, a budget ceiling for the DEFINE stage has not been set as of this writing, needed by DEFINE start, 2026-03-05.

## 8. Decision requested

- **Ask:** fund definition, that is, carry this problem from DISCOVER into DEFINE rather than returning to more discovery or retiring it.
- **From:** Faisal Mirza · **By:** 2026-02-20

## Exit gate

(feeds Gate 1: problem worth solving)

- [x] Exactly one problem in this file: settling a recurring utility bill by its due date, nothing else.
- [x] Problem statement contains no solution words: no product, feature or proposed channel is named in section 3; the branch and bill shop named there are how the household pays today.
- [x] Every evidence row has a source ID and a strength label: E1 to E4 labeled weak with the reason stated; rows 5 and 6 are Sahulat's own system data and are labeled strong.
- [x] Cost of inaction carries a number or a named owner and date for the number: section 5 carries the figures (N27, N28); the one open figure, the DEFINE budget ceiling, has an owner and a date in section 7.
- [x] A single accountable owner is named: Hira Baig, in the header.
- [x] The decision requested names the sponsor and a date: Faisal Mirza, by 2026-02-20, in section 8.

This checklist is the author's own read of the file, not a gate result. Gate 1 itself was walked and signed by Faisal Mirza as sponsor and Hira Baig as owner: attempt 1 on 2026-02-20 returned this file on two lines, a cost of inaction with no arithmetic behind it, which is why section 5 above carries the household and business tables rather than a sentence, and a success signal that was usage; the exact wording of the returned draft is not preserved in this record, only the two reasons it failed. Attempt 2 on 2026-02-27, with those tables added and the signal rewritten as an outcome outside the product, was signed GO. The rewritten signal, quoted verbatim, is carried forward as O1 in [sahulat-user-stories.md](sahulat-user-stories.md): "a bill due in the household is paid through Sahulat before its due date, and no late surcharge is paid that month"; its first drafting is filed as `gates/gate-1-attempt-2.md` in the product workspace, not reproduced here.
