# Acceptance Criteria: Expense Copilot

Fills [templates/definition/acceptance-criteria.md](../templates/definition/acceptance-criteria.md). Everything here is invented and ILLUSTRATIVE: Ledgerline, its people and every date, id and threshold below are fiction, drawn from [expense-copilot-journey.md](expense-copilot-journey.md)'s data sheet and [ledgerline-journey.md](ledgerline-journey.md)'s N-rows so this pass-or-fail contract agrees with the rest of the internal-v1 chain, not to describe any real expense tool or receipt-extraction model. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-08-28 · **Status:** Approved at Gate 2, SIGNED (V7, V8)
**Covers:** [PRD functional scope](expense-copilot-prd.md#functional-scope) and [user stories](expense-copilot-prd.md#user-stories) · REQ-1 to REQ-6 and AC-1 to AC-10 in [the journey's shared identifiers](expense-copilot-journey.md#shared-identifiers)

## 1. Criteria

Ten criteria, AC-1 to AC-10, ids fixed by [expense-copilot-journey.md](expense-copilot-journey.md)'s data sheet (V18) and never renumbered, each verifying one or more of REQ-1 to REQ-6 (V17), the six rows of [the PRD](expense-copilot-prd.md)'s Functional scope table in that table's own order. This PRD carries no separate user-stories.md or FRD, so REQ ids alone carry the traceability a story id would elsewhere in this repository. AC-1 verifies REQ-1 and REQ-2 together, because one photographed receipt exercises both ingestion and extraction in a single pass; every other criterion verifies exactly one REQ id.

### AC-1 verifies REQ-1 and REQ-2 (happy path)

```
GIVEN a filer with a legible photographed receipt for a business expense
WHEN  the filer uploads the photo to the copilot
THEN  the copilot drafts a line item carrying merchant, date, amount and currency
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, all four fields populated when the receipt is legible
- **Test data needed:** a legible photographed receipt fixture showing merchant, date, amount and currency
- **Automatable:** yes
- **Paired eval reference:** model-driven; see [templates/ai/eval-spec.md](../templates/ai/eval-spec.md), not yet filled for this chain, and D-4's acceptance of an ILLUSTRATIVE threshold there rather than a finance-agreed number

### AC-2 verifies REQ-1 (happy path)

```
GIVEN a filer who forwards a receipt by email instead of photographing it
WHEN  the copilot ingests the forwarded email
THEN  the copilot drafts the same four fields AC-1 drafts from a photo: merchant, date, amount and currency
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, same four fields as AC-1
- **Test data needed:** a forwarded-email receipt fixture carrying an image or PDF attachment
- **Automatable:** yes
- **Paired eval reference:** model-driven, the same extraction path AC-1 uses; see [templates/ai/eval-spec.md](../templates/ai/eval-spec.md), not yet filled for this chain

### AC-3 verifies REQ-2 (negative)

```
GIVEN a receipt where one field, for example the currency, is not legible or not present
WHEN  the copilot extracts fields from the receipt
THEN  that field stays blank and flagged rather than guessed
```

- **Type:** negative
- **Measurable threshold:** binary outcome, no field is populated without source text on the receipt
- **Test data needed:** a receipt fixture with one field illegible or missing
- **Automatable:** yes
- **Paired eval reference:** model-driven; see [templates/ai/eval-spec.md](../templates/ai/eval-spec.md), not yet filled for this chain. This is the PRD's own never-invent rule, which follows [templates/ai/hallucination-controls.md](../templates/ai/hallucination-controls.md) per the PRD's Functional scope row 2, and it is the consequence ADR-0001 (expense-copilot-adr.md, not yet written) records for its receipt-pipeline decision (V9)

### AC-4 verifies REQ-3 (happy path)

```
GIVEN a drafted line item whose merchant matches a policy line in the static category mapping (D-3)
WHEN  the filer opens the draft
THEN  the line shows the suggested category and the policy line it matched
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, a policy line is shown alongside every suggested category
- **Test data needed:** a receipt whose merchant maps to a known policy line in the static mapping
- **Automatable:** yes
- **Paired eval reference:** model-driven; see [templates/ai/eval-spec.md](../templates/ai/eval-spec.md), not yet filled for this chain

### AC-5 verifies REQ-4 (happy path)

```
GIVEN a drafted report with at least one editable field
WHEN  the filer edits that field before pressing submit
THEN  the edit holds in what the filer sees and in what is submitted
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, the edited value is unchanged from edit through submit
- **Test data needed:** a drafted report with at least one editable field
- **Automatable:** yes

### AC-6 verifies REQ-4 (negative, guardrail)

```
GIVEN a drafted report at any stage of completeness
WHEN  no filer has pressed submit
THEN  no report reaches finance
```

- **Type:** negative, guardrail
- **Measurable threshold:** binary outcome, zero reports transmitted to finance without a submit action attributable to the filer
- **Test data needed:** a drafted report left untouched past the point a defect could auto-submit it
- **Automatable:** yes
- **Guardrail note:** this is the load-bearing guardrail the PRD's Out of scope section names, "not a v2 candidate"; see [templates/ai/human-approval-gates.md](../templates/ai/human-approval-gates.md), not yet filled for this chain, which the PRD's Launch criteria requires to confirm no submission path bypasses the filer

### AC-7 verifies REQ-5 (happy path)

```
GIVEN a drafted field the model marked low-confidence
WHEN  the reviewer opens the report
THEN  that field is visually distinct from a high-confidence field in the reviewer's view
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, low-confidence fields are visually distinguishable from other fields
- **Test data needed:** a drafted report carrying at least one low-confidence field and one high-confidence field
- **Automatable:** partially; the confidence flag itself is automatable, the visual-distinction check is manual until a UI test asserts the styling. Owner: Priya Nair

### AC-8 verifies REQ-6 (happy path)

```
GIVEN a category mapping an admin wants to correct
WHEN  the admin corrects the mapping
THEN  the correction is logged with who made it and when
```

- **Type:** happy path
- **Measurable threshold:** binary outcome, a log entry naming the admin and a timestamp exists for the correction
- **Test data needed:** an existing category mapping and an admin account
- **Automatable:** yes
- **Note:** per D-3, the correction is logged but not fed back into future suggestions in v1; AC-8 checks only the logging half of REQ-6

### AC-9 verifies REQ-6 (edge)

```
GIVEN a report the filer already submitted under a mapping's old value
WHEN  an admin later corrects that mapping
THEN  the already-submitted report's category is not silently rewritten
```

- **Type:** edge
- **Measurable threshold:** binary outcome, the submitted report's stored category is unchanged after the correction
- **Test data needed:** one submitted report filed under a mapping, then corrected afterward
- **Automatable:** yes

### AC-10 verifies REQ-1 (edge)

```
GIVEN a single photo that frames more than one receipt
WHEN  the filer uploads it
THEN  the copilot rejects the photo back to the filer with a prompt asking for one receipt per photo
```

- **Type:** edge
- **Measurable threshold:** binary outcome, no draft line item is created from a multi-receipt photo
- **Test data needed:** a photo fixture framing two or more receipts at once
- **Automatable:** yes
- **Note:** per the PRD's Trade-offs accepted table, row 1, and D-2, v1 ships one receipt per item; ADR-0001 (expense-copilot-adr.md, not yet written) later records the architectural half of the same call (V9)

## 2. Edge and negative case coverage

| Story / FR | Edge or negative condition | Expected behavior | Criterion ID or reason not covered |
|---|---|---|---|
| REQ-1 | A single photo frames more than one receipt | Rejected back to the filer with a per-receipt prompt, no draft line item created | AC-10 |
| REQ-1 | A forwarded email carries an attachment that is neither an image nor a PDF | Not specified | Not covered: no criterion for an unsupported attachment format. Open: Maya Chen |
| REQ-2 | One field on an otherwise legible receipt is not present or not legible | Stays blank and flagged, never guessed | AC-3 |
| REQ-2 | A receipt with zero legible fields, the whole receipt rather than one field | Not specified | Not covered: no criterion distinguishes a wholly illegible receipt from a partially legible one. Open: Priya Nair |
| REQ-3 | A merchant the static policy mapping (D-3) does not cover | Not specified | Not covered: no criterion for an unmapped merchant. Open: Maya Chen |
| REQ-4 | The filer edits a drafted field before pressing submit | The edit holds through submit | AC-5 |
| REQ-4 | No submit action from the filer, at any stage of completeness | Nothing reaches finance | AC-6 |
| REQ-5 | A field the model marks low-confidence | Visually distinct in the reviewer's view | AC-7 |
| REQ-5 | A field exactly at the confidence-flagging boundary | Not specified | Not covered: no criterion for the boundary itself. Open: Priya Nair |
| REQ-6 | An admin corrects a category mapping | Logged with who and when | AC-8 |
| REQ-6 | A mapping corrected after a report was already submitted under the old value | The submitted report's category is not silently rewritten | AC-9 |

## 3. Coverage summary

| Story / FR | Happy path ACs | Edge ACs | Negative ACs | Gaps |
|---|---|---|---|---|
| REQ-1 | AC-1, AC-2 | AC-10 | none | No criterion for an unsupported forwarded-email attachment format. Open: Maya Chen |
| REQ-2 | AC-1 (shared with REQ-1) | none | AC-3 | No criterion for a wholly illegible receipt, every field rather than one. Open: Priya Nair |
| REQ-3 | AC-4 | none | none | No criterion for a merchant the static mapping does not cover. Open: Maya Chen |
| REQ-4 | AC-5 | none | AC-6 | none |
| REQ-5 | AC-7 | none | none | No criterion for the confidence-flagging boundary itself. Open: Priya Nair |
| REQ-6 | AC-8 | AC-9 | none | none |

**Must stories with zero negative cases:** REQ-1, REQ-3, REQ-5 and REQ-6. The PRD's Functional scope table carries no should or could split, so all six REQ ids are read as v1's must set. REQ-1 and REQ-6 each carry an edge criterion instead (AC-10, AC-9); REQ-3 and REQ-5 carry only the happy-path criterion listed above, with the gap named and owned in the Gaps column: an unmapped merchant for REQ-3 (open, Maya Chen) and the confidence-flagging boundary for REQ-5 (open, Priya Nair). REQ-2 and REQ-4 each carry a negative case (AC-3, AC-6) and are not on this list.

## How these criteria fail

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Restates the story | An early draft of AC-1 might have read "receipt extraction works," against REQ-1 and REQ-2 | AC-1 names the four fields drafted, merchant, date, amount and currency, and the input channel, a behavior REQ-1 and REQ-2's own titles do not already state |
| Could never fail | "Extraction is accurate" | Rewritten to AC-3's binary rule: an unread field stays blank and flagged, never guessed, checkable against a fixture with a missing field |
| Happy path only | REQ-3 and REQ-5 each still carry one happy-path criterion and nothing else | Flagged by name with an owner in section 3, not left silent |
| Adjectives as thresholds | "Confidence is shown clearly" | AC-7 requires the low-confidence field to be visually distinct from other fields in the reviewer's view; D-4 keeps the model's own accuracy number out of this contract entirely, parked as ILLUSTRATIVE in the eval spec instead of invented here |
| A tester cannot run it | "Handle the multi-receipt case gracefully" | Rewritten to AC-10: the photo is rejected back to the filer with a per-receipt prompt, and no draft line item is created from it |
| Message promises more than the rule enforces | AC-10's rejection prompt could have implied the copilot counted the receipts in frame | AC-10 tests only what the message promises, that the filer is asked to resubmit one receipt per photo, not a claim about how many receipts the copilot detected |

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every must story and must FR has at least one criterion. The PRD's Functional scope table carries no should or could split, so REQ-1 to REQ-6 are read as the whole must set for v1, and each has at least one criterion above.
- [x] Every criterion has one action and one observable outcome. AC-1 to AC-10 are each one GIVEN, one WHEN and one THEN; none is bundled.
- [x] Every threshold is a number, labeled ILLUSTRATIVE where unagreed, or a binary outcome where no number exists. Neither data sheet carries a per-criterion latency or throughput figure for this chain, so every criterion above uses binary outcome rather than inventing one; the PRD's own numeric targets (first-submission approval, filing time) are Gate 5 objective-level metrics, not per-criterion thresholds, and stay in [expense-copilot-prd.md](expense-copilot-prd.md)'s Success metrics table rather than being duplicated here.
- [x] Every story has edge and negative coverage or a written reason. Section 2 carries a row and a criterion id or a named reason for all six REQ ids.
- [x] "Must stories with zero negative cases" says "none" or carries an owner and date. Section 3 names REQ-1, REQ-3, REQ-5 and REQ-6, each with an owner.
- [x] Model-driven criteria are paired with an eval spec reference. AC-1, AC-2, AC-3 and AC-4 turn on model output; each is paired above with [templates/ai/eval-spec.md](../templates/ai/eval-spec.md), not yet filled for this chain, and D-4's own acceptance of an ILLUSTRATIVE threshold there rather than a finance-agreed number.

Signed at Gate 2, 2026-08-28: Maya Chen as product owner, Priya Nair as engineering lead, and Daniel Okafor as business sponsor, approved together with the vision, the product strategy, the roadmap and the PRD (V8). This contract closes at Gate 2 and is one of the nine links the development handoff (expense-copilot-development-handoff.md, not yet written) carries when DESIGN closes at Gate 3.
