---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Capital markets", "Trading and market infrastructure", "Post-trade", "capital-markets"]
---
# Capital markets

This domain is the plumbing other financial products assume already works: the venue that matches an order, the pipe that reports the trade, and the utility that settles it. A retail app can be well designed and still depend on a matching engine and a clearinghouse it never shows the customer, and a fault in either becomes the app's outage even though its own code never changed. The loop is measured in microseconds and settlement days at once, an unusual span for one product to own.

The second distinctive fact is that speed is a feature with a regulatory ceiling, not just an engineering target: a firm with market access must have pre-trade risk controls in place before an order reaches the market, and a system fast enough to be valuable is fast enough to do a large amount of damage before a human notices. The Knight Capital incident on 1 August 2012, dormant code reactivated on deployment, roughly $440 million lost in under an hour (verify the exact figure before relying), is the canonical case for why a kill switch is a requirement, not a nice-to-have.

Settlement is also moving faster on different clocks: the US and Canada moved to T+1 in 2024, and India had already phased it in for equities by early 2023 (verify current status before relying). A product built on a T+2 assumption breaks quietly the day its market moves past it.

## Questions a PM must ask

1. Which venue type is this: a regulated exchange, a multilateral trading facility, or something that only looks like one? MiFID II's category, or its local equivalent, decides which transparency and reporting duties attach.
2. Does the firm have market access risk controls in place before an order can reach the market? Rule 15c3-5 in the US, and equivalent obligations elsewhere, require this before launch, not after the first incident.
3. What settlement cycle does this product assume, and does it match what the market actually runs today? A hardcoded T+2 assumption in a market that moved to T+1 fails quietly at the clearinghouse, not the interface.
4. Who is the counterparty when a trade fails to settle, and what does that failure cost? Under the EU's CSDR, cash penalties for fails are a known, calculable cost; elsewhere it may be undocumented.
5. What does the surveillance system actually catch, and what does it only log? A logged alert nobody reviews is not surveillance; it is an audit trail of an unexamined risk.
6. What is the kill switch, who can pull it, and has it been tested under load? A circuit breaker that has only run in a tabletop exercise is a plan, not a control.
7. What is the latency budget end to end, including the client's own distance from the venue, not just the matching engine's own number? That is the number the client actually experiences.
8. Which market data can this product redistribute, to whom, and at what tier? Exchange data licensing restricts redistribution by professional and non-professional status, and violating it can get a feed cut immediately.

## Gatekeepers

- **The exchange or venue operator.** Sets the rules of the market and membership requirements, and can suspend a member's access on a surveillance finding alone, before any regulator is involved.
- **The central counterparty (CCP).** LCH, Eurex Clearing, or a national equivalent; sets margin requirements and default-fund contributions, and can force a member to unwind positions on a risk breach.
- **The central securities depository (CSD).** DTC in the US, Euroclear and Clearstream in Europe, the Central Depository Company of Pakistan Limited for Pakistan Stock Exchange securities, with the National Clearing Company of Pakistan Limited as the separate clearing, settlement and risk-management body; settlement finality happens here, and a fail here is a fail no matter how correct the trade looked upstream.
- **Market abuse surveillance and the regulator behind it.** The EU's Market Abuse Regulation (596/2014) requires suspicious transaction and order reports; a system that cannot produce one on demand is not meeting the duty it exists for.
- **The systems and controls regulator.** The SEC's Regulation SCI for critical US market infrastructure, or an equivalent operational-resilience regime elsewhere, treats uptime as compliance, not only engineering.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Fill rate | Whether orders execute | Rises by routing only the easy, liquid orders and leaving the hard ones for a slower path the headline never sees |
| Implementation shortfall against arrival price | True cost of execution, beyond the quoted spread | A tight average hides a fat tail of large orders that moved the market against themselves, which is where the real cost lives |
| Order-to-trade ratio | Efficiency of order flow and message-traffic cost | A low ratio can mean discipline or a strategy too slow to cancel stale quotes; the number alone does not say which |
| Tick-to-trade latency | Speed of the matching engine | Measured at the exchange's own colocation, it says nothing about the latency a client outside that facility experiences |
| Settlement fail rate | Post-trade reliability | Can fall by recycling a failed trade as a new ticket rather than resolving the original fail, moving the number without moving the problem |
| Straight-through processing rate | Share of trades needing no manual touch | Counts a trade as clean the moment it clears the first system, even when a break surfaces two systems later at reconciliation |
| Surveillance alert-to-case conversion rate | Whether alerts translate into real investigations | A very low rate can mean good tuning or an overwhelmed team closing everything to clear a backlog, and the two look identical on a dashboard |
| System uptime during trading hours | Availability of the matching engine or gateway | An uptime average hides outages concentrated in the first and last minutes of a session, when volume and damage are highest |
| Margin calls met on time | Counterparty risk health | A perfect on-time record can just mean the margin methodology understates real exposure, not that risk is well managed |
| Cost per trade | Unit economics | Falls as volume rises regardless of execution quality, so a shrinking cost per trade can coexist with worse client fills |

## Reading

- **MiFID II (Directive 2014/65/EU) and MiFIR (Regulation 600/2014), especially MiFIR Article 26 on transaction reporting and MiFID II Article 27 on best execution.** Read the Level 1 text before any vendor's summary of it.
- **The Market Abuse Regulation, (EU) No 596/2014.** Defines insider dealing and market manipulation and creates the suspicious transaction and order report duty a surveillance product exists to serve.
- **SEC Rule 15c3-5, the Market Access Rule, and the enforcement order against Knight Capital Americas LLC, Release No. 70694, 16 October 2013.** Read the order for how one control failure, a code deployment left live on a single server, became a named, priced regulatory finding.
- **The Central Securities Depositories Regulation, (EU) 2018/1229 RTS on settlement discipline.** Read for the cash-penalty mechanism, noting its mandatory buy-in provisions have had a long, unsettled history (verify current status before relying).
- **SEBI's phased move to T+1 settlement for Indian equities, completed by early 2023.** Read alongside the US and Canadian move to T+1 in 2024 for how the same target arrived on different clocks (verify exact dates before relying).

**Conductor overlay:** this domain sharpens DESIGN-6 (seeing the system misbehave means watching latency and message-rate anomalies, not just error logs), BUILD-3 (a failure rehearsal here means pulling the kill switch under simulated load, not tabletop talk), DELIVER-1 (the rollback has to be proven at a pre-production venue connection, because a bad deploy at a matching engine is Knight Capital's story), and OPERATE-4 (cost to run includes exchange fees, market-data licensing, and clearing member risk charges a typical cost model has no line for).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (latency and uptime budgets are contractual with the venue, not aspirational), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (the kill switch and who may pull it belong here, written down before launch), [observability](../../templates/architecture/observability.md) (surveillance and market monitoring are a form of observability with a regulator as a stakeholder), and [release-readiness](../../templates/delivery/release-readiness.md) (a pre-production rollback rehearsal is a named line item, not implied by "tested").
