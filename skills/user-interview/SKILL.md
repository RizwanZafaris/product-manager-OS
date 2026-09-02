---
name: user-interview
description: Build an interview guide from a research question, run the session on a note sheet that keeps facts apart from compliments, and turn each session into an evidence note. Use when a discovery question needs answers from real users, when Gate 1 cites fewer than five conversations, or when a persona or job statement is still marked assumption. Takes the research questions, a segment, and the team's current beliefs; returns the guide, one note sheet and one evidence note per session, and a handoff to feedback synthesis.
---

# User Interview: questions that get facts, notes that survive the week

Interviews fail quietly. The guide asks whether people would use the idea, the room fills with compliments, the notes blend what was said with what the interviewer hoped, and a week later nobody can tell a pattern from a polite participant. This skill builds a guide that cannot pitch, runs the session so facts and compliments are counted apart, and files each session as evidence a gate can check.

## Files this skill drives

- [../../templates/discovery/interview-guide.md](../../templates/discovery/interview-guide.md), one per study
- [../../templates/discovery/interview-notes.md](../../templates/discovery/interview-notes.md), one per session
- [../../templates/discovery/user-research-plan.md](../../templates/discovery/user-research-plan.md), sections 1 to 5
- [../../templates/discovery/evidence-note.md](../../templates/discovery/evidence-note.md), one per session
- Worksheets: [../../frameworks/discovery/mom-test-interview-guide.md](../../frameworks/discovery/mom-test-interview-guide.md) (Fitzpatrick, The Mom Test, 2013), [../../frameworks/discovery/jtbd-job-map.md](../../frameworks/discovery/jtbd-job-map.md) (Ulwick's job map, Moesta's four forces), [../../frameworks/discovery/empathy-map.md](../../frameworks/discovery/empathy-map.md) (Gray, XPLANE, 2005 onward)
- Method background: the Mom Test entry in [../../knowledge/INDEX.md](../../knowledge/INDEX.md), [../../knowledge/jobs-to-be-done.md](../../knowledge/jobs-to-be-done.md), [../../knowledge/torres-continuous-discovery.md](../../knowledge/torres-continuous-discovery.md)
- Hands the notes to [../../skills/feedback-synthesis/SKILL.md](../../skills/feedback-synthesis/SKILL.md), which owns section 6

## When to use

- A question that tickets and analytics cannot answer: why, not how many
- Before Gate 1, when the discovery document cites fewer than five real conversations
- When a persona, journey map, or JTBD spec is marked assumption
- After Gate 6, when an input moved, the north star did not, and nobody knows why

## Inputs

The research questions, three to five, from section 1 of the research plan, and the decision they serve. The segment and a behavior-based screener. The session count and who interviews. The team's current beliefs, written down before the first session so the surprises are real.

Ask for what is missing. No decision named: stop; interviews with no decision behind them produce a quote reel. No screener: build one from recent behavior ("filed a report in the last thirty days"), never from attitude. No belief log: write one now.

## Workflow

### 1. Turn research questions into things a person could have done

Each research question must be answerable by something a participant did, tried, paid for, or gave up on. Rewrite any question about the future or about liking. Decision rule: a question that can only be answered with "would you" is not an interview question; route it to a survey through `templates/discovery/survey-design.md` or to an experiment through [../../skills/experiment-designer/SKILL.md](../../skills/experiment-designer/SKILL.md). One primary research question per session; a thirty-minute session holds one deep dive, not four.

### 2. Build the guide

Fill the guide from the Mom Test worksheet's script skeleton: opening and consent, a timeline walk ("the last time you did this, start from what triggered it"), the pain and workaround block, the prioritization question, the commitment probe, the close. Add job-map prompts where the pain lives: which of the eight steps (define, locate, prepare, confirm, execute, monitor, modify, conclude) slowed, failed, or got skipped. Add the four forces as probes: push, pull, anxiety, habit.

Three cuts, applied to every question: it names the product or the idea; it contains "would you", "do you like", or "how much would you pay"; it maps to no research question. Cut questions are deleted, not softened.

### 3. Prepare the note sheet

One sheet per session. Columns: timestamp, observation in the participant's words, interpretation, research question touched, and a class: fact, compliment, commitment, or generic. Two people where possible, one asking and one writing. Participant codes, never names. Consent to record captured before the first question.

### 4. Run the session

When they generalize, ask for the last specific time. When they compliment, ask what they do today instead. When they request a feature, ask what it would let them do that they cannot do now, and write down the current workaround. When they pause, wait. Talk far less than they do. Never explain the idea; the moment you pitch, the session stops producing evidence. Close with the commitment probe (time, an introduction, money) and record the answer as given, a polite no included.

### 5. Debrief within the hour

The strongest moment in one sentence, the commitments made or refused, the count of facts against compliments, and every surprise against the belief log. Write one evidence note per session: claim, verbatim quote, evidence class "interview claim", confidence single-source, ledger row copied into STATE.md. Notes written the next day are reconstructions.

### 6. Know when to stop, then hand off

Decision rule for ending a round: the plan's session count per segment is reached, or the last two sessions produced nothing new on the primary research question. A new segment surfacing mid-round is a new round, not an extension. After the fifth session, fill the empathy map with a source ID in every cell; a cell with no source stays empty. Then hand the session IDs, the belief log, and the note sheets to feedback synthesis. Themes are not made here.

## Output format

1. The filled guide, every question tagged with its research question
2. One note sheet per session with the tally: facts, compliments, commitments
3. One evidence note per session, ledger row included
4. A debrief block per session: strongest moment, commitments, surprises
5. The stop decision with its rule, the empathy map, and the handoff line to feedback synthesis with the session IDs

## Failure modes this skill guards against

- Pitching in the room, then recording the polite reaction as demand
- "Would you use this" and "how much would you pay" as research questions
- Compliments counted as evidence; only past behavior and commitments count
- Interviewing the buyer and calling it the user, or recruiting friends
- Notes that blend observation with interpretation
- Six sessions inside one account counted as six sources
- Stopping after two sessions because they agreed with the team
- Theming in the debrief, before the sessions are counted

## Exit gate

The sessions feed Gate 1 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md), which asks for five real user conversations cited by source. Do not report it done until the guide has no cut question left in it, every session has a note sheet and an evidence note, the commitment tally is written, and feedback synthesis has the handoff.
