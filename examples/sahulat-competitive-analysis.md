# Competitive Analysis: Sahulat Bill Pay

Fills [templates/discovery/competitive-analysis.md](../templates/discovery/competitive-analysis.md). Everything here is invented: Sahulat is a fictional mobile-money wallet in Pakistan, its people, agents, customers, billers, bank, aggregator and telco are fiction, and every number, name and date is ILLUSTRATIVE, drawn from the shared data sheet in the [Sahulat journey](sahulat-journey.md) rather than from any real wallet or market. See the [examples index](README.md).

**Owner:** Hira Baig, Product Manager · **Date:** 2026-04-03 · **Refresh by:** one-off for this decision (reopens only if Darya's cut-off moves past 20:00 seven days a week, per D3)

## 1. The decision this informs (mandatory)

- **Decision:** Whether to integrate Darya Bank Limited's BillLink rail or build directly against the BillBridge aggregator for Rel-1 of Sahulat Bill Pay
- **Decided by:** Faisal Mirza · **Needed by:** 2026-04-03
- **What would change the decision:** A settlement cut-off after 20:00 on seven days a week, which removes the weekend-surcharge reproduction that kills the rail's core value proposition, combined with a revenue share leaving Sahulat at least PKR 7 net per bill, matching the BillBridge economics
- **Where the decision gets recorded:** [sahulat-decision-log.md](sahulat-decision-log.md), entry D3

## 2. The job and the current alternatives

- **The job:** Shazia needs her Ravi Power electricity bill and Chenab Gas bill paid before the due date so no late surcharge lands on the next statement, without taking a trip to a bank branch or a bill shop when the office is shut or the queue is long.
- **What they hire today:** Four of eight interviewed customers go to a bank branch; four of eight use a bill shop charging an estimated PKR 30 to 50 per bill (N63, N21). When a due date falls on a weekend, the branch is closed and the shop fee plus the surcharge still apply (E1, T5). For agents like Rafiq, six or seven people a day ask about bill pay and he sends them across the road to a shop that keeps the fee (E3).

## 3. Competitor set

| # | Who | What they are for, in their words | Who they serve | Why they are in this set |
|---|---|---|---|---|
| C1 | Darya BillLink | A ready API and catalogue of 210 billers for fast integration | Wallets needing broad biller coverage quickly | Named vendor alternative evaluated under D3; quoted terms dated 2026-03-30 |
| C2 | BillBridge | An aggregator posting to the biller within 30 minutes, seven days a week, 160 billers | Wallets needing reliable same-day posting | Chosen path under D3 and ADR-1; rate card confirmed 2026-02-10 |
| C3 | Doing nothing / manual workaround | Traveling to a branch or paying a bill-shop fee | All customers today | The status quo the product exists to replace; evidenced by N63, N21, E1, E3 |

## 4. Evidence per competitor

| # | Claim | Source (used it / docs / pricing page / customer said / analyst) | Date checked | Confidence (high / medium / low) |
|---|---|---|---|---|
| C1 | Settlement cut-off is 15:00 on bank working days; later payments post to the biller the next working day | Darya term sheet, quoted | 2026-03-30 | high |
| C1 | Revenue share takes 60 percent of the biller-paid fee, leaving Sahulat PKR 4 per bill | Darya term sheet, quoted | 2026-03-30 | high |
| C1 | Catalogue covers 210 billers | Darya term sheet, quoted | 2026-03-30 | high |
| C2 | Posts to the biller within 30 minutes, seven days a week; settlement to the biller T+1 through Sahulat's settlement bank | BillBridge rate card, quoted | 2026-02-10 | high |
| C2 | Biller-paid fee is PKR 10 per bill; BillBridge takes PKR 3, Sahulat nets PKR 7 | BillBridge indicative quote and rate card, quoted | 2026-01-13 and 2026-02-10 | high |
| C2 | Catalogue covers 160 billers | BillBridge rate card, quoted | 2026-02-10 | high |
| C3 | Three of eight most recent due dates fell on a Saturday or Sunday | Interview notes, bills shown | 2026-02-02 to 2026-02-09 | high |
| C3 | Six of eight customers pay on the due date itself | Interview notes, told | 2026-02-02 to 2026-02-09 | medium |
| C3 | Bill shops charge PKR 30 to 50 per bill | Agent sessions INT-009 to INT-014, told | 2026-02-04 to 2026-02-13 | medium |
| C3 | Agents field six or seven bill questions daily and refer customers to a shop | INT-011 at 06:50, customer said | 2026-02-06 | high |

## 5. Comparison on the axes that matter to the decision

| Axis (why it matters to the decision) | Us today | C1 (Darya BillLink) | C2 (BillBridge) | C3 (Manual/Shop) |
|---|---|---|---|---|
| Weekend and due-date posting (the product exists to remove the surcharge; a rail that delays weekend postings reproduces the problem) | Not built | Fails: 15:00 weekday cut-off pushes weekend-due bills to the next working day (N35) | Passes: posts within 30 minutes, seven days a week (N36) | Fails: branch shut on weekends; shop charges anyway (E1, T5) |
| Net revenue per bill (determines whether the feature can fund agent commissions and support costs) | Target PKR 7 (N32) | PKR 4 (N34) | PKR 7 (N32) | Negative: customer pays PKR 30 to 50 fee (N21); agent earns PKR 0 in v7 (N68) |
| Time to launch (affects whether the board key result of 520,000 active wallets has anything in the pipeline by year end) | Estimated 9 weeks longer via BillBridge (N38) | About 9 weeks sooner on a ready API (N38) | Baseline for comparison | Immediate, but does not move money onto the ledger (N10 pass-through persists) |
| Biller catalogue breadth (affects how many households can use the feature without calling support) | Not built | 210 billers (N37) | 160 billers (N37) | Limited to whatever the local branch or shop accepts |

## 6. So what

- **What this says about the decision:** Darya BillLink loses because its 15:00 weekday cut-off reproduces the exact weekend surcharge the product exists to remove, given that three of eight sampled customers had weekend due dates and six of eight pay on the due date itself. Its PKR 4 net per bill also fails the unit economics needed to sustain the feature. The nine weeks saved do not outweigh shipping a rail that breaks the core promise on day one.
- **Where we are genuinely behind, and whether it matters to this decision:** We are behind on time to launch by about nine weeks and on catalogue breadth by 50 billers. Neither matters to this decision because the cut-off failure is structural, not a gap we can close later, and 160 billers cover the Ravi Power and Chenab Gas references validated in test (N58 shows water failed validation, not that BillBridge lacks breadth for the must-have billers).
- **What we will not copy, and why:** We will not adopt Darya's revenue-share model even if it returns with better timing, because a PKR 4 net leaves no room for the agent commission schedule needed post-pivot (N39 proposes PKR 5, already tight against PKR 7). We will not treat "more billers" as a proxy for readiness; Mehran Water was dropped from Rel-1 not for catalogue size but because three of ten test bills failed reference validation (N58, D5).
- **Open questions that would change the answer:** None outstanding for this decision. D3 records the reopen condition: if Darya's cut-off moves past 20:00 seven days a week, the analysis is refreshed. Open: none assigned, since the condition is external to Sahulat's control.

## 7. Worked micro-example (illustrative, invented; delete once real content exists)

> **Decision:** Whether the first release of a receipt-scanning feature ships our own extraction or a vendor's, decided by the product lead by the end of the month.
> **What would change it:** A vendor priced under our per-receipt cost ceiling that also allows an on-premises deployment for our regulated customers.
> **The job:** A field rep wants a filed expense to be accepted the first time, without typing.
> **What they hire today:** The phone camera plus manual entry, and for two of our largest accounts, an outsourced processing team.
> **So what:** Vendor A clears the accuracy axis and fails the residency axis, which is the axis with a contract behind it, so the first release routes through Vendor B and the residency question goes to legal with a date.

---

## 8. How this analysis fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Feature checklist | Rows of features with ticks, no weighting, no user impact | Compare on the job the user is hiring for, not on counts |
| Cherry-picked set | Only the direct rivals appear, and not the tools users really consider | Include at least one non-obvious substitute per segment |
| Undated claims | "Market leader", or a screenshot with no source and no date | Every claim carries a source and the date it was retrieved |
| No decision attached | A long document ending in "more research needed" | Section 1 names the decision. If none, do not write this document |
| Copying their roadmap | The plan mirrors a rival's recent launches rather than your own thesis | Prioritise against your differentiation, not their shipping log |
| Ignoring the real alternative | A spreadsheet, a manual process, or doing nothing is never scored | Score the status quo as a first-class competitor. It usually wins |

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Checkable by someone who did not do the research. -->

- [x] Section 1 names one decision, one decider, and one date
- [x] The finding that would flip the decision was written before the research started
- [x] The competitor set includes at least one non-product alternative
- [x] Every claim carries a source and a date checked, with secondhand claims labeled
- [x] Comparison axes are the ones that can move this decision, not a feature checklist
- [x] The so-what section commits to a reading rather than listing both sides
- [x] The analysis is linked from the decision log entry it fed

Signed: Faisal Mirza, Chief Executive, 2026-04-03
