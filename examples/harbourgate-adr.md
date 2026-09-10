# ADR 0003: Route every card payment through Kestrel from Quay and retire the Marlowe and Tidewater integrations

Fills [templates/architecture/adr.md](../templates/architecture/adr.md). Everything here is invented: Harbourgate is a fictional mid-market retailer, Kestrel, Marlowe and Tidewater are fictional payment providers, Quay is the fictional payment service this ADR creates, every person is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from the shared data sheet in the [Harbourgate journey](harbourgate-journey.md) rather than from any real payments stack. See the [examples index](README.md).

Stage: DESIGN, feeds Gate 3
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [architect agent](../agents/architect-agent.md)

**Status:** Accepted · **Date:** 2026-04-09 · **Deciders:** Ife Adeyemi, Product Manager; Tomasz Wierzbicki, Engineering Lead

## Context

checkout-pay reaches three card providers, each bolted on at a different time: Kestrel for the web in 2017, Marlowe in 2019 as a second acquirer with a cascade rule (BR-008) that retries Kestrel declines through it, and Tidewater in 2021 for the 61 kiosk PIN pads, through a wrapper written by a contractor who left the same year and whose replacement has never been named. Kestrel already carries 58% of orders reaching the payment step, Marlowe 27%, Tidewater's kiosks 15% (N12). Marlowe logs no declines at all, and the wrapper's log files were found at the 2026-04-08 STRIDE walk to hold the masked PAN and cardholder name in plain text (F1, which became R8). Separately, nobody owns the wrapper when it misbehaves: that is R2, raised at today's premortem and scored 6 (L3 x I2), one of the register's joint-highest scores, and it has sat unowned since the contractor left in 2021. The wrapper's client certificate also expires 2027-02-03 (N66, read by Hamid Qureshi on 2026-04-08), which is a renewal nobody has an owner to carry out, and one more reason to retire the wrapper rather than keep it. Kestrel's contract carries a 99.9% monthly availability commitment (N26); Marlowe's carries 99.5% (N27); Tidewater's 2021 contract carries no SLA clause at all (N28). Seven systems sit inside PCI DSS assessment scope today because the Marlowe path carries the card number through Harbourgate's own servers (N55). Gate 2 was signed on 2026-04-07 against a decline-rate baseline that must not get worse per provider (N13 to N15), which means whatever we build has to be provably at least as good as what it replaces, per provider, not just in aggregate. Quay, the separate payment service of ADR-0001, is where that connector will live. The engineering team's first instinct, reachable within the existing contracts and requiring no new merchant relationship, was a routing layer in front of all three providers rather than choosing one.

## Decision

We will build Quay's connector to route every card payment, web, app and kiosk, through Kestrel, and retire the Marlowe and Tidewater integrations rather than keep either behind a routing layer.

## Consequences

- One settlement file format, one decline vocabulary, one on-call surface and one provider contract to operate, instead of three. PCI DSS assessment scope is a target of 3 systems once the sunset completes and an external assessor confirms it (N55); today it is 7, and the reduction is not yet an assessed fact.
- Retiring Marlowe removes BR-008, the 2019 cascade rule that retries a Kestrel decline through Marlowe. The cascade is a second automatic authorisation path, the kind of retry path the premortem's R1 names. Once BR-008 goes, BR-001 (offer one retry with a different method, never re-submit the same card automatically) becomes the only retry behaviour left on a decline, with nothing to fall back on.
- A single provider is a single point of failure: an outage at Kestrel would stop every card payment on every surface, web, app and kiosk together, where before an outage at one provider left the other two trading. This is R4, scored 3 (L1 x I3) at today's premortem. It is named here, not hidden inside a consequence nobody reads, and it needs an accountable acceptor before the first provider moves; none is named yet.
- Kestrel's terminal SDK supports the kiosk PIN pad model, pending certification (DEP-1, needed by 2026-07-20), and the kiosk firmware also needs updating across all 61 shops (R12). Until both land, Tidewater's wrapper, the component nobody could name an owner for, cannot be retired.
- The legacy table shape has to keep being written by Quay for reporting, finance reconciliation and the order-history page (ADR-0002); this becomes R5 (a change to that shape breaks reporting, finance reconciliation or the order-history page). The two retired integrations' settlement and refund tails also have to be reconciled against Quay's own ledger until each retired provider's in-flight settlements and refunds have cleared, once each provider's traffic moves; no register row for that reconciliation work exists yet.
- The migration needs a temporary legacy adapter and a routing switch that can move traffic from the legacy path to Quay's Kestrel connector; the ramp mechanism is a later build decision, and the scaffolding is retired once the legacy path carries no traffic. It is migration scaffolding, not the routing layer rejected below, and it does not reopen that option.
- Retiring Marlowe and Tidewater creates follow-on work with no register home yet: the 90-day contract termination notices, the refund tail on legacy-authorised orders, and the PCI re-assessment that would confirm the scope reduction above. This work seeds a sunset plan still to be written.
- Consolidating onto one provider also closes off having a second acquirer to fail over to, and weakens Harbourgate's negotiating leverage when Kestrel's contract next comes up for renewal.
- Cost moves with volume rather than with integration count: blended card processing cost is estimated to fall from 1.38% of card value to 1.29% once consolidated onto Kestrel's interchange-plus schedule (N56), but that estimate is not the reason for this decision and is not re-argued here; it is recorded because a reader who checks the data sheet should find the same number (N56), not a different one invented for this document.

