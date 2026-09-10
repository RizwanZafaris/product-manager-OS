# Positioning: Expense Copilot

Fills [templates/planning/positioning.md](../templates/planning/positioning.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count and dollar figure is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so it can be checked against the documents this positioning feeds. See the [examples index](README.md).

**Owner:** Tomas Lindqvist, head of product marketing · **Date:** 2026-10-30 · **Status:** Signed at PLANNING; feeds the GTM plan and the pricing and packaging document · **Segment this positions for:** S-5, Business-plan accounts with first-submission approval under 75% and five or more filers (N36)

## 1. Competitive alternatives

Isabel Ferreira's D1 on 2026-10-15 set the rule this section follows: the add-on pass reuses internal evidence only where a written reason says it transfers, so none of the rows below are Ledgerline's own numbers. They come from the commercial evidence gathered 2026-10-15 to 2026-10-28: six design-partner interviews (EV-C01 to EV-C06), the platform data pull of 2026-10-22 (EV-C07), the Q3 win-loss batch (EV-C08), and the Q3 support-ticket pull (EV-C09). All figures ILLUSTRATIVE.

| Alternative (what they actually do) | Why it is good enough today | Evidence |
|---|---|---|
| Type receipt data straight into the Expenses form, no draft | Free, already how every account files, and it is not catastrophically bad: S-1's own median first-submission approval sits at 66% (N35), and the design partners' own Q3 baseline was 64% (N44) before any product touched it | Platform data pull, EV-C07 (N32, N33, N35); support tickets tagged category or receipt, EV-C09 (N38, 610 in Q3, showing where the mechanical cost lands, not that the workaround has failed) |
| Keep a shared spreadsheet alongside or instead of the form | Free, familiar, and gives a finance lead a shape the Expenses form does not: four of six interviewed design partners run one today | Design-partner interviews, EV-C01 to EV-C06 (N40) |
| Buy Cinderwick, a seat-priced receipt-capture vendor | Already does the extraction the copilot does, and is a known quantity to a buyer who has shopped this category before; two of six interviewed partners had already trialled it | Design-partner interviews, EV-C01 to EV-C06 (N40); Cinderwick's quote, $8 per seat per month for 900 seats, quoted 2026-08-13 (N13); Q3 win-loss batch, EV-C08 (N37: 9 of 31 lost deals named receipt capture, 7 of those 9 chose Cinderwick) |

## 2. Unique attributes

| Attribute | Which alternatives lack it |
|---|---|
| Drafts the line item, with matched receipt and category, inside the same Expenses workflow the account already approves reports through | Typing (no draft exists at all); Cinderwick (a separate product with its own login; the result still has to be moved back into the Expenses form before a reviewer can approve it) |
| Matches drafted fields to the account's own written policy, not a generic category list | Typing (the filer has to already know the policy); the spreadsheet (no policy engine, categories are whatever the sheet's owner typed) |
| Activates on the Business plan the account already runs and bills on that same account, no new vendor contract, no separate security review to open | Cinderwick (a new vendor: its own contract, its own onboarding, its own pass through procurement) |

## 3. Value, with proof

All figures ILLUSTRATIVE; none of the claims below are proven at a customer account as of this signing.

| Attribute | Value it enables | Proof (or "unproven") |
|---|---|---|
| Drafts inside the existing workflow | The filer stops re-typing what the receipt already says | Unproven at a customer account. Five of six interviewed design partners said they would pay "something" for this, but zero of six were asked a price (N40); phase 1 with the six design partners, beginning 2026-11-10, is the test, not this document |
| Matches drafted fields to the account's own policy | Fewer bounces, so the reviewer stops re-checking what the filer was already told | Unproven at a customer account. The number any improvement will be judged against is written down now: S-1's 66% median and the design partners' own 64% (N35, N44), not a number this document invents |
| Activates on the existing account, no new vendor | The buyer skips a second contract and a second security pass to open a second vendor | Unproven as a universal driver. Two of six interviewed partners had already tried and dropped Cinderwick (N40), which shows the second-vendor cost is real for at least some buyers, not that it decides every deal |

## 4. Customers who care most

