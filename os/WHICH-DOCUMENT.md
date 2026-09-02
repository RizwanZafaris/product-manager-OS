# Which Document

Before you fill anything in, decide how much document this decision deserves. Most teams own one PRD template and use it for everything, so a two-day change gets a twelve-section spec and a two-quarter platform bet gets the same twelve sections, which means neither gets the attention it needed. The weight is a choice. This file makes it an explicit one.

Three questions decide it. Answer them in this order.

1. **Stakes.** What does being wrong cost: an afternoon, a sprint, a quarter, a license?
2. **Audience.** Who has to read this and act on it: you and one engineer, a squad, five functions, a sponsor who signs, a regulator who audits?
3. **Reversibility.** Can you undo it in a day with a flag, or does it set data models, contracts, or public commitments that outlive the team?

Low stakes plus a small audience plus easy reversal means write less. Any one of them going high raises the weight by one step. Two of them going high raises it by two.

## The five weights

```
decide and log        -> reversible, no build, one or two people
ticket only           -> one sprint or less, one team, flag-reversible
one-pager             -> a few sprints, one squad plus a stakeholder or two
full PRD              -> a quarter or more, several functions, a sponsor signs
BRD + PRD + FRD       -> funding decision, contracts, or a regulator in scope
```

| Weight | Use it when | The artifact | What it costs you |
|---|---|---|---|
| Decide and log | The decision is reversible and needs no build, but someone will ask why in six months | One entry in [decision-log.md](../templates/execution/decision-log.md) | Ten minutes |
| Ticket only | Scope fits a sprint, one team owns it end to end, a flag turns it off | Your tracker, plus acceptance criteria pasted from [acceptance-criteria.md](../templates/definition/acceptance-criteria.md) | An hour |
| One-pager | Real user-facing change, one squad, a stakeholder or two who must not be surprised | [one-pager.md](../templates/definition/one-pager.md) | Half a day |
| Full PRD | Multiple functions, a quarter or more of work, a sponsor who signs at Gate 2 | [prd.md](../templates/definition/prd.md), plus FRD and NFR where the detail is load-bearing | Days, spread over the DEFINE stage |
| BRD, PRD, FRD stack | Money is being allocated, external contracts are signed, or a regulator can ask for the file | [brd.md](../templates/definition/brd.md), then [prd.md](../templates/definition/prd.md), then [frd.md](../templates/definition/frd.md) | A DEFINE stage of its own |

## The tree

```
Does anything get built?
  no  -> decide and log
  yes -> Can one team ship it inside a sprint, behind a flag?
           yes -> ticket only, with acceptance criteria attached
           no  -> Does a named sponsor have to sign, or do three or more
                  functions have to agree?
                    no  -> one-pager
                    yes -> Is funding, a contract, or a regulator in scope?
                             no  -> full PRD
                             yes -> BRD + PRD + FRD stack
```

## Overlays sit on top of the weight, not inside it

The weight decides how much specification. The overlays decide what extra questions get answered, and they apply at every weight above ticket-only.

- **The product contains a model.** The AI overlay attaches: eval sets replace prose acceptance criteria, starting at [eval-spec.md](../templates/ai/eval-spec.md). A one-pager with a model in it still needs an eval row; "the summaries should be accurate" is not a criterion.
- **A financial or data regulator governs the product.** The regulated module governs and its own template is used as shipped. See [modules/regulated/README.md](../modules/regulated/README.md). A regulated feature never runs at ticket weight, whatever its size.

## Documents that live around the weight ladder

The ladder above sizes the DEFINE artifact for one decision. The documents below attach to a trigger, a recurring moment or a question, rather than to a weight. When one of them references the decision you are specifying, its depth follows the weight you chose above: a ticket-weight change gets one line in the comms plan, a BRD-weight bet gets its own.

Upstream, before any single decision is worth weighing:

