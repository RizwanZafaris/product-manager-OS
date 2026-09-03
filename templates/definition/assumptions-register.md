# Assumptions Register: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md); [program-premortem](../../skills/program-premortem/SKILL.md) when an assumption becomes a risk

<!-- Read this before deciding you are too busy for this file.

     This is the most skipped artifact in product work, and skipping it has a
     precise cost: every plan is a stack of guesses, and the unwritten ones are
     load-bearing. When an unwritten assumption fails, it fails in production, in
     the launch review, or in the revenue line, and the team relearns it at the
     most expensive possible moment. Teams do not get burned by the risks they
     listed; they get burned by the ones they were sure enough about to leave
     unwritten. Writing an assumption down costs one row. Not writing it down
     costs whatever the assumption was holding up.

     The practice of mapping assumptions by importance and evidence, then testing
     the important unevidenced ones first, is based on the ideas of David J.
     Bland's assumption-mapping work, restated here in this repo's own words.

     What belongs here: anything the plan treats as true without proof. Demand
     ("users will switch"), behavior ("reps will photograph at capture time"),
     technical ("the vendor API sustains our volume"), business ("finance signs
     the method"), timing ("the partner ships their side by Q3").

     What does not: risks (things that MIGHT happen; risk-register at DESIGN) and
     decisions (things you CHOSE; decision-log). An assumption is something you
     currently believe. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Review cadence:** [weekly during DEFINE and DESIGN]
**Feeds:** [PRD section 9](prd.md) · [BRD sensitivity](brd.md)

## 1. Register

<!-- Confidence is your honest belief the assumption holds. Impact is what breaks
     if it does not. The rows to act on first: low confidence, high impact.
     Status moves: OPEN -> TESTING -> VALIDATED / BUSTED / EXPIRED. -->

| ID | Assumption (stated as a belief that could be false) | Category (demand / behavior / technical / business / timing) | Confidence (high / med / low) | Impact if wrong (high / med / low) | Validation method | Validate by | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| AS-001 | | | | | [the cheapest test that could prove this false] | [date] | | OPEN |
| AS-002 | | | | | | | | |

## 2. Priority view

<!-- Recopy the IDs, nothing else. This is the reading order for a reviewer. -->

- **Test first (low confidence, high impact):** [IDs]
- **Watch (high confidence, high impact):** [IDs]
- **Accept for now (any confidence, low impact):** [IDs]

## 3. Busted assumptions

<!-- A busted assumption is a win: the register did its job before production
     did. Record what it changed so the lesson outlives the project. -->

| ID | What we believed | What turned out to be true | Found how | What changed as a result |
|---|---|---|---|---|
| | | | | |

## 4. Expiry sweep

- **Rows past their validate-by date:** [IDs, or "none"]
- **Action for each:** [retest, re-date with reason, or promote to risk-register at DESIGN]

<!-- An expired row is a silent guess again. The sweep runs at every review
     cadence tick; Gate 2 fails on unexplained expiries. -->

---

### Worked micro-example (illustrative, invented)

> **AS-001:** Field reps will photograph receipts at capture time rather than batching, once first-pass feedback is instant. Category: behavior. Confidence: low. Impact: high (the whole hypothesis rests on it). Validation: two-week prompt experiment with one region, measuring capture-time submissions. Validate by: May 10. Owner: PM. Status: TESTING.
> The point of the row: if it busts, the team learns for the cost of a prompt experiment, not a shipped feature.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every "we assume", "should", and "probably" in the BRD, PRD, and FRD has a row here
- [ ] Every row has confidence, impact, a validation method, a date, and an owner
- [ ] Every low-confidence high-impact row is in TESTING or has a scheduled test
- [ ] The BRD sensitivity assumption appears in the register
- [ ] No row is past its validate-by date without an action recorded
- [ ] Busted assumptions record what changed as a result
