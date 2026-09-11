---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["AI products", "ai-products"]
---
# AI products

When the product itself contains a model, two things change that no other domain prepares you for. First, wrong answers become a cost of goods sold: every hallucination spends review time, refunds, support tickets, or user trust, so grounding, abstention, and verification are unit-economics decisions, not quality polish. Second, acceptance criteria stop being binary: the same input can produce different outputs tomorrow, so the eval suite, a scored set of scenarios with pass thresholds, replaces the traditional test plan as the thing that decides whether you may ship. This card orients the domain; the working documents live in [the AI overlay template pack](../../templates/ai/eval-spec.md), which is this domain's template pack.

## Questions a PM must ask

1. What does the eval suite measure, on what golden dataset, with what pass threshold, and does it run against the exact configuration that ships? An eval on last month's model version approves a product nobody is shipping. The [eval-spec](../../templates/ai/eval-spec.md) template holds these answers.
2. What is the cost per task, fully loaded: inference, retries, context, and the human review the error rate forces? Model pricing changes quarterly; a margin built on today's token price needs a dated assumption in the assumptions register.
3. What happens when the model is wrong, and who catches it before the user acts on it? Abstain, verify, escalate to a human, or ship the error; pick per flow, on purpose, in [hallucination-controls](../../templates/ai/hallucination-controls.md) and [human-approval-gates](../../templates/ai/human-approval-gates.md).
4. Where does the EU AI Act place this product? Prohibited, high-risk, transparency-only, or minimal: the classification decides the documentation and conformity burden, and, since the Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026), the high-risk obligations apply from 2 December 2027 for Annex III systems and from 2 August 2028 for high-risk AI embedded in Annex I regulated products (verify current status before relying). Classify early; retrofitting Annex-style technical documentation after build is a rewrite.
5. What is our dependency risk on the model vendor: terms of use, rate limits, deprecation cadence, data-use rights over our prompts? A product is architected differently when the model is a swappable component versus a foundation.
6. What data trained or grounds the system, and do we hold the rights to use it that way? Provenance questions arrive from enterprise buyers, regulators, and rights holders, in that order.
7. What did the red team break? An AI feature that has not been attacked with injections, jailbreaks, and tool-misuse attempts before launch will be attacked after it, on someone else's schedule. [red-team-review](../../templates/ai/red-team-review.md) is the record.
8. Would this feature be better without the model? The honest baseline comparison, against rules or a plain lookup, is the question most AI roadmaps never wrote down.
9. What does the user actually see: which states, which citations, which rating controls, and what happens when the model is withdrawn mid-conversation? The model-facing half is the eval spec; the user-facing half is a separate design decision, specified in [ai-interaction-spec.md](../../templates/ai/ai-interaction-spec.md), and a team that only specs the former ships a feature nobody can tell is working or failing.

## Gatekeepers

- **AI regulation.** The EU AI Act's staged obligations (prohibitions and general-purpose model duties already live; high-risk system duties from 2 December 2027 for Annex III uses and 2 August 2028 for Annex I products, as amended by Regulation (EU) 2026/1744), plus sector regulators claiming AI within their existing powers; for financially regulated products the [regulated module](../../modules/regulated/README.md) carries the verified citations.
- **Model vendors.** Usage policies, rate limits, and deprecations function as platform gates; a vendor policy change is a product change you did not schedule.
- **Enterprise security and procurement.** AI features trigger their own review lane now: data handling, training-use guarantees, and auditability questions arrive before the contract.
- **Privacy regulators.** Training data, prompt logs, and model outputs are all personal data when they contain personal data; the compliance-impact-assessment applies.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Eval pass rate on the shipping configuration | Whether the product does the job today | Passing a stale golden dataset measures yesterday's job |
| Task success rate in production | The eval's claim, checked against reality | Users silently correcting the model looks like success in the logs |
| Cost per completed task | Whether the economics survive usage | Averages hide the long-context and retry tail that dominates spend |
| Escalation and abstention rate | How often the system knows it does not know | Driving it to zero usually means shipping confident errors instead |
| Human review burden per thousand tasks | The hidden headcount in the margin | Falls out of every projection until someone hires the reviewers |
| Error taxonomy trend | Which failure modes grow as usage shifts | An overall accuracy number hides a new failure mode until users find it |
| Citation resolution rate | Whether a citation shown to a user actually points at a real supporting passage | A high rate can mean the model is well grounded, or that citations are only generated for easy queries where retrieval already worked; segment by query difficulty before trusting an aggregate |

