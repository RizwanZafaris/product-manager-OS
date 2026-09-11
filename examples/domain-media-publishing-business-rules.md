# Business Rules Register: Thornfield Post

Fills [templates/definition/business-rules.md](../templates/definition/business-rules.md). Everything here is invented for this standalone example: Thornfield Post is a fictional news and opinion platform, Priya Raghunathan its only fictional product manager, and every number, name, date, and regulatory interpretation is ILLUSTRATIVE, not drawn from any real publisher or market. There is no external Thornfield journey or data sheet. See the [examples index](README.md).

**Owner:** Priya Raghunathan · **Date:** 2026-09-11 · **Status:** Approved at Gate 2 attempt 1
**Applies to:** PRD and FRD not filled for this example (ILLUSTRATIVE)

## 1. Active rules

| ID | Rule statement (WHEN ... THEN ...) | Trigger point in the product | Source of truth | Business owner | Exceptions | Enforced by (FR ID) | Test traceability |
|---|---|---|---|---|---|---|---|
| BR-001 | WHEN a notice under the EU Digital Services Act is submitted against content reachable from an EU IP range THEN the platform records a statement of reasons and either removes, restricts, or rejects the notice within the internally set target of 24 hours, whichever the assessment supports | Notice intake queue, EU jurisdiction flag set at ingestion | Regulation (EU) 2022/2065 (Digital Services Act), Articles 16 and 17 (verify current article numbering and any applicable timeline before relying; as of 2026-09-11, confirm with counsel, not legal advice) | Head of Trust and Safety | A notice flagged as manifestly unfounded at intake is logged but does not start the removal clock; the statement of reasons is still required | FR-092 (notice intake) | AC-31: a test notice submitted from an EU-tagged session produces a timestamped statement of reasons visible to the notifier within the target window |
| BR-002 | WHEN a DMCA takedown notice is received AND a valid counter-notice is filed THEN the removed content is restored after 10 to 14 business days unless the rights holder notifies the platform it has filed a court action seeking to restrain the user from the infringing activity | Copyright dispute resolution workflow | US Digital Millennium Copyright Act, section 512(g)(2)(C) (as of 2026-09-11, confirm with counsel, not legal advice); this is the safe-harbor procedure a service provider follows to keep its 512 liability shield, not a stand-alone statutory command to the platform | General Counsel | None; the 10-to-14-business-day window is fixed by statute, restoration does not happen before day 10 or after day 14 | FR-104 (copyright dispute handling) | AC-45: simulation of counter-notice filing triggers restoration check at day 10 and day 14 boundaries |
| BR-003 | WHEN a factual error is identified in published content THEN a correction notice is appended to the article body and a correction log entry is created | Editorial review tool, "Flag for Correction" action | Thornfield Post Editorial Code v3, Section 4.2 (Corrections and Clarifications) | Standards Editor | None; all factual errors require correction regardless of severity | FR-112 (correction logging) | AC-58: submitting a correction flag generates a visible correction banner and a corresponding entry in the public corrections log |
| BR-004 | WHEN a non-subscriber reads their fifth metered article in a rolling 7-day period THEN subsequent article views are blocked behind the paywall prompt until subscription or 7-day reset | Content delivery gateway, user session tracking | Subscription Policy v2, Metered Access Clause | VP of Product | Subscribers, press pass holders, and authenticated journalists are exempt | FR-120 (metering logic) | AC-62: viewing 5 articles then attempting a 6th results in a 403 Forbidden response with paywall redirect |
| BR-005 | WHEN a reader comment receives three or more reports for hate speech OR one report for imminent harm THEN the comment is automatically hidden pending human review | Comment moderation queue, automated reporting threshold | Internal Moderation Escalation Matrix v1, which sets the specific 3-report and 1-report thresholds as this platform's implementation of the risk-mitigation duties in the UK Online Safety Act 2023, Duties on User-to-User Services (the Act does not itself specify a report count; as of 2026-09-11, confirm with counsel, not legal advice) | Head of Trust and Safety | None; automated hiding is mandatory for high-severity flags | FR-135 (automated moderation escalation) | AC-70: test comments with varying report counts verify hiding trigger at exactly 3 reports for hate speech and 1 for imminent harm |

## 2. Retired rules

| ID | Rule statement | Retired on | Retired by | Why | Replaced by |
|---|---|---|---|---|---|
| BR-000 | WHEN a DSA notice is received THEN remove within 48 hours | 2026-08-15 | Priya Raghunathan | Internal target tightened to 24 hours following Q3 compliance audit findings regarding slow response times | BR-001 |

## 3. Exception handling

| Rule ID | Exception | Who may grant it | Recorded where |
|---|---|---|---|
| BR-001 | Manifestly unfounded notices do not start the removal clock | Senior Trust and Safety Manager | Audit log entry with reason code "MFU-01" |
| BR-004 | Press pass exemption for verified journalists | Newsroom Managing Editor | Subscriber database flag "PRESS-PASS" |

## 4. Change control

- **Who may change a rule:** The named business owner in column 5 of section 1; changes to moderation rules require sign-off from the Standards Editor, not engineering.
- **How a change lands:** Request via Jira epic MERIDIAN-COMPLIANCE, approved by Owner and Legal, deployed via feature flag rollout over 7 days.
- **Review cadence:** Quarterly, aligned with the Board Risk Committee schedule; next review due 2026-12-15.

---

### Worked micro-example (illustrative, invented)

> **BR-001:** WHEN a notice under the EU Digital Services Act is submitted against a piece of content reachable from an EU IP range THEN the platform records a statement of reasons and either removes, restricts, or rejects the notice within the internally set target of 24 hours, whichever the assessment supports. Trigger: Notice intake queue. Source of truth: Regulation (EU) 2022/2065, Articles 16 and 17. Business owner: Head of Trust and Safety. Exceptions: Manifestly unfounded notices. Enforced by FR-092. Test: AC-31.
> If the regulation's interpretation shifts or internal SLAs tighten, the change enters through section 4, BR-001 is retired into section 2, and a new BR replaces it. The history explains why August notices behaved differently from September notices.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every rule is atomic: one trigger, one outcome
- [x] Every rule names a source of truth a reviewer could open
- [x] Every rule has a business owner outside the product team
- [x] Exceptions are enumerated with a decider, or marked "none"
- [x] Every rule maps to an enforcing FR and a test ID, or carries an owner and date to close the gap
- [x] Change control names who may change rules and how changes reach production

Signed: Priya Raghunathan, Product Manager, 2026-09-11
