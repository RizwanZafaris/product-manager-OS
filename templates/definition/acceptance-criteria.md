# Acceptance Criteria: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [story-writer](../../skills/story-writer/SKILL.md)

<!-- Acceptance criteria are the pass-or-fail contract between the requirement
     and the release. If a criterion cannot fail, it is a ceremony; if it cannot
     be run, it is a hope. Every criterion here must be executable by a tester
     who has read nothing else.

     The given/when/then form is based on the behavior-driven development work of
     Dan North, restated in this repo's own words: fix the starting state, apply
     one action, assert one observable outcome.

     Three rules:
     1. One behavior per criterion. "And" in a THEN line usually means two
        criteria.
     2. Numbers, not adjectives. "Quickly" is an argument; "within [n] ms at
        p95" is a check. Unagreed numbers are labeled ILLUSTRATIVE.
     3. The unhappy paths are the contract's real value. Every AC group carries
        edge and negative cases; the happy path alone is the demo, not the spec.

     For model-driven behavior, given/when/then is necessary but not sufficient:
     the same input can produce different outputs. Those requirements ALSO need
     an eval set with a threshold; see ../ai/eval-spec.md. Deeper edge-case and
     failure work continues at DELIVER in ../delivery/edge-cases.md and
     ../delivery/failure-scenarios.md.

     IDs are permanent: never renumber, only append. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Covers:** [PRD stories](prd.md) · [FRD requirements](frd.md)

## 1. Criteria

<!-- Duplicate the block per criterion. Group blocks under the story or FR they
     verify. -->

### AC-1 · verifies [USn / FR-nnn]

```
GIVEN [precondition: system state, user state, data on hand]
WHEN  [one action or event]
THEN  [one observable outcome, with its measurable threshold where one applies]
```

- **Type:** happy path / edge / negative
- **Measurable threshold:** [the number that makes this checkable, or "binary outcome"]
- **Test data needed:** [fixtures or accounts required]
- **Automatable:** [yes / no; if no, who runs it manually]

### AC-2 · verifies [USn / FR-nnn]

```
GIVEN
WHEN
THEN
```

- **Type:**
- **Measurable threshold:**
- **Test data needed:**
- **Automatable:**

## 2. Edge and negative case coverage

<!-- Per story or capability: what happens at the boundaries and on bad input.
     Every row becomes a criterion above or names the reason it does not. -->

| Story / FR | Edge or negative condition | Expected behavior | Criterion ID or reason not covered |
|---|---|---|---|
| | [empty input / max length / duplicate / offline / permission denied / timeout] | | |

## 3. Coverage summary

| Story / FR | Happy path ACs | Edge ACs | Negative ACs | Gaps |
|---|---|---|---|---|
| | | | | |

**Must stories with zero negative cases:** [list, or "none"]

---

### Worked micro-example (illustrative, invented)

> **AC-1 · verifies FR-001 (happy path)**
> GIVEN a signed-in rep with camera permission granted
> WHEN the rep captures a legible receipt photo
> THEN the app shows an accept verdict before the submit control activates, within 2 seconds (ILLUSTRATIVE) on a mid-tier device.
>
> **AC-2 · verifies FR-001 (negative)**
> GIVEN the legibility service is unreachable
> WHEN the rep captures a receipt photo
> THEN the app accepts the photo, queues server-side validation, and shows "we will confirm this receipt within a day"; no error state blocks submission.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every must story and must FR has at least one criterion
- [ ] Every criterion has one action and one observable outcome
- [ ] Every threshold is a number, labeled ILLUSTRATIVE where unagreed
- [ ] Every story has edge and negative coverage or a written reason
- [ ] "Must stories with zero negative cases" says "none" or carries an owner and date
- [ ] Model-driven criteria are paired with an eval spec reference
