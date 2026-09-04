---
layer: templates
stage: BUILD
gate: 4
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Backlog", "backlog", "product backlog", "intake"]
---
# Backlog: [product or squad name]

Stage: BUILD, feeds Gate 4 (acceptance criteria met), worked continuously from DISCOVER onward
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [roadmap-builder](../../skills/roadmap-builder/SKILL.md)

<!-- What this file is, and what it deliberately is not.

     It is not where stories are written. That is
     [user-stories.md](../definition/user-stories.md), which defines every US
     id. This file governs the queue those stories come out of: what is
     allowed in, how it is ranked, how often it is looked at, and when an item
     is killed rather than carried.

     It is also not your tracker. If your team works in a tracker, that is
     where the items live and this file holds the policy the tracker is run
     by, plus the health numbers nobody computes automatically. Copying every
     item here guarantees the two disagree within a month, and the tracker
     will win silently because that is where people actually work.

     The governing fact about backlogs: they are the only product artifact
     that gets worse by itself. Every other document decays when nobody
     updates it. A backlog decays when people do update it, because intake is
     easier than triage and the gap compounds. Everything below is a
     mechanism against that one asymmetry. -->

**Owner:** [name] · **Refinement cadence:** [day and meeting] · **Last triaged:** [YYYY-MM-DD]
**Tracker of record:** [link, or "this file"] · **Size cap:** [n] active items

## 1. Intake: what is allowed in

<!-- The single highest-leverage section here. A backlog with no intake
     standard is a list of everyone's wishes, and triage then means a product
     manager privately deciding whose wish loses, every week, forever.

     The right-hand column matters more than the others: an incomplete request
     has somewhere else to go, so refusing it is not a rejection of the
     person. Without that column the only options are accept it or fight, and
     the backlog always wins that argument. -->

| Intake source | Who raises it | What it must carry before it enters | Where it goes if incomplete |
|---|---|---|---|
| Customer support | Support lead | Ticket volume, severity, sample tickets, affected segment | Back to support with the missing field named |
| Sales | Account executive or sales operations | Account, contract value, close date, what the deal is blocked on | Stays in the CRM. A deal blocker is not a backlog item until it is a product problem |
| Engineering and tech debt | Engineering lead | Systems affected, user-visible impact, rough effort | Stays in the engineering wiki until user impact is stated |
| Leadership request | The executive or a named delegate | The strategic goal it serves, a success metric, a deadline if real | Leadership queue, visibly unranked, rather than silently at the top |
| Product discovery | Product manager or designer | Hypothesis, target user, expected outcome, evidence so far | Ideas bin, not the ranked backlog |

## 2. The register

<!-- One row per active item. "Active" means it is genuinely a candidate for
     the next two or three planning cycles; everything else belongs in the
     ideas bin or dead, and pretending otherwise is what produces a backlog
     nobody can read.

     Requester and date raised are mandatory and are the two fields most often
     skipped. Without a requester there is nobody to ask when the context has
     evaporated, and the item becomes unkillable because nobody can confirm it
     is dead. Without a date the ageing checks in section 4 cannot run. -->

| ID | Item (the problem, not the solution) | Source | Requester | Raised | Rank | Size | State | Linked story or PRD |
|---|---|---|---|---|---|---|---|---|
| B1 | | | | [YYYY-MM-DD] | | | candidate | |

**States, fixed vocabulary:** `candidate` (in the queue), `refined` (understood and sized), `committed` (in a release slice), `blocked` (named blocker), `parked` (deliberately deferred with a revisit date), `dead` (see section 5).

## 3. Ranking

<!-- Do not invent a scoring scheme here. This repository already carries the
     sheets, each with its arithmetic written out, and the point of naming one
     is that everyone can reproduce the order rather than argue about it.

     Record which method this backlog uses and stay on it. Switching method to
     get a preferred answer is the most common and least visible way a ranking
     stops meaning anything, so a change of method is a decision-log entry. -->

**Method in use:** [one of the below] · **Last re-ranked:** [YYYY-MM-DD] · **Changed method? Log it in [decision-log.md](decision-log.md)**

| Method | Use it when | Sheet |
|---|---|---|
| RICE | Comparable items, and you want the arithmetic visible | [rice-scoring-sheet](../../frameworks/prioritization/rice-scoring-sheet.md) |
| MoSCoW | One release scope, negotiating what ships | [moscow](../../frameworks/prioritization/moscow.md) |
| WSJF and cost of delay | Sequencing where waiting has a measurable price | [wsjf-cost-of-delay](../../frameworks/prioritization/wsjf-cost-of-delay.md) |
| Weighted decision matrix | Several criteria that are not all commensurable | [weighted-decision-matrix](../../frameworks/prioritization/weighted-decision-matrix.md) |
| Now, next, later | Communicating outward, where dates would be read as promises | [now-next-later](../../frameworks/prioritization/now-next-later.md) |

