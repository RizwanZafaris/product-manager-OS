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

**Adjacent industries:** automotive retail (dealer management systems, car marketplaces, online car buying, finance and insurance) reads this card for the vehicle and [Lending and credit](lending-credit.md) and [Marketplaces](marketplaces.md) for the deal. Dealer franchise laws in many US states restrict or bar manufacturers from selling direct, so the dealer is both customer and gatekeeper to the buyer. Dealer-arranged finance is regulated consumer lending (ECOA, TILA, scrutiny of dealer markup). Title, registration and DMV integrations differ by state, and used-car disclosure and advertised-price rules are enforced under state consumer-protection law (the FTC's CARS Rule was vacated in 2025). Rail signalling software reads this card's functional-safety material under rail's own standard (CENELEC EN 50716, which replaced EN 50128); rail freight reads [Logistics](logistics.md) and passenger ticketing reads [Travel and hospitality](travel-hospitality.md). As of 2026-09-11; verify and confirm with counsel.

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

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays: an automated-driving or driver-facing model fires the AI overlay, and the regulated overlay fires only where a financial or data regulator also applies to that model, per the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); vehicle type approval is not what the regulated module covers), DESIGN-4 (the premortem centers on safety-critical failure modes, not only project risk), DELIVER-6 (regulated overlay drift, as homologation status and driver-classification rulings shift under a live fleet), and OPERATE-9 (the kill condition is usually a safety incident, not a metric threshold).

**Templates this bends:** [nfr](../../templates/definition/nfr.md) (safety and latency requirements stated as numbered thresholds, not narrative), [release-readiness](../../templates/delivery/release-readiness.md) (homologation and safety sign-off as go or no-go rows), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (connectivity loss and handoff moments as named scenarios with owners), and [risk-register](../../templates/execution/risk-register.md) (safety and classification risk carried alongside delivery risk).

**Filled in this repo:** [domain-automotive-mobility-risk-register.md](../../examples/domain-automotive-mobility-risk-register.md) fills the [risk-register](../../templates/execution/risk-register.md) template directly for this domain, for Calderun Systems, a Tier-1 supplier shipping an over-the-air lane-assist update: the steering-torque limiter row that engineering called a tuning change and the assessor reclassified as ASIL C under ISO 26262, which triggers UN Regulation No. 156 software-update management, plus UN R155 cybersecurity-management evidence and one risk accepted by name at executive level, the discipline question 5's liability question asks for. For the other three bent templates, [harbourgate-nfr.md](../../examples/harbourgate-nfr.md) and [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md) remain the nearest reading, for a numbered, re-signed threshold and a named go or no-go sign-off table, though both are payments examples with no functional-safety level or homologation clock. [harbourgate-failure-scenarios.md](../../examples/harbourgate-failure-scenarios.md) exists but is a payments outage set, not a connectivity-loss or handoff scenario.

**Worked example (ILLUSTRATIVE):** a slice of a [risk-register](../../templates/execution/risk-register.md) row, in the sourced, dated style of [harbourgate-risk-register.md](../../examples/harbourgate-risk-register.md), for a lane-assist feature update (question 1 and question 3 above).

| Risk | Classification | Owner | Mitigation | Status |
|---|---|---|---|---|
| OTA update to lane-assist steering-torque limiter, flagged by engineering as a tuning change, not a safety change | ASIL C under ISO 26262 (assessor finding, overturns the engineering team's own classification), which triggers UN Regulation No. 156 software-update-management review before rollout | Head of Functional Safety, ILLUSTRATIVE name J. Okonkwo | Re-classify the change as safety-relevant; hold the fleet rollout for a full ISO 26262 change-impact assessment and, if the assessor confirms ASIL C, re-homologation before any vehicle receives the update | Accepted as blocking by the CTO on 2026-03-12 (ILLUSTRATIVE); fleet rollout held pending assessor sign-off |

This is question 2's warning in a single row: a change the team read as a tuning tweak becomes, once classified, an event that can require re-approval before an already-sold fleet may legally receive it.
