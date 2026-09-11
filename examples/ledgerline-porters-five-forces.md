# Porter's five forces: Ledgerline Expense Copilot

Fills [frameworks/strategy/porters-five-forces.md](../frameworks/strategy/porters-five-forces.md).

Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, customers, vendor, scores and figures are fiction built to demonstrate the worksheet. No figure is a benchmark, a target to copy, or a claim about any real market.

**Owner:** Maya Chen, Product Manager · **Scored with:** Tomas Lindqvist, Head of Product Marketing · **Date:** 2026-10-27 · **Segment:** S-1 buying receipt capture

## What it is for

This sheet scores the five forces for segment S-1, Business accounts active in Expenses with 10 or more reports last quarter. S-1 contains 2,900 accounts with 10 or more reports in Q3, and the customer approval baseline is 66% median first-submission approval across S-1.

The two strongest forces are substitutes and suppliers. The substitute force points to pricing against the labour hidden by typing and spreadsheets. That implication became the reviewer-cost anchor in EXP-1. The supplier force points to a volume re-quote, DEP2, and to the open risk that model cost exceeds the margin floor, R6.

Evidence is drawn from the [journey data sheet](ledgerline-journey.md) and its [coverage sheet](ledgerline-coverage-sheet.md).

## Run it when

- Before the receipt-capture pricing decision for S-1, to identify what can discount the list price
- When comparing Ledgerline's product with typing, spreadsheets and Cinderwick
- When the model supplier's quoted terms are not yet contracted
- When the roadmap needs a named response to the strongest margin pressures
- On the next strategy review if supplier terms or the competitive win-loss evidence changes

**Skip it when:** no segment has been chosen. This sheet is scored for S-1, not for the software market generally.

## Inputs you need first

- **Segment and job:** S-1, Business accounts active in Expenses, with 10 or more reports last quarter, buying receipt capture. S-1 has 2,900 accounts and a 66% median first-submission approval baseline.
- **Alternatives:** typing into the Expenses workflow and keeping a spreadsheet. Four of six design-partner interviews recorded that the account kept a spreadsheet, and all six named bounces. See LC2.
- **Rival evidence:** the Q3 lost Business-plan batch recorded 31 lost deals, 9 naming receipt capture as the primary reason, and 7 of those 9 choosing Cinderwick. Cinderwick was quoted at $8 per seat per month.
- **Supplier evidence:** one model supplier is represented in the five-forces evidence, and its price is $0.22 per receipt, quoted at about 40,000 receipts a year, not contracted. See N9 and LC8.
- **Buyer evidence:** S-1 is the named segment, but no buyer concentration or switching-cost measurement is recorded in the available data.

## The worksheet

Score 1 to 5 for the pressure the force puts on Ledgerline's margin in S-1: 1 weak, 3 moderate, 5 strong. The scores are estimates recorded in LC8. Arithmetic is shown where the evidence provides a count or derived comparison.

| Force | Driving questions | Score 1 to 5 | Evidence | Implication for pricing | Implication for roadmap | Owner |
|---|---|---:|---|---|---|---|
| Rivalry among existing competitors | How many rivals, how alike, how fast do they match features, do they compete on price | 3 | The Q3 win-loss batch recorded 31 lost Business-plan deals. Receipt capture was the primary reason in 9 of 31 lost deals, and 7 of those 9 chose Cinderwick. Arithmetic: 7 of 9 receipt-capture losses chose Cinderwick. Cinderwick's quote was $8 per seat per month. This is moderate pressure, not a claim that all 31 losses were competitive receipt-capture losses. | Hold the comparison against Cinderwick's quoted $8 per seat per month, while avoiding a price-only position. Reopen the benchmark if later win-loss evidence shows that price parity is the deciding factor. | Preserve the platform-specific policy match and approval-rate experience as the differentiating dimension. Do not use feature breadth alone as the roadmap response. | Tomas Lindqvist |
| Threat of new entrants | What does entry cost, what do incumbents hold that entrants cannot, how fast could a new team ship a credible copy | 3 | The available sheet does not record a quantified entry cost or a dated copy estimate. Ledgerline does hold customer workflow context inside the platform, but no defensible barrier is scored yet. The force is therefore moderate, not low. | Do not price as though receipt capture is rare. Keep the price tied to delivered value and the alternative cost rather than to novelty. | Strengthen the account-specific policy match and the approval-rate evidence. Treat the approval flow as a candidate advantage, not an established switching cost. | Maya Chen |
| Threat of substitutes | What does the customer do instead, what does that cost them, when does it stop being good enough | 4 | Typing and spreadsheets are the observed alternatives. LC2 records that 4 of 6 interviews kept a spreadsheet, and all 6 named bounces. S-1's customer approval baseline is 66% median first-submission approval. The spreadsheet's labour cost is hidden rather than priced as a software invoice. | Price against the labour the spreadsheet hides, including reviewer effort, rather than against spreadsheet licence cost. This implication originated the EXP-1 reviewer-cost anchor, which used N7's 30 reviewer-hours a month across three reviewers at $60 an hour. | Beat typing and spreadsheets on the job, first-submission approval and reduced re-checking, not on feature count. Carry the reviewer-cost anchor into the experiment record, while testing whether the buyer's labour context transfers from Ledgerline's internal case. | Maya Chen |
| Bargaining power of buyers | How concentrated are buyers, how low are their switching costs, can they build it themselves, do they see prices transparently | 3 | Buyer concentration is not measured in the available evidence. S-1 contains 2,900 accounts, but that count does not establish concentration or switching cost. Buyers can compare the product with typing, spreadsheets and the quoted Cinderwick offer. The absence of concentration evidence supports a moderate score, not a weak score. | Expect comparison and discount pressure. Keep the value story explicit and avoid treating the $8 Cinderwick quote as proof that every buyer will pay a similar amount. | Make activation, policy matching and approval-rate evidence useful inside the account. Deepen the workflow integration before relying on switching costs. | Maya Chen |
| Bargaining power of suppliers | How many suppliers per component, what does switching cost, can a supplier move into our product | 4 | The five-forces evidence identifies one model vendor, and N9 records $0.22 per receipt, quoted at about 40,000 receipts a year, quoted, not contracted. The customer-scale volume re-quote is DEP2. R6 records the risk that model cost per drafted report exceeds the margin floor once volume moves off the quote. Arithmetic for the current quoted report cost: 4.2 receipts per report x $0.22 per receipt = $0.92 per drafted report, N11. | Obtain the DEP2 volume re-quote before scale. Protect the margin calculation from a supplier price change, and do not make a free bundle decision that assumes the quoted rate remains available. | Abstract the model supplier behind an interface and keep the cost and usage boundary visible. Resolve DEP2 and monitor R6, with a second supplier path considered if the quote threatens the margin floor. | Daniel Okafor with procurement |

