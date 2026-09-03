---
layer: frameworks
stage: ALL STAGES
gate: 1
feeds: ["templates/planning/first-90-days.md", "templates/execution/retrospective.md", "frameworks/execution/retrospective-formats.md"]
method: "knowledge/INDEX.md"
aliases: ["Westrum culture typology", "westrum-culture-typology"]
---
# Westrum culture typology

Based on the ideas of Ron Westrum, from "A Typology of Organisational Cultures", Quality and Safety in Health Care (2004). Explained here in this repository's own words.

## What it is for

Deciding how much to discount what you are told. Westrum's argument is that an organization can be read by watching what happens to information, and specifically to bad information: in a pathological climate it is held back and the carrier pays; in a bureaucratic one it moves through the proper channel, arrives after it is useful, and belongs to nobody; in a generative one it is chased before anyone asks and the carrier is asked to come back. This sheet scores six behaviors against dated events rather than against stated values, because a culture survey asks people to perform the thing it is measuring, and a pathological organization scores itself generative. The argument it settles is the one that follows every slip: the status was green for six weeks, somebody knew, and the room splits between "our process is broken" and "our people did not speak". Those need opposite fixes, and this tells you which one you are holding.

## Run it when

- A date slipped after weeks of green status and nobody can say when the slip became knowable
- Before you facilitate a premortem, retro, or postmortem with a team you have not run one with
- In the first 30 days of a new role, before you commit to anything in writing
- After the reporting line above the team changes: new sponsor, new skip-level, reorg, acquisition

**Skip it when:** you have no authority over how risk information is gathered and no intention of changing how you gather it. The score changes nothing, and a written finding that this place punishes messengers is itself a message travelling through the channel you just scored.

## Inputs you need first

- Three to five occasions in the last two quarters when somebody knew something bad before the organization acted on it, with dates
- The last two [retrospectives](../../templates/execution/retrospective.md) and the latest [incident postmortem](../../templates/operate/incident-postmortem.md), read for what they name and what they carefully do not
- The [status reports](../../templates/execution/status-report.md) covering the weeks before the last slip, to see what colour was shown while it was already known
- Two people who were in those rooms and do not report to you

## The worksheet

### 1. The three types

<!-- Reference table, not a fillable one. Score against the behavior in the cell, never
     against the label at the top: nobody writes "pathological" about their own team, and
     the label is not the finding. The events are. -->

| Behavior | 1, pathological | 2, bureaucratic | 3, generative |
|---|---|---|---|
| How information travels | held back, because carrying it is a personal risk | moves through the proper channel and lands after it matters | chased before anyone asks for it |
| What happens to the messenger | they pay for it once, visibly, and everyone else learns | heard, thanked, and never asked again | asked to come back with more, and taught where to look |
| Where responsibility sits | ducked, and whoever is holding it last loses | each function owns its box; the gaps between boxes are nobody's | shared across the boundary the work crosses |
| Contact across boundaries | discouraged, and going around a manager is an offence | permitted, unfunded, first thing cancelled | rewarded, and written into someone's objectives |
| What a failure produces | a cover story and a quiet reassignment | a fair process, a file, and no change to the system | an inquiry that changes something an outsider can point at |
| What a new idea meets | crushed, because it implies the old one was wrong | treated as a routing problem | welcomed, and given someone's time |

### 2. Evidence log

<!-- Fill this before scoring anything. One row per occasion. The question is always what
     happened, never how it felt: who knew, when, who they told, what was done. Use roles,
     not names, so the sheet survives being left open on a laptop. -->

| # | What was known, and by which role | Date | Who they told | What happened next | Gap from known to acted on |
|---|---|---|---|---|---|
| E1 | [ ] | [YYYY-MM-DD] | [role] | [ ] | [days] |
| E2 | [ ] | [YYYY-MM-DD] | [role] | [ ] | [days] |
| E3 | [ ] | [YYYY-MM-DD] | [role] | [ ] | [days] |

### 3. Scoring sheet

<!-- Score against the most recent event in the log, not the average of five years and not
     what the team would like to be true. Path scored: name it here, from the person who
     first notices to the person who can stop the launch. -->

