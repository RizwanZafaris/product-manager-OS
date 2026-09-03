---
layer: knowledge
stage: DEFINE
gate: 2
feeds: ["templates/planning/roadmap.md", "templates/definition/prd.md", "frameworks/execution/estimation-sheet.md"]
method: ""
aliases: ["Shape Up", "shape-up"]
---
# Shape Up

Based on the ideas in Shape Up by Ryan Singer, published by Basecamp (2019).

## The essence

Shape Up inverts the usual question. Instead of "how long will this take?" it asks "how much time is this worth?" That number is the appetite, fixed before work begins: typically a six-week cycle for a big bet or a two-week slice for a small one. Scope then bends to fit the appetite, never the reverse. An estimate grows to protect the team; an appetite shrinks the problem to protect the calendar.

Before anything is bet on, it is shaped. Shaping is senior, private work that produces a pitch: the problem, the appetite, a solution sketched at the right altitude (breadboards and fat-marker drawings, deliberately too coarse to be mistaken for specs), the rabbit holes patched in advance, and the no-gos stated. Shaped work is bounded but not detailed, which leaves the building team real design room while protecting them from unbounded discovery mid-cycle.

Bets replace backlogs. At the betting table, leadership commits a team to a pitch for one cycle, uninterrupted. Nothing else is queued; unpitched ideas simply come back if they matter. The circuit breaker is the enforcement: work not done at cycle's end does not roll over by default. It must be re-pitched and re-bet, which makes runaway projects die of natural causes instead of consuming quarters. A cooldown period between cycles absorbs bug fixing and exploration.

The mechanism is a transfer of authority, not a change of calendar. An estimate is a prediction the team owes the business; an appetite is a budget the business owes the team, and the team spends it by choosing what not to build. Every part of the method exists to make that spending possible. Shaping identifies in advance which parts are load-bearing and which are decoration, because a team cannot cut what nobody has marked as cuttable. The no-gos are pre-authorized refusals. The circuit breaker is the promise that an overrun ends the bet instead of quietly borrowing next cycle's budget, which is what makes the appetite a real constraint rather than a hopeful number.

The pitch is the other half of that transfer, and its coarseness is deliberate rather than lazy. A breadboard shows the connections between places in the product without showing a layout, which leaves the team the decisions they are best placed to make while removing the ones that would have consumed the cycle. A pitch detailed enough to implement has taken back the authority the appetite was supposed to hand over.

Read that way, the six weeks is the least important number in the system. What matters is that scope is variable, the variation is decided by the people doing the work, and the deadline is enforced by cancellation rather than by overtime. A team with those three properties and four-week cycles is running Shape Up. A team with six-week cycles and none of them has renamed its sprints.

## Where it came from

The method is a description of how one company worked, and that company's constraints are the unwritten preconditions of the method. Basecamp built its own product, so nobody outside could set a date; it had no enterprise customers with contractual feature commitments; teams were tiny, typically a designer and one or two programmers; those teams were full-stack enough to finish a slice without waiting on another team; and the founders, who were also the shapers, had both the authority to cancel work and the hours to shape it.

Every well-known failure of adopted Shape Up is one of those preconditions missing. That is why the honest question before adopting it is not whether the cycle length suits you but which of those five conditions you have. The parts of the method are separable, and a company with two of the five can still take the appetite discipline and leave the betting table alone.

## What the method assumes

