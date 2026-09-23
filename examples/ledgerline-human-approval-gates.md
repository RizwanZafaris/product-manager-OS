# Human Approval Gates: Ledgerline Expense Copilot Add-on

Fills [templates/ai/human-approval-gates.md](../templates/ai/human-approval-gates.md). Everything here is invented: Ledgerline is a fictional software company, the Expense Copilot add-on is fictional, and every person, date, threshold and identifier is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md). See the [examples index](README.md).

**Gates owner:** Maya Chen · **Document date:** 2026-11-04

## 1. Gate table

| # | Trigger condition (specific, testable) | Action held | Approver role (role, not person; person on rota) | Channel and SLA | On timeout | Test (positive, plus the NAC IDs from section 6 that apply) |
|---|---|---|---|---|---|---|
| 1 | A draft is ready for submission, or an auto-submit request is received | Submission of the expense report | Filer for the account | Filer review surface; no automatic approval | deny and notify the filer; the report remains unsubmitted | AG-01 · NAC-1 to NAC-6 |
| 2 | Any extracted field or suggested category has model confidence under 0.80 | Release of the flagged field or category into the reviewable draft | Finance reviewer for the account | Reviewer queue; reviewer response is required before the flagged field is confirmed | deny and notify the filer and reviewer; the field remains flagged | AG-02 · NAC-1 to NAC-6 |
| 3 | A finance admin proposes a category mapping correction | Acceptance of the proposed correction into the audit log; v1 does not feed the correction back into the model or mapping behavior | Finance admin for the account | Finance-admin correction queue; correction decision is required before the correction is recorded | deny and notify the finance admin; the correction is not recorded | AG-03 · NAC-1 to NAC-6 |
| 4 | An account admin has selected activation for the add-on and a charge is ready to be presented | Add-on activation and creation of the charge | Account admin for the account | Expenses settings activation surface; charge must be confirmed before activation | deny and notify the account admin; the add-on remains inactive | AG-04 · NAC-1 to NAC-6 |

Gate 1 is the filer control described by the PRD's out-of-scope line: auto-submission is not in scope, and the filer submits, always. Gate 2 implements [LEDGERLINE-S3](ledgerline-journey.md), using the assumption that a field or suggested category under 0.80 model confidence is flagged (LC22). Gate 3 records the finance-admin correction, but the correction is never fed back into the drafting model or mapping behavior in v1. Gate 4 implements [LEDGERLINE-S1](ledgerline-journey.md): the account admin sees and confirms the charge before activation.

## 2. Audit log requirement

Every gate decision writes a record with, at minimum:

- Request ID, approval ID, action revision, timestamp, and the triggering condition matched
- The held action's full parameters as presented to the approver, including the report, flagged field, proposed mapping correction, or charge details as applicable
- Approver identity, the authority scope applied, decision, decision time, and free-text reason if denied
- Every state change of the approval record in section 4: approved, consumed, expired, revoked or superseded, with who or what caused it
- For each submission attempt: the attempt ID, the execution token presented, the outcome, and, where the outcome was unknown, the reconciliation query against the expense backend and its result
- Model version and prompt version that produced the request, where a model or prompt produced it: model pin `docmodel-2026-09-30`; prompt ids `copilot-extract` and `copilot-policy-match`, with their applicable versions from LC17
- Retention period for these records: 7 years, the finance-records rule; this is an assumption and the legal lead is to confirm it for customer accounts (LC27)
- Where the log lives and who can read it: the approval-gate audit store, readable by the gates owner, the relevant finance and billing administrators, the legal lead, and authorised reviewers on the account

The log records denials as well as approvals. A timeout is recorded as a denial, with the timeout reason and notification outcome. A finance-admin mapping correction is retained as an audit event even though it is not fed back into v1.

## 3. Exceptions and fail-open register

There are no fail-open exceptions. Every gate denies on timeout. No operational reason, risk owner, or compensating control has been approved for a fail-open path.

| Gate # | Why it fails open | Compensating control | Risk owner | Review date |
|---|---|---|---|---|
| None | None. No gate fails open. | Not applicable. Every timeout denies and notifies. | Not applicable | Not applicable |

## 4. Approval record

Every held action writes one approval record into the approval-gate audit store, alongside the decision log in section 2. The instance below is the AG-01 submission gate; AG-02 to AG-04 write the same seven fields with their own actions. Every identifier and time here is ILLUSTRATIVE.

