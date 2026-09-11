# Failure Scenarios: Fernrow Logistics cross-border and last-mile network

Fills [templates/delivery/failure-scenarios.md](../templates/delivery/failure-scenarios.md). Everything here is invented: Fernrow Logistics is a fictional last-mile and cross-border parcel network, the people are roles filled by invented names, and every number, name and date is ILLUSTRATIVE, drawn from the Fernrow data sheet used across this example rather than from any real carrier, broker or customs authority. See the [examples index](README.md). Regulatory statements are current as of 2026-09-11, are not legal advice, and should be confirmed with counsel before any commitment.

**Owner:** Priya Nandakumar, head of network operations · **Reviewed with:** Owen Bradley, on-call lead · **Date:** 2026-09-11

This document fills the failure-scenarios template for a logistics network, where the exception path is the product: the happy path needs no scenario, and the rows below concentrate on the exception types the [logistics domain card](../knowledge/domains/logistics.md) names as where software earns its keep or gets replaced by a phone call. Sourcing follows the card's gatekeepers (transport regulators, customs authorities, shipper compliance programs, insurers) and its metrics (OTIF, first-attempt delivery rate, exception rate by type, route density).

## 1. Scenario table

Detection means how Fernrow knows within minutes without a customer telling us. Where the honest answer is a customer report, section 2 records the gap. Recovery names steps, an owner and a time estimate.

| ID | Scenario | Blast radius | Detection | Recovery | Data loss risk |
|---|---|---|---|---|---|
| FS-4 | Customs broker's entry-filing API times out during a cross-border batch | All shipments in that day's cross-border batch sit uncleared at the border; no delivery-window promise can be made for the affected lane until filing clears | Filing-success rate alert below 90% over 15 minutes | Fail over to the broker's manual portal for the batch; owner: cross-border ops lead; expected 45 minutes to re-file | None, filed data is durable; delivery-window promises already sent to customers are stale and must be reissued |
| FS-1 | Carrier capacity collapse on a peak day (contracted linehaul and last-mile partners cannot cover the day's volume) | Same-day and next-day promises on the two densest metro lanes miss; depot docks back up; OTIF against retail scorecards degrades for the peak week | Capacity utilisation dashboard above 95% with unassigned route count rising over 30 minutes | Activate the spot-carrier bench and shift volume to pickup points; owner: network capacity lead; expected 4 hours to re-cover the day, 24 hours to clear the backlog | None; route assignments are re-routable, and no consignment data is lost |
| FS-2 | Bad address data causing failed deliveries | First-attempt delivery rate falls; failed attempts concentrate in new-build and cross-border zones where the address string does not resolve to a geocode | Failed-attempt rate by zone rises above baseline for 1 hour, plus geocode-failure count at scan-in | Route to the address-repair queue, attempt a geocode match, dispatch to a neighbour or pickup point where the customer consents; owner: last-mile ops lead; expected 2 hours to resolve the day's flagged stops | None; the failed attempt is recorded and the consignment is re-tendered |
| FS-3 | Proof-of-delivery disputes (customer claims non-delivery where a POD exists or is missing) | Claims cost, retail chargebacks and shipper-confidence damage on the affected accounts | Claims dashboard above threshold, or a shipper scorecard chargeback notice; often first seen as a customer report | Pull the POD record (signature, photo, GPS timestamp), reconcile against the depot scan trail, and where the POD is missing re-drive or settle; owner: claims and compliance lead; expected 5 working days per dispute | Possible: POD photograph or signature not captured at the door for the affected stop |
| FS-5 | Courier app offline in dead zones | Couriers in low-coverage zones cannot scan, capture POD, or receive route updates; stops are done but records are delayed | Courier app heartbeat gap above 15 minutes for a route, or a cluster of late scan events at depot sync | Fall back to offline scan-and-cache mode, then bulk-sync at depot; where the courier cannot use the app at all, paper manifest and manual depot entry; owner: field technology lead; expected 1 hour after coverage returns to sync the route | Possible: scan events held on device are lost if the device fails before sync |
| FS-6 | Depot sort-machine outage | The affected depot's sort throughput drops; downstream linehaul misses its departure window; OTIF for the depot's outbound lanes degrades | Sort-machine fault alarm and throughput-below-threshold alert on the depot control screen | Switch to manual sort lanes with the cross-trained sort team, prioritise the earliest linehaul departures; owner: depot operations lead; expected 3 hours to restore nominal throughput, with a 6-hour backlog tail | None; sort state is a physical position, not a data record |

The FS-4 row is carried unchanged from the [logistics domain card](../knowledge/domains/logistics.md) because the customs hold is the archetypal exception the card names: customs holds are data-quality failures wearing a uniform, and the manual portal fallback is the designed non-software path. The remaining rows extend the same shape to the other exception types the card's metrics track (capacity utilisation, first-attempt delivery rate, exception rate by type).

## 2. Monitoring gaps found while writing this

Writing the table surfaced one gap that has been open since the network launched: exception-queue age was never measured by exception type. Fernrow measured a single overall exception count, which the domain card warns hides that one type causes most of the phone calls. The gap below records that and the fixes the table rows depend on.

| Gap | Fix | Owner | Date |
|---|---|---|---|
| Exception-queue age is not measured by exception type; only an overall exception count exists, so the network cannot tell which exception type drives the phone calls | Add a per-type exception-age metric to the ops dashboard, split by the types in section 1 | Priya Nandakumar | 2026-10-09 |
| POD capture has no completeness alert; a missing POD is only found when a dispute is raised (often a customer report) | Add a POD-completeness alert per route and per depot, feeding the claims dashboard | Claims and compliance lead | 2026-10-23 |
| Courier app heartbeat gaps are not alerted; a dead-zone route is currently discovered at depot sync | Add a heartbeat-gap alert above 15 minutes per active route | Field technology lead | 2026-10-16 |

## 3. Rehearsal

- Scenarios rehearsed (game day or tabletop), with dates: FS-4 cross-border filing failover, tabletop, 2026-08-14; FS-6 depot sort-machine outage, game day at the north depot, 2026-07-22
- The scenario we most doubt our recovery steps for: FS-1 (carrier capacity collapse on a peak day), because the spot-carrier bench has never been tested at peak volume and the four-hour recovery estimate assumes bench depth the network has not verified under a real peak-week load

## Exit gate

This document passes when:

- [x] Every external dependency has at least one scenario row. FS-4 covers the customs broker's filing API; FS-1 covers contracted and spot carriers; FS-5 covers the courier connectivity dependency. As of 2026-09-11, confirm the live status of any regulatory dependency with counsel before treating this row set as complete.
- [x] Every row states detection, and "customer report" answers created a section 2 gap. FS-3's detection row names a customer report as one path, and the POD-completeness gap in section 2 is the resulting monitoring gap.
- [x] Every recovery names an owner and a time estimate, not just steps. Each of FS-1 to FS-6 carries a role owner and an expected recovery time.
- [x] Data loss risk is stated per row, including "none". FS-1, FS-2, FS-4 and FS-6 state none; FS-3 and FS-5 state possible data loss with the affected data named.
- [x] At least the highest blast-radius scenario has a rehearsal date. FS-4, the highest blast-radius row (an entire cross-border batch), was rehearsed 2026-08-14.

Signed: Priya Nandakumar, head of network operations, 2026-09-11, reviewed with Owen Bradley, on-call lead, 2026-09-11.
