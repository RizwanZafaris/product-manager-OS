# OKRs

Based on the ideas of Andy Grove at Intel (High Output Management, 1983), popularized by John Doerr in Measure What Matters (2018).

## The essence

An OKR is two questions answered in public. The objective answers the question of destination: qualitative, directional, ambitious enough to matter, small enough in number to remember. The key results answer the question of pace, whether you are actually getting there: three to five measurable statements per objective, each with a baseline and a target, each falling due inside the cycle. Grove's original insight was that the pairing disciplines both halves. An objective without key results is a wish; key results without an objective are a dashboard with no destination.

The system's mechanics carry most of its value. OKRs are set partly bottom-up, because the people closest to the work know what is achievable and commit harder to what they authored. They are scored at cycle's end, and a score around 70 percent of an ambitious target is treated as success, because a team that scores 100 percent every quarter is sandbagging, not achieving. And they are deliberately decoupled from compensation, because the moment a key result prices a bonus, every baseline gets negotiated and every target gets padded, and the instrument stops measuring anything.

The three mechanics interlock, and each one fails without the others. Bottom-up authorship is what makes an ambitious target honest, because a target handed down is a demand and a target authored is a bet. The 70 percent norm is what makes ambition survivable, because it prices a miss as information rather than failure. Decoupling from pay is what keeps the baseline true, because a person who is paid on the delta will negotiate the starting number first and the target second. Remove any one and the other two collapse: aspirational targets tied to a bonus produce padded goals, and honest goals scored as pass or fail produce goals set at what was going to happen anyway.

The count is also load-bearing rather than stylistic. Three to five key results per objective is the range where the set still describes one destination from several angles; at eight, the sheet has become a work log and no reader can say what would count as a good quarter. The same logic caps objectives: a team with six objectives has stated no priority, and the first genuine conflict of the quarter will be resolved by whoever is loudest, not by the sheet.

## Where it came from

Grove was adapting management by objectives, which Peter Drucker had proposed decades earlier and which had spread through large companies as a paperwork exercise. His addition was the second half of the pair: objectives had always been written down, and what they lacked was a small set of numbers that could contradict them. He also ran the system on a monthly rhythm in a manufacturing business, where the distance between a decision and its measurable effect was short.

Two features of the modern practice make more sense with that lineage in view. The cascade instinct is inherited from management by objectives, not from Grove, whose version pushed authorship down rather than pushing targets down. And the quarterly cycle, carried into software by John Doerr's arrival at Google in the late 1990s, is a compromise with a business whose metrics respond more slowly than a fabrication line's, which is why so many teams find their key results only half-answerable at the moment they are scored.

## What the system assumes

1. **The outcome is uncertain and within the team's influence.** A key result must be able to fail, which rules out committed work with a known result, and it must be movable by the people who signed it, which rules out a metric another team owns. Break the first and scoring is theater; break the second and the team learns that the sheet describes their luck.
2. **Measurement predates the cycle.** A baseline requires history. A target without a baseline cannot be scored, because nobody can say afterwards whether the number moved or the definition did, and the argument at cycle's end will be about the instrument rather than the result.
3. **The metric responds inside the cycle.** If the effect takes two quarters to show, scoring at the end of one measures noise and teaches the team that their good work scored badly. Either pick a leading input on the same tree, or run that ambition as an annual objective with quarterly inputs beneath it.
4. **Scores buy nothing.** Decoupling is a precondition, not a nicety. It is the only reason a team will write down a baseline that makes them look bad in week one.

## When to use it

- When filling the OKR template: it asks for baseline, target, and scoring cadence per key result because this card says a KR without them is not one.
- When connecting a roadmap to intent: each initiative should name the key result it serves, or explain why it is on the roadmap at all.
- When running a quarterly metrics review, as the scoring ritual: score, learn, reset, and resist the urge to explain a 0.3 into a 0.7.

**Skip it when:** the quarter is one committed migration with an external date. That is a plan, and dressing it as an objective with key results adds ceremony without adding clarity. Run it as a program with a gate and keep the OKR sheet for the work where the outcome is genuinely uncertain.

## A worked case, ILLUSTRATIVE

Rowan is an invented onboarding tool for small employers. Every number is made up. The draft objective read "Ship the redesigned setup wizard", with three key results: design signed off, wizard released to all accounts, help center updated. All three shipped in week nine and the set scored 1.0 in a quarter where nothing about the business changed. That is the failure the next version was built to prevent.

The rewritten objective: "A new employer can run their first payroll without talking to us." Three key results, each with a baseline and a target inside the cycle.

| Key result | Baseline | Target | Result | Score |
|---|---|---|---|---|
| Share of new accounts reaching first payroll unaided | 41 percent | 60 percent | 52 percent | 0.58 |
| Median days from signup to first payroll | 11 | 6 | 7 | 0.80 |
| Setup tickets per hundred new accounts | 34 | 18 | 31 | 0.19 |

