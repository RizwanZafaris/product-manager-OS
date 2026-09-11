---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["marketplace", "marketplaces", "two-sided", "platform marketplace"]
---
# Marketplaces

The distinctive fact is that you have two sets of users with opposed interests and you cannot make either happy alone. A feature that helps buyers usually costs sellers something, and the marketplace works only at the point where both sides keep showing up. The second distinctive fact is that the number everyone quotes is not the business: gross merchandise value is what flows through you, and revenue is the fraction you keep, so a marketplace can grow the headline while the company gets worse. The third is that your product's success creates its own predator, because a buyer and a seller who meet on your platform have a standing incentive to transact off it, and the better you match them the stronger that incentive becomes.

**Adjacent industries:** home-services and on-demand care platforms (cleaners, trades, sitters for children or pets) read this card, with safety and liability added because the provider enters the customer's home or looks after a dependant. Background checks are a launch gate, run in the US through the FCRA's consent and adverse-action flow, and trade-licence and insurance verification are listing requirements, not trust badges. How the platform answers for in-home damage or injury shapes the guarantee and the take rate that funds it. Worker-classification risk grows with how much the platform controls price and dispatch; the fuller treatment is in [Food delivery and quick commerce](food-delivery-quick-commerce.md). Disintermediation is at its extreme here, because a customer who liked the first visit books the second directly. Field-service software sold to the trades themselves reads [B2B SaaS](saas-b2b.md). As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Which side is constrained? Almost always one is hard to get and the other follows. Spending on the easy side is the most common and most expensive mistake in this domain, and it looks like growth while it is happening.
2. What is liquidity here, stated as a probability with a window: the chance that a listing transacts, or that a search ends in a transaction, within a defined period? Aggregate liquidity hides the listings that never received a view, and those sellers churn first.
3. What is the smallest self-sustaining unit, by geography, category or time? A marketplace that is liquid in one city and thin everywhere else is a real business; one that is uniformly thin everywhere is not, and the averages look similar.
4. What is the take rate, and where does it start driving people off the platform? Category benchmarks vary widely, and a rate at the top of the range in a market with low switching costs funds a competitor made of your own users.
5. What prevents disintermediation once a match is made, and is it a value you provide or a rule you impose? Rules leak. Payments, guarantees, dispute resolution and recourse are the retention mechanisms that survive contact with two motivated parties.
6. Who is liable when the transaction goes wrong, and does the product's design match that answer? The more you curate, rank and guarantee, the less you look like a neutral conduit.
7. What is the trust and safety response time, and who pays for it? Fraud, counterfeits and disputes are a permanent cost of goods sold in this domain, not a launch phase.
8. What does the cold start look like in a new segment, and are you willing to fake or subsidise one side to get there?

## Gatekeepers

- **The constrained side, collectively.** Not a formal gatekeeper and the one that decides your fate. Suppliers who stop listing remove liquidity immediately, and the damage is not reversible by acquiring more of them.
- **Payments and financial partners.** Acquirers, processors and, where you hold funds between parties, financial regulation. Splitting a payment between platform and seller changes what you are legally doing with money. See [fintech](fintech.md), which routes to the regulated module.
- **Platform regulation, where you are large or consumer-facing.** Obligations around trader traceability, notice and action on illegal listings, transparency of ranking, and dispute handling turn moderation and search from product choices into documented duties.
- **Trust and safety, internally.** Owns the standard that decides what may be listed. A growth feature that increases fraud exposure will be stopped here, and should be.
- **App stores, where the marketplace is mobile.** Control distribution and, for digital goods, take their own share of the transaction you thought was yours.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Gross merchandise value | Scale of activity flowing through the platform | It is not revenue and is commonly presented as though it were. It rises with subsidy, promotion and low-quality volume, all of which cost you money |
| Take rate | The share you keep | The listed rate is not the effective rate. Discounts, refunds, disputes and incentives sit between them, and the gap is where the margin went |
| Liquidity | Probability that supply transacts, or that a search succeeds | Reported in aggregate it averages a liquid core with a dead tail. The tail is the churn you will see next quarter |
| Take rate pushed too high | Short-term margin | Above the range a category tolerates it funds disintermediation. The metric improves right up until the supply leaves |
| Buyers and sellers acquired | Growth | Blending the two hides which side you actually bought, and the constrained side is the only one that mattered |
| Repeat transaction rate | Stickiness | Strong signal, but concentrated repeats between the same pair are often a relationship that is about to move off-platform |
| Time to first transaction for a new listing | Whether new supply is discoverable | The median flatters. Read the long tail, because listings that never transact are sellers who are leaving |
| Dispute and refund rate | Trust health | Falls when disputes become hard to file. Read it beside resolution time and outcome, or it measures friction rather than safety |
| Match rate | Efficiency of matching | Depends entirely on what counts as a match. Counting an inquiry rather than a completed transaction turns a matching problem into a good number |

