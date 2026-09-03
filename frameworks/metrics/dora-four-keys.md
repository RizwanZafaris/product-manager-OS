---
layer: frameworks
stage: DELIVER
gate: 5
feeds: ["templates/operate/metrics-review.md", "templates/operate/incident-postmortem.md", "templates/delivery/release-readiness.md"]
method: ""
aliases: ["DORA Four Keys", "dora-four-keys"]
---
# DORA Four Keys

Based on the delivery-performance research of Nicole Forsgren, Jez Humble, and Gene Kim, reported in Accelerate (2018). Explained here in this repository's own words.

## What it is for

Four numbers that describe how a team moves a change from a developer's machine to a customer: how often it deploys, how long a change waits, how often a deploy breaks something, and how fast service comes back. Two of them measure throughput (deployment frequency, lead time for changes) and two measure stability (change failure rate, time to restore service). They settle the argument that returns every planning period: engineering says the delivery system is why dates slip, product hears "it feels slow", and neither side is holding an instrument. The research behind these four found throughput and stability moving together in the teams that did well, which makes "deploy less often so we break less" a claim to test rather than a truism to accept. For a PM the payoff is narrower and more useful than a DevOps scorecard: these numbers set what a roadmap date can honestly promise, and they turn a request for platform time into a costed argument.

## Run it when

- Before a planning period, when engineering asks for delivery-system work and the case on the table is a feeling
- After an incident review where "release less often" is being proposed as the fix
- When a roadmap commits to a date whose release cadence nobody has measured
- Before and after a change to how the team ships (a branching change, a test-suite rebuild, a new approval step), so the change has a before

**Skip it when:** the team ships on somebody else's calendar. On a vendor-scheduled quarterly release or an embedded release train, three of the four keys are set upstream; measure lead time to the release cut and use the [estimation sheet](../execution/estimation-sheet.md) for the rest.

## Inputs you need first

- Production deployment records for one named service, with a timestamp each, from the build and release system
- Commit timestamps joined to those deployments, so lead time is measured rather than remembered
- Incident records carrying an impact-start time and a restored time, from the [incident postmortem](../../templates/operate/incident-postmortem.md), section 1
- One service or application to measure; a figure averaged over a portfolio describes nobody
- Your own previous period's four figures, because this sheet compares you to you

## The worksheet

### Step 1: agree the four definitions before anyone reads a number

| Key | Clock starts | Clock stops | Counting rule | Source system | Value this period | Same figure last period |
|---|---|---|---|---|---|---|
| Deployment frequency | [n/a, it is a count] | | [one promotion of one artifact to production counts once, whatever it contains] | | [per week] | |
| Lead time for changes | [first commit on the branch] | [the change is serving production traffic] | [report the median and the 85th percentile] | | | |
| Change failure rate | [n/a, it is a ratio] | | [a deployment "failed" if it needed a remedial deployment: hotfix, rollback, forward fix, config revert] | | | |
| Time to restore service | [impact began: state detection or first customer effect, and never change the rule] | [service restored, not root cause found] | [report the median and the worst case] | | | |

The arithmetic, written out because a delivery figure whose formula lives in a dashboard is a number nobody can audit:

- deployment frequency = production deployments in the window / weeks in the window
- lead time for one change = time serving production minus time of first commit; the reported figure is the median of those, with the 85th percentile beside it, because the mean belongs to the oldest branch
- change failure rate = deployments needing a remedial deployment / all production deployments in the window, times 100; the denominator is deployments, never incidents and never changes
- time to restore for one incident = time restored minus time impact began; report median and worst

### Step 2: score the direction of travel

Scale per key, against your own previous period: minus 1 worse, 0 unchanged, plus 1 better. "Unchanged" means inside the noise band, where the noise band is 20% of the previous period's value, floored at one deployment per week for frequency and at one hour for time to restore. Add the four rows for a total between minus 4 and plus 4.

| Key | Previous | This period | Change | Noise band | Score (minus 1, 0, plus 1) |
|---|---|---|---|---|---|
| Deployment frequency | | | | | |
| Lead time (median) | | | | | |
| Change failure rate | | | | | |
| Time to restore (median) | | | | | |
| | | | | **Total** | |

Why the scale is this coarse: the timestamps underneath it are worse than the scale. Deploy logs miss manual releases, incident clocks start when a human noticed, and lead time moves with branching habits that changed mid-quarter. A ten-point scale would produce arguments about whether a figure is a six or a seven while the input is hours wrong. Three points is what the data supports, and the total is a conversation opener rather than a grade: a plus 2 built from throughput while stability fell is not a plus 2, it is two separate findings.

### Step 3: decompose the worst key

The stages must sum to the median within a working day. If they do not, the pipeline holds a step nobody has written down, and finding that step is the result.

| Stage (lead time) | Median time | Share of lead time | Who is waiting | Fix candidate |
|---|---|---|---|---|
| First commit to review requested | | | | |
| Review requested to merged | | | | |
| Merged to build and tests done | | | | |
| Tests done to release approved | | | | |
| Approved to serving production | | | | |

For time to restore, run the same shape over detect, page, diagnose, remediate, confirm.

### Step 4: one counter-metric per key

Each of these four moves without anything improving. Report the counter beside the key or do not report the key.

| Key | How it moves without improving | Counter-metric reported beside it | Owner |
|---|---|---|---|
| Deployment frequency | Empty deployments; one artifact split into several promotions | Share of deployments carrying no customer-visible change | |
| Lead time for changes | The branch is cut late, so the clock starts late; work waits in a queue before the first commit | Age of the oldest open change, timed from when work started | |
| Change failure rate | Incidents go unrecorded, or a failure is relabeled a planned follow-up | Remedial deployment count taken from the deploy log, not the incident log | |
| Time to restore service | The clock starts at declaration rather than at impact | Time from first customer report to declaration | |

