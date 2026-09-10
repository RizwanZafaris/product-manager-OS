# Pricing and Packaging: Expense Copilot Add-on

Fills [templates/planning/pricing-packaging.md](../templates/planning/pricing-packaging.md). Everything here is invented: Ledgerline is a fictional mid-market software company, Cinderwick is a fictional competitor, and every price, discount, margin figure and date is ILLUSTRATIVE, built for this repository so the arithmetic can be checked, not as a benchmark or a target to copy. See the [examples index](README.md).

**Owner:** Isabel Ferreira, Chief Product Officer, the one person who can approve a price change · **Date:** signed 2026-11-03, section 1 reopened 2026-12-21 · **Status:** Signed then reopened. D6 reopened section 1 on 2026-12-21 after the per-seat price failed its own kill rule; sections 2 through 5 still describe the price as it was sold between 2026-11-03 and 2026-12-21 and are marked where they no longer hold · **Positioning doc:** the positioning document for this add-on, which sets the category's pricing assumptions and is not yet filed in this workspace

## 1. Value metric

Figures in this section are ILLUSTRATIVE. The add-on sells into the 6,400 Business-plan accounts (N26) at a $149-a-month list price (N27) and about 78% gross margin (N28), roughly $11.4M of ARR (N29). Of those, 2,900 accounts are active in Expenses (S-1, N32), filing about 96,000 reports in Q3 alone (N33) at a median first-submission approval of 66% (N35). This document is signed against D1: reuse internal evidence only where a written reason says it transfers.

| Field | Answer |
|---|---|
| Unit we charge by | Plan seats: the account's total Business-plan seat count, at $6 per seat per month (N46) |
| How it tracks delivered value | Poorly. A seat held by someone who never files still gets billed, and an account with many filers and few seats gets relatively cheap access. It tracks the plan's own seat count, not the reports the copilot drafts (M-001), because billing can already meter seats (ADR-007) and no other meter existed at signing (DEP4) |
| North star tie | Mismatch, accepted in writing at D3 because billing already meters seats and sales forecasts in seats. D3 also names the condition that reopens it: the EXP-1 kill rule firing, or a win-loss pattern naming seats. Both happened, R5 was realised on 2026-12-18 (N61) and the win-loss batch found the same pattern (N77), and section 1 is reopened as of 2026-12-21 (D6) |
| Evidence customers accept this unit | Assumption, not evidence. Two other units were scored and rejected at D3: per drafted report, which tracks value but had no meter (DEP4), and per active filer, which had no agreed definition. Plan seats was the only unit billing could already charge by. The design-partner interviews (N40, EV-C01 to EV-C06, six finance leads, 2026-10-19 to 2026-10-28) found that 5 of 6 would pay "something" and 4 of 6 keep a spreadsheet today, but 0 of 6 were asked a price, let alone a per-seat price. Nobody validated that this specific unit is what a buyer accepts |

## 2. Pricing model

- **Model:** Subscription add-on, billed monthly per plan seat, layered on top of the existing Business-plan subscription. Not usage-based, not freemium, not a one-time fee.
- **Why this model for this buyer:** Business-plan buyers already buy the base platform per seat (N27), and the nearest competitive alternative, Cinderwick, sells the same way at $8 a seat a month (N13). Billing could already meter and charge by seat under ADR-007, while a usage meter for drafted reports did not exist (DEP4), so the model that could ship for phase 1 on 2026-11-10 (N43) was the seat model, not the model the evidence most favoured.
- **Failure mode accepted:** Seat pricing bills for people who hold a plan seat but rarely file, so an account's price scales with headcount rather than with the reports the copilot drafts. Per the [B2B SaaS card](../knowledge/domains/saas-b2b.md), what drives expansion, seats, usage or tier upgrades, is supposed to be a decision, not an accident; this is the accident. The honest reason for the choice was what billing could already do, not what the evidence favoured. Building the seat meter itself cost about 1.5 person-months, about $15,000 at the $10,000-a-person-month engineering rate (N12, N86), and does not carry over to a usage price if one ships.

