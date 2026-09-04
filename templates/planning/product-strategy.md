---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Product Strategy", "product-strategy"]
---
# Product Strategy: [product name]

**Stage:** PLANNING track (feeds every stage of the [operating loop](../../os/OPERATING-LOOP.md))
**Knowledge:** [Knowledge index, strategy kernel and Playing to Win entries](../../knowledge/INDEX.md)
**Skill:** [write-vision-strategy](../../skills/write-vision-strategy/SKILL.md); [strategy-critic](../../skills/strategy-critic/SKILL.md) for the attack pass

<!-- Strategy is choice under constraint, not a goals slide. The spine here is Richard
     Rumelt's kernel, restated in this repository's own words: a diagnosis of the
     situation, a guiding policy that responds to it, and coherent actions that follow
     from the policy. The where-to-play framing comes from A.G. Lafley and Roger
     Martin's Playing to Win, likewise in our own words. Both are index entries in the
     knowledge layer.

     The test for every section: does it exclude something? A strategy that no
     reasonable competitor would state differently is a mission statement. This file
     sits between the [vision](vision.md) (the destination) and the
     [roadmap](roadmap.md) (the next three horizons); it explains why the roadmap
     contains these bets and not others. -->

**Owner:** [name] · **Period:** [e.g. FY27] · **Last updated:** [YYYY-MM-DD]

## 1. Strategic context: the diagnosis

<!-- What is actually going on: the market shift, the customer struggle, the
     competitive fact, the internal constraint. A diagnosis names the crux, the one
     obstacle that, if solved, unlocks the rest. Claims here need evidence links, not
     adjectives. -->

- **The situation:** [2 to 4 sentences, each claim linked to evidence]
- **The crux:** [the one obstacle this strategy exists to beat]
- **What changed recently:** [why last year's strategy is not automatically this year's]

## 1b. The guiding policy

**In one sentence:** [how the diagnosis gets beaten, stated as a constraint that refuses something a reasonable competitor might choose instead]

| Test | Answer |
|---|---|
| The opposite policy, written out | [if the opposite is absurd, the policy is a platitude; if a sane rival might choose it, the policy is real] |
| What this policy refuses | [the thing a competitor gets to do that you now do not] |
| Who has to change what they do on Monday | [name the team and the change; a policy nobody acts on differently is a slogan] |

<!-- Rumelt's kernel has three parts and most strategy documents ship two of them:
     the diagnosis above and the actions below, with the policy left implicit. The
     implicit policy is where strategies go to die, because everything downstream
     can be justified against a sentence nobody wrote. It is numbered 1b rather than
     2 so that every section number below it, and every document that cites one,
     keeps meaning what it meant before this section existed.

     "Grow the business" and "invest in innovation" both fail the opposite test:
     nobody's strategy is to shrink the business. Keep rewriting until the sentence
     would make a rival's product lead wince. -->

## 2. Where to play: the bets

<!-- Two or three bets, not seven. Each bet is a segment, geography, use case, or
     channel we choose, which means others we refuse. The refused column is the
     proof a choice was made. -->

| Bet | What we choose | What we thereby refuse | Evidence for the bet |
|---|---|---|---|
| 1 | | | [linked] |
| 2 | | | |
| *example* | *mid-market ops teams already on our integration partner* | *self-serve consumer, enterprise RFPs this period* | *pilot waitlist and partner referral data, filed in discovery/* |

## 3. How we win: differentiation

<!-- Why the chosen customer picks us over their current alternative. Anchor it in
     something durable: a capability, an asset, a position competitors would have to
     hurt themselves to copy. "Better UX" is a claim every deck makes; name what makes
     it defensible, or admit the edge is temporary and plan for that. -->

- **Our edge:** [one sentence]
- **Why it holds:** [the mechanism: switching costs, data, distribution, counter-positioning, or admit "execution speed only"]
- **The named alternative it beats:** [what the customer does today]

## 4. Sequencing

<!-- Order matters more than ambition. State what must be true before each later bet
     is funded, so the strategy self-corrects instead of running on inertia. -->

| Order | Move | Precondition (evidence, not a date) | Feeds |
|---|---|---|---|
| 1 | | [what must be proven first] | |
| 2 | | | |

## 5. Success metrics

<!-- Two or three, each traceable to the [north star sheet](north-star-metric.md) or
     an input on its tree. A strategy scored on a private metric cannot be compared to
     the strategies it displaced. -->

| Metric | Baseline | Target for the period | Tree link |
|---|---|---|---|
| | | | [north star or input metric it feeds] |

## 6. Key risks

<!-- What would make this strategy wrong, and how we would notice before the
     retrospective does. Feed material rows into the [risk register](../execution/risk-register.md). -->

| Risk to the strategy | Early signal we would see | Response if seen | Owner |
|---|---|---|---|
| | | | |

## How this strategy fails

<!-- Rumelt's test, applied here: a strategy needs a diagnosis, a guiding
     policy and coherent action. Most documents called strategy have the third
     only, which is why they read as busy and decide nothing. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Goals with no diagnosis | Targets and initiatives, and no statement of what is actually in the way | Every bet names the obstacle it removes |
| Nothing is refused | Everything is strategic, and no option was given up | Each policy names what it deprioritises, by name |
| Bets untraceable to the policy | Initiatives in the plan that no stated principle would have produced | A bet that cannot be derived from the policy is a preference |
| Copying a competitor | The plan mirrors a rival's shipping log, feature for feature | Each bet states the problem you are positioned to solve and they are not |
| Survives any evidence | Unchanged after a win, a loss and a market shift | Name the observation that would kill each bet, and a date to check |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- The kernel, compressed. Delete once real content exists. -->

*Diagnosis: reps do not avoid filing expenses because the form is slow; they avoid it because a rejected claim costs them a second submission and an argument. Filing time is a symptom.*

*Guiding policy: optimise for first-time acceptance, not for filing speed. We will refuse work that shortens the form at the cost of accuracy.*

*Coherent action: extraction accuracy on the fields finance rejects most, an in-app pre-check against policy before submission, and no autofill of any field we cannot verify. We are explicitly not building bulk upload, which is the most requested feature and does not touch acceptance.*

*What would kill it: acceptance rate does not move while filing time does. Checked at the end of the pilot.*

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


This strategy is fit to operate on when:

- [ ] The diagnosis names a crux, and every situational claim links to evidence
- [ ] The guiding policy is one sentence that refuses something, and its opposite is a choice a sane rival could make
- [ ] There are at most three bets, and each names what it refuses
- [ ] The differentiation names a mechanism and a real alternative, not an adjective
- [ ] Sequencing gates later bets on evidence conditions, not calendar quarters
- [ ] Every success metric traces to the north star tree
- [ ] Each risk has an early signal someone is actually watching

Signed: [name], [role], [YYYY-MM-DD]
