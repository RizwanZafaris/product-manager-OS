# North Star Metric

Based on the ideas of Sean Ellis and the growth community, codified in Amplitude's North Star Playbook by John Cutler and colleagues (2019).

## The essence

A north star metric is the one number that best expresses the value customers are actually receiving. Not revenue: revenue is a lagging result of value delivered earlier, and steering by it is driving by the rearview mirror. The classic examples share a shape: nights booked, messages sent within a team's first week, orders delivered on time, weekly learners completing a lesson. Each one goes up only when a customer got the thing they came for.

The metric never stands alone. It sits atop a small tree of input metrics: the three to five drivers that teams can directly move, whose movement provably feeds the north star. Breadth of usage, frequency, depth, efficiency of the core action. The north star aligns the company; the inputs give each team a dial it can own. A team cannot move "nights booked" on a Tuesday, but it can move search-to-booking conversion, and the tree is the documented claim that the second feeds the first.

Choosing the metric is a strategy decision in disguise, which is why it is hard and why it is worth doing: it forces the company to state, in one measurable sentence, what value it believes it creates and for whom.

## When to use it

- When setting OKRs, so key results ladder up to one shared definition of value instead of five departmental ones.
- When writing the success metrics section of a PRD, to check that the feature's metric feeds an input on the tree rather than inventing a private definition of winning.
- When running a metrics review, as the frame for asking whether the inputs moved, whether the north star followed, and whether the causal claim between them survived contact with reality.

**Skip it when:** nothing is instrumented yet. A north star named before anything can be measured is a slogan, and it will be quoted for a year with no number behind it. Build the measurement first, then name the metric it makes possible.

## The trap: vanity metrics

The counterfeit north star is the number that only goes up: cumulative signups, registered users, total downloads, page views. Monotonic metrics measure the passage of time wearing a growth costume. They cannot disappoint, which is precisely why they cannot inform; a metric that cannot go down when customers stop getting value is not measuring value. The related counterfeit is the activity metric, sessions or clicks, which measures motion through the product rather than progress for the customer. The test for a candidate north star: if every customer silently stopped benefiting tomorrow, would this number fall within the quarter? If not, it is decoration, and the strategy it was supposed to encode is still unwritten.

## Used by

- [OKRs](../templates/planning/okrs.md)
- [Metrics review](../templates/operate/metrics-review.md)
- [PRD](../templates/definition/prd.md)
- [Growth plan](../templates/planning/growth-plan.md)
- [North star sheet](../templates/planning/north-star-metric.md)
- [Analytics instrumentation spec](../templates/delivery/analytics-instrumentation-spec.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [North star input tree](../frameworks/metrics/north-star-input-tree.md), the tree, its owners, and the lead against lag split
