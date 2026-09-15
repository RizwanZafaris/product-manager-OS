# API Contract: Expense Copilot API v1

Fills [templates/architecture/api-contract.md](../templates/architecture/api-contract.md). Everything here is invented: Ledgerline is the fictional mid-market software company of [ledgerline-journey.md](ledgerline-journey.md) and [expense-copilot-journey.md](expense-copilot-journey.md), the Expense Copilot is its fictional internal expense tool, every person named below is fictional, and every number, date and identifier is ILLUSTRATIVE, carried from those two data sheets rather than from any real receipt-processing API. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md)
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [architect agent](../agents/architect-agent.md)

**API:** Expense Copilot API v1 · **Contract owner:** Priya Nair, Engineering Lead · **First consumer:** the Expense Copilot filer client (photo upload and forwarded-email intake, REQ-1)
**Status:** Approved at Gate 3, 2026-09-11, with several limits left open (see section 5) · **Date:** 2026-09-05
**Style:** REST · **Spec file:** `services/expense-copilot/openapi/expense-copilot-api-v1.yaml`

This contract carries the six resources [expense-copilot-journey.md](expense-copilot-journey.md) names (V11), each tied to the REQ id it serves: ingestion and extraction status feed the drafting flow (REQ-1, REQ-2), the draft, edit and submit calls carry REQ-4's assembly and edit surface with AC-6's guardrail that nothing reaches finance before the filer presses submit, and the category-mapping correction call carries REQ-6's admin loop with AC-8's log and AC-9's guarantee that a correction never rewrites a submitted report. It exists because of what [expense-copilot-adr.md](expense-copilot-adr.md) (ADR-0001) decided: every extraction call answers for one receipt, matched to one uploaded photo or one forwarded-email attachment, so Ingest a receipt never accepts a batch. Entity shapes below follow [expense-copilot-data-model.md](expense-copilot-data-model.md).

## 1. Endpoints

| Operation | Method and path (or event name) | Purpose | Idempotent? How? | Auth scope required |
|---|---|---|---|---|
| Ingest a receipt | `POST /receipts` | Accept one uploaded photo or one forwarded-email attachment for extraction, never a batch, per ADR-0001 (REQ-1) | Yes: an `Idempotency-Key` header is required; the dedupe window is not sized on either data sheet [OPEN] | `receipts:write` |
| Get receipt | `GET /receipts/{id}` | Read a receipt's extraction status and drafted fields (REQ-2) | N/A, read-only | `receipts:read` |
| Assemble draft report | `POST /reports/{id}/draft` | Assemble the filer's receipts into an editable draft report (REQ-4) | Yes: a repeat call for a report id that already has a draft returns the existing draft rather than assembling a second one | `reports:write` |
| Edit a line item | `PATCH /reports/{id}/line-items/{id}` | The filer edits a drafted field before submit (REQ-4, AC-5) | Yes: PATCH sets the named field to the given value; a repeated identical edit yields the same state | `reports:write` |
| Submit report | `POST /reports/{id}/submit` | Close the report; the only action that sends it to finance (REQ-4, AC-6) | Yes: a repeat call on a report already in submitted status returns the existing submitted state rather than submitting again | `reports:submit` |
| Correct a category mapping | `PATCH /category-mappings/{id}` | An admin corrects a category mapping; the correction is logged with who and when, and does not rewrite an already-submitted report (REQ-6, AC-8, AC-9) | Yes: the mapping's resulting state is idempotent under a repeated identical correction; each call is still written as its own CorrectionLogEntry, per AC-8 | `category-mappings:admin` |

`reports:submit` is never issued alongside `receipts:write` or `category-mappings:admin`. AC-6 ties the submit action to the filer's own review, and a credential scoped for ingestion or for the admin correction loop is not the filer's review. A call to Submit report carrying the wrong scope is rejected (section 4).

## 2. Schemas

Full shapes live in the spec file above; a reviewer needs these fields. Entity names follow [expense-copilot-data-model.md](expense-copilot-data-model.md) section 2.

**`POST /receipts`**
Request: `source_channel` (enum `photo_upload`, `forwarded_email`, required, REQ-1), `content` (the photo or the forwarded-email attachment itself, required).
Response: `id` (string, the Receipt's receipt_id), `source_channel` (enum as above), `extraction_status` (enum `pending`, `drafted`, `rejected_multiple_receipts`; the last is AC-10's per-receipt prompt case, one receipt per photo in this v1 scope).

**`GET /receipts/{id}`**
Response: same shape as the Ingest response above, reflecting current extraction status (REQ-2, AC-1, AC-2).

**`POST /reports/{id}/draft`**
Request: no body beyond the path id; the report is assembled from the filer's own receipts.
Response: `id` (the DraftReport's report_id), `status` (enum `draft`, `submitted`), `line_items` (array; each carries `merchant`, `date`, `amount`, `currency`, blank and flagged rather than guessed when the model could not read a field, per AC-3; `confidence`, enum `high`, `low`, shown distinct in the reviewer's view per REQ-5 and AC-7; `suggested_mapping`, a reference to a CategoryMapping and its matched policy line, per REQ-3 and AC-4).

**`PATCH /reports/{id}/line-items/{id}`**
Request: the one field the filer is changing, by name (REQ-4, AC-5).
Response: the updated line item, in the same shape `POST /reports/{id}/draft` returns.

