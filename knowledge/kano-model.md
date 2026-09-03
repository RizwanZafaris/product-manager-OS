---
layer: knowledge
stage: DISCOVER
gate: 1
feeds: ["templates/definition/prd.md", "templates/planning/roadmap.md", "frameworks/discovery/kano-survey.md"]
method: ""
aliases: ["Kano Model", "kano-model"]
---
# Kano Model

Based on the ideas of Noriaki Kano and colleagues, from the paper on attractive quality and must-be quality (1984).

## The essence

Not all product attributes buy satisfaction the same way, and treating them as one pool is how teams overspend on the wrong ones. Kano's insight is that attributes fall into classes with different satisfaction curves:

- **Basics (must-be).** Their absence enrages; their presence earns nothing. Nobody praises a banking app for not losing money. Investment past "reliably present" is wasted.
- **Performance (one-dimensional).** More is better, roughly linearly. Speed, battery life, storage. These are the attributes customers can articulate when asked, which is why surveys overweight them.
- **Delighters (attractive).** Their absence costs nothing because nobody expects them; their presence produces disproportionate joy. Customers cannot ask for them, by definition.

Two further classes matter in practice: **indifferent** attributes, which move nothing either way and are pure cost, and **reverse** attributes, where some users actively dislike what others want. Classification is empirical, not intuitive: ask each attribute as a pair of questions, how would you feel if it were present, and how would you feel if it were absent, and let the answer pair place it in a class.

The strategic reading: cover every basic, compete on chosen performance attributes, and hold a small budget for delighters, because that is where differentiation lives.

The mechanism worth understanding is the asymmetry. Kano's real claim is that the value of having an attribute and the cost of lacking it are two different quantities, and that a single importance rating destroys the distinction by averaging them. Ask a customer how important reliable delivery is and they say extremely, which reads identically to how they rate a genuinely differentiating feature; ask the pair of questions and reliability shows its true shape, catastrophic when absent and worth nothing when present. Everything the model is good for follows from separating those two numbers.

The second structural idea is that a class is not a property of an attribute. It is a property of the attribute for a given segment at a given moment against a given set of alternatives. The same capability is attractive to a new customer, must-be to a customer whose workflow has come to depend on it, and indifferent to a segment that solved the problem another way. Any sentence of the form "X is a delighter" is missing two thirds of its subject, and most misuse of the model traces back to that missing context.

## Where it came from

Kano's paper came out of Japanese quality engineering in the early 1980s, a tradition preoccupied with defects and conformance, and its intellectual debt is to Frederick Herzberg's two-factor theory of workplace motivation, which had argued that the things that cause dissatisfaction at work and the things that cause satisfaction are different things rather than two ends of one scale. Kano carried that asymmetry into product attributes.

Knowing the lineage explains what the model measures and what it ignores. It came from a world where quality was the question and price was set elsewhere, which is why the instrument asks about feeling and never about money. It also explains the model's confidence about basics: in a manufacturing context, the catastrophic cost of a missing must-be attribute was obvious to everyone, whereas in software a missing basic is often invisible to the team that ships it and visible only in the support queue.

## What the classification assumes

1. **The respondent has lived the scenario.** The dysfunctional question asks how you would feel if something were absent, which only produces signal from someone who can imagine the absence concretely. Ask a person who has never done the task and you get politeness, which lands as attractive because nobody misses what they never had.
2. **The attribute is atomic.** A compound attribute splits its own votes: automatic categorization plus a way to correct it is one must-be and one performance factor wearing one name, and it will classify as whichever half the wording emphasized.
3. **Satisfaction is the right dependent variable.** Kano measures feeling about presence and absence, not willingness to pay and not behavior. A delighter can be adored and unpurchased, which is not a contradiction; it is the model answering the question it was asked.
4. **The classes hold for the horizon you are planning.** Over a release, usually yes. Over three years, no, and the trap section below is the reason.

## When to use it

- When scoping a release: the PRD's functional scope should cover basics completely before any delighter spends a line of the budget.
- When sequencing a roadmap: performance investments compound predictably; delighter investments are bets and should be sized like bets.
- When a stakeholder insists every requirement is critical, as the instrument that forces a classification with the customer's voice rather than the loudest voice.

**Skip it when:** one basic is visibly broken. Classification will tell you what every support ticket already says, and the survey costs a week you could spend fixing the thing. Come back to Kano once the floor holds.

## A worked case, ILLUSTRATIVE

Orchard is an invented grocery delivery service, and every number below is made up. The team had ten engineer-weeks for the next release and a draft plan that spent seven of them on a recipe engine that reads your basket and suggests meals, with three weeks left for the substitutions flow, which currently emails you a replacement item after the driver has left.

The classification came back with substitutions as must-be, delivery-window accuracy as one-dimensional, and the recipe engine as indifferent for the main segment and attractive for a small one. The numbers behind those classes mattered less than what they did to the plan. About one order in nine contained a substitution; roughly two in five of those orders generated a support contact; and among customers who had two substitution surprises, the reorder rate was visibly lower than the base. The recipe engine, meanwhile, would be adored by a segment the team could size at fewer than one customer in fifteen.

