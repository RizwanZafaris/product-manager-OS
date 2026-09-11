# Context Management: Ledgerline Expense Copilot Policy Match

Fills [templates/ai/context-management.md](../templates/ai/context-management.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, and every count, token budget, date and policy rule are fiction carried from the [Ledgerline journey data sheet](ledgerline-journey.md) and the [Ledgerline coverage sheet](ledgerline-coverage-sheet.md).

**Feature:** Policy-match context for Ledgerline's customer Expense Copilot drafts · **Context owner:** Priya Nair · **Document date:** 2026-11-04
**Model context window:** 32,000 tokens · **Working budget (leave headroom for output):** 24,000 tokens

## 1. Context sources

| Source | What it contributes | Freshness (live / cached, max age) | PII class (none / personal / sensitive) | Filter applied before inclusion |
|---|---|---|---|---|
| System prompt, `copilot-policy-match` v4 | Role, rails, output contract, instruction to treat customer policy text as quoted data, and abstention behavior | Versioned, pinned in the prompt change log | none | n/a |
| Receipt's extracted fields | Merchant, date, amount, currency and other extracted fields passed from the extraction step | Live for the current receipt | personal | Context sanitizer masks filer and guest names, card digits, home addresses on hotel folios and phone numbers before assembly |
| Category list with policy-line ids | Candidate categories and the ids used to connect a suggestion to the account's policy | Live for the current account and request | none | Static schema validation; no free-text instructions are accepted as category ids |
| Static category-to-policy mapping | The v1 mapping used to connect categories to policy lines; admin corrections are logged and versioned but are not fed back in v1 | Versioned, current mapping | none | Deterministic id validation; policy text cannot change the mapping during the call |
| Account policy excerpt, top-ranked sections | The account's own policy language needed to match the receipt and explain the suggested category | Cached policy index, maximum age 24 hours; refreshed on every admin save | sensitive | Retrieved sections are sanitized, then wrapped as quoted data so policy instructions cannot become model instructions. RT-02 and CTX-05 cover this boundary |
| Four few-shot examples | Four synthetic or sanitized examples showing the expected policy-match output shape | Versioned with the prompt | personal | Sanitized examples only; names, account identifiers and other masked classes are removed |
| Filer's free-text note | Additional context supplied with the receipt, when present | Live for the current receipt | personal | Truncation and the same PII sanitizer as the extracted fields; it cannot override the system prompt or quoted policy data |

The account policy excerpt is retrieved rather than placed in full. Tessellate Consulting's largest design-partner policy is 38 pages and about 21,000 tokens, so including the complete document would consume most of the 32,000-token window before the receipt and policy-match instructions arrive (LC24, [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)).

Customer prompt handling follows D5: prompt records are retained for 30 days and the vendor's terms include the existing no-training clause. The policy text is treated as data under RT-02, not as an instruction source (D5, LC28, [ledgerline-journey.md](ledgerline-journey.md), [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)).

## 2. Token budget and priority order

The slot budget is the LC23 target. The arithmetic is:

`1,500 + 300 + 2,000 + 1,200 + 9,000 + 2,400 + 200 = 16,600 tokens`

The working headroom is:

`24,000 - 16,600 = 7,400 tokens`

| Slot | Budget (tokens) | Priority (1 = never dropped) | Drop behavior when over budget |
|---|---:|---:|---|
| System prompt | 1,500 | 1 | Never dropped. If it alone exceeds the working budget, that is a build failure |
| Receipt's extracted fields | 300 | 1 | Never dropped. Missing or invalid fields remain blank and flagged rather than being guessed |
| Category list with policy-line ids | 2,000 | 1 | Never dropped. If the call cannot fit this slot, the call does not proceed |
| Static category-to-policy mapping | 1,200 | 1 | Never dropped. It is the v1 deterministic mapping and is not replaced by model output |
| Account policy excerpt, top-ranked sections | 9,000 | 2 | Lowest-ranked retrieved policy section is dropped first. The policy excerpt drops before the category list or static mapping ever does. If the required policy evidence is no longer present, the policy-match step abstains and flags the field |
| Four few-shot examples | 2,400 | 3 | Cut from four examples to two, then to none |
| Filer's free-text note | 200 | 3 | Truncated first within this slot, then omitted if the budget is still tight |

The explicit drop order is:

1. Drop the lowest-ranked policy section.
2. Reduce four few-shot examples to two.
3. Remove the remaining few-shot examples.
4. Truncate or remove the filer's free-text note.
5. Do not drop the system prompt, extracted fields, category list or static mapping. If the required policy evidence cannot fit, abstain rather than silently match against less context.

The policy excerpt is priority 2 deliberately. A wrong category match caused by missing customer policy text is worse than a shorter response with no free-text note or few-shot example. The static mapping remains priority 1 because v1 uses the PRD's static mapping and does not learn from an unreviewed correction loop ([expense-copilot-prd.md](expense-copilot-prd.md)).

## 3. Staleness policy

- Max acceptable age per cached source: account policy index, 24 hours. The system prompt, static mapping and few-shot examples are versioned rather than governed by a live age window. Receipt fields, category list and filer note are live for the current request.
- What happens when a source exceeds its age: refresh the account policy index synchronously. If it remains older than 24 hours, the policy-match step abstains, produces no suggestion, and flags the field for review.
- Who is alerted when a refresh pipeline fails: Priya Nair's on-call rota.

The policy index refreshes on every account-admin save. The 24-hour maximum is the backstop for a failed or delayed refresh, not permission to use stale policy silently (LC25, [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)).

## 4. PII filter

- What is stripped or masked before the model sees it: filer and guest names, card digits, home addresses on hotel folios, and phone numbers. The account's own policy text is not treated as an instruction. It is passed only as quoted data after sanitization and boundary wrapping. These classes are tested by CTX-01 to CTX-05.
- Where the filter runs (before the context is assembled, not after): the context sanitizer, between source retrieval and context assembly. No post-assembly filter is treated as a substitute for this step.
- Test: CTX-01 covers filer and guest names; CTX-02 covers card digits; CTX-03 covers home addresses on hotel folios; CTX-04 covers phone numbers; CTX-05 covers the account's own policy text sent as quoted data. RT-02 separately tests an instruction planted in a customer's policy document. The red-team result initially broke on RT-02, followed on 3 of 20 attempts, and the fixed boundary was held on re-test by Nadia Rahimi on 2026-11-06 (LC28, [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md)).
- What is logged about context contents, and how the log avoids re-collecting the PII the filter removed: log the prompt version, source types, retrieval status, staleness decision, slot budgets, drop decisions, abstention reason and test or request identifier. Do not log raw receipt text, raw policy text, masked values, card digits, addresses, phone numbers, names or the assembled prompt. D5's 30-day prompt retention applies to approved prompt records, and the no-training clause prevents the vendor from using them to train its model.
- For regulated products, residency and vendor-terms questions about this data belong to the overlay in [../modules/regulated/README.md](../modules/regulated/README.md)

## Worked micro-example

A Ledgerline policy-match call has a 32,000-token window and a 24,000-token working budget ILLUSTRATIVE. Its planned slots total 16,600 tokens:

`1,500 + 300 + 2,000 + 1,200 + 9,000 + 2,400 + 200 = 16,600`

Tessellate Consulting's policy is 38 pages and about 21,000 tokens ILLUSTRATIVE, so retrieval supplies only the top-ranked sections in the 9,000-token policy slot. If the call is tight, the lowest-ranked policy section is removed first. The category list and the static category-to-policy mapping remain in the call. Four few-shot examples then become two, then none, and the filer's note is truncated or removed. The policy excerpt drops before either the category list or the static mapping, because a policy-match call without the required policy evidence must abstain rather than invent a match.

## Exit gate

- [x] Every context source has a row with freshness, PII class, and filter stated. The source table covers the system prompt, extracted fields, category list, static mapping, policy excerpt, few-shot examples and filer note.
- [x] The budget table covers everything in section 1 and fits the working budget. The slots total 16,600 tokens, and `24,000 - 16,600 = 7,400` tokens remain as headroom.
- [x] Drop order is explicit; nothing relies on framework defaults. The policy excerpt drops first among substantive retrieval content, followed by few-shot examples and the filer note. Priority 1 sources are never dropped.
- [x] The PII filter has tests per class and runs before assembly. CTX-01 to CTX-05 cover the masked classes and the quoted policy-data boundary.
- [x] Staleness has a behavior and an alerted owner, not just a number. A policy index older than 24 hours causes abstention and alerts Priya Nair's on-call rota.

Signed at Gate 3, 2026-11-04: Priya Nair, engineering lead.
