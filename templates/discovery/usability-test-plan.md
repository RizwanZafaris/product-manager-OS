---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: ""
aliases: ["Usability Test Plan", "usability-test-plan"]
---
# Usability Test Plan: [design or prototype name]

Stage: DISCOVER, feeds [Gate 1: problem worth solving](../../os/STAGE-GATES.md); rerun against prototypes in DESIGN and BUILD, where findings feed Gates 3 and 4
Knowledge: [HEART metrics worksheet](../../frameworks/metrics/heart-metrics.md)
Skill: [user-interview](../../skills/user-interview/SKILL.md) for moderation and notes, [research-agent](../../agents/research-agent.md) for recruiting

> **Delete any section you do not need.** Five participants per segment is the usual round; a bigger round is usually better spent as a second round after fixes. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- A usability test evaluates a solution; it does not discover a problem.
     Mixing the two produces a session that pitches and a participant who is
     polite. Problem discovery lives in user-research-plan.md and
     interview-guide.md; what the design is trying to achieve lives in
     ../definition/design-brief.md; what must pass at Gate 4 lives in
     ../definition/acceptance-criteria.md. This plan owns the tasks, the success
     criteria, the script, the severity scale, and the findings. Task success
     and the satisfaction measure come from the HEART worksheet's task-success
     and happiness rows. Fill the tasks and their success definitions first; a
     task with no success definition cannot fail, so it cannot teach. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Piloted / Running / Reported

## 1. What is being tested

| Field | Value |
|---|---|
| Artifact | [prototype, build, or live feature; link] |
| Fidelity and version | [paper / clickable / coded; version id, so findings are attributable] |
| Design questions this round must answer | [two or three, from the design brief] |
| Out of scope this round | [what participants may notice that you will not act on yet] |
| Environment | [lab, remote, in context; device; who sets it up] |

## 2. Participants

<!-- Screen on behavior, from the same segments as the research plan.
     Participant codes replace names everywhere. -->

| Segment | Count | Screener criteria (behavior in the last n days) | Source | Codes |
|---|---|---|---|---|
| | | | | P1 to P[n] |

## 3. Tasks

<!-- Scenarios, not instructions: give the goal and the situation in the
     participant's words, never the name of a control. The starting point is
     stated so every participant begins in the same place. Max time is a field,
     taken from the pilot. The italic row is an invented example on the expense
     copilot. -->

| Task id | Scenario read to the participant | Starting point | Success is | Max time | Data to capture |
|---|---|---|---|---|---|
| T1 | | | [observable end state] | [minutes] | completion, errors, assists, time, path |
| T2 | | | | | |
| *T0* | *"You took a client to lunch yesterday and have the receipt on your phone. Get it into this month's report."* | *home screen, logged in* | *receipt attached to the current report with the amount matching* | *[minutes]* | *as above, plus whether the proposed amount was checked* |

## 4. Success criteria

<!-- Targets are fields agreed before the round, so a result cannot be argued
     into a pass afterwards. Assisted completions count separately: an assist
     is a failure the facilitator rescued. -->

| Measure | Definition | Target agreed before the round | Why this target |
|---|---|---|---|
| Task completion, unassisted | share of participants reaching the success state without help | [target] | |
| Errors per task | wrong paths, recovered or not | [target] | |
| Assists | facilitator interventions needed | [target] | |
| Time on task | median, against the max in section 3 | [target] | |
| Satisfaction | [post-task rating; scale and labels stated] | [target] | |

## 5. Script

- Intro (2 minutes): who we are; we are testing the design, not you; think aloud; there are no wrong answers; you can stop at any time; consent to record confirmed
- Think-aloud reminder: "keep telling me what you expect to happen"
- Facilitator may: repeat the scenario, ask "what would you do next", ask "what did you expect"
- Facilitator may not: explain the interface, answer "is this right", name a control, react to success or failure
- After each task: [the satisfaction question, then "what was hardest about that"]
- Debrief (5 minutes): what would you change first; anything you avoided; thanks and incentive

## 6. Severity scale

<!-- Agree the scale before the round so severity is a judgment against a
     definition, not a negotiation with the designer. Examples are invented. -->

| Level | Definition | Example | Action |
|---|---|---|---|
| 4, blocker | participant cannot complete the task; no recovery | submit control not reachable by keyboard | fix before any release; row in the risk register |
| 3, major | completes with an assist or a serious detour; likely to cause errors in real use | wrong amount accepted without notice | fix before release |
| 2, minor | hesitation or a recoverable wrong turn; task still completes | label misread once, then understood | fix in the next iteration |
| 1, cosmetic | noticed, no effect on completion | spacing, wording preference | backlog |

## 7. Findings

<!-- One row per finding, not per participant. Evidence is a timestamp in a
     recording or a quoted line, so a skeptic can check it. -->

| Id | Task | Participants affected (codes) | What happened | Severity | Evidence (clip time or quote) | Recommended change | Owner |
|---|---|---|---|---|---|---|---|
| F-1 | | | | | | | |

## 8. Results against criteria

| Measure | Target | Result | Met |
|---|---|---|---|
| | | | yes / no |

**Decision:** [ship as is / fix findings rated 3 and above and retest / redesign; decided by name, date]

## Exit gate (feeds Gate 1: problem worth solving)

In DISCOVER, findings enter [discovery-synthesis.md](discovery-synthesis.md); in DESIGN and BUILD, blockers become rows in [risk-register.md](../execution/risk-register.md) and unmet criteria block [acceptance-criteria.md](../definition/acceptance-criteria.md) at [Gate 4](../../os/STAGE-GATES.md).

- [ ] Every task is a scenario in the participant's words with an observable success state
- [ ] Every success measure has a target agreed before the first session
- [ ] The script forbids explaining the interface, and the facilitator followed it
- [ ] Every finding names affected participant codes, a severity against the scale, and checkable evidence
- [ ] Results are recorded against every target, and the decision is signed by name
- [ ] Signed by [name], [date]