1. **The team can cut scope without asking.** Variable scope is the load-bearing mechanism, so if every cut needs sign-off from a stakeholder who promised the whole thing to a customer, the appetite becomes a deadline with fixed scope, which is the worst arrangement available.
2. **A bet can be finished by one team.** The cycle has no room for a dependency that queues behind another team's roadmap. Where that dependency exists, either the interface is agreed before the bet is placed or the bet is not shapeable yet.
3. **Senior people have real hours to shape.** Shaping is unscheduled, hard-to-track work that has to happen a cycle ahead of building. An organization that has loaded its senior people to capacity with meetings cannot run this method and will discover that fact only after the first unshaped bet fails.
4. **Cancellation is survivable.** The circuit breaker only works in a culture where a killed bet is a normal outcome. If a cancelled project ends someone's promotion case, the team will ship something rather than nothing, and the something will be the thin, unloved version.
5. **The work is discretionary.** No external date, no regulatory clock, no signed commitment to a specific capability. The skip line below is this assumption stated as a rule.

## When to use it

- When projects chronically overrun, as a diagnosis kit: overruns usually mean unshaped work was bet on, not that the team is slow.
- When writing a roadmap entry or PRD, to attach an appetite to each initiative and let appetite discipline scope before engineering ever estimates.
- When the backlog has become a guilt archive hundreds of items deep, as permission to delete it.

**Skip it when:** the date is external and immovable, as with a regulatory deadline, a scheme mandate, or a contracted go-live. Fixed appetite works by letting scope bend and, if needed, by letting the bet die at the circuit breaker. Neither is available when a supervisor set the date, so run that work as a program with a gate instead.

## A worked case, ILLUSTRATIVE

Coldbrook is an invented scheduling tool for small clinics, and every detail below is made up. The pitch was shared availability across practitioners, appetite six weeks, one designer and two programmers. The shaping had marked two rabbit holes, recurring appointments and time zones, and stated one no-go: no calendar sync with outside systems in this cycle.

Week three looked healthy on a task count, with roughly two thirds of the checklist closed, and was in fact the danger point. Everything closed was work the team already knew how to do: the grid layout, the practitioner list, the filters. The unsolved part was conflict resolution when two practitioners share a room, which nobody had yet found an approach for. This is the distinction that makes the method's progress reporting work: uphill work is figuring out what to do, downhill work is doing it, and a task count treats them identically. Two thirds of the tasks done with the hard problem untouched is not two thirds of the way through the cycle.

Naming it in week three bought three weeks of options. The team spent four days on the room-conflict question, found an approach they trusted, and cut the filters, which had been marked as cuttable during shaping. The cycle ended with shared availability working for the common case, no filters, and no outside sync.

Notice which cut was available. Filters were cuttable because a senior person had said so before the cycle started, in writing, when nobody was under pressure. A cut invented in week five under deadline pressure is a different and much worse decision, made by tired people with no time to check what depends on it.

The counterfactual is the point. Had the same situation been discovered in week five, the available moves would have been to ship the easy two thirds without the part that made the feature useful, or to roll into the next cycle and start a project that eats quarters. Both are the standard outcomes of estimate-driven planning, and both were avoided by an artifact that separates uphill from downhill and a cut that had been pre-authorized weeks earlier by someone senior. If the approach had not been found by day four, the correct move was to let the bet die and re-pitch a narrower problem, which is the circuit breaker being a feature rather than a punishment.

## The trap: cycles without shaping

The most copied part of Shape Up is the six-week cycle, because renaming sprints is free. The load-bearing part is shaping, because it costs senior people real hours every cycle. Adopt the first without the second and you get raw, unbounded problems handed to teams with a deadline three times longer than a sprint and fewer checkpoints, which is strictly worse than the scrum it replaced. The tell is the artifact: if bets are being placed on one-line ideas rather than pitches with rabbit holes and no-gos written down, the circuit breaker becomes a guillotine for teams doing discovery that shapers should have done, and the method gets blamed for the missing half of itself.

The second half of the trap is the missing cooldown. Cooldown is where bug fixes, small requests, and exploration live, and a company that deletes it has not saved two weeks; it has moved that work inside the cycles, where it silently consumes a fifth of every bet. The tell is the retrospective in which every cycle ran late by about the same amount. That is not a shaping problem or an estimating problem. It is unscheduled work being charged to a scheduled budget.

