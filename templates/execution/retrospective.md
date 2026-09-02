# Retrospective: [team or initiative], [cycle or milestone]

Stage: any stage, run at the end of each cycle and after each gate; feeds the next cycle's plan and [Gate 6: outcomes verified](../../os/STAGE-GATES.md), whose last check asks what this pass taught us
Knowledge: [retrospective formats](../../frameworks/execution/retrospective-formats.md)
Skill: [postmortem-facilitator](../../skills/postmortem-facilitator/SKILL.md) for the blameless facilitation rules

> **Delete any section you do not need.** Pick one format in section 1 and delete the other three column sets. A retro that runs every format runs none of them. Never leave a heading standing over white space.

<!-- The cycle review that turns what happened into two or three actions with
     owners. It is blameless in the same sense as the incident postmortem: people
     acted reasonably on what they knew, and the review interrogates the system that
     gave them that knowledge. The moment a board item names a person as a cause,
     the next retro collects fiction.

     Neighbours: the incident postmortem (../operate/incident-postmortem.md)
     dissects one operational failure; the post-launch review
     (../operate/post-launch-review.md) judges a launch against its goals; the
     metrics review (../operate/metrics-review.md) reads the numbers. This file is
     about how the team worked.

     Fill first: the facts in section 2, the board in section 3, and the actions in
     section 5. -->

**Facilitator:** [name, not the team lead] · **Scribe:** [name] · **Cycle:** [dates] · **Held on:** [YYYY-MM-DD] · **Attendees:** [roles, count] · **Format:** [start-stop-continue / 4Ls / sailboat / timeline]

## 1. Format choice

<!-- One line each so the choice is a choice. Details and facilitation rules are in
     the formats worksheet. -->

| Format | Pick it when |
|---|---|
| Start, stop, continue | The team wants actions fast and the cycle was ordinary |
| 4Ls (liked, learned, lacked, longed for) | Morale is the question, or a new team is forming |
| Sailboat (wind, anchors, rocks, island) | The team has a shared goal and needs to name what drags on it |
| Timeline | The cycle was long or eventful and memories disagree about what happened when |

**Chosen:** [format], because [one sentence].

## 2. Facts first

<!-- Ten minutes, before any opinion. Pulled from the status reports, the decision
     log, and the tracker, not from memory. Numbers are labeled ILLUSTRATIVE until
     someone checks them against the source. -->

| Date | What happened | Source |
|---|---|---|
| | | |

- Planned versus delivered: [n of n items, or scope points]
- Gate outcome this cycle, if any: [passed / returned, and why]
- Defects found after "done": [n] · Interrupts absorbed: [n, or team-days]

## 3. The board

<!-- Column names follow the chosen format. Everyone writes silently first, then
     items are read out and grouped, then each person votes on the groups they want
     to discuss. Roles are fine; names are not. -->

| Column | Item | Raised by (role) | Votes |
|---|---|---|---|
| | | | |

## 4. Themes and root causes

<!-- A root cause is something the team can change. "The vendor was late" is a
     fact; "we had no fixture to build against while waiting" is a cause. Ask why
     a few times per theme until the answer is inside the team's authority. -->

| Theme | Evidence from the board | Root cause (inside our authority) | Keep or change |
|---|---|---|---|
| | | | |

## 5. Actions

<!-- Two to four. More is a wish list that the next retro will find untouched. At
     least one action stops something; a team that only adds will run out of
     cycle. Verification is how the next retro will know it happened. -->

| Action | Owner | Due | Verification | Status |
|---|---|---|---|---|
| | | | | |

## 6. Previous retro's actions

<!-- The retro opens by reading these. An action carried over twice is either the
     wrong action or the wrong owner; decide which. -->

| Action from last retro | Done (yes / no) | Effect observed | If carried over, what changes |
|---|---|---|---|
| | | | |

## 7. Health of the retro itself

- Did the quieter voices speak, and how does the facilitator know: [one line]
- Attendance against the team: [n of n]
- Duration: [minutes, against the [n]-minute box]
- One thing to change about the next retro: [one line, or "nothing"]

---

## Exit gate (feeds the next cycle's plan and Gate 6: outcomes verified)

Done when every box is honestly ticked. Actions go to the team's tracker; actions that change how the team works also go to [decision-log.md](decision-log.md); the three-sentence lesson goes to the [Gate 6](../../os/STAGE-GATES.md) form when the cycle closes a stage.

- [ ] Facts were on the board before opinions
- [ ] One format was chosen and the reason is written
- [ ] Every theme has a root cause inside the team's authority
- [ ] Two to four actions, each with an owner, a date, and a verification
- [ ] At least one action stops something
- [ ] The previous retro's actions were reviewed with their observed effect
- [ ] No item names a person as a cause
- [ ] Actions are in the tracker, and the ones that change working agreements are in the decision log
- [ ] Signed by the facilitator, [name], [date]
