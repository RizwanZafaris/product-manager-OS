---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/operate/metrics-dictionary.md", "templates/planning/capacity-plan.md", "templates/operate/metrics-review.md"]
method: "knowledge/INDEX.md"
aliases: ["SPACE Framework", "space-framework"]
---
# SPACE Framework

Based on the ideas of Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, and Jenna Butler, from "The SPACE of Developer Productivity" (ACM Queue 19(1), 2021). Explained here in this repository's own words.

## What it is for

The meeting where someone senior asks for one number for how productive the team is, and the room reaches for whatever the tooling already emits: merged pull requests, story points, tickets closed. The argument in the paper is that productivity is not one thing. It has five dimensions (satisfaction and well being, performance, activity, communication and collaboration, efficiency and flow), and any single metric held up alone is optimized until it stops describing the work. This worksheet turns that argument into a rule the sheet can fail on: a slate covering fewer than three dimensions, or three dimensions with nothing asked of a human, is not quotable, and "the slate is incomplete" is the answer the meeting gets. It also settles the sibling argument, the one where a tool is bought on a promise of speed and nobody wrote down beforehand what evidence would count.

## Run it when

- A leader asks for a single productivity number and wants it on a dashboard by Friday
- A tool, a process change, or an AI assistant is bought on the claim that it makes the team faster, and somebody has to say now what would count as evidence later
- Two squads are being compared, or a reorg is being argued from a velocity chart
- The team is visibly busy and the roadmap is visibly late, and nobody can say where the time goes

**Skip it when:** the constraint is already known and gets named in standup every morning. One shared staging environment with a queue, one approver for every release: instrumenting five dimensions to rediscover that spends a cycle producing a chart of the thing everyone can already say out loud. Fix the bottleneck, then baseline.

## Inputs you need first

- The question in the asker's words, and the decision it changes, which is usually a hire, a purchase, or a process change
- A repeated survey with wording that does not change between runs, from the [feedback program](../../templates/operate/feedback-program.md); satisfaction is asked, never inferred from telemetry
- State timestamps out of the tracker, so waiting time is a fact rather than a feeling; entity and period conventions come from the [metrics dictionary](../../templates/operate/metrics-dictionary.md), section 1
- A baseline window that closes before the intervention starts, and the team's shape on that date from the [capacity plan](../../templates/planning/capacity-plan.md), section 2

## The worksheet

### The five dimensions

| Dimension | What it measures | Usual instrument | What it cannot see |
|---|---|---|---|
| Satisfaction and well being | Whether people are fulfilled by the work and whether the pace is sustainable | Survey, same wording every run | Anything about output |
| Performance | The outcome of the work as shipped: does it hold up in production and for the customer | Change failure rate, escaped defects, the outcome metric the work targeted | The human cost of getting there |
| Activity | Counts of output: commits, reviews, deploys, tickets closed | System telemetry, free and therefore tempting | Value, quality, and whether the work was needed at all |
| Communication and collaboration | How work and knowledge move: review latency, discoverability, time to a first useful contribution | Telemetry plus survey | Whether the talking produced decisions |
| Efficiency and flow | Completing work with little delay or interruption: flow time, waiting time, handoff count | Value-stream telemetry, plus a survey question on interruption | Whether the fast work mattered |

### Step 1: frame the question and the level

| The question in the asker's words | What they will do with the answer | Level: individual, team, or system | Period and baseline window | Will any row reach a performance review or a cross-person comparison? |
|---|---|---|---|---|
| [question] | [the decision] | [level] | [window, dates] | no |

Rule: the last cell reads no, or the sheet stops here. Individual-level rows exist for the person's own use; the moment a row can be read as a ranking, every telemetry row becomes a target and starts describing what people do when counted.

### Step 2: the slate

One row per dimension. A dimension you are not measuring stays in the table with the reason written in, because an empty row is evidence and a deleted row is not.

<!-- Fill the gaming column before the guardrail column. If you cannot write down how a metric rises while the work gets worse, you do not understand the metric well enough to publish it. -->

