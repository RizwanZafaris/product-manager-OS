---
layer: frameworks
stage: ALL STAGES
gate: 1
feeds: ["templates/planning/roadmap.md", "templates/planning/capacity-plan.md", "frameworks/prioritization/wsjf-cost-of-delay.md"]
method: "knowledge/INDEX.md"
aliases: ["Theory of Constraints", "theory-of-constraints"]
---
# Theory of Constraints

Based on the ideas of Eliyahu Goldratt, taught as a factory novel in The Goal (1984), whose five focusing steps are reworked here for a product team's delivery line. Explained here in this repository's own words.

## What it is for

Finding the one step in a delivery line that sets the pace of the whole line, then proving on paper that work aimed anywhere else buys nothing. The meeting it resolves is the one where cycle time has climbed for a quarter, every function reports itself busy, and the fix on the table is more people or a better tool for whichever function argued hardest. A line moves at the speed of its slowest station. Raise the throughput of any other station and you have bought a longer queue, not a faster line.

The output is one named station, an evidence score behind the naming, and a ranked list of what to do about it in an order that spends nothing before it spends anything. Most roadmaps fail the test in step 1. Four funded rows with three of them aimed at stations that are not the constraint is the normal result of a planning cycle that never asked the question.

## Run it when

- Cycle time has risen over two or more months while items shipped per month has not, and every function reports itself busy
- A quarter of funded work is about to be committed and nobody can say which step in the line each row speeds up
- Someone is asking for headcount, a tool budget, or an outsourcing contract in order to go faster
- The answer to "why is this slow" is "everything", or a different function each week

**Skip it when:** throughput is not the complaint. If work flows and the argument is about what to build, this sheet makes a team efficient at the wrong thing; run the [strategy kernel](../strategy/strategy-kernel.md) or the [RICE sheet](../prioritization/rice-scoring-sheet.md) instead. Also skip it for one team of five working one item at a time, where the queue is visible without a worksheet.

## Inputs you need first

- Stage transition dates from the tracker for the last 8 to 12 weeks, measured rather than remembered
- Every station an item passes on the way to live, including the ones you do not own: a shared platform team, a review board, a vendor, a regulator's window
- The funded rows for the next period, from the [roadmap](../../templates/planning/roadmap.md) Now and Next tables, so the throughput test has something to test
- What actually fills the week of the people at the slowest station, from them, not from the plan
- The [capacity plan](../../templates/planning/capacity-plan.md) section 2, for what each station's supply is on paper
- One rule agreed out loud before starting: stations get named, people do not

## The worksheet

### Step 1: identify the constraint

<!-- One row per station, in the order work passes through them. Arrival and completion are
     counts from the tracker over the same window, not opinions. Queue trend is the only
     column nobody can argue with, so fill it from three consecutive weekly readings. -->

| # | Station | Arrival (items per week) | Completion (items per week) | U = arrival / completion | Waiting now | Queue trend over 3 readings | Age of oldest waiting item |
|---|---|---|---|---|---|---|---|
| | [station] | [n] | [n] | [n] | [n] | [up / flat / down] | [days] |

System throughput equals the completion rate of the slowest station, whatever the rest of the line can do. U above 1 means the queue grows by (arrival minus completion) items every week, without limit, until someone throttles upstream or quietly works around the station.

Then score the candidate. Three observations, each worth 1 point, added.

| Test | What counts as a yes | Point |
|---|---|---|
| Queue | The longest queue on the line sits in front of this station, and it grew across the last three readings | [0 / 1] |
| Starvation | The station immediately downstream idles waiting for this one | [0 / 1] |
| Expedite | One item pushed to the front of this station's queue reached live measurably sooner than the median | [0 / 1] |

Evidence = the sum, 0 to 3.

| Evidence | What it means | What you may do |
|---|---|---|
| 3 | Confirmed constraint | Run steps 2 to 5 in order |
| 2 | Probable | Run the expedite test for one week, then decide. Exploit changes that cost nothing may start now |
| 0 to 1 | Not established | You are guessing. Fix the measurement before subordinating a whole line to a hunch |

The scale is three binary observations rather than a confidence rating because each test is either visible on the board or it is not, and a 1 to 5 rating buys an argument about whether design is a 3 or a 4 while changing nothing about what the team may do next. They add rather than multiply because they are three independent looks at one fact and none of them compounds: a growing queue with no starvation behind it is half a case and should score as half a case.

Then the test the rest of this repository exists to survive.

| Funded row | Station it improves | Is that the constraint? | Throughput bought (items per week) | Verdict |
|---|---|---|---|---|
| [roadmap row] | [station] | [y / n] | [n, or zero] | [keep / re-aim / park] |

A row aimed at a non-constraint station buys zero throughput by definition. It may still be worth doing for a reason that is not speed: a risk retired, a commitment met, a cost removed. Write that reason in the verdict cell. "It helps the team" is not one of them.

