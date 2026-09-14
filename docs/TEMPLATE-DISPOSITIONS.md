# Template dispositions for F21

## Why this exists

Audit finding F21 flagged 40 templates scoring below a diagnostic 70-point bar
in `tools/template_rubric.py` at commit `fefddd1`, and its fix said: review
whether each low score reflects missing teaching or missing examples, or
sensible brevity the regex simply cannot see, and never pad a document just
to move a number. Its acceptance criterion is that each of the 40 receives a
human disposition and a successful representative completion exercise.

This page is that disposition, one row per template. A filled example under
`examples/` is each template's representative completion exercise: it is a
document a PM actually finished, following the template end to end, proving
the template is completable rather than merely fillable in the abstract.

**The owner reviews this table in the pull request.** Every disposition below
is a claim this document makes so it can be checked, not a decision that
closes itself: the score, the commit, and the example are all named so a
reader can verify each row in under a minute rather than trust it.

## Baseline

The "score at fefddd1" column below is read from
`rubric-ec8da5c.json`, the rubric's own `--json` snapshot at commit
`ec8da5c`. That commit sits on the same tree state as `fefddd1` for every
file this table covers: none of the 40 templates named here changed between
the two commits, so the two snapshots agree row for row and the earlier one
is used because it is what this slice's working set carried forward.

## The five dispositions

- **Improved by GLM.** The OpenRouter `z-ai/glm-5.2` writer taught the
  template a genuine missing dimension (guidance comments, traps, tables, or
  links), and the OpenRouter `qwen/qwen3.8-flash` critic accepted the patch.
  Cited by commit.
- **Improved by Claude.** Claude Sonnet wrote the teaching directly, either
  because GLM's critic was never reached (a provider outage) and Claude
  reviewed the patch by hand in its place, or because GLM exhausted both of
  its attempts and Claude wrote the change from the same brief. Cited by
  commit.
- **Example linked and credited.** The template already carried a real,
  completed example under `examples/`; the only defect was in the rubric,
  which had no way to see a worked example living in a separate linked file
  rather than inside the template's own text. No teaching was missing here,
  so none was added: `tools/template_rubric.py`'s `worked_example_link()`
  now credits it, and the pointer line this branch adds is what lets that
  credit find its target. Cited by the two commits that make this true.
- **Brief by design, with a reason.** Not used by any row below: every one
  of the 40 templates, once its example was credited or its genuine gap was
  taught, cleared the bar on measured content rather than on an argument
  that the bar is wrong for it. The category stays in this legend because a
  future audit pass over a different set of templates may need it, and
  because claiming otherwise here, when it was not actually exercised, would
  be exactly the kind of unearned claim F21 warns against.
- **In flight.** One template, named below, whose representative completion
  exercise is not in this tree yet.

## The table

