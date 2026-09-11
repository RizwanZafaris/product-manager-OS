---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Food delivery", "quick commerce", "q-commerce", "food-delivery-quick-commerce"]
---
# Food delivery and quick commerce

Three or four sides move at once: the diner who orders, the restaurant or dark store that fulfills, the courier who moves the order, and, for aggregator models, the platform's own commission sitting between all of them. A change that shortens delivery time for the diner routinely does it by tightening the courier's trip window, and the product's real tradeoffs live in that transfer, not in the app's UI. The distinctive fact is that the courier is a worker whose classification, employee, independent contractor, or a jurisdiction's third category, this product's own dispatch and pay logic effectively decides, whatever the contract says, and that question is actively litigated and legislated across multiple markets at once. The EU's directive on platform work pushes member states toward a presumption of employment where a platform exercises enough control over how work is done, a materially different starting point than the contractor-first assumption common in US gig-economy products; a dispatch algorithm passing as "just matching" under one framework can trigger a presumption of employment under the other.

## Questions a PM must ask

1. Which side is actually constrained in this market: riders, restaurants, or demand? Subsidizing the wrong side burns cash while the real bottleneck stays unaddressed.
2. What does the dispatch and incentive algorithm decide about a courier's working conditions: route, acceptance pressure, effective hourly pay after unpaid waiting time? Regulators and courts increasingly treat the degree of algorithmic control as the test for employment status, not the contract's label.
3. Who owns food-safety failure at each handoff: the restaurant's preparation, the dark store's storage, or the courier's transport time and temperature? A single restaurant-partner liability clause does not cover a dark-store model where your own facility did the storage.
4. What is the unit economics per order once courier pay, restaurant commission, and delivery subsidy are all netted out? A rapidly growing order count can mean a rapidly growing loss per order if the subsidy behind it is invisible to whoever is watching.
5. What happens when demand spikes past courier supply in a small radius, a weather event or a big local event? Surge pricing and long waits are a designed response to a real constraint, but still need explaining to a hungry customer.
6. For a dark-store model: who holds the inventory risk, and what is the spoilage picture for a fast-moving, perishable catalog stored for speed rather than turnover efficiency?
7. What data does the platform hold about the restaurant's own customers, and does the restaurant get access to it? Restaurants often cannot see their own repeat customers on an aggregator platform.
8. What is a courier's actual recourse when the algorithm deactivates them? An opaque deactivation process draws the same black-box scrutiny automated hiring tools draw in HR tech.

## Gatekeepers

- **Employment and labour regulators, and the courts deciding worker-classification cases.** Whether a courier is an employee, an independent contractor, or a jurisdiction-specific third category turns on the control the platform's dispatch, pricing, and deactivation logic exercises, not the contract's label.
- **The EU's directive on platform work.** Directive (EU) 2024/2831, adopted 23 October 2024 with transposition due by 2 December 2026, requires a rebuttable presumption of employment where facts indicating direction and control are found under national law, collective agreements and practice; the originally proposed list of control indicators with a threshold count did not survive into the final text. It also regulates algorithmic management, monitoring and automated decisions affecting working conditions (verify transposition in your target member state).
- **Food-safety regulators.** The FDA Food Code, or a national equivalent, and the EU's General Food Law framework govern temperature control, allergen handling, and traceability; a delivery-time promise that compromises cold-chain integrity is a finding regardless of commercial success.
- **Local licensing and zoning authorities for dark stores.** Many jurisdictions never zoned for a delivery-only fulfillment center at retail-adjacent hours and density; permitting, noise, and traffic rules are being tightened in some cities in response.
- **Consumer-protection regulators, on pricing transparency.** Delivery fees, service fees, and surge pricing draw the same drip-pricing scrutiny as travel booking; several markets now require all-in pricing before checkout.
- **Restaurant partners, collectively.** Not a formal regulator, but function as one: a commission rate or ranking change a critical mass of restaurants finds unworkable produces delisting or a public dispute, and restaurant associations in several markets have organized specifically around commission rates.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Delivery time (order to door) | Speed-promise reliability | Improves by pressuring courier acceptance windows and routing, pushing cost onto effective courier pay per hour, invisible to this metric |
| Contribution margin per order | Real unit economics after courier pay and commission | Growth funded by delivery-fee or courier-pay subsidy looks identical to organic growth on a top-line dashboard |
| Courier effective hourly pay | Whether the labour model is sustainable and lawful | Headline per-delivery pay looks adequate while unpaid waiting time and uncovered vehicle cost quietly erode it |
| Order acceptance rate (couriers) | Whether the dispatch offer is attractive | A falling rate reads as a supply problem when it often signals unattractive pay or routing |
| Restaurant or dark-store on-time fulfillment rate | Whether the kitchen or store side holds | Blended across partners, it hides that a handful of chronically late ones drive most complaints |
| Food-safety complaint rate | Safety performance across the chain | Under-reports by default, since a diner who gets mildly sick rarely files a report tied to a specific order and handoff |
| Order growth rate | Demand momentum | Says nothing about whether growth is profitable, subsidized, or concentrated in a radius the courier network cannot sustain |
| Dark-store shrink and spoilage rate | Real cost of holding a fast, perishable catalog | A low rate can reflect an overly conservative, thin catalog rather than efficient operations |
| Courier deactivation rate and appeal outcome | Whether algorithmic management is fair and lawful | A low rate can mean a well-behaved pool, or disputes resolved by attrition before ever being logged |

