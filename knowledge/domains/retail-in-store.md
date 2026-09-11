---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Retail in-store", "brick-and-mortar retail", "in-store retail technology", "retail-in-store"]
---
# Retail (in-store)

This product runs on the shop floor, so every failure is witnessed in real time by a customer standing at a register or an associate holding a scanner, with no buffering layer between a bug and a bad experience. A dashboard that looks fine at headquarters can coexist with stores where the till has been down for twenty minutes. The distinctive fact is that point of sale, inventory, and labour scheduling are one system pretending to be three: a sale decrements inventory that a scheduling tool assumed would still need stocking, and a promotion that lifts basket size can blow through a schedule built for pre-promotion volume, so features shipped by three different teams collide physically at the same counter on the same afternoon. Payment-card rules are global but not uniform in practice: many markets outside the US moved further and faster on chip-and-PIN and contactless liability shift, so a POS built on a US card-present assumption can mishandle liability abroad.

**Adjacent industries:** restaurant POS, kitchen display and table-service systems read this card for offline-first tills, PCI scope and labour scheduling; the aggregator side is in [Food delivery and quick commerce](food-delivery-quick-commerce.md). Four things are restaurant-specific. Tips and service charges are regulated money: tip-pooling and tip-credit wage rules decide how the POS may split them, and junk-fee laws such as California's SB 478 govern how a service charge is shown. Menu data carries allergen and calorie-labelling duties. The kitchen display is as outage-critical as the till, because an order the kitchen never sees becomes a refunded meal. And dine-in, first-party online and several aggregators draw on one kitchen's capacity, so throttling incoming orders is a product decision. Dispensary and liquor-store tills read this card with the age-restricted goods material in [Ecommerce](ecommerce.md). As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. What happens at the register when connectivity drops? A store that cannot sell during an outage is not degraded, it is closed; offline capability at the point of sale is a requirement, not a resilience nicety.
2. Does this feature expand PCI DSS scope? Touching, storing, or transmitting cardholder data anywhere in the flow pulls that system into audit scope, usually discovered at audit time, not design time.
3. What is the real cost of a stockout versus an overstock for this category, and does the inventory model treat them symmetrically when they are not? A stockout loses today's sale; an overstock ties up cash and ends in a markdown.
4. Who executes this at store level, under what labour constraint, and did anyone check the schedule before assuming the feature is free to run? A planogram reset that looks like five minutes at headquarters is an hour multiplied across every store, unbudgeted anywhere.
5. What does the loyalty or promotion mechanic do to margin at the register, and is that visible before the discount applies or only in the monthly report? A stacking bug is found by a customer immediately, not by finance at month-end.
6. What is the plan when the planogram, the shelf, and the system of record disagree? They will disagree constantly at real-world execution fidelity, and the product needs a reconciliation path, not an assumption of sync.
7. What does the fraud and shrink picture look like for this specific change: self-checkout, a new return flow, a price-override permission? An override eased for a legitimate associate is eased for the wrong reason too.
8. What happens during the highest-volume day of the year, a national sales event or holiday rush? In-store systems are sized and tested for an average Tuesday far more often than for the one day that produces the year's incident postmortems.

## Gatekeepers

- **PCI DSS and the acquiring bank or payment processor.** Governs anywhere cardholder data is stored, processed, or transmitted; scope follows data flow, not intent, and a processor can suspend a non-compliant merchant.
- **EMV and regional liability-shift rules.** Chip and contactless standards decide who eats a fraud loss, and the liability owner differs by market and by which party failed to support the current standard.
- **Weights-and-measures and pricing-accuracy regulators.** Enforce that the scanned price matches the posted price, with accuracy thresholds in many jurisdictions; a promotion-engine bug that mis-scans at scale is a regulatory finding, not a refund queue.
- **Labour regulators and, where they apply, predictive-scheduling laws.** A growing set of jurisdictions require advance notice of schedules and predictability pay for late changes; an optimizer that ignores the local notice rule can generate a wage claim per affected shift.
- **Food-safety inspectors**, for categories that carry them. Cold-chain and expiry tracking inside inventory systems are inspected directly, and a system that cannot produce a lot-and-date trace on demand fails regardless of its sales analytics.
- **Store operations and loss prevention, internally.** Own the standard for what an associate may override at the register; loosening it without their sign-off is a shrink increase with a launch date.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Transaction success rate at POS | Whether the register actually works | Averaged across a chain, a handful of stores with a dead card reader for an hour disappears into a number that still looks like four nines |
| Stockout rate | Lost-sale exposure on the shelf | Measured from system-of-record inventory, not the shelf; a phantom stockout is invisible to this metric and visible to every customer who saw the gap |
| Inventory accuracy (system vs. count) | Whether decisions on the data can be trusted | A high SKU-count accuracy can hide errors concentrated in the highest-velocity, highest-margin items, where it matters most |
| Labour cost as a percentage of sales | Staffing efficiency | Improves by understaffing exactly the hours that drive the sales the ratio is measured against, producing a queue the metric cannot see |
| Shrink rate | Loss from theft, damage, and error | A blended rate hides whether the driver is external theft, internal fraud, or scanning error; each needs a different fix and the metric recommends none |
| Self-checkout loss rate vs. staffed-lane rate | Whether a channel shift trades service cost for shrink | Rises quietly for months before anyone compares the two lanes, since they report through separate systems |
| Price-accuracy rate (shelf vs. scanned) | Regulatory and trust exposure | A chain-wide average can be compliant while specific promotional end-caps run persistently wrong |
| Planogram compliance rate | Whether the shelf matches the plan | Self-reported by store staff in many chains, rewarding marking it done over doing it; an audited sample tells a different story |
| On-time replenishment rate | Supply chain reliability into the store | Measured to the back room, not the shelf; stock can sit unshelved for days while the metric reports success |

