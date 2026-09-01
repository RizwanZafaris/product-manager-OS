# Shape Up

Based on the ideas in Shape Up by Ryan Singer, published by Basecamp (2019).

## The essence

Shape Up inverts the usual question. Instead of "how long will this take?" it asks "how much time is this worth?" That number is the appetite, fixed before work begins: typically a six-week cycle for a big bet or a two-week slice for a small one. Scope then bends to fit the appetite, never the reverse. An estimate grows to protect the team; an appetite shrinks the problem to protect the calendar.

Before anything is bet on, it is shaped. Shaping is senior, private work that produces a pitch: the problem, the appetite, a solution sketched at the right altitude (breadboards and fat-marker drawings, deliberately too coarse to be mistaken for specs), the rabbit holes patched in advance, and the no-gos stated. Shaped work is bounded but not detailed, which leaves the building team real design room while protecting them from unbounded discovery mid-cycle.

Bets replace backlogs. At the betting table, leadership commits a team to a pitch for one cycle, uninterrupted. Nothing else is queued; unpitched ideas simply come back if they matter. The circuit breaker is the enforcement: work not done at cycle's end does not roll over by default. It must be re-pitched and re-bet, which makes runaway projects die of natural causes instead of consuming quarters. A cooldown period between cycles absorbs bug fixing and exploration.

## When to use it

- When projects chronically overrun, as a diagnosis kit: overruns usually mean unshaped work was bet on, not that the team is slow.
- When writing a roadmap entry or PRD, to attach an appetite to each initiative and let appetite discipline scope before engineering ever estimates.
- When the backlog has become a guilt archive hundreds of items deep, as permission to delete it.

**Skip it when:** the date is external and immovable, as with a regulatory deadline, a scheme mandate, or a contracted go-live. Fixed appetite works by letting scope bend and, if needed, by letting the bet die at the circuit breaker. Neither is available when a supervisor set the date, so run that work as a program with a gate instead.

## The trap: cycles without shaping

The most copied part of Shape Up is the six-week cycle, because renaming sprints is free. The load-bearing part is shaping, because it costs senior people real hours every cycle. Adopt the first without the second and you get raw, unbounded problems handed to teams with a deadline three times longer than a sprint and fewer checkpoints, which is strictly worse than the scrum it replaced. The tell is the artifact: if bets are being placed on one-line ideas rather than pitches with rabbit holes and no-gos written down, the circuit breaker becomes a guillotine for teams doing discovery that shapers should have done, and the method gets blamed for the missing half of itself.

## Used by

- [Roadmap](../templates/planning/roadmap.md)
- [PRD](../templates/definition/prd.md)
