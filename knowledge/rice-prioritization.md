# RICE Prioritization

Based on the ideas of Sean McBride, developed at Intercom and published on the Intercom blog (2016).

## The essence

RICE exists to solve a specific meeting: five initiatives, four advocates, and no shared basis for comparison. It scores each initiative on four factors and produces one comparable number.

- **Reach.** How many people does this touch per time period? A count from real data: users per quarter, transactions per month. Not a percentage of an imagined market.
- **Impact.** How much does it move the goal for each person reached? Scored on a coarse scale (3 for massive, 2 for high, 1 for medium, 0.5 for low, 0.25 for minimal), coarse on purpose, because finer claims to precision would be fiction.
- **Confidence.** How much of the above do you actually believe? 100 percent for shipped-and-measured certainty, 80 percent for evidence, 50 percent for educated hope. Below 50 percent, the honest move is to go get evidence, not to score.
- **Effort.** Person-months, from the people who would do the work.

Score = (Reach x Impact x Confidence) / Effort. The confidence factor is the quiet genius of the scheme: it taxes enthusiasm. A gigantic reach estimate built on air gets multiplied by the air.

What the arithmetic encodes is a rate, not a size. Reach times impact times confidence is expected movement of the goal; dividing by effort converts that into movement per unit of engineering time. The division is the whole argument. It is why a modest improvement that takes two weeks can and should outrank a transformative one that takes two quarters, and it is why RICE is a claim about opportunity cost rather than about desirability. Every row on the sheet competes for the same scarce input, and the score says how efficiently each converts that input into goal movement.

Read that way, the score also tells you what it cannot compare. Two rows drawn from different capacity pools have different scarce inputs in the denominator, so their rates are not on one axis, and a sheet that mixes them produces a ranking whose top item nobody can act on this quarter.

The second structural choice is coarseness. Impact has five permitted values and confidence has three. Kept that way, the sheet cannot express a distinction the evidence does not support, and disagreement is forced up to the level where it is arguable: not "is this 1.7 or 1.9" but "is this medium or high, and what would we have to see to call it high". A team that adds decimal places to the impact column has quietly deleted the feature that made the tool honest.

## Where it came from

RICE was built inside one product team at Intercom to solve a local problem: comparing projects of genuinely different kinds, a bug-reduction push against a new integration against a pricing change, when the team had already decided what it was trying to grow. That origin explains two things about the shape of the method.

It explains the missing strategy term. There is no fit or alignment factor because fit was settled upstream, by the goal the impact column is scored against; adding one later re-imports the argument the sheet was built to end. It also explains the effort unit. Person-months come from an environment where a small team estimated its own work, so the denominator was hard to inflate without lying to colleagues, which is exactly the property that erodes when a sheet is filled in privately by sponsors who will not do the work.

## What the score assumes

Four assumptions ride under the formula. Each is fine until it is not, and knowing which one broke is how you tell a wrong ranking from a wrong method.

1. **The items are substitutable claims on one pool of capacity.** If two rows draw on different budgets, or one needs a specialist nobody else can use, the ranking compares numbers that were never in competition. Split the sheet by pool before splitting hairs over the scores.
2. **Value is linear in reach.** Each additional person reached is assumed to add the same increment. That is false for anything with a network effect, because the tenth team on a shared workspace is worth more than the second, and false again at saturation, because the reach count includes events where the change could not act at all. When value is not linear, the reach cell stands in for a curve and the score inherits the error silently.
3. **Effort and impact are independent.** They almost never are. Halving the scope halves the effort and usually cuts the impact by more, because the half that got cut was the half doing the work. A sheet where scope changed and only the effort column moved reports a score no version of the product would earn.
4. **The goal is fixed for the period.** Impact means impact on one named metric. Rescore, or retire the sheet, the moment that metric changes, because a stale sheet keeps producing confident rankings against a target nobody is judged on any more.

## When to use it

- When a roadmap has more candidates than capacity and the ordering debate has gone circular.
- When two initiatives feel equally urgent, as a forcing function to write down the beliefs behind each and see which one is built on measurement and which on adrenaline.
- When saying no: a low score with visible inputs is a kinder and more durable rejection than a manager's mood.

**Skip it when:** the list is under five items, or the items are not comparable. A compliance mandate scored against a revenue feature produces a number that looks like a decision and is not one; mandates get a deadline lane instead. Two obvious priorities and a clear third do not need arithmetic to sort them.

## A worked case, ILLUSTRATIVE

Quayside is an invented booking tool for small freight brokers, and every number below is made up. The metric for the quarter is the share of loads booked without a phone call; the reach unit is loads booked per quarter.

| Item | Reach | Impact | Confidence | Effort | Arithmetic | Score |
|---|---|---|---|---|---|---|
| Saved lane templates | 3,200 | 1 | 0.8 | 2 | 3,200 x 1 x 0.8 / 2 | 1,280 |
| Carrier auto-match | 3,200 | 2 | 0.5 | 5 | 3,200 x 2 x 0.5 / 5 | 640 |

