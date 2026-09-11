---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Travel and hospitality", "travel tech", "hospitality technology", "travel-hospitality"]
---
# Travel and hospitality

This product sits inside somebody else's inventory and somebody else's distribution pipe more completely than almost any other domain. Airlines and hotels set the fare or rate; GDSs such as Amadeus, Sabre, and Travelport move the availability; a booking product is mostly an orchestration layer over systems it does not own and cannot change on its own schedule. The distinctive fact that follows is that the exception is the product. Anyone can sell a seat that departs on time; disruption, the cancelled flight, the overbooked room, the missed connection, is where the money, the reputation, and the regulatory exposure concentrate, and it is rare in a demo and common in the first bad-weather week after launch. Duties also differ sharply by jurisdiction and do not align: EU passenger-rights rules are more specific and stricter than the US framework, so a product built to the more permissive regime violates the stricter one the moment a European traveler books.

**Adjacent industries:** events and ticketing (primary ticketing, resale and event management) read this card: the service is delivered long after the charge, chargebacks spike on cancellation, and drip pricing is regulated. Three rules are ticketing's own. All-in price display is required for live-event tickets in the US under the FTC's 2025 rule on unfair or deceptive fees, which also covers short-term lodging (verify scope). The BOTS Act and on-sale surges make queue fairness and bot defence the launch-critical system. Resale price caps and transfer restrictions vary by market, and venue and promoter exclusivity decides what inventory exists at all; resale mechanics are in [Marketplaces](marketplaces.md). Passenger rail ticketing reads this card too, with delay-compensation and refund rights playing the part air passenger rights play for flights. As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Are we the merchant of record, an OTA or agent, or a metasearch referrer? The answer decides who owes the refund and whose name is on the card statement in a dispute.
2. What inventory source feeds this: a direct airline or hotel API, a GDS, or a channel manager aggregating both? Each has different update latency, and a shown rate or seat can already be gone by the time a booking posts.
3. What is the actual refund and cancellation obligation, by jurisdiction? EU Regulation 261/2004 sets specific compensation for denied boarding, cancellation, and long delay on qualifying flights; the US framework is narrower and enforced differently. Assuming one regime is global mis-prices the promise.
4. What happens to a booking, and to money already collected, if the supplier becomes insolvent mid-trip? Package-travel protection schemes exist for exactly this, and selling packages without checking eligibility can strand a customer and leave the seller liable.
5. How fresh is our inventory data, and what happens when a confirmed booking turns out oversold at the property or the gate? Overbooking is normal supply-side practice; the product needs a designed response, not a support ticket.
6. Loyalty points: are we minting a liability, redeeming someone else's, or both? Points are a deferred-revenue question before they are a UX feature, and breakage assumptions are not yours to set unilaterally.
7. What is the chargeback exposure when a trip is disrupted? Travel carries some of the highest chargeback rates of any vertical because service is delivered long after the charge, leaving room for expectation and performance to diverge.
8. What does the product do during a mass-disruption event, a grounded fleet or a visa-rule change? Support volume during an irregular-operations event is a different failure mode, not a scaled-up normal day.

## Gatekeepers

- **Aviation regulators and passenger-rights rules.** The US DOT's refund rule requires cash refunds for cancelled or significantly changed flights when the passenger declines the alternative (verify current thresholds before relying); the EU's Regulation 261/2004 sets fixed compensation tiers for denied boarding, cancellation, and long delay. The regimes do not defer to each other.
- **The EU Package Travel Directive (Directive (EU) 2015/2302).** Anyone combining flight, accommodation, or car hire into a package takes on organizer liability and insolvency-protection duties; bundling two supplier products can create an organizer without anyone deciding that on purpose.
- **IATA and the GDS layer.** Set the technical and commercial rules for how fares, availability, and PNRs move; a distribution deal or accreditation requirement can gate whether a product may sell certain inventory at all.
- **Card networks and acquirers.** The long gap between charge and delivery draws extra scrutiny; a chargeback-ratio program threshold can restrict what a travel merchant is allowed to process.
- **Airline and hotel revenue-management teams.** Not regulators in the legal sense, but rate-parity clauses and channel rules decide what a product may show and at what price, and breaching them can mean losing the feed.
- **Consumer-protection authorities.** Enforce accurate pricing and cancellation-policy honesty; specific disclosure rules vary sharply by country, so a format compliant in one market can violate the next (verify your specific markets before relying).

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Booking conversion rate | Funnel efficiency | Rises when drip pricing hides mandatory fees until the last step; the complaint arrives after the booking completes |
| Net revenue per booking | Real yield after supplier cost | Blends merchant-of-record and agency-model bookings with different cost structures into one number that describes neither |
| Load factor or occupancy | Utilization of the inventory | High utilization is exactly the condition that produces overbooking; read it beside disruption compensation paid |
| Refund cycle time | Whether disrupted customers get paid back on the regime's clock | A median hides the tail: disputed refunds that miss the statutory window are the ones that become chargebacks |
| Chargeback rate | Payment health and trust | Falls if disputes become hard to file, which shows up later as a card-network penalty rather than a problem solved |
| Ancillary revenue per booking | Monetization beyond the base fare | Grows by making a previously included item a paid add-on; total price and perceived fairness can move opposite the metric |
| Net Promoter Score | Perceived experience | Collected after a smooth booking and rarely after a disrupted trip, so the sample excludes the experience that matters most |
| Loyalty point liability outstanding | Deferred-revenue exposure | A growing balance reads as engagement; it is also a growing liability that breakage assumptions may understate |
| Disruption resolution rate within SLA | Whether the exception path works | An internal SLA can be looser than the statutory one it is meant to satisfy, so green can still mean a live obligation |