## Other ways it fails, and the tell for each

- **The appetite that is really a deadline.** Scope is fixed by a commitment made elsewhere and only the time is called an appetite. The tell: nothing was cut during the cycle, and the team worked late in the final week. A cycle where nothing was cut is either a lucky bet or a fixed-scope project in costume.
- **Shaping by committee.** The pitch is written by five people in a workshop, so it contains everyone's requirement and no no-gos. The tell: a pitch with no stated non-goals, which means nothing was decided, only collected.
- **The circuit breaker that never fires.** Every unfinished bet is re-bet immediately, so rollover has been reinstated with extra ceremony. The tell: no bet has been abandoned in the last year. A method whose enforcement mechanism has never been used is running on the honor system.
- **Bets that block on another team.** Two weeks in, the work is waiting on a platform change nobody owns. The tell: a cycle report whose reason for delay names another team. Shape the interface first, or do not place the bet.
- **The betting table as backlog grooming.** The meeting reviews every idea rather than choosing among a few pitches, and takes a day. The tell: the table's agenda is a list rather than a small set of written pitches with appetites attached.
- **Hill charts filled in by wishful thinking.** Scopes are reported as over the hill because the team hopes they are. The tell: several scopes that have sat at the same position for two weeks, which is the shape of a problem nobody has admitted is still uphill.
- **Shaping too finely.** The pitch arrives as a specification with screens, so the team has no design room and every discovery becomes a deviation from the plan. The tell: pitch fidelity high enough that a developer could implement it without a designer, which is a spec, not a shape.
- **Interrupted cycles.** An escalation lands in week two and the bet absorbs it, so the appetite was spent on something nobody bet on. The tell: the cycle report contains work that appears in no pitch. Uninterrupted time is a term of the bet, and a company that cannot honor it should not be betting.
- **The rabbit hole nobody patched.** Shaping skipped the technical unknown because the shaper could not judge it, and the cycle discovers it in week four. The tell: a pitch whose rabbit-hole section names only product questions, with no engineering ones.
- **Appetite inflation.** Every problem turns out to be worth six weeks. The tell: no two-week bets in the last two cycles, which usually means nobody is willing to propose the small version of anything.

## How it lies

Shape Up reports on execution and is silent about worth. A well-shaped bet on the wrong problem finishes on time, inside appetite, with a clean hill chart, and moves nothing; the method has no place to record that outcome, because the bet was judged at the betting table on the strength of the pitch and never revisited afterwards. Teams that adopt it wholesale often stop measuring outcomes at all, having replaced a roadmap that at least named a goal with a stream of well-run projects. Pair it with something that judges results, which in this repository means the appetite lives on the roadmap entry beside the key result it serves.

The second distortion is a claim the method does not make but readers hear anyway: that six weeks is a discovered natural length. It is a choice that fits a company where nobody outside could set a date. Presenting it as universal is how the method arrives at organizations that have none of Basecamp's preconditions, where the cycle length is the only part that gets copied because it is the only part that does not require giving a team the authority to cut.

The practical guard is to ask, of any adoption proposal, which of the five preconditions the company actually has. Two or three is common and is not a reason to give up; it is a reason to take the appetite discipline and leave the betting table for later.

Finally, the pitch format flatters a certain kind of writer. A well-drawn breadboard and a confident set of rabbit holes read as shaped work even when the shaper never checked feasibility with an engineer. The unshaped pitch that looks shaped is the most expensive artifact the method can produce, and its tell is the absence of any recorded conversation with the people who will build it.

The question that settles most adoption debates is not about cycle length: ask who is allowed to cut scope on the last Friday, without asking anyone. If the answer is nobody, the rest of the method cannot function.

## What good looks like