| Trigger | Document |
|---|---|
| Someone asks where this product is going, and the roadmap is the wrong answer | [vision.md](../templates/planning/vision.md), then [product-strategy.md](../templates/planning/product-strategy.md) for the bets behind it |
| Teams are optimizing five private definitions of winning | [north-star-metric.md](../templates/planning/north-star-metric.md) |
| Nobody can say in one sentence why a buyer picks you over the named alternative | [positioning.md](../templates/planning/positioning.md) |
| Price came from a meeting, not a document | [pricing-packaging.md](../templates/planning/pricing-packaging.md) |
| An idea wants discovery time and has not earned it | [opportunity-assessment.md](../templates/discovery/opportunity-assessment.md), the go or no-go before the weight question even applies |
| A partnership is on the table and nobody has written the go or no-go | [partner-integration-brief.md](../templates/planning/partner-integration-brief.md), at one-pager weight; the decision lands in the decision log |
| Research happened and lives in seven heads | [discovery-synthesis.md](../templates/discovery/discovery-synthesis.md) |
| You know who the user is but not the progress they are hiring for | [jtbd-spec.md](../templates/discovery/jtbd-spec.md) |
| The org decides by narrative, working backward from launch | [prfaq.md](../templates/definition/prfaq.md), a DEFINE front door at one-pager to PRD weight |
| A decision could be bought with data instead of argued | [experiment-brief.md](../templates/operate/experiment-brief.md), usually at ticket weight |

Downstream, once something is being built and shipped:

| Trigger | Document |
|---|---|
| The PRD names metrics and nothing emits the events to compute them | [analytics-instrumentation-spec.md](../templates/delivery/analytics-instrumentation-spec.md), written before BUILD starts |
| More than two audiences must hear different things at different times | [launch-comms-plan.md](../templates/delivery/launch-comms-plan.md); below that bar, the release-readiness comms table suffices |
| A launch happened and the team is already on the next thing | [post-launch-review.md](../templates/operate/post-launch-review.md), once, within six weeks |
| A deal was won, lost, or died of no decision | [win-loss-review.md](../templates/operate/win-loss-review.md) |
| Leadership needs the metrics review they will actually read | [qbr-board-update.md](../templates/operate/qbr-board-update.md), quarterly |
| Gate 6 said sunset | [sunset-eol-plan.md](../templates/operate/sunset-eol-plan.md) |

## Four documents you will be asked for by name

These arrive as requests, usually from outside product, and none of them is a template here, because each is already served by documents that exist. Route them; do not build them.

- **MRD (market requirements document).** The market half is the [discovery document](../templates/discovery/discovery-document.md), the bet half is the [opportunity assessment](../templates/discovery/opportunity-assessment.md). Filled together they answer everything an MRD asks, without maintaining a third document that drifts from both.
- **Business case.** The [BRD](../templates/definition/brd.md) is the business case: objectives, ROI, constraints, a sponsor who signs. If someone wants "the business case" as a separate artifact, hand them the BRD's first two sections.
- **Sales enablement one-pager.** An output, not a template: derive it from [positioning.md](../templates/planning/positioning.md) plus the sales row of the [launch comms plan](../templates/delivery/launch-comms-plan.md). If it says anything those two do not, one of the three is wrong.
- **Stakeholder newsletter.** A cut-down of the [QBR update](../templates/operate/qbr-board-update.md): headline, wins, asks. Never compute a number for the newsletter that the metrics review does not already hold.

## Rules

1. **Delete what you do not need.** Every template here is a superset. An empty section is worse than no section: it reads as an unanswered question and it trains readers to skim. Delete the sections that do not apply, or write "N/A because <reason>". Never leave the heading standing over white space.
2. **Customize the top three fields first.** Every template's header comment names the fields that carry the document. Fill those, then decide whether the rest earns its space.
3. **Upgrading is normal, downgrading is a decision.** A ticket that grows into a quarter gets promoted to a one-pager or a PRD, and the promotion is logged. Cutting a PRD down to a one-pager mid-flight is also allowed, and also logged, because someone signed the heavier version.
4. **The gate does not change with the weight.** Gate 2 in [STAGE-GATES.md](STAGE-GATES.md) asks the same questions of a one-pager and a full PRD: does every requirement have a pass condition, does every assumption have an owner. A lighter document answers them in fewer words, not in fewer answers.
5. **When two answers are defensible, take the lighter one and say so.** Write one line in the decision log naming the weight you chose and why. If the choice was wrong, that line is what tells the next person where the gap came from.
