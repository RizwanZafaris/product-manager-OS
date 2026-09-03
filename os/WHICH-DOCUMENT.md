# Which Document

Before you fill anything in, decide how much document this decision deserves. Most teams own one PRD template and use it for everything, so a two-day change gets a twelve-section spec and a two-quarter platform bet gets the same twelve sections, which means neither gets the attention it needed. The weight is a choice. This file makes it an explicit one.

Three questions decide it. Answer them in this order.

1. **Stakes.** What does being wrong cost: an afternoon, a sprint, a quarter, a license?
2. **Audience.** Who has to read this and act on it: you and one engineer, a squad, five functions, a sponsor who signs, a regulator who audits?
3. **Reversibility.** Can you undo it in a day with a flag, or does it set data models, contracts, or public commitments that outlive the team?

Low stakes plus a small audience plus easy reversal means write less. Any one of them going high raises the weight by one step. Two of them going high raises it by two.

The order is not decoration. Stakes first, because it is the question people answer honestly before they have a document in mind. Reversibility last, because it is the one teams talk themselves out of: almost everything feels reversible in the week it is built, and the things that are not reversible are not reversible for reasons that show up later. If you find yourself arguing that a schema change is flag-reversible, you have answered question 3 with question 1's optimism.

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

## Seven routing cases, worked

Each case is a real-sounding request, the three questions answered, the weight, and what breaks at the weight next to it. All of them concern Ledgerline, the fictional invoicing product from [HOW-TO-RUN-A-PRODUCT.md](HOW-TO-RUN-A-PRODUCT.md), so the cases can be compared to each other.

**Case 1. "Change the invoice reminder default from 7 days to 5."**

Stakes: a sprint at most, and the number can be changed back. Audience: one squad, plus a line in the release notes. Reversibility: a config value. Nothing about the three answers goes high, and something does get built. **Ticket only**, with acceptance criteria attached. Written as a one-pager it would consume half a day producing sections about market context for a config default. Written with no artifact at all it would be fine until someone asks in March why reminders changed, which is what the log entry inside the ticket is for.

**Case 2. "Stop supporting invoices in the two currencies the bank feed cannot classify."**

Stakes: a sprint of engineering, and some existing customers lose a capability. Audience: one squad, plus support and the account manager for the affected accounts. Reversibility: the code is reversible; the customer conversation is not. Reversibility goes high on its own, so the weight rises one step from ticket. **One-pager**, whose most valuable section is the affected-account count, because that number is what stops the decision being reopened from memory every quarter. This is the case people route to ticket weight and then relitigate three times.

**Case 3. "Should the forecast screen show a chart or a table first?"**

Stakes: an afternoon of design. Audience: the PM and one engineer. Reversibility: a flag. Nothing goes high, and the honest answer is that this does not deserve a document at all. **Decide and log**, or a ticket if it is being built this sprint. The failure mode here is not over-documenting; it is a PM who feels a design decision deserves a written rationale and produces a one-pager that reads as if the choice mattered more than it did, which trains the squad to skim one-pagers.

**Case 4. "Build the two-week cash-flow forecast with model-generated explanations."**

Stakes: a quarter of engineering plus a bank-feed dependency. Audience: product, engineering, design, support, and a signing sponsor. Reversibility: it sets a data model and a provider contract. Two of three go high. **BRD plus PRD plus FRD stack**, which is what the walkthrough uses. Routed to full PRD instead, the missing artifact is the business case, and the specific loss is a sponsor who signs a process rather than a commitment; Gate 2's checklist asks for a signature on the BRD itself for exactly this reason. Routed to one-pager, the FRD's traceability disappears and BUILD starts negotiating requirements it cannot cite.

**Case 5. "Add a lending referral to the shortfall warning, paid on conversion."**

Stakes: revenue, a partner contract, and a regulatory question. Audience: five functions plus legal. Reversibility: a signed partner agreement and a public commitment on a money screen. All three go high, and one answer changes the shape rather than the size: a financial regulator may now be in scope. **BRD plus PRD plus FRD stack, plus the regulated module**, and the module attaches at Gate 2 rather than later, per [OPERATING-LOOP.md](OPERATING-LOOP.md). Note what a lighter weight would have hidden: the negative regulated determination recorded on Ledgerline's day one contains the sentence "makes no decisions about anyone's access to money", and this proposal breaks it. The weight question found the constraint because the file it points to was written down.

**Case 6. "Replace the forecasting model with a newer version from the same vendor."**

Stakes: forecast behavior across every account. Audience: engineering, product, and support, who will answer the tickets if outputs shift. Reversibility: pinning the old version back is a config change, so mechanically easy. Reversibility says light, stakes say heavy, and the tie is broken by a question the tree does not ask directly: does the product's behavior change when the model version changes? It does, so the AI overlay governs. **Ticket weight for the change, with the eval suite from [eval-spec.md](../templates/ai/eval-spec.md) run against the new version as its acceptance criteria.** The document is small and the gate is not. A team that reads "ticket only" as "no evidence needed" ships a model swap on a green build and a red eval, which the Gate 4 precedents in [STAGE-GATES.md](STAGE-GATES.md) name as the most common route from a green spec to a red launch.

**Case 7. "Marketing needs the market requirements document for the forecast launch."**

Nothing gets built by this request. Stakes: reputational and internal. Audience: marketing plus the sponsor. **No new weight at all**: this is a routing question, not a specification question, and the last section of this file answers it. The market half is the discovery document and the bet half is the opportunity assessment, both already filled. Producing a third document that restates them creates a fourth problem, which is three documents that disagree by next quarter.

## Reading the tree wrong

