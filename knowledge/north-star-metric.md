---
layer: knowledge
stage: PLANNING
gate: 6
feeds: ["templates/planning/okrs.md", "templates/operate/metrics-review.md", "templates/definition/prd.md"]
method: ""
aliases: ["North Star Metric", "north-star-metric"]
---
# North Star Metric

Based on the ideas of Sean Ellis and the growth community, codified in Amplitude's North Star Playbook by John Cutler and colleagues (2019).

## The essence

A north star metric is the one number that best expresses the value customers are actually receiving. Not revenue: revenue is a lagging result of value delivered earlier, and steering by it is driving by the rearview mirror. The classic examples share a shape: nights booked, messages sent within a team's first week, orders delivered on time, weekly learners completing a lesson. Each one goes up only when a customer got the thing they came for.

The metric never stands alone. It sits atop a small tree of input metrics: the three to five drivers that teams can directly move, whose movement provably feeds the north star. Breadth of usage, frequency, depth, efficiency of the core action. The north star aligns the company; the inputs give each team a dial it can own. A team cannot move "nights booked" on a Tuesday, but it can move search-to-booking conversion, and the tree is the documented claim that the second feeds the first.

Choosing the metric is a strategy decision in disguise, which is why it is hard and why it is worth doing: it forces the company to state, in one measurable sentence, what value it believes it creates and for whom.

The mechanism underneath is coordination, not measurement. A company already has hundreds of numbers; what it lacks is a shared answer to "better for whom, at what". The north star works by removing the argument from a thousand small decisions and relocating it to one annual argument about the metric itself, where senior people can actually have it. That is also why the metric is expensive to change: every roadmap, dashboard, and key result downstream is a derivative of it, and a company that renames its north star twice a year has bought the coordination cost without the coordination.

It follows that the metric is worth arguing about for a week and worth leaving alone for a year. Teams that find the choice easy have usually picked the number they already had.

The choice is measured against the customer's unit of value, not the company's. This is the fork most teams get wrong on the first attempt. The number of reports created measures the product working; the number of reports approved without rework measures the customer finishing the thing they came for. Those two are correlated until the day the product ships a feature that produces more drafts and more rework, at which point only one of them tells you what happened.

## Where it came from

The idea grew out of growth teams in the years after analytics tooling got cheap, and the problem it was invented against is worth remembering: not an absence of measurement but a flood of it. Teams had dashboards with dozens of tiles, each defensible, and no way to settle an argument between two of them. Sean Ellis's growth practice pushed toward a single number per stage; Amplitude's playbook, written with John Cutler and colleagues, added the tree of inputs and the insistence that the top number express delivered value rather than company revenue.

That history explains the model's emphasis and its blind spot. The emphasis on one number is a response to dashboard sprawl, so the method is strong on coordination and weak on nuance. The blind spot is multi-sided businesses, because the practice was codified largely on products with one clear customer, and it has to be extended by hand with guardrails whenever two customer groups trade against each other.

## What the choice assumes

1. **One number can carry the strategy.** True when the business has one core value exchange, false when it has two that trade against each other. A marketplace serves buyers and suppliers, and a single number always favors one side; that is survivable only if the tree carries a named guardrail for the other side.
2. **The metric is downstream of many teams and gameable by none alone.** A number one team can move by itself becomes that team's target and stops describing the company. A number no team can influence within a quarter becomes wallpaper.
3. **Causation runs from inputs to north star.** The tree is a set of claims about mechanism, not an arithmetic decomposition. If the inputs merely sum to the total, you have written the metric twice and learned nothing about what to do on Monday.
4. **The measurement exists and is stable.** A metric whose definition changes with the query is not one metric; it is a family of metrics sharing a name, and the family will always contain a member that agrees with whoever is presenting.

## When to use it

- When setting OKRs, so key results ladder up to one shared definition of value instead of five departmental ones.
- When writing the success metrics section of a PRD, to check that the feature's metric feeds an input on the tree rather than inventing a private definition of winning.
- When running a metrics review, as the frame for asking whether the inputs moved, whether the north star followed, and whether the causal claim between them survived contact with reality.

**Skip it when:** nothing is instrumented yet. A north star named before anything can be measured is a slogan, and it will be quoted for a year with no number behind it. Build the measurement first, then name the metric it makes possible.

## A worked case, ILLUSTRATIVE

Halden is an invented marketplace for local appliance repair, and every number is made up. The first north star chosen was jobs completed per week, which passed the obvious test: it falls if customers stop getting repairs. Over two quarters it rose from 4,100 to 5,300, and the company celebrated.

Two other numbers moved in the same window. The share of customers booking a second job within six months fell from 38 percent to 29 percent, and the share of jobs where the technician arrived without the right part rose. The growth had come almost entirely from a discount campaign that filled schedules with one-off jobs the network was not equipped to serve well. Jobs completed measured the transaction, and the value customers came for was a working appliance and a repairer worth calling again.