| Dimension | Metric (numerator / denominator, period) | Level | Perceptual or telemetric | Owner (one name) | Baseline (date) | How it rises while the work gets worse | Guardrail that catches that |
|---|---|---|---|---|---|---|---|
| Satisfaction and well being | | | perceptual | | | | |
| Performance | | | | | | | |
| Activity | | | telemetric | | | | |
| Communication and collaboration | | | | | | | |
| Efficiency and flow | | | | | | | |

Rules: exactly one owner per row; a metric needs a numerator, a denominator, and a period; satisfaction is perceptual by definition and cannot be swapped for a proxy like hours logged; a row with an empty gaming column is not finished and does not count toward coverage.

### Step 3: the coverage arithmetic

Score each dimension: 0 nothing measured, 1 a metric named but missing an owner, a baseline, or a source, 2 instrumented with a named source, a baseline date, an owner, and a filled gaming column. Coverage total is the five scores summed, out of 10. The scale is deliberately coarse because the only decision it drives is quotable or not; a finer scale invites an argument about whether a dimension is a 6 or a 7 when the question is only whether it is covered, half covered, or absent.

Let D be the count of dimensions scoring 2. The gate is D, not the total.

| Check | Arithmetic | Pass condition | Result |
|---|---|---|---|
| Three dimensions, minimum | D = dimensions scoring 2 | D is 3 or more | [pass or fail] |
| Something was asked, not only logged | Perceptual rows among the dimensions scoring 2 | 1 or more | |
| Activity is not carrying the slate | D minus 1 if Activity scored 2 | 2 or more | |
| Every row is gameable on paper | Rows with both the gaming move and its guardrail written / rows scoring 2 | equals 1 | |
| No row is a ranking | Individual-level rows appearing in any cross-person comparison | 0 | |

A slate failing any check is not published and not quoted. A total of 7 with D at 2 fails: two thoroughly instrumented dimensions are a confident half-picture, which is the failure mode the paper is about.

## Reading the result

Read the rows in pairs. A single row moving is not a finding; two rows moving against each other is.

| What you see | What it means | The action it implies |
|---|---|---|
| Activity up, performance flat or down | More output, no better result: rework, or work nobody needed | Stop the hiring conversation and look at what the extra output was for |
| Activity up, satisfaction down | Speed bought from people, usually with overtime or skipped review | Read the free-text answers before the next planning round; this one has a shelf life |
| Efficiency up, communication down | Waiting time fell because review became a rubber stamp | Check the guardrail on review depth; the flow-time gain is likely borrowed against a later defect |
| Performance up, activity down | The team stopped doing work that did not matter | Defend it out loud, because it looks like a slowdown on any activity dashboard |
| Efficiency flat while activity is healthy | The team is waiting, not slow; the constraint sits outside the team | Take it to the [five whys](../execution/five-whys-fishbone.md), then to the tech debt register or the dependency owner |
| Satisfaction up, everything else flat | A calmer period, not a faster one, or the survey went out the week after a launch | Check the send date before reporting it |

Any dimension scoring 1 names its own next task: an instrumentation change, dated and owned, not a caveat in a footnote. And no combination of the five answers whether the work was worth doing; performance measures the outcome of the work as shipped, not whether the bet was right. That question belongs to the [north star input tree](north-star-input-tree.md).

**The decision it feeds:** whether the next cycle buys capacity (people, tools, licences) or buys flow (removing waiting, handoffs, and single approvers), and whether a vendor's or a team's productivity claim is allowed to change the staffing assumption.

**Where the output lands:** the slate becomes rows in the [metrics dictionary](../../templates/operate/metrics-dictionary.md), section 2; the read lands in the [capacity plan](../../templates/planning/capacity-plan.md), section 7, as the assumption the plan rests on.

**Re-run trigger:** re-run at the start of each planning period, and inside a period whenever the team changes shape (a joiner, a leaver, a split, a new manager) or a tool claiming a productivity gain is rolled out; baselines that predate the current team describe a team that no longer exists.

## ILLUSTRATIVE example

Invented figures throughout, for the squad building Ledgerline's expense-report copilot, after the wave 2 slip. The ask: merged pull requests per engineer per week, on a weekly slide. Level: team. Baseline window: the eight weeks before the copilot's policy-rules work started. Nothing on the slate reaches a review, and the sheet says so in step 1.

