# Release Notes: Harbourgate

Fills [templates/delivery/release-notes.md](../templates/delivery/release-notes.md). Everything here is invented: Harbourgate, Quay, Kestrel, Marlowe and Tidewater are fictional, every person is fictional, and every number, date, rate and pound is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md).

**Owner:** Ife Adeyemi · **Date:** 2026-07-08 · **Status:** Approved, GO WITH CONDITIONS for Marlowe cohort 1

## 1. Release facts

| Field | Value |
|---|---|
| Release | Marlowe cohort 1 |
| Ship date and time | 2026-07-13, 10:00 Europe/London |
| Rollout shape | Staged behind a per-provider flag: Marlowe cohort 1 at 5%, followed by 50% and 100% cohorts on 2026-07-16 and 2026-07-20 |
| Readiness decision | GO WITH CONDITIONS, [release-readiness.md](harbourgate-release-readiness.md), Gate 5 attempt 2 |
| Scope cuts since sign-off | None recorded in the release readiness decision |
| Rollback trigger and owner | Cohort decline rate above baseline + 2 percentage points over 30 minutes, or Kestrel 5xx above 2% of calls over 5 minutes; on-call calls the rollback without discussion. The flag flip to legacy was rehearsed in 3 min 50 s |

The release is silent. The internal note was sent on 2026-07-08 in the payments channel and the finance weekly, and the flag was flipped to 5% on 2026-07-13 at 10:00 Europe/London. See [harbourgate-journey.md](harbourgate-journey.md) and [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md), rows HC25, N17, N40 and N71.

## 2. Customer notes

This is a silent release. Nothing changes for you because the payment step keeps the existing customer-facing flow while Harbourgate changes the payment provider path behind it.

**What is new**

- Nothing customer-visible. The payment step continues to work as before while the internal payment path is shifted in stages.

**What changed**

| Before | Now | What you need to do |
|---|---|---|
| Payments for this cohort used the Marlowe path, including its existing internal fallback behaviour | The cohort is being shifted behind a per-provider flag as part of Harbourgate's payment-path modernisation | Nothing |

**What was removed or deprecated:** The old Marlowe fallback rule, BR-008, which retried a Kestrel decline through Marlowe, is retired when Marlowe cohort 3 reaches 100% on 2026-07-20. It is replaced by BR-001: offer one retry with a different method, and never resubmit the same card automatically.

**Known limitations in this release:** A small number of Kestrel declines may still be shown with the reason class “other”. That class covered 6% of Kestrel declines at Gate 5 attempt 2. The mapping fix is scheduled for 2026-08-14 and brings the measured share to 1.5%.

## 3. Internal notes

- Problem this release addresses: Harbourgate's payment path did not attribute all declines to a provider, and one order in nine reaching the payment step did not complete it.
- Metric it is expected to move: Decline event completeness, from 0% of Marlowe declines carrying provider and reason information at entry to 100% of all declines at Gate 6. The supporting dashboard is the [Harbourgate observability record](harbourgate-observability.md).
- Watch for in the first cohort dwell: The cohort decline rate against its provider baseline, Kestrel 5xx calls, and the rollback trigger. The first cohort dwell is 3 days. Owner: Bea Lindqvist, with the on-call owner calling rollback when N17 fires.
- Flags and configuration: The per-provider routing flag controls the Marlowe cohort. A flag change needs two named approvers and is logged with both names. The on-call may call rollback without discussion when N17 fires.
- Not in this release, and when: Marlowe cohorts 2 and 3 follow on 2026-07-16 and 2026-07-20. BR-008 retires at Marlowe cohort 3 on 2026-07-20. Tidewater store cohorts begin on 2026-08-03, and the Kestrel legacy connector cohorts begin on 2026-08-31.

## 4. Support notes

| # | Symptom the customer will report | Cause | Workaround or answer | Escalate to | Fix date |
|---|---|---|---|---|---|
| KI-1 | “My payment was declined, but the reason says other.” | Some Kestrel declines are still mapped to the reason class “other”. The measured share was 6% at Gate 5 attempt 2. | Confirm the order id and decline event. Explain that the payment was declined and the reason-class label is incomplete. Offer one retry with a different method. Do not resubmit the same card automatically. | Bea Lindqvist, payments on-call | 2026-08-14 |
| KI-2 | “My payment or refund is still being checked after the provider change.” | The settlement straddle set had not yet met a live settlement cycle when this release note was written. | Do not promise an immediate reconciliation result. Record the order id and allow the dual-path reconciliation to classify the straddle set. | Bea Lindqvist | 2026-07-16 |
| KI-3 | “Why has Marlowe not answered my payment question yet?” | Marlowe support is a ticket queue only, with a 4-hour response commitment. | Record the provider ticket and order id. Tell the customer that the provider response is handled through the ticket queue. | Bea Lindqvist, then Marlowe merchant support | 2026-12-15 |

