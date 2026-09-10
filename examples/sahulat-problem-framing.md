# Problem Framing: Sahulat Bill Pay

Fills [templates/discovery/problem-framing.md](../templates/discovery/problem-framing.md). Everything here is invented: Sahulat is a fictional mobile-money wallet run by a fictional Pakistani electronic money institution, every person, quote, call count and PKR figure is invented to agree with the rest of the [Sahulat journey](sahulat-journey.md), and none of it describes any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM · **Date:** 2026-02-16 · **Status:** Framed for Gate 1; revised 2026-02-23 after Gate 1 attempt 1 was returned on 2026-02-20, signed GO at Gate 1 attempt 2 on 2026-02-27

## 1. Situation

Sahulat Digital runs a mobile-money wallet with 1,900,000 registered wallets and 3,200 active agents as of 2025-12-31. Most customers reach it over a USSD short code on a feature phone or through an agent behind a counter rather than through a smartphone app, and cash moving into a wallet has always run well ahead of any use of that money once it is there: 61 percent of cash-ins were fully cashed out again within 48 hours in the quarter ending 2025-12-31, a pattern the team already knew going into 2026 and treats as ordinary. Households in this customer base pay recurring utility bills, most commonly electricity and gas, each due on a fixed date printed on a paper bill, and today none of those bills touches the wallet at any point.

## 2. Complication

In the four weeks to 2026-01-09, the agent helpline logged 412 calls tagged as customers asking whether Sahulat could pay an electricity or gas bill, a feature that did not exist. Set beside the 61 percent cash-out pattern, the two numbers pointed at the same fact from two directions: money enters the wallet and leaves again with nothing keeping it there, and the board's 2026 key result of 520,000 30-day active wallets, against 410,000 active at the end of 2025, had nothing in the product roadmap that would close that gap. On 2026-01-12, Hira Baig put the 412 calls and the 61 percent side by side and asked what a customer was actually trying to do that the wallet could not yet do for them. Fourteen research sessions followed, eight customers and six agents, run 2026-01-26 to 2026-02-13, and this document is their synthesis.

## 3. Problem statement

> A household that already holds a mobile-money wallet needs a way to settle a monthly electricity or gas bill by its due date without a dedicated trip during business hours, because missing that window adds a surcharge to the next bill, but today no such option reaches that household through the channel it already uses, so it travels to a bank branch or pays someone to do it for them, which costs the household about 14 hours a year and, depending on which of those costs it incurs, roughly PKR 720 to PKR 3,320 a year in cash.

## 4. Evidence

| # | Evidence item | Type | Source or ID | Strength |
|---|---|---|---|---|
| 1 | "The bill was due on a Sunday. The bank was shut, the shop man charged me fifty, and the office still put the fine on the next bill." | interview | INT-004 (C-04), 2026-02-02 | weak (n=1 session; corroborated by 3 of 8 sample due dates falling on a weekend) |
| 2 | "I only put money in the phone when I need to send it that day. Why would I leave it there?" | interview | INT-004 (C-04), 2026-02-02 | weak (n=1 session; consistent with theme T2 in the research plan, seen in 6 of 8 customer sessions) |
| 3 | "Six or seven people a day ask me if I can do their bill. I send them to the shop across the road and he keeps the fifty." | interview | INT-011, agent session (2026-02-04 to 2026-02-13) | weak (n=1 agent; not independently tallied across the six agent sessions) |
| 4 | "The screen went off in the middle and I did not know if the money went. I waited ten minutes for the message and then dialed again." | interview | INT-007 (C-07), 2026-02-06 | weak (n=1 session; channel-reliability context, not counted toward the arithmetic below) |

None of these four is a metric from Sahulat's own systems; all four are single-session quotes from the fourteen-session round and are labeled weak for that reason. The tallies in sections 5 and 6 below come from the same fourteen sessions counted across the full sample, which is the stronger evidence behind this framing.

## 5. Cost of inaction

**To the user:** a household in the interview sample pays this cost every month a bill is due, in time it always spends and cash it spends only when a payment fails or is handed to someone else (ILLUSTRATIVE, all rows from the household arithmetic worked in the research synthesis).

| Component | Amount | Basis |
|---|---|---|
| Trips to pay bills | 14 hours a year (12 trips a year x 70 minutes a trip) | median trip length across 8 customer sessions |
| Transport | PKR 720 a year (12 x PKR 60 a trip) | median transport cost across 8 customer sessions |
| Late surcharges | PKR 800 a year, for the 5 of 8 households in the sample who paid one (4 occurrences x PKR 200) | 4 of the 5 surcharge bills were shown, not only described |
| Fee to a bill shop | PKR 1,080 to PKR 1,800 a year, for the 4 of 8 households in the sample who pay a shop to do it (3 bills x PKR 30 to 50 a bill x 12 months) | told, agent sessions and customer sessions agree on the PKR 30 to 50 range |

The 14 hours and PKR 720 in transport apply to every household in the sample; the surcharge row and the shop-fee row apply to different, partly overlapping halves of it. A household that both pays a surcharge and uses a shop is exposed to roughly PKR 2,600 to PKR 3,320 a year in cash on top of the 14 hours; a household that does neither still loses the 14 hours and PKR 720.