The plan inverted: seven weeks on approve-or-reject substitutions before the driver packs, three on a recipe experiment for the segment that wanted it. That inversion is the entire practical value of the model, and notice it is not a preference for boring work. The reasoning is structural: the must-be attribute had a large population, a negative tail, and no upside for exceeding it, so the correct spend is exactly enough to make it reliably present and not one week more. The attractive attribute had a small population and an upside, so the correct spend is a bet sized to what you can afford to lose. A single importance score would have ranked both as high and told the team nothing about how much to spend on either.

The shape of the spend follows from the shape of the curve, which is the part worth carrying to the next release. A must-be attribute has a cliff and then a plateau, so the money buys everything up to the plateau and nothing after it. A performance attribute has a slope, so spending is a judgment about how far along the slope your competitors sit. An attractive attribute has an option's payoff, so it is sized like an option: small, several of them, and most expected to expire worthless.

One further reading, easy to miss: the recipe engine was indifferent, not reverse. Nobody disliked it. That is what makes indifferent attributes dangerous rather than merely useless, because they survive every review on the grounds that they harm nothing, and their cost shows up as the release that did not happen.

## The trap: delighters decay into basics

The classes are not stable, and the drift runs in one direction. Yesterday's delighter becomes today's performance attribute and tomorrow's basic: cameras in phones, free shipping, autosave. A team that classified its attributes once and filed the result is now defending a differentiator that the market reclassified as table stakes years ago, and wondering why the delight line item stopped producing delight. The decay has a second edge: a competitor's delighter can silently become your missing basic. Reclassify on a cadence, and treat any delighter more than a couple of years old as a suspect basic until the question pair says otherwise.

The decay is also what makes the model a strategy instrument rather than a scoping one. If every attractive attribute eventually becomes must-be, then a company's differentiation has a half-life, and the only durable position is a rate of producing new attractive attributes faster than the market absorbs the old ones. A roadmap made entirely of must-be work is describing a product that will be adequate and unremarkable in two years, which is a legitimate choice for some businesses and a slow death for others. The classification tells you which of those you are currently building.

## Other ways it fails, and the tell for each

- **Everything is must-be, according to stakeholders.** Asked directly, an internal team classifies every requirement as a basic, because that is the class that guarantees funding. The tell: the must-be list is longer than the release and no item on it has a support ticket, a churn interview, or a lost deal behind it.
- **Reverse attributes averaged into invisibility.** Two segments disagree, the counts cancel, and the attribute reads indifferent. The tell: an unusually flat distribution across all classes on an attribute someone feels strongly about. Cut the tabulation by segment before believing any flat row.
- **Class as verdict rather than as budget guidance.** A team hears "indifferent" and deletes, or hears "must-be" and gold-plates. The tell: engineering effort on a must-be item continuing past the point where it is reliably present, usually described as making it best in class.
- **Basics starved by prioritization arithmetic.** Any score built on movement of a goal metric will rank a basic last, because a basic delivers the absence of a bad outcome and moves nothing when present. The tell: a floor requirement losing to a feature on a scoring sheet. See the [RICE card](rice-prioritization.md) for why the formula cannot see it and must be overridden by the classification.
- **Classifying a category nobody has experienced.** For a genuinely new product, the dysfunctional question has no referent and the survey returns attractive across the board. The tell: no must-be rows at all, which is not a finding about a market, it is a broken instrument.
- **The competitor's roadmap as a classification.** Attributes get treated as must-be because a rival shipped them, which is a claim about the market's expectations and needs the same evidence as any other. The tell: the must-be list matches a competitor's release notes more closely than it matches your own support queue.
- **Basics inferred from the loudest complaint.** A vocal minority produces an attribute that feels catastrophic and classifies as indifferent for almost everyone. The tell: the evidence is a named account rather than a count.
- **Sample too small to carry six classes.** Six categories over a few dozen respondents leaves most rows decided by a handful of votes. The tell: winning margins of one or two respondents, treated as classifications.

## How it lies

Kano lies about magnitude. It sorts attributes into classes and says nothing about how much any of them is worth, so a room can leave the exercise agreeing that three attributes are one-dimensional and still have no idea which of the three to fund. That gap is filled by importance ratings, opportunity scoring, or price research, and a team that treats the class label as a priority order has confused a taxonomy for a ranking.

It also lies by consensus. The class is the mode of a distribution, and a mode is a poor summary of a genuinely split population. An attribute that reads must-be at sixty percent and indifferent at thirty is reported as a basic, and the reported basic is invisibly a segmentation finding: you have two products or one product with an option. The distribution is the evidence; the class is a compression of it, and the compression is where the information goes.

The consequence for a review meeting is specific: never let a class label enter a decision without the counts behind it. A room that hears "that one came back must-be" cannot tell a unanimous result from a coin flip, and the two justify very different spending.

Finally it lies about the future by construction. The question pair asks about now, and every answer is anchored to what the respondent's current alternatives already provide. That is why the model can never nominate the next delighter, only recognize one after it exists. Discovery has to supply the candidates; Kano can only sort them.

