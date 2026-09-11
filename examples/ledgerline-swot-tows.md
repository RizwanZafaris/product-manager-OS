# SWOT and TOWS: Ledgerline Expense Copilot

Fills [frameworks/strategy/swot-tows.md](../frameworks/strategy/swot-tows.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, Cinderwick, the people, the evidence and every figure are fiction built for this worksheet. See the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md).

**Owner:** Maya Chen, Product Manager · **With:** Tomas Lindqvist, Head of Product Marketing · **Date:** 2026-10-19 · **Status:** First commercial-pass facts, before positioning or diagnosis

## What it is for

This page sorts the known facts for the Ledgerline product add-on against Cinderwick before positioning work begins. Strengths and weaknesses are relative to Cinderwick or to the current customer process. Opportunities and threats are external and dated.

The evidence is taken from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md). The first pass produced four owned moves. The period cut keeps the three moves with the clearest commercial consequence first, while the volume re-quote remains an owned dependency.

## Run it when

- The commercial pass needs one page of facts before positioning and diagnosis.
- A competitor is named as the reason for a lost deal.
- A strength needs a comparator and evidence before it can influence strategy.
- A known weakness needs a TOWS response rather than a description.

**Skip it when:** the strategy already has a diagnosis with evidence. This worksheet is the pre-diagnosis sorting pass dated 2026-10-19.

## Inputs you need first

- The Cinderwick comparator: $8 per seat per month, quoted 2026-08-13 for 900 seats (N13).
- Ledgerline platform and customer evidence: 6,400 Business-plan accounts (N26), the Q3 lost-deal batch (N37), customer support tickets (N38), and the six design-partner interviews (N40).
- Product and delivery risks: foreign-language extraction risk R3, the customer DPA subprocessor gap R4, the model API quote of $0.22 per receipt (N9), and the dependency records for the subprocessor addendum and volume re-quote.
- Capacity facts for the owners: Maya Chen, Tomas Lindqvist, the legal lead, and Daniel Okafor with procurement.

## The worksheet

### Part 1: SWOT, with rules

#### Strengths

| ID | Strength (internal, relative to Cinderwick) | Evidence | Rank |
|---|---|---|---|
| SWOT-S1 | Ledgerline already operates the Expenses platform used by 6,400 Business-plan accounts, so the add-on can sit inside the account's existing workflow rather than requiring a separate receipt-capture vendor relationship. Cinderwick is the separate seat-priced comparator. | N26, N13; [journey data sheet](ledgerline-journey.md) | 1 |
| SWOT-S2 | Ledgerline has direct discovery access to the buyer problem: all 6 of 6 finance leads named bounces, 4 of 6 keep a spreadsheet, 2 had trialled Cinderwick, and 5 of 6 would pay "something". | N40, EV-C01 to EV-C06; [journey data sheet](ledgerline-journey.md) | 2 |

#### Weaknesses

| ID | Weakness (internal, relative to Cinderwick) | Evidence | Rank |
|---|---|---|---|
| SWOT-W1 | Foreign-language receipt extraction is unproven for the Ledgerline add-on, so the product cannot yet claim parity across the customer receipt mix. This is R3. | R3; N40 records that 2 of 6 design partners had trialled Cinderwick, but does not establish Ledgerline extraction quality; [journey data sheet](ledgerline-journey.md) | 1 |
| SWOT-W2 | Customer-scale model cost is exposed to a quoted, not contracted, receipt rate, while the commercial offer would need a dependable margin case. | N9, DEP2; [journey data sheet](ledgerline-journey.md) | 2 |
| SWOT-W3 | The customer Data Processing Agreement does not name the model vendor as a subprocessor, so customer data cannot flow until an addendum is signed, which threatens to block the Enterprise pipeline. | Raised in this session as DEP3, needed by 2026-11-06; [journey data sheet](ledgerline-journey.md) | 3 |

#### Opportunities

| ID | Opportunity (external, horizon in quarters) | Evidence | Rank |
|---|---|---|---|
| SWOT-O1 | Receipt capture is an active buying problem in the near commercial horizon: 9 of 31 lost Business-plan deals named it as the primary reason, and 7 of those 9 chose Cinderwick. | N37, Q4 2026 horizon; [journey data sheet](ledgerline-journey.md) | 1 |
| SWOT-O2 | The existing Expenses customer base contains a reachable problem pool, with 2,900 Business accounts active in Expenses and 610 Q3 support tickets tagged category or receipt. | N32, N38, Q4 2026 to Q1 2027 horizon; [journey data sheet](ledgerline-journey.md) | 2 |

#### Threats

