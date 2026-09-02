---
name: escalation
description: Turn a stuck decision or a blocked dependency into a one-page brief (Situation, Impact, Urgency, Options, Recommendation, Ask) and route it up a named ladder with SLAs. Use when a decision has missed its needed-by date, when two teams deadlock, when a risk owner will not act, or when a governance forum keeps noting things without deciding anything.
---

# Escalation: making the ask someone can grant

Escalation is a service to the decider, not an act of aggression. The [program premortem](../program-premortem/SKILL.md) names the disease as failure mode 3, governance without decision rights: forums that receive updates but cannot kill, fund, or resequence anything. Naming the disease is not a procedure. This skill is the procedure: a brief a decider can act on in five minutes, routed to someone who actually holds the decision, with the outcome recorded where the next person can find it.

## Files this skill drives

- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where the outcome lands, granted or declined
- [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md), which absorbs a declined or deferred ask as an owned, accepted risk
- Reads: [../../templates/execution/stakeholder-map.md](../../templates/execution/stakeholder-map.md) for who holds which decision, and [../../templates/execution/dependency-register.md](../../templates/execution/dependency-register.md) for the escalation contacts it names

## When to use

- A decision has a needed-by date and the date passed, or will pass before the current forum meets again
- Two teams deadlock and the dispute path in [triad decision rights](../../knowledge/roles/triad-decision-rights.md) ran out of road
- A risk or dependency owner acknowledges the item and does not act
- Your steering forum has "noted" the same item twice

## The brief

One page, six labeled parts, in this order:

1. **Situation.** Two sentences, facts only, no adjectives. What was agreed, what is happening instead.
2. **Impact.** Quantified: what it costs, whom, per what period, with the calculation shown. "This blocks the team" is not an impact; "each week of delay moves the launch a week and burns the committed vendor window" is.
3. **Urgency.** The date after which options expire, and what expires. Urgency is a property of the calendar, not of your stress level.
4. **Options.** Two or three, each with cost and consequence, including "do nothing", priced. A single option is a demand wearing a brief's clothing.
5. **Recommendation.** One option, committed. Hedging across options transfers the analysis you were supposed to do.
6. **Ask.** The specific decision requested, from a named person, by a date. Not "alignment", not "visibility", not "support": a decision.

## The routing ladder

Same brief at every rung, plus the recorded outcome of the rung before. Skipping rungs spends trust; if you must, write down why.

| Rung | Route to | SLA to answer or pass |
|---|---|---|
| 1 | The counterpart owner, directly | 2 business days |
| 2 | Both managers, jointly, one thread | 3 business days |
| 3 | The sponsor or forum holding the decision, per the stakeholder map | Its next session, or 5 business days |

Two standing rules. The counterpart sees the brief before it goes up a rung: no ambushes, and half the time the brief itself unlocks rung 1. And escalate the decision, never the person: the brief describes a stuck question, not a colleague's failings.

## Workflow

1. Confirm the decision exists: what exactly is being decided, who holds it (stakeholder map), and the needed-by date. If no one holds it, that gap is the real finding; log it in the decision log and escalate the ownership question first.
2. Write the six-part brief. Show it to the counterpart.
3. Route up the ladder, one rung at a time, on the SLAs above.
4. Record the outcome in the decision log: granted, declined, or deferred, with the decider named. A declined or deferred ask becomes a risk-register row with the decider recorded as accepting the risk, a likelihood, an impact, and a review date.

## Exit gate

The escalation is not done when the meeting happens; it is done when the ask has a written answer in the decision log, or the risk register carries the accepted risk with the decider's name and a review date. An escalation that ends in "we discussed it" changed nothing and will run again next month, longer.
