---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Ecommerce"]
---
# Ecommerce

Selling goods per order means every feature decision lands on a contribution margin waterfall: revenue, minus cost of goods, minus fulfillment and shipping, minus payment costs and returns, minus the marketing that produced the order. A product that grows top-line GMV while the waterfall leaks at returns or last-mile shipping is a product that scales losses. The PM's job in this domain is to know which layer of the waterfall each initiative touches before anyone celebrates a conversion win.

**Adjacent industries:** four neighbours read this card with one change each. Consumer brands selling through retailers (CPG) do not own the customer or the data, so retail-media networks and clean rooms are the channel (see [Marketing and advertising technology](martech-adtech.md)) and trade-promotion spend is the real P&L lever; food and household goods add labelling, recall and traceability duties such as the FDA's FSMA 204 food traceability rule (verify its compliance date). Fashion and beauty add fit and sizing as the returns driver, cosmetics rules that bound claims copy and listings (US MoCRA registration and adverse-event duties, the EU Cosmetics Regulation), and virtual try-on that captures face geometry biometric-privacy law such as Illinois BIPA regulates. B2B and wholesale commerce replaces the funnel with a procurement integration: contract pricing per customer, EDI and punchout into the buyer's system (cXML, OCI), net-terms credit (see [Lending and credit](lending-credit.md)) and approval workflows, because the purchaser is not the user. Age-restricted goods (alcohol, tobacco and vapes, cannabis) need age checks at checkout and again at hand-off, legality that varies by state, the alcohol three-tier system, mandated seed-to-sale tracking for cannabis, shipping limits on vapes (the PACT Act and the USPS mailing ban), and payment access that card networks and banks may refuse while cannabis remains federally illegal in the US. As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Which layer of the contribution margin waterfall does this initiative move, and has finance agreed on that waterfall's definitions? Two teams with two definitions of CM2 will approve opposite roadmaps.
2. Are we the merchant of record or a marketplace broker? The answer decides who owns inventory risk, returns, tax collection, and consumer-protection liability, and it changes almost every template downstream.
3. What does a return actually cost us end to end, and who decided the return policy? Free returns are a conversion feature priced by a different department.
4. Where does demand come from, and what share of it do we rent? A store built on paid acquisition and a marketplace's search ranking has two landlords who can raise the rent in the same quarter.
5. In which states and countries have we crossed an economic nexus threshold? Since South Dakota v. Wayfair (2018), US states can require sales tax collection on volume alone, no warehouse or office needed, and the obligation arrives silently.
6. What happens to the unit economics at the promised delivery speed? Faster promises buy conversion with fulfillment margin, and the trade is rarely priced on the same dashboard.
7. For cross-border orders: who is the importer of record, and are duties shown at checkout or discovered at the door? Surprise duties convert a customer into a chargeback.
8. What breaks at peak? An ecommerce system is sized for its worst November hour, not its average Tuesday.

## Gatekeepers

- **Tax authorities.** Post-Wayfair economic nexus in the US, VAT registration thresholds in the EU and UK, customs regimes for cross-border. They do not review your launch; they audit it later.
- **Payment schemes and processors.** Chargeback ratios carry program thresholds; storing credentials expands PCI-DSS scope; a processor can hold funds or offboard a merchant category with little notice.
- **Consumer-protection regulators.** Distance-selling withdrawal rights in the EU, FTC rules on shipping promises and subscription cancellation in the US, pricing-display rules that vary by market.
- **Marketplaces and channels.** If you sell through Amazon, Google Shopping, or an app store, their listing rules, ranking systems, and fee changes are gate reviews you do not get to attend.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Contribution margin per order (CM1/CM2/CM3) | Whether an order is worth having, layer by layer | Definitions drift between teams; agree the waterfall once, in writing |
| GMV and take rate | Marketplace scale and monetization | GMV counts what flows through, not what you keep; take rate hides subsidy spend |
| Conversion rate by step | Where the funnel leaks | A conversion win from discounting shows up here as pure upside |
| Average order value | Basket economics | Rises when you push bundles that inflate returns |
| Return rate by category | Real cost of the sales you booked | Averages hide category disasters; apparel and electronics need their own rows |
| Repeat purchase rate | Whether marketing bought a customer or a transaction | Cohort it; a blended number mixes this quarter's promotion into last year's loyalty |

## Reading

- **Lean Analytics**, Alistair Croll and Benjamin Yoskovitz (2013). The ecommerce chapters give the mode split this card assumes: acquisition-driven versus loyalty-driven stores are different businesses with different one-metrics, and treating a low-repeat-rate store as a loyalty business wastes a year.
- **The Everything Store**, Brad Stone (2013). Not a playbook but a case history: the strongest available record of how pricing, logistics, and platform decisions compound in this domain, and of how thin margins were chosen as a weapon rather than suffered.

**Conductor overlay:** this domain sharpens DISCOVER-3 (the workaround is the current buying path), DELIVER-4 (the first cohort is a channel decision), and OPERATE-2 and OPERATE-4 (outcome versus target and cost to run are the waterfall, per order).

**Templates this bends:** [gtm-plan](../../templates/planning/gtm-plan.md) (channel economics per cohort) and [metrics-review](../../templates/operate/metrics-review.md) (input metrics become waterfall layers).

**Filled in this repo:** [domain-ecommerce-metrics-review.md](../../examples/domain-ecommerce-metrics-review.md) fills the [metrics-review](../../templates/operate/metrics-review.md) template directly for this domain, for Threadmere Apparel: checkout step 3 conversion at 3.10% target against 3.42% actual and free-returns-eligible SKU share at 18% against 31%, walked through a per-order contribution-margin waterfall (CM1, CM2, CM3) that shows conversion rising while CM2 fell as return rates rose on the widened free-returns SKUs, with return rate by size band added as the fit counter-metric. Nothing filled here bends [gtm-plan](../../templates/planning/gtm-plan.md) with an ecommerce channel-economics table specifically; [ledgerline-gtm-plan.md](../../examples/ledgerline-gtm-plan.md) is the nearest reading, only near because it sequences a B2B SaaS cohort, not a retail channel mix.

**Worked example (ILLUSTRATIVE):** a `metrics-review.md` input-metrics row, filled the way this card's contribution-margin waterfall would bend it. All names and figures invented.

| Input metric | Target (signed) | Actual | Read |
|---|---|---|---|
| Conversion rate, checkout step 3 | 3.10% | 3.42% | Up, but see CM2 below before calling this a win |
| Free-returns eligible SKU share | 18% | 31% | The merchandising team widened eligibility to chase the conversion number above; not on this review's original target list, added because it explains the SKU-level CM2 drop |
| CM2 per order, free-returns-eligible SKUs | $6.40 | $2.15 | Return processing and re-shipment ate two-thirds of the margin the conversion gain bought; this line is why the input metric above is on this review at all |
| CM2 per order, whole store | $5.90 | $5.55 | Blended number moves less than either row above; reading it alone would have hidden the trade entirely |

Note in the review: the conversion win is real and the waterfall says it is not yet worth its return cost on this SKU set; owner to bring a category-level cap or a restocking fee to next cycle's review rather than rolling the eligibility change back blind.
