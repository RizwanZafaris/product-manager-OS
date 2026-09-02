# Empathy map

Based on the ideas of Dave Gray and XPLANE, from the empathy map (2005 onward), Gamestorming (2010), and the Empathy Map Canvas revision (2017). Explained here in this repository's own words.

## What it is for

An empathy map is a one-page portrait of a person doing a job, built from what you observed them say, do, think, and feel, plus the pains and gains they described. Its value is the discipline it forces: every cell carries a source, so the portrait cannot drift into what the team would like the customer to be. The map's best output is the contradiction between says and does, because that gap is where the real behavior, and the real requirement, lives. It improves the persona and the problem statement by grounding both in sessions you can cite, and it is the quickest way to hand a design team the person rather than the segment.

## Run it when

- Five or more sessions are noted and the persona is about to be written or revised.
- The team keeps describing the customer in adjectives ("frustrated", "busy") that no participant used.
- Design needs a one-page brief on the person before sketching starts.

**Skip it when:** you have no session notes. A map filled from memory in a workshop is a persona with adjectives, and it will be quoted as evidence for a year.

## Inputs you need first

- Session notes with IDs and timestamps from [user research plan](../../templates/discovery/user-research-plan.md) section 5.
- Evidence notes for any quote that will carry weight.
- One role and one job per map; a map for "users" is a map of nobody.

## The worksheet

### 1. Frame

| Field | Entry |
|---|---|
| Who we are mapping | [role, segment, the sessions behind it] |
| What they need to do | [the job, in their words] |
| Sessions used | [IDs] |

### 2. The six cells

<!-- Evidence class: observed (you saw or recorded it), said (a quote), inferred (your
     reading; it must cite the observation or quote it comes from). Thinks and feels are
     inferred by definition. An entry with no source goes to section 4, never here. -->

| Cell | Entry (verbatim or observed) | Source (session ID, timestamp) | Evidence class |
|---|---|---|---|
| Says | | | said |
| Does | | | observed |
| Thinks | | | inferred from [source] |
| Feels | | | inferred from [source] |
| Pains | | | |
| Gains | | | |

**Decision rule:** the map is usable when every cell holds at least two entries from two different sessions, and every inferred entry names the observation it comes from.

### 3. Contradictions

| Says | Does | What it might mean | Follow-up question |
|---|---|---|---|
| | | | |

### 4. Unsourced (assumptions)

| Entry | Who believes it | Register ID |
|---|---|---|
| | | |

## Reading the result

Read the contradictions first. Says weekly, does quarterly, means the requirement is not "make filing faster" but "make quarter-end survivable", and the design brief changes. Pains and gains go to the persona's pains and workarounds section and to the problem statement's evidence table; thinks and feels shape tone, defaults, and what the first screen must reassure. Anything in section 4 either gets a session scheduled or gets logged in the assumptions register with an owner. A map with an empty contradictions table is usually a map built from one kind of source; add observation to interviews, or interviews to logs, and look again.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot. Person: a field account executive who travels most weeks, mapped from sessions INT-003, INT-005, and INT-007. Says: "I file everything within the week" (INT-003, 04:10). Does: filed 31 receipts in one sitting on the last Sunday of the quarter (INT-003, calendar and report export; observed). Thinks: "finance is going to bounce this" (inferred from INT-003 reopening the policy PDF twice while narrating, 18:40). Feels: dread at quarter end (INT-005, "I hate that weekend", 11:02). Pains: lost receipts, rejected lines, a three-week reimbursement lag (INT-003, INT-005, INT-007). Gains: card statement matched automatically; never opening the policy PDF again (INT-007, 21:15). Contradiction: says weekly, does quarterly; meaning: the intent is fine and the trigger is missing; follow-up: "what would have made you file on the Tuesday after the trip?" Unsourced: "filers would pay for this themselves", the sales lead's belief, register ID AS-011.

## The trap

The feels cell written in the team's vocabulary. "Frustrated" and "overwhelmed" appear on the map, no participant said either, and the map now certifies an emotion the team supplied. A feeling on this sheet needs a quote or an observed behavior beside it, or it moves to section 4. The companion failure is the composite person: three roles blended into one map so every cell is full and nothing is true of anyone. One role, one job, sourced cells, or do not draw it.

## Feeds

- [Personas](../../templates/discovery/personas.md): the pains and workarounds section and the evidence section
- [Journey map](../../templates/discovery/journey-map.md): section 1 (current journey), the feeling row
- [Problem framing](../../templates/discovery/problem-framing.md): section 4 (evidence)
- [User research plan](../../templates/discovery/user-research-plan.md): section 6 (synthesis themes)
- DISCOVER, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md)
- Method background: [jobs to be done](../../knowledge/jobs-to-be-done.md); [Mom Test interview guide](mom-test-interview-guide.md) for how the source sessions are run
