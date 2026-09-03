---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/definition/prd.md", "templates/discovery/opportunity-solution-tree.md", "templates/definition/assumptions-register.md"]
method: "knowledge/torres-continuous-discovery.md"
aliases: ["Impact mapping", "impact-mapping"]
---
# Impact mapping

Based on the ideas of Gojko Adzic, from Impact Mapping (2012). Explained here in this repository's own words.

## What it is for

A tree with four levels: the goal (why), the actors who can help or hinder it (who), the behavior changes in those actors that would move the goal (how), and the deliverables that might cause those changes (what). The rule that makes it a tool rather than a diagram: every deliverable must trace up through an impact and an actor to the goal, and every link is a hypothesis. It answers "why are we building this, and what would we stop building if it did not work." It is the cheapest scope-cutting instrument in this repository, because a deliverable with no path to the goal has no place on the map, however loved.

## Run it when

- An objective exists and the team needs to turn it into scope without inheriting last quarter's backlog.
- A backlog has grown by accretion and nobody can say what behavior each item is supposed to change.
- Before a PRD, to fill its objectives and out-of-scope sections with reasons rather than lists.

**Skip it when:** the goal cannot be stated as a measurable change. A map drawn under "improve the expense experience" produces impacts nobody can observe and deliverables nobody can cut; go back to the [OKR sheet](../../templates/planning/okrs.md) and get a number first. Mandated work with no behavior behind it belongs in the RICE sheet's mandate lane, not here.

## Inputs you need first

- The goal with a metric, a baseline, and a target, from the OKR sheet or the [north star metric](../../templates/planning/north-star-metric.md).
- The actors, including the ones who can hinder, from the [personas](../../templates/discovery/personas.md) and the [stakeholder map](../../templates/execution/stakeholder-map.md).
- Evidence of current behavior, from the [discovery synthesis](../../templates/discovery/discovery-synthesis.md).
- The candidate deliverables, from the backlog.

## The worksheet

### Level 1: the goal

| Goal (one sentence, an outcome, not a deliverable) | Metric | Baseline | Target | By when | Owner |
|---|---|---|---|---|---|
| [goal] | [metric] | [n, source] | [n] | [date] | [role] |

### Level 2: actors

| Actor | Type | What they do today | Evidence |
|---|---|---|---|
| [actor] | [primary user / secondary user / internal / hindering] | [behavior] | [source] |

### Level 3: impacts

An impact is a change in an actor's behavior, written with a verb: starts, stops, does more, does less, does faster. A feature is not an impact.

| Actor | Impact (behavior change) | How you would observe it | Why it moves the goal |
|---|---|---|---|
| [actor] | [starts / stops / does X] | [signal, where measured] | [one sentence] |

### Level 4: deliverables

| Deliverable | Impact it serves | Assumption connecting them | Cheapest test of the assumption | Size | Keep, test, or cut |
|---|---|---|---|---|---|
| [item] | [impact ref, or none] | [if we ship this, the actor will...] | [test] | [S / M / L] | [decision] |

Decision rules: no deliverable without an impact; no impact without an actor; no actor without a path to the goal. A deliverable with "none" in its impact column is cut or parked, with the reason written down. Read each path aloud as one line: goal, actor, impact, deliverable. If the sentence is absurd, so is the row.

## Reading the result

Count deliverables per impact. The impact with the most deliverables is where the team's bets are concentrated; ask whether that actor is the one who can move the goal most, or just the one the team knows best. Pick the shortest path to the goal and test it first; the whole map is a set of hypotheses, and the link most likely to be wrong is the one between deliverable and impact. When a deliverable ships and the impact does not appear, the deliverable succeeded and the assumption failed: stop, record it in the [assumptions register](../../templates/definition/assumptions-register.md), and do not build the next deliverable on the same path.

## ILLUSTRATIVE example

Ledgerline's expense-report copilot, all numbers invented. Goal: reviewer hours spent on mechanical checks fall from about 30 a month (finance's time logs) to 15 by the end of the second quarter after launch.

| Actor | Impact | Observed by | Deliverable | Keep, test, or cut |
|---|---|---|---|---|
| Filers (primary) | Submit reports whose fields match the receipt | Field corrections at review, per report | Receipt auto-extraction | Keep; test on the pilot set first |
| Filers | Pick the policy category right first time | Category bounces per hundred reports | Category suggestion with the matched policy line | Test; the assumption that filers accept a suggested category is unmeasured |
| Finance reviewers (secondary) | Stop opening receipts to check totals | Time per review, from reviewer logs | "Drafted by copilot, fields verified" badge | Keep |
| Finance policy owner (hindering) | Publishes categories in a form the system can read | Policy export exists and is current | Policy export format agreed with finance | Keep; without it the suggestion decays at every refresh |
| Filers | none | | Dark mode for the expense form | Cut: no impact on the map |

Paths read aloud: "To halve mechanical review hours, finance reviewers stop opening receipts to check totals, because the badge tells them the fields were verified." The dark-mode row does not produce a sentence, and leaves.

## The trap

The map drawn backward. The team already knows what it wants to build, so it writes the deliverables first and invents an impact to sit above each one. The tell is symmetry: every deliverable has exactly one impact, no impact has zero deliverables, and no actor is a hindering one. A real map is lopsided, has impacts with nothing under them yet, and includes at least one actor who can wreck the goal. When the sheet looks tidy, the question to ask is who drew the deliverables first.

## Feeds

- [PRD](../../templates/definition/prd.md): section 2 objectives from the goal and impacts, section 7 out of scope from the cut rows
- [Opportunity solution tree](../../templates/discovery/opportunity-solution-tree.md): impacts and opportunities describe the same layer; use one or the other, not both
- [Assumptions register](../../templates/definition/assumptions-register.md): every deliverable-to-impact link
- [Decision log](../../templates/execution/decision-log.md): every cut, with the reason
- [Gate 1: problem worth solving](../../os/STAGE-GATES.md) for the goal and actors; Gate 2 for the deliverables that survived
- Method background: the attribution above; the neighbouring method is [continuous discovery](../../knowledge/torres-continuous-discovery.md)