| Behavior | Score (1 to 3) | Event (ID and date) | Who else saw it |
|---|---|---|---|
| How information travels | [1 / 2 / 3] | [E?] | [role] |
| What happens to the messenger | [1 / 2 / 3] | [E?] | [role] |
| Where responsibility sits | [1 / 2 / 3] | [E?] | [role] |
| Contact across boundaries | [1 / 2 / 3] | [E?] | [role] |
| What a failure produces | [1 / 2 / 3] | [E?] | [role] |
| What a new idea meets | [1 / 2 / 3] | [E?] | [role] |

The scale is three points and no more, for two reasons: it maps onto the three named types, so a score is a claim someone can argue with, and the evidence is a handful of remembered events, which will not carry a finer grain. A five-point scale buys you a 3 that means "not sure", and unsure is the reading that lets a room agree on a number and change nothing.

Two mechanical rules, and they are the method. A 3 with no dated event drops to 2, because generative is the flattering answer and it needs an instance. A 1 with no dated event also drops to 2, because pathology scored from atmosphere is unfalsifiable and it is the mirror error.

Arithmetic: total is the sum of the six, from 6 to 18; floor is the lowest single score. Read the floor first.

| Reading | Entry |
|---|---|
| Path scored | [who notices, to who can stop it] |
| Total | [6 to 18] |
| Floor | [1 to 3], on [behavior] |
| Band from total | [6 to 9 pathological / 10 to 14 bureaucratic / 15 to 18 generative] |
| Band after the intake rule | [ ] |

**Intake rule:** a 1 on how information travels, or on what happens to the messenger, caps the reading at pathological whatever the total says. Those two behaviors are the intake. Information that never arrives cannot be compartmentalized, bridged, or inquired into, so high scores on the other four are describing a pipe with nothing in it.

## Reading the result

A floor of 1 on either intake behavior means do not add a forum. A new meeting in a pathological climate is a new place to be careful in. Change the consequence first: the next person who raises something gets the thanks in the room the sponsor is in, and gets the fix they asked for, and until that has happened twice you gather risk one to one and put it on the register in the facilitator's name.

A total of 6 to 9 means nothing built on self-report is evidence, so stop reading the register and the status colour as though they were. Your instruments are incident timelines, the support queue, and deployment records: artifacts nobody had to volunteer.

A total of 10 to 14 means the information exists, arrives, and dies at a boundary. This is the cheap reading, and the fix is structural rather than emotional: one accountable name on every cross-function row ([RACI](../execution/raci.md)), a standing bridge between the two functions either side of the gap, and triggers instead of review dates on the top rows of the [risk register](../../templates/execution/risk-register.md), because a trigger fires without anybody deciding to speak.

A total of 15 to 18 means run the methods as written and spend the surplus elsewhere. The generative failure mode is its own thing: everything gets raised, the register outgrows the review, and decisions queue behind discussion. That is a [risk matrix](../execution/risk-matrix.md) problem, not a culture problem.

The split profile is the common one and the expensive one: 3 on what a failure produces, 1 on what happens to the messenger. Such a place reviews incidents honestly and punishes the warning that would have prevented them, so every lesson has to be bought with an incident. Movement beats level. A behavior that drops a point after a reorg is the finding whatever the total says, which is why the second run is worth more than the first.

## ILLUSTRATIVE example

Invented reading for Ledgerline's expense-report copilot, scored before the wave-3 rollout by the copilot PM with the support lead and one engineer from another team. Every score below is ILLUSTRATIVE.

Evidence log, abbreviated. E1: the support lead said at the wave-1 review that "the copilot misread my receipt" tickets had no runbook; it became an action with no owner and was raised again at wave 2, a gap of one quarter. E2: an engineer posted in a channel that month-end connector errors would get worse at 4,000 filers, and was asked privately not to put capacity worries where finance can read them; the connector failed at month end six weeks later. E3: the retention question for stored receipts sat between the finance controller and the engineering lead for six weeks, because they share no review. E4: the postmortem after that failure named the missing canary stage and the alert threshold, fixed both inside the quarter, and named no person. E5: support's per-card exclusion idea was welcomed and took two quarters to find a sponsor.