Scoring is proportional progress from baseline to target, so the first row reads eleven points of movement against a nineteen-point ask. The set averages near 0.5, which sounds like a bad quarter and is in fact the most useful sheet Rowan had produced, because the third row disagrees with the first two. Accounts got to first payroll faster and mostly unaided, and they still called. The team's assumption had been that tickets were caused by the wizard; the split says something else generates them, and the honest next move is a discovery pass on what the remaining callers were actually stuck on, not another wizard iteration.

The objective earned its keep here too. Read alone, the three rows are a mixed report; read against "a new employer can run their first payroll without talking to us", the ticket row is the one that says the objective was not met, whatever the average says. That is the work an objective does that a dashboard cannot: it tells you which row to believe when the rows disagree.

Notice what the ticket row cost. It was the row most likely to score badly and the row that carried all the information, which is exactly the trade a team declines when scores decide bonuses. Notice also that the third row is stated per hundred new accounts rather than as a raw count. A raw ticket count would have fallen on its own during a slow signup month, and a key result that improves when the business shrinks is not measuring the team.

## The trap: key results that are tasks

The most common corruption is quiet: "Launch the new onboarding flow" appears in the KR column. That is a task. It can be completed while the world remains entirely unchanged, which is exactly the property a key result must not have. The distinction is checkable: a task is something you do, a key result is something that becomes true in the world and can fail even when every task shipped. Activation rate moving from a stated baseline to a stated target can fail after a flawless launch, and that possibility of failure is what makes it information. Teams write task-KRs because tasks are controllable and outcomes are frightening, but an OKR sheet full of tasks is a project plan wearing a strategy's clothes, and it will score 1.0 in a quarter the product went nowhere.

The reason teams keep writing them is worth stating plainly, because scolding does not fix it. A task-KR is a promise a team can keep by working hard, and an outcome-KR is a bet that can be lost by a team that did everything right. Asking people to sign the second is asking them to accept public risk, and they will only do it in an organization where a 0.5 with a clear lesson is treated better than a 1.0 with none. The failure is cultural, and the sheet only reports it.

The disguise gets better than "launch". Watch for the milestone in metric clothing: "onboarding redesign live for all segments" has a percentage attached and is still a task, because the percentage counts rollout rather than result. Watch too for the effort metric, "run twelve customer interviews", which is a commitment worth making and belongs in the plan, not in the column that reports whether the customer's world improved. One question separates them in every case: could this be fully true at quarter's end with the customer no better off? If yes, it is a task, however many digits it carries.

## Other ways it fails, and the tell for each

- **The cascade that becomes a translation.** Each level restates its parent's key result as its own objective, and by the fourth level a team owns a fragment nobody can connect to a customer. The tell: a team can recite its key result but not name the company outcome it feeds. Alignment means each level names the parent it serves and chooses its own path there, not that each level receives a smaller copy.
- **Guardrail-free ambition.** A key result pursued alone gets hit at the expense of something unmeasured: conversion rises and refunds rise with it. The tell: the sheet has no metric that is supposed to stay flat. Every set needs at least one number defined as a floor, not a target.
- **The rewrite in week ten.** The target moves when the miss becomes visible, and the sheet ends the quarter green and evidence-free. The tell: the version history shows a target change with no accompanying note about what was learned. Targets can legitimately change when the world changes; the change is logged with a date and a reason, or it never happened.
- **Metric definition drift.** The number improves because the definition loosened. The tell: the same key result would produce two different values depending on which query ran, and nobody can produce the query. A key result needs a definition in the metrics dictionary before it needs a target.
- **Orphaned roadmap.** The sheet is set, filed, and never consulted while the roadmap is decided by escalation. The tell: no initiative on the roadmap names a key result, and no key result would change if the roadmap did.
- **The set nobody could fail.** Every target sits within reach of the current trend, so the quarter scores near 1.0 and the sheet has predicted the future rather than shaped it. The tell: extend last quarter's line on each chart and it lands on this quarter's target.
- **Too many owners on one key result.** Shared ownership reads as collaboration and behaves as absence, because at scoring time each owner can point at the other's half. The tell: a row with a team name instead of a person's name in the owner column.
- **Scoring as a performance review.** People start explaining rather than learning. The tell: the scoring meeting produces reasons and no reset, and the following quarter's targets sit suspiciously close to last quarter's actuals.

## How it gets gamed

The reliable exploit is the baseline, not the target. Everyone reviews the target, because it is the ambitious-looking number; almost nobody re-derives the baseline, which is quietly the other half of the fraction. A baseline picked from the worst week of last quarter buys twenty points of scored progress before any work happens. Its tell is a mismatch of windows: the baseline is a point in time and the result is an average, or the reverse.

Padding the target is the amateur version of the same trick, and it is easy to catch because an unambitious target looks unambitious. A shifted baseline looks like diligence.

