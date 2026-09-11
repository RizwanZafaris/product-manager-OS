# Exec Update: Ledgerline Expense Copilot, 2026-12-22

Fills [templates/planning/exec-update.md](../templates/planning/exec-update.md). Everything here is invented: Ledgerline is a fictional company, the Expense Copilot is a fictional product, and every person, number, date and decision is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and its [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Maya Chen · **Period:** 2026-12-08 to 2026-12-22 · **Audience:** Isabel Ferreira and executive staff · **Date:** 2026-12-22
**Sources:** [ledgerline-journey.md](ledgerline-journey.md), [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md).

## 1. Headline

- **Situation:** EXP-1 killed the $6 per seat price on 2026-12-18 because control converted at 2.4% and the anchored arm at 2.9%, so the packaging decision is now PIVOT, D6.
- **Complication:** D7 queues EXP-2 at $2.40 per drafted report, but the DEP2 volume re-quote is still open and the two Enterprise quotes cannot be safely re-opened at the price D6 killed.
- **Resolution:** Direct procurement to return the DEP2 re-quote before EXP-2 opens on 2027-01-11, and keep the Halvard Marine and Ostrander Group quotes withdrawn until EXP-2 resolves, the decision that becomes D10.

## 2. Asks

| Ask | Why now | Options | Our recommendation | Needed by | Cost of no decision by then |
|---|---|---|---|---|---|
| **CFO:** direct procurement to return the DEP2 model-vendor volume re-quote | EXP-2 is the usage re-offer at $2.40 per drafted report, and its margin depends on customer-scale model cost | Open EXP-2 without the re-quote; delay EXP-2; direct procurement to return the re-quote before exposure opens | Direct procurement to return the DEP2 re-quote before EXP-2 opens | 2027-01-11 | EXP-2 cannot open against the customer-scale cost assumption |
| **Ruth Adeyemi and Isabel Ferreira:** keep the Halvard Marine and Ostrander Group quotes withdrawn | D6 killed the seat price, and both Enterprise quotes were priced against that offer | Re-quote both at the killed seat price; hold both quotes withdrawn until EXP-2 resolves | Keep both quotes withdrawn until EXP-2 resolves; this becomes D10 on 2026-12-23 | 2026-12-23 | We re-sell the price D6 killed and create a successor-price commitment before EXP-2 resolves |

## 3. Commitments from the last update

| Commitment made last update | Status (done / on track / slipped to [date] / dropped) | Evidence or reason |
|---|---|---|
| Execute the EXP-1 rule on 2026-12-18 as written | Done, 2026-12-18 | EXP-1 returned KILL under the pre-declared rule, executed by Maya Chen and ratified as D6 |
| Score the German-language eval set by 2026-12-11 | Done, 2026-12-11 | 300 labeled receipts scored at 71% field accuracy against the 90% eval threshold |
| Get procurement's volume re-quote, DEP2, by 2026-12-11 | Slipped, no new date from procurement | DEP2 remains open; procurement owns the date |
| Finish the win-loss batch by 2026-12-16 | Done, signed 2026-12-17 | WL-01 to WL-06 completed by Hana Sato; the batch found that 4 of 6 named seats billed for people who never file, or an add-on priced above the plan |

The 2026-12-08 update held M-002 and M-007 to the 2026-12-18 analysis date rather than reporting figures before the analysis cut.

## 4. Risks and changes

| Risk or change | Movement (new / worse / same / retired) | What we are doing | Ask, if any | Owner |
|---|---|---|---|---|
| R5, the per-seat value metric mismatches the north star and the price fails to convert | Worse, realised | D6 killed the per-seat price and reopened packaging; D7 moves the next bet to usage pricing | Approve the EXP-2 path and keep its 6.0% bar | Maya Chen |
| R6, model cost per drafted report may exceed the margin floor at customer scale | Same, open | Keep DEP2 open and request the volume re-quote before EXP-2 | CFO to direct procurement before 2027-01-11 | Daniel Okafor with procurement |
| R3, foreign-language receipts fail extraction | Same, realised at Wrenfield | Carry the 71% German-language eval result into the next product decision; do not treat the pivot as an extraction-quality fix | None in this update | Priya Nair |
| D6, packaging pivot to a usage metric | New | Hold phase 3, swap the offer page, reopen pricing, and replace the seat offer with EXP-2 | CFO and sales decisions above | Maya Chen (execution); decided by Isabel Ferreira on the metrics review |
| D10, Enterprise quotes remain withdrawn until EXP-2 resolves | New | Keep Halvard Marine and Ostrander Group withdrawn rather than re-quote at the killed seat price | Ruth Adeyemi and Isabel Ferreira to decide | Ruth Adeyemi and Isabel Ferreira |

## 5. Metrics that moved

| Metric | Last update | Now | Why it moved | Confidence | Source |
|---|---|---|---|---|---|
| EXP-1 offer-to-paid conversion, M-007 | Not reported in the 2026-12-08 update; held to the 2026-12-18 analysis date | 2.7% pooled, 73 of 2,748 exposed accounts; control 2.4%, anchored 2.9% | The per-seat offer failed the pre-declared kill line in both arms; the 0.5-point arm difference sits inside a standard error of about 0.6 points | Measured | [ledgerline-journey.md](ledgerline-journey.md), N61 |
| Active add-on accounts, M-002 | Not reported in the 2026-12-08 update; held to the 2026-12-18 analysis date | 79, 73 paid accounts plus 6 design partners | EXP-1 produced 73 paid accounts and the design partners remained active | Measured; G-1 can undercount by up to 3 in the window | [ledgerline-journey.md](ledgerline-journey.md), N64 |
| Share of eligible reports drafted, M-003 | Phase 1: 54% | 47%, 555 of 1,180 eligible reports | The active-account window includes the broader add-on population beyond the six design partners | Measured | [ledgerline-journey.md](ledgerline-journey.md), N44 and N65 |
| First-submission approval on drafted reports, M-006 | Phase 1: 77% | 76%, 422 approved first time | Approval held broadly steady while the pricing conversion failed | Measured; G-2 excludes classic-approvals events without a draft id | [ledgerline-journey.md](ledgerline-journey.md), N44 and N65 |
| Add-on MRR, M-011 | Baseline $0; target $30,000 | $15,906, 53% of target | 73 paid accounts contributed $14,880 across 2,480 seats, and 6 design partners contributed $1,026 across 228 seats at the 25% design-partner discount | Measured | [ledgerline-journey.md](ledgerline-journey.md), N68 and N73 |
| KR1, accounts with the add-on active | Baseline 0; target 180 | Actual 79; score 0.44 | The seat-priced offer converted below the decision rule, limiting active-account growth | Target; measured actual | [ledgerline-journey.md](ledgerline-journey.md), N70 |
| KR2, first-submission approval on drafted reports | Baseline 66%; target 78% | Actual 76%; score 0.83 | Draft quality and reviewer approval remained close to the committed target | Target; measured actual | [ledgerline-journey.md](ledgerline-journey.md), N71 |
| KR3, share of eligible reports drafted in active accounts | Baseline 0; target 50% | Actual 47%; score 0.94 | Draft usage approached the committed target despite the pricing failure | Target; measured actual | [ledgerline-journey.md](ledgerline-journey.md), N72 |
| KR4, add-on MRR | Baseline $0; target $30,000 | Actual $15,906; score 0.53 | The active base and the $6 per seat price produced less MRR than the committed target; the price is now killed | Target; measured actual | [ledgerline-journey.md](ledgerline-journey.md), N73 |

## 6. Commitments for the next period

| Commitment | Date | Owner |
|---|---|---|
| Deliver the usage meter for drafted reports, DEP4, for billing in arrears | 2027-01-08 | Priya Nair with billing |
| Return the DEP2 model-vendor volume re-quote before EXP-2 exposure opens | 2027-01-11 | Procurement, directed by the CFO |
| Open EXP-2 to about 2,818 to 2,821 S-1 accounts not paying (2,675 exposed non-converters plus 152 never exposed, less the 6 design partners and up to 3 G-1 manual-invoice accounts), using the $2.40 per drafted report offer and the 6.0% activation bar | 2027-01-11 | Maya Chen |
| Keep the Halvard Marine and Ostrander Group quotes withdrawn until EXP-2 resolves | 2027-02-12 | Ruth Adeyemi and Isabel Ferreira |

---

## 7. How this update fails while looking complete

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Status theatre | The update reports the pivot as progress but omits the failed price and the slipped DEP2 commitment | Name D6, the failed EXP-1 result, and the slipped commitment in the headline and tables |
| The ask is buried | The DEP2 and Enterprise decisions appear after the metrics | Section 2 carries both decisions, options, recommendations, dates and costs |
| Metrics with no baseline | Conversion and MRR appear as isolated current numbers | Show the last-update state, baseline or target, current value, and source in the same row |
| Silent commitment drops | The four commitments from 2026-12-08 are replaced with a new list | Account for all four commitments before listing the next period |
| Soft risk language | DEP2 is described as a dependency without an owner or consequence | Name procurement, the CFO ask, the exposure date and the cost of opening without the re-quote |
| Written for comfort | The update celebrates approval and drafting while hiding that the price failed | Give the wrong-way conversion, KR1 and KR4 results equal prominence with the metrics that held |

## Exit gate (feeds the gate in progress and the QBR)

- [x] The whole update fits on one page
- [x] The headline is three sentences in situation, complication, resolution order
- [x] Every ask has options, a recommendation, a needed-by date, and a cost of no decision
- [x] Every commitment from the last update is accounted for, including the slipped DEP2 commitment
- [x] Every number traces to the journey or coverage data sheet, with the firmness or confidence note included
- [x] Metrics that moved the wrong way appear with the same prominence as the rest
- [x] Next-period commitments are dated and owned
- [ ] After the meeting: decisions made are logged within a day
- [x] Signed by Maya Chen, 2026-12-22

Signed: Maya Chen, Product Manager, 2026-12-22