| Field | Value in this product |
|---|---|
| Approval ID | `AG-01-2026-11-04-0031`, issued when the filer is asked to submit |
| Action revision | SHA-256 over the report's line items, totals, category assignments and the account it files against; the value the filer saw, not a summary of it |
| Approver identity and authority scope | The filer for the account, acting for that account only; a filer cannot approve another account's submission, and no reviewer role inherits the submit right |
| Issued at / Expires at | 2026-11-04T09:12+00:00 / 2026-11-04T09:42+00:00, a 30 minute window |
| State | approved; the record moves to consumed on the submission attempt, or to expired, revoked or superseded under section 5 |
| Single-use execution token | `sub-AG-01-0031-a`, valid for exactly one submission call and used as the idempotency key against the expense backend |
| Execution record | Attempt `sub-0031-1`, outcome `done`, reconciliation not required; an outcome of `unknown` holds the record open until the reconciliation query in R6 has returned |

## 5. Invalidation, replay and reconciliation rules

1. **R1 binding.** Editing any line item, total or category after the filer approved supersedes the approval, and the draft returns to the filer for a fresh yes on the new revision.
2. **R2 authority.** The executor checks at submission time that the approver is still the account's filer, so an approval given before an account transfer does not submit after it.
3. **R3 expiry.** A submission approval older than its 30 minute window is expired and never submits; the draft returns to the filer.
4. **R4 revocation.** The filer, or the finance reviewer for the account, can revoke the approval at any point before the submission runs, and a revoked approval never submits.
5. **R5 one-use.** One submission per approval: a second call presenting `sub-AG-01-0031-a` is refused as a replay and is not retried under another token.
6. **R6 uncertain outcome.** If the submission call times out or returns no acknowledgement, the executor queries the expense backend by the idempotency key and records whether the report landed, and only then may a retry be issued; a retry without that query is refused.

## 6. Negative acceptance criteria

AG-01 to AG-04 test that each gate holds its action. The six below test that the approval stops being usable, which is the half a happy-path suite never reaches.

| ID | Rule | Given | When | Then (must fail) |
|---|---|---|---|---|
| NAC-1 | R1 | An approved submission, one line item edited afterwards | Submission attempted | Refused: superseded; the filer is asked again |
| NAC-2 | R2 | The approver is no longer the account's filer | Submission attempted | Refused: out of authority scope |
| NAC-3 | R3 | An approval issued 09:12, submission at 09:44 | Submission attempted | Refused: expired; draft returns to the filer |
| NAC-4 | R4 | The finance reviewer revoked the approval at 09:20 | Submission attempted at 09:21 | Refused: revoked |
| NAC-5 | R5 | Token `sub-AG-01-0031-a` already consumed | Second submission attempted | Refused: replay, no second report filed |
| NAC-6 | R6 | The first submission call timed out, outcome unknown | Retry attempted before the backend is queried | Refused until the idempotency key has been reconciled |

Gate 1 carries AG-01 and NAC-1 to NAC-6; gates 2 to 4 carry their own AG test and the same six negative criteria against their own held action. All are ILLUSTRATIVE.

## Worked micro-example

Gate: an auto-submit request arrives for a drafted report. Trigger: the request would submit the report without the filer pressing submit. Approver role: the filer. Channel: the filer review surface. On timeout: the report is not submitted, the filer is notified, and the draft remains available for review. Log: the request ID, the attempted submission parameters, the filer identity, the decision, the model pin, and the applicable prompt versions. The report that never went out because the filer did not approve it is the control working, not the control failing. ILLUSTRATIVE.

## Exit gate

- [x] Every trigger condition is testable, not a vibe. The four triggers identify a ready-to-submit report, confidence under 0.80, a proposed mapping correction, and a charge awaiting activation confirmation.
- [x] Every approver is a role with a rota, and the rota exists. The approvers are the filer, finance reviewer, finance admin, and account admin roles, with the relevant account's person responsible for each decision.
- [x] Every timeout behavior is deny, or the fail-open is in section 3 with an owner. All four gates deny and notify on timeout, and the fail-open register is honestly empty.
- [x] The audit record fields are implemented, not aspirational; someone has read one. AG-01 to AG-04 test the four records, including the model and prompt versions and the 7-year retention assumption requiring legal confirmation.
- [x] Every held action produces an approval record with all seven fields in section 4. AG-01's record is written out above; AG-02 to AG-04 write the same fields against their own held actions.
- [x] R1 to R6 are implemented by the executor, not only written here; each has a test. NAC-1 to NAC-6 cover them.
- [x] NAC-1 to NAC-6 each name a test that fails when the rule is removed, and each gate row names the NAC IDs that apply to it.
- [x] An attempt with an unknown outcome cannot be retried until it has been reconciled. R6 holds the record open and NAC-6 is the refusal.

Signed: Maya Chen, Product Manager, 2026-11-04
