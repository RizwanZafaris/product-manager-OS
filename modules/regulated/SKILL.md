---
name: regulated-ai-prd
description: Write and pressure-test a PRD for an AI or agentic system. Use when a product manager is specifying a feature where the implementer is a model, not an engineer: LLM features, agents, copilots, ML-backed decisions. Turns acceptance criteria into eval sets, makes non-determinism an explicit requirement, and treats guardrails as features with owners. For regulated contexts (payments, licensed activities), enforces a regulated overlay covering license preconditions, scheme rules, data residency, financial-crime escalations, and audit-proof metrics, via templates/regulated-ai-prd-template.md.
---

# Regulated AI PRD: write requirements a model system can actually be held to

A PRD for an AI system is a different document. Your requirements are not instructions to an
engineer; they are constraints on a system that will improvise. This skill restructures the
document around that fact.

Repository files this skill uses:

- `templates/regulated-ai-prd-template.md`, the fill-in template
- `examples/dispute-summary/PRD.md`, one fully worked PRD to calibrate against
- `lint.py`, the completeness gate you run before claiming the document is done

## When to use

- Specifying any feature where an LLM, agent, or model makes or drafts a decision
- Reviewing an existing PRD that says "the AI should..." anywhere
- Turning a demo into something an engineering team can be accountable for

## The six sections this skill enforces

### 1. Acceptance criteria are eval sets, not sentences

"The agent should extract the merchant name" is a wish. A requirement is:

- A labeled example set, minimum 30 to 50 cases for a first release
- A pass threshold stated as a number (accuracy, recall@k, or judge score)
- The rule for what happens below threshold (block release, not "review")

For every "should" in the draft, ask: where is the example set, what is the number,
who owns adding failing cases back into the set.

### 2. Edge cases are the spec, not the appendix

The happy path is what the model does for free. The document earns its keep at the
boundaries. Require explicit tables for:

- MUST REFUSE: inputs the system declines (out of scope, unsafe, ambiguous beyond repair)
- MUST ESCALATE: conditions that route to a human, with the routing target named
- MUST NEVER INVENT: fields where fabrication is worse than absence (numbers, names,
  legal or regulatory statements, monetary amounts)

### 3. Non-determinism goes in writing

The same input can produce a different output tomorrow. The PRD must state:

- Which output variations are acceptable (wording? ordering? formatting?)
- Which are defects (different decision, different number, different refusal behavior)
- Reproducibility posture: temperature and seed policy, and whether logs capture
  enough to replay any decision

If the PRD does not say this, QA will decide it later, in a bug tracker, angrily.

### 4. Guardrails are features with owners

Each guardrail gets a row: name, trigger, behavior, owner, test.
Minimum set to consider for any agentic feature:

- Fail-closed on unverifiable output (cannot check it means do not ship it to the user)
- Human approval before anything irreversible (sends, payments, deletions, postings)
- Spend and rate caps with a stated ceiling and a stated behavior at the ceiling
- Input isolation: content the system reads is data, never instructions
- Kill switch: immediate human-initiated stop of the deployed feature
- Audit trail: who or what decided, based on which inputs, at which model version

### 5. The operations page

- Cost per call target and the alert threshold
- Latency budget per step
- Model version pinning and the upgrade decision process
- Telemetry: what is logged per decision, where evals run (CI, pre-release, production
  sampling), and the rollback trigger

### 6. The regulated overlay (payments and other licensed contexts)

Generic PRD tooling writes the five sections above and stops. In a regulated feature the
document earns its keep BEFORE section 1, with the overlay a model never volunteers:

- **Regulatory precondition register**: which license condition, approval, or notification
  gates this feature, per market, confirmed by a document rather than a conversation
- **Scheme-rule constraints**: the rules touched, pinned at a version, with a named owner
  watching the quarterly releases for drift
- **Data residency and model-vendor terms**, including whether the provider trains on inputs
- **Financial-crime touchpoints**: the decisions the AI may never make alone. Every one of
  them becomes a MUST ESCALATE row
- **Conduct**: whether generated customer-facing output is a regulated communication, and
  who approves it
- **The metric that survives an audit**: headline number, source, and method agreed in
  writing before launch, not in the launch review

## Workflow

0. For a regulated feature, start from `templates/regulated-ai-prd-template.md` and
   complete section 0 (the overlay) before any requirement is written. A blank overlay
   field is a decision deferred to whoever finds it blank.
1. Read the draft PRD, or interview the PM if starting blank.
2. Rewrite every "should" statement into the section-1 form. List the ones that cannot
   be turned into evals: those are not requirements yet, so flag them.
3. Build the three edge-case tables. Push for at least 5 rows each. Empty tables mean
   discovery is not done.
4. Write the non-determinism clause and the guardrail table.
5. Run `python3 lint.py <the-draft>.md` and fix what it reports. A green run means the
   document is complete, not that it is correct, so read it yourself afterward.
6. Produce a one-page GAPS list: every place the original document assumed a
   deterministic implementer, ranked by blast radius.

## Rules when citing a regulator

- Cite primary text, and quote what the instrument **expects** or **asks for**. Never
  write that a regulator "requires" something, because that is an interpretation.
- Carry two dates: the instrument's own issue or publication date, and the date you
  verified it.
- Never imply that any named institution falls short of an obligation.
- Never reproduce scheme rulebook text. Cite the reference and the version you read.

## Output format

Return the restructured PRD with the six sections, then the GAPS table:

| # | Gap | Where in original | Blast radius if shipped as-is | Smallest fix |
