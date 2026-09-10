# Opportunity Assessment: Sahulat Bill Pay

Fills [templates/discovery/opportunity-assessment.md](../templates/discovery/opportunity-assessment.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan run by a fictional electronic-money institution, Hira Baig and Faisal Mirza are fictional roles, and every figure is ILLUSTRATIVE, drawn from the data sheet in the [Sahulat journey](sahulat-journey.md) so the ten answers agree with the rest of that journey rather than describing any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-01-15 · **Requested by:** Faisal Mirza, Chief Executive · **Status:** Decided, go to discovery (D1, logged 2026-01-16)
**Sector cards:** [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) · [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. The ten questions

1. **What problem does this solve?** A Sahulat wallet holder who owes an electricity or gas bill has no way to pay it from the wallet: the trip to a bank branch or a bill shop still happens, and the wallet earns no part in it. In the four weeks to 2026-01-09 the agent helpline logged 412 calls asking whether Sahulat could pay a bill (N13), against a feature that does not exist.
2. **Who has this problem?** Sahulat wallet holders in Pakistan who receive a monthly electricity or gas bill for their household and reach the wallet mainly through USSD or an agent counter, not the smartphone app, the majority channel this domain runs on. Which of those wallet holders keeps money in the phone long enough to pay a bill from it, rather than cashing in and spending the same day, is exactly what discovery has to find, not something this assessment can answer.
3. **How big is the opportunity?** Sahulat has 1,900,000 registered wallets (N1) and 3,200 active agents already handling cash-in and cash-out (N5). An early cut of the ledger, the same query Sara Lodhi would formalize in February as BP-01, finds 246,000 wallets with a cash-in on the 5th to 10th of the month, the bill-peak window, in two of the last three months (N64), a rough proxy for households already paying something on a bill cycle. At an early, informal figure from BillBridge ahead of its dated rate card, PKR 10 a bill with Sahulat keeping PKR 7 (N31, N32), two bills a month across that proxy population gives 246,000 x 2 x PKR 7 = PKR 3,440,000 a month (N65), an ILLUSTRATIVE ceiling at full adoption, not a forecast. Set beside the board's 2026 key result of 520,000 30-day active wallets (N4) against 410,000 today (N2), that is a gap of 110,000 wallets with nothing else in the pipeline.
4. **What alternatives exist today?** A queue at a bank branch during banking hours, or a bill-paying shop that charges a per-bill handling fee, both requiring the customer to be present with cash or the paper bill near the due date. ASSUMPTION: this is the team's own knowledge of how households in this market pay a utility bill, not a session count; RQ1 in the research plan exists to test it properly.
5. **Why are we suited to win?** The 3,200-agent network (N5) already does the cash-in a bill payment would draw on, and Sahulat already holds the electronic-money license the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) card names as the first gatekeeper for holding pooled customer funds. No biller integration, aggregator relationship or agent commission line for bill pay exists yet, so the win is a capability to build on an asset already in hand, not a partnership already signed.
6. **Why now?** The board's 520,000-wallet key result for 2026 (N4) has nothing in the pipeline against a 410,000-wallet base (N2), and registrations alone will not close that gap: 61 percent of cash-ins are fully cashed out again within 48 hours (N10), a remittance pass-through wearing an inclusion story rather than money staying on the ledger. The 412 helpline calls in four weeks (N13) arrived unprompted, the freshest evidence that the want is real right now, not manufactured by a survey.
7. **How would we take it to market?** Start at the agent counter in one pilot district, since the agent already holds the cash-in relationship the customer trusts; discovery has to name the district and the first biller before this is a plan rather than a direction.
8. **How will we measure success?** The candidate north star is wallets with at least one on-ledger payment in the trailing 30 days, 96,000 wallets in December 2025 (N14) on the query the [north star metric](../templates/planning/north-star-metric.md) will formalize as M5 once PLANNING opens; bill pay would be the first new payment type feeding it.
9. **What is critical to get right?** Whether customers keep enough of a balance to fund a bill payment from it, rather than cashing in and paying the same day, the pattern N10's 61 percent pass-through already suggests; and whether a payment posts to the biller reliably enough, before the due date, that the surcharge this product exists to remove does not land anyway.
10. **Given all of the above, what do we recommend?** Go to discovery on bill pay, not on the cashback-for-keeping-a-balance promotion Faisal Mirza first proposed. A promotion pays customers to hold a balance before anyone has evidence they will, the exact behavior question 9 names as unproven, and the PKR 3,440,000 ceiling in question 3 (N65) is worth discovery time before it is worth a promotion budget spent on an assumption.

## 2. Evidence behind the answers

Every figure below is ILLUSTRATIVE, drawn from the [Sahulat journey's data sheet](sahulat-journey.md#numbers-illustrative). A row with no evidence, marked assumption, is that claim named rather than hidden.

| Question # | Claim | Evidence | Confidence |
|---|---|---|---|
| 1, 6 | 412 helpline calls in the four weeks to 2026-01-09 asked whether Sahulat could pay a bill | Agent helpline, tag BILL-ASK; N13, measured | high |
| 3, 6, 9 | 61 percent of cash-ins are fully cashed out again within 48 hours | Core ledger, query PT-01, Q4 2025; N10, measured | high |
| 3 | 246,000 wallets show a cash-in on the bill-peak window in two of the last three months | Early cut of the query later formalized as BP-01; N64, estimate | medium, one query, not yet checked against real bill-paying behavior |
| 3 | BillBridge would post at PKR 10 a bill, Sahulat net PKR 7 | Informal BillBridge conversation ahead of its dated rate card; N31, N32, estimate at this date | medium, not yet a signed rate card |
| 3, 6 | Board key result is 520,000 30-day active wallets by 2026-12-31, against 410,000 today | Board OKR sheet, December 2025; core ledger; N4 target, N2 measured | high |
| 4 | Customers pay a utility bill today at a bank branch or a bill shop | None yet; the team's own market knowledge | assumption |
| 9 | Customers will keep a balance in order to pay from it | None yet; runs against the pattern in N10 | assumption, the riskiest one |

## 3. Decision

| Field | Answer |
|---|---|
| Recommendation | Go to discovery on bill pay, not on the cashback-for-balance promotion Faisal Mirza first raised |
| The riskiest assumption if we proceed | Customers will keep a balance in order to pay from it, rather than cashing in and paying the same day the way N10's 61 percent pass-through pattern suggests they already treat the wallet |
| Decided by | Faisal Mirza, Chief Executive |
| Logged | D1, 2026-01-16, in the decision record inside the [Sahulat journey's shared identifiers](sahulat-journey.md#shared-identifiers); the standalone decision log fills at DEFINE |

## Exit gate

This assessment has done its job when:

- [x] All ten questions carry answers of one to three sentences, none left blank
- [x] Every factual claim either links evidence or is marked assumption
- [x] The alternatives answer includes what customers do today, not only named competitors
- [x] The success metric traces to the north star tree or admits it cannot yet
- [x] The recommendation is a decision (go, no, or revisit-on-condition), not "more analysis needed"
- [ ] A no-go is recorded with the same care as a go, so the idea does not return unexamined. Not tested this round: the recommendation is a go on bill pay; the only no-go here is the narrower promotion path in question 10, argued with the same evidence as the go.

Signed: Faisal Mirza, Chief Executive, 2026-01-16