| Done well | The version that looks the same and is not |
|---|---|
| Something was cut mid-cycle, from a list marked cuttable during shaping | Nothing was cut, and the last week was long |
| Every pitch states its no-gos | Every pitch states its requirements |
| A bet has been abandoned at the circuit breaker in living memory | Unfinished bets are re-bet automatically, described as continuity |
| Cooldown exists and absorbs the unscheduled work | Cooldown was removed to gain capacity, and every cycle runs late by a fifth |
| Progress reported as uphill or downhill per scope | Progress reported as a percentage of tasks closed |
| Shaping happens a cycle ahead, by people with the authority to say no | Shaping happens in the first week of the cycle, by the team building it |
| The appetite sits beside the outcome the bet is meant to move | The appetite is the only number attached to the work |

## Where it sits in the loop

- Stage: DEFINE and BUILD. The pitch is a definition artifact; the cycle is a build discipline. Discovery belongs before the pitch, not inside the bet.
- Upstream: shaping consumes discovery evidence, usually a [problem framing](../templates/discovery/problem-framing.md) or [opportunity assessment](../templates/discovery/opportunity-assessment.md), so the bet is placed on a problem someone has heard a customer describe.
- Downstream: the [roadmap](../templates/planning/roadmap.md) carries the appetite per entry, the [PRD](../templates/definition/prd.md) records what the no-gos excluded, and the [retrospective](../templates/execution/retrospective.md) asks what was cut and when it was noticed.
- Compared at [Gate 2: requirements signed off](../os/STAGE-GATES.md), where an appetite and an estimate that disagree by a wide margin is the signal to reshape rather than to negotiate.
- Related: the [estimation sheet](../frameworks/execution/estimation-sheet.md) exists for the opposite situation, where scope is fixed and the date is the unknown.

## What it is not for

- **Committed dates.** Repeated because it is the most expensive mistake: with no scope authority and no cancellation option, the appetite is a countdown and the method's protections are all absent.
- **Multi-team platform programs.** Work that spans four teams with sequencing between them needs a dependency register and a program charter. A betting table cannot commit other people's teams.
- **Discovery.** A bet is placed on a shaped solution to a known problem. Unbounded learning inside a fixed appetite ends the cycle with insight and no product, which is a fine outcome badly labeled.
- **Continuous operational load.** Support rotations, incident response, and compliance chores do not fit a bet and belong in cooldown or in a capacity plan.
- **Very large single deliverables.** A migration with a cutover cannot be cut down to fit six weeks and cannot be abandoned halfway. Run it as a program with gates.

## Variants worth knowing

- **Appetite without cycles**, the most useful partial adoption: keep whatever cadence you have, and require every roadmap entry to carry a time budget the team is allowed to spend by cutting scope. This is the part that changes behavior, and it costs no reorganization.
- **Small batches**, two-week bets run several to a cycle. Lower ceremony, and better suited to teams whose work arrives in smaller pieces than a six-week problem.
- **Hill charts as reporting only**, adopted by teams that keep their existing process. Separating uphill from downhill is worth having on its own, because it is the only common progress display that distinguishes not-yet-understood from not-yet-typed.
- **Shaping as a standing role**, where one or two senior people shape continuously a cycle ahead. Closer to how the original company actually worked than the tidy sequence the book presents.
- **Betting with a strategy filter**, an addition rather than a variant: the table only considers pitches naming the outcome they serve. It reintroduces the judgment of worth that the method leaves out, at the cost of a slower table.

## Used by

- [Roadmap](../templates/planning/roadmap.md)
- [PRD](../templates/definition/prd.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [Estimation sheet](../frameworks/execution/estimation-sheet.md), the appetite against estimate comparison, with ranges
- [MoSCoW](../frameworks/prioritization/moscow.md), the scope-cutting language for the case where the date is fixed and the appetite is not yours
- [Retrospective formats](../frameworks/execution/retrospective-formats.md), for the cycle review that asks what was cut and when it was seen
- [Empowered product teams](cagan-product-teams.md), the card on the autonomy this method presupposes