Templates win by two to one, and the instructive part happens next. Auto-match's sponsor proposes a cheaper version: suggest three carriers without the ranking model, effort down from five to two. Rescored honestly, impact falls from high to low, because the ranking model was the part that made a suggestion trustworthy enough to act on. The new score is 3,200 x 0.5 x 0.5 / 2, which is 400: worse than the version that was already losing. The cheap version looked like a win on the denominator and was a loss on the rate. This is the most common way a live sheet drifts from the truth: scope gets trimmed in a planning meeting, the effort cell is updated on the spot, and the impact cell is not.

Now read the confidence column instead of the ranking. Auto-match sits at 0.5, which means nobody has measured anything and the row is a belief with a spreadsheet around it. Three weeks of instrumented analysis of how brokers actually choose a carrier would move it to 0.8 if the belief survives, and at 0.8 with impact holding the score becomes 1,024, inside the tie band with templates and no longer resolvable by arithmetic. So the best use of the next three weeks was neither build; it was the measurement that decides between them. That conclusion was the sheet's real output, and it came from the column teams fill in last.

## The trap: false precision

The output is a number, and numbers borrow authority they have not earned. A score of 47.3 beats a score of 45.1 on the spreadsheet, but three of the four inputs were estimates with error bars wider than the gap, so the ranking of those two rows is noise presented as arithmetic. Teams then defend the number instead of the beliefs behind it, and the tool built to expose assumptions starts laundering them. The discipline: treat scores as buckets, not rankings; near scores are ties, and ties get resolved by judgment, in the open. The score's real product was never the number. It was the argument you had to have about reach and confidence to produce it.

The tell that precision has gone false is social rather than mathematical. Listen for the phrase "the score says". A team using the tool well says "we scored it high because we measured the drop-off at that step, and here is the date"; a team being used by the tool says the score said so and cannot name which cell carries the claim. Once the inputs are invisible and only the output is quoted, the sheet has stopped being an argument and become an oracle, and an oracle cannot be corrected by evidence.

## Other ways it fails, and the tell for each

- **Denominator gaming.** Effort is the one input a sponsor controls unilaterally, so it is the one that gets shaved. The tell: estimates arrive as suspiciously round small integers, and the phrase "phase two" appears in the description of a row whose effort covers only phase one. A phase two required for the impact to materialize belongs in the same row.
- **The reach of everyone.** The tell: two unrelated rows carry the identical reach number, because both were scored as all monthly active users. Real reach counts the events where this change could plausibly act, which is a fraction of the base, and a different fraction for every item.
- **Confidence inflation after the room.** The tell: a confidence cell moves from 0.5 to 0.8 between draft and published version with no new evidence link and no new date. Seniority changed the number. The rule that closes it: confidence may only change in the same edit that changes the evidence cell.
- **The unscored winner.** The tell: the thing the team actually built this quarter is not on the sheet at all. Escalations and pet projects enter by a side door, and the sheet's authority quietly shrinks to the items nobody cared about. Every build slot maps to a row or to the mandate lane, and unscored work is logged as an exception with a name on it.
- **Impact against a private goal.** The tell: you could not verify two rows with the same metric, because each sponsor scored impact against the outcome they personally care about. The sheet then ranks incommensurables and looks composed while doing it.
- **The bundled row.** Three unrelated changes ride in one row because they share a sponsor, and the row scores on the best of them and costs the effort of all three. The tell: a description containing the word "and" twice, or an effort figure that no single change could consume. Split it and watch two of the three fall down the list.
- **Reach borrowed from the market.** The reach cell holds a share of an addressable market rather than a count of events in your own logs. The tell: a round number ending in three zeros with no query behind it. Market size belongs in the business case; reach belongs to the population you can already observe.
- **Score decay.** The tell: the newest evidence date anywhere on the sheet is older than the current quarter. Reach counts move, effort ages badly after an architecture change, and a sheet nobody rescores is a snapshot being cited as an instrument.

## How it gets gamed

RICE is gamed most effectively by people who believe they are being rigorous. The move is not to invent a number; it is to choose, among several defensible numbers, the one that helps, and to do it in all four cells. Reach takes the widest defensible unit, impact takes the top of its range because "that is what it does once adopted", confidence takes the analogy tier on the strength of a competitor's blog post, and effort takes the estimate that assumes nothing goes wrong. Each choice survives challenge on its own. Together they move a score by an order of magnitude while every cell stays arguable.

The signature of a gamed sheet is therefore not an outlier cell; it is a row where all four cells sit at the favorable end of their defensible ranges at once. That pattern is worth checking directly, because it is visible in ten seconds and no individual challenge will ever surface it.

