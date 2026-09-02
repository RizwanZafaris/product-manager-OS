# Retrospective Formats

Based on the ideas of Norman Kerth, from Project Retrospectives (2001), and of Esther Derby and Diana Larsen, from Agile Retrospectives (2006); the sailboat adapts Luke Hohmann's Speed Boat game from Innovation Games (2006), and the 4Ls come from Mary Gorman and Ellen Gottesdiener (2010). Explained here in this repository's own words.

## What it is for

Turning a period of work into two or three changes that have owners. The format is chosen for what the team needs, not for variety: to change habits, to process a hard period and name what was learned, to surface drag and unspoken risk, or to reconstruct what actually happened when memories disagree. The decision it improves is what the team does differently next cycle, which is the only output a retrospective has. Everything else it produces is conversation.

## Run it when

- The end of a cycle, sprint, or bet
- After a launch, alongside the post-launch review, for the team rather than the outcome
- After an incident, once the postmortem has done the systems analysis
- After a gate that failed, to find what the team knew and did not say

**Skip it when:** the last retrospective's actions are not done. Running another produces a second list on top of the first, and the team learns that the list is decorative. Do the actions, then retro.

## Inputs you need first

- The previous action table, with a status per row
- The cycle's facts: what shipped, what slipped, the metrics, the decision-log entries
- A timeline, if the format needs one, from the status reports and chat history
- A facilitator who is not the team's manager

## The worksheet

### Step 1: choose the format

| Format | The question it asks | Fits when | Does not fit when | Time |
|---|---|---|---|---|
| Start, stop, continue | Which habits change? | A stable team making incremental improvements | A big event needs processing; it also yields the same list every cycle on autopilot | 45 minutes |
| 4Ls (liked, learned, lacked, longed for) | What did we take from this? | After a launch or a hard cycle; a new team; learning matters more than habits this time | A specific failure needs causes: use [five whys](five-whys-fishbone.md) | 60 minutes |
| Sailboat (wind, anchors, rocks, island) | What pushes us, what drags, what could sink us, where are we going? | Goal ambiguity or unspoken risk; cross-team work | A team of three; a team that dislikes metaphor | 60 minutes |
| Timeline | What actually happened, and when? | Memories disagree; a long cycle; after an incident or a missed gate | A short cycle everyone remembers the same way | 90 minutes |

### Step 2: facilitation rules

| Rule | Why |
|---|---|
| Read Kerth's prime directive aloud, paraphrased: everyone did the best job they could with what they knew | It moves the room from blame to conditions |
| Review the last action table first, row by row | A retro that skips this teaches that actions are optional |
| Silent writing before any discussion | Otherwise the loudest voice anchors the room |
| Facts, then feelings, then actions, in that order | Actions proposed before facts are guesses with energy |
| Three dot votes per person; the top three items get actions, the rest are logged | Ten actions is zero actions |
| The manager speaks last and votes last | Rank compresses candour |
| No names in problem statements; roles and conditions only | Same reason as the postmortem |
| Timebox held by the facilitator, not the manager | Overrun retros become status meetings |

### Step 3: the actions table

| # | Action (a change to how we work, verifiable) | Owner (one name) | Due (before the next retro) | How we will know it happened | Status at next retro |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Rules: three actions at most; each has a done-test a reviewer can check without asking the owner; "communicate better" fails the done-test and is not an action. Completion rate = actions done / actions committed, from the previous table. Below half, the next retrospective has one topic: why.

## Reading the result

The same item in three consecutive retros means the retro is not the fix; it is an escalation, and it goes to the decision log or the risk register with a name attached. No "stop" items across several cycles means the team is only adding, which is usually fear. A sailboat with no rocks means the team is not saying what could sink it; run the [premortem](premortem-worksheet.md). A timeline where the facts were known to someone nine days before the team acted is a status-reporting finding, not a people finding. Attendance and the completion rate are the retro's own health metrics; watch them like any other.

## ILLUSTRATIVE example

Invented retrospective for Ledgerline's expense-report copilot team after rollout wave 2 slipped by two weeks. Format: timeline, because the engineering lead and the PM disagreed about when the mailbox-connector defect became known. Previous actions: two of three done.

Timeline extract, three of eleven rows: day 3, connector defect reproduced by the ML engineer and logged; day 5, status report to the sponsor marked green; day 12, wave date moved after the release manager's rehearsal failed on the connector.

Finding: the defect was known nine days before the date moved and was absent from two green status reports. Nobody hid it; the report template had no field for known defects on the wave path.

| # | Action | Owner | Due | Done-test |
|---|---|---|---|---|
| 1 | Status report rule: any known defect on the wave path makes the status amber with a date | copilot PM | next report | The rule is in the report's header comment and the next report applies it |
| 2 | Connector integration test added to the release checklist | engineering lead | before wave 3 | The checklist row exists and a failed run blocks the rehearsal |
| 3 | Wave go or no-go moves to 48 hours after a full rehearsal | release manager | before wave 3 | The wave 3 calendar shows rehearsal, then decision |

## The trap

Start, stop, continue on autopilot. The same format every cycle, the same facilitator, the same twenty minutes; items rotate between the columns, nothing is checked against last time, attendance drifts down, and the retro becomes the meeting people describe as fine. The tell is an action table with no status column filled in. Review last time's actions first, compute the completion rate out loud, and change the format when the list stops changing.

## Feeds

- [Retrospective template](../../templates/execution/retrospective.md), which records the format choice, the facts, and the actions table
- [Decision log](../../templates/execution/decision-log.md), for any decision the retro produced
- [Risk register](../../templates/execution/risk-register.md), for rocks that are risks rather than actions
- [Post-launch review](../../templates/operate/post-launch-review.md), section 3, and [incident postmortem](../../templates/operate/incident-postmortem.md), section 4, for what worked
- Every stage, at the end of each cycle, and after any gate that returned the work, which the [operating loop](../../os/OPERATING-LOOP.md) says to expect
- Method background: [knowledge index](../../knowledge/INDEX.md); the sources above are the reference