| Template | Stage | Score at fefddd1 | Score now | Filled example(s) | Disposition | Remaining gap |
|---|---|---|---|---|---|---|
| `templates/ai/agent-architecture.md` | AI OVERLAY | 42.5 | 91.7 | [Ledgerline customer add-on](../examples/ledgerline-agent-architecture.md) | Improved by Claude (`06e9086` teach templates/ai/agent-architecture.md (F21)) | None. |
| `templates/ai/ai-interaction-spec.md` | AI OVERLAY | 64.3 | 93.9 | [The Expense Copilot Draft-Report Panel](../examples/ledgerline-ai-interaction-spec.md) | Improved by GLM (`6e35f47` teach templates/ai/ai-interaction-spec.md (F21)) | None. |
| `templates/ai/model-card.md` | AI OVERLAY | 69.2 | 94.2 | [Ledgerline Expense Copilot](../examples/ledgerline-model-card.md) | Improved by GLM (`127fa43` teach templates/ai/model-card.md (F21)) | None. |
| `templates/ai/multi-agent-workflow.md` | AI OVERLAY | 56.2 | 92.9 | [Ledgerline Expense Copilot Receipt Draft](../examples/ledgerline-multi-agent-workflow.md) | Improved by Claude (`10af352` teach templates/ai/multi-agent-workflow.md (F21)) | None. |
| `templates/ai/prompt-structure.md` | AI OVERLAY | 55.8 | 100.0 | [copilot-policy-match](../examples/ledgerline-prompt-structure.md) | Improved by GLM (`70e98b9` teach templates/ai/prompt-structure.md (F21)) | None. |
| `templates/architecture/development-handoff.md` | DESIGN | 10.5 | 82.5 | [Ledgerline expense copilot](../examples/expense-copilot-development-handoff.md) | Improved in slice R6a (`b63567b`); its filled example landed in slice W9f (`0088934`) | None. |
| `templates/architecture/integrations.md` | DESIGN | 56.2 | 73.8 | [Fernbridge Core Platform](../examples/domain-embedded-finance-baas-integrations.md); [Quay Payment Service](../examples/harbourgate-integrations.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/architecture/observability.md` | DESIGN | 68.6 | 90.7 | [Quay payment service](../examples/harbourgate-observability.md) | Improved by GLM (`f252e86` teach templates/architecture/observability.md (F21)) | None. |
| `templates/architecture/security-architecture.md` | DESIGN | 60.5 | 78.0 | [Quay](../examples/harbourgate-security-architecture.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/architecture/sequence-diagram.md` | DESIGN | 47.5 | 95.0 | [Harbourgate web and app card authorisation](../examples/harbourgate-sequence-diagram.md) | Improved by Claude (`0064274` teach templates/architecture/sequence-diagram.md (F21)) | None. |
| `templates/architecture/solution-architecture.md` | DESIGN | 58.3 | 75.8 | [Checkout modernisation (Quay)](../examples/harbourgate-solution-architecture.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/architecture/system-design.md` | DESIGN | 69.2 | 86.7 | [Quay](../examples/harbourgate-system-design.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/definition/prfaq.md` | DEFINE | 62.0 | 79.5 | [Wrenfield Verified Same-Day](../examples/example-prfaq.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/analytics-instrumentation-spec.md` | DELIVER | 60.4 | 77.9 | [Meridian Planner, allied air force deployment](../examples/domain-aerospace-defence-analytics-instrumentation-spec.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/customer-comms.md` | DELIVER | 66.2 | 81.2 | [Harbourgate checkout cutover](../examples/harbourgate-customer-comms.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/edge-cases.md` | BUILD | 61.2 | 76.2 | [Harbourgate Quay checkout payment flow](../examples/harbourgate-edge-cases.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/failure-scenarios.md` | DELIVER | 57.5 | 72.5 | [Driftcast moderation, age assurance and recommendation surfaces](../examples/domain-consumer-social-failure-scenarios.md); [Fernrow Logistics cross-border and last-mile network](../examples/domain-logistics-failure-scenarios.md); [Tradewind Transfers, UK-to-Pakistan cash payout](../examples/domain-remittances-failure-scenarios.md); [Westgate Treasury bulk payment platform](../examples/domain-transaction-banking-failure-scenarios.md); [Larkhollow Air Booking and Disruption Management](../examples/domain-travel-hospitality-failure-scenarios.md); [Harbourgate Quay payment service](../examples/harbourgate-failure-scenarios.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/launch-comms-plan.md` | DELIVER | 57.1 | 72.1 | [Sahulat Bill Pay](../examples/sahulat-launch-comms-plan.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/migration-cutover-plan.md` | DELIVER | 66.2 | 81.2 | [Quay Payment Migration, Plan v2](../examples/harbourgate-migration-cutover-plan.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/sla-slo-definition.md` | DELIVER | 60.6 | 75.6 | [Aldergate Core, real-time posting and overnight batch](../examples/domain-core-banking-sla-slo-definition.md); [Gridline Outage Management (Urban Feeder Restoration)](../examples/domain-energy-utilities-sla-slo-definition.md); [Harbourgate Quay payment service](../examples/harbourgate-sla-slo-definition.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/support-runbook.md` | DELIVER | 63.8 | 78.8 | [Harbourgate payment tickets](../examples/harbourgate-support-runbook.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/testing-strategy.md` | DELIVER | 62.1 | 77.1 | [Harbourgate](../examples/harbourgate-testing-strategy.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/delivery/uat-plan.md` | DELIVER | 55.7 | 70.7 | [Harbourgate Quay payment service](../examples/harbourgate-uat-plan.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/discovery-synthesis.md` | DISCOVER | 50.8 | 95.8 | [Ledgerline commercial pass](../examples/ledgerline-discovery-synthesis.md) | Improved by GLM (`0748985` teach templates/discovery/discovery-synthesis.md (F21)) | None. |
| `templates/discovery/interview-guide.md` | DISCOVER | 67.5 | 82.5 | [Sahulat Bill Pay](../examples/sahulat-interview-guide.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/interview-notes.md` | DISCOVER | 61.1 | 76.1 | [Sahulat Bill Pay (INT-004)](../examples/sahulat-interview-notes.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/jtbd-spec.md` | DISCOVER | 61.7 | 79.2 | [Sahulat Bill Pay](../examples/sahulat-jtbd-spec.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/opportunity-assessment.md` | DISCOVER | 61.2 | 76.2 | [Sahulat Bill Pay](../examples/sahulat-opportunity-assessment.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/survey-design.md` | DISCOVER | 57.5 | 72.5 | [SV-1, Agent-App Bill-Pay Census](../examples/sahulat-survey-design.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/discovery/usability-test-plan.md` | DISCOVER | 65.0 | 80.0 | [Sahulat Bill Pay, menu script v0.3](../examples/sahulat-usability-test-plan.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/execution/change-request.md` | BUILD | 62.5 | 77.5 | [CR-1, AC-3 re-baseline after provider migration decision](../examples/harbourgate-change-request.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/operate/compliance-impact-assessment.md` | DEFINE | 48.5 | 97.5 | [Brightpath Learning K-12 Literacy Platform](../examples/domain-edtech-compliance-impact-assessment.md); [Cobaltine Health Companion](../examples/domain-healthtech-compliance-impact-assessment.md); [Quay](../examples/harbourgate-compliance-impact-assessment.md) | Improved by Claude (`f268e94` teach templates/operate/compliance-impact-assessment.md (F21)) | None. |
| `templates/operate/feedback-program.md` | OPERATE | 46.4 | 96.4 | [Ledgerline Expenses Advisory Board](../examples/ledgerline-feedback-program.md) | Improved by GLM (`01f7945` teach templates/operate/feedback-program.md (F21)) | None. |
| `templates/operate/qbr-board-update.md` | OPERATE | 63.8 | 81.2 | [Ledgerline Expense Copilot, Q4 2026](../examples/ledgerline-qbr-board-update.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/operate/sunset-eol-plan.md` | OPERATE | 54.4 | 96.9 | [Harbourgate legacy payment path (Marlowe, Tidewater, the contractor's wrapper)](../examples/harbourgate-sunset-eol-plan.md) | Improved by GLM (`5b22376` teach templates/operate/sunset-eol-plan.md (F21)) | None. |
| `templates/operate/win-loss-review.md` | OPERATE | 54.2 | 95.8 | [Expense Copilot Add-On, Batch WL-01 to WL-06](../examples/ledgerline-win-loss-review.md) | Improved by GLM (`a288c68` teach templates/operate/win-loss-review.md (F21)) | None. |
| `templates/planning/decision-memo.md` | PLANNING | 57.5 | 72.5 | [Should Ledgerline accept the model vendor's standard subprocessor terms in the customer DPA?](../examples/ledgerline-decision-memo.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/planning/first-90-days.md` | PLANNING | 59.4 | 74.4 | [Hira Baig, Product Manager, Sahulat Bill Pay](../examples/sahulat-first-90-days.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |
| `templates/planning/partner-integration-brief.md` | PLANNING | 68.9 | 96.4 | [Kestrel](../examples/harbourgate-partner-integration-brief.md) | Improved by GLM (`88d736a` teach templates/planning/partner-integration-brief.md (F21)) | None. |
| `templates/planning/positioning.md` | PLANNING | 67.5 | 82.5 | [Expense Copilot](../examples/ledgerline-positioning.md) | Example linked and credited (`8a3e67f` point each flagged template at its filled example(s); `0964f38` credit worked_example for a real linked example) | None. |

## What this table does not claim

A score at or above 70 is a structural signal, not proof of product-management
judgment: F22 already names that gap and this table does not try to close it.
Every "Score now" figure above comes straight from a fresh run of
`python3 tools/template_rubric.py`, so it moves if the rubric or the
templates move again; treat the table as current as of the commit that last
touched it, not as a permanent record.

Filled examples are explicitly fictional, invented for teaching shape rather
than observed from a real product. `examples/README.md` states that, and
this table inherits it: a representative completion exercise proves a
template is completable, not that a real team completed it.
