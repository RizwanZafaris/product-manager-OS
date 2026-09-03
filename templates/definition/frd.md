---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/INDEX.md"
aliases: ["FRD", "Functional Requirements Document"]
---
# Functional Requirements Document: [feature or product name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md)

<!-- The FRD decomposes the PRD's functional scope into individually testable
     requirements, with the data flows and interfaces that connect them. Its
     audience is the people who build and test.

     Traceability is the whole point of this file. Every FR traces up to a PRD
     capability (F-row) and down to at least one acceptance criterion. A
     requirement with no parent is scope creep; a requirement with no test is a
     wish. The matrix in section 5 makes both visible.

     Write each requirement so a tester who has read nothing else can decide
     pass or fail. "The system shall support fast search" fails that bar;
     "search returns results in under [n] ms for a catalog of [n] items" passes. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved · **Version:** [n]
**Parent PRD:** [prd.md](prd.md)

## 1. Functional requirements

<!-- One row per requirement. IDs are permanent: never renumber, only append.
     Priority inherits from the parent story unless stated. -->

| ID | Requirement (testable statement) | Parent capability (PRD F-row) | Priority (must / should / later) | Acceptance criteria ID | Notes |
|---|---|---|---|---|---|
| FR-001 | | F[n] | | AC-[n] | |
| FR-002 | | | | | |

## 2. Data flows

<!-- One block per significant flow. Prose plus a simple step list beats a
     diagram nobody updates; the architecture stage owns formal diagrams in
     ../architecture/sequence-diagram.md. -->

### Flow: [name, e.g. "receipt submission"]

- **Trigger:** [what starts the flow]
- **Steps:**
  1. [actor or system] [does what] with [what data]
  2. [next step]
  3. [next step]
- **Data in:** [fields entering the flow, and their source]
- **Data out:** [fields leaving, and their destination]
- **Failure behavior:** [what the user and the system each see when a step fails]
- **Requirements covered:** FR-[n], FR-[n]

## 3. Interfaces

| Interface | Direction (in / out / both) | Counterpart system | Data exchanged | Contract detail lives in |
|---|---|---|---|---|
| | | | | [../architecture/api-contract.md](../architecture/api-contract.md) or [../architecture/integrations.md](../architecture/integrations.md) |

## 4. Business rule references

[Rules that constrain these requirements live in business-rules.md, not here. List only the rule IDs each FR must honor, e.g. "FR-004 honors BR-002, BR-005". Duplicated rule text drifts; references do not.]

Register: [business-rules.md](business-rules.md)

## 5. Traceability matrix

<!-- The reviewer's map. Every FR appears exactly once. Gaps in either direction
     are findings: an FR without AC cannot be verified; a PRD capability with no
     FRs is not yet specified. -->

| FR ID | PRD capability | Story | Acceptance criteria | Test case (filled at BUILD) |
|---|---|---|---|---|
| FR-001 | F[n] | US[n] | AC-[n] | [test ID when it exists] |

**PRD capabilities with zero FRs:** [list, or "none"]
**FRs with zero acceptance criteria:** [list, or "none"]

---

### Worked micro-example (illustrative, invented)

> **FR-001:** When a receipt photo is captured, the system evaluates image legibility on the device and returns an accept or retake verdict before submission completes. Parent: F1. Priority: must. AC: AC-1.
> **Flow "receipt submission", failure behavior:** on verdict service timeout after [n] ms, the app accepts the photo, queues server-side validation, and tells the user "we will confirm this receipt within a day."

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every FR is testable by a stranger: observable behavior, measurable bound
- [ ] Every FR traces to a PRD capability; both zero-lists in section 5 say "none" or carry an owner and date
- [ ] Every must FR has an acceptance criteria ID
- [ ] Every flow states its failure behavior
- [ ] Every interface row names its counterpart and its contract location
- [ ] Rule constraints are referenced by ID, never pasted in
