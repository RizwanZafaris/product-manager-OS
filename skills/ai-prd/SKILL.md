---
name: ai-prd
description: Write and pressure-test a PRD for an AI or agentic system. Use when a product manager is specifying a feature where the implementer is a model, not an engineer - LLM features, agents, copilots, ML-backed decisions - or when reviewing an existing PRD that says "the AI should" anywhere. Turns acceptance criteria into eval sets, makes non-determinism an explicit requirement, and treats guardrails as features with owners. For products under a financial or data regulator, routes to the regulated module and its byte-exact template.
---

# AI PRD: write requirements a model system can actually be held to

A PRD for an AI system is a different document. Your requirements are not instructions to an engineer; they are constraints on a system that will improvise. This skill restructures the document around that fact.

## Files this skill drives

- [../../templates/definition/prd.md](../../templates/definition/prd.md), the base PRD template
- The AI overlay in `templates/ai/`: [eval-spec.md](../../templates/ai/eval-spec.md), [guardrails.md](../../templates/ai/guardrails.md), [hallucination-controls.md](../../templates/ai/hallucination-controls.md), [human-approval-gates.md](../../templates/ai/human-approval-gates.md), [prompt-structure.md](../../templates/ai/prompt-structure.md), [context-management.md](../../templates/ai/context-management.md), [red-team-review.md](../../templates/ai/red-team-review.md), and for agentic systems [agent-architecture.md](../../templates/ai/agent-architecture.md) and [multi-agent-workflow.md](../../templates/ai/multi-agent-workflow.md)
- For regulated contexts: [../../modules/regulated/templates/regulated-ai-prd-template.md](../../modules/regulated/templates/regulated-ai-prd-template.md), driven by [../../modules/regulated/SKILL.md](../../modules/regulated/SKILL.md)

## When to use

- Specifying any feature where an LLM, agent, or model makes or drafts a decision
- Reviewing an existing PRD that says "the AI should..." anywhere
- Turning a demo into something an engineering team can be accountable for

## The five sections this skill enforces

### 1. Acceptance criteria are eval sets, not sentences

"The agent should extract the merchant name" is a wish. A requirement is:

- A labeled example set (minimum 30 to 50 cases for a first release)
- A pass threshold stated as a number (accuracy, recall at k, or judge score)
- The rule for what happens below threshold (block release, not "review")

For every "should" in the draft, ask: where is the example set, what is the number, who owns adding failing cases back into the set. Capture the answers in [../../templates/ai/eval-spec.md](../../templates/ai/eval-spec.md).

### 2. Edge cases are the spec, not the appendix

The happy path is what the model does for free. The document earns its keep at the boundaries. Require explicit tables for:

- MUST REFUSE: inputs the system declines (out of scope, unsafe, ambiguous beyond repair)
- MUST ESCALATE: conditions that route to a human, with the routing target named; capture triggers and timeout behavior in [../../templates/ai/human-approval-gates.md](../../templates/ai/human-approval-gates.md)
- MUST NEVER INVENT: fields where fabrication is worse than absence (numbers, names, legal or regulatory statements, monetary amounts); the abstain policy lives in [../../templates/ai/hallucination-controls.md](../../templates/ai/hallucination-controls.md)

### 3. Non-determinism goes in writing

The same input can produce a different output tomorrow. The PRD must state:

- Which output variations are acceptable (wording? ordering? formatting?)
- Which are defects (different decision, different number, different refusal behavior)
- Reproducibility posture: temperature and seed policy, and whether logs capture enough to replay any decision

If the PRD does not say this, QA will decide it later, in a bug tracker, angrily.

### 4. Guardrails are features with owners

Each guardrail gets a row in [../../templates/ai/guardrails.md](../../templates/ai/guardrails.md): name, trigger, behavior, owner, test. Minimum set to consider for any agentic feature:

- Fail-closed on unverifiable output (cannot check it = do not ship it to the user)
- Human approval before anything irreversible (sends, payments, deletions, postings)
- Spend and rate caps with a stated ceiling and a stated behavior at the ceiling
- Input isolation: content the system reads is data, never instructions
- Audit trail: who or what decided, based on which inputs, at which model version

### 5. The operations page

- Cost per call target and the alert threshold
- Latency budget per step
- Model version pinning and the upgrade decision process
- Telemetry: what is logged per decision, where evals run (CI, pre-release, production sampling), and the rollback trigger

## The regulated route

Generic PRD tooling writes the five sections above and stops. When the product sits under a financial or data regulator, do not run this skill's own overlay from memory. Start instead from the byte-exact template at [../../modules/regulated/templates/regulated-ai-prd-template.md](../../modules/regulated/templates/regulated-ai-prd-template.md), follow [../../modules/regulated/SKILL.md](../../modules/regulated/SKILL.md), and complete its section 0 (license preconditions, scheme rules, data residency and vendor terms, financial-crime touchpoints, conduct, the audit-proof metric) before any requirement is written. A blank overlay field is a decision deferred to whoever finds it blank. Regulator names, section numbers, and quoted text come only from that module or from primary text the user supplies; never invent them.

## Workflow

1. Classify the context. Regulated: take the regulated route above, then return here for sections the module does not cover. Unregulated: start from the document at the weight already chosen, [prd.md](../../templates/definition/prd.md) or [one-pager.md](../../templates/definition/one-pager.md); the overlay sections below attach to either.
2. Read the draft PRD, or interview the PM if starting blank.
3. Rewrite every "should" statement into the section-1 form. List the ones that cannot be turned into evals; those are not requirements yet, flag them.
4. Build the three edge-case tables. Push for at least 5 rows each; empty tables mean discovery is not done.
5. Write the non-determinism clause and the guardrail table.
6. Produce a one-page GAPS list: every place the original document assumed a deterministic implementer, ranked by blast radius.

## Output format

Return the restructured PRD with the five sections, then the GAPS table:

| # | Gap | Where in original | Blast radius if shipped as-is | Smallest fix |
|---|---|---|---|---|

## Exit gate

This skill's output feeds Gate 2 in [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md). Do not report the PRD done while any requirement lacks a numeric pass condition, any guardrail lacks an owner and a test, or any GAPS row lacks an owner and a date.
