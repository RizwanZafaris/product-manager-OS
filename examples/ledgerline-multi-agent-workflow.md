# Multi-Agent Workflow: Ledgerline Expense Copilot Receipt Draft

Fills [templates/ai/multi-agent-workflow.md](../templates/ai/multi-agent-workflow.md). Everything here is invented: Ledgerline is a fictional company, the Expense Copilot is a fictional product, the agents and people are fictional, and every number, date and identifier is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) and its [coverage sheet](ledgerline-coverage-sheet.md). See the [examples index](README.md).

**Workflow owner:** Priya Nair, engineering lead · **Document date:** 2026-11-04
**Workflow:** receipt in, entitlement-checked extraction and policy-matched draft out, with unknown fields blank and flagged for human review
**Agents involved:** Extraction agent, extraction tier; Policy-match agent, drafting tier; fixed-pipeline orchestrator and finance reviewer are control roles, not additional agents

## 1. Handoff sequence

The fixed-pipeline orchestrator controls the order. The forwarded-email path must enter at step 1, because RT-06 found that drafts could otherwise be produced for accounts without the add-on active. RT-06 was fixed and re-attacked by Nadia Rahimi on 2026-11-06, with the test held.

| Step | From | To | Payload (format, required fields) | On malformed payload |
|---|---|---|---|---|
| 1, entitlement check | Receipt intake and fixed-pipeline orchestrator | Fixed-pipeline orchestrator | Receipt envelope JSON: `account_id`, `receipt_source`, `receipt_object_reference`, `add_on_entitlement`, `received_at`; `add_on_entitlement` must resolve to active or inactive from the billing entitlement record | Reject the receipt from drafting, record the reason, and tell the filer that no draft was created. Do not retry around the entitlement check. A forwarded email follows the same check and cannot bypass it |
| 2, extraction | Fixed-pipeline orchestrator | Extraction agent | Entitled receipt envelope plus the receipt image or PDF. Output JSON must contain `merchant`, `date`, `amount`, `currency`, one confidence value per extracted field, and `extraction_status`. Unknown fields are empty and have a confidence flag | Return the payload to the orchestrator as malformed, record the missing field or invalid type, and send no extraction result to policy match. The orchestrator may use the one permitted retry, then escalates the run to the reviewer with the receipt and the failure |
| 3, policy match | Fixed-pipeline orchestrator | Policy-match agent | Extraction result plus `account_id`, the account's retrieved policy excerpt, category list with policy-line ids, and the policy freshness result. Output JSON must contain `suggested_category`, `policy_line_id`, `category_confidence`, `policy_match_status`, and `policy_source` | Do not create a policy suggestion. Keep the extracted fields, leave `suggested_category` and `policy_line_id` empty, flag the draft for the reviewer, and record whether the failure was malformed input, stale policy, or no match |
| 4, draft assembly | Fixed-pipeline orchestrator | Shared draft state, then reviewer when flagged | Draft JSON containing the receipt fields, policy suggestion fields, confidence flags, entitlement result, source references, and `draft_status` | Do not publish the draft as ready for filing. Preserve the last valid shared state, mark the draft flagged, and route it to the finance reviewer. The filer remains the submitter, and no agent can submit the report |

The policy-match agent uses the account's own policy excerpt, as required by `copilot-policy-match` v4 on 2026-11-04 and v5 on 2026-11-06. The policy index refreshes on every admin save and has a maximum age of 24 hours. Past that age, policy match abstains, leaves the suggestion blank, and flags the field.

## 2. Shared state

- **Where it lives:** one account-scoped draft record in the Expense Copilot draft store, keyed by the receipt envelope's `account_id` and `receipt_object_reference`. The orchestrator creates the record only after the entitlement check passes.
- **Schema:** `account_id`, `receipt_object_reference`, `receipt_source`, `entitlement_status`, `merchant`, `date`, `amount`, `currency`, `suggested_category`, `policy_line_id`, `extraction_confidence`, `category_confidence`, `field_flags`, `policy_match_status`, `source_references`, `draft_status`, `reviewer_override_fields`, `reviewer_decision`, and audit timestamps.
- **Who may write which fields:**

| Field or field group | One writer | Rule |
|---|---|---|
| `account_id`, `receipt_object_reference`, `receipt_source`, `entitlement_status` | Fixed-pipeline orchestrator | Written during entitlement check and immutable for the run |
| `merchant`, `date`, `amount`, `currency` | Extraction agent | Unknown values remain empty. The agent cannot replace an empty value with a guess |
| `extraction_confidence`, extraction field flags | Extraction agent | One confidence value and flag per extracted field |
| `suggested_category`, `policy_line_id`, `category_confidence`, `policy_match_status` | Policy-match agent | A no-match or stale-policy result writes an empty suggestion and a flag |
| `source_references`, `draft_status`, audit timestamps | Fixed-pipeline orchestrator | The orchestrator assembles the draft and controls state transitions |
| `reviewer_override_fields`, `reviewer_decision` | Finance reviewer | Reviewer corrections are separate from agent output. They do not silently rewrite the agent's original fields |
| Filer submission | Filer through the approval gate | No agent has a submit action |

There are no two writers to one field. The agent output is retained as the original value, while reviewer corrections use the separate override fields. The draft is the shared state, not a free-form message passed between agents.

- **What a human sees when inspecting a run in flight:** the reviewer view shows the receipt, entitlement result, every extracted field, every policy suggestion, the confidence flag beside the relevant field, the policy line used, the source reference, the agent status, and the audit history. Blank unknown fields are visible as blank and flagged, not replaced with placeholder text.

## 3. Escalation to a human

