# Playing to Win cascade: Ledgerline Expense Copilot

Fills [frameworks/strategy/playing-to-win.md](../frameworks/strategy/playing-to-win.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, and every count, price, date and decision are fiction. See the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Isabel Ferreira, Chief Product Officer · **With:** Maya Chen, Product Manager · **Date:** 2026-11-02 · **Status:** Option A funded conditionally; Option B rejected; amended 2026-12-21 to record the EXP-1 outcome and the DEP1 sequencing exception

## What it is for

This cascade compared the two options still argued for the Ledgerline product's commercial pass:

- **Option A:** a paid add-on for the best-fit segment, S-5.
- **Option B:** free inside the Business plan.

The cascade was run between positioning and pricing. Ruth Adeyemi wrote the conditions for A because she argued for the option least; Daniel Okafor wrote the conditions for B because he argued for the option least.

Option B died when its company condition was known false: the free bundle would cost about 1.9 points of Business-plan gross margin at the 60% drafted-share assumption, against Daniel Okafor's rule that no feature costing more than one point ships without its own revenue line.

Option A survived with its lowest-confidence condition named explicitly: buyers must pay a monthly price in the plan's own unit. EXP-1 was selected to test that condition. The sheet also records the breach in sequencing: seat-metering build money moved before EXP-1 ran. DEP1 delivered on 2026-11-19, with N86 recording 1.5 person-months and $15,000 at N12. EXP-1 was analysed on 2026-12-18.

**Amendment, 2026-12-21.** The sections below that describe DEP1's delivery, EXP-1's exposure and conversion numbers, the KILL decision, and D6's ratification were added at this amendment to fold the outcome into the record the Gate 1 sign-off already carried forward; they postdate the 2026-11-02 sign-off and are not being presented as known at that date.

## Run it when

- Two credible commercial options remain on the table and the team needs a choice rather than an average
- A paid add-on must be compared with a free bundle
- The team needs to identify the condition most likely to kill the leading option
- A capability or billing dependency could turn a strategy into an unfunded wish

## Inputs you need first

- The positioning work for the Ledgerline product
- The S-5 segment definition: 1,240 Business accounts with approval under 75% and 5 or more filers
- The Business-plan margin rule and the free-bundle arithmetic
- The capability and billing dependencies for the paid add-on
- The condition set in LC10 of the [coverage sheet](ledgerline-coverage-sheet.md)
- The relevant pricing and experiment identifiers: D2, D3, DEP1, EXP-1 and N86

## The worksheet

### Part 1: the cascade, per option

| Choice | Option A: paid add-on for S-5 | Option B: free inside the Business plan | What each refuses |
|---|---|---|---|
| Winning aspiration (what winning looks like for the user, not a number) | Finance teams in S-5 get drafted reports matched to their own policies, with less reviewer re-checking and a clearer first-submission path | Business-plan accounts get receipt drafting without a separate purchase, so the capability is available inside the platform they already run | A refuses to make the copilot universally free or available to every plan. B refuses a separate revenue line and a paid add-on choice for the Business plan |
| Where to play (user, scope, geography, channel) | Business accounts active in Expenses, specifically S-5 accounts with approval under 75% and 5 or more filers; customer filers, reviewers and account admins; in-app offer and the existing Ledgerline platform | All Business-plan accounts, including accounts outside S-5; customer filers and reviewers; the existing Business-plan product and its current distribution | A refuses Starter accounts, Enterprise accounts outside S-6, and a universal Business-plan launch. B refuses S-5-only targeting and an in-app paid offer |
| How to win (why the chosen user picks this over the alternative) | A paid add-on keeps the account's own policy line beside the draft and gives the buyer a focused way to improve the review workflow, instead of typing, using a spreadsheet or buying Cinderwick | Convenience and breadth: the feature is already included in the Business plan, so the buyer does not need another purchase or vendor relationship | A refuses to win through free inclusion. B refuses a paid value exchange and the comparison against Cinderwick's $8 per seat per month |
| Capabilities required (three to five things we must do better than the alternative) | Draft from customer receipts; match the account's own policy; expose confidence and approval outcomes to the reviewer; meter and charge the plan's unit; reach account admins through the in-app offer | Operate the drafting workflow at Business-plan scale; absorb model cost within the Business-plan margin; distribute the feature to all Business accounts; support the same customer-policy and approval workflow without a separate revenue line | A refuses scale before the S-5 learning is proven and refuses a billing model unrelated to the plan's unit. B refuses metered customer payment as the capability that funds model cost |
| Management systems (measures, rituals, and structures that keep the capabilities sharp) | EXP-1 tests the plan-unit price condition; DEP1 tracks billing readiness; phase 1 exit checks transfer of drafting quality to customer policies; the pricing and metrics reviews use D3, M-002, M-006, M-007, M-008 and M-009; D2 provides the margin constraint | Finance reviews model cost against Business-plan gross margin; D2 governs the one-point rule; any free-bundle proposal must show its own revenue line or be rejected | A refuses a free bundle without a separate revenue line. B refuses the experiment-led paid packaging and the associated price test |

**Coherence check:** Option A's where-to-play is S-5, and its how-to-win is the policy-matched draft delivered as a paid add-on inside the existing platform. Its billing and customer-policy capabilities have dependencies, named tests or phase exits. Option B's where-to-play is every Business-plan account, while its how-to-win is inclusion at no extra charge. Its model-cost condition fails the stated margin rule, so the cascade does not treat it as a survivor.

### Part 2: what would have to be true

The conditions for A were written by Ruth Adeyemi, who argued for B. The condition for B was written by Daniel Okafor, who argued for A.

| Option | Condition that would have to be true | Category | Confidence (high / med / low) | Cheapest test | Owner | By |
|---|---|---|---|---|---|---|
| A | Buyers pay a monthly price in the plan's own unit | user | low | EXP-1, the per-seat offer test | Maya Chen | 2026-12-18 |
| A | Billing can meter and charge by phase 2 | company | medium | DEP1, seat metering for add-ons in the billing system | Priya Nair with the billing lead | 2026-11-20 |
| A | Drafting quality transfers to customer policies | company | medium | Phase 1 exit with the six design partners | Priya Nair | 2026-11-23 |
| A | Cinderwick does not price under $6 a seat inside two quarters | alternative | medium | Win-loss batch | Tomas Lindqvist with Hana Sato | 2026-12-17 |
| A | The in-app offer reaches account admins | channel | medium | EXP-1 exposure count | Kwame Boateng | 2026-12-04 |
| B | Model cost stays under one point of Business-plan gross margin | company | known false | Free-bundle arithmetic: N51 gives about 1.9 points at the 60% drafted-share assumption, against N50's one-point rule | Daniel Okafor | 2026-11-03 |

**Option B decision arithmetic:**

- Business-plan accounts active in Expenses: 2,900
- Reports per account per year: 11 per month x 12 months = 132
- Annual reports: 2,900 x 132 = 382,800
- At 60% drafted share: 382,800 x 0.60 = 229,680 drafted reports
- Receipts: 229,680 x 4.2 = 964,656 receipts, about 965,000
- Model cost: 964,656 x $0.22 = $212,224.32, about $212,000
- This is about 1.9 points of Business-plan gross margin, against N50's maximum of one point

Therefore, **Option B dies**. D2 was reaffirmed on 2026-11-03.

**Option A decision and sequencing:**

Option A has five written conditions. Its lowest-confidence condition is the user condition that buyers pay in the plan's own unit. EXP-1 was the cheapest named test and was due on 2026-12-18. Under the worksheet's decision rule, that test should have run before build money moved.

That sequence did not hold. DEP1, the seat-metering dependency, delivered on 2026-11-19. N86 records the build at **1.5 person-months x $10,000 per person-month = $15,000**, and records that the work is not reused by the usage model. The sheet records this as a sequencing exception, not as evidence that the condition was proven.

## Reading the result

Option B does not survive because its only written condition is known false: the free bundle's about 1.9 points of Business-plan gross margin exceed N50's one-point rule. D2 records the rejection and was reaffirmed on 2026-11-03.

Option A survives conditionally because every condition has a named test or dependency:

- The lowest-confidence condition is the user condition, tested by EXP-1.
- Billing readiness is tested by DEP1.
- Customer-policy transfer is tested at the phase 1 exit.
- The alternative condition is tested by the win-loss batch.
- Channel reach is tested by the EXP-1 exposure count.

The funding decision is therefore:

1. Reject B under N50 and N51.
2. Fund A conditionally, with EXP-1 as the first commercial test.
3. Do not treat DEP1 as proof that buyers will pay.
4. Carry the $15,000 seat-metering spend as money that moved before the lowest-confidence condition was tested.
5. Reopen packaging if EXP-1 fails its pre-declared rule.

**2026-12-21 amendment: the later result.** It confirms why this condition was ranked first. EXP-1 exposed 2,748 accounts. The control converted 33 of 1,371, or 2.4%. The anchored arm converted 40 of 1,377, or 2.9%. Both arms were under the 4.0% kill line, so EXP-1 was killed on 2026-12-18 under N57 and ratified as D6 on 2026-12-21.

## ILLUSTRATIVE example

This is an invented example for the Ledgerline product. The cascade was run on 2026-11-02 by Isabel Ferreira and Maya Chen.

Option A, the paid add-on for S-5, was selected over Option B, the free Business-plan bundle, only after the conditions were written by the skeptics. Ruth Adeyemi wrote A's conditions. Daniel Okafor wrote B's condition.

A's lowest-confidence condition was:

> Buyers pay a monthly price in the plan's own unit.

The test was EXP-1, due 2026-12-18. The condition was not assumed to be true because the product already worked internally, and it was not treated as proven by the pricing team's preference for seats. The team recorded that DEP1 and N86 moved the seat-metering build ahead of the test, which violated the preferred order of learning before build spend.

B's condition was:

> Model cost stays under one point of Business-plan gross margin.

The arithmetic was:

- 2,900 accounts x 11 reports per month x 12 months = 382,800 reports per year
- 382,800 x 60% drafted share = 229,680 drafted reports
- 229,680 x 4.2 receipts per report = 964,656 receipts, about 965,000
- 964,656 x $0.22 per receipt = $212,224.32, about $212,000
- The result is about 1.9 points of Business-plan gross margin

Because 1.9 points is greater than N50's one-point rule, B died. D2 reaffirmed that result on 2026-11-03.

## The trap

The trap here was treating the billing unit as a capability decision instead of a user condition. Seats were available for billing, so the team accepted D3 even though the value metric did not match the north star. The condition that mattered most was whether buyers would pay in that unit.

A second trap was allowing the build dependency to create commitment before the test ran. DEP1 delivered on 2026-11-19, and N86 records 1.5 person-months and $15,000 spent on seat metering. EXP-1 was not analysed until 2026-12-18. The ledger records the order honestly: the lowest-confidence condition was named, but the build money moved first.

A third trap was writing only the condition that supported the free bundle. Daniel Okafor's margin condition made the rejection testable. Once N51 was compared with N50, B was not kept alive by an unpriced promise of adoption.

## Feeds

- [ledgerline-positioning.md](ledgerline-positioning.md): the paid add-on positioning and the rejected free-feature frame
- [ledgerline-pricing-packaging.md](ledgerline-pricing-packaging.md): D2, D3, the seat price and the later packaging pivot
- [ledgerline-experiment-brief.md](ledgerline-experiment-brief.md): EXP-1's arms, dates and decision rule
- [ledgerline-metrics-review.md](ledgerline-metrics-review.md): the KILL result and D6
- [ledgerline-growth-plan.md](ledgerline-growth-plan.md): the usage re-offer after the seat-price pivot
- [ledgerline-journey.md](ledgerline-journey.md): canonical Ledgerline data sheet, N50, N51, N86, DEP1, D2, D3 and EXP-1
- [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): LC10, the Playing to Win condition record
- Method background: based on A.G. Lafley and Roger L. Martin's *Playing to Win* (2013), explained in this repository's own words

### Exit gate

**Gate 1 walk, signed:** Option B rejected under N50 and N51. Option A funded conditionally with EXP-1 as the lowest-confidence test. The pre-test seat-metering spend is recorded as a sequencing exception: DEP1 delivered on 2026-11-19, and N86 records **1.5 person-months x $10,000 = $15,000** before EXP-1 was analysed. **Signed by Isabel Ferreira, Chief Product Officer, with Maya Chen, Product Manager, on 2026-11-02.**

**2026-12-21 amendment:** EXP-1 was analysed on 2026-12-18 and killed per N57 (both arms under the 4.0% line); the metrics review ratified the pivot as D6 on 2026-12-21. Folded into this record the same day rather than at a new gate attempt, since it confirms the funded option's lowest-confidence test rather than reopening the funding decision itself.
