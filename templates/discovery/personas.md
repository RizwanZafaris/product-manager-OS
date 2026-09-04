---
layer: templates
stage: DISCOVER
gate: 1
feeds: []
method: "knowledge/jobs-to-be-done.md"
aliases: ["Personas"]
---
# Personas: [product or problem space]

Stage: DISCOVER, feeds Gate 1 (problem worth solving)
Knowledge: [Jobs to be done](../../knowledge/jobs-to-be-done.md)
Skill: [persona-builder](../../skills/persona-builder/SKILL.md)

<!-- A persona is a claim about who your user is and what drives them. Claims need
     evidence. This template's hard rule: a persona cites a minimum of FIVE
     interview or session IDs from user-research-plan.md, or it carries the
     ASSUMPTION label in its title. Assumption personas are legal; disguised ones
     are not, because everything built on them inherits the disguise.

     The persona format traces to Alan Cooper's goal-directed design work; the
     "job" line comes from jobs-to-be-done thinking (Ulwick, Christensen, Moesta).
     Both are encoded here in this repo's own words.

     Keep it to two or three personas. Beyond that, either your segments are real
     and deserve separate products, or your personas are decoration.

     Duplicate the persona block below once per persona. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Source study:** [link, e.g. user-research-plan.md]

---

## Persona: [memorable name] [append " (ASSUMPTION)" if the evidence bar below is not met]

### Snapshot

- **Role and context:** [what they do, where, on what device or channel]
- **Segment size:** [how many of them exist for you, with the source of the count]
- **Frequency of contact with the problem:** [daily / weekly / monthly]

### The job

> When [situation], I want to [motivation], so I can [expected outcome].

<!-- One primary job per persona, phrased as progress the person is trying to
     make. If two personas share the identical job and differ only in
     demographics, merge them: demographics without behavioral difference do not
     earn a persona. -->

### Goals and success

- **They consider the day won when:** [observable outcome in their terms]
- **They are measured or judged by:** [their boss's metric, their customer's expectation]

### Pains and workarounds

| Pain | Current workaround | What the workaround costs them |
|---|---|---|
| | | |

### Behaviors that matter to design

[Two to four observed behaviors that should shape the product: tools they live in, moments they act, constraints like gloves, sunlight, deadlines, approvals.]

### What they distrust

[What has burned this persona before: tools, promises, processes. New products inherit that scar tissue.]

### Evidence (mandatory)

<!-- Minimum five distinct session IDs, or retitle this persona with
     " (ASSUMPTION)". Each row states what that session contributed to THIS
     persona, so a reviewer can trace every claim above to a row here. -->

| # | Session ID | What it contributed to this persona |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

**Claims above with no evidence row:** [list them honestly, or "none"]

### Anti-persona note

**Who this persona is NOT:** [the nearby group people will confuse them with, and the one behavioral difference that separates them]

---

### Worked micro-example (illustrative, invented)

> **Persona: Roadside Riya (ASSUMPTION)**
> Field sales rep, files expenses from a phone in a parked car. Job: when a client day ends, I want my receipts filed in one pass, so I can stop thinking about them. Day won when: nothing bounces back. Pain: receipt photos fail validation; workaround: batches a month of receipts on a Sunday, costing an evening and a late close. Evidence: two sessions only (INT-003, INT-007), so this persona carries the ASSUMPTION label until three more sessions land.

---

## How these personas fail

<!-- Personas are the artifact most often produced from the team's own
     assumptions and then cited as evidence for them, which is worse than
     having none. -->

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Invented | Polished profiles, no interview behind any of them, everyone agrees | Each persona cites a source interview, or is labelled an assumption |
| Detail that decides nothing | Age, city, income, a stock photograph, and no decision they change | Every field earns its place by naming a decision it informs |
| One per segment, not per behaviour | Personas mirror the sales segmentation rather than observed use | Split where behaviour differs, and merge where it does not |
| Never updated | Written once, cited for years, product changed underneath | Review on a stated cadence, and mark stale rather than quietly trusting |
| Used to win arguments | "Our persona would not want that", with nothing behind it | If it cannot be traced to evidence, it cannot settle the argument |

## Exit gate (feeds Gate 1: problem worth solving)

<!-- Checkable by someone who did not write this document, which is the
     test of whether a gate is a gate. -->


- [ ] Two or three personas, no more
- [ ] Every persona has five or more evidence rows, or " (ASSUMPTION)" in its title
- [ ] Every persona has exactly one primary job statement
- [ ] No two personas share the same job with only demographic differences
- [ ] Each persona names its anti-persona and the behavioral difference
- [ ] Unevidenced claims are listed, not hidden