- **Conditions that force escalation:**
  - Any extracted field or suggested category has model confidence under 0.80, the LC22 threshold.
  - An extracted field is unknown, malformed, or blank.
  - The policy is older than 24 hours, the LC25 maximum age, or the policy-match agent abstains.
  - The extraction agent and policy-match agent cannot produce a consistent draft, including a missing policy line for a suggested category.
  - The entitlement result is inactive, unavailable, or inconsistent with the receipt source. The run stops rather than attempting a bypass.
  - A step exhausts its one permitted retry, or a cost ceiling is reached.
- **Escalates to (role with a rota, not a name):** finance reviewer on the customer account's reviewer rota. Cost and workflow exceptions also notify the engineering on-call role and the finance lead.
- **What the human receives:** the preserved run state, the receipt, the entitlement result, the field or fields in dispute, the confidence values and flags, the policy excerpt and policy freshness result, the agent error if present, the retry count, and the recommended action: accept, correct, or reject the draft.
- **Approval-gated actions inside the workflow route through the filled [human approval gates](ledgerline-human-approval-gates.md), not through an agent's own judgment.** In particular, the filer submits the report, the reviewer confirms flagged fields, and no agent submits, activates, bills, or changes a mapping.

## 4. Termination

- **Success:** the entitlement check is active, extraction has produced a complete or reviewer-accepted set of fields, policy match has produced an accepted category and policy line or the reviewer has explicitly resolved the abstention, and the draft record is marked `ready_for_filer`. Code can check that the draft has an active entitlement, a value or explicit reviewer resolution for each required field, a recorded policy outcome, and no unresolved confidence flag.
- **Failure:** the run ends as failed when entitlement is inactive or cannot be verified, the receipt payload remains malformed after the permitted retry, the receipt cannot be processed, or the reviewer rejects the draft. The requester is told that no submission-ready draft was created and is given the reason, such as add-on not active, unreadable receipt, missing field, or policy match unavailable. The run state and audit record are retained for review.
- **Budget stop:** the run halts when it hits any of the caps in section 5, preserving state for human review, never silently retrying past a cap. The filer gets a blank, flagged draft and a message that the draft needs reviewer attention. The entitlement result is never treated as active merely because the budget stop occurred.

## 5. Cost cap

- **Per-run token or spend ceiling:** per receipt, $0.30; per drafted report, $1.05, the M-009 ceiling. The measured M-009 cost was $0.93 per drafted report in the review window, so the measured amount was under the ceiling by `$1.05 minus $0.93 = $0.12`.
- **Per-day ceiling for the whole workflow:** $150 across all customer accounts. The measured review-window arithmetic was `555 drafted reports x $0.93 = $516.15`; `26 days`, so `$516.15 / 26 = $19.85`, about $20 a day, against the $150 ceiling.
- **Max steps per run (loop guard):** 3 steps per receipt. The fixed sequence contains entitlement check, extraction, policy match, and draft assembly, with draft assembly as the state transition rather than another model step.
- **Max retries per step:** 1 retry per step.
- **At any ceiling:** halt and escalate. Do not degrade silently, continue past the cap, or retry after the cap. The filer receives a blank, flagged draft, and the state is preserved for the reviewer.
- **Who reads the spend report, on what cadence:** Daniel Okafor, finance lead, reads the spend report weekly. The report includes per-receipt spend, per-drafted-report spend, daily spend, cap events, retries, and the drafted count.

The caps are the customer workflow's target controls agreed with Daniel Okafor on 2026-11-04. The measured $0.93 per drafted report and 555 drafted reports are from M-009 and the active add-on review window, not a forecast.

## Worked micro-example

A Ledgerline receipt arrives by forwarded email. The fixed-pipeline orchestrator first checks the account entitlement. If it is active, the orchestrator writes the receipt envelope to the shared draft state and sends the entitled payload to the Extraction agent.

The Extraction agent writes `merchant`, `date`, `amount`, and `currency`. If the amount is unreadable, it leaves `amount` blank and writes the field flag. It does not infer the value from surrounding text.

The orchestrator sends the extraction result and the account's policy excerpt to the Policy-match agent. The agent writes the suggested category, policy line, category confidence, and match status. If confidence is under 0.80, the field is flagged.

The orchestrator assembles the draft without taking ownership of either agent's fields. A reviewer sees the blank amount and the low-confidence category flag, corrects or confirms them through the approval gate, and the filer reviews the complete report before submitting. If the account lacks the add-on, the run ends at entitlement check and no draft is produced. If cost reaches a cap, the run ends with a blank, flagged draft and preserved state.

## Exit gate

- [x] Every handoff is numbered with a payload format and a malformed-payload behavior. Steps 1 to 4 cover entitlement check, extraction, policy match, and draft assembly.
- [x] Every shared-state field has exactly one writer, or a written merge rule. The field map gives one writer per field, with reviewer overrides stored separately from agent output.
- [x] Escalation conditions are testable and route to a role with a rota. The 0.80 confidence threshold, 24-hour policy age, retry cap, malformed payload, disagreement, and entitlement conditions route to the finance reviewer or the relevant on-call role.
- [x] All three termination paths are written, including the budget stop. Success, failure, and budget stop each state the condition, preserved state, and requester outcome.
- [x] Every cap has a number and a named reader of the spend report. The caps are $0.30 per receipt, $1.05 per drafted report, $150 per day, 3 steps per receipt, and 1 retry per step. Daniel Okafor reads the report weekly.

Signed at AI overlay Gate 3, 2026-11-04: Priya Nair, engineering lead. Least-access review completed with Nadia Rahimi, application security lead, on 2026-11-04.