**Implication guide, when a force scores 4 or 5.** The substitute response is to price against the substitute's total cost, including the labour it hides, and to beat it on the job rather than on features. The supplier response is to obtain the volume re-quote, DEP2, and manage R6 through supplier abstraction and cost monitoring.

**Decision rule.** Rank the forces by score:

1. Substitutes: 4
2. Suppliers: 4
3. Rivalry: 3
4. Buyer power: 3
5. New entrants: 3

Arithmetic: the top two both score 4, while each remaining force scores 3. The strategy problem is therefore the combined substitute and supplier pressure. The named responses are the EXP-1 reviewer-cost anchor for substitutes, and DEP2 plus R6 for suppliers.

## Reading the result

- **Substitutes lead jointly with suppliers.** Ledgerline must show why receipt capture is worth more than typing or a spreadsheet, including the reviewer labour those alternatives hide.
- **Supplier pressure is material.** The model API price is quoted, not contracted. Procurement owns DEP2, and Daniel Okafor with procurement owns R6.
- **Rivalry is moderate.** Cinderwick won 7 of the 9 Q3 lost deals that named receipt capture, and its quote was $8 per seat per month. Ledgerline cannot assume that a lower price alone creates defensibility.
- **Buyer power is not fully evidenced.** The 2,900-account S-1 population does not provide a buyer concentration measure, so this score should not be read as proof of low buyer power.
- **New entrants are not yet a defensibility finding.** The evidence does not quantify entry cost or copy speed. The account-specific policy context and approval flow remain candidate barriers.

## ILLUSTRATIVE example

This filled worksheet scores Ledgerline's product for S-1 buying receipt capture on 2026-10-27. The scores are estimates from LC8.

The arithmetic behind the leading forces is:

- **Substitute evidence:** 4 of 6 interviews kept a spreadsheet, and 6 of 6 named bounces, as recorded in LC2.
- **Supplier evidence:** the model price is $0.22 per receipt, quoted at about 40,000 receipts a year, not contracted, as recorded in N9.
- **Rivalry evidence:** 7 of 9 lost deals that named receipt capture chose Cinderwick. Cinderwick's quote was $8 per seat per month.
- **Model cost implication:** 4.2 receipts per report x $0.22 per receipt = $0.92 per drafted report, the derived estimate in N11.
- **Rank arithmetic:** substitutes 4 and suppliers 4 are above rivalry 3, buyer power 3 and new entrants 3.

Top two: substitutes and suppliers. The substitute implication became the reviewer-cost anchor in EXP-1. The supplier implication became DEP2 and R6. The result is an unattractive margin position for a product that has neither supplier leverage nor a proven barrier yet, but it gives the roadmap and pricing work two specific responses rather than a general warning.

## The trap

Scoring the industry instead of S-1 would hide the actual alternatives. The relevant substitute is not an abstract software category. It is the customer's existing typing workflow and spreadsheet, which 4 of 6 interviewed design partners kept, while all 6 named bounces.

The other trap is treating a quoted model price as a contract. N9 is $0.22 per receipt, quoted at about 40,000 receipts a year, not contracted. At 4.2 receipts per report, the arithmetic is $0.92 per drafted report, but R6 remains open because the customer-scale price may change. DEP2 is therefore a strategy response, not an administrative detail.

The rivalry evidence also needs careful handling. Cinderwick was chosen in 7 of the 9 lost deals that named receipt capture, not in all 31 lost Business-plan deals. The score uses the receipt-capture evidence and does not turn it into a claim about the entire Business-plan market.

## Feeds

- [Competitive analysis](../templates/discovery/competitive-analysis.md): sections 5 and 6, to test the Cinderwick comparison and the spreadsheet alternative
- [Pricing and packaging](../templates/planning/pricing-packaging.md): the competitive benchmark and the price decision that used the reviewer-cost anchor
- [Product strategy](../templates/planning/product-strategy.md): diagnosis and key risks, including supplier dependency
- [Business case](../templates/planning/business-case.md): model cost and market-attractiveness reasoning
- [Risk register](../templates/execution/risk-register.md): R6 and the supplier response
- PLANNING track and DISCOVER, ahead of Gate 1
- Method background: the worksheet is based on Michael E. Porter's ideas from "How Competitive Forces Shape Strategy", Harvard Business Review (1979), explained in this repository's own words
- Source data: [ledgerline-journey.md](ledgerline-journey.md) and [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)
