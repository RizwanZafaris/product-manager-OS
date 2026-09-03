---
name: pm-hiring
description: Design and run a PM hiring loop that hires on judgment instead of polish: a scorecard written before any candidate exists, a structured interview loop with a work sample, blind-vote calibration, and a written decision. Use when a PM req opens, when a loop keeps advancing confident storytellers who underperform in the job, when interviewers disagree and the debate is settled by seniority, or when a senior hire is really a stage mismatch. Takes the ladder rung, the seat's scope, and the team's stage; returns the filled hiring scorecard, the interview loop with rubric-linked questions, and the debrief record with the decision.
---

# PM Hiring: scorecard first, candidate second

The bad PM hire is rarely a mystery in hindsight: the rubric was written after the first impressive candidate, the interviews were conversations, and the debrief anchored on the most senior voice. Confident storytelling and framework fluency predict interview success and almost nothing else. This skill fixes the order: define the seat, write the scorecard, run the same structured loop for everyone, vote blind, then decide on evidence rows.

## Files this skill drives

- [../../templates/execution/hiring-scorecard.md](../../templates/execution/hiring-scorecard.md), the scorecard, the loop, and the decision in one document
- [../../templates/planning/first-90-days.md](../../templates/planning/first-90-days.md), which the hired person fills, seeded from the scorecard's outcomes
- Reads: [../../knowledge/roles/ladder.md](../../knowledge/roles/ladder.md) for the rung, [../../knowledge/roles/specializations.md](../../knowledge/roles/specializations.md) for the terrain, [../../knowledge/roles/stage-shift.md](../../knowledge/roles/stage-shift.md) for the stage check
- Method background: [../../knowledge/roles/pm-hiring-and-growth.md](../../knowledge/roles/pm-hiring-and-growth.md), which draws on the structured-interviewing evidence line from Frank Schmidt and John Hunter's selection research (1998 and successors): work samples and structured loops predict, unstructured conversation flatters. Restated here in this repository's own words.

## When to use

- A PM req is approved and no scorecard exists
- Two loops in a row hired well in the room and poorly in the job
- Interviewers split and the debrief resolved it by rank rather than by evidence
- A senior candidate looks perfect on title and the team is at a different company stage

## Inputs

The ladder rung, the product area and where it sits in the operating loop, the hiring manager's name, and the interviewer pool. Ask for these when missing: the outcomes the seat must move in its first year (three, in the unit the business tracks); the specialization terrain (platform, growth, AI, regulated, and so on); the company stage and the candidate's, for the stage-shift check; and the calendar constraint. Decision rule: no candidate is screened until the scorecard exists. A rubric written after the first candidate is a rationalization with rows.

## Workflow

### 1. Define the seat

Pick the rung from the ladder and copy its "owns" and "decides" lines. Name the three outcomes the seat is accountable for, each measurable. Run the stage-shift check: what the candidate's previous company stage rewarded, and whether this seat rewards the same things. Most bad senior hires are stage mismatches wearing a matching title.

### 2. Write the scorecard

Three or four judgment behaviors the rung demands, each with what strong evidence sounds like and what weak evidence sounds like, written as past-behavior signals: killed a bet on evidence, changed a decision with data, wrote the unknowns down as unknowns. Add the one or two must-have constraints (domain, location, regulatory knowledge) and mark everything else as nice to have. Decision rule: if a behavior cannot be evidenced from a candidate's past, it is not on the scorecard.

### 3. Design the loop

One screen of thirty minutes, past behavior only: a decision they got wrong and what they did about it, a bet they killed, evidence that changed their mind. One structured project: the same prompt for every candidate at the rung, timeboxed to two or three hours, graded on reasoning rather than shine; good prompts look like the job, such as a thin discovery document to critique or a messy backlog to sequence with the reasoning shown. Then three or four rubric-linked interviews, each interviewer assigned specific behaviors, so nobody covers everything and nothing goes uncovered. Ban hypotheticals ("how would you prioritize") as scoring evidence; they measure framework fluency, which is the thing to discount.

### 4. Run it the same way for everyone

Same prompt, same questions, same rubric, same timebox. Each interviewer writes evidence rows within an hour of the interview: the behavior, what the candidate said or did, strong or weak. "Great energy" is not a row.

### 5. Debrief with a blind vote

Every interviewer submits a written score and their evidence rows before anyone speaks. Then discuss, rows against rows. Decision rule: a score changes only when an evidence row changes it; seniority changes no score. Where the rows conflict, the hiring manager names the conflict and either resolves it from the rows or sends the candidate to one more targeted interview on that behavior, never to a general "culture" conversation.

### 6. Decide and record

Hire, no hire, or one more interview on a named behavior. The decision names the deciding rows. For a hire, seed the first-90-days plan from the scorecard's three outcomes. For a no hire, record what the loop learned about the scorecard itself; a scorecard that no candidate can meet is describing two seats.

## Output format

1. Seat definition: rung, owns and decides lines, the three outcomes, the stage-shift check result
2. Scorecard table: | Behavior | Strong evidence sounds like | Weak evidence sounds like | Must-have or nice-to-have |
3. Loop plan: | Stage | Interviewer | Behaviors covered | Questions or prompt | Timebox |
4. Debrief record: | Interviewer | Blind score | Evidence rows | Score after discussion | Row that changed it |
5. Decision: hire / no hire / one more interview on [behavior], with the deciding rows, the hiring manager's name, and the date

## Failure modes this skill guards against

- **Interviewing for polish.** The confident narrator who never says "I do not know". The rubric and the blind vote are the two mechanical defenses; use both.
- **The rubric written after the candidate.** It fits the person in the room, and every later candidate is graded against them.
- **Hypotheticals as evidence.** Fluency in frameworks is the thing to discount.
- **The senior voice as tiebreaker.** A five-person loop that becomes one opinion with witnesses.
- **The stage-mismatch hire.** Perfect title, wrong company stage; the check runs before the screen.
- **The unscored project.** A work sample admired for its slides and never graded against the rubric.
- **Notes in the wrong place.** Coaching and evaluation notes live in the company's people system; the scorecard and the calibration source live here.

## Exit gate

The loop feeds [../../templates/execution/hiring-scorecard.md](../../templates/execution/hiring-scorecard.md) and, for a hire, [../../templates/planning/first-90-days.md](../../templates/planning/first-90-days.md). Do not report the hire done until the decision names its evidence rows and the scorecard's outcomes are copied into the new PM's first-90-days plan.