There is a second reading of the same episode. The metric was not wrong in the sense of being mismeasured; it was wrong in the sense of being a faithful measure of the wrong exchange. Halden's customers were not buying jobs, they were buying working appliances, and the gap between those two nouns is where two quarters went.

The repaired metric was jobs completed on the first visit per week, with repeat booking rate held as a guardrail with a floor. The change reads cosmetic and was not: under the old metric, the highest-scoring initiative on the roadmap was more discount inventory, and under the new one it was parts prediction from the appliance model at booking time. The metric had been selecting the roadmap all along, which is what a north star is for; it had simply been selecting the wrong one, confidently, for two quarters.

Note where the failure would have been caught early. Nobody had written down the leak for the candidate metric: the sentence "jobs completed could rise while customers get less if the jobs are cheap, one-off, and badly served". A candidate metric whose leak nobody can name has not been tested, it has been liked.

## The trap: vanity metrics

The counterfeit north star is the number that only goes up: cumulative signups, registered users, total downloads, page views. Monotonic metrics measure the passage of time wearing a growth costume. They cannot disappoint, which is precisely why they cannot inform; a metric that cannot go down when customers stop getting value is not measuring value. The related counterfeit is the activity metric, sessions or clicks, which measures motion through the product rather than progress for the customer. The test for a candidate north star: if every customer silently stopped benefiting tomorrow, would this number fall within the quarter? If not, it is decoration, and the strategy it was supposed to encode is still unwritten.

There is a subtler counterfeit that passes that test: the number that can fall but only for reasons outside the product, such as total transaction value in a business whose customers are seasonal. It falls in January and nobody learns anything, because the fall carries no signal about whether the product got better. A useful north star is sensitive to the thing you control and robust to the things you do not, which usually means a rate or a per-customer figure rather than a raw total.

## Other ways it fails, and the tell for each

- **Goodhart capture.** Once the number is the target, the cheapest way to move it stops being the way that creates value. The tell: the metric improved and no qualitative signal did, or a leaderboard exists that ranks teams by it directly.
- **A north star per team.** Every group adopts its own, and within a year the company has six and coordinates on none. The tell: two teams can both be winning while the company is losing, and neither sheet shows the conflict.
- **The tree that is arithmetic.** Inputs are defined so they multiply back to the top number. The tell: no input row could ever be wrong, because each is a factor rather than a claim. The point of the tree is that a metrics review can grade its claims and find one false.
- **Instrumentation lag.** The metric is adopted before the join between two systems exists, so the reported figure is a proxy nobody documented as a proxy. The tell: nobody can produce the query, or two people produce two.
- **The immovable star.** The metric responds over a year and the company plans in quarters, so every review discusses inputs and nobody remembers what the top number was for. The tell: the north star chart is on slide two and is never the subject of a decision.
- **Survivor framing.** The metric is computed over active customers only, so the ones who left improve it by leaving. The tell: the denominator is defined by current engagement.
- **Mix shift read as improvement.** The number rises because the customer mix changed, not because anything got better for anyone. The tell: the total moved and every segment inside it was flat, which is a fact about acquisition wearing a product result's clothes.
- **The star that is really a constraint.** Reliability, latency, or safety gets promoted to north star because it matters enormously. The tell: the target is a floor rather than a direction, and nobody wants the number to rise without bound. Constraints belong in the guardrail row, where exceeding them earns nothing, exactly as the [Kano card](kano-model.md) describes for basics.

## How it gets gamed

Rarely by fraud and almost always by definition. The three usual moves: narrow the population (count only accounts past onboarding, where the metric is naturally higher), widen the event (count a partial completion as a completion), or shift the window (measure weekly when the weekly figure flatters, monthly when it does not). Each is defensible in isolation and each is a fifteen-minute conversation with an analyst, which is why the definition belongs in the metrics dictionary with a date and an owner rather than in a dashboard title.

The reason to expect this is structural rather than moral. The metric is public, the definition is technical, and the audience for the number is far less equipped to interrogate the definition than the people producing it. Any measure in that position drifts toward its most flattering legitimate reading unless something holds it still.

The organizational defense is separation: the person who reports the number is not the person whose performance the number describes. The cultural defense is cheaper and works better in small companies. Publish the leak alongside the metric, that is, the written sentence describing how this number could rise while customers get less, plus the guardrail that would catch it. A team that has named its own escape route in public is markedly less likely to take it.

## What good looks like

Scoring a candidate, writing the causal claims and setting the guardrails are the [input tree worksheet](../frameworks/metrics/north-star-input-tree.md)'s job. What follows is how you tell a tree that governs decisions from a tree that decorates a planning deck.

| Done well | The version that looks the same and is not |
|---|---|
| The star has fallen, and the fall was explained rather than adjusted away | The star has never fallen, and the definition has been revised twice |
| An input owner can name what they stopped doing because of their row | Every input has an owner and nobody's week has changed |
| Inputs that move against each other, visibly, in the same quarter | Inputs that rise together, which means they are one measurement sliced |
| The star is quoted by people who do not report to whoever chose it | The star is quoted only inside the function that authored it |
| Somebody has argued in writing that an input is the wrong lever, and lost on evidence | Nobody has argued with the tree since the workshop that drew it |
| Reported with the population it excludes | Reported as a total, so a shrinking core hides inside a growing base |
| Changed rarely, and when changed, with the reason recorded | Renamed each planning cycle, so no chart spans two years |

