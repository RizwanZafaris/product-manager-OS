---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Automotive", "Mobility", "connected vehicles", "ride-hailing", "automotive-mobility"]
---
# Automotive and mobility

A car is now a rolling software platform that also happens to be a two-ton object moving through traffic, and the two halves are certified by different regimes on different clocks. The distinctive fact of this domain is that a change to safety-relevant software is, to a type-approval authority, the same kind of event as a change to the brakes: it can require re-approval before the vehicle may legally be sold or, for an already-sold fleet, before an update may be pushed.

The second distinctive fact belongs to the mobility side: a ride-hailing or micromobility product runs on a workforce it insists it does not employ, and that classification question, worker or contractor, has already reached a final answer in some courts and is still open in others. The answer changes cost structure, scheduling rules, and what the product may lawfully do with a driver's time.

## Questions a PM must ask

1. Is the feature safety-relevant under a recognized functional-safety framework, and what safety level applies? The classification, not the team's intuition, decides how much review the change needs before it ships.
2. Does this change require re-approval from a type-approval or homologation authority? A vehicle already certified can be decertified by a change nobody flagged as safety-relevant.
3. Can this software be updated over the air, and is the update process itself certified under a recognized software-update management framework? Regulators increasingly treat the update pipeline as part of the vehicle, not a separate IT system.
4. In which jurisdictions are drivers or riders classified as workers, contractors, or something else, and what does that classification require of the product? A scheduling or pay feature fine in one country can be an unlawful working-time violation in another.
5. What is the insurance and liability position if this feature contributes to a collision? A routing choice, an assist feature, or a fee structure that pressures speed can sit inside a liability claim years later.
6. What does the vehicle or app do when connectivity drops mid-trip? A fare calculation or safety feature that silently fails offline is a safety gap wearing a UX label.
7. What is the disengagement or override story for any automated driving feature, and who is accountable for the seconds around a handoff? The handoff moment is where most serious automation incidents concentrate.
8. What happens to utilization and safety numbers during subsidized growth? A discounted market-entry period can make unit economics and safety metrics both look better than the steady state that follows.

## Gatekeepers

- **The type-approval or homologation authority.** Regimes such as the EU's vehicle type-approval framework, or national self-certification regimes elsewhere, gate whether a vehicle, and a change to it, may legally be sold or driven.
- **A functional-safety assessor.** ISO 26262 assessments set the safety level for any feature touching vehicle control, and a minor over-the-air change to a safety-relevant system is a regulated change, not a patch.
- **The cybersecurity and software-update auditor.** UNECE regulations on vehicle cybersecurity and on software-update management require an audited management system as a condition of type approval in markets that adopted them, tying your engineering process to a certification.
- **National and municipal transport authorities.** Ride-hailing and micromobility operate under city or state permits, driver licensing and background-check rules, and sometimes fleet caps, all negotiated locally rather than globally.
- **Labor courts and employment regulators.** Driver classification, argued to a final answer against Uber by the UK Supreme Court in 2021, can change cost structure and scheduling obligations overnight wherever a similar case lands next.
- **Motor insurers.** Mandatory-insurance regimes and an insurer's own risk appetite decide which vehicles and features may legally operate, and at what premium, independent of what the product team believes is safe.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Disengagement rate (automated driving) | How often a human had to intervene | Defined and measured by the operator, so cross-company comparisons are close to meaningless without a shared test-mile mix |
| Distance between safety-relevant incidents | Real-world safety performance | Easy suburban miles versus dense urban miles change the difficulty of the denominator enormously |
| OTA update success and rollback rate | Fleet software reliability | A successful flash is not the same as correct behavior afterward; a regression can post-date the metric that called it a success |
| Time to re-homologation after a change | Regulatory cycle speed | Teams learn to route a change through a path that avoids triggering re-approval, a compliance risk dressed as efficiency |
| Driver or rider acceptance and cancellation rate | Marketplace reliability | An incentive-inflated acceptance rate looks identical to a genuinely reliable service until the incentive is removed |
| Vehicle utilization rate | Fleet efficiency | High utilization can mean too few vehicles for demand, which shows up in wait time rather than in this metric |
| Recall or campaign closure rate | Whether a known defect was fixed | Counted at owner notification rather than at the vehicle actually being fixed, so unreachable owners never close the loop |
| Safety-critical defect rate per vehicle-year | Field safety of the design | Warranty-window reporting undercounts issues surfacing after the vehicle is out of warranty or has changed hands |
| Cost per trip or ride | Marketplace unit economics | Investor-subsidized fares make unit economics look solved well before they actually are |

## Reading

- **ISO 26262**, functional safety for road-vehicle electrical and electronic systems, the standard behind every safety-level rating referenced in a vehicle safety case.
- **ISO/SAE 21434**, road-vehicle cybersecurity engineering, read alongside UN Regulation No. 155 on cybersecurity management systems, the pairing that makes vehicle cybersecurity a certification requirement rather than a best practice.
- **UN Regulation No. 156**, the software-update management system regulation, the instrument that makes over-the-air updates a regulated capability rather than a feature.
- **Uber BV v Aslam**, UK Supreme Court, 19 February 2021, holding Uber drivers to be workers entitled to minimum wage and paid leave. Read it as the shape of the argument; the same question is being relitigated elsewhere with different answers.
- **The Volkswagen emissions defeat-device case**, disclosed September 2015, the standing lesson that a hidden software mode built to satisfy a regulator's test becomes the regulator's problem, at enormous cost, the day it is discovered rather than the day it shipped.
- **California DMV's 2023 suspension of Cruise's autonomous-vehicle permit** after a pedestrian-dragging incident (verify specific dates before relying on them), the modern version of the same lesson for autonomy claims made in public before the safety case was fully proven.

**Conductor overlay:** this domain sharpens DEFINE-8 (both the regulated and, for automated-driving features, the AI overlay commonly fire together), DESIGN-4 (the premortem centers on safety-critical failure modes, not only project risk), DELIVER-6 (regulated overlay drift, as homologation status and driver-classification rulings shift under a live fleet), and OPERATE-9 (the kill condition is usually a safety incident, not a metric threshold).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (safety and latency requirements stated as numbered thresholds, not narrative), [release-readiness](../../templates/delivery/release-readiness.md) (homologation and safety sign-off as go or no-go rows), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (connectivity loss and handoff moments as named scenarios with owners), and [risk-register](../../templates/execution/risk-register.md) (safety and classification risk carried alongside delivery risk).