## How to read the result

Read the pairs, then the total. Throughput better and stability held is a delivery system improving; name the change that did it before someone else claims it. Throughput better and stability worse usually means batch size fell while the safety net did not move, so the tests, the rollback, or the review are no longer catching what a slower cadence used to catch by accident. Throughput flat and stability worse is a system under load; read the decomposition before anyone proposes a process. All four flat across three periods, with a loud complaint about slowness, means the complaint is about something these four cannot see, most often the wait before the first commit, which is a product decision problem wearing an engineering costume. A change failure rate near one deployment in two outranks every other row: the team ships twice for each change that lands, and the frequency figure is counting repair work as progress.

Where the reported bands live: the annual State of DevOps report sorts teams into named performance groups with a range per key, re-derived from each year's survey, so the numbers shift year to year and a band quoted from memory is usually a band from a different year. If you want that comparison, read the current report at https://dora.dev/research/ and write the year into the sheet. This worksheet asserts no band, and you against you last period is the more actionable comparison anyway.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot, one deployable service, four weeks measured against the previous four. All figures ILLUSTRATIVE.

| Key | Previous | This period | Noise band | Score |
|---|---|---|---|---|
| Deployment frequency | 1.0 per week | 1.5 per week | 1 per week (floor) | 0 |
| Lead time, median | 12 days | 9 days | 2.4 days | plus 1 |
| Lead time, 85th percentile | 26 days | 24 days | reported, not scored | |
| Change failure rate | 2 of 4 deployments, 50% | 3 of 6 deployments, 50% | 10 points | 0 |
| Time to restore, median | 5 hours | 7 hours | 1 hour (floor) | minus 1 |

Total: 0. Decomposition of the 9-day median lead time: first commit to review requested 1.0 day; review requested to merged 5.0 days; merged to tests done 0.5 days; tests done to approved 2.5 days, held by a weekly change-approval board; approved to production 0.2 days. The stages sum to 9.2 days against a 9-day median, so no hidden step is implied, and two stages hold 7.5 of the 9 days. Counters: 1 of the 6 deployments carried no customer-visible change (a config revert), so the frequency rise is thinner than the chart; the deploy log shows 3 remedial deployments, matching the incident log, so failures are not being under-recorded.

Reading: the total of 0 hides the finding. One deployment in two needs a repair, so the extra deploy the team earned this period went into fixing the last one, and the frequency chart rose while no more value shipped. The constraint is not cadence. It is a review queue plus a weekly board holding most of the lead time, with a test suite that misses policy-rule regressions doing most of the breaking. What went into planning was not "deploy less often" but two named items, a policy-rule test pack and a standing review slot, with the change failure rate as the number they are meant to move.

## The decision it feeds

Whether the next planning period buys delivery-system work, and how much of it. The output is one sized line of standing demand in the capacity plan, argued from four measured numbers instead of from a feeling, plus a ruling on the recurring "should we slow down to be safer" question in whichever direction the evidence actually points. It also sets the release cadence a roadmap date is allowed to assume.

## Where the output lands

- [Capacity plan](../../templates/planning/capacity-plan.md), section 4, standing demand: the reserved share for the constraint this sheet named
- [Tech debt register](../../templates/execution/tech-debt-register.md), section 2, one row per constraint the decomposition found, with the key it damages recorded as its interest
- [Metrics dictionary](../../templates/operate/metrics-dictionary.md), one row per key, carrying the clock rules agreed in step 1

## Re-run trigger

Re-run at the start of each planning period, and again four weeks after any change to how the team ships: a new approval step, a test-suite rebuild, a branching change, a team split, or on-call moving to a different group. Four weeks is the floor because over six deployments a single failure moves the rate about 17 points, so a shorter window measures luck.

## When this method misleads you

The four produce confident nonsense the moment they are read as a verdict on people rather than a description of a system. Put them on a leaderboard across teams and within a week they stop measuring delivery: deployments get split, incidents get renamed, restore clocks start late, and the sheet reports reporting behavior. They also mislead when the service boundary is wrong, because an average across a monolith, a nightly batch job, and a mobile app is actionable for none of them, and mobile carries a store review inside its lead time that no team-level change will move. The largest misread is quieter: all four keys can improve while the product gets worse, since none of them looks at a customer. Deployment frequency measures a conveyor belt, so pair these with the [north star input tree](north-star-input-tree.md) or you will optimize the belt. Finally, watch the denominators. Over six deployments one incident is worth about 17 points, so an improvement from 50% to 33% may be one release that happened not to break; report counts beside every rate.

## Feeds

- [Metrics review](../../templates/operate/metrics-review.md), section 2, where the movement is read against what was predicted
- [Incident postmortem](../../templates/operate/incident-postmortem.md), section 1, which supplies the restore clock and is corrected by it
- [Release readiness](../../templates/delivery/release-readiness.md), section 4 for rollback and section 5 for operations and monitoring
- [Testing strategy](../../templates/delivery/testing-strategy.md), whenever change failure rate is the worst key
- [Retrospective](../../templates/execution/retrospective.md), where the step 3 table is worth more than a round of feelings
- [North star input tree](north-star-input-tree.md), which keeps these four honest about customer value
- DELIVER and OPERATE, read at [Gate 5: release readiness green](../../os/STAGE-GATES.md) and again at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- The [release manager agent](../../agents/release-manager-agent.md) and the [postmortem-facilitator skill](../../skills/postmortem-facilitator/SKILL.md) both read this sheet
- Method background: the source named at the top of this file; the [knowledge index](../../knowledge/INDEX.md) carries no card for it yet
