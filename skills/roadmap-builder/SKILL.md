---
name: roadmap-builder
description: Convert a backlog and a strategy statement into a scored, sequenced, defensible roadmap. Use when a PM has a pile of asks (features, integrations, compliance items, tech debt) and needs a prioritized quarter-by-quarter plan that survives an executive review - RICE scoring with domain-aware guidance, launch gates, dependency and risk columns, and a regulatory calendar overlay.
---

# Roadmap Builder: from backlog pile to defensible sequence

A roadmap fails in review for one of three reasons: the scores are vibes, the sequence ignores dependencies, or a regulator's calendar overrides it in month two. This skill builds the roadmap so all three challenges are answered before they are asked.

## Files this skill drives

- [../../templates/planning/roadmap.md](../../templates/planning/roadmap.md), where the sequenced plan lands
- [../../templates/planning/okrs.md](../../templates/planning/okrs.md), the metric the year is judged on
- [../../templates/execution/dependency-register.md](../../templates/execution/dependency-register.md), the dependency overlay's source of truth
- See also [../../frameworks/systems/cynefin.md](../../frameworks/systems/cynefin.md) (Kurtz and Snowden, 2003) before you accept a dated commitment on an item whose outcome nobody can predict, and [../../frameworks/execution/theory-of-constraints.md](../../frameworks/execution/theory-of-constraints.md) (Goldratt, 1984) when cycle time has climbed for a quarter and every function reports itself busy. Sequencing assumes the line can absorb the sequence; if three of four funded rows aim at stations that are not the constraint, the roadmap is scored correctly and buys nothing
- Method background: [../../knowledge/rice-prioritization.md](../../knowledge/rice-prioritization.md) and [../../knowledge/okrs.md](../../knowledge/okrs.md); read the trap sections before scoring

## When to use

- Quarterly or annual planning from a raw backlog
- Re-planning after a strategy shift, a funding change, or a new regulatory mandate
- Defending a sequence to executives who each sponsor a different item

## Inputs

The backlog (any format), plus (ask if missing): the strategy in one sentence, capacity (teams or rough engineer-months per quarter), hard external dates (regulatory deadlines, scheme mandates, contract commitments), and the metric the year is judged on, taken from the filled-in OKRs template where one exists.

## Workflow

### 1. Normalize the backlog

One row per item: name, type (revenue feature / enabler / compliance / debt / discovery), requesting stakeholder, and the outcome it claims in one sentence. Merge duplicates; split anything larger than a quarter into stages with their own outcomes.

### 2. Score with RICE, domain-aware

RICE is Reach x Impact x Confidence / Effort, originated by Sean McBride at Intercom; the knowledge card above covers its false-precision trap.

- **Reach**: count the unit that matters (merchants, transactions, markets) per quarter. Beware the classic distortion: reach measured in customers hides per-transaction impact. An item touching 5 merchants that carry half the volume outreaches one touching 50 tails.
- **Impact**: score against THE stated metric, not general goodness. 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal.
- **Confidence**: 100% only with data; 80% with strong analogy; 50% for opinion. Anything at 50% gets a discovery task, not a build slot.
- **Effort**: person-months, including compliance and operational readiness effort, which is where payments estimates usually lie.
- Compliance items and hard mandates do NOT get RICE-ranked against features. They get a deadline lane. Ranking a mandate against a revenue feature is how you get to explain to a regulator why the feature won.

### 3. Have the stakeholder conversations

Scores create losers, and a loser who first learns their fate in the review becomes an enemy of the whole sequence. Before sequencing, walk each requesting stakeholder through their item's score, arithmetic visible. For the items that lost, use the saying-no moves from [../../knowledge/roles/triad-decision-rights.md](../../knowledge/roles/triad-decision-rights.md): ask them to stack-rank their own P0s, and ask which outcome the item moves, by how much, and how you would both know. Two outcomes are acceptable: the stakeholder surfaces evidence that changes a score (log the change and the evidence), or they understand why the item waits. Seniority changes no score; only evidence does.

### 4. Sequence with the three overlays

- **Dependency overlay**: for each item, list what must exist first (technical, vendor, license, data), and record each in the dependency register so it gets governed weekly rather than remembered at kickoff. An item with an unbuilt dependency moves after it, whatever its score.
- **Regulatory calendar overlay**: hard external dates pin items to quarters regardless of score. Mark each pinned item with its date and the cost of missing it.
- **Capacity overlay**: fill quarters to 80% of stated capacity, never 100%. The remaining 20% is incident response, review findings and discovery. It WILL be used.

### 5. Attach the program spine

For each quarter: entry gate (what must be true to start), exit gate (what must be demonstrably true to call it done, a number, not a demo), and the top three risks with owner and trigger. A roadmap without gates is a wish list with dates.

### 6. Write the defense page

One page, three parts: the five highest-scored items NOT funded and the one-line reason; the items funded DESPITE lower scores (pinned by mandate or dependency) and why; what would change the sequence (the two assumptions doing the most work).

## Planning as a process

A roadmap built in one sitting is a document; a roadmap the org believes is the residue of a process people were part of. Run the quarter's planning as a three-week campaign:

- **Strategy session, three weeks before the quarter starts.** Leadership restates the strategy sentence and the metric the year is judged on, so teams score against the actual target instead of last quarter's memory. Thirty minutes, written output.
- **Team breakouts, week two.** Each team drafts its slice: normalized items, scores with arithmetic, and its dependency list. Breakouts, not one big room, because a room of forty produces the loudest voice's roadmap.
- **Capacity negotiation, week three.** Slices meet stated capacity and the cuts happen here, in the room, with the stakeholder conversations from step 3 already held. A cut made in a negotiation is owned; a cut discovered in the published roadmap is appealed.
- **Separate the review forums afterward.** The QBR scores last quarter's commitments, number versus number; the initiative review inspects one item's health in depth. One meeting asked to do both does neither, and the roadmap stops being checked against anything.

## Output format

1. Scored backlog table: | Item | Type | R | I | C | E | RICE | Pinned? | Depends on |
2. Quarter-by-quarter sequence with gates and the 80% capacity line shown, written into the roadmap template's fields
3. The defense page

## Rules

- Every score must show its arithmetic; no bare RICE numbers.
- If capacity is unknown, build TWO sequences (lean and full) rather than one fiction.
- The roadmap states what is deliberately NOT being done. A roadmap with no cuts is a list, and lists lose reviews.

## Failure modes this skill guards against

- **Scores that defend nothing.** Reach guessed and never validated, impact defaulting to medium, confidence sitting at full marks, and effort hidden behind sizes nobody calibrated. The arithmetic is real and the inputs are not.
- **Dependency-blind sequencing.** Items slotted into quarters before dependencies are mapped, so two squads collide on a shared service and a gating interface ships after the feature that needs it.
- **The regulatory calendar treated as background.** A filing window or mandate date read as nice to know, so required work misses its deadline or displaces capacity that should have been reserved months earlier.
- **Launch dates with no launch gates.** Dates committed without exit criteria, so done becomes a negotiation each release and stakeholders learn that every date is aspirational.
- **The risk column as decoration.** Risks listed with no owner, trigger or mitigation cost, so the single external dependency detonates silently and the roadmap loses its only defence in review.

## Exit gate

The roadmap feeds the PLANNING track that runs across every stage of [../../os/OPERATING-LOOP.md](../../os/OPERATING-LOOP.md). Do not report it done until the roadmap template's fields are filled, every pinned item carries its external date, and the defense page exists.
