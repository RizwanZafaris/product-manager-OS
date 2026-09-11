---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Energy", "Utilities", "energy retail", "smart metering", "energy-utilities"]
---
# Energy and utilities

An energy product sells something with no substitute and no memory: a household cannot skip electricity for a billing cycle in protest, and a kilowatt-hour delivered is indistinguishable from any other. The whole business runs on infrastructure, tariffs, and reliability duties set largely outside the product team's control. The distinctive fact of this domain is that the physical grid and the software layer on top of it are regulated separately, and a feature that looks purely digital, a demand-response signal, a dynamic tariff, can still trip a grid-code or licence condition the moment it changes how power actually flows.

The second distinctive fact is that outages carry statutory consequences most software never faces: guaranteed-standards schemes, automatic compensation, and public reliability reporting turn a service incident into a regulatory filing. A metering or billing product also inherits data revealing when a household is home, asleep, or away, which makes an ordinary usage chart a surveillance risk if handled carelessly.

## Questions a PM must ask

1. Which licence or market role does this feature touch: supply, distribution, generation, or an unregulated overlay on top? Regulatory obligations attach to the licensed activity, not to how the feature is described internally.
2. What guaranteed-standard or reliability-reporting duty do this product's outages fall under, and does the system produce the evidence that duty requires? A regulator's compensation scheme runs on your own outage data.
3. Does this feature require a grid connection agreement, or a change to one, and what is that queue actually running at? A strong demand-response product is worthless behind a multi-year connection queue.
4. What happens to a smart meter or charger when it loses its communication link? Devices installed in the field for a decade need a defined, tested offline behavior, not an assumption of permanent connectivity.
5. Where does interval usage data go, who can access it, and what does it reveal about occupancy? Half-hourly consumption data is close to a movement log for the household it comes from.
6. What tariff or price-cap rules constrain what this product may charge or how it may present a price? A pricing screen that is clean UX in software can be a mis-selling complaint in a regulated tariff market.
7. What is the cybersecurity posture of anything able to influence load or generation, even indirectly? Control-adjacent software inherits critical-infrastructure obligations even when it never touches a physical relay.
8. What is the plan when this feature is active during a genuine supply emergency: a cold snap, a heatwave peak, a grid fault? Energy products get judged on the worst week of the year, not the average one.

## Gatekeepers

- **The national or regional energy regulator.** Bodies such as Ofgem in the UK, FERC and state commissions in the US, or national regulators coordinated through the EU's ACER, set licence conditions, tariff rules, and switching rights a product cannot quietly opt out of.
- **The grid or system operator.** Connection agreements and grid codes, run by the national grid operator or a regional equivalent, gate anything that exports power or shifts load, including EV charging and demand response.
- **Critical-infrastructure cybersecurity authorities.** Regimes such as NERC's CIP standards in North America carry real financial penalties, and the EU's NIS2 Directive treats energy as an essential sector; a control-system change is a compliance event, not just a deploy.
- **The metering or smart-meter data-network operator.** In markets with a centralized metering data layer, such as the UK's Data Communications Company, you do not get raw access to meter data; you get what the scheme allows.
- **The consumer or tariff-protection regulator.** Price caps, standing charges, and switching rules are set externally and can change on a schedule the product team does not control.
- **Local permitting and planning authorities.** Physical infrastructure, chargers, meters, and substation upgrades, needs permits that run on municipal timeframes, not release schedules.
- **Safety and outage-standards bodies.** Guaranteed-standards or reliability-index regimes impose automatic compensation and public reporting duties that a software incident report alone does not satisfy.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| SAIDI / SAIFI (outage duration and frequency) | Grid reliability | System-wide averages hide that a rural or poorly-served minority carries almost all the outage-minutes |
| Smart meter rollout rate | Metering modernization progress | Installed is not communicating; a meter stuck in fallback mode counts toward rollout while delivering none of the data value |
| Demand-response enrollment rate | Flexible capacity on paper | Enrollment counts customers who signed up once and never curtail when called; dispatched versus enrolled is the honest number |
| EV charger uptime | Charging network reliability | Firmware-reported uptime often excludes payment failures, so a charger can be up and still undriveable-through |
| Time to restore after an outage | Outage response speed | Measured from fault detection, not from when the first customer reported it, so a detection gap disappears from the number |
| Billing accuracy / estimated-read rate | Metering and billing quality | A low estimated-read rate can still hide a systemic error if the estimation method is wrong for an entire tariff class |
| Grid connection queue time | Whether new load can actually connect | A completed study can still leave a customer behind a much longer physical-works queue the metric never shows |
| Peak-demand reduction attributed to a program | Program effectiveness | Weather-normalization assumptions can manufacture savings a hot or cold snap would have erased anyway |
| Cybersecurity patch compliance on control assets | OT security posture | Patched per inventory does not mean the inventory is complete; unmanaged legacy systems are the ones actually at risk |
| Customer switching rate | Market competitiveness | In a market with a sticky default tariff, low churn can mean satisfaction or a switching process that is quietly hard |

