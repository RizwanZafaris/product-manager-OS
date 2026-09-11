# Opportunity Assessment: Sahulat Bill Pay

Fills [templates/discovery/opportunity-assessment.md](../templates/discovery/opportunity-assessment.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan run by a fictional electronic-money institution, Hira Baig and Faisal Mirza are fictional roles, and every figure is ILLUSTRATIVE, drawn from the data sheet in the [Sahulat journey](sahulat-journey.md) so the ten answers agree with the rest of that journey rather than describing any real wallet, market or regulator. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager, the only PM in the company · **Date:** 2026-01-15 · **Requested by:** Faisal Mirza, Chief Executive (who asked for a keep-balance promotion); bill pay itself raised by Hira Baig from the 2026-01-12 helpline trigger · **Status:** Decided, go to discovery (D1, logged 2026-01-16); annotated 2026-08-28
**Sector cards:** [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) · [payments acquiring](../knowledge/domains/payments-acquiring.md)

## 1. The ten questions

1. **What problem does this solve?** A Sahulat wallet holder who owes an electricity or gas bill has no way to pay it from the wallet: the trip to a bank branch or a bill shop still happens, and the wallet earns no part in it. In the four weeks to 2026-01-09 the agent helpline logged 412 calls asking whether Sahulat could pay a bill (N13), against a feature that does not exist.
2. **Who has this problem?** Sahulat wallet holders in Pakistan who receive a monthly electricity or gas bill for their household and reach the wallet mainly through USSD or an agent counter, the majority channels in this domain, rather than the smartphone app. Which of those wallet holders keeps money in the phone long enough to pay a bill from it, rather than cashing in and spending the same day, is exactly what discovery has to find, not something this assessment can answer.
3. **How big is the opportunity?** Sahulat has 1,900,000 registered wallets (N1) and 3,200 active agents already handling cash-in and cash-out (N5). A first ledger cut Sara Lodhi ran for this assessment finds 246,000 wallets with a cash-in on the 5th to 10th of the month (N64), a rough proxy for households already paying something on a bill cycle; ASSUMPTION: the team believes most bills fall due early in the month, calling this a "bill-peak window", and the research plan to follow will test it. Using BillBridge's rate of PKR 10 a bill, with Sahulat keeping PKR 7 (N31, N32), two bills a month across that proxy population gives 246,000 x 2 x PKR 7 = PKR 3,444,000 a month (N65, about PKR 3.44 million), an ILLUSTRATIVE ceiling at full adoption, not a forecast.
4. **What alternatives exist today?** A queue at a bank branch during banking hours, a bill-paying shop that charges a per-bill handling fee, or another wallet or bank app that already pays bills, or simply paying late and absorbing the surcharge, each requiring the customer to be present with cash or the paper bill near the due date, or to accept the surcharge. ASSUMPTION: this is the team's own knowledge of how households in this market pay a utility bill, not a session count; the research plan to follow will test it (it became RQ1).
5. **Why are we suited to win?** The 3,200-agent network (N5) already does the cash-in a bill payment would draw on, and Sahulat already holds the electronic-money license the [mobile money and wallets](../knowledge/domains/mobile-money-wallets.md) card names as the first gatekeeper for holding pooled customer funds. No biller integration, aggregator relationship or agent commission line for bill pay exists yet, so the win is a capability to build on an asset already in hand, not a partnership already signed; nothing yet answers why a customer would choose Sahulat over a wallet or bank app that already pays bills.
6. **Why now?** The board's 520,000-wallet key result for 2026 (N4) has nothing in the pipeline against a 410,000-wallet base (N2), a gap of 110,000 wallets, and registrations alone will not close it in a way that means anything: 61 percent of cash-ins are fully cashed out again within 48 hours (N10), pass-through activity that could nominally satisfy a 30-day-active count while leaving nothing on the ledger, which is why question 8 measures on-ledger payments instead. The 412 helpline calls in four weeks (N13) arrived unprompted, the freshest evidence that the want is real right now, not manufactured by a survey.
7. **How would we take it to market?** Start at the agent counter in one pilot district, since the agent already holds the cash-in relationship the customer trusts; discovery has to name the district and the first biller before this is a plan rather than a direction.
8. **How will we measure success?** The metric is wallets that pay at least one bill in a trailing 30 days, a new input feeding the candidate north star of wallets with at least one on-ledger payment in 30 days, 96,000 wallets in December 2025 (N14), which the [north star metric](../templates/planning/north-star-metric.md) will formalize as M5 once PLANNING opens.
9. **What is critical to get right?** Whether customers keep enough of a balance to fund a bill payment from it, rather than cashing in and paying the same day, the pattern N10's 61 percent pass-through already suggests; and whether a payment posts to the biller reliably enough, before the due date, that a late surcharge does not land anyway. ASSUMPTION: the team believes a late payment carries a surcharge, and that BillBridge would post reliably enough to avoid one; the research plan to follow will test both.
10. **Given all of the above, what do we recommend?** Go to discovery on bill pay, not on the cashback-for-keeping-a-balance promotion Faisal Mirza first proposed. A promotion pays customers to hold a balance before anyone has evidence they will, the exact behavior question 9 names as unproven, and the PKR 3.44 million ceiling in question 3 (N65) is worth discovery time before it is worth a promotion budget spent on an assumption.

## 2. Evidence behind the answers

Every figure below is ILLUSTRATIVE, drawn from the [Sahulat journey's data sheet](sahulat-journey.md#numbers-illustrative). A row with no evidence, marked assumption, is that claim named rather than hidden.

| Question # | Claim | Evidence | Confidence |
|---|---|---|---|
| 1, 6 | 412 helpline calls in the four weeks to 2026-01-09 asked whether Sahulat could pay a bill | Agent helpline, tag BILL-ASK; N13, measured | high |
| 3, 6, 9 | 61 percent of cash-ins are fully cashed out again within 48 hours | Core ledger, query PT-01, Q4 2025; N10, measured | high |
| 3 | 246,000 wallets show a cash-in on the 5th to 10th of the month in two of the last three months | Ledger cut run for this assessment; N64, estimate | medium, one query, not yet checked against real bill-paying behavior |
| 3 | BillBridge would post at PKR 10 a bill, Sahulat net PKR 7 | BillBridge indicative quote, 2026-01-13; N31, N32, quoted | medium, not yet a signed rate card |
| 3, 6 | Board key result is 520,000 30-day active wallets by 2026-12-31, against 410,000 today | Board OKR sheet, December 2025; core ledger; N4 target, N2 measured | high |
| 3 | The 5th to 10th is a "bill-peak window", when most bills fall due | None yet at this assessment's 2026-01-15 date. Amended 2026-08-28: N57 measured bill-peak days in July and August 2026, after this assessment, and confirmed the window | assumption at this date; see the 2026-08-28 amendment |
| 4 | Customers pay today at a bank branch, a bill shop, another wallet or bank app, or pay late | None yet; the team's own market knowledge | assumption |
| 7 | The agent counter is the right first channel to launch in | None yet; the team's own judgment | assumption |
| 9 | Customers will keep a balance in order to pay from it | None yet; runs against the pattern in N10 | assumption, the riskiest one |
| 9 | A late payment carries a surcharge that bill pay would remove | None yet; the team's belief at this date | assumption |
| 9 | BillBridge would post reliably enough that the surcharge does not land anyway | None yet at this assessment's 2026-01-15 date. Amended 2026-08-28: BillBridge's posting SLA (N36), a quoted 30-minute post within seven days, is on the rate card dated 2026-02-10, after this assessment, and is itself a quote, not a measured result | assumption at this date; see the 2026-08-28 amendment |

## 3. Decision

| Field | Answer |
|---|---|
| Recommendation | Go to discovery on bill pay, not on the cashback-for-balance promotion Faisal Mirza first raised |
| The riskiest assumption if we proceed | Customers will keep a balance in order to pay from it, rather than cashing in and paying the same day the way N10's 61 percent pass-through pattern suggests they already treat the wallet. Test: the research plan to follow, with a falsification bar the research plan will set before fielding; owner Hira Baig; feeds the assumptions register at DEFINE |
| Decided by | Faisal Mirza, Chief Executive |
| Logged | D1, 2026-01-16, [decision log](sahulat-decision-log.md#d1-enter-discover-on-bill-pay-not-a-keep-balance-cashback-promotion) |

## Exit gate

This assessment has done its job when:

- [x] All ten questions carry answers of one to three sentences, none left blank
- [x] Every factual claim either links evidence or is marked assumption
- [x] The alternatives answer includes what customers do today, not only named competitors
- [x] The success metric traces to the north star tree or admits it cannot yet
- [x] The recommendation is a decision (go, no, or revisit-on-condition), not "more analysis needed"
- [x] A no-go is recorded with the same care as a go, so the idea does not return unexamined. The rejected cashback-for-balance promotion is recorded with its own argument in question 10 and as the losing option in D1's decision log entry, not left unexamined.

Signed: Faisal Mirza, Chief Executive, 2026-01-16