The second exploit is definitional. Choose the metric whose measurement you also own, and the number becomes editable. The defense is boring and works: baselines are computed for the trailing period, using a definition written in the metrics dictionary, by someone who is not scored on the result, and the query is attached to the sheet. If that feels like distrust, remember what the alternative buys: a set of numbers that can only go up, which is the same information as no numbers at all.

The shortest test of a finished sheet: read it to someone outside the team and ask what this product is trying to do this quarter. If they can answer, the objective is doing its job; if they can only list activities, the set is a plan.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| A key result that can be fully true while the team's plan fails, and false while it succeeds | A key result that becomes true the moment the planned work ships |
| Baseline computed for a stated trailing window, with the query attached | Baseline asserted in the sheet with no window and no source |
| Three to five key results describing one destination from different angles | Eight key results describing the quarter's task list |
| At least one guardrail number defined as a floor, published beside the targets | Targets only, with the side effects discovered by support in week eleven |
| A miss discussed as evidence, with the next question named | A miss discussed as a reason, with the target quietly adjusted |
| Targets authored by the team and challenged by the manager | Targets issued by the manager and accepted by the team |
| Every roadmap initiative names the key result it serves | A roadmap and an OKR sheet that could be swapped between products unnoticed |

## Where it sits in the loop

- Stage: PLANNING, at the start of a cycle, and OPERATE at the end of it when the set is scored. The sheet is written once and read weekly.
- Upstream: the [product strategy](../templates/planning/product-strategy.md) supplies the intent, and the [north star input tree](../frameworks/metrics/north-star-input-tree.md) supplies inputs a key result can legitimately name.
- Downstream: the [roadmap](../templates/planning/roadmap.md) traces each initiative to a key result, and the [metrics review](../templates/operate/metrics-review.md) grades progress against the baselines.
- On trial at [Gate 6: outcomes verified](../os/STAGE-GATES.md), which is where a task-shaped key result is finally exposed, because the gate asks what changed for the customer rather than what shipped.
- Reviewed by the [OKR critic skill](../skills/okr-critic/SKILL.md) before publication, which is cheaper than discovering the defect at scoring.

## What it is not for

- **Committed delivery with a date.** A migration, a scheme mandate, or a contracted launch is a program with a gate. Scoring it 0.7 is meaningless, because there is no partial credit for a cutover that did not happen.
- **Cataloguing the team's work.** OKRs cover the change the team intends to cause; keep-the-lights-on work, support rotations, and debt paydown are real and belong in the capacity plan, not on the sheet. A team that tries to represent all of its work in key results ends up with eleven of them and no priority.
- **Individual performance measurement.** The moment a key result appraises a person, the padding begins. Grove's separation of the two systems is the load-bearing part of the design, not a cultural preference.
- **Setting strategy.** OKRs express a strategy that already exists. A team that cannot say why this objective and not another has used the sheet to skip the harder document, and no amount of measurable key results will supply the missing diagnosis.
- **Very short horizons.** Under about six weeks, a metric has no time to respond and the sheet becomes a task list again. Use an appetite and a bet for that horizon instead.

## Variants worth knowing

- **Grove's original at Intel** was tighter and more operational than what most companies now run: fewer key results, monthly review, and an explicit pairing of an activity indicator with an output indicator, so effort was never graded as its own result. See [High Output Management](high-output-management.md) for the frame it came from.
- **Committed against aspirational**, from Google's practice: committed OKRs are expected to reach 1.0 and are used for work with a floor, while aspirational ones are expected to land near 0.7. The two are scored differently and mixing them on one sheet without a label is how a committed miss gets excused as ambition.
- **V2MOM**, from Marc Benioff at Salesforce, adds explicit obstacles and measures to a vision and values statement. Worth knowing because the obstacles section names what OKRs leave implicit.
- **Health metrics or guardrails**, a common and useful addition: a small set of numbers that must not move, published beside the key results, which is the cheapest available protection against a single-metric optimization.
- **Annual objectives with quarterly key results**, the right shape when the outcome you care about genuinely takes a year to move. It keeps the ambition at the altitude where it is true and puts the leading inputs on the cycle where they can be scored, which is the honest fix for the response-lag assumption above.
- **Company-level only**, a deliberate simplification for organizations under roughly fifty people. One shared set, no cascade, no per-team sheets. Often the right answer, and always better than a cascade nobody maintains.

## Used by

- [OKRs](../templates/planning/okrs.md)
- [Roadmap](../templates/planning/roadmap.md)
- [Metrics review](../templates/operate/metrics-review.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [North star input tree](../frameworks/metrics/north-star-input-tree.md), supplies the measurable inputs a key result can name
- [OKR critic](../skills/okr-critic/SKILL.md), the review pass that tests every key result for the failure modes above
- [Metrics dictionary](../templates/operate/metrics-dictionary.md), where a key result's definition lives before it gets a target
- [North star metric](north-star-metric.md), the card that explains why the parent number is chosen the way it is