| Dimension | Metric (ILLUSTRATIVE) | Instrument | Owner | Baseline (ILLUSTRATIVE, quarter start) | Gaming move | Guardrail |
|---|---|---|---|---|---|---|
| Satisfaction | Share answering 4 or 5 of 5 to "I can do my best work here", quarterly | perceptual | engineering manager | 61% | Send it the week after a good launch | Fixed send date, read with the free text |
| Performance | Releases needing a fix or a rollback / releases, monthly | telemetric | release manager | 18% | Fewer, larger releases hide failures | Releases per month, floor of 4 |
| Activity | Deploys to production per week | telemetric | release manager | 6 | Splitting one change across many deploys | Read only against the performance row |
| Communication | Median hours from review requested to first review | telemetric | tech lead | 31 | Approvals with no comments | Merges with zero review comments, ceiling 25% |
| Efficiency and flow | Median flow time in days, and waiting share = time in waiting states / flow time | telemetric | copilot PM | 9.5 days; waiting share not yet computable | Opening tickets late so the clock starts late | Work in progress, ceiling of 2 per engineer |

Coverage (ILLUSTRATIVE): satisfaction 2, performance 2, activity 2, communication 2, efficiency 1, total 9 of 10. Efficiency scores 1 because waiting states carry no timestamps; a two-week tracker change, owned by the copilot PM, fixes it. D is 4, one of them perceptual, three of them not activity, so the slate publishes.

The read: activity was never the problem, and the two rows that mattered were efficiency and communication. Once the timestamps landed, waiting share came out at 62% of flow time (ILLUSTRATIVE), and most of the waiting sat in one place, a single finance approver for every policy-rule change. Two more engineers would have added output to a queue. The cycle bought a second approver and a batching rule instead, and the capacity plan's assumption was rewritten from "throughput is limited by engineers" to "throughput is limited by policy sign-off".

## The trap

The one number that survives the meeting. Five columns do not fit on a slide, so the deck carries a single team-productivity tile, and it is the activity row because that is the one telemetry gives away free. Within a quarter the tile is a target: changes get split to raise the count, reviews get rubber-stamped to clear the queue, tickets get opened late so the flow clock starts late, and every one of those moves looks like improvement.

The instrument produces confident nonsense under four conditions worth naming. Individual rows used to compare people: the telemetry stops measuring the work and starts measuring what people do when they know they are counted. A survey whose wording was tidied up between runs, or sent right after a launch: the satisfaction row is no longer comparable, and it is the row that would have caught the cost of the speed. A slate read one row at a time, where each row is defensible alone and the tradeoff only exists in the pair. And a period containing a reorg, a long holiday, or a team of three, where one person's month moves every number and the denominator changed underneath the comparison. In all four the sheet still fills in cleanly, which is what makes it dangerous.

## Feeds

- [Metrics dictionary](../../templates/operate/metrics-dictionary.md), section 2, one row per slate row, driven by the [metrics-tree skill](../../skills/metrics-tree/SKILL.md)
- [Capacity plan](../../templates/planning/capacity-plan.md), sections 2 and 7, where the supply number and its assumption are argued
- [Metrics review](../../templates/operate/metrics-review.md), section 3, where the guardrails are read against the metrics they guard
- [Retrospective](../../templates/execution/retrospective.md), section 2, which takes the satisfaction and flow rows as facts rather than impressions
- [Tech debt register](../../templates/execution/tech-debt-register.md), section 2, for waiting and handoff findings that are debt rather than actions
- [Dashboard spec](../../templates/operate/dashboard-spec.md), section 3, where the slate is laid out as a set of tiles that cannot be read one at a time
- [Decision log](../../templates/execution/decision-log.md), for the capacity-or-flow decision the read produced
- BUILD and OPERATE, at each cycle boundary in the [operating loop](../../os/OPERATING-LOOP.md), and at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Sibling worksheets: [HEART metrics](heart-metrics.md) for the user's experience of the product, this sheet for the team's experience of building it
- Method background: [knowledge index](../../knowledge/INDEX.md); the source above is the reference