### Step 2: exploit the constraint

Get more out of the station before spending anything on it.

| Waste at the constraint | Share of the station's week it consumes | Smallest change that reclaims it | Owner | Hours per week recovered |
|---|---|---|---|---|
| [what the time goes to] | [percent] | [the change] | [one name] | [n] |

Rows worth checking every time: work at this station someone else could do; rework caused by input that arrived incomplete; idle time waiting for a decision nobody scheduled; multitasking across several items so everything is half done; and work that should never have entered the line.

Recovered capacity = station hours per week x share reclaimed. New completion rate = old rate x (1 + share reclaimed). Write both numbers down. Exploit is the only free step, and it is the step teams skip.

### Step 3: subordinate everything else to it

Every other station runs at the constraint's pace. This is the step that makes people angry, so it is written as rules with names against them.

| Station | Current local rule or metric | New rule that paces it to the constraint | What stops being measured | Who will object | Expiry review date |
|---|---|---|---|---|---|
| [station] | [the metric today] | [the new rule] | [what is dropped] | [one name] | [YYYY-MM-DD] |

Two rules do most of the work. Release new work into the line only when the constraint's queue falls below the buffer. Buffer = the constraint's completion rate (items per week) x the longest upstream delay you must absorb (weeks); keep it small, because a large buffer is the queue with a friendlier name.

Every row carries an expiry review date. A subordination rule is correct only while the constraint sits where you found it.

### Step 4: elevate the constraint

Only now, and only for the constraint.

| Option | What it does | Throughput bought (items per week) | Ongoing cost (engineer-years, 1.0 = one full-time person) | Lead time to effect (weeks) | Cost per added item per week |
|---|---|---|---|---|---|
| [option] | [mechanism] | [n] | [n] | [n] | [cost / throughput] |

Cost per added item per week = ongoing cost / throughput bought. Rank by that number, then break ties on lead time, because an option that pays off after the constraint has moved has bought nothing. Removing the step for a defined class of work is an option and belongs in the table.

### Step 5: repeat, because the constraint moves

| If the constraint's rate reaches | The next constraint is | At what rate | Which step 3 rules expire that day |
|---|---|---|---|
| [n] | [station] | [n] | [rule] |

Name the successor before you improve anything. Goldratt's own last warning is the one that bites: the rules written in step 3 outlive the constraint that justified them, and the sheet's own output becomes the next thing slowing the line.

## ILLUSTRATIVE example

Invented delivery line for Ledgerline's expense-report copilot, over a ten-week window. Every figure below is invented and ILLUSTRATIVE.

| # | Station | Arrival | Completion | U | Waiting | Trend | Oldest |
|---|---|---|---|---|---|---|---|
| 1 | Intake and shaping | 6 | 8 | 0.75 | 5 | flat | 4 days |
| 2 | Design | 6 | 7 | 0.86 | 4 | flat | 5 days |
| 3 | Build | 6 | 6 | 1.00 | 9 | up | 6 days |
| 4 | Model eval and prompt tuning | 6 | 2.5 | 2.40 | 16 | up | 26 days |
| 5 | Privacy and security review | 2.5 | 4 | 0.63 | 1 | flat | 2 days |
| 6 | Release and rollout | 2.5 | 5 | 0.50 | 0 | flat | 1 day |

Station 4 scores 3: the longest queue, rising by 3.5 items a week; station 5 idle two days in a normal week; one expedited item reached live in 9 days against a median of 31. System throughput is 2.5 items a week even though intake can shape 8.

The roadmap test, four funded rows.

| Funded row | Station | Constraint? | Throughput bought | Verdict |
|---|---|---|---|---|
| Faster intake triage tooling | 1 | no | zero | park |
| Design system components for the receipt table | 2 | no | zero | keep, retires a usability risk, not a speed row |
| A second build squad | 3 | no | zero, and it raises arrival at station 4 | park |
| Labeled receipt set and an automated eval runner | 4 | yes | plus 2.0 | keep, move to Now |

Three of four funded rows bought no throughput, and one of them made the queue worse.

Exploit, station 4, two engineers at 80 hours a week between them: 30 percent goes to hand-labeling receipts anyone could label (24 hours), 15 percent to waiting on the finance controller for rulings on ambiguous policy cases (12 hours), and whole suites are re-run because builds arrive with no pinned prompt version. Moving labeling out recovers 24 hours; a standing 20-minute Tuesday ruling slot recovers about half the waiting time, 6 hours. That is 30 of 80 hours, so 2.5 x 1.375 = 3.4 items a week, bought with no money.

Subordinate: intake releases work only when station 4's queue is below 5 items (buffer = 2.5 x 2 weeks of upstream variability). Build stops being measured on stories merged per sprint and takes prompt-version pinning as an entry condition. The build lead objects, by name, in the decision log. Expiry review at quarter end.

Elevate, three options.