Four mistakes account for most bad routings, and each has a tell you can see without knowing the domain.

1. **Reversibility answered by the code.** "We can turn it off" is true of the feature and false of the data it wrote, the contract it signed, or the promise it made. Tell: the reversibility answer names a flag and the change touches a schema, a price, or an external party.
2. **Audience counted as attendees.** Five people in the kickoff is not five functions who must agree. Conversely, a change with two people in the room and a legal review afterward has a five-function audience. Tell: the audience answer lists names rather than functions and their decisions.
3. **Weight inflated by anxiety.** A PM new to an organization writes a PRD for a config change, because a document feels like proof of diligence. Tell: the artifact's first three sections say things nobody at the table disputes. Rule 5 below exists for this: take the lighter option and log why.
4. **Weight deflated by deadline.** The quarter is half gone, so the quarter-sized bet gets a one-pager. Tell: the one-pager has an out-of-scope section longer than its scope section, because the author is using the light artifact to hold back a heavy decision. That is the routing that produces the Gate 2 return, and the week it saves in DEFINE is paid back with interest in BUILD.

## Overlays sit on top of the weight, not inside it

The weight decides how much specification. The overlays decide what extra questions get answered, and they apply at every weight above ticket-only.

- **The product contains a model.** The AI overlay attaches: eval sets replace prose acceptance criteria, starting at [eval-spec.md](../templates/ai/eval-spec.md). A one-pager with a model in it still needs an eval row; "the summaries should be accurate" is not a criterion.
- **A financial or data regulator governs the product.** The regulated module governs and its own template is used as shipped. See [modules/regulated/README.md](../modules/regulated/README.md). A regulated feature never runs at ticket weight, whatever its size: this is the one place in this file where size does not decide. A three-line edit to a disclosure string is a small change and a regulated artifact at once, and the artifact is what a supervisor asks for two years later, when nobody can remember whether the wording was reviewed.

The distinction is worth holding precisely, because the two are often collapsed. Weight is a volume control on specification; an overlay is a set of questions that must be answered at any volume. Case 6 above is the clean illustration: a ticket-weight change carrying the AI overlay's full evidence requirement. The reverse error is more expensive: a heavy PRD stack that never routes its model behaviors into an eval spec is a large document with a hole in the middle, and the hole is exactly where a launch fails.

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

Two of these are dated rather than triggered, which is the distinction that decides whether they get written at all. The post-launch review has a window, once within six weeks, because after that the team's memory of the launch has been overwritten by the next launch and the review becomes a reconstruction. The instrumentation spec has a deadline in the other direction: before BUILD starts, because events added after launch have no baseline, and a Gate 6 comparing a number to nothing is the outcome the whole loop exists to prevent.

## Four documents you will be asked for by name

These arrive as requests, usually from outside product, and none of them is a template here, because each is already served by documents that exist. Route them; do not build them.

- **MRD (market requirements document).** The market half is the [discovery document](../templates/discovery/discovery-document.md), the bet half is the [opportunity assessment](../templates/discovery/opportunity-assessment.md). Filled together they answer everything an MRD asks, without maintaining a third document that drifts from both.
- **Business case.** The [BRD](../templates/definition/brd.md) is the business case: objectives, ROI, constraints, a sponsor who signs. If someone wants "the business case" as a separate artifact, hand them the BRD's first two sections.
- **Sales enablement one-pager.** An output, not a template: derive it from [positioning.md](../templates/planning/positioning.md) plus the sales row of the [launch comms plan](../templates/delivery/launch-comms-plan.md). If it says anything those two do not, one of the three is wrong.
- **Stakeholder newsletter.** A cut-down of the [QBR update](../templates/operate/qbr-board-update.md): headline, wins, asks. Never compute a number for the newsletter that the metrics review does not already hold.

The rule underneath all four: a derived document must contain no number and no claim that its source does not. The moment it does, you own two documents that disagree, and the one that gets read by the person making a decision is the one that was easiest to open. Route the request to the source, or produce the derivative and cite the source line by line so the drift is visible when it starts.

## Rules

1. **Delete what you do not need.** Every template here is a superset. An empty section is worse than no section: it reads as an unanswered question and it trains readers to skim. Delete the sections that do not apply, or write "N/A because <reason>". Never leave the heading standing over white space. The "because" is the part that earns its space: a reader who disagrees with the reason knows to reopen the section, and a reader facing a bare "N/A" cannot tell whether it was considered or dodged.
2. **Customize the top three fields first.** Every template's header comment names the fields that carry the document. Fill those, then decide whether the rest earns its space. A template filled front to back gets its best attention on section 1 and its worst on the section that decides the launch.
3. **Upgrading is normal, downgrading is a decision.** A ticket that grows into a quarter gets promoted to a one-pager or a PRD, and the promotion is logged. Cutting a PRD down to a one-pager mid-flight is also allowed, and also logged, because someone signed the heavier version and has a right to know their signature now covers less.
4. **The gate does not change with the weight.** Gate 2 in [STAGE-GATES.md](STAGE-GATES.md) asks the same questions of a one-pager and a full PRD: does every requirement have a pass condition, does every assumption have an owner. A lighter document answers them in fewer words, not in fewer answers. Anyone who reads a light weight as a discount on evidence has inverted the tool: the weight is chosen to save writing, never to save knowing.
5. **When two answers are defensible, take the lighter one and say so.** Write one line in the decision log naming the weight you chose and why. If the choice was wrong, that line is what tells the next person where the gap came from. The asymmetry justifies the bias: an under-weighted artifact is promoted mid-flight at the cost of an afternoon, while an over-weighted one is never demoted, because nobody volunteers to have written too much.
