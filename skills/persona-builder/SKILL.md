---
name: persona-builder
description: Turn discovery evidence into the artifacts that name who the product is for and the job they are trying to get done: a job story, sourced personas, a journey map, and an opportunity solution tree. Use when Gate 1 needs personas built on real interviews, when an existing persona has gone stale or unsourced, when the team argues about what the user wants instead of what the evidence says, or when a journey map was drawn from the org chart rather than the user's day. Takes the evidence notes and interview notes from a completed research round; returns the JTBD spec, personas each cited or marked assumption, the journey map, and the opportunity solution tree, distilled into a fundable problem framing.
---

# Persona Builder: sourced claims, not stock photos

Personas fail quietly. A team runs five interviews, someone drafts "Sarah, 34, busy mum" from memory over the weekend, and by the next planning cycle the room debates what Sarah wants as if she were real. She is not; the five interviews are, and nothing in the deck traces back to them. A persona is a claim about real people: every attribute cites an evidence note ID or is marked an assumption with a validate-by date. A persona built from imagination is worse than none, because it launders a guess into a shared fact the whole team then plans against.

## Files this skill drives

- [../../templates/discovery/jtbd-spec.md](../../templates/discovery/jtbd-spec.md), the job statement, written before any persona
- [../../templates/discovery/personas.md](../../templates/discovery/personas.md), two or three personas, each with five or more cited sessions or the ASSUMPTION label
- [../../templates/discovery/journey-map.md](../../templates/discovery/journey-map.md), current and future journey, mapped against the job
- [../../templates/discovery/service-blueprint.md](../../templates/discovery/service-blueprint.md), the journey map's operational twin, run when a fix lives backstage
- [../../templates/discovery/opportunity-solution-tree.md](../../templates/discovery/opportunity-solution-tree.md), opportunities, compared solutions, assumption tests
- [../../templates/discovery/problem-framing.md](../../templates/discovery/problem-framing.md), the single problem the tree distills to
- Worksheets: [../../frameworks/discovery/jtbd-job-map.md](../../frameworks/discovery/jtbd-job-map.md) (Ulwick and Bettencourt, 2008; Moesta, 2020), [../../frameworks/discovery/empathy-map.md](../../frameworks/discovery/empathy-map.md) (Gray and XPLANE, 2005 onward), [../../frameworks/discovery/opportunity-scoring.md](../../frameworks/discovery/opportunity-scoring.md) (Ulwick, 2005), [../../frameworks/discovery/assumption-mapping.md](../../frameworks/discovery/assumption-mapping.md) (Bland and Osterwalder, 2019)
- Reads: [../../templates/discovery/evidence-note.md](../../templates/discovery/evidence-note.md) and [../../templates/discovery/interview-notes.md](../../templates/discovery/interview-notes.md), the sessions this skill builds from
- Method background: [../../knowledge/jobs-to-be-done.md](../../knowledge/jobs-to-be-done.md), [../../knowledge/torres-continuous-discovery.md](../../knowledge/torres-continuous-discovery.md)
- Hands the funded framing to `skills/write-prd/SKILL.md`; an unfunded opportunity stays in the tree, fed weekly

Themes arrive here, they are not made here: [feedback-synthesis](../feedback-synthesis/SKILL.md) turns raw transcripts, tickets and survey text into themes with source counts, and this skill turns those themes into the people and the jobs behind them. If the evidence is still unsynthesized, run that skill first.

## When to use

- A research round has five or more interviews and no persona, job story, or journey map built from them yet
- Gate 1 needs personas and the ones on file are undated, unsourced, or nobody remembers building them
- The team argues about what "the user" wants instead of about what the evidence says
- A journey map or persona was drawn in a workshop, from memory, before or instead of a research round
- An opportunity solution tree has gone two or more weeks without a new branch or a killed one

## Inputs

The evidence set: every evidence note and interview note from the round, with session IDs and the segment each was screened into. The research questions the round was run to answer. The team's current beliefs about the persona, written down before this pass, so later surprises are real.

Ask for what is missing. Fewer than five sessions for a segment: proceed, but title anything built from it ASSUMPTION with a validate-by date. No segment definition: build one from behavior, not title or company size. No job content anywhere in the evidence, no situation, trigger, or outcome in any note: stop and route to [../user-interview/SKILL.md](../user-interview/SKILL.md) first; a persona built before any job evidence exists is a face with no progress behind it.