Every drafted report also carries a fully loaded model cost, about $0.92 at the quoted rate (N9 to N11), quoted but not contracted (DEP2). Per the [AI products card](../knowledge/domains/ai-products.md), a margin built on today's token price needs a dated assumption, and this is one: the $6 seat price clears the 60% gross-margin floor on the model line only while the quote holds (N49), and R6 tracks the exposure if the volume re-quote (DEP2) comes back worse.

**Rejected: free bundle (D2).** Bundling the copilot at no charge into the Business plan was argued twice, by sales at the positioning session on 2026-10-30 and by a design partner at this pricing review, and lost both times on margin. At the business case's own 60% adoption assumption, a free bundle across the 2,900 S-1 accounts drafts about 229,680 reports a year, about 965,000 receipts at 4.2 receipts a report (N10), about $212,000 a year in model cost at the $0.22 quoted rate (N9), about 1.9 points of the 78% Business-plan gross margin (N28, N51). At 100% adoption the cost is about $354,000 a year, about 3.1 points (N52). Even a friendlier re-quote does not flip the arithmetic: at an assumed $0.14 a receipt, the volume DEP2 is chasing, a free bundle still costs about $135,000 a year, about 1.2 points (N53). Daniel Okafor's rule, recorded at D2: no feature costing more than one point of Business-plan gross margin ships without its own revenue line (N50). A ten-report free allowance was rejected too, on the grounds that the accounts that need the product most are exactly the accounts that would exhaust it.

## 3. Tiers and packaging

| Tier | Price | Aimed at | What is included | What moves them to the next tier |
|---|---|---|---|---|
| Copilot add-on (ILLUSTRATIVE) | $6 per plan seat per month (N46) | Business-plan accounts in the best-fit segment S-5: approval under 75% and 5 or more filers, 1,240 accounts (N36), drawn from the 2,900 accounts active in Expenses (S-1, N32) | Receipt capture and draft, policy-line matching and reviewer confidence flags (LEDGERLINE-S2, LEDGERLINE-S3), and the account-level approval-rate tile (LEDGERLINE-S5) | Open: Isabel Ferreira and Maya Chen own this. No upgrade tier exists in v1. Enterprise accounts (S-6, 310 accounts, N31) are sold bespoke outside this price list rather than through a named higher tier |

The [good-better-best worksheet](../frameworks/pricing/packaging-good-better-best.md) was read before this table was built. Its own skip clause applied on the surface, one segment and one job, so this document runs a single tier rather than three. Its own ILLUSTRATIVE worked example for this same product, though, prices by active filer per month, not seats, precisely the unit D3 could not use because no meter existed (DEP4). The worksheet was consulted and then not followed on the value metric; section 1 records why, and section 6 records that the gap came back to bite.

## 4. Competitive benchmark

Table below is ILLUSTRATIVE.

| Alternative | Their unit | Their price | Where we sit relative, and why that is defensible |
|---|---|---|---|
| Cinderwick, a seat-priced receipt-capture vendor | Per seat per month | $8.00 per seat per month, quoted 2026-08-13 for 900 seats (N13) | $6 sits 25% under Cinderwick's $8 (N46). Defensible because Cinderwick is a stand-alone product needing its own integration, while the add-on activates inside the platform the account already runs |
| Spreadsheet, or typing straight into the Expenses form | No charge, no vendor | $0 explicit price | Positioned against, not priced against: 4 of 6 design-partner finance leads keep a spreadsheet today (N40). The true cost is the filer's and reviewer's own time, at $55 and $60 an hour (N6), which this document does not re-argue in dollars, only flags as the real competitor |

What this table never carried, at signing on 2026-11-03 or at the 2026-12-21 reopening, is a row for the account's own Business-plan price. A median S-1 account runs 34 seats (N34); at $6 a seat the add-on costs $204 a month (N47), against a $149-a-month Business plan (N27), about 137% of the plan itself. Nobody benchmarked the add-on against the product it was bolted onto, only against the competitor and the free alternative. The win-loss review found this later in the buyer's own words (N77): 4 of 6 interviews named seats billed for people who never file, or an add-on priced above the plan. That row is not added here as an after-the-fact fix, because the point this document records is that it was missing when the price was set.