---

## Rejected option: keep all three providers behind a new routing layer

A new wrapper over Kestrel, Marlowe and Tidewater together, replacing the contractor's Tidewater-only wrapper with a supported one and gaining the ability to send any order to any acquirer, was the engineers' first instinct. It lost on operational risk. Keeping three providers behind one layer means three settlement file formats, three decline vocabularies, three on-call surfaces and three contracts, forever, bought in exchange for a routing flexibility that the evidence already available today argued against: the 2019 cascade rule was exactly that flexibility, applied to two providers, and today's premortem raised R1, a shadow-comparison retry authorising the same card twice, as a medium (score 4, L2 x I2) precisely because that kind of flexibility invites exactly this failure. The wrapper itself is the second argument: a wrapper is what an integration becomes when it is nobody's, and Tidewater's has gone without a named owner since the contractor left in 2021, a gap that has no named owner today. Building a second, larger wrapper on the same pattern the team is actively trying to retire was rejected as repeating the failure mode rather than fixing it. This option reopens if Kestrel misses its availability commitment (N26, 99.9% monthly) in any month, or if an R4 outage stops card payments on any surface; the decision to reopen it sits with whoever is named to accept R4, at the next scheduled review. Until then it stays rejected, not merely unconsidered.

## Exit gate

- [x] The title states the decision, not the topic: "Route every card payment through Kestrel from Quay and retire the Marlowe and Tidewater integrations", not "Payment provider architecture"
- [x] Status, date, and deciders are filled in: Accepted, 2026-04-09, Ife Adeyemi and Tomasz Wierzbicki
- [x] Context explains the forces, not just the requirement: the per-provider volume and SLA split, the wrapper's ownership gap and certificate expiry, the decline-baseline constraint from Gate 2, and the routing layer as the team's own first instinct
- [x] The decision is one or two sentences in active voice: "We will build Quay's connector to route every card payment... through Kestrel, and retire the Marlowe and Tidewater integrations"
- [x] At least one negative consequence is recorded: the single point of failure (R4), the reconciliation burden while legacy settlements and refunds clear, BR-008's removal leaving BR-001 to carry the whole retry story alone, and the PCI scope reduction being a target rather than an assessed fact
- [x] If this supersedes an earlier ADR, that ADR's status line now points here: not applicable; ADR-0003 supersedes no earlier record, and none has superseded it

Reviewed at [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md) and accepted 2026-04-10, with one miss recorded against the whole design set: the wrapper had no named owner, and Tomasz Wierzbicki was to name one by 2026-04-24. Signed off by Tomasz Wierzbicki, Engineering Lead and design owner, as the decider who commits the team to Kestrel as the routing target. See the [Harbourgate journey](harbourgate-journey.md) for how this decision reached Gate 3 and for the same rejected option retold in the wider narrative.

### Later history (added after acceptance; not part of the decision)

Nothing below changed the decision above. It is recorded here, dated, because a reader following this ADR forward should be able to find out what happened without mistaking hindsight for the reasoning of 2026-04-09.

- 2026-04-14: D-011 ramps the new path by traffic percentage with a shadow comparison.
- 2026-04-24: R2 (the unowned wrapper) closes; Bea Lindqvist is named caretaker.
- 2026-05-19: R1 occurs, a shadow-comparison retry authorising the same card twice.
- 2026-05-21: D-017 replaces the shadow-comparison ramp with a per-provider flag, closing R1.
- 2026-06-19: ADR-0004, born from incident HG-INC-14, sets how both paths reconcile from one ledger for the length of the drain.
- 2026-07-09: DEP-1 (Kestrel terminal SDK certified for the kiosk PIN pad model) delivers.
- 2026-07-20: BR-008 retires once Marlowe's traffic reaches 100%.
- 2026-07-30: R12 (kiosk firmware) closes via DEP-5.
- 2026-08-24: D-022 records Rohan Iyer accepting R4 by name, alongside the kiosk fallback (N31), the peak change freeze (N64) and a review the decision log calls quarterly. The risk register instead carries a fixed revisit date, 2027-01-31, for the same acceptance; the two do not agree, and that mismatch belongs to the underlying data sheet rather than to this ADR.

