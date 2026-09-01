# PRD: Expense Copilot

Produced with [templates/definition/prd.md](../templates/definition/prd.md). Fictional product, fictional company, every number invented for illustration; thresholds are shown to demonstrate the format, not to recommend values. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Engineering owner:** Priya Nair · **Status:** Approved at Gate 2
**Version:** 2 · **Date:** 2026-08-28

## Background

Discovery ran 2026-07-20 to 2026-08-14 and closed with a GO: see [expense-copilot-discovery.md](expense-copilot-discovery.md). Short version: filers at Fernwood Software re-type receipt data and bounce on category rules they have never read; reviewers burn their time on mechanical checks. The signed hypothesis is that a machine-drafted, human-approved report attacks both bounce causes at once. This PRD defines the first shippable slice. Because the product contains a model, the AI overlay applies: the eval, guardrail, and approval-gate documents named under Launch criteria are part of this spec, not attachments to it.

## Objectives

1. Raise first-submission approval rate for copilot-drafted reports from the 62% baseline toward 80% within one quarter of launch (baseline and method agreed with Daniel Okafor, finance lead, 2026-08-12, from the finance system of record).
2. Cut median filing time for a five-receipt report from 25 minutes to under 10 (baseline from timed sessions in discovery, n=8, so treat as directional).
3. Earn voluntary adoption: half of eligible reports through the draft flow within two months, with no mandate.

## User stories

- As a filer, I photograph or forward a receipt and get a drafted line item (merchant, date, amount, currency, suggested category) that I can accept, edit, or reject, so filing happens in one sitting.
- As a filer, I see the policy line behind every suggested category, so a bounce becomes a conversation with a rule, not a mystery.
- As a filer, nothing is submitted until I review the full report and press submit, so I stay accountable for what goes to finance.
- As a reviewer, machine-drafted fields arrive flagged with the model's confidence, so I spend judgment where it is needed instead of re-checking arithmetic.
- As a finance admin, I can correct a category mapping once and have future drafts follow it, so the system converges on our policy instead of fighting it.

## Functional scope

| # | Capability | Notes |
|---|---|---|
| 1 | Receipt ingestion: photo upload and forwarded email | image and PDF; one receipt per item in v1 |
| 2 | Field extraction: merchant, date, amount, currency | unknown fields are left blank and flagged, never guessed; the never-invent rule follows [templates/ai/hallucination-controls.md](../templates/ai/hallucination-controls.md) |
| 3 | Category suggestion with the matched policy line shown | suggestion only; filer confirms |
| 4 | Draft report assembly and edit surface | filer can edit every field before submit |
| 5 | Confidence flags passed through to the reviewer view | low-confidence fields visually distinct |
| 6 | Admin correction loop for category mappings | corrections logged and versioned |

## Success metrics

| Metric | Baseline | Target | Source | Owner |
|---|---|---|---|---|
| First-submission approval rate, drafted reports | 62% | 80% | finance system of record | D. Okafor |
| Median filing time, five-receipt report | 25 min | under 10 min | in-product timing | M. Chen |
| Eligible reports using draft flow at month two | 0% | 50% | product analytics | M. Chen |
| Guardrail: reviewer-caught extraction errors per 100 reports | n/a (new) | under 3, and never silently rising | reviewer flag button | P. Nair |

Extraction accuracy itself is specified in the eval spec, with a labeled receipt set and a numeric pass threshold; that document, not this table, is what blocks release on model quality.

## Out of scope

- Auto-submission of any report. The filer submits, always; this is a load-bearing guardrail, not a v2 candidate.
- Corporate-card feed reconciliation, mileage, and per-diem rules.
- Filing on behalf of another person (the parked EA workflow from discovery).
- Any use of expense data to train vendor models: contract must forbid it, and the open vendor-terms gap from discovery lives in this PRD's gap list until legal confirms the clause.

## Trade-offs accepted at Gate 2

Left in deliberately, because a worked example where nothing was given up is not a worked example.

| What we wanted | What we shipped instead | Who paid for it | Why we accepted it |
|---|---|---|---|
| Multi-receipt capture in one photo | One receipt per item | Filers with a stack of restaurant slips, who keep photographing one at a time | The extraction eval set could not hold a threshold on overlapping receipts, and shipping a feature that fails on the messiest real case would have cost trust we need for the rest of it |
| Category suggestion trained on our own corrected mappings from day one | Static policy mapping in v1, admin corrections logged but not fed back | The finance admin, who corrects the same mapping more than once this quarter | The feedback loop needs a review step nobody had capacity to design before the launch window, and an unreviewed loop is how a wrong mapping becomes policy |
| An accuracy target agreed with finance | An ILLUSTRATIVE threshold in the eval spec, revisited after four weeks of live data | The team, who cannot yet say the number is a commitment | We had no baseline for machine extraction on our own receipt mix. Agreeing a number we invented would have made the eval gate look rigorous while measuring nothing |

The third row is the uncomfortable one and it is here on purpose: the honest state at Gate 2 was that one of this document's headline quality bars had no agreed number behind it, and the gate passed anyway, with the gap named, owned, and dated rather than dressed up.

## Launch criteria

Launch is Gate 5, and it runs on the delivery and overlay documents, filled for this product:

- [Testing strategy](../templates/delivery/testing-strategy.md), [edge-case register](../templates/delivery/edge-cases.md), and [failure scenarios](../templates/delivery/failure-scenarios.md) complete, with the receipt-storage outage scenario rehearsed.
- [UAT](../templates/delivery/uat-plan.md) with named filers and one finance reviewer, exit criteria met.
- AI overlay: [eval spec](../templates/ai/eval-spec.md) thresholds met on the labeled receipt set, [guardrails](../templates/ai/guardrails.md) each with an owner and a test, [human approval gates](../templates/ai/human-approval-gates.md) confirming no submission path bypasses the filer, and the [red-team review](../templates/ai/red-team-review.md) closed, including the receipt-as-prompt-injection case.
- [Compliance impact assessment](../templates/operate/compliance-impact-assessment.md) signed: receipts carry personal data and the vendor-terms answer gates launch.
- [Release readiness](../templates/delivery/release-readiness.md) signed per function, with rollback owner and trigger named.

First [metrics review](../templates/operate/metrics-review.md) is calendared for four weeks after launch, where objective 1 is graded against the finance system and the persist, pivot, or sunset decision is made in writing.