**Expected questions, with the agreed answer:**

- **Will customers see a new payment screen?** No. This is a silent release. The customer-facing payment step does not change.
- **What should an agent do when a payment is declined?** Confirm the order id, explain the visible result, and offer one retry with a different method. The same card must not be resubmitted automatically.
- **Why does the decline reason say “other”?** Some Kestrel decline events still use that class. The mapping fix is scheduled for 2026-08-14.
- **What happens to a refund for an order authorised by a legacy provider?** Route it to the provider that authorised the order while the legacy refund capability remains available.
- **Who handles a Marlowe provider question?** Marlowe support handles it through the ticket queue. Escalate internally to Bea Lindqvist with the order id and provider ticket.

**Escalation path for this release:** Sev 1 pages the payment-path on-call. The squad's five engineers rotate on call, with acknowledgement within 5 minutes, escalation to Bea Lindqvist at 15 minutes and to Tomasz Wierzbicki at 30 minutes. Sev 2 covers one provider cohort or a group of shops, and Sev 3 covers one customer. Support owner: Callum Fraser.

**Where the runbook lives:** [harbourgate-support-runbook.md](harbourgate-support-runbook.md)

## 5. Breaking changes and deprecations

| Change | Who it affects | Migration path | Old behavior ends | Notice sent (date, channel) |
|---|---|---|---|---|
| BR-008, the Marlowe fallback after a Kestrel decline, is retired | Internal payment consumers and support teams relying on the old cascade behaviour | Use BR-001: offer one retry with a different method, and never resubmit the same card automatically | 2026-07-20, when Marlowe cohort 3 reaches 100% | 2026-07-08, payments channel and finance weekly |
| The `422 legacy_provider_refund` behaviour applies to order service and finance tooling consumers | Order service and finance tooling consumers handling refunds for legacy-authorised orders | Handle the `422 legacy_provider_refund` response and keep legacy-authorised refunds on the original provider path under BR-002 | The legacy provider path is scheduled for shutdown on 2026-12-15 | 2026-07-08, payments channel and finance weekly |

## 6. Distribution

| Audience | Where it is published | Owner | Approved by | Published (date) |
|---|---|---|---|---|
| Customers | Not published, silent release | Ife Adeyemi | Ines Castellanos | Not published |
| Internal | Payments channel and finance weekly | Ife Adeyemi | Priya Raman | 2026-07-08 |
| Support | [harbourgate-support-runbook.md](harbourgate-support-runbook.md) and support briefing | Callum Fraser | Callum Fraser and Bea Lindqvist | 2026-07-10 |

## 7. How release notes fail

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Internal language leaks out | A line describing a service, a queue or a refactor | Every line says what a user can now do, see, or stop seeing |
| Changes nobody can act on | “Improved internal error handling” | If a reader cannot tell whether it affects them, it does not belong here |
| Vague bug fixes | “Fixed an issue with exports” | Name the symptom and the situation, so the person who reported it recognises it |
| Removals go unmentioned | Only additions appear, and something quietly stopped working | A required section for anything removed, deprecated, or changed by default |
| Written after the release | Users meet the change before the note explaining it exists | The draft is done before the release, and the gate above checks that |
| No owner, so they stop | A gap of several releases, then an apology | A named owner, and a missing note is a missed deliverable rather than an oversight |

## Exit gate (feeds Gate 5: release readiness green)

The customer and support blocks satisfy the comms rows of [release-readiness.md](harbourgate-release-readiness.md) section 6 and the comms checkbox at Gate 5. The release readiness record is also indexed in [harbourgate-journey.md](harbourgate-journey.md) and the release-note coverage is recorded in [harbourgate-coverage-sheet.md](harbourgate-coverage-sheet.md).

- [x] Section 1 matches the filled release-readiness.md line for line
- [x] Every customer-facing line names a capability or a change, not an adjective
- [x] Every removal or deprecation has an end date and a migration path
- [x] Every known issue in the readiness document appears in section 4 as a symptom with a workaround
- [x] Support has read section 4 before any customer copy is published
- [x] Each audience row in section 6 has a named approver
- [x] Signed by Ife Adeyemi, 2026-07-08
