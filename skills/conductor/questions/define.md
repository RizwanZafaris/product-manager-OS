---
layer: skills
stage: DEFINE
gate: 2
feeds: []
method: ""
aliases: ["DEFINE bank"]
---
# DEFINE bank

Stage: DEFINE, feeds Gate 2 (requirements signed off) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md).
Working handoffs: drafting via [../../../agents/drafting-agent.md](../../../agents/drafting-agent.md); [../../ai-prd/SKILL.md](../../ai-prd/SKILL.md) when a model is inside; [../../../agents/validation-agent.md](../../../agents/validation-agent.md) before the gate.
Questions 1 to 3 run the tree in [../../../os/WHICH-DOCUMENT.md](../../../os/WHICH-DOCUMENT.md) and pick the artifact weight before any template opens. The honest outcome may be "decide and log", in which case the interview ends with one decision-log entry and no document.
Format and ladder: [README.md](README.md).

### DEFINE-1: stakes

Ask: What does being wrong here cost?
Wrong costs: Weight follows stakes; misjudge this and either a quarter of work gets a ticket or a two-day change gets a twelve-section spec.
Evidence class: 5 is acceptable, this is a judgment the user owns; the judgment must still pick one option.
Options: a) an afternoon, which implies decide and log or a ticket. b) a sprint, which implies a ticket with acceptance criteria. c) a quarter, which implies a one-pager or a full PRD. d) a license or a contract, which implies the full stack and a regulatory look.
Cross-examine when: the answer hedges across two options. Move: banned openers, then force one.
Accept when: exactly one option, with one line of reasoning.
Lands in: `execution/decision-log.md` weight entry and STATE.md accepted answers, at every weight.

### DEFINE-2: audience

