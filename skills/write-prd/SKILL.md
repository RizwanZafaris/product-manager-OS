---
name: write-prd
description: Write the general-purpose PRD, and the requirements stack around it (one-pager, BRD, PRD, FRD, NFR, business rules, PR FAQ), sized first against the weight ladder in os/WHICH-DOCUMENT.md. Use when a PM needs to write a PRD or any document in that stack for a feature a human engineering team will build, when a draft has a features table with no objective above it or targets nobody agreed to, or when a request for a PRD has nowhere else in this repository to land. Routes away immediately, before drafting continues, when the implementer is a model (to ai-prd) or a financial or data regulator is in scope (to reg-gap-check). Takes discovery evidence and a weight decision; returns the filled document with kill criteria and a clean pass from spec-review.
---

# Write PRD: objectives before features, a kill switch before launch

Ask this operating system for a PRD before this release and the router had nothing general enough to hand you: ai-prd assumes the implementer is a model, and every other skill assumed you already knew which document you needed. This skill is the ordinary case: a human engineering team building something real. The moment that stops being true, this skill stops too and hands the whole document to [ai-prd](../ai-prd/SKILL.md), explained below in step 2. Past that fork, it exists to stop three more specific failures: a spec written to avoid doing the discovery work, a features table with no objective above it, and a document that can start work but never says how to stop it.

## Files this skill drives

- [../../templates/definition/prd.md](../../templates/definition/prd.md), the primary artifact, run from section 0 (the one-read summary) through section 13 (companion documents), then the sign-off block
- The rest of the requirements stack, at whichever weight applies: [one-pager.md](../../templates/definition/one-pager.md), [brd.md](../../templates/definition/brd.md), [frd.md](../../templates/definition/frd.md), [nfr.md](../../templates/definition/nfr.md), [business-rules.md](../../templates/definition/business-rules.md), [prfaq.md](../../templates/definition/prfaq.md), and [assumptions-register.md](../../templates/definition/assumptions-register.md), which section 11's index points into by row ID
- Reads [../../os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) first, every time, before a section gets drafted; [../../knowledge/cagan-product-teams.md](../../knowledge/cagan-product-teams.md) for the four risks in section 10
- Hands off, not overlaps: [../story-writer/SKILL.md](../story-writer/SKILL.md) for epics and criteria once stories are signed, [../ai-prd/SKILL.md](../ai-prd/SKILL.md) the moment the implementer is a model, [../reg-gap-check/SKILL.md](../reg-gap-check/SKILL.md) with [../../modules/regulated/README.md](../../modules/regulated/README.md) the moment a regulator is in scope, and [../spec-review/SKILL.md](../spec-review/SKILL.md) for the writing check this skill runs before Gate 2

## When to use

- A human engineering team is building this, and the weight ladder in [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) lands at one-pager or heavier
- A draft has a functional scope table with no objective above it, or a target nobody has agreed to
- A request for a PRD has nowhere else in this repository to go, the exact gap this skill closes
- The definition set is heading to Gate 2 and needs its writing tested before a sponsor signs

## Inputs

The problem statement and its evidence from DISCOVER (the discovery document, or at minimum [problem-framing.md](../../templates/discovery/problem-framing.md)), the personas the product serves, and the name of the person who signs at Gate 2. Ask for these when missing: which of the five weights in [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) this decision earns, answered in order rather than guessed; whether the implementer is a model or a regulator is in scope, both of which route away before section 1 gets drafted; and the owner of every target in the objectives table, because a target nobody has agreed to is not a target. If Gate 1 has not passed, stop; a PRD drafted before discovery is the first trap this skill exists to catch.

## Workflow

### 1. Pick the weight

Answer the three questions in [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md), in order, before a single section gets drafted: stakes, audience, reversibility. Land on one of the five weights. If the honest answer is a ticket or a decide-and-log entry, write that instead and stop here; a PRD is not the default, it is what a quarter of work and a sponsor's signature earn. Log the choice and the reason, per that file's own rule.

### 2. Declare the reader

Ask, before section 1: who builds this, a human engineering team or a model. If any capability in scope is an LLM, an agent, or a model making or drafting a decision, or a draft already contains "the AI should" anywhere, stop and hand the whole document to [ai-prd](../ai-prd/SKILL.md); this skill does not also draft eval sets and guardrail rows from memory. If a financial or data regulator governs the product, stop the same way and route through [reg-gap-check](../reg-gap-check/SKILL.md) before writing another section. The regulated module itself is entered only when the product also contains an AI or machine-learning feature, which is the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); for a regulated product with no model, reg-gap-check maps the gaps and the regulatory owner names what covers the rest.

### 3. Write section 0 last, place it first