## Reading

- **The PCI Security Standards Council's PCI DSS standard**, current version. Read the scoping guidance before assuming a feature that merely displays a receipt is out of scope.
- **EMVCo's documentation on chip and contactless liability shift**, and your acquirer's regional bulletin. Read your own region's rule rather than a US-centric summary.
- **A national weights-and-measures agency's price-accuracy inspection program**, for example US state item-pricing programs or a comparable EU member-state consumer-protection authority's shelf-price rules. Read the accuracy threshold your market enforces.
- **A predictive-scheduling ("fair workweek") ordinance** in a jurisdiction your footprint includes. Read the advance-notice and predictability-pay mechanics directly; they are specific numbers, not general fairness language.
- **Reporting on a major retailer's self-checkout shrink data or policy reversal.** Several large chains have publicly scaled back self-checkout after shrink data came in worse than projected; read for the mechanism, not just the reversal.
- **The FDA Food Code, or your national food-safety code**, for any footprint selling perishable goods. Read the cold-chain and traceability requirements if your inventory system is the record an inspector will ask to see.

**Conductor overlay:** this domain sharpens DESIGN-2 (integrations: the POS, payment terminal, and inventory stack are third-party systems with PCI scope and their own outage behavior, and connectivity loss at one store is a designed scenario, not an incident), DESIGN-6 (seeing it misbehave: a register hang is visible to a queue of customers before any dashboard alert fires, so store-floor thresholds have to be tighter than headquarters ones), DELIVER-1 (the rollback: a fleet-wide POS or pricing push needs a rehearsed rollback, because a bad update can take down thousands of registers in one deployment window), and OPERATE-4 (cost to run: labour hours and store-manager support burden belong beside incident counts, since a technically healthy system can still run store staff ragged).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (POS, payment terminal, and inventory systems carry PCI scope and offline behavior as first-class rows), [observability](../../templates/architecture/observability.md) (store-floor SLOs and alert thresholds, tighter than a typical back-office system's), [release-readiness](../../templates/delivery/release-readiness.md) (a fleet-wide POS or price-file push gets its own rehearsed rollback line), and [capacity-plan](../../templates/planning/capacity-plan.md) (labour hours per store are a capacity constraint a feature can silently consume).

**Filled in this repo:** [harbourgate-integrations.md](../../examples/harbourgate-integrations.md) is a direct sector match, a retailer's payment-service integration register; read rows I-1 and I-3 for how a kiosk falls back to "pay at the till" rather than going dark, and how PCI scope rides along with each card-data boundary. [harbourgate-observability.md](../../examples/harbourgate-observability.md) is a direct match; read the kiosk SLO row for a store-floor threshold held tighter, per shop per day, than the back-office availability SLO beside it. [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md) is a direct match; read the rollback rehearsal timing (a flag flip rehearsed at 3 minutes 50 seconds before any cohort went live) for what "rehearsed" has to mean before a fleet-wide push. [harbourgate-capacity-plan.md](../../examples/harbourgate-capacity-plan.md) fills the capacity-plan template this card bends: read it for labour-hours-per-store carried as a named capacity constraint.

**Worked example (ILLUSTRATIVE):** a slice of [integrations](../../templates/architecture/integrations.md) section 1, showing how this sector's offline requirement changes a POS row. Names and numbers are fiction.

| # | Counterparty system | Direction | Protocol | Auth | Counterparty SLA (and source) | Owner (ours) | Failure behavior (one clause) |
|---|---|---|---|---|---|---|---|
| I-4 | In-store card terminal, chip and contactless | Outbound | Vendor SDK over the store LAN | Terminal keys, per device | 99.9% monthly availability, acquirer MSA schedule 2 (ILLUSTRATIVE) | Dana Okoye, Payments Engineering | On connectivity loss the terminal switches to store-and-forward: the card is authorised offline up to a $50 floor limit (ILLUSTRATIVE, per the acquirer's offline-auth rules) and queued for online settlement on reconnect; the register never goes "closed" for a network blip alone |

The row's PCI-scope note, carried in the detail block below the register rather than the table above, is what this sector adds that a generic integrations row would not think to ask: whether cardholder data crosses the LAN unencrypted at the terminal decides whether this one boundary pulls the whole store network into PCI DSS scope.
