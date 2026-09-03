---
name: stakeholder-update
description: Write the executive or board update as a situation, complication, resolution narrative that puts the decisions needed on the first page, with every number traced to the metrics review. Use when a QBR or board update is due, when a monthly executive review needs a pre-read, when a one-page update must get a decision this week, or when a sponsor asks "where are we" and the honest answer is longer than a sentence. Takes the filled metrics review, the OKR sheet, the decisions needed with their options, the risk register, and the audience; returns the headline, the decisions table, the metrics and risks sections, the next-period slice, and the objection sheet for the presenter.
---

# Stakeholder Update: the narrative that gets a decision, not a nod

Updates fail as activity lists. The ask is on page four, the misses are missing, the numbers were computed fresh for the deck, and the room says "noted". This skill writes the update on Minto's spine, situation, complication, resolution, so the reader knows where things stand, what changed, and what you need, before they stop reading.

## Files this skill drives

- [../../templates/operate/qbr-board-update.md](../../templates/operate/qbr-board-update.md), the quarterly instrument
- [../../templates/planning/exec-update.md](../../templates/planning/exec-update.md), the one-page version for a decision between quarters
- [../../templates/execution/status-report.md](../../templates/execution/status-report.md), the weekly instrument beneath both
- Read first: [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md), the only source of numbers; [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md); [../../templates/planning/roadmap.md](../../templates/planning/roadmap.md) for the next-period slice; [../../templates/execution/stakeholder-map.md](../../templates/execution/stakeholder-map.md) for who can decide what
- [../../templates/execution/decision-log.md](../../templates/execution/decision-log.md), where every decision the room makes is logged within a day
- Worksheet: [../../frameworks/execution/stakeholder-power-interest.md](../../frameworks/execution/stakeholder-power-interest.md) (Mendelow, 1991), for the objection sheet
- Method background: the SCR entry in [../../knowledge/INDEX.md](../../knowledge/INDEX.md) (Minto, The Pyramid Principle, 1978), [../../knowledge/high-output-management.md](../../knowledge/high-output-management.md) on meetings as a manager's output
- When the ask is a stuck decision rather than a report, [../../skills/escalation/SKILL.md](../../skills/escalation/SKILL.md) owns it

## When to use

- A quarterly business review or board update is due
- A monthly executive review needs a pre-read that fits the meeting
- Something changed, and one page must get a decision this week
- The weekly async narrative, the light form of the same discipline
- A sponsor asks "where are we", and the honest answer takes more than a sentence

## Inputs

The filled metrics review, with its confidence notes. The OKR sheet. The decisions needed, each with its options. The risk register, with movement since the last update. The roadmap's Now and Next with their confidence levels. The audience, what it can decide, and its time and pre-read norms, from the stakeholder map. What the audience already believes about the product.

Ask one question first: what decision do you need from this room. If the answer is none, the update is an FYI; it goes out in writing and does not take a meeting.

## Workflow

### 1. Fix the audience and the decision

One update per audience. The board version and the team version differ in what each can act on, never in candor. Decision rule: no decision needed, no meeting; write the weekly async narrative instead, three parts, what changed, next week's commitments, detail below the fold.

### 2. Pull the numbers, do not make them

Every number comes from the metrics review, confidence note attached. Nothing is computed fresh for this document, because a number that exists only in the deck is a number nobody can check. Missed metrics get the same prominence as hit ones; a board that only sees green rows prices the reporting at zero.

### 3. Write the spine

Situation: where the product stands against the goal, in numbers the reader already accepts. Complication: the one thing that makes today different from the last update, a miss, a risk that moved, a market move, a dependency slip. Resolution: what you propose, and what you need from this room. The headline is three sentences, one per part. Decision rule: if the complication is genuinely "nothing changed", say so in one line and cancel the meeting; an update that manufactures drama trains the room to discount the real one.

### 4. Build the body in reading order

The decisions table goes second, because pages after it may never be read: decision, options, recommendation, needed by, cost of waiting a quarter. The cost-of-waiting column is what forces a decision today instead of next time. Then metrics against goal, copied rows. Then wins as outcomes with numbers, not shipped features. Then risks with their movement and the ask attached to each. Then next period as a slice of the real roadmap with its confidence levels, never a parallel roadmap. Two pages, hard cap.

### 5. Pre-wire the room

For each decision, an objection sheet: the stakeholder, placed on the power and interest grid, the objection they will raise, the answer, the evidence line, and what would change your recommendation. The decision-holders see the ask before the meeting. Decision rule: a sponsor who first meets the ask in the room will defer it; a surprise is a deferral with a date.

### 6. Close the loop

Within a day: decisions logged with one decider by name and the options that lost; "noted" is not a decision and is not logged as one. Risk register updated with the asks granted or refused. The written version sent to everyone who was not there. The weekly narrative continues beneath, so the next quarterly has no surprises in it.

## Output format

1. Headline: three sentences, situation, complication, resolution
2. Decisions table: | Decision | Options | Our recommendation | Needed by | Cost of waiting |
3. Metrics against goal, rows copied from the metrics review with confidence intact
4. Wins as outcomes with numbers; risks with movement and the ask
5. Next period: | Theme | Target period | Confidence | What would change this |
6. Objection sheet, for the presenter and not sent: | Stakeholder | Likely objection | Answer | Evidence | What would change our recommendation |
7. After the meeting: the decision log entries and the risk register changes

## Failure modes this skill guards against

- An activity list with no decision in it
- The ask on the last page
- Only the green rows shown
- Numbers computed fresh for the deck, untraceable afterwards
- No cost of waiting, so every decision defers a quarter
- The same deck for every audience
- A sponsor surprised in the room
- A weekly meeting held to read a page aloud
- "Noted" recorded as a decision
- A recommendation hedged across two options

## Exit gate

The update feeds Gate 6 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) through the QBR template and lands its outcomes in the decision log. Do not report it done until every number traces to the metrics review, the decisions table is on the first page with a needed-by date per row, the objection sheet exists, and the whole thing fits in two pages.