## Reading

- **The EU Electricity Directive**, Directive (EU) 2019/944, part of the Clean Energy Package, the internal-market rulebook behind unbundling, switching rights, and smart metering across the EU.
- **FERC Order No. 2222** (2020), which opened US wholesale electricity markets to aggregated distributed energy resources, the regulatory move behind most modern demand-response products.
- **The EU's Alternative Fuels Infrastructure Regulation**, Regulation (EU) 2023/1804, setting minimum EV charging-point density and requiring ad hoc card or contactless payment without a mandatory subscription (verify current thresholds before relying on them).
- **NERC's Critical Infrastructure Protection standards**, the mandatory, penalty-backed cybersecurity requirements for the North American bulk power system, worth reading even outside North America as a mature rulebook of its kind.
- **The EU's NIS2 Directive**, placing energy among the essential-entity sectors carrying the strictest cybersecurity and incident-reporting duties.
- **The December 2015 Ukraine power-grid cyberattack**, the first confirmed cyberattack-caused blackout, and the standing argument for why operational-technology security in energy sits at board level, not only in IT.
- **ERCOT and Winter Storm Uri, February 2021** (verify specific figures before relying on them), the modern lesson that a market can clear on paper while the physical grid still fails the people depending on it.

**Conductor overlay:** this domain sharpens DEFINE-1 (the stakes include physical safety and statutory outage duties, not only commercial risk), DESIGN-2 (integrations are the grid operator and the metering data network, both gatekept), DELIVER-6 (regulated overlay drift, as licence conditions and tariff rules change under a live product), and OPERATE-4 (cost to run includes settlement and connection costs the roadmap rarely prices in upfront).

**Templates this bends:** [integrations](../../templates/architecture/integrations.md) (grid operator and metering-network interfaces carry SLAs and failure behavior as first-class rows), [sla-slo-definition](../../templates/delivery/sla-slo-definition.md) (outage restoration measured the way the regulator's guaranteed-standards scheme measures it), [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (licence conditions and critical-infrastructure duties per market), and [risk-register](../../templates/execution/risk-register.md) (grid-dependency and connection-queue risk carried alongside delivery risk).

**Filled in this repo:** [domain-energy-utilities-sla-slo-definition.md](../../examples/domain-energy-utilities-sla-slo-definition.md) fills the [sla-slo-definition](../../templates/delivery/sla-slo-definition.md) template directly for this domain, for Gridline Utilities: an 18-hour restoration SLI for 90% of customers on an urban feeder, timed from the earlier of the first customer report or automated detection, with SLIs for detection gap, estimated-restoration accuracy, notification latency, and priority-services-register contact, an error budget tied to guaranteed-standards compensation exposure, and major-event exemptions, reviewed with the DNO's regulatory reporting lead. For the other three bent templates, [harbourgate-integrations.md](../../examples/harbourgate-integrations.md), [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) and [harbourgate-risk-register.md](../../examples/harbourgate-risk-register.md) remain the nearest reading for counterparty-SLA, licence-condition, and grid-dependency-risk row shapes, though all three evidence a payments checkout, not a grid operator or metering network.

**Worked example (ILLUSTRATIVE):** an SLA/SLO row for a guaranteed-standards restoration duty:

| Service | SLO target | Measurement window | Regulator-facing duty it evidences | Owner |
|---|---|---|---|---|
| Unplanned outage restoration, urban feeder | Restore within 18 hours for 90% of affected customers per event (ILLUSTRATIVE target; verify the applicable scheme's actual threshold before quoting a real figure) | Per event, timed from the earlier of first customer report or automated fault detection | A guaranteed-standards compensation-scheme filing, the pattern bodies such as Ofgem in the UK run | Grid Operations Lead |

The window is written deliberately as "the earlier of" the two timestamps, not from detection alone: the card's own metrics table warns that measuring restoration from fault detection rather than the first customer report hides the detection gap from the number, so this SLO closes the gap the metric would otherwise let slide.