## Workflow

### 1. Gather the evidence set and count it

Pull every evidence note and interview note from the round, and state the count in the open: sessions, segments, window, and what the sample cannot support. Decision rule: cite session IDs, never a bare count; five sessions split across three segments supports zero personas until each clears the bar alone.

### 2. Segment by behavior and job, never by demographic alone

Cluster sessions by what people do and the job they chase, not by title, age, or company size. Run the empathy map worksheet per segment: says, does, thinks, feels, each cell sourced, and read the contradictions row first; a says versus does gap is usually the real requirement. Decision rule: two clusters sharing a job and differing only in demographics are one segment.

### 3. Write the job story before the persona

Fill the JTBD spec's job statement, situation, motivation, outcome, before opening the persona file, then run the job map worksheet: a struggle score per step from evidence, then the four forces, push, pull, anxiety, habit. The job outlives the persona; if renaming the personas next year would force a rewrite of the job statement, it was written around a person, not the progress being made.

### 4. Build the persona from the evidence rows

Write the evidence table first, session ID then contribution, and only then fill the snapshot, job, goals, pains, behaviors, and distrust sections from it. The format is Alan Cooper's, from The Inmates Are Running the Asylum (1999): one real behavioral pattern, never a composite of everyone the team has met. Cap the count at two or three; past that, the segments deserve separate products or the extras are decoration.

### 5. Mark every unevidenced attribute

The rule this file exists to enforce. Every attribute traces to an evidence note ID, or the whole persona is titled " (ASSUMPTION)" with a validate-by date. Read each finished persona aloud against its own evidence table; an unsupported sentence gets deleted or the label goes on, and the unevidenced-claims line is filled honestly, never left to imply there were none.

### 6. Map the journey against the job, not your funnel

Use the job map's steps, not your product's stage names, as the journey map's columns; a map built from the funnel maps the dashboard, not the user's day. Draw the current journey first from cited evidence, one session ID per emotional low, then sketch only what the future changes. When a fix sits out of the user's sight, open the service blueprint and name the fix owner by person, never by team.

### 7. Find the opportunity, then hand off

Feed the ranked opportunities and the job map's worst steps into the opportunity solution tree, Teresa Torres's tool from Continuous Discovery Habits (2021): one outcome tied to a north star input, opportunities in the customer's words, two or more compared solutions per branch, and the riskiest assumption under each sent through assumption mapping. Opportunity scoring ranks the opportunities that feed the tree; it has no input for an assumption, so it does not substitute here. Decision rule: the top row must be something a customer said; relabel it as a feature and it was a solution tree already. Distill the targeted branch into problem framing and hand it to `skills/write-prd/SKILL.md`; feed the tree weekly, or it re-earns its branches before the next gate.

## Output format

1. The evidence count and its limits, session IDs included
2. The job statement, filed before any persona
3. Two or three personas, each with a five-plus-session evidence table or the ASSUMPTION label
4. The current and future journey map, a session ID at every emotional low, plus a service blueprint where a fix lives backstage
5. The opportunity solution tree: targeted branches chosen by comparison, two or more compared solutions, the test running this week
6. The problem framing distillation, with its owner, and the handoff line naming the next artifact

## Failure modes this skill guards against

- The persona that is a demographic sketch with a stock photo: an age, a title, an adjective, nothing a session ID could check
- Personas that multiply until nobody remembers them, several by the next quarter, none revisited
- The internal-stakeholder persona, built from one sales anecdote and named because a salesperson was in the room
- "Sarah, 34, busy mum" standing in for a job statement, so the job never gets written or sourced
- A journey map drawn from the org chart or the funnel instead of the user's day
- The opportunity tree that is a solution tree with the top row relabeled into the customer's voice
- Personas that outlive the launch they justified, never revisited once the evidence has moved on

## Exit gate

The framing feeds [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md) Gate 1, which asks for personas built on five or more cited interviews, or explicitly marked assumption, and a problem statement with named evidence. Do not report it done until every persona's evidence table is filled or its title says ASSUMPTION, the job statement names no product, the journey map's lows all cite a session, the opportunity tree has a live test this week, and the problem framing names one owner and one decider.