| Behavior | Score (ILLUSTRATIVE) | Event |
|---|---|---|
| How information travels | 2 | E1, it arrived and was routed to nobody |
| What happens to the messenger | 1 | E2, the person holding the specific number was told where not to say it |
| Where responsibility sits | 2 | policy rules had no owner and fell between finance and engineering |
| Contact across boundaries | 2 | E3, no standing review between the two people who needed one |
| What a failure produces | 3 | E4, systems causes, both fixed, no names |
| What a new idea meets | 2 | E5, welcomed and unfunded for two quarters |

Total 12 (ILLUSTRATIVE), which bands bureaucratic. Floor 1 on the messenger, which the intake rule caps at pathological. What changed as a result: the wave-3 [premortem](../execution/premortem-worksheet.md) was not run as written. Causes were collected in writing beforehand and read out by the outsider, the sponsor was absent rather than merely speaking last, and the capacity number went onto the register in the facilitator's name. The green status reports from the weeks before the connector failure stopped being treated as evidence that nothing was known.

## The decision it feeds

Whether to add a channel or change a consequence. That is the fork this instrument exists to settle, and the two options look identical from a status report. A bureaucratic reading buys a structural fix: an owner, a bridge, a trigger, and the information starts arriving in time to matter. A pathological reading means every forum you build is another place for people to be careful in, and the first change has to be to what happens to whoever speaks. The same reading sets your discount rate on the artifacts: how much of the register, the colour, and the retro board you are willing to treat as evidence next quarter.

## Where the output lands

The [first 90 days](../../templates/planning/first-90-days.md) plan. Section 2 takes the reading as one of the three questions, with the date you will have answered it and what it decides; section 7 takes what you will deliberately not do, which under a pathological reading is "start a new risk forum". Carry the total, the floor, and the path scored, because a floor without a path is a slogan.

## Re-run trigger

Re-run when the reporting line above the team changes (new sponsor, new skip-level, new incident-review facilitator), and after any incident where somebody says afterwards that they already knew. A climate is a set of current consequences, so it changes with the person administering them and not with the calendar; a score older than the manager it describes is fiction.

## When this method misleads you

The confident nonsense comes from scoring the wrong thing at the wrong scale.

- **Scoring the company instead of the path.** Flow is local. A generative team sits inside a bureaucratic division under a pathological executive, and all three are true of different paths. Score one path, write it on the sheet, and a sheet with no path named describes a company nobody works in.
- **Scoring from your own inbox.** You are either the person people bring things to or the person they route around, and you cannot tell which from the inside. That is what the two people outside your reporting line are for; without them the sheet measures your position.
- **Turning it into a survey.** Once this becomes a questionnaire with a mean, it measures how people want to be seen, and a pathological organization returns a generative score because answering honestly is the exact behavior in question. The output is confident, precise, and inverted.
- **One vivid event standing in for a pattern.** A shot messenger under a manager who left last year is a fact about that manager. Date every event and discard the ones from before the current reporting line.
- **Handing the label to the sponsor.** "We scored 8, we are pathological" is a diagnosis delivered as an insult, and how it is received is itself a reading of the messenger behavior. Report the events and the one consequence you want changed; the label is for your own planning.

## Feeds

- [First 90 days](../../templates/planning/first-90-days.md), section 2 (as a question with a date) and section 7 (as a thing you will not do)
- [Retrospective](../../templates/execution/retrospective.md), section 1 (why this format) and section 7 (health of the retro, where the messenger behavior is measured weekly), plus the [retrospective formats](../execution/retrospective-formats.md) sheet the reading narrows
- [Premortem worksheet](../execution/premortem-worksheet.md), whose facilitation rules tighten when the floor is 1, and the [program-premortem skill](../../skills/program-premortem/SKILL.md)
- [Incident postmortem](../../templates/operate/incident-postmortem.md), sections 3 and 4, and the [postmortem-facilitator skill](../../skills/postmortem-facilitator/SKILL.md), which cannot run blameless in a climate that is not
- [Risk register](../../templates/execution/risk-register.md) and [status report](../../templates/execution/status-report.md) section 1, where the reading sets what a colour is worth, plus the [escalation skill](../../skills/escalation/SKILL.md), which is the channel a pathological reading tells you not to trust
- Method background: [knowledge index](../../knowledge/INDEX.md); adjacent instruments, the [risk matrix](../execution/risk-matrix.md) and [five whys and fishbone](../execution/five-whys-fishbone.md)