Two of those rows carry most of the weight. Inputs that never move against each other are the commonest structural defect, because a tree of correlated measures gives four teams the same job and no way to trade between them: when all five rows rise and fall together, you have one metric with five names, and the quarterly conversation reduces to encouragement. The composition row is the subtler one. A total can climb while every cohort inside it declines, provided new customers arrive faster than existing ones give up, which is exactly the shape of a product that has stopped delivering and started acquiring. Neither failure is a wrong number and neither trips a guardrail, which is why both survive review cycles that check arithmetic.

## Where it sits in the loop

- Stage: PLANNING for the choice, OPERATE for the reading. The metric is chosen once a year at most and consulted every cycle.
- Upstream: the [vision](../templates/planning/vision.md) and [product strategy](../templates/planning/product-strategy.md) say what value the company claims to create, and the [analytics instrumentation spec](../templates/delivery/analytics-instrumentation-spec.md) says what is computable today.
- Downstream: the [north star sheet](../templates/planning/north-star-metric.md) holds the adopted metric, [OKRs](../templates/planning/okrs.md) attach key results to input rows, and every [PRD](../templates/definition/prd.md) success metric names the input it feeds.
- On trial at [Gate 6: outcomes verified](../os/STAGE-GATES.md), where the causal claims in the tree are graded rather than admired.
- Built by the [metrics tree skill](../skills/metrics-tree/SKILL.md), which drives the worksheet and the dictionary rows together.

## What it is not for

- **Team-level targets.** Teams own inputs, not the star. A key result set on the north star itself is either unmovable by that team or evidence that the metric is too narrow to be a company metric.
- **Feature success measurement.** A feature moves an input, and often a sub-input of an input. Judging a checkout change by the company north star produces a number too noisy to read and an argument nobody can settle.
- **Financial planning.** The north star leads revenue; it does not substitute for it. Board planning needs both, and a company that reports only the north star has replaced one partial picture with another.
- **Early-stage products with no retention yet.** Before there is a repeated behavior to measure, the honest instruments are qualitative and small-sample: interviews, the product-market-fit survey, hand-counted cohorts. Naming a star over an empty dataset produces a slogan.
- **Diagnosing a drop.** The star tells you that value fell, never why. The inputs narrow it, and the actual answer usually comes from a cohort cut or a conversation. A review that stares at the top chart and speculates has skipped both.
- **Two-sided health.** One number cannot express both sides of a marketplace or platform. Choose the side whose scarcity binds today, guard the other explicitly, and revisit when the binding side changes.

## Variants worth knowing

- **HEART**, from Kerry Rodden and colleagues at Google: happiness, engagement, adoption, retention, task success, each paired with a goal, a signal, and a metric. Useful precisely where a single star is too coarse, at feature level.
- **AARRR**, from Dave McClure: acquisition, activation, retention, referral, revenue. A funnel that locates where growth leaks; complementary rather than competing, because the leak it finds usually becomes an input row.
- **One metric that matters**, from Alistair Croll and Benjamin Yoskovitz in Lean Analytics: deliberately temporary, changing as the company's stage changes. The honest correction to treating a north star as permanent, though it costs the long-run coordination the permanent version buys.
- **Engagement ratio**, such as daily over monthly active users: a shape rather than a size, which resists the total-count vanity failure but says nothing about whether the engagement was worth having.
- **The input tree without a star**, an underrated option for a company whose value exchange genuinely resists one number. Publish the three to five inputs, own them, and skip the top box rather than inventing a composite index; a weighted blend of five metrics is a number nobody can interpret and everybody can move.
- **Paired counter-metric**, a discipline more than a variant: every star ships with a named number that must not move. Cheap, and it prevents most of the failures listed above.

## Used by

- [OKRs](../templates/planning/okrs.md)
- [Metrics review](../templates/operate/metrics-review.md)
- [PRD](../templates/definition/prd.md)
- [Growth plan](../templates/planning/growth-plan.md)
- [North star sheet](../templates/planning/north-star-metric.md)
- [Analytics instrumentation spec](../templates/delivery/analytics-instrumentation-spec.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [North star input tree](../frameworks/metrics/north-star-input-tree.md), the tree, its owners, and the lead against lag split
- [HEART metrics](../frameworks/metrics/heart-metrics.md), for the feature-level question this metric is too coarse to answer
- [AARRR funnel](../frameworks/metrics/aarrr-funnel.md), for locating the leak that becomes an input row
- [Metrics dictionary](../templates/operate/metrics-dictionary.md), where the definition lives so it cannot drift
- [OKRs](okrs.md), the card explaining why key results attach to inputs rather than to the star
