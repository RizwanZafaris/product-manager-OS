---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Exec Update", "exec-update"]
---
# Exec Update: [product or program], [period]

Stage: PLANNING track, runs through every stage; feeds the [gate in progress](../../os/STAGE-GATES.md) by getting its blocking decisions made, and rolls up into the [QBR](../operate/qbr-board-update.md)
Knowledge: [SCR, Minto, in the knowledge index](../../knowledge/INDEX.md)
Skill: [stakeholder-update](../../skills/stakeholder-update/SKILL.md)

> **Delete any section you do not need.** This is one page. When it does not fit, cut section 5, then section 4; never cut section 2. Never leave a heading standing over white space.

<!-- The monthly, or on-demand, one-page read for the executives who fund and
     unblock the work. It ends in asks, because an update with no ask is a
     newsletter and executives do not act on newsletters. The spine is Minto's
     situation, complication, resolution: where we are, what changed, what we need,
     in that order, in the first three sentences.

     Neighbours: the status report (../execution/status-report.md) is the weekly
     instrument this is built from; the QBR (../operate/qbr-board-update.md) is the
     quarterly instrument with metrics against goal; a single decision that needs
     more than a paragraph gets its own decision memo (decision-memo.md).

     Fill first: the headline in section 1, the asks in section 2, and the
     commitments table in section 3. Numbers are copied from the status reports and
     the metrics review; nothing is computed fresh here. -->

**Owner:** [name] · **Period:** [month or dates] · **Audience:** [forum or names] · **Date:** [YYYY-MM-DD]
**Sources:** [links to the status reports and the metrics review this draws on]

## 1. Headline

<!-- Three sentences, one per line, and no more. Situation: where the work stands
     against the plan. Complication: the one thing that changed or is blocked.
     Resolution: what we need from the reader. If the reader stops here, they have
     the ask. -->

- **Situation:** [sentence]
- **Complication:** [sentence]
- **Resolution:** [sentence]

## 2. Asks

<!-- Second, not last, because the page after this may not be read. Each ask is a
     decision with options and a recommendation, never "support" or "awareness".
     Cost of no decision is what makes the ask happen this month rather than next. -->

| Ask | Why now | Options | Our recommendation | Needed by | Cost of no decision by then |
|---|---|---|---|---|---|
| | | | | | |

## 3. Commitments from the last update

<!-- Report against what you said last time, copied verbatim, not against a fresh
     list. A slipped commitment carries its new date; a dropped one carries the
     reason. Readers price the whole update on whether this table is honest. -->

| Commitment made last update | Status (done / on track / slipped to [date] / dropped) | Evidence or reason |
|---|---|---|
| | | |

## 4. Risks and changes

<!-- Movement only. The register holds the full list; this table shows what moved
     since the last update and whether it needs anything from this audience. -->

| Risk or change | Movement (new / worse / same / retired) | What we are doing | Ask, if any | Owner |
|---|---|---|---|---|
| | | | | |

## 5. Metrics that moved

<!-- Only the rows that changed, with their confidence note intact from the
     metrics review. A metric that moved the wrong way appears here with the same
     prominence as one that moved the right way. -->

| Metric | Last update | Now | Why it moved | Confidence | Source |
|---|---|---|---|---|---|
| | | | | | [metrics-review.md](../operate/metrics-review.md) copy |

## 6. Commitments for the next period

<!-- Three to five, dated, in the form a reader can check next time. These become
     section 3 of the next update, verbatim. -->

| Commitment | Date | Owner |
|---|---|---|
| | | |

---

## 7. How this update fails while looking complete

<!-- Every row is a way a status update reads as informative and moves
     nothing. The common thread: the document is written for the writer's
     comfort rather than the reader's decision, and the tell is that nothing
     in it can be disagreed with. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Status theatre | Every row green, no amber, no red, week after week | If nothing is amber, say plainly that nothing is, and expect to be asked why |
| The ask is buried | The decision needed sits under three sections of progress prose | Section 2 is the ask, and the headline states it in one sentence |
| Metrics with no baseline | "Adoption up" with no prior number, no target, no period | Every metric carries prior value, target and the period, in the same row |
| Silent commitment drops | Last period's commitments are not mentioned, and the slipped ones vanish | Section 3 lists every prior commitment and its outcome, including the dropped ones |
| Soft risk language | "Something to keep an eye on", with no owner and no date | A risk names impact, owner, and the date you will know more |
| Written for comfort | Dense narrative celebrating activity, with no choice put to the reader | Lead with the decision: the options, the trade, the recommendation, the deadline |

### Worked micro-example (ILLUSTRATIVE, invented)

<!-- One period of a real-shaped update. It is short on purpose: the failure
     this template exists to prevent is length, not brevity. Note that the ask
     is first, the amber is stated without softening, and last period's
     dropped commitment is named rather than omitted. Delete once real
     content exists. -->

**Headline.** *Receipt extraction ships to one market on 12 June. We need a decision on the second market by 5 June or it slips a quarter.*

**Ask.** *Approve support headcount for a second queue, or confirm we launch market two in Q4. Decision needed by 5 June, owner: you.*

| Commitment from last period | Outcome |
|---|---|
| *Support runbook published* | *Done, 28 May* |
| *Second-market pricing agreed* | ***Not done.** Pricing owner was on leave. Now the critical path for the ask above* |

| Risk | Impact | Owner | We will know more by |
|---|---|---|---|
| *Extraction accuracy on low-light photos is below the pre-launch bar* | *Higher manual entry, support load in week one* | *S. Kaur* | *4 June, from the pilot cohort* |

| Metric | Prior | Now | Target | Period |
|---|---|---|---|---|
| *Median time to file an expense* | *4m 10s* | *2m 55s* | *under 3m* | *pilot, 3 weeks* |

The second commitment row is the point. It slipped, it is stated as slipped, and it is connected to the ask rather than buried. An update that omits it reads better and is worth less.

## Exit gate (feeds the gate in progress and the QBR)

<!-- Checkable by the reader, not the writer. Each box is a fact about the
     document rather than a claim about the work it describes. -->


Done when every box is honestly ticked. Decisions the update produces go to [decision-log.md](../execution/decision-log.md); the quarter's updates roll into [qbr-board-update.md](../operate/qbr-board-update.md); the gate they unblock is in [STAGE-GATES.md](../../os/STAGE-GATES.md).

- [ ] The whole update fits on one page
- [ ] The headline is three sentences in situation, complication, resolution order
- [ ] Every ask has options, a recommendation, a needed-by date, and a cost of no decision
- [ ] Every commitment from the last update is accounted for, slips with a new date, drops with a reason
- [ ] Every number traces to a status report or the metrics review, confidence note included
- [ ] Metrics that moved the wrong way appear with the same prominence as the rest
- [ ] Next-period commitments are dated and owned
- [ ] After the meeting: decisions made are logged within a day
- [ ] Signed by [name], [date]
