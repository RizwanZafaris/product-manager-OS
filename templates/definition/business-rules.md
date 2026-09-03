---
layer: templates
stage: DEFINE
gate: 2
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Business Rules Register", "business-rules"]
---
# Business Rules Register: [product or domain name]

Stage: DEFINE, feeds Gate 2 (requirements signed off)
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [write-prd](../../skills/write-prd/SKILL.md)

<!-- A business rule is a decision the organization has already made, which the
     product must enforce rather than re-decide: eligibility, limits, approvals,
     calculations, cutoffs. Rules change on the business's schedule, not the
     release schedule, which is why they live in their own register instead of
     being buried inside requirements.

     Three disciplines make this register worth keeping:
     1. One rule per row, atomic. "Refunds over [n] need approval AND expire
        after 30 days" is two rules.
     2. Every rule names its source of truth: the policy, contract, regulation,
        or named decision it enforces. A rule with no source is a guess with an
        ID, and nobody can safely change it later.
     3. Every rule is traceable to a test. An unenforced rule is a liability
        dressed as a control.

     IDs are permanent: never renumber, never reuse. Retired rules stay in
     section 2 so old behavior stays explicable. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Applies to:** [PRD](prd.md) · [FRD](frd.md)

## 1. Active rules

<!-- Statement pattern: WHEN [trigger condition] THEN [required outcome or
     constraint]. Write the rule so it can be read aloud to the business owner
     and confirmed word for word. -->

| ID | Rule statement (WHEN ... THEN ...) | Trigger point in the product | Source of truth | Business owner | Exceptions | Enforced by (FR ID) | Test traceability |
|---|---|---|---|---|---|---|---|
| BR-001 | | | [policy doc, contract clause, regulation, decision log entry] | [name] | [conditions under which the rule does not apply, or "none"] | FR-[n] | [AC or test ID] |
| BR-002 | | | | | | | |

## 2. Retired rules

| ID | Rule statement | Retired on | Retired by | Why | Replaced by |
|---|---|---|---|---|---|
| | | | | | [new BR ID, or "nothing"] |

## 3. Exception handling

<!-- Exceptions are where rules rot. Each named exception needs its own decider
     and audit trail, or it silently becomes the real rule. -->

| Rule ID | Exception | Who may grant it | Recorded where |
|---|---|---|---|
| | | | |

## 4. Change control

- **Who may change a rule:** [role or name; the business owner of the rule, not the product team]
- **How a change lands:** [request route, approval, and the release path from rule change to enforced behavior]
- **Review cadence:** [when the register is re-confirmed against its sources, e.g. quarterly]

---

### Worked micro-example (illustrative, invented)

> **BR-001:** WHEN an expense line exceeds 500 in local currency THEN the report requires manager approval before payout. Trigger: report submission. Source of truth: Travel and Expense Policy v4, section 3.2. Business owner: the controller. Exceptions: none. Enforced by FR-009. Test: AC-12.
> A month later the policy moves the threshold to 750: the change enters through section 4, BR-001 is retired into section 2, and BR-003 replaces it. The history explains why February reports behaved differently from April reports.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [ ] Every rule is atomic: one trigger, one outcome
- [ ] Every rule names a source of truth a reviewer could open
- [ ] Every rule has a business owner outside the product team
- [ ] Exceptions are enumerated with a decider, or marked "none"
- [ ] Every rule maps to an enforcing FR and a test ID, or carries an owner and date to close the gap
- [ ] Change control names who may change rules and how changes reach production
