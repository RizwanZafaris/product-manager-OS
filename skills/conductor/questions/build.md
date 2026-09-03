---
layer: skills
stage: BUILD
gate: 4
feeds: []
method: ""
aliases: ["BUILD bank"]
---
# BUILD bank

Stage: BUILD, feeds Gate 4 (acceptance criteria met) in [../../../os/STAGE-GATES.md](../../../os/STAGE-GATES.md).
Working handoffs: [../../../agents/validation-agent.md](../../../agents/validation-agent.md) checks drafts against criteria; [../../../agents/red-team-agent.md](../../../agents/red-team-agent.md) attacks the build, using the filled copy of `templates/ai/red-team-review.md` when a model is inside.
This bank interviews about evidence of testing, not about the code. Demonstrated means a run a reader could reproduce, not a green badge remembered.
Format and ladder: [README.md](README.md).

### BUILD-1: criteria demonstrated

Ask: Which acceptance criteria are demonstrated passing, and for each miss, who owns it and what was decided?
Wrong costs: "Code complete" quietly replaces "criteria met", and the difference ships to customers.
Evidence class: 2, test results a reader could open, criterion by criterion.
Cross-examine when: the answer is a coverage figure or "the suite is green" with no mapping to criteria. Move: naked numbers, then: which criterion, which run, where recorded?
Accept when: every Gate 2 criterion maps to a passing run, or appears as a miss with an owner and a decision.
Lands in: `delivery/testing-strategy.md` results section, and STATE.md accepted answers.

### BUILD-2: undecided edges

Ask: Which edge-case rows are still undecided?
Wrong costs: The rows nobody decided become production incidents decided by whoever is on call.
Evidence class: 2, the edge-case register itself.
Cross-examine when: the register is suspiciously short for the surface area. Move: banned openers, then walk the hunting list in the template together.
Accept when: the undecided count is zero; anything else is a named miss with an owner. Every case has an expected behavior and a linked test.
Lands in: `delivery/edge-cases.md` section 2, and STATE.md accepted answers.

### BUILD-3: failure rehearsal

Ask: Were the failure scenarios exercised, and did detection fire and recovery match the write-up?
Wrong costs: A failure plan that was never run is a guess with a table of contents.
Evidence class: 1, the exercise itself, dated, with what fired and what recovered.
Cross-examine when: "we tested failures" arrives without a date or a scenario name. Move: interest to behavior, which scenario, run when, observed where?
Accept when: each scenario in the table was exercised, detection fired, recovery matched or the divergence is written up.
Lands in: `delivery/failure-scenarios.md` sections 1 and 3, and STATE.md accepted answers.

### BUILD-4: scope drift

Ask: What changed in scope since Gate 2, and where is each change in the decision log with a decider named?
Wrong costs: Scope absorbed to be agreeable leaves a baseline that no longer describes the product.
Evidence class: 2, decision-log entries, one per change, each with a decider.
Cross-examine when: "nothing really changed" on a build of any length. Move: banned openers, then diff the shipped surface against the Gate 2 scope list together.
Accept when: every change is logged with a decider, including the rejections.
Lands in: `execution/decision-log.md`, and STATE.md accepted answers.

### BUILD-5: AI overlay, evals on the shipping version

Ask: Did the eval sets run against the model version that ships, and what happened at each threshold?
Wrong costs: An eval suite run against last month's model is the most common way a green spec produces a red launch.
Evidence class: 2, the eval run, version-stamped, threshold by threshold.
Cross-examine when: the run predates the current model version, or a threshold miss is explained rather than escalated. Move: naked numbers.
Accept when: the run is against the shipping version and every threshold passed or its miss is escalated with an owner. Skip this entry with a cited source when STATE.md says the AI overlay is not active.
Lands in: the workspace copy of `templates/ai/eval-spec.md` results, and STATE.md accepted answers.

### BUILD-6: what the red team broke

Ask: What did the red team break, and was every fix re-tested?
Wrong costs: A fix that was never re-attacked is a hypothesis wearing a checkmark.
Evidence class: 2, the red-team findings and the re-test evidence per fix.
Cross-examine when: the red team found nothing, or a fix's re-test is "should be fine now". Move: banned openers; a clean red-team pass on a first attempt is a finding about the red team.
Accept when: findings listed, every fix re-tested, no unfixed break rated high.
Lands in: the red-team review copy in the workspace and `execution/risk-register.md` for accepted residual risk, and STATE.md accepted answers.

## Forced pair

On "advance anyway": BUILD-1, then BUILD-3. Undemonstrated criteria and unrehearsed failure paths are exactly what Gate 4 exists to catch.

## Gate 4 rendering

| Gate 4 checklist line | Evidenced by |
|---|---|
| Every criterion demonstrated passing, or a miss with owner and decision | BUILD-1 |
| No edge-case row undecided; expected behavior and linked test per case | BUILD-2 |
| Failure scenarios exercised, detection fired, recovery matched | BUILD-3 |
| Coverage meets targets, gaps listed by name | BUILD-1, via the validation-agent handoff against `delivery/testing-strategy.md` |
| Scope changes since Gate 2 all in the decision log with deciders | BUILD-4 |
| AI overlay: evals ran on the shipping version, red team clean or escalated | BUILD-5, BUILD-6 |