## Reading

- **EU Regulation (EC) No 261/2004.** Read the compensation tiers and the "extraordinary circumstances" carve-out directly; airlines litigate that carve-out constantly, and refund logic has to encode it correctly.
- **The US DOT's airline refund rule.** Read the current requirement for automatic cash refunds on cancelled or significantly changed flights (verify current thresholds and dates, since this rulemaking has moved more than once).
- **The EU Package Travel Directive (Directive (EU) 2015/2302).** Read the organizer-liability and insolvency-protection provisions before assuming a bundling feature is just a booking flow.
- **IATA's distribution and NDC documentation.** Orientation for why availability and fares move through intermediaries with their own commercial terms.
- **Reporting on Southwest Airlines' December 2022 holiday-period meltdown.** The booking system worked; the crew-scheduling and rebooking systems could not absorb the exception volume, the pattern this domain repeats.
- **A national consumer-protection regulator's guidance on drip pricing in travel**, for example Australia's ACCC. Non-US enforcement is often ahead of the US on mandatory total-price display.

**Conductor overlay:** this domain sharpens DEFINE-5 (how requirements fail: cancellation, denied boarding, and refund paths are the requirements, not edge cases bolted on afterward), DESIGN-2 (integrations: the GDS or channel-manager feed is a third party's SLA, and availability can be stale before your own system notices), DELIVER-4 (the first cohort is a route or market, because passenger-rights regimes and supplier relationships are both local), and OPERATE-8 (the counter-metric: booking growth or load factor can rise while disruption-compensation exposure and chargebacks rise with it).

**Templates this bends:** [failure-scenarios](../../templates/delivery/failure-scenarios.md) (cancellation, denied boarding, and supplier insolvency become named scenarios with a detection and compensation owner), [integrations](../../templates/architecture/integrations.md) (the GDS or channel-manager connection carries someone else's latency and outage), [customer-comms](../../templates/delivery/customer-comms.md) (a disruption notice is a different document than a marketing email and often has a statutory deadline), [gtm-plan](../../templates/planning/gtm-plan.md) (the first cohort is a route or corridor, not a broadcast), and [metrics-review](../../templates/operate/metrics-review.md) (a compensation-exposure and chargeback row sits beside the growth metrics every review).

**Filled in this repo:** [domain-travel-hospitality-failure-scenarios.md](../../examples/domain-travel-hospitality-failure-scenarios.md) fills the [failure-scenarios](../../templates/delivery/failure-scenarios.md) template directly for this domain, for Larkhollow Air: the FS-2 denied-boarding row under EU Regulation 261/2004 for 6 passengers, a schedule change triggering automatic refunds under the US DOT 2024 refunds rule, a GDS or channel-manager sync failure causing oversale, a cancellation with an extraordinary-circumstances assessment, mass rebooking during irregular operations, and a partner hotel walking guests, with compensation calculated and offered in the app before the passenger files anything. For the other four bent templates, [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) and [ledgerline-gtm-plan.md](../../examples/ledgerline-gtm-plan.md) remain the nearest reading for the connection-latency and evidence-based-cohort shapes. customer-comms has no filled example in the repository yet.

**Worked example (ILLUSTRATIVE):** A denied-boarding scenario row, in the shape of `templates/delivery/failure-scenarios.md` section 1. Every name below is invented; the cited regulation is real and named accurately.

| ID | Scenario | Blast radius | Detection | Recovery | Data loss risk |
|---|---|---|---|---|---|
| FS-2 | An EU-departing flight is denied boarding for 6 confirmed passengers due to overbooking | The 6 affected passengers are owed fixed compensation under EU Regulation (EC) No 261/2004; every other passenger on the flight is unaffected | The airline's departure-control-system overbooking event, ingested within 15 minutes; a support ticket alone is too slow to catch the statutory window | Auto-calculate the EU261 compensation tier by flight distance and offer it in-app without the passenger filing a claim, escalating to a human agent only if the passenger disputes the tier; owner: Priyanka Iyer, Disruption Ops; target: offer sent within 2 hours of the departure-control-system event | None directly, but a missed statutory deadline converts into chargeback risk once the passenger disputes through their card issuer instead |

The template's own columns stay unchanged; what a travel product adds is a recovery step that runs before the customer files anything, because the compensation is owed on a regulator's clock, not on the support queue's.
