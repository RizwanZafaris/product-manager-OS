# Opportunity Solution Tree: Ledgerline Expense Copilot

Fills [templates/discovery/opportunity-solution-tree.md](../templates/discovery/opportunity-solution-tree.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, customers, vendor, prices, counts and dates are fictional, carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Maya Chen, Product Manager · **Started:** 2026-10-19 · **Last fed by:** EXP-1, 2026-12-18
**Trio:** Maya Chen · design lead · Priya Nair

## 1. Outcome

**Outcome:** Increase accounts with the add-on active from 0 to 180 by 2026-12-31. At the last feed, 79 accounts were active, against the target of 180.
**Traces to:** KR1, accounts with the add-on active, baseline 0, target 180, actual 79, score 0.44, aspirational (N70).
**Why this outcome now:** The commercial pass found receipt capture in 9 of 31 lost Business-plan deals, with 7 of those 9 choosing Cinderwick, while the add-on still needed a value metric that customers would accept (N37, D3).

## 2. Opportunity branches

| ID | Opportunity, in the customer's words | Parent | Evidence (note IDs) | Heard how often | Targeted now? |
|---|---|---|---|---|---|
| OST-O1 | “The report comes back because the receipt or category does not match, and someone has to check it again.” | root | EV-C01 to EV-C06, LC2 | 6 of 6 interviews | yes |
| OST-O2 | “We keep a separate spreadsheet to keep the receipt and category work under control.” | root | EV-C01, EV-C02, EV-C04, EV-C06, LC2 | 4 of 6 interviews | no |
| OST-O3 | “We need receipt capture, but adding another vendor means another tool and another relationship to manage.” | root | EV-C02, EV-C03, EV-C08, N37, LC2 | 3 of 9 discovery sources named a separate receipt tool, including 2 of 6 interviews | no |
| OST-O4 | “Do not bill me for people who never file.” | root | WL-01, WL-04, EV-AB01, LC5, N77, N78 | 4 of 6 win-loss interviews and 6 of 8 advisory-board members | yes |

**Target selection:** OST-O1 remains targeted because it is the most frequent pain and connects directly to first-submission approval, the customer outcome behind the add-on. OST-O4 became targeted after the win-loss and advisory-board evidence showed that the seat value metric charged for non-filers. OST-O2 and OST-O3 remain live branches, but lose this cycle because the spreadsheet and separate-vendor evidence explain the alternatives rather than identify the next test after the EXP-1 kill.

## 3. Solutions per targeted opportunity

| ID | Solution sketch (one sentence) | Opportunity | Comparison status |
|---|---|---|---|
| OST-S1 | Sell the Expense Copilot as an add-on inside the Ledgerline Expenses workflow, where drafts are reviewed before submission. | OST-O1 | compared against reselling Cinderwick and the free bundle |
| OST-S2 | Resell Cinderwick's receipt-capture service to Ledgerline accounts that want the capability. | OST-O1 | rejected comparison, because it adds the separate vendor relationship and does not use the Ledgerline approval flow |
| OST-S3 | Bundle the Expense Copilot free into the Business plan. | OST-O1 | rejected comparison under D2, because the free bundle has no revenue line and its model cost is about 1.9 points of Business-plan gross margin at the 60% drafted-share assumption (N50, N51) |
| OST-S4 | Re-offer the add-on at $2.40 per drafted report, billed monthly in arrears, with no seat charge or minimum. | OST-O4 | compared against LEDGERLINE-S4; proposed for EXP-2 (N89, D7) |
| OST-S5 | Let an account admin see how many seats would be billed and which users filed a report last quarter before activation. | OST-O4 | compared against the usage price; proposed as LEDGERLINE-S4 from WL-01 and WL-04 |

## 4. Assumptions per solution

| ID | Assumption | Solution | Type | Risk if wrong (H/M/L) | Evidence today |
|---|---|---|---|---|---|
| OST-A1 | Business-plan account admins will activate the add-on when it is priced at $6 per plan seat per month, including when the offer is anchored on reviewer cost. | OST-S1 | desirability / viability | H | D3, N46, EXP-1 |
| OST-A2 | A usage price of $2.40 per drafted report will activate accounts at or above the 6.0% success bar without breaking the margin floor. | OST-S4 | desirability / viability | H | N49, N89, EXP-2 |
| OST-A3 | Showing billed seats and recent filers before activation will reduce the objection from accounts with few filers. | OST-S5 | desirability | M | WL-01, WL-04, N77, LEDGERLINE-S4 |
| OST-A4 | The free bundle would cost more than the one-point Business-plan gross-margin rule allows without its own revenue line. | OST-S3 | viability | H | D2, N50, N51 |

## 5. Assumption tests

| Assumption | Smallest test design | Pass / kill signal | Status | Result |
|---|---|---|---|---|
| OST-A1 | Run EXP-1 with S-1 accounts split by account id into a plain per-seat offer and an anchored per-seat offer, exposed from 2026-11-23 to 2026-12-04, with a 14-day conversion window. | Ship at 6.0% or better in the anchored arm; iterate between 4.0% and 6.0%; kill when both arms are under 4.0%, subject to the guardrails. | done | KILL. Control was 33 of 1,371, or 2.4%; anchored was 40 of 1,377, or 2.9%; pooled conversion was 73 of 2,748, or 2.7%. The 0.5-point difference sat inside a standard error of about 0.6 points (N61, N62). |
| OST-A2 | Run EXP-2 as a single-arm re-offer to about 2,818 to 2,821 S-1 accounts not paying, after the usage meter lands, with exposure planned from 2027-01-11. | Activate at 6.0% or more within 14 days; kill under 4.0% at the analysis date or on 2027-02-12, whichever comes first. | planned | No result yet. EXP-2 remains open, with M-009 at most $1.05, M-006 at least 70%, and M-010 at most 8 per week as counter-metrics (N91, N92). |
| OST-A3 | Show the billed-seat count and recent-filer list before activation, then ask the account admin whether the information resolves the pricing objection in the WL-01 and WL-04 pattern. | Continue LEDGERLINE-S4 if the objection is resolved for the affected accounts; otherwise keep it parked and do not treat visibility as a pricing fix. | planned | No test result yet. LEDGERLINE-S4 is proposed from WL-01 and WL-04 and is superseded by LEDGERLINE-S6 if the usage price ships. |
| OST-A4 | Compare the free-bundle model cost with Daniel Okafor's one-point gross-margin rule using the existing drafted-share assumption. | Kill the free bundle when its model cost exceeds one point of Business-plan gross margin without a revenue line. | done | KILL under D2. At the 60% drafted-share assumption, the bundle is about 965,000 receipts and about $212,000 a year in model cost, about 1.9 points of Business-plan gross margin (N50, N51). |

**This week's test:** EXP-1, owned by Maya Chen, used the analysis slot on 2026-12-18. It was done at the last feed and killed OST-A1 under the pre-declared rule. The next planned test is EXP-2, owned by Maya Chen, after DEP4 lands.

---

## Exit gate (feeds Gate 1: problem worth solving)

- [x] One outcome, traced to a named north star input metric or key result. The tree traces to KR1, N70.
- [x] Every opportunity branch cites at least one evidence note ID, or is marked assumption with an interview slot against it. OST-O1 to OST-O3 cite EV-C01 to EV-C09 or the associated synthesis rows; OST-O4 cites WL-01, WL-04 and EV-AB01.
- [x] Targeted opportunities were selected by comparison, and the losing branches show why they lost. OST-O1 and OST-O4 are targeted; OST-O2 and OST-O3 remain live but are not the next test branches.
- [x] Every targeted opportunity carries at least two compared solutions, or a labeled single-solution bet. OST-O1 carries three compared solutions; OST-O4 carries two.
- [x] Every solution's riskiest assumption has a test designed, and at least one test is live this week. OST-A1 was tested by EXP-1 and killed; OST-A2 is pre-declared for EXP-2; OST-A3 and OST-A4 have tests or decision checks recorded.
- [x] "Last fed by" is within two weeks; a staler tree re-earns its branches before it feeds a gate. The tree was last fed by EXP-1 on 2026-12-18.

Signed at the discovery gate: Maya Chen, Product Manager, 2026-12-18