**To the business:** the same 61 percent pattern that triggered this inquiry has a monthly cost the business already pays, whether or not it ever builds bill pay (ILLUSTRATIVE, from the business arithmetic worked in the opportunity assessment).

| Component | Amount | Basis |
|---|---|---|
| Pass-through cycles a month | 701,500 (1,150,000 cash-ins x 61 percent) | core ledger, December 2025, query PT-01 |
| Agent commission paid on money that never stays | about PKR 24.6 million a month (701,500 x PKR 35, the PKR 15 cash-in and PKR 20 cash-out commission combined) | commission schedule v6, 2025-10-01 |
| Board key-result gap | 110,000 wallets (520,000 target for 2026-12-31 minus 410,000 active at 2025-12-31) with nothing in the roadmap to close it | board OKR sheet, December 2025 |

The PKR 24.6 million a month is commission the business already pays for cash that touches the wallet and leaves the same day; it is not a projection of what bill pay would earn, only what today's pattern already costs.

**Trajectory:** stable and, on its own, not self-correcting. Fourteen sessions gave no reason to expect the 61 percent pattern to improve without a reason to keep money in the wallet: money enters for a purpose and leaves the same day in 6 of 8 customer sessions (theme T2), and the two sessions that contradict it are one persona's worth of evidence, not a trend. If anything the channel these households already use is about to get a little more expensive: Falak Telecom's tariff notice of 2025-12-18 raises the USSD session rate from PKR 0.40 to PKR 0.65, effective 2026-10-01, which does not create this problem but does not fade it either.

## 6. Who feels it and how often

| Segment | How many | Frequency of the pain | Severity |
|---|---|---|---|
| Households with a wallet whose cash-in pattern matches a bill-paying customer | about 246,000 wallets (a proxy: wallets with a cash-in on the 5th to the 10th of the month in 2 of the last 3 months, query BP-01, ILLUSTRATIVE estimate) | 3 bills a month per household in the interview sample, electricity, gas and water, each with its own due date | slows a task every household already has to do, and turns into a real cash loss whenever the trip fails to land before the due date |
| Agents fielding bill questions they cannot resolve | 3,200 active agents; the helpline alone logged 412 such calls in 4 weeks | multiple times a day per agent, by one agent's own account | sends business the agent could have kept to a competing shop, unpaid |

## 7. Constraints on any resolution

Any resolution must sit inside the scope of activities permitted under Sahulat Digital's electronic money institution licence, granted under the State Bank of Pakistan's EMI Regulations; a flow that involves settling money to a biller, not only moving it between wallets, may need its own compliance filing before launch, which is why Amna Rasheed, head of compliance, is a party to this decision even though bill pay does not exist yet as a feature. Customers reached through the agent network and the USSD channel sit across more than one KYC tier under the branchless-banking tiered due-diligence regime described in the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) sector card; a resolution that assumed every customer already held the wallet's higher tier would exclude the same low-balance, cash-based households this problem describes, so no resolution may treat a tier upgrade as a precondition. This document does not consider what happens once a bill payment is approved and its posting to a biller fails afterward; that question belongs to whichever resolution DESIGN produces, and the [payments acquiring](../knowledge/domains/payments-acquiring.md) sector card is the reference for it at that point, not this one. The company has one product manager and nine engineers in total; any commitment past Gate 1 competes with whatever else those nine engineers already carry, a capacity constraint this document does not attempt to size. The board's 2026 key result of 520,000 30-day active wallets by 2026-12-31 is a fixed year-end deadline that bounds how long DEFINE and DESIGN can run if this problem is funded. Open: Faisal Mirza, a budget ceiling for the DEFINE stage has not been set as of this writing.

## 8. Decision requested

- **Ask:** fund definition, that is, carry this problem from DISCOVER into DEFINE rather than returning to more discovery or retiring it.
- **From:** Faisal Mirza · **By:** 2026-02-20

## Exit gate

(feeds Gate 1: problem worth solving)

- [x] Exactly one problem in this file: settling a recurring utility bill by its due date, nothing else.
- [x] Problem statement contains no solution words: no product, feature or channel is named in section 3.
- [x] Every evidence row has a source ID and a strength label: E1 to E4, all labeled weak with the reason stated.
- [x] Cost of inaction carries a number or a named owner and date for the number: section 5 carries both, and the one open figure, the DEFINE budget ceiling, has an owner in section 7.
- [x] A single accountable owner is named: Hira Baig, in the header.
- [x] The decision requested names the sponsor and a date: Faisal Mirza, by 2026-02-20, in section 8.

This checklist is the author's own read of the file, not a gate result. Gate 1 itself was walked and signed by Faisal Mirza as sponsor and Hira Baig as owner: attempt 1 on 2026-02-20 returned this file for a cost of inaction with no arithmetic behind it, which is why section 5 above carries the household and business tables rather than a sentence; attempt 2 on 2026-02-27, with those tables added, was signed GO.