Section 0, the one-read summary, is the last paragraph drafted and the first thing everyone else reads. Write sections 1 through 13 first; summarizing decisions nobody has made yet produces a confident paragraph about a document that does not exist. Once they exist, compress the problem, who it is for, what ships, how you will know it worked, and what would stop you into under 150 words, then place it at the top.

### 4. Fill objectives before features

Section 2 before section 4, every time. An objective states an outcome in user or business terms with a metric, a baseline, and a target; a feature is a thing that ships. Draft the functional scope table first and the result is a features list wearing a plan's clothing, the single most common way a PRD stops being a decision and becomes an inventory. Every row in section 4 must name the objective it serves before it earns a place in the table.

### 5. Write out of scope before scope

Draft section 7's exclusions before section 4's capability table, even though section 4 sits earlier in the document. Excluding something before any capability names it is a five-minute conversation; excluding it after an engineer has built toward it, or an agent has inferred it, is a scope fight with a sunk cost on one side. An exclusion missing from this table is not neutral: the reader assumes it is in.

### 6. Force kill criteria

Section 9 exists because nothing in the landscape this operating system was checked against has it: every system surveyed can start work, and none can stop it. Do not accept "ongoing" or "we will know it when we see it" for a kill row. Each one needs a metric or a date, a threshold, a check point on the calendar, and a named person who calls it, the same rigor section 8's launch criteria already get.

### 7. Force the strongest evidence against

For each of the four risks in section 10, write the strongest evidence against the answer just given, not the evidence for it restated in different words. A risk cell with nothing arguing against it was not actually interrogated; failing to find counter-evidence is itself a finding, and it belongs written in the cell, not left as silence.

### 8. Run spec-review

Before this document goes near its signer, run [spec-review](../spec-review/SKILL.md) against it. Fix every blocking finding. Carry a should-fix finding forward with a named owner if you disagree it blocks, rather than deleting the row. A PRD that has never had its prose tested reads clean to the person who wrote it and unravels at the first engineering question.

### 9. Take it to Gate 2 with a named signer

Gate 2 in [os/STAGE-GATES.md](../../os/STAGE-GATES.md) asks the same questions at every weight: does every requirement have a pass condition, does every assumption have an owner. A clean spec-review is evidence, not a signature; find the approver named in the sign-off block, or the sponsor named in `brd.md` at the heavier weight, and get the date.

## Output format

The filled document at the chosen weight, in the template's own section numbers, plus two things that are not decoration:

1. Section 13's companion table, filled only with rows a trigger actually fired: companion document, trigger. Drawn from `templates/delivery/`, `templates/architecture/`, `templates/operate/`, `templates/planning/`, `templates/execution/`, and the AI and regulated overlays above. A row nobody triggered does not appear; it is never filled with N/A. One short mandatory spine plus a table of companions added by product type is the adapt-in pattern, borrowed from the BMAD-METHOD project's PRD template.
2. The one-line weight rationale for the decision log: the weight chosen, from [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md), and why.

## Failure modes this skill guards against

- **The PRD written instead of the discovery, not after it.** A spec written to avoid doing the discovery work reads fluent and was never tested against a real user; if Gate 1 has not passed, this skill has nothing to draft against yet.
- **The superset filled section by section until nobody reads it.** Working straight down the template instead of starting with the load-bearing fields produces a document long enough that the reader skims section 2 and never notices section 9 is empty.
- **Targets nobody agreed to.** A number typed into the objectives table by the PM alone is a hope with a decimal point; label it ILLUSTRATIVE until the metric owner has actually agreed it.
- **"The system should be fast."** Every unquantified adjective in a requirement is a decision deferred to whoever builds it first. [spec-review](../spec-review/SKILL.md) catches these after the fact; this workflow exists to stop writing them in the first place.
- **A features table with no objective above it.** Section 4 with no section 2 behind it is an inventory, not a plan; step 4 above is the guard.
- **Open questions used as a graveyard.** An open question with no owner and no needed-by date is not open, it is abandoned, and an uncapped table of them stops getting read by anyone.
- **The prototype that already answered the question the PRD is re-asking.** If usability or value risk in section 10 was already settled by a clickable prototype, cite the test and its result; a paragraph re-asking a question an afternoon of user testing already answered wastes both.
- **Scope creep entering through the FRD, not the scope table.** Section 4 is the contract of record for what ships; an FRD requirement with no parent capability is scope creep that skipped the argument, and it only reaches `frd.md`'s own exit gate if this skill's handoff actually sends the drafter there.

## Exit gate

This skill's output feeds Gate 2 in [os/STAGE-GATES.md](../../os/STAGE-GATES.md), at whichever weight [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md) chose. Do not report the document done while any objective lacks a metric, any kill criterion lacks a threshold and a named caller, any risk's evidence-against cell is empty, or [spec-review](../spec-review/SKILL.md) has not returned a clean pass on the current draft. A clean spec-review is evidence, not a signature; the approver named in the sign-off block still has to read it and sign.