| ID | Threat (external, horizon in quarters) | Evidence | Rank |
|---|---|---|---|
| SWOT-T1 | Cinderwick can present a simple, comparable seat price of $8 per seat per month to accounts already considering receipt capture. | N13, Q4 2026 to Q1 2027 horizon; [journey data sheet](ledgerline-journey.md) | 1 |
| SWOT-T2 | The model supplier's quoted rate may not hold at customer scale, creating a cost threat before a volume re-quote is secured. | N9 is quoted, not contracted; DEP2 and R6; [journey data sheet](ledgerline-journey.md) | 2 |

### Part 2: TOWS, the moves

| Cell | Move | Internal ID | External ID | Owner | Feeds |
|---|---|---|---|---|---|
| SO: strength takes opportunity | Position the copilot as an add-on inside the platform the account already runs, using Ledgerline's existing Expenses workflow and customer access to address the receipt-capture demand. | SWOT-S1 | SWOT-O1 | Tomas Lindqvist | D1 |
| WO: fix weakness to take opportunity | Close the customer DPA subprocessor addendum before customer data flows, so the commercial opportunity is not blocked by the customer-tenancy trust gap. Raise it as DEP3, needed by 2026-11-06. | SWOT-W3 | SWOT-O1 | the legal lead | DEP3, D1 |
| ST: strength blunts threat | Price the add-on under Cinderwick's $8 per seat per month while using the Ledgerline platform relationship as the distribution advantage. | SWOT-S1 | SWOT-T1 | Isabel Ferreira | D1 |
| WT: shrink weakness a threat would exploit | Get a model-vendor volume re-quote before customer scale, so the quoted $0.22 per receipt does not become an avoidable margin exposure. Raise it as DEP2. | SWOT-W2 | SWOT-T2 | Daniel Okafor with procurement | DEP2, D1 |

**Decision rule applied.** Each row has exactly one internal ID and one external ID. All four moves have owners. The first three are the period cut, ranked by the nearest commercial horizon. The fourth remains an owned dependency because its evidence and action are required before scale. The Weaknesses box carries a third row, SWOT-W3, past this pass's two-row starting point and still under the framework's four-row cap, because the WO move needed a weakness that actually describes the DPA subprocessor gap it closes, rather than borrowing the unrelated foreign-language extraction weakness.

The only un-moved product-quality issue is the foreign-language extraction risk within SWOT-W1. It is carried as R3, owned by Priya Nair, rather than being represented as a new move on this first page.

## Reading the result

- **The four moves are owned.** The SO move becomes the commercial frame, the WO move becomes DEP3, the ST move becomes the price comparison, and the WT move becomes DEP2.
- **The first three period moves are SO, WO and ST.** The team is not treating Cinderwick only as a pricing problem. The subprocessor addendum is a prerequisite to customer data flow, and the volume re-quote is a prerequisite to scale.
- **The strongest internal advantage is access to the existing platform and customer workflow, not an unqualified extraction claim.** The foreign-language gap remains R3.
- **The opportunity has evidence but not willingness-to-pay evidence.** N40 records that 5 of 6 would pay "something", while 0 of 6 were asked a price. That finding is not converted into a price claim.
- **The comparator is explicit.** Cinderwick is quoted at $8 per seat per month. Ledgerline's later positioning and pricing work must test whether the add-on can win against that alternative without confusing platform access with customer value.

## ILLUSTRATIVE example

This is the Ledgerline commercial pass itself, not a reusable benchmark. The four TOWS moves are:

1. Use the existing Ledgerline platform to address the receipt-capture opportunity.
2. Close the customer DPA subprocessor addendum before data flows.
3. Price below Cinderwick's quoted $8 per seat per month.
4. Secure a volume re-quote before customer-scale usage.

The source record for these four decisions is LC7 in the [coverage sheet](ledgerline-coverage-sheet.md).

## The trap

The trap here would be writing "strong product" or "strong team" without naming the comparator. The useful strength is narrower: Ledgerline already operates the platform for 6,400 Business-plan accounts, while Cinderwick is a separate seat-priced vendor. The useful weakness is also narrower: foreign-language extraction is unproven and the model rate is quoted, not contracted.

The framework caps each box at four rows; this first pass started at two rows per box, with one named exception: the Weaknesses box carries a third row, SWOT-W3, because the WO move's content (the DPA subprocessor gap) needed its own weakness rather than being tagged onto SWOT-W1's unrelated foreign-language extraction gap. A row without evidence or without a TOWS pairing is not promoted into the strategy.

## Feeds

- [Product strategy](../templates/planning/product-strategy.md): situation facts and sequencing.
- [Risk register](../templates/execution/risk-register.md): R3 and any later threat that remains without a response.
- [Roadmap](../templates/planning/roadmap.md): the three period moves in the Next column.
- [ledgerline-journey.md](ledgerline-journey.md): canonical facts, identifiers and later dependency status.
- [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md): LC7, the recorded SWOT and TOWS decisions.
- PLANNING track, Gate 1, before positioning and diagnosis work.