A useful closing question for any classification session: which attribute on this list would a competitor's customer describe as the reason they would never switch back. That answer is a basic you may not have, and it will not appear in your own survey.

## What good looks like

The question pairs, the classification grid, the tie-break order and the action per class live on the [survey worksheet](../frameworks/discovery/kano-survey.md). What follows is how you tell a classification that changed a decision from one that decorated a decision already taken.

| Done well | The version that looks the same and is not |
|---|---|
| The classification cut something the team had already started building | The classification confirmed the plan the team walked in with |
| A must-be surfaced that nobody had thought to name | Every must-be it found was already in the release scope |
| The distribution kept beside the class label | The class label alone, with a mode of forty percent presented as a finding |
| A class read as this year's answer from this market | A class read as a property of the feature |
| The attractive bet has an owner who is permitted to abandon it | The attractive bet has a date and an audience already expecting it |
| A sample containing people who could plausibly leave you | A sample containing the people most willing to answer, who are the least likely to leave |
| The team can name what moved an attribute out of attractive since the last reading | The last reading is cited as though expectations were a constant |

The unifying error in the right-hand column is treating a class as a fact about the product rather than a measurement of one population at one time. That confusion is expensive in a specific direction: it makes must-be creep invisible. A delighter that your competitors all shipped last year has already become a basic in the customer's head, and nothing in your own instrument will report the change, because the survey you ran before they shipped is still on file and still reads attractive. So the load-bearing question is never "what did the classification say", it is "what has moved since it said it, and who noticed". A team that cannot answer the second question is running a three-year-old reading of a market that reprices expectations annually.

## Where it sits in the loop

- Stage: DISCOVER for the fielding, DEFINE for the consequence. Classification is a scoping instrument, so it is worth nothing after scope is fixed.
- Upstream: the [survey design](../templates/discovery/survey-design.md) supplies the sample plan, and the attribute list comes from interviews and the [journey map](../templates/discovery/journey-map.md), not from the backlog.
- Downstream: the [PRD](../templates/definition/prd.md) functional scope takes the must-be rows first, and the [roadmap](../templates/planning/roadmap.md) takes performance attributes as its compounding line and attractive ones as bets.
- On trial at [Gate 2: requirements signed off](../os/STAGE-GATES.md), where a scope with an unfunded basic should not pass.
- Related: the [RICE card](rice-prioritization.md) explains why a scoring sheet will rank the basics last, and why the classification overrides the sheet rather than feeding it.

## What it is not for

- **Pricing.** Satisfaction is not willingness to pay. Use van Westendorp or Gabor Granger for the price question, and expect a delighter that everyone loves and nobody will pay for.
- **Ranking inside a class.** Once you have five one-dimensional attributes, Kano is finished. Opportunity scoring or a weighted matrix does that job.
- **Bug triage.** A defect in a shipped basic is not a classification question, it is a floor that broke, and running a survey to confirm it wastes the week the fix needed.
- **Novel categories.** No lived scenario, no dysfunctional signal. Use interviews about the job and the existing workaround, then bring candidates back to Kano when there is something to be absent.
- **Deciding whether to build at all.** Every class assumes the attribute belongs to a product someone already wants. The prior question, whether the job is worth serving, belongs to [jobs to be done](jobs-to-be-done.md).

## Variants worth knowing

- **Kano with self-stated importance**, the most common practical extension: ask an importance rating alongside the pair, so the one-dimensional attributes arrive pre-sized. Cheap, and it fixes the magnitude gap above.
- **Better and worse coefficients**, from Charles Berger and colleagues (1993): two indices per attribute computed from the class counts, one for satisfaction gained by presence, one for dissatisfaction caused by absence. Useful because they preserve the distribution instead of collapsing it to a mode.
- **Continuous or graded scales**, replacing the five fixed answers with a longer scale. Better statistics, worse comparability with the standard classification table, and a common source of arguments about which variant a past result used.
- **Kano against a competitor**, run by asking the pair about the rival's product as well as your own. The interesting output is not where you lose but where you both overspend: an attribute classified indifferent for both is a shared industry habit and the cheapest differentiation budget available.
- **Reverse-first reading**, a discipline rather than a variant: scan the reverse column before the mode column, because a concentrated reverse signal is the most actionable single result the survey produces and the mode hides it.
- **Ulwick's outcome-based cousin**, from the jobs-to-be-done tradition: instead of classifying features, rate desired outcomes on importance and satisfaction and read the gap. Different unit of analysis, same underlying suspicion of a single importance score.

## Used by

- [PRD](../templates/definition/prd.md)
- [Roadmap](../templates/planning/roadmap.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [Kano survey](../frameworks/discovery/kano-survey.md), the question pair, the classification table, and the tabulation
- [Opportunity scoring](../frameworks/discovery/opportunity-scoring.md), for ranking inside the one-dimensional class
- [Survey design](../templates/discovery/survey-design.md), for the sample plan the classification depends on
- [Van Westendorp](../frameworks/pricing/van-westendorp.md), for the price question this model cannot answer
