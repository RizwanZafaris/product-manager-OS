# The PM and PMM Boundary

Product management decides what to build and why; product marketing decides how the market will understand it and equips the people who sell it. Both jobs claim the customer, the segment, and the launch, which is why this boundary produces more quiet duplication and louder turf disputes than any other pairing in the building. This card states a workable default split. Your company will differ; the point is to differ in writing.

## Frontloaded and backloaded

The two roles concentrate their effort at opposite ends of the lifecycle. The PM's heaviest lifting is frontloaded: discovery, definition, and the gates before code, where being wrong is still cheap. The PMM's heaviest lifting is backloaded: positioning applied, messaging built, sales equipped, adoption pushed, around launch and after.

Concentrated is not confined. The failure this framing warns against is the launch-day handoff: product tosses a finished thing over the wall and marketing meets it cold. A PMM who first sees the product at DELIVER writes positioning by archaeology. The cheap fix is standing presence: PMM reads the [discovery document](../../templates/discovery/discovery-document.md) and sits in on Gate 2; the PM reviews the positioning and stays on the field through launch metrics.

## Who decides what

| Decision | Default owner | The other side's part |
|---|---|---|
| What to build, and why now | PM | PMM supplies market and competitive evidence |
| Roadmap and sequencing | PM | PMM flags market timing windows |
| Target user of the product | PM | PMM tests whether that segment can be reached and named |
| Market category and positioning | PMM | PM keeps claims inside what the product truly does |
| Messaging and naming | PMM | PM reviews for accuracy, not for taste |
| Pricing and packaging | Shared | PM owns the value metric; PMM owns competitive framing; the tiebreaker gets a [decision log](../../templates/execution/decision-log.md) entry |
| Launch timing and tier | Shared | PM certifies readiness; PMM certifies the market moment |
| Sales enablement and analyst material | PMM | PM supplies the substance and checks the claims |
| Win-loss analysis | PMM runs it | PM consumes it as discovery evidence |

## Documents each side owns

The PM side of the boundary lives in this repository: the [discovery document](../../templates/discovery/discovery-document.md), [PRD](../../templates/definition/prd.md), [roadmap](../../templates/planning/roadmap.md), and the [GTM plan](../../templates/planning/gtm-plan.md), which is deliberately a product document: first cohort, channel evidence, launch metric, stop condition.

The PMM side produces the positioning document, the messaging guide, the sales enablement one-pager, and the launch communications plan. This repository ships the first and last as [positioning](../../templates/planning/positioning.md) and the [launch comms plan](../../templates/delivery/launch-comms-plan.md); [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) routes the rest. A PMM document that contradicts the PRD's stated scope is a defect, and lint will not catch it; only the standing-presence habit above does.

## The boundary is fuzzy, and that is not the problem

At a startup one person does both jobs, usually the PM or a founder, and the split above is a checklist of hats rather than an org chart; see [stage-shift.md](stage-shift.md). At scale the split staffs out, and where exactly pricing or the beta program lands varies by company, by category, and by the personalities involved. None of that is pathological.

The pathology is the unwritten boundary. Every dispute filed as "PMM is overstepping" or "product will not share" is really the absence of a page saying who decides. The remedy costs one hour: put both names in the [stakeholder map](../../templates/execution/stakeholder-map.md), assign each row of the table above, and log the assignments in the [decision log](../../templates/execution/decision-log.md). Revisit when either seat changes hands, because the boundary is partly a treaty between two specific people.

## Sources

- April Dunford, Obviously Awesome (2019): positioning as a deliberate, cross-functional choice built from competitive alternatives and provable value, not a tagline exercise; the reason positioning sits with PMM but cannot be done without the PM in the room.
- Marty Cagan, SVPG essays on product versus product marketing: the what-and-why versus go-to-market division this card's table starts from. See [empowered product teams](../cagan-product-teams.md) for the viability risk that PM retains either way.
