# OPERATE bank

Stage: OPERATE, feeds Gate 6 (outcomes verified) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md), which loops back to DISCOVER.
Working handoffs: metric evidence via the [product analyst](../../product-analyst/SKILL.md); the accepted answers fill [../../../templates/operate/metrics-review.md](../../../templates/operate/metrics-review.md) and the workspace copy of [../../../templates/planning/growth-plan.md](../../../templates/planning/growth-plan.md).
Applies: the north star method in [../../../knowledge/north-star-metric.md](../../../knowledge/north-star-metric.md), one metric expressing delivered customer value, driven by input metrics teams can actually move. The Conductor names this method aloud when OPERATE-3 and OPERATE-5 run.
Questions 5 and 7 through 9 are the growth block; their accepted answers fill the growth plan.
Format and ladder: [README.md](README.md).

### OPERATE-1: the promised signal

Ask: Was the Gate 1 success signal measured, with the source system and the calculation stated?
Wrong costs: A signal promised at DISCOVER and unmeasured at OPERATE means the loop never closed and nobody can say whether the product worked.
Evidence class: 2, the measurement, source system and calculation shown.
Cross-examine when: the signal reported differs from the one DISCOVER-7 accepted, or the calculation is not shown. Move: naked numbers.
Accept when: the same signal, measured, with source system and calculation a reader could re-run.
Lands in: `operate/metrics-review.md` section 1, and STATE.md accepted answers.

### OPERATE-2: number versus number

Ask: For each key result, what is the number against the number?
Wrong costs: Adjectives grade themselves; a target either was hit or was not.
Evidence class: 2, actual versus target per key result. Adjectives are returned unanswered.
Cross-examine when: any result arrives as "strong", "on track", or "improving". Move: naked numbers.
Accept when: every key result scored actual against target, misses included.
Lands in: `operate/metrics-review.md` section 1, and STATE.md accepted answers.

### OPERATE-3: did the drivers move

Ask: Did the input metrics move, or did the headline move for an unrelated reason?
Wrong costs: A headline lifted by seasonality or a pricing change credits the product for weather.
Evidence class: 2, input metric movement examined alongside the headline.
Cross-examine when: the headline moved and no input did, and the answer waves at momentum. Move: banned openers, then: what else changed in the period?
Accept when: each input metric's movement is stated and the headline's movement is attributed or honestly marked unexplained.
Lands in: `operate/metrics-review.md` section 2, and STATE.md accepted answers.

### OPERATE-4: cost to run

Ask: What does this cost to run, in incidents, support volume, and on-call load?
Wrong costs: A product that hits its targets while burning its operators is a resignation letter on a delay.
Evidence class: 2, the operational numbers from their source systems.
Cross-examine when: "operationally it is fine" without counts. Move: naked numbers.
Accept when: incident count, support volume, and on-call load stated with sources for the review window.
Lands in: `operate/metrics-review.md` section 3 and `operate/operational-readiness-review.md`, and STATE.md accepted answers.

### OPERATE-5: the next bet

Ask: Which input metric is the next growth bet, and what is the cheapest experiment that would move it?
Wrong costs: Growth effort not aimed at an input metric is aimed at the headline, which no team can move directly.
Evidence class: the chosen input metric from OPERATE-3's examined set, plus an experiment with a cost attached.
Cross-examine when: the bet is on the headline itself, or the experiment starts at a quarter of work. Move: naked numbers, then: what is the version that costs a week?
Accept when: one input metric, one experiment, its cost, and what result would justify scaling it.
Lands in: the workspace growth plan, next bet section, and STATE.md accepted answers.

### OPERATE-6: persist, pivot, or sunset

Ask: Is the decision persist, pivot, or sunset, and what consequence is scheduled?
Wrong costs: The zombie portfolio is made of products where nobody decided anything.
Evidence class: one of exactly three decisions, with its consequence scheduled: the next DISCOVER pass, the pivot's Gate 1, or the sunset plan with dates and an owner.
Options: a) persist, which implies the next DISCOVER pass is scheduled. b) pivot, which implies a new Gate 1 with a date. c) sunset, which implies a plan with dates and an owner.
Cross-examine when: the answer is "keep watching it". Move: banned openers; watching is persisting without admitting the cost.
Accept when: one decision, one scheduled consequence with a date and an owner. The Conductor recommends, the humans at Gate 6 decide.
Lands in: `operate/metrics-review.md` section 5 and `execution/decision-log.md`, and STATE.md accepted answers.

### OPERATE-7: the loop behind the metric

Ask: What loop or channel actually drives the input metric you are betting on?
Wrong costs: An experiment on a metric with no mechanism behind it is a lottery ticket with a dashboard.
Evidence class: 2, the mechanism traced: who does what, which triggers the metric, observed at least once.
Cross-examine when: the mechanism is "word of mouth" or "virality" unobserved. Move: interest to behavior, show one instance of the loop completing.
Accept when: the loop or channel named, with one observed completion.
Lands in: the workspace growth plan, mechanism section, and STATE.md accepted answers.

### OPERATE-8: the counter-metric

Ask: Which counter-metric catches the damage if this experiment works for the wrong reason?
Wrong costs: Growth that cannibalizes trust reports as success right up until the churn arrives.
Evidence class: a measurable counter-metric with a threshold and the same review window as the experiment.
Cross-examine when: "there is no downside". Move: banned openers; an experiment with no conceivable damage is not changing anything.
Accept when: one counter-metric, one threshold, watched over the same window.
Lands in: the workspace growth plan, guardrail section, and `operate/metrics-review.md` section 3, and STATE.md accepted answers.

### OPERATE-9: the kill condition

Ask: What result kills the experiment?
Wrong costs: Experiments without kill conditions become programs, and programs without results become furniture.
Evidence class: an observable result plus a date, either of which ends it.
Cross-examine when: the condition is "if it clearly fails". Move: naked numbers.
Accept when: a result threshold and a date, and the owner who calls it.
Lands in: the workspace growth plan, kill condition section, and STATE.md accepted answers.

## Forced pair

On "advance anyway": OPERATE-1, then OPERATE-6. An unmeasured promise and an unmade decision are how a product joins the zombie portfolio, which is Gate 6's own skip warning.

## Gate 6 rendering

| Gate 6 checklist line | Evidenced by |
|---|---|
| Gate 1 signal measured, source and calculation stated | OPERATE-1 |
| Every key result scored number versus number | OPERATE-2 |
| Input metrics examined, not just the headline | OPERATE-3 |
| Operational load reviewed | OPERATE-4 |
| Decision is one of persist, pivot, sunset | OPERATE-6 |
| The decision's consequence is scheduled | OPERATE-6 |
| What this pass taught us, three sentences, filed findably | Drafted by the Conductor from the accepted answers, confirmed word by word by the user before filing |
