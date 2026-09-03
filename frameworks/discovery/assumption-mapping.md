---
layer: frameworks
stage: DISCOVER
gate: 1
feeds: ["templates/definition/assumptions-register.md", "templates/discovery/opportunity-solution-tree.md", "templates/operate/experiment-brief.md"]
method: "knowledge/torres-continuous-discovery.md"
aliases: ["Assumption mapping", "assumption-mapping"]
---
# Assumption mapping

Based on the ideas of David J. Bland and Alex Osterwalder, from Testing Business Ideas (2019). Explained here in this repository's own words.

## What it is for

Every product idea is a stack of beliefs, and the dangerous ones are the beliefs nobody has written down. Assumption mapping makes the stack explicit: for the idea to work, what must be true about desirability (do they want it), feasibility (can we build and run it), and viability (does it pay). Each assumption is then placed on a grid of importance against evidence, and the important ones with no evidence get tested first, cheaply, before any of them earns a sprint. Test cards fix the pass criterion before the test runs; learning cards record what happened and what changes. The decision it improves is sequencing: which risk to retire this week.

## Run it when

- A one-pager or PRD is drafted and the team can list its beliefs but not its evidence.
- Before Gate 1 and again before Gate 2, once the opportunity solution tree has picked a solution.
- An experiment is being proposed and nobody can say which assumption it would kill.

**Skip it when:** the idea is a compliance mandate or a fix for something broken. The assumptions are known and settled, and a grid full of "already true" entries is a week of theater.

## Inputs you need first

- The idea in one paragraph, from the [one-pager](../../templates/definition/one-pager.md) or the [discovery document](../../templates/discovery/discovery-document.md) section 4.
- Existing evidence notes with IDs, so an assumption can cite what supports it.
- The [assumptions register](../../templates/definition/assumptions-register.md), which this sheet feeds and reads.

## The worksheet

### 1. Inventory

<!-- Write each as "for this to work, it must be true that...". Importance: 3 = if false, the
     idea dies; 2 = if false, major rework; 1 = if false, a tweak. Evidence: 3 = observed
     behavior or data, linked; 2 = interview claims or artifacts, linked; 1 = team belief,
     nothing linked. An evidence score of 2 or 3 without a linked note is a 1. -->

| ID | It must be true that | Type (D / F / V) | Importance (1 to 3) | Evidence (1 to 3) | Priority = importance minus evidence | Grid cell |
|---|---|---|---|---|---|---|
| D1 | | desirability | | | | |
| F1 | | feasibility | | | | |
| V1 | | viability | | | | |

### 2. Grid

| | Evidence 1 (none) | Evidence 2 (weak) | Evidence 3 (strong) |
|---|---|---|---|
| Importance 3 | Test now | Test next | Watch |
| Importance 2 | Test next | Watch | Accept |
| Importance 1 | Accept | Accept | Accept |

**Decision rule:** test in descending priority; ties go to desirability, because a thing nobody wants makes feasibility moot. Nothing in "test now" waits for a sprint.

### 3. Test card

| Field | Entry |
|---|---|
| Assumption ID | |
| We believe that | [the assumption, restated] |
| To test it we will | [the cheapest test that could prove it false: interview prompt, fake door, concierge run, data pull, spike] |
| We will measure | [the observable, with its source] |
| We are right if | [the threshold, fixed before the test; label it ILLUSTRATIVE until agreed] |
| Cost and duration | [days and people] |

### 4. Learning card

| Field | Entry |
|---|---|
| We believed that | |
| We observed | [counts, quotes, artifacts, with IDs] |
| From that we learned | [one sentence] |
| Therefore we will | [proceed / rewrite the assumption / kill the idea; the new evidence score] |

## Reading the result

A test moves the evidence score, never the importance score; if you find yourself lowering importance after a failed test, the idea is being rescued. An importance-3 assumption that fails kills or pivots the idea, and the register's busted section records it. Passing a test is only a move from 1 to 2 or from 2 to 3; three passes on weak tests do not make strong evidence. When "test now" is empty, the map is done for this stage. When it never empties, the idea is generating assumptions faster than you can retire them, which is itself a result worth reporting.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot.

| ID | It must be true that | Type | Importance | Evidence | Cell |
|---|---|---|---|---|---|
| D1 | Filers will grant the copilot access to their corporate card feed | D | 3 | 1 | Test now |
| V1 | Finance buyers will pay per active filer rather than per seat | V | 3 | 1 | Test now |
| F1 | Receipt extraction from phone photos is accurate enough to trust without review | F | 3 | 2 (vendor demo, note E-017) | Test next |
| D2 | Filers want a nudge the day a charge posts | D | 2 | 2 (five interviews) | Watch |

Test card for D1: in the pilot, show 30 invited filers a real consent screen before any feature is built; we are right if at least 18 grant access (ILLUSTRATIVE threshold, set by the team beforehand). Learning card: 21 of 30 granted; 9 of the 21 asked to exclude a personal card on the same account. Learned: consent is not the barrier, scope control is. Therefore: D1 moves to evidence 3, and a new assumption D3 (filers need per-card exclusion before they trust the feed) enters at importance 2.

## The trap

Evidence inflation. The team scores its belief a 2 because "we have all heard this from customers", nobody can produce the note, and the assumption drifts into the watch cell where nothing gets tested. The rule that saves the map is mechanical: a 2 or a 3 needs a linked evidence note with a date, or it is a 1. The mirror failure is padding the inventory with assumptions already known to be true ("filers need to file expenses") so the grid looks green; if the falsity of an assumption would surprise nobody, it does not belong on the sheet.

## Feeds

- [Assumptions register](../../templates/definition/assumptions-register.md): section 1 (register) takes every row; section 3 (busted assumptions) takes the failed tests
- [Opportunity solution tree](../../templates/discovery/opportunity-solution-tree.md): section 4 (assumptions per solution) and section 5 (assumption tests)
- [Experiment brief](../../templates/operate/experiment-brief.md): sections 1 and 5, when a test outgrows a card
- DISCOVER and DEFINE, feeding [Gate 1: problem worth solving](../../os/STAGE-GATES.md) and Gate 2
- Method background: [Torres, continuous discovery](../../knowledge/torres-continuous-discovery.md); [knowledge index, Lean Startup entry](../../knowledge/INDEX.md)