## Reading

- **Andreessen Horowitz's marketplace writing on liquidity.** The durable claim is that liquidity, not size, is the best predictor of health: a marketplace with a hundred listings where everything sells is stronger than one with ten thousand where nothing does. Read it for the framing, and note that most published benchmark ranges are vendor-supplied and should be treated as orientation rather than targets.
- **Andrew Chen, The Cold Start Problem** (2021). The atomic network idea is the useful part: find the smallest unit that can sustain itself, saturate it, then replicate. It is the most common failure to launch a marketplace nationally and be thin everywhere.
- **Any marketplace's own trust and safety transparency reporting.** Read one from a platform in your category. It tells you the real shape of the cost you are taking on, which is almost never in the business case.

**Conductor overlay:** this domain sharpens DISCOVER-1 (there are two personas with opposed interests and both need naming), DISCOVER-4 (the problem must be stated for the constrained side first), DEFINE-6 (out of scope: scope decisions favour one side, so the trade goes on the written exclusion list the sponsor acknowledges rather than being discovered later), and OPERATE-2 (liquidity by segment is the metric tree's root, and gross merchandise value belongs underneath it rather than at the top).

**Templates this bends:** [north-star-metric](../../templates/planning/north-star-metric.md) (liquidity rather than volume, or the tree optimises the wrong thing from the start), [personas](../../templates/discovery/personas.md) (at least two, and the constrained side gets the deeper treatment), [pricing-packaging](../../templates/planning/pricing-packaging.md) (the take rate is the price, and its ceiling is set by disintermediation risk rather than by willingness to pay), and [business-case](../../templates/planning/business-case.md) (trust and safety is a permanent line item, not a launch cost).

**Filled in this repo:** [domain-marketplaces-north-star-metric.md](../../examples/domain-marketplaces-north-star-metric.md) fills the [north-star-metric](../../templates/planning/north-star-metric.md) template directly for this domain: a liquidity north star, a guardrail pair (gross margin per subsidy pound, provider earnings per hour), and the two-sided input-metric tree this card asks for. For the other bent templates, [sahulat-personas.md](../../examples/sahulat-personas.md) fills the personas template; useful for format, though it writes one wallet-holder persona rather than the two opposed-interest sides this card asks for. [ledgerline-pricing-packaging.md](../../examples/ledgerline-pricing-packaging.md) fills pricing-packaging; read it for how a pricing table cites the evidence behind each tier, though its number is a SaaS seat price, not a take rate with a disintermediation ceiling. [ledgerline-business-case.md](../../examples/ledgerline-business-case.md) fills business-case; useful for the sourced-arithmetic format, though its costs are engineering hours, not a standing trust-and-safety line.

**Worked example (ILLUSTRATIVE):** an input-metric-tree row (fills [north-star-metric](../../templates/planning/north-star-metric.md) section 2) for a two-sided services marketplace:

| Input metric | Causal claim | Owner | Current | Target |
|---|---|---|---|---|
| Liquidity: share of active listings that transact within 14 days | A listing that transacts is a supplier who gets paid and stays; liquidity is what keeps the constrained side, suppliers, from leaving, which is the precondition the GMV number assumes and never states | Head of Supply | 34% | 45% |

The card's rule that GMV is not the business is why this row, not a GMV row, sits in the tree: GMV can rise on subsidy and promotion while liquidity, the probability a listing actually transacts, falls, and the tree is built so that failure shows up here first.
