---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Service Blueprint", "service-blueprint"]
---
# Service Blueprint: [scenario short name]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [persona-builder](../../skills/persona-builder/SKILL.md)

<!-- The blueprint form originates with G. Lynn Shostack's 1980s work on
     designing services; the scoping discipline here follows Nielsen Norman
     Group's published guidance, restated in this repo's own words: one
     scenario, eight to twelve user actions. A blueprint that tries to cover
     the whole service becomes wallpaper.

     Division of labor with the [journey map](journey-map.md): the journey map
     shows the user's experience; the blueprint shows what the organization
     does to produce it. When the journey map's backstage note says "the fix
     lives backstage", this is the file that goes and finds it. Most service
     failures happen at the line of visibility, where frontstage promises meet
     backstage reality; section 3 exists to name an owner at each such point. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD]
**Evidence base:** [session IDs, support tickets, ops interviews this blueprint is drawn from]

## 1. Scenario, trigger, and scope

**Scenario:** [one sentence: which persona doing which job, link the persona block in [personas.md](personas.md)]
**Trigger:** [the event that starts the scenario]
**Scope statement:** [this blueprint covers from [first user action] through [last user action] and nothing else]

## 2. The blueprint

<!-- One row per user action, eight to twelve rows. Frontstage is what the user
     sees; backstage is the people and actions out of sight; support systems
     include vendors, and every vendor is named, because the user experiences
     their outage as yours. Write what happens today, from evidence, not the
     process diagram on the wiki. -->

| # | User action | Frontstage (what the user sees) | Backstage (people and actions out of sight) | Support systems and vendors |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

## 3. Failure points at the line of visibility

<!-- Where the handoff between frontstage and backstage drops, delays, or lies:
     the confirmation shown before the work is done, the queue nobody watches,
     the vendor callback that fails silently. Every row gets the person who
     owns the fix conversation, not a team name. -->

| # | Blueprint step | What fails or drops | Owner of the fix conversation | Evidence |
|---|---|---|---|---|
| F1 | | | [name, not a team] | [ticket ID, session ID, metric] |

## 4. Time and waits

<!-- Annotate the steps where time hurts. Elapsed is wall clock end to end;
     waiting is the slice the user spends doing nothing. The longest wait and
     the worst failure point are usually neighbors. -->

| Blueprint step | Elapsed time | Of which waiting | What the user is waiting on | Evidence |
|---|---|---|---|---|
| | | | | |

## 5. Fix candidates

<!-- Route, do not solve here. A candidate worth funding becomes a
     [problem framing](problem-framing.md); a small operational fix goes to the
     owning team's backlog; the rest is recorded and left alone. -->

| Candidate | Blueprint step(s) | Who feels it and how often | Route |
|---|---|---|---|
| | | | [problem-framing.md](problem-framing.md) / owning team backlog / not now |

---

### Worked micro-example (illustrative, invented)

> **Scenario:** Roadside Riya disputes a duplicate charge from the app.
> Nine user actions from "spots the duplicate" to "sees the refund". Frontstage shows "dispute filed" at step 3; backstage, the case enters a queue reviewed once daily, and the card processor vendor confirms only by end of next day.
> F1: the step-3 confirmation implies action that has not started (line-of-visibility lie), owner: dispute ops lead by name. Longest wait: 26 hours at step 4, waiting on the daily queue.
> Fix candidate: move the queue review to twice daily; routed to problem-framing.md.

---

## Exit gate (feeds Gate 1: problem worth solving)

- [ ] One scenario, one persona, and an explicit scope statement, held to eight to twelve user actions
- [ ] Every row drawn from cited evidence, not the official process diagram
- [ ] Every vendor in the support row is named
- [ ] Every failure point has a named owner for the fix conversation
- [ ] Time and wait annotations exist for the painful steps, with evidence
- [ ] Every fix candidate is routed: problem framing, owning team, or not now