- **Best-fit segment:** S-5, the 1,240 Business-plan accounts with first-submission approval under 75% and five or more filers (N36), drawn from the 2,900 Business accounts active in Expenses with ten or more reports last quarter (S-1, N32).
- **What marks them out:** a median of 34 plan seats and 11 filers per account across S-1 (N34), filing a median of 33 reports a quarter, about 11 a month (N33). Large enough that a bounce is not one person's Friday-afternoon problem, small enough that most have not already bought a dedicated tool. The [B2B SaaS card](../knowledge/domains/saas-b2b.md) names the user, the buyer and the blocker as usually three different people: here the user is the filer who bounces and the reviewer who catches it, the buyer is the account admin with billing authority on the Business plan, and the blocker is whoever at the account signs off a new flow of receipt images through a third-party model, a role that is real even at this scale even though it is lighter than the Enterprise DPA review the wider journey ran into. The six design partners recruited to test this positioning span this same range, from Oakhurst Dental Partners at 22 seats and 6 filers to Tessellate Consulting at 60 seats and 44 filers, 228 seats in total (N41).
- **Why the value is urgent for them:** this is where deals are being lost today, not a hypothetical. Nine of 31 lost Q3 Business-plan deals named receipt capture as the primary reason, and seven of those nine chose Cinderwick (N37); the account logged 610 support tickets tagged category or receipt in the same quarter (N38, EV-C09).

## 5. Market category

All figures ILLUSTRATIVE.

| Field | Answer |
|---|---|
| Category we position in | An add-on to the finance platform the account already runs, not a stand-alone receipt-capture product and not a general AI assistant |
| What this category makes them assume | Three things, before we say a word: the price is a small fraction of what the account already pays for the plan; it is billed on whatever unit that plan already uses to size the account (seats, since Business accounts already carry a seat count, N34); and it works inside the same login and the same approval flow, with no new vendor to onboard |
| Assumptions we do not meet, and how we handle that | We do not yet know the exact number the pricing document will set. Open: Isabel Ferreira and the pricing document own that number (P4). What we can already check: against a $149 monthly plan, even a modest per-seat number adds up fast for the median 34-seat account (N34); at the vendor's own anchor of $8 a seat (N13), that account's bill would be $272, already above the plan itself. This is the exact case this section exists to flag before a price ships: the pricing document later set $6 a seat, and the median account's bill came to $204 a month, one and a third times the $149 plan (N47). Whatever unit and number pricing chooses, it has to clear this bar or it breaks the promise written down in this row |
| Frames considered and rejected | Free feature bundled into the Business plan, argued twice, by sales in this positioning session and again at the pricing review: rejected (D2). The [AI products card](../knowledge/domains/ai-products.md) is why: model calls are cost of goods sold here, not a rounding error, so Daniel Okafor's rule is that no feature costing more than one point of Business-plan gross margin ships without its own revenue line; a free bundle at the business case's own 60% adoption assumption costs about $212,000 a year in model calls, about 1.9 points of Business-plan gross margin (N51), and a free feature cannot be positioned against a vendor charging $8 a seat (N13), because it announces the value is zero. Stand-alone receipt-capture tool, competing directly with Cinderwick on its own category: rejected, because it inherits Cinderwick's buyer expectations, a dedicated vendor with its own contract, exactly where section 2's third attribute stops applying. General "AI assistant" category: rejected, because it invites comparison to every other AI feature on the market instead of to what the reviewer actually does today, abandoning the alternative-first method D1 committed to |

## Exit gate

This positioning is fit to build messaging on when:

- [x] Section 1 names what customers actually do today, evidence-linked, not the battle-card logo. Typing, a spreadsheet and Cinderwick, each tied to EV-C01 through EV-C09
- [x] Every attribute in section 2 is absent from at least one listed alternative
- [x] Every value claim carries proof or is marked unproven. All three rows in section 3 are marked unproven, honestly, because phase 1 had not run at signing
- [x] The best-fit segment is described precisely enough to build a list. S-5 is a filterable query: approval under 75%, five or more filers, on the Business plan (N36)
- [x] The category was chosen after sections 1 to 4, and its silent promises are written down. Section 5's second row is that promise, and section 5's third row shows it was correct
- [x] The GTM plan's positioning skeleton can be filled from this file with no new inventions

Signed: Tomas Lindqvist, head of product marketing, 2026-10-30