## Reading

- **AI Engineering**, Chip Huyen (2025). The build-side canon: evaluation as the central engineering discipline, why application-layer evals matter more than benchmark scores, and how latency, cost, and quality trade against each other in production systems. The eval-first posture of this repository's AI overlay matches her argument.
- **Co-Intelligence**, Ethan Mollick (2024). The adoption side: how people actually work with model output, the jagged frontier where the model is expert and idiot within one task, and why user calibration (knowing when to trust) is a product surface you must design rather than hope for.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays: the AI overlay always fires here), DESIGN-7 (least access for every tool the model can call), BUILD-5 (evals run on the shipping version, no exceptions), and BUILD-6 (what the red team broke, and what changed because of it).

**Templates this bends:** it activates the AI overlay outright; the pack in [templates/ai/](../../templates/ai/eval-spec.md) (eval-spec, guardrails, hallucination-controls, human-approval-gates, red-team-review, ai-interaction-spec, and the agent and prompt templates) is this domain's template pack, and [assumptions-register](../../templates/definition/assumptions-register.md) gains dated rows for model pricing, vendor terms, and regulatory classification.

**Filled in this repo:** [expense-copilot-prd.md](../../examples/expense-copilot-prd.md), the closest fit in the repository: an expense-report copilot whose PRD names the AI overlay outright and holds the never-invent extraction rule (question 3), a guardrail metric separate from the eval threshold, and an explicit "would this be better without the model" cut of the multi-receipt feature (question 8). [expense-copilot-discovery.md](../../examples/expense-copilot-discovery.md) carries the honest baseline (62% first-submission approval before the model) that any eval or task-success claim in this domain has to beat. [ledgerline-north-star-tree.md](../../examples/ledgerline-north-star-tree.md) shows a metric tree input sourced explicitly to "eval set only" with an open field flagging that the live figure is still unknown, the exact discipline question 1 asks for. None of the three fills the AI-overlay documents themselves (eval-spec, guardrails, hallucination-controls, human-approval-gates, red-team-review); those templates are referenced by the PRD but not yet filled as standalone artifacts in this repository, so treat the PRD's citations as the nearest worked answer to what those documents should contain, not as a substitute for filling them.

**Worked example (ILLUSTRATIVE):** a slice of an [eval-spec](../../templates/ai/eval-spec.md) scenario row, in the style of [expense-copilot-prd.md](../../examples/expense-copilot-prd.md)'s never-invent framing (question 1 and question 3 above).

| Scenario | Golden input | Shipping configuration | Pass threshold | Result at last run |
|---|---|---|---|---|
| Receipt with an unreadable merchant field (crumpled or foreign-language) | 40-item labeled receipt set, crumpled/foreign-language subset (12 items) | gpt-ILLUSTRATIVE-model-v3, extraction prompt v7, pinned 2026-08-20 | Field left blank and flagged for reviewer in at least 95% of cases; a guessed merchant name in more than 5% fails the run | 91% blank-and-flag, 9% guessed: BELOW THRESHOLD, ships behind the human-approval gate until the prompt fix in D-06 lands |

This is question 1's discipline in miniature: the eval ran against the exact pinned configuration that ships, the pass line is numeric, and a below-threshold result blocks release rather than getting rounded up to "close enough," the failure mode the card calls a stale golden dataset approving a product nobody is shipping.