## 4. Health check

<!-- Run at the refinement cadence and write the numbers down. Each row is a
     way a backlog rots, and each has a rule rather than a judgment, because
     the alternative is a product manager relitigating the same argument every
     week with the person who raised the item.

     The thresholds in brackets are yours to set once and then hold. A
     threshold that moves whenever it is breached is not a threshold. -->

| Failure mode | What it looks like | The rule | This period |
|---|---|---|---|
| Infinite growth | The register passes the size cap and triage quietly stops | Cap at [n] active items. Overflow goes to the ideas bin, not to the bottom of the list | |
| Zombie items | Carried for quarters, no owner, never scheduled | An item with no requester for [90] days is archived, and the last owner is told | |
| Duplicates | The same problem filed under three titles | Search before entry, and link rather than re-file. Merge on sight and keep the older id | |
| No requester | An anonymous row nobody can explain | Requester and use case are mandatory at intake, per section 1 | |
| Priority inflation | Everything arrives marked highest | Each source gets at most one top-priority item per cycle. The rest are stack-ranked against each other | |
| Stale context | The item cites a plan, a quarter or a metric that no longer exists | Anything with no update in [180] days is re-validated against the current strategy or killed | |

**Numbers to record each period:** active items [n] · added [n] · killed [n] · median age [days] · oldest item [days]

<!-- Added against killed is the number that matters, and almost nobody
     computes it. If added exceeds killed for several periods running, the
     backlog is growing regardless of how much the team ships, and no amount
     of velocity will close it. -->

## 5. Kill policy

<!-- Written down in advance, because killing an item in the moment always
     looks like a judgment on the person who raised it. A policy agreed when
     nothing is at stake is what makes it procedural instead.

     Killing is not deletion of the record. The id is spent and the row moves
     to the dead table, so the same idea arriving again is recognised as a
     returning idea rather than a new one. -->

- Untouched for [6] months with no deferral date: archive, and tell the last known owner.
- The requester has left and nobody claimed it within [30] days: kill, and log the removal.
- Duplicated by, or superseded by, something already shipped: close it, link the successor, remove within a week.
- It belongs to another team or product: redirect it to that owner and do not keep a local copy.
- It has been carried through [3] planning cycles without being ranked into one: it is not a candidate, whatever anyone says in the meeting.

| ID | Item | Killed on | Why | Who was told |
|---|---|---|---|---|
| | | | | |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- Kept to show the intake standard doing real work. Delete it once the
     register has real rows. -->

| ID | Item | Source | Requester | Raised | Rank | State | Note |
|---|---|---|---|---|---|---|---|
| B7 | *Field reps refile expenses because a scanned total is wrong and there is no way to correct it before submission* | Support | *Support lead* | *2026-02-11* | *RICE 42* | *refined* | *Became US3 in [user-stories.md](../definition/user-stories.md)* |
| B8 | *Add a bulk export button to the admin console* | Sales | *unnamed* | *2025-08-02* | *unranked* | *dead* | *Killed: requester left, unclaimed for 30 days, no use case recorded* |

The second row is the common case. It was raised for one deal, the person who
wanted it moved on, and nobody could say what it was for. It survived a year
because deleting it felt rude, which is the whole reason section 5 is agreed
in advance rather than decided in the moment.

## Exit gate (feeds Gate 4: acceptance criteria met)

<!-- Checkable by someone who did not run the backlog, which is the test of
     whether a gate is a gate. Every box below is a fact about the file rather
     than an opinion about the queue. -->

- [ ] Every active item names a problem, not a solution, and carries a requester and a date raised
- [ ] Intake sources each have a stated destination for incomplete requests
- [ ] One ranking method is named, and any change of method has a decision-log entry
- [ ] The health check has been run this period and the six numbers are recorded
- [ ] Added against killed has been computed, not estimated
- [ ] The register is inside its size cap, or the overflow is in the ideas bin
- [ ] No item has been carried through more than the stated number of planning cycles unranked
- [ ] Killed items are in the dead table with their ids spent and the reason written
- [ ] Committed items link to a story id in [user-stories.md](../definition/user-stories.md)
- [ ] The worked example above has been removed