## Reading

- **The EU's directive on platform work.** Read Article 5 on the employment presumption, which turns on facts indicating direction and control under national law rather than on a count of indicators, and the algorithmic-management chapter directly; they name the exact dispatch and monitoring features a product team builds without thinking of them as legally load-bearing (verify transposition status in your target member state).
- **Uber BV v Aslam [2021] UKSC 5 (UK Supreme Court).** Read for which features, routing, pricing, deactivation, counted as evidence of control; drivers were found "workers," a UK status short of employment but carrying minimum-wage and holiday-pay rights.
- **The FDA Food Code**, or your national food-safety code, and the EU's General Food Law framework where applicable. Read the temperature-control and traceability sections directly.
- **Reporting on a major quick-commerce dark-store retrenchment or shutdown wave.** Several well-funded operators scaled back or exited markets after unit economics did not hold at the promised delivery-time band; read for which cost line broke first.
- **A city or national regulator's ruling or guidance on dark-store zoning.** Several European and Asian cities issued specific rules for quick-commerce dark stores that a plain retail-zoning assumption will miss.
- **A restaurant-association public statement or study on aggregator commission rates.** Read one from your market for the restaurant-economics side of the platform, otherwise invisible to a diner- or courier-focused team.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: the courier is a worker whose pay and classification this product's logic effectively decides, not merely a "partner" abstraction), DESIGN-2 (integrations: restaurant POS or menu feeds and courier dispatch are third-party systems with their own SLA and outage behavior), DELIVER-4 (the first cohort is a delivery radius or dark-store catchment, not a city, because courier density and demand both have to clear a local liquidity bar), and OPERATE-8 (the counter-metric: delivery time and order growth can improve while courier effective pay, food-safety incidents, or deactivation disputes worsen alongside them).

**Templates this bends:** [personas](../../templates/discovery/personas.md) (the courier gets a named persona with its own incentives, not a fulfillment-layer abstraction), [integrations](../../templates/architecture/integrations.md) (restaurant POS/menu and courier-dispatch systems as third-party dependencies with SLAs you do not control), [metrics-review](../../templates/operate/metrics-review.md) (courier effective pay and food-safety incidents sit beside delivery-time and growth every review), and [risk-register](../../templates/execution/risk-register.md) (worker-classification exposure and food-safety chain-of-custody are standing risk rows, not one-time launch checks).

**Filled in this repo:** [domain-food-delivery-quick-commerce-risk-register.md](../../examples/domain-food-delivery-quick-commerce-risk-register.md) fills the [risk-register](../../templates/execution/risk-register.md) template directly for this domain, for DashCrate: the courier-classification row in the viability category, cold-chain temperature excursions and recall handling in dark stores, dependence of unit economics on subsidy, algorithmic-management transparency under the EU Platform Work Directive, city zoning limits on dark stores, and rider-safety incidents driven by the 15-minute promise, with one accepted risk signed by the CEO. For the other three bent templates, [sahulat-personas.md](../../examples/sahulat-personas.md), [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) and [ledgerline-metrics-review.md](../../examples/ledgerline-metrics-review.md) remain the nearest reading for persona, integration, and counter-metric row shapes, though none carries a gig-worker, dispatch-provider, or per-order unit-economics fact.

**Worked example (ILLUSTRATIVE):** a filled risk-register row for a fictional quick-commerce operator, "DashCrate," following the [risk-register](../../templates/execution/risk-register.md) shape used in [harbourgate-risk-register.md](../../examples/harbourgate-risk-register.md):

| # | Risk (event, not a vague noun) | Category | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| R9 | DashCrate's dispatch-and-deactivation logic is found to exercise enough direction and control that couriers are presumed employees under the EU platform-work directive in a launched member state | viability | 2 | 3 | 6 | mitigate | Legal review of the dispatch algorithm's control indicators against the transposed national law before entering that market; a published, human-reviewable deactivation-appeal process on a fixed clock, so the presumption's "direction and control" test has a countervailing fact on file | Priya Nakamura, Head of Legal | 2026-11-30 |

A generic risk-register row scores "vendor outage" or "data breach"; this one names a labour-law presumption with a specific directive and a specific trigger (entering a transposing member state), because in this sector the dispatch algorithm's design, not a contract clause, is the fact regulators and courts weigh. The category is "viability," the template's six-value enum (value / usability / feasibility / viability / delivery / security) holding no "compliance" value: a presumption-of-employment finding converts the courier workforce from a flexible, per-order cost into one carrying minimum-wage, holiday-pay, and termination obligations overnight, the same cost-structure-and-business-continuity threat harbourgate-risk-register.md's R4 (single-provider concentration) scores as viability, not a standalone compliance category the template does not define.