| Option | Throughput bought | Ongoing cost | Lead time | Cost per item per week |
|---|---|---|---|---|
| Hire a second eval engineer | plus 1.7 | 1.00 | 16 | 0.59 |
| Buy a labeled corpus and an automated runner | plus 2.0 | 0.35 | 6 | 0.18 |
| Exempt copy-only changes from full eval, with the controller's sign-off | plus 1.2 | 0.05 | 2 | 0.04 |

Order: the exemption, then the corpus, and the hire only if the constraint holds after both. Repeat: at 3.4 + 1.2 + 2.0 = 6.6 items a week, station 4 stops being the constraint and build becomes it, at 6. The intake release rule expires that day, because from then on it throttles the line to protect a station that has stopped being the problem.

## Reading the result

Evidence 3 with a rising queue is the clean case: work the steps in order, and stop anyone who wants to start at step 4. Two stations that look tied are resolved by taking the upstream one, because a downstream queue can be an artifact of a station starved half the week and flooded the other half.

No station with a rising queue, and a line that is still slow, means throughput is not capacity-bound. The time is going to waiting between stations rather than work inside them, and this is the wrong instrument: run the [iceberg model](../systems/iceberg-model.md) on the handoff, or look at batch size.

A constraint you do not own (a platform team, a review board, a vendor, a regulator's window) cannot be exploited or elevated by you. You can subordinate to it and you can escalate it, and both are documented moves: a [dependency register](../../templates/execution/dependency-register.md) row and the [escalation skill](../../skills/escalation/SKILL.md). Do not write an exploit plan for another team and call it a decision.

If more than half the funded rows buy zero throughput, the finding is about the planning cycle rather than the line, and it goes to the roadmap conversation in exactly those words.

## The decision it feeds

Which funded rows survive the next planning cycle, and where the next hire or tool spend goes. Concretely: the contents of the roadmap's Now table, the demand side of the capacity plan, and whether the headcount request in front of the sponsor is aimed at the station that sets the pace or at the one that argued best.

## Where the output lands

- [Roadmap](../../templates/planning/roadmap.md), the Now table and the Parked and killed table, with the throughput column as the stated reason
- [Capacity plan](../../templates/planning/capacity-plan.md), section 3 (demand per initiative) and section 6 (gaps and hiring), where an elevate option becomes a request with arithmetic behind it
- [Decision log](../../templates/execution/decision-log.md), one entry per subordination rule, carrying the objector's name and the expiry date
- [Dependency register](../../templates/execution/dependency-register.md), when the constraint belongs to another team

## Re-run trigger

Re-run at the start of each planning period, and immediately whenever the constraint's completion rate reaches the successor rate named in step 5. Those are one event seen from two directions: the constraint moves when you improve it, and it moves again when the org changes shape, so a step 3 rule nobody has re-read this quarter is throttling the line for a reason that has expired.

## When this method misleads you

Four conditions produce confident nonsense.

Stage timestamps that are fiction. A team that drags cards in a batch on Friday afternoon gives every station the same apparent wait, and the longest queue on the sheet is a record of when someone tidied the board. Check whether transition times cluster on one weekday before believing any queue column.

A line that is not a line. Work that loops (design, build, redesign) shows its rework as a downstream queue, so the sheet points at the station receiving bad input instead of the one producing it. Measure a rework rate per station before trusting the map, or you will subordinate a whole team to a symptom.

Lumpy demand. A station that keeps up for three weeks and drowns in the fourth is a batching problem wearing a capacity problem's clothes. Elevating it permanently buys idle capacity for three weeks a month, and the month-end burst arrives anyway.

Inertia, which is Goldratt's own last warning. The intake freeze and the queue limit outlive the constraint, nobody remembers why they exist, and they get defended with "that is how we release work". The tell is a rule with no expiry date and no name against it.

The failure specific to a tired team is more common than all four. They run step 1, name the constraint correctly, skip exploit and subordinate because those steps cost political capital rather than money, and arrive at step 4 with a headcount request. The method is then remembered as the framework that asks for people, and the free capacity sitting inside the constraint's own week is never recovered.

## Feeds

- [Roadmap](../../templates/planning/roadmap.md) and [capacity plan](../../templates/planning/capacity-plan.md), as above
- [WSJF and cost of delay](../prioritization/wsjf-cost-of-delay.md), which sequences the queue in front of the constraint once you know which queue matters
- [Estimation sheet](estimation-sheet.md), whose duration ranges are the constraint's completion rate seen one item at a time
- [Iceberg model](../systems/iceberg-model.md), when the constraint turns out to be a policy or an incentive rather than a capacity
- [Five whys and fishbone](five-whys-fishbone.md), for the rework that made a station look slow
- [Status report](../../templates/execution/status-report.md), section 3, where the constraint's queue length is the one flow number worth reporting weekly
- Method background: [knowledge index](../../knowledge/INDEX.md)
