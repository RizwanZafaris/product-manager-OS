# Human Approval Gates: Ledgerline Expense Copilot Add-on

Fills [templates/ai/human-approval-gates.md](../templates/ai/human-approval-gates.md). Everything here is invented: Ledgerline is a fictional software company, the Expense Copilot add-on is fictional, and every person, date, threshold and identifier is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and the [coverage sheet](ledgerline-coverage-sheet.md). See the [examples index](README.md).

**Gates owner:** Maya Chen · **Document date:** 2026-11-04

## 1. Gate table

| # | Trigger condition (specific, testable) | Action held | Approver role (role, not person; person on rota) | Channel and SLA | On timeout | Test |
|---|---|---|---|---|---|---|
| 1 | A draft is ready for submission, or an auto-submit request is received | Submission of the expense report | Filer for the account | Filer review surface; no automatic approval | deny and notify the filer; the report remains unsubmitted | AG-01 |
| 2 | Any extracted field or suggested category has model confidence under 0.80 | Release of the flagged field or category into the reviewable draft | Finance reviewer for the account | Reviewer queue; reviewer response is required before the flagged field is confirmed | deny and notify the filer and reviewer; the field remains flagged | AG-02 |
| 3 | A finance admin proposes a category mapping correction | Acceptance of the proposed correction into the audit log; v1 does not feed the correction back into the model or mapping behavior | Finance admin for the account | Finance-admin correction queue; correction decision is required before the correction is recorded | deny and notify the finance admin; the correction is not recorded | AG-03 |
| 4 | An account admin has selected activation for the add-on and a charge is ready to be presented | Add-on activation and creation of the charge | Account admin for the account | Expenses settings activation surface; charge must be confirmed before activation | deny and notify the account admin; the add-on remains inactive | AG-04 |

Gate 1 is the filer control described by the PRD's out-of-scope line: auto-submission is not in scope, and the filer submits, always. Gate 2 implements [LEDGERLINE-S3](ledgerline-journey.md), using the assumption that a field or suggested category under 0.80 model confidence is flagged (LC22). Gate 3 records the finance-admin correction, but the correction is never fed back into the drafting model or mapping behavior in v1. Gate 4 implements [LEDGERLINE-S1](ledgerline-journey.md): the account admin sees and confirms the charge before activation.

## 2. Audit log requirement

Every gate decision writes a record with, at minimum:

- Request ID, timestamp, and the triggering condition matched
- The held action's full parameters as presented to the approver, including the report, flagged field, proposed mapping correction, or charge details as applicable
- Approver identity, decision, decision time, and free-text reason if denied
- Model version and prompt version that produced the request, where a model or prompt produced it: model pin `docmodel-2026-09-30`; prompt ids `copilot-extract` and `copilot-policy-match`, with their applicable versions from LC17
- Retention period for these records: 7 years, the finance-records rule; this is an assumption and the legal lead is to confirm it for customer accounts (LC27)
- Where the log lives and who can read it: the approval-gate audit store, readable by the gates owner, the relevant finance and billing administrators, the legal lead, and authorised reviewers on the account

The log records denials as well as approvals. A timeout is recorded as a denial, with the timeout reason and notification outcome. A finance-admin mapping correction is retained as an audit event even though it is not fed back into v1.

## 3. Exceptions and fail-open register

There are no fail-open exceptions. Every gate denies on timeout. No operational reason, risk owner, or compensating control has been approved for a fail-open path.

| Gate # | Why it fails open | Compensating control | Risk owner | Review date |
|---|---|---|---|---|
| None | None. No gate fails open. | Not applicable. Every timeout denies and notifies. | Not applicable | Not applicable |

## Worked micro-example

Gate: an auto-submit request arrives for a drafted report. Trigger: the request would submit the report without the filer pressing submit. Approver role: the filer. Channel: the filer review surface. On timeout: the report is not submitted, the filer is notified, and the draft remains available for review. Log: the request ID, the attempted submission parameters, the filer identity, the decision, the model pin, and the applicable prompt versions. The report that never went out because the filer did not approve it is the control working, not the control failing. ILLUSTRATIVE.

## Exit gate

- [x] Every trigger condition is testable, not a vibe. The four triggers identify a ready-to-submit report, confidence under 0.80, a proposed mapping correction, and a charge awaiting activation confirmation.
- [x] Every approver is a role with a rota, and the rota exists. The approvers are the filer, finance reviewer, finance admin, and account admin roles, with the relevant account's person responsible for each decision.
- [x] Every timeout behavior is deny, or the fail-open is in section 3 with an owner. All four gates deny and notify on timeout, and the fail-open register is honestly empty.
- [x] The audit record fields are implemented, not aspirational; someone has read one. AG-01 to AG-04 test the four records, including the model and prompt versions and the 7-year retention assumption requiring legal confirmation.

Signed: Maya Chen, Product Manager, 2026-11-04