Ask: Who must read this document and act on it?
Wrong costs: A document written for nobody in particular is read by nobody at all.
Evidence class: named roles, or named people where they exist.
Cross-examine when: the answer is "the team" or "stakeholders". Move: category to name.
Accept when: each reader named with the action their reading triggers.
Lands in: `execution/decision-log.md` weight entry always; at one-pager weight, also `definition/one-pager.md` "Reviewers who must not be surprised" once DEFINE-3 lands the weight (full-PRD and BRD-stack weight route this answer to section 3 "Users and stories" of the PRD and section 4 "Stakeholders" of the BRD instead, filled during those templates' own drafting), and STATE.md accepted answers.

### DEFINE-3: reversibility

Ask: Can this be undone in a day with a flag, or does it set contracts, data models, or public commitments that outlive the team?
Wrong costs: Treating a one-way door as reversible is how a weekend decision becomes a two-year migration.
Evidence class: 2 where the claim is a flag or a rollback path, an artifact should exist; otherwise a reasoned judgment.
Cross-examine when: "we can always roll it back" arrives with no named mechanism. Move: interest to behavior, has that rollback ever been performed?
Accept when: reversible with the mechanism named, or irreversible with what it locks in named. The three answers so far pick the weight; the Conductor states the pick and why before continuing.
Lands in: `execution/decision-log.md` weight entry, plus `definition/one-pager.md` section 3 "Scope" at one-pager weight (full-PRD and BRD-stack weight route this answer into section 4 "Functional scope" of the PRD instead, filled during that template's own drafting), and STATE.md accepted answers.

### DEFINE-4: objective traceability

Ask: Which Gate 1 problem statement does each objective trace to?
Wrong costs: An objective that traces to nothing is scope smuggled past discovery.
Evidence class: 2, the trace itself, objective to problem statement, line by line.
Cross-examine when: an objective traces to a goal, a competitor, or a wish instead of the Gate 1 problem. Move: banned openers, then: cut it, or name the gap out loud in the document.
Accept when: every objective traces, or the untraced ones are cut or explicitly flagged as new scope needing its own discovery.
Lands in: `definition/prd.md` section 2 at full-PRD or BRD-stack weight; `definition/one-pager.md` section 4 at one-pager weight, and STATE.md accepted answers.

### DEFINE-5: how requirements fail

Ask: For each requirement, how does it fail?
Wrong costs: Prose that cannot fail cannot be tested, and its gaps ship silently.
Evidence class: 2, a condition, an expected result, and a measurable threshold per requirement.
Cross-examine when: a criterion contains "works well", "fast", "intuitive", or any word a demo could not falsify. Move: naked numbers, threshold or it is not a criterion.
Accept when: every requirement has a failing condition a tester could stage. Prose that cannot fail is returned, not accepted.
Lands in: `definition/acceptance-criteria.md`, plus `definition/frd.md` at BRD-stack weight, and STATE.md accepted answers.

### DEFINE-6: out of scope

Ask: What is out of scope, and has the sponsor read the list?
Wrong costs: The unwritten exclusion is the launch-week surprise, delivered by the sponsor.
Evidence class: 3, named commitment, the sponsor's written acknowledgment of the list.
Cross-examine when: the list exists but the sponsor has "seen it around". Move: interest to behavior, where is the written yes?
Accept when: the list is written and the sponsor's acknowledgment is dated.
Lands in: `definition/prd.md` section 7 at full-PRD or BRD-stack weight; `definition/one-pager.md` section 5 at one-pager weight, and STATE.md accepted answers.

### DEFINE-7: the assumptions

Ask: Which assumptions is this built on?
Wrong costs: The unsigned assumption is the one that resurfaces in the launch review.
Evidence class: 5, filed properly: each assumption gets a confidence, a validation method, and a validate-by date.
Cross-examine when: the register is empty or every confidence is high. Move: banned openers, an empty register on a new product is itself the strongest claim in the room.
Accept when: each assumption carries all three fields and an owner.
Lands in: `definition/assumptions-register.md` section 1, and STATE.md accepted answers.

### DEFINE-8: overlays

Ask: Does a model produce any user-facing output, and does a financial or data regulator govern any target market?
Wrong costs: A deferred overlay resurfaces later with an eval gap or a regulator's reference number attached.
Evidence class: a stated yes or no per half, each with one line of grounds.
Cross-examine when: either half is "probably not". Move: banned openers, then: which markets, which data, which model, checked against what?
Accept when: both halves answered with grounds. Yes to the model half attaches the AI overlay, eval rows replacing prose criteria via [../../ai-prd/SKILL.md](../../ai-prd/SKILL.md). Yes to the regulator half routes through [../../reg-gap-check/SKILL.md](../../reg-gap-check/SKILL.md) before Gate 2, because the regulated overlay's preconditions freeze here. Yes to both halves activates the regulated overlay itself, which is the rule in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md); a yes on the regulator half alone does not, and STATE.md records what the regulatory owner carries instead.
Lands in: STATE.md position block (overlays active) and `execution/decision-log.md`, and STATE.md accepted answers.

### DEFINE-9: user-facing surface

Ask: Does this change have a user-facing surface? If so, does the UI state inventory list every screen's states with an owner?
Wrong costs: A screen whose states are unlisted ships with gaps in behavior, accessibility, and ownership.
Evidence class: 2, the inventory, or a stated reason the product has no UI.
Cross-examine when: the answer is "we have a UI" but the inventory is missing or incomplete. Move: banned openers, then: name every screen, name its states, name its owner.
Accept when: a filled inventory, or a stated reason the product has no UI.
Lands in: `definition/ui-state-inventory.md` and STATE.md accepted answers.

## Forced pair

On "advance anyway": DEFINE-5, then DEFINE-8. Untestable requirements and an unexamined overlay are the two skips that multiply in cost with every stage they survive.

## Gate 2 rendering

| Gate 2 checklist line | Evidenced by |
|---|---|
| Every objective traces to Gate 1; every requirement traces to a PRD item | DEFINE-4, DEFINE-5 |
| Every acceptance criterion can fail | DEFINE-5 |
| Every NFR target is a number or names a dated owner | DEFINE-5, checked by the validation agent against `definition/nfr.md` |
| Assumptions register complete per assumption | DEFINE-7 |
| Out of scope written and read by the sponsor | DEFINE-6 |
| Sponsor signed the definition artifact at the chosen weight | Human signature on the one-pager, PRD, or BRD sign-off block; the Conductor reports presence or absence, never supplies it |
| AI overlay: eval sets with thresholds, not prose | DEFINE-8, via the ai-prd handoff |
| Regulated overlay: section 0 answered per market, lint green | DEFINE-8, via the reg-gap-check handoff |