## 5. Discount rules

Table below is ILLUSTRATIVE.

| Situation | Maximum discount | Approver | Expires |
|---|---|---|---|
| Annual prepay | 15% off list (N48) | Ruth Adeyemi, VP Sales (P6) | Contracted prices hold for 12 months from signing (N48) |
| Design partner, one of the six named accounts activated in 2026-11 (S-2, N41) | 25% off list for 12 months (N42) | Isabel Ferreira, Chief Product Officer (P4) | Offer expires 2026-12-31 for new partners. The six existing partners hold their 25% until each account's own 12-month term ends |
| Anything else | 0%, no standing exception | Isabel Ferreira, Chief Product Officer (P4), logged in the [decision log](../templates/execution/decision-log.md) | Per request, approved before it is offered, no standing expiry |

These rules were signed 2026-11-03, six days before phase 1 opened to the first design partner on 2026-11-10 (N43), before the first negotiation. No discount outside this table has been logged as of the 2026-12-22 growth plan (N74). Separately, and outside this table because it is a price hold rather than a discount: the 73 accounts that paid during EXP-1 (N60, N64) keep their $6-per-seat price for 12 months from activation before any migration to a successor price (N93, N48).

## 6. Review

- **Review cadence:** Every two quarters, and at each Gate 6 review of the add-on, aligned to the OKR cycle running 2026-11-02 to 2026-12-31 (N69).
- **What triggers an off-cycle review:** A win-loss pattern naming the value metric, a competitor price move, or the EXP-1 experiment's own pre-declared kill rule (N57). Two of those three fired together here: R5 was realised on 2026-12-18 (N61), 4 of 6 win-loss interviews named seats or a price above the plan unprompted (N77), and the advisory board said the same thing three weeks earlier, on 2026-12-02, with 6 of 8 members present agreeing (N78, EV-AB01).
- **Next review:** Open: Isabel Ferreira and Maya Chen own the date. It is not scheduled ahead of EXP-2's own kill-or-ship date of 2027-02-12 (N92); section 1 stays open until that result is known.

A price change worth testing before committing runs as a pricing experiment through [experiment-brief.md](../templates/operate/experiment-brief.md), decision rule and all, before it lands in section 2. EXP-1, the per-seat offer anchored on the reviewer's hourly cost, ran exactly this test between 2026-11-23 and 2026-12-04 (N54 to N62) and is the reason section 1 is reopened. EXP-2, the usage re-offer at $2.40 per drafted report (N89), is queued to become the next section 2 entry once the usage meter ships (D7, DEP4), and this document is due to be re-signed once EXP-2's own kill-or-ship date resolves.

## Exit gate

This pricing is fit to publish when:

- [x] The value metric is stated, tied to the north star tree or the mismatch is accepted in writing. Section 1 states the mismatch and the reopening condition; D3 accepted it on 2026-11-03.
- [x] The model names its accepted failure mode. Section 2 names it: seats bill headcount, not reports drafted.
- [ ] Every tier aims at a named segment and names its upgrade trigger. The single tier names its segment (S-5) but no upgrade trigger exists in v1; there is nothing above it to move a customer toward.
- [ ] The benchmark includes the customer's real alternative, dated and sourced. Cinderwick and the spreadsheet are both dated and sourced, but the account's own Business-plan price was never in the table, which section 4 records as the gap the win-loss review later found.
- [x] Discount rules exist, with named approvers, before the first negotiation. Section 5's table predates phase 1 by six days, with Ruth Adeyemi and Isabel Ferreira named.
- [ ] One owner is named who can approve changes, and a review date is on a calendar. Isabel Ferreira is named; the next review date is Open, pending EXP-2's kill-or-ship date of 2027-02-12.

Signed: Isabel Ferreira, Chief Product Officer, 2026-11-03. Reopened 2026-12-21 per D6; not re-signed as of the growth plan's date, 2026-12-22. Open: Isabel Ferreira owns the re-sign, once EXP-2 either ships a usage price or is killed.
