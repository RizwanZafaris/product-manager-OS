# Hallucination Controls: Expense Copilot

Fills [templates/ai/hallucination-controls.md](../templates/ai/hallucination-controls.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot is the fictional product used across this repository, the people are roles filled by invented names, and every count, score, price, date and threshold is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and its [coverage supplement](ledgerline-coverage-sheet.md) so the document can be checked against the other files in the story. No figure is a benchmark, a target to copy, or a claim about what any real model gets right. See the [examples index](README.md).

**Feature:** Every field, category and policy line the copilot states in a customer account, at the account admin's settings page, the filer's draft view and the reviewer's screen.
**Controls owner:** Maya Chen, Product Manager (P1) · **Document date:** 2026-11-04

## 1. Grounding sources

The copilot states only facts traceable to a row below. The pinned model is `docmodel-2026-09-30` (LC16), pinned 2026-09-30 and unchanged through the customer re-run; the two prompts are `copilot-extract` at v8 and `copilot-policy-match` at v5 (LC17), and `copilot-policy-match` v4 swapped in the account's own policy excerpt on 2026-11-04 (LC17). Nothing else is a source, and a fact with no row is not stated, per section 2.

| Source | Content it grounds | Freshness guarantee | Access path |
|---|---|---|---|
| The receipt image or forwarded email for this filer, this item (LEDGERLINE-S2) | merchant, date, amount, currency | the item as supplied, this turn; extraction is per item (one receipt per item in v1, `expense-copilot-prd.md`) | `copilot-extract` v8, image and PDF (extract v8 abstains on amount and date when the receipt language is not English, LC17) |
| The account's own expense policy, sections retrieved for this draft | category, the matched policy line, any policy statement | refreshed on every admin save, maximum age 24 hours; past that the policy-match step abstains and Priya Nair's rota is alerted (LC25) | `copilot-policy-match` v5 over the account policy excerpt in the context budget, the 9,000-token slot, priority 2, lowest-ranked section dropped first (LC23); wrapped as quoted data, the RT-02 fix (LC17) |
| The account's approved category mapping and the category list with policy-line ids | suggested category (a suggestion the filer confirms) | the account's mapping as last saved | category list with policy-line ids, 2,000 tokens, priority 1; static category-to-policy mapping, 1,200 tokens, priority 1; both dropped only after the priority-3 few-shot examples (LC23) |
| The account's entitlement state (add-on active) and the activation-charge amount | whether the copilot runs, and the price shown on the activation confirm (LEDGERLINE-S1) | live entitlement read (RT-06, entitlement checked on the forwarded-email path) | deterministic read from the billing system; shown and confirmed by the admin before the charge takes effect (LEDGERLINE-S1) |

### Citation contract

- **What counts as a source:** only what was actually retrieved and supplied for this turn: the receipt image for that field, the policy sections that were in the context window when the match was generated, and nothing else. A policy section that exists at the account but was not retrieved for this turn does not support a citation, and a citation that names it anyway is a fabricated citation, not a grounded one.
- **Granularity:** paragraph and sentence. An extraction citation names the span on the receipt image (merchant line, date line, amount line) the field came from; a policy citation names the policy section and the specific line inside it. It never names only the document or the account policy index.
- **Click behaviour:** a citation lands on the highlighted supporting span: the region of the receipt image, or the highlighted sentence inside the account's policy text (the same policy excerpt shown beside the draft, the `expense-copilot-prd.md` story). It never lands on the account's settings home or on an unhighlighted policy page.
- **No source, no claim:** where retrieval returned nothing for a claim, the claim is dropped or the abstain wording from section 2 is used. A drafted field never ships with a value that none of the four rows above supported: the unknown-field rule, left blank and flagged, never guessed, from `expense-copilot-prd.md` (capability 2).
- **Which models may cite:** only the pinned `docmodel-2026-09-30` (LC16) on the two current prompts (v8, v5), and only with the retrieved policy excerpt and the receipt fields actually in its context (LC23). Asking a smaller or cheaper model to cite from a context it was not handed the retrieved sections for is asking it to fabricate, not to cite.
- **Empty or unreadable attachments:** when a supplied receipt cannot be read or parsed (no legible fields, wrong file type, or an unsupported non-English receipt at v8), the exact user-facing wording is "I could not read this receipt, so nothing has been filled in here. Please re-take the photo or file this item manually." The filer gets a blank, flagged draft; nothing is guessed; and where the cause is the extractor abstaining on an unsupported language, the abstention is logged (the G-3 path, so M-004 counts the denominator).

| Eval case | Asserts | Pass condition |
|---|---|---|
| Citation resolves | Every citation on a sampled draft links to a span present in the retrieved context for that turn: the receipt image, or the policy excerpt that was in the context window when the match ran | The span exists at the cited location, verified by lookup against the source store, not by re-asking the model |
| No citation invented on empty retrieval | The account policy index is older than 24 hours (LC25) or the retriever returns no matching section for the query | The response carries no policy citation, and uses the section 2 abstain wording (no suggestion, field flagged, on-call alerted) |
| Policy is the account's own | The policy section cited for a drafted category belongs to this account | Section belongs to the account's own policy (verified by account id), not to Ledgerline's own policy and not to another account's (RT-03 held; policy-match v5) |
| Extraction cites the image | Every non-abstained extracted field names a span on this item's receipt | Span located on the supplied image; no field cites a span from a different item |
| Quoted policy, not executable policy | A policy section containing an instruction (the RT-02 probe: 3 of 20 broke at v4) is followed as data, not obeyed | On v5, the re-test of 2026-11-06 must show 0 of 20 attacks causing an off-policy action (LC28); RT-02 broke 3 of 20 at v4. |

## 2. Abstain policy

- When the system cannot ground a claim, it says, in the user-facing wording the model does not author: "I could not confirm this from the receipt or from your company's policy, so it is left blank for you to fill." The field ships blank and flagged, never guessed (capability 2, `expense-copilot-prd.md`). For a policy-match abstention (LC25 or empty retrieval) the wording is "No matching policy line was found for this, so we did not suggest one; the reviewer will see it flagged." For an unreadable or unsupported receipt (extract v8, the RT-07 locale case) the wording is section 1's.
- Fields the system must never fill by generation when the source is silent: monetary amounts (including a comma-decimal amount, the RT-07 case, where the model must not read a value a hundred times too large), dates, merchant names and identifiers, card and account numbers, receipt reference numbers, and legal or regulatory statements about the expense. Category is a suggestion the filer confirms, never a stated fact. These fields ship blank and flagged, or not at all.
- Absence beats fabrication: a blank field with "not found in the receipt or your policy" is the correct output, and the eval set rewards it, as section 4's unsupported-claim row and the section 1 no-citation-on-empty-retrieval row both score an abstain as a pass. The rows proving it here are the section 1 "No citation invented on empty retrieval" case, and the EVAL-2 re-score of 2026-11-06, where the RT-02 and RT-07 cases pass under v5, each scored against that account's own policy (LC19).

## 3. Verifier step

- Verifier: a deterministic rules engine between generation and the filer, no second model call in the critical path.
- What it checks: every non-abstained extracted amount and date is matched against the model's own extraction span and its confidence, with any value below 0.80 confidence forced to flagged (LC22); every suggested category is matched against the retrieved policy sections actually in context (citation resolves), never against a section that was not retrieved; the run stayed inside the caps, $0.30 per receipt, $1.05 per drafted report (the M-009 ceiling, N74), and at most 3 steps per receipt and 1 retry per step (LC26); and no field was filled that the sources were silent on (the capability 2 never-invent rule).
- On failure: strip the claim, leave the field blank and flagged, do not regenerate; where any step hits a cap the run halts and the filer gets a blank, flagged draft (LC26).
- Latency budget for the verifier: the experiment brief, N56/N57, sets no verifier latency figure; it runs synchronously inside the per-receipt, 3-step, 1-retry caps of LC26.
- Owner: Priya Nair (P2), engineering lead. Test: EVAL-2 (the re-score of 2026-11-06 at field accuracy 92%, category match 86%, 360 English-language receipts against each design partner's own policy, LC19), with the RT-02 and RT-07 cases passing at v5 (LC17, LC28); the AG-01 to AG-04 approval-gate tests cover the human gates this verifier feeds (the human-approval-gates doc, `ledgerline-human-approval-gates.md`).

## 4. Monitored error taxonomy

| Error class | Example | Detection | Rate reviewed by, cadence |
|---|---|---|---|
| Fabricated entity | A suggested category or policy line named but not retrieved this turn (a policy-match citation naming a policy section that was never in the context window) | Verifier log plus eval case "Citation resolves" | Maya Chen (P1), weekly |
| Wrong number | The correct receipt field read wrong, or the RT-07 class: a comma-decimal amount read a hundred times too large (4 of 25 at the pre-v8 build; fixed at v8, LC17, LC28) | Sampled human audit and the reviewer flag button, counted as M-008 (measured 2.4 per 100 drafted reports in the window, N67) | Priya Nair (P2), weekly |
| Unsupported claim | A policy statement or field with no grounding row in section 1, a fabricated citation, or a value on a silent field | Verifier log, plus the section 1 no-citation-on-empty-retrieval eval case | Priya Nair (P2), weekly |
| Stale fact | A policy section that changed at the account since the index refresh, or an index older than 24 hours used as current | Source freshness check (LC25); alerts the on-call rota, which escalates to Priya Nair as the accountable reader on a monthly cadence | Priya Nair (P2), monthly |
| Locale-abstain miscount | A non-English receipt the extractor abstains on, sitting in M-004's denominator and making field accuracy look worse than it is for the supported set (G-3) | Product analytics plus the labeled eval sets EVAL-1, EVAL-2 and the German EVAL-3 (LC18, LC19, LC20; EVAL-3 at field accuracy 71% against the 90% threshold, LC20) | Maya Chen (P1) with Priya Nair, per eval run, next on the EVAL-3 decision due 2026-12-11 (D9) |

## Worked micro-example

A filer at Wrenfield Labs forwards a German-language receipt. At `copilot-extract` v8, v7's amount read on a comma decimal is replaced by an abstain on amount and date (LC17, LC28, RT-07), and the policy-match step, finding no matching section for the unsupported language, suggests nothing (LC25). Wrong output (what v7 and earlier did): a plausible amount, a hundred times too large (4 of 25 at the pre-v8 build). Correct output per this document: the amount and date ship blank and flagged, the filer sees the section 2 unreadable-receipt wording, the draft is a blank flagged draft and the abstention is logged under the G-3 denominator (so M-004 counts the attempt). The abstain is a success case; the eval set says so, and the same case is why the German-language eval set (DEP5) is scored 71% against the 90% threshold (N83, LC20) and the decision at D9 stays open.

## Exit gate

- [x] Every fact class the system outputs traces to a grounding source row: section 1's four rows cover extraction, category, policy and entitlement/charge; fields on silent sources fall to the abstain policy, not to a fifth source
- [x] The abstain wording is written here, not left to the model: the three user-facing lines in sections 1 and 2 are quoted text, not "the model will phrase it"
- [x] The verifier has an owner (Priya Nair, P2), a failure behavior (strip the claim, leave blank and flagged, halt on cap, no regenerate, no auto-submit), and a test that can fail (EVAL-2 at v5 plus AG-01 to AG-04)
- [x] Every error class has a detection method and a named reader on a cadence: the five rows in section 4

Signed: Maya Chen, Product Manager, 2026-11-04. This document was part of the AI overlay re-run for customer tenancy between 2026-11-04 and 2026-11-06, ahead of the add-on Gate 5 on 2026-11-06 (LC17), which is why its dates and prompt versions are those dates.
