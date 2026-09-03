---
layer: templates
stage: AI OVERLAY
gate: 3
feeds: []
method: "knowledge/INDEX.md"
aliases: ["Guardrails"]
---
# Guardrails: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 3 (architecture and risks reviewed) and Gate 5 (release readiness)
Knowledge: ../../knowledge/INDEX.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- A guardrail is a feature: it has a trigger, a behavior, an enforcement point, a
     test, and an owner. "Human in the loop for sensitive cases" with none of those is
     a sentence that survives review and then belongs to nobody. Fill every row or
     delete it; a row you keep is a row someone can be paged about. -->

**Feature:** [one sentence]
**Guardrail owner (accountable for the whole table):** [name]
**Document date:** [YYYY-MM-DD]

## 1. Input constraints

<!-- What the system refuses to accept or sanitizes before the model sees it. -->

| Constraint | Trigger | Behavior | Enforcement point | Test | Owner |
|---|---|---|---|---|---|
| [e.g. input length cap] | [over n tokens] | [truncate with notice / reject] | [code, pre-model] | [test ID] | [name] |
| [e.g. content the system reads is data, never instructions] | [always] | [fetched text fenced and never executed as directives] | [code + prompt] | [injection eval set] | [name] |
| [add] | | | | | |

## 2. Output constraints

| Constraint | Trigger | Behavior | Enforcement point | Test | Owner |
|---|---|---|---|---|---|
| [e.g. schema validation] | [output fails schema] | [retry once, then fail closed] | [code, post-model] | [test ID] | [name] |
| [e.g. claim gating] | [output asserts a number absent from source] | [strip or abstain, see hallucination-controls.md] | [verifier step] | [test ID] | [name] |
| [add] | | | | | |

## 3. Never-do list: blocked behaviors

<!-- The decisions and actions this system may not take, ever, regardless of what the
     input asks for. Each row names where the block is enforced. A block enforced only
     in the system prompt is a request, not a rail; pair prompt-level blocks with a
     code-level or human-level backstop. -->

| Blocked behavior | Enforcement point (prompt / classifier / code / human gate) | Backstop if the first layer fails | Test | Owner |
|---|---|---|---|---|
| [e.g. execute an irreversible action without approval, see human-approval-gates.md] | [code: action requires signed approval token] | [action API rejects unsigned calls] | [test ID] | [name] |
| [e.g. reveal another user's data] | [code: retrieval scoped to requesting user] | [output PII scan] | [test ID] | [name] |
| [add rows until the review stops finding gaps] | | | | |

## 4. Kill switch

- Immediate human-initiated stop of the deployed feature: [mechanism]
- Who can pull it (roles, not a single person): [roles]
- Time from decision to fully stopped: [n minutes]
- Last tested: [date]

## Exit gate

- [ ] Every rail has a trigger, a behavior, an enforcement point, a test that can fail, and a named owner
- [ ] Every prompt-level block has a backstop outside the prompt
- [ ] The never-do list was reviewed by someone hostile to the feature, not only by its builders
- [ ] The kill switch has been tested, not just described