The defense is not a tighter scale, because a tighter scale only relocates the argument. It is making the choice visible: every cell carries its source and date, the sheet is scored in one sitting by one group rather than filled in privately by each sponsor, and each sponsor is walked through their own row before publication. The walkthrough is not for approval. It works because a person will defend in writing a number they will not defend out loud to the team whose slot it takes.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| One reach unit declared at the top of the sheet and used in every row | Each row scored in whatever unit its sponsor had data for |
| Effort quoted by the people who would do the work, covering every discipline | Effort quoted by the sponsor, covering the engineering half |
| Confidence cells carry a source and a date, and change only when those change | Confidence cells carry a number that rose after the review meeting |
| Scores within about a fifth of each other treated as tied and settled in the open | Rows ordered strictly by score to one decimal place |
| Rows at opinion-level confidence get a discovery task, however high they score | High-scoring guesses get build slots and are validated in production |
| Mandates take capacity first, outside the ranking, with their dates | Mandates scored against the goal metric and losing to a feature |
| The sheet is rescored when the goal metric changes | The sheet is cited for three quarters against a target that moved in the first |

## Where it sits in the loop

- Stage: PLANNING, between a strategy that has named the metric and a roadmap that needs an order. It consumes evidence and produces a sequence.
- Upstream: the [OKR sheet](../templates/planning/okrs.md) for the metric, the [metrics review](../templates/operate/metrics-review.md) or an [evidence note](../templates/discovery/evidence-note.md) for reach counts, and the [dependency register](../templates/execution/dependency-register.md) for hard dates.
- Downstream: the [roadmap](../templates/planning/roadmap.md) takes the ranked list, and the [decision log](../templates/execution/decision-log.md) takes every tie-break with the option that lost.
- On trial at [Gate 1: problem worth solving](../os/STAGE-GATES.md), where a high score with opinion-level confidence is exactly what the gate exists to stop.
- Automated by the [roadmap builder skill](../skills/roadmap-builder/SKILL.md), which fills the sheet at its scoring step.

## What it is not for

- **Deciding whether to do anything at all.** RICE ranks; it does not clear a bar. A list of weak ideas yields a best weak idea with a confident score, and no part of the arithmetic will suggest throwing the list away. That judgment comes from the strategy.
- **Sequencing dependent work.** The score is a value rate, blind to order of feasibility. If the second-ranked row unlocks the first, the ranking is not yet a plan; sequence with cost of delay and the dependency register after ranking, never instead of it.
- **Items with an external date.** A contracted go-live or a scheme deadline is not a bet whose value you compare, because missing it carries a cost the impact scale cannot express. That work takes capacity first, off the ranked list.
- **Platform and enablement work.** Its reach is other teams and its value is that later items become cheaper, and the formula has no column for a change in someone else's denominator. Score it by the effort it removes from named downstream rows, or accept that the sheet will starve it every quarter.
- **Basics, in the Kano sense.** An attribute whose absence enrages and whose presence earns nothing scores low on impact, because impact measures movement and a basic delivers the absence of rage. Read the [Kano card](kano-model.md) before letting a sheet defund a floor requirement.

## Variants worth knowing

- **ICE**, from Sean Ellis's growth practice: impact times confidence times ease, one to ten each, no reach term. Its job is triaging raw intake in an hour, not allocating build slots. Never mix ICE and RICE numbers in one ranking; the scales share no unit.
- **A strategic-fit multiplier**, which many teams bolt on as a fifth factor. Know what you are buying: a free parameter, applied after the other four are visible, that can reach any answer. If you add one, cap its range, set it before the scores are shown, and record who set it.
- **Cost of delay and WSJF**, from Don Reinertsen: divide by duration rather than effort and price the value of time itself, which is the right instrument when candidates decay at different rates.
- **Weighted decision matrix**, when the decision is genuinely multi-criteria. RICE collapses to one axis by design, and forcing a real trade-off through it hides the trade-off instead of resolving it.
- **Bucketed RICE**, a small discipline that fixes the method's worst habit: publish results as three tiers rather than a ranked list, so the arithmetic sorts items into groups and human judgment orders within a group. Everything the score is good at survives; the false ranking of near-ties does not.
- **Opportunity scoring**, from Tony Ulwick, for the earlier question. RICE ranks candidate solutions; opportunity scoring ranks underserved outcomes when you do not yet have candidates worth scoring.

## Used by

- [Roadmap](../templates/planning/roadmap.md)
- [Discovery document](../templates/discovery/discovery-document.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [RICE scoring sheet](../frameworks/prioritization/rice-scoring-sheet.md), the sheet that runs this method, with the arithmetic written out
- [WSJF cost of delay](../frameworks/prioritization/wsjf-cost-of-delay.md), for sequencing once the ranking exists
- [MoSCoW](../frameworks/prioritization/moscow.md), for scoping against a date the ranking cannot move
- [Decision log](../templates/execution/decision-log.md), where every tie-break belongs, with the option that lost
- [OKRs](okrs.md), which supplies the one metric impact is scored against
