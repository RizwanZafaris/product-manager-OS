---
layer: templates
stage: DISCOVER
gate: 2
feeds: []
method: "knowledge/high-output-management.md"
aliases: ["Stakeholder Map", "stakeholder-map"]
---
# Stakeholder Map: `<initiative name>`

Stage: DISCOVER through OPERATE, first required at [Gate 2: requirements signed off](../../os/STAGE-GATES.md)
Knowledge: [Grove on managerial output](../../knowledge/high-output-management.md)
Skill: [stakeholder-update](../../skills/stakeholder-update/SKILL.md)

<!-- Built early, revisited at every gate. The stakeholder who sinks a launch is
     rarely the loud one in the kickoff; it is the one nobody mapped, discovered in
     week nine holding a veto. The RACI discipline here is the classic responsibility
     charting method from 1970s management practice, encoded in this repo's own
     words: Responsible does the work, Accountable owns the outcome (exactly one
     name per decision area), Consulted gives input before, Informed hears after. -->

**Initiative:** `<name>` · **Map owner:** `<name>` · **Last reviewed:** `<YYYY-MM-DD>`

## 1. The map

<!-- Influence and interest are scored high / medium / low, honestly, in private
     language you would not mind them reading anyway. Cadence is a commitment: if
     the row says biweekly, a calendar entry exists. -->

| Name | Role or function | Interest (H/M/L) | Influence (H/M/L) | RACI on this initiative | Cadence | Current concerns (their words, not yours) |
|---|---|---|---|---|---|---|
| | | | | | | |

## 2. Decision areas

<!-- RACI is assigned per decision area, not per person-in-general. One Accountable
     name per row; two names in that column means nobody is accountable. -->

| Decision area | Responsible | Accountable (exactly one) | Consulted | Informed |
|---|---|---|---|---|
| scope changes | | | | |
| budget | | | | |
| launch go or no-go | | | | |
| `<add areas>` | | | | |

## 3. Engagement plan for the difficult quadrant

<!-- High influence, low interest is the dangerous quadrant: they can stop you and
     are not paying attention. One row each: what they need to hear, from whom, when. -->

| Name | What would move them from bystander to sponsor | Who engages them | By when |
|---|---|---|---|
| | | | |

## 4. Map health

<!-- The health check that matters is whether anyone has spoken to these
     people recently. A map maintained from memory ages faster than the
     organisation does. -->


- Stakeholders who joined or left since last review: `<names, or "none">`
- Concerns that changed since last review: `<summary>`
- Anyone with veto power not yet met face to face: `<names, or "none">`

## How this map fails

<!-- A stakeholder map drawn from the org chart tells you who exists. The
     useful version tells you who can stop you and what they want, which is
     rarely the same list. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Titles instead of interests | Boxes with roles, and nothing about what each person is protecting | Every row carries an interest: what they want, and what they fear |
| No record of what they can block | Names and influence ratings, and no specific decision attached | Name the decision each person can stop. Influence with no decision attached is gossip |
| Drawn once | An org chart from before the last reorganisation, still cited | Re-read it at the cadence of the risk register, and date the review |
| Influence guessed | The senior title is assumed powerful, and the real blocker is elsewhere | Cite a recent thing the person actually stopped or unblocked |
| No plan for the person against it | The objector is listed and then avoided until launch | One named next step per opponent, before the work starts rather than after |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- The row that matters is the last one. An opponent with a named next step
     is managed; an opponent listed and avoided is a launch-day surprise.
     Delete once real rows exist. -->

| Person and role | What they want | What they fear | What they can block | Evidence of influence | Next step |
|---|---|---|---|---|---|
| *R. Okonkwo, Support Director* | *Ticket volume flat through launch* | *A release that lands in her queue unbriefed* | *Gate 5 sign-off* | *Held the March release for two weeks over a runbook gap* | *Brief her on the fallback path by 2 June, owner S. Kaur* |
| *M. Devi, Finance Controller* | *Accurate expense data, no manual correction* | *Auto-filled fields she cannot audit* | *Production rollout to finance-owned accounts* | *Required a reconciliation report before the last data change* | ***Opposed.** Walk her through the confidence threshold and the manual-review path, before the readiness review, owner R. Ali* |

*The second row is the point. She is against it, that is written down, and there is a dated step against her name. A map that listed her and stopped there would have discovered this at the gate.*

## Exit gate

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


- [ ] Every function that can block launch appears in the map (legal, security, finance, support, and operations checked explicitly)
- [ ] Every decision area has exactly one Accountable name
- [ ] Every high-influence stakeholder has a cadence with a real calendar entry
- [ ] Concerns are recorded in the stakeholder's own words, dated
- [ ] The difficult quadrant has an engagement row per person
- [ ] The map has been reviewed within the current stage, not inherited from the last one