**`POST /reports/{id}/submit`**
Request: no body beyond the path id.
Response: `id`, `status` (`submitted`, unchanged if already submitted, AC-6, AC-9).

**`PATCH /category-mappings/{id}`**
Request: the corrected `policy_line_reference` (REQ-6).
Response: `id` (the CategoryMapping's mapping_id), `policy_line_reference`, `version` (increments on each logged correction, REQ-6), plus the CorrectionLogEntry this call writes: `corrected_by`, `corrected_at` (AC-8).

## 3. Authentication and authorization

- Mechanism: OAuth 2.0 client credentials for the filer client and for the finance admin's correction tooling. Neither credential's own lifetime or format is set on either data sheet, so the choice stops at the mechanism rather than being invented further.
- Token or key lifetime and rotation: not set on either data sheet [OPEN: owner Priya Nair, before BUILD].
- Authorization model: `receipts:write` and `receipts:read` are issued to the filer client. `reports:write` is issued to the filer client. `reports:submit` is issued to the filer client only, never to admin tooling, per AC-6. `category-mappings:admin` is issued to finance admin tooling only, per REQ-6's admin correction loop, never to the filer client.

## 4. Errors

| Condition | Status or code | Error body shape | Consumer's correct reaction | Retryable? |
|---|---|---|---|---|
| A photo carries more than one receipt in frame | 422 Unprocessable Content | `{code: "multiple_receipts_detected"}` | Show the per-receipt prompt from AC-10; the filer re-photographs one receipt at a time, per the one-receipt-per-item v1 scope (ADR-0001) | Yes, after re-photographing one receipt |
| `Idempotency-Key` reused with a different request body | 409 Conflict | `{code: "idempotency_conflict", original_receipt_id}` | Do not resend with the same key; read the original receipt by the id returned | No |
| `Idempotency-Key` header missing on Ingest a receipt | 400 Bad Request | `{code: "missing_idempotency_key"}` | Add the header and resend as a new request | No, until the header is added |
| `PATCH /reports/{id}/line-items/{id}` called on a report already in submitted status | 409 Conflict | `{code: "report_already_submitted"}` | No action; the report is closed, per AC-6 | No |
| `PATCH /category-mappings/{id}` for a mapping already suggested on a submitted report's line item | 200 OK | `{id, policy_line_reference, version}` | Not an error: the mapping updates for future drafts only; the already-submitted report's line item is not rewritten, per AC-9 | N/A |
| Credential's scope does not cover the operation called | 403 Forbidden | `{code: "insufficient_scope"}` | Call with the credential scoped for this operation, per section 3 | No |
| Unknown receipt, report, line item, or category-mapping id | 404 Not Found | `{code: "not_found"}` | Verify the id; do not resend the same id expecting a different result | No |
| Request fails schema validation | 400 Bad Request | `{code: "invalid_request", field}` | Fix the named field; do not resend unchanged | No |
| Unauthenticated or expired credential | 401 Unauthorized | `{code: "unauthenticated"}` | Refresh the credential once, then retry | Yes, after refreshing |
| Unexpected failure inside the service | 500 Internal Server Error | `{code: "internal_error"}` | Retry once with backoff; escalate if it persists | Yes, once |

The 422 row is the one this contract exists to get right: ADR-0001 accepts one receipt per call precisely so a field the model cannot read stays blank and flagged rather than guessed (AC-3), and a photo carrying more than one receipt is the case that rule cannot silently absorb, so it is rejected rather than drafted from a guess at which receipt was meant.

## 5. Limits and versioning

- Rate limit per consumer: not sized on either data sheet [OPEN: owner Priya Nair, before BUILD]. Behavior at the limit: 429 Too Many Requests, `Retry-After` header.
- Payload size limit: not sized on either data sheet [OPEN: a photographed receipt needs a defensive ceiling before launch; owner Priya Nair].
- Versioning scheme: URL version (`/v1/`, as the header's API name states), additive-only within a version.
- Breaking change policy: not sized on either data sheet [OPEN: notice period and approver not yet named].
- Deprecation contract: not sized on either data sheet [OPEN].

## Exit gate

- [x] Every operation states its idempotency behavior: section 1, each row; the `Idempotency-Key` window on Ingest a receipt is named open rather than invented
- [x] Every error row tells the consumer what to do, and whether to retry: section 4
- [ ] Auth mechanism, scopes, and rotation are stated: mechanism and scopes are stated in section 3; rotation is named open rather than invented
- [ ] Rate limits and at-limit behavior are stated with numbers: the at-limit behavior is stated; the numbers themselves are named open rather than invented, because neither data sheet sizes them
- [x] Versioning and breaking-change policy are stated: versioning is stated; the breaking-change notice period is open, named in section 5
- [x] The machine-readable spec file exists at the path named in the header: `services/expense-copilot/openapi/expense-copilot-api-v1.yaml`, in the copilot's own service repository, not this documentation repository
- [x] The worked micro-example has been deleted

Approved at Gate 3, 2026-09-11 (document dated 2026-09-05), with the rate-limit, payload-size, rotation and breaking-change items above left open by design rather than invented: Maya Chen, Product Owner, and Priya Nair, Engineering Lead. Full journey: [expense-copilot-journey.md](expense-copilot-journey.md); shared figures: [ledgerline-journey.md](ledgerline-journey.md).
