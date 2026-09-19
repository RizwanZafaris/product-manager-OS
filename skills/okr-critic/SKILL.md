---
name: okr-critic
description: Draft or critique an OKR set so that every key result is an outcome someone could score without asking what the team did. Use when a team is writing OKRs for a period, when a draft needs review before signature, when the key result column has filled with tasks and launches, or when team and company OKRs do not add up. Takes the draft set, or the strategy and last period's scores; returns a critique table with a verdict per line, rewritten key results with baselines and owners, and a cascade check, in the OKR template.
---

# OKR Critic: key results that could fail

An OKR sheet fails in three quiet ways: the key results are tasks, so the sheet scores 1.0 in a quarter the product went nowhere; the numbers have no baseline, so nobody can say what moved; or the team's sheet adds up to nothing the company asked for. This skill reads a draft the way a skeptical scorer will read it at period end, and fixes the lines before signature.

## Files this skill drives

- [../../templates/planning/okrs.md](../../templates/planning/okrs.md), where the accepted set lands with baselines, targets, owners, and guardrails
- [../../templates/planning/roadmap.md](../../templates/planning/roadmap.md), whose items must each name the key result they serve
- [../../templates/operate/metrics-review.md](../../templates/operate/metrics-review.md), where the period's scores are read at Gate 6
- Reads: [../../templates/planning/product-strategy.md](../../templates/planning/product-strategy.md) for the bets the objectives serve, and [../../templates/planning/north-star-metric.md](../../templates/planning/north-star-metric.md) for the tree the key results sit on
- Method background: [../../knowledge/okrs.md](../../knowledge/okrs.md) (Andy Grove, High Output Management, 1983; John Doerr, Measure What Matters, 2018); read the trap section first

## When to use

- Drafting OKRs for a quarter or a cycle, from a strategy and last period's scores
- Reviewing a team's draft before the sponsor signs it
- When the check-in log shows every KR at 1.0 by week six, or none movable at all
- When three teams' OKRs and the company objective they claim do not reconcile

## Inputs

The draft set, or, when there is none, the strategy's bets and last period's scored sheet. Ask for these when missing: the period and the scoring date; the parent objectives this set cascades from; the baseline source for each number (a dashboard, a query, or "unknown", which is itself a finding); and the metric owner per line. If nobody can name where a baseline would come from, the first action is a metric definition, not a target.

## Workflow

### 1. Test every objective

An objective is qualitative, memorable, time-bound, and excludes something. Decision rule: if a reasonable competitor would state it the same way, it is a mission line; ask what this period is for and rewrite. Cap at three per team; a fourth means the strategy has not chosen.

### 2. Run the four tests on every key result

For each KR, record a pass or a fail on each test, with the reason:

- **Outcome, not task.** Could a scorer grade it without asking what the team did? "Ship the auto-extraction flow" fails. "Weekly active teams using auto-extraction rises from [baseline] to [target]" passes. A KR completable while the world stays unchanged is a task.
- **Measurable, with a baseline.** Number, source, and current value present. A target with no baseline is a wish with a number on it; get the baseline before arguing the target.
- **Falls due inside the period.** A lagging metric that cannot move in one cycle needs a leading proxy from the north star tree, labeled as one.
- **Owned.** One name per KR. A team is not an owner.

### 3. Check the count and the mix

Three to five KRs per objective. Six or more means the objective is really two, or the team is listing its dashboard. Keep the KRs whose failure would change a decision. Mark each committed (1.0 expected) or aspirational (0.7 is success); a sheet with no aspirational lines is sandbagged, and one with no committed lines has no floor.

### 4. Check the cascade

Lay the team set beside the parent set. For each team objective, name the parent KR it moves and roughly how much, in the parent's unit. Decision rule: a team KR that moves no parent KR is local hygiene (fine; mark it so, keep it out of the roll-up) or drift. Two teams claiming the same parent KR in full are double-counting; agree the split in writing.

### 5. Add the guardrails

For each objective, name what must not degrade while chasing it: support volume, latency, error rate, a compliance metric, a neighboring team's number. Guardrails are monitored, not scored, each with a watcher; an objective without one can be gamed silently.

### 6. Write the set into the template

Fill the OKR sheet: baseline, target, current, owner, and commitment type per KR; guardrails; a scoring cadence with calendar entries, not intentions. Every roadmap item then names the KR it serves, or a written reason for being on the roadmap.

## Output format

1. Critique table: | Objective or KR | Test failed (outcome / baseline / period / owner / count / cascade) | Why, in one sentence | Rewrite |
2. The rewritten set in the OKR template's tables, with commitment type and guardrails filled
3. Cascade map: | Team objective | Parent KR it moves | Expected contribution, in the parent's unit | Shared with |
4. Open items: metrics with no baseline source, each with an owner and a date

## Failure modes this skill guards against

- **Tasks in the KR column.** The most common corruption; every test above is built to catch it.
- **Targets without baselines.** A number nobody can compare to last period is not a result.
- **The dashboard as OKR sheet.** Eight KRs per objective; nothing is a priority when everything is.
- **All committed, nothing aspirational**, or the reverse. Either way the grading scale carries no information.
- **Cascade by vocabulary.** Team objectives that repeat the parent's words and move none of its numbers.
- **Explaining a 0.3 into a 0.7 at scoring time.** Scores are numbers against numbers; diagnosis belongs in the end-of-period section.
- **Compensation attached to a KR.** Once a KR prices a bonus, every baseline gets negotiated. Flag it and escalate; the sheet cannot fix it.

## Exit gate

The set feeds the PLANNING track across every stage of [../../os/OPERATING-LOOP.md](../../os/OPERATING-LOOP.md); its scores are read at Gate 6 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md). Do not report the set done until every KR passes all four tests, the OKR template's exit gate is honestly checkable, and the scoring dates are on a calendar.

## What checks this

Some checks on this skill run automatically and some depend on a person. This section says which is which. It is generated by `python3 tools/what_checks.py` from the declarations it links to, and CI fails when it falls out of date.

- **Checked by CI on every commit.** This file must carry the seven sections every prose skill carries: `python3 tools/skill_rubric.py --min 7` fails the `skill-rubric` gate in `python3 tools/ci_gate.py` when one is missing. That checks structure, not whether the advice is right.
- **Checked by the runtime.** This skill is declared against Gate 6 in [SKILL.graph.yml](SKILL.graph.yml). Gate 6 is recorded with `pmos gate --bank-id operate`, which refuses the proof unless every question in that bank has been accepted and the bank is the current one, requires the proof to name its `source`, `source_sha256`, `actor_id`, `requester_id`, `decision` and `approved_at`, and rejects self-approval and any approver the bank does not pin. Approver ids are typed, not authenticated, so a recorded approval is a local attestation, not proof of who signed. If the proof's source changes after approval the gate goes stale and nothing later completes until it is proved again. [The journey run](../../examples/journey-run.md) shows all six gates and a stale gate being proved again.
- **Checked by a person.** The runtime checks who approved and that the evidence has not changed. It does not check whether the reasoning in this skill's Workflow was followed well; that judgment belongs to the people who sign the gate. Gate 6 is signed by the product owner and the sponsor, per the sign-off tables in [os/STAGE-GATES.md](../../os/STAGE-GATES.md).
