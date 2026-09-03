---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Logistics"]
---
# Logistics

Logistics products make promises about atoms: this thing, there, by then, intact. The economics concentrate brutally at the last mile, the leg where density collapses and a driver meets one door at a time, which is why cost per delivery and route density govern more product decisions than any feature request. The other defining fact is that the exception path IS the product: anyone can track a package that arrives; the failed delivery attempt, the damaged pallet, the missed dock window, and the customs hold are where software either earns its keep or gets replaced by a phone call.

## Questions a PM must ask

1. What is the cost per delivery at current density, and what does the model say it becomes if volume doubles in the same zones versus new zones? Density, not volume, is the lever; growth that spreads thin makes every stop more expensive.
2. What share of the end-to-end cost is the last mile, and which product levers actually touch it: first-attempt success, pickup points, delivery windows, route optimization? Precision on this beats a year of dashboard work.
3. What is our OTIF (on time, in full), measured the way the customer measures it? Retail customers score OTIF on their own definitions and charge penalties against them; your internal number is trivia if it is not their number.
4. What are the top five exception types by cost, and what is the designed path for each? Count the exceptions that end in a human phone call; that count is your real product backlog.
5. Which regulated constraint binds the network: driver hours-of-service rules (DOT/FMCSA in the US, with electronic logging mandated), vehicle and weight regimes, dangerous-goods rules? Route plans that ignore the legal clock are fiction.
6. If drones or autonomy are on the roadmap: what does the current rulebook actually permit? US drone operations run under FAA Part 107 waivers today, with a broader beyond-visual-line-of-sight framework (Part 108) proposed but not settled; verify the live status before any commitment, and treat vendor claims about it as marketing.
7. For cross-border flows: who files customs entries, who is the importer of record, and what data must be perfect for the shipment not to sit? Customs holds are data-quality failures wearing a uniform.
8. What does peak look like, and what breaks first: capacity, the promise engine, or the exception queue? Networks are sized for their worst week.

## Gatekeepers

- **Transport regulators.** DOT/FMCSA hours-of-service and ELD rules bind routing and scheduling; FAA governs anything airborne; equivalents per market.
- **Customs authorities.** Documentation, classification, and duties gate every border crossing; their clock is not negotiable in-app.
- **Shipper compliance programs.** Large retail customers enforce OTIF scorecards, labeling specs, and dock-scheduling rules with chargebacks; their requirements documents are your requirements documents.
- **Insurers and safety auditors.** Coverage terms constrain what the network may carry and how; incidents reprice the whole operation.
- **Labor agreements**, where present: work rules shape what the software may schedule.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Cost per delivery | The unit economics of the promise | Averaged across zones it hides that some routes fund others; split by density tier |
| OTIF, customer-defined | Reliability as the customer scores it | Internal on-time definitions drift friendlier; reconcile to the scorecard that charges penalties |
| First-attempt delivery rate | Last-mile efficiency and customer experience in one number | Inflating it with "safe place" drops trades cost for claims |
| Route density (stops per hour) | Whether growth is compounding or diluting | Improves mechanically when service area shrinks; pair with coverage |
| Exception rate by type, and cost per exception | Where the product work is | An overall exception percentage hides that one type causes most of the phone calls |
| Capacity utilization | Asset economics | Runs highest just before service collapses; watch it with OTIF, never alone |

## Reading

- **The Box**, Marc Levinson (2006). The container's history as the domain's founding lesson: the breakthrough was not the steel box but the standardization of interfaces between ship, truck, rail, and port, which made the system composable and collapsed costs. Every integration decision in logistics software is a small rerun of this story.
- **Logistics Clusters**, Yossi Sheffi (2012). Why logistics activity agglomerates and why density is the industry's gravity: infrastructure, labor pools, and freight lanes compound in place. The product translation: network shape decisions beat feature decisions, and the map is a strategy document.

**Conductor overlay:** this domain sharpens DEFINE-5 (how requirements fail: enumerate the exception paths, they are the requirements), DESIGN-2 (integrations: carriers, WMS, customs, and the customer's scorecard system), and OPERATE-4 (cost to run is cost per delivery, split by zone).

**Templates this bends:** [failure-scenarios](../../templates/delivery/failure-scenarios.md) (exception types become scenarios with detection and recovery owners) and [integrations](../../templates/architecture/integrations.md) (carrier and customs interfaces carry SLAs and failure behavior as first-class rows).
