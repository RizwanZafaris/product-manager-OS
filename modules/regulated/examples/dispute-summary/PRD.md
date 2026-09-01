# PRD: Dispute Summary Assistant

> **This is a fictional worked example.** The institution, the systems, the ticket and register numbers, the dates, the people, and every metric are invented to show what a completed template looks like. Every threshold, limit, budget, retention period, and SLA carries the label **ILLUSTRATIVE** where it is stated, and none is a recommendation. The only things here that are real are the two regulatory instruments and the public dataset, all cited to primary sources and read on 2026-09-01.
>
> **Owners are written as role seats** rather than personal names, because this example is public. In a real PRD every one of these is a person, because a seat cannot be paged and a person can.

**Feature:** An LLM assistant that drafts a structured summary and evidence checklist for an inbound cardholder dispute, for a human disputes analyst to review before the analyst decides how to handle the case. The assistant never decides a dispute.
**Markets in scope:** UAE (CBUAE-licensed retail payment services provider) and Ireland (EU entity, serving EEA acquiring). Answers below differ per market where marked.
**Implementer type:** LLM feature, retrieval over the case file, single turn, no tool calls, no autonomous actions.
**Document owner:** Product Lead, Disputes · **Regulatory owner:** Regulatory Affairs Lead · **Engineering owner:** Engineering Manager, Disputes Platform
**Status:** In review · **Version:** 4 · **Document date:** 2026-08-28
**Regulatory references verified as of:** 2026-09-01

---

## What this document is for

The disputes queue is the part of the business where a wrong number becomes a customer complaint, and a customer complaint becomes a regulator's reference number. This feature puts a language model in front of that queue. This document is the contract that says what the model may do, what it may never do, how we will know, and who is accountable when it is wrong.

The assistant drafts. A named human decides. Everything below is written to keep that sentence true under load.

---

## 0. Regulated overlay

### 0.1 Regulatory precondition register

| Market | License condition, approval, or notification that gates this feature | Regulator | Confirmed how (a document, not a conversation) | Confirmed date | Owner |
|---|---|---|---|---|---|
| UAE | No change to licensed activity identified: the assistant is internal decision support, does not contact customers, and does not alter the customer terms. Checked against the entity's schedule of permitted activities | CBUAE | Regulatory Affairs memo REG-2026-114, attaching the permitted-activities schedule | 2026-07-30 | Regulatory Affairs Lead |
| UAE | Governance expectations of the [CBUAE Guidance Note on AI and ML](https://rulebook.centralbank.ae/en/rulebook/guidance-note-consumer-protection-and-responsible-adoption-and-use-artificial-intelligence) (issued 11 February 2026) mapped to the entity's model governance framework; feature entered in the AI model inventory with a risk rating before any production traffic | CBUAE | AI inventory record AI-INV-0042; Guidance Note read in full and mapped in memo MRM-2026-08 | 2026-08-20 | Model Risk Lead |
| UAE | Board and senior management reporting route for this model agreed and added to the quarterly model risk pack | CBUAE | Model Risk Committee minutes MRC-2026-06, item 4 | 2026-08-25 | Model Risk Lead |
| Ireland (EU) | Open question: whether this feature is a high-risk AI system under Article 6 of Regulation (EU) 2024/1689, and therefore whether Annex IV technical documentation applies. Working assumption is that it is not, because the assistant drafts and a human decides, but that assumption is not confirmed. Instructed to external counsel; opinion not yet received | External counsel, EU entity | Counsel instruction LEG-2026-221 issued 2026-08-12; opinion due 2026-09-30 | Not yet confirmed. See GAPS row 1 | Regulatory Affairs Lead |
| Ireland (EU) | No new authorization or notification identified for internal decision support under the existing payment institution authorization, subject to the row above | Central Bank of Ireland | Regulatory Affairs memo REG-2026-118 | 2026-08-14 | Regulatory Affairs Lead |

### 0.2 Scheme-rule constraints

Scheme rulebooks are licensed documents. Rows cite the internal register entry that pins the edition we read, not the text itself, and this public example does not reproduce or date any scheme edition.

| Rule area touched (authorization, tokenization, disputes, data) | Scheme and rule or bulletin reference | Version pinned at spec time | Who watches the quarterly releases for drift |
|---|---|---|---|
| Dispute reason codes and their definitions | Card scheme A, dispute rules chapter, held under scheme documentation register entry SR-2026-03 | Edition in force at spec time, recorded in SR-2026-03 | Disputes Rules Analyst |
| Dispute time limits and representment windows | Card scheme A, dispute rules chapter, register entry SR-2026-03 | Edition in force at spec time, recorded in SR-2026-03 | Disputes Rules Analyst |
| Evidence and compelling-evidence requirements | Card scheme B, dispute rules chapter, register entry SR-2026-04 | Edition in force at spec time, recorded in SR-2026-04 | Disputes Rules Analyst |
| Cardholder data handling in the evidence pack | Scheme data security requirements, register entry SR-2026-07 | Edition in force at spec time, recorded in SR-2026-07 | Security Architect, Disputes |
| Non-card rails (account-to-account disputes) | Not applicable. This release is card disputes only. Non-card rails are out of scope and blocked at the intake filter | N/A because there is no non-card rule set to pin while non-card rails are blocked at intake | Not applicable in this release. Owner assigned when scope extends: Disputes Rules Analyst. See GAPS row 7 |

### 0.3 Data residency and model-vendor terms

- Data classes in the flow, and where each is stored and processed: case metadata, cardholder narrative text, merchant details, transaction reference, disputed amount, and uploaded evidence documents. UAE cases are stored and processed in the UAE cloud region and inference is served from the UAE region only. EU cases are stored and processed in the EU (Ireland) region and inference is served from the EU region only. No case data crosses between the two.
- Cross-border transfer basis where applicable: none required in this design, because there is no cross-border transfer. If the UAE region loses inference capacity, the feature fails closed and cases queue for manual handling rather than failing over across a border. This is a deliberate availability sacrifice, recorded in section 5.
- Model vendor terms verified: the provider does not train on our inputs or outputs. Enterprise agreement clause 7.3, plus the zero-retention addendum executed 2026-06-11. Verified by Procurement and Legal, memo LEG-2026-198.
- Vendor audit and information rights secured in contract: yes. Enterprise agreement clauses 11.2 (information rights) and 11.4 (audit on notice), plus the vendor's current third-party security attestation reviewed annually by Security Assurance.
- Retention period per record class, per applicable requirement: dispute case records 24 months after case closure, per the disputes retention standard RET-04. Model input and output logs 90 days, extended to case-record retention where a log is attached to a case that is under complaint or regulatory query. Eval sets and their labels are retained for the life of the model version plus 12 months. All three periods are ILLUSTRATIVE.
- Model and prompt version pinning: yes. The model version string and the prompt template version are both pinned in configuration and logged on every call. A change to either is a release, approved by the Model Risk Lead with a full eval re-run attached.

### 0.4 Financial-crime touchpoints

- Screening points in the flow (AML, CTF, sanctions), and what happens on a hit: screening happens upstream in the case management system at case intake, before the assistant is invoked, and it is unchanged by this feature. On a screening hit the case is locked to the financial crime queue and the assistant is not invoked at all. The assistant therefore never sees, and never comments on, a screened-positive case.
- Decisions the AI may NEVER make alone. Every item here is a MUST ESCALATE row in section 2: any sanctions or screening disposition, any suspicious-activity judgment or anything that would feed a report to the financial intelligence unit, any first-party-fraud allegation against the cardholder, any reclassification of a case between fraud and dispute, any determination that a customer is vulnerable, and any outcome that closes a dispute against the cardholder.
- Does any output of this feature enter a regulatory report or filing? No, and this is enforced rather than assumed: assistant output is written to a distinct field in the case record that is excluded from the export used to prepare financial intelligence unit filings. The exclusion is covered by a test in the release pipeline, owned by the Engineering Manager, Disputes Platform.

### 0.5 Customer-communication conduct

- Is any AI output shown to customers a regulated communication in any in-scope market? Not in this release. The assistant's output is internal only and never leaves the analyst's workspace. If a later release makes any generated text customer-facing, that is a new conduct question in both markets and a new version of this document, not a configuration change.
- Is the customer told an AI system is involved, and where in the journey? The customer is not told, because in this release the customer never receives AI-generated text and the AI does not make or influence the final decision record. The [CBUAE Guidance Note](https://rulebook.centralbank.ae/en/rulebook/guidance-note-consumer-protection-and-responsible-adoption-and-use-artificial-intelligence) (issued 11 February 2026) sets transparency expectations that bite hardest where a customer interacts with an AI application or is subject to a high-impact decision. The position taken here is that neither applies to an internal draft reviewed and superseded by a human, and that position is recorded in memo REG-2026-114 so that it can be challenged rather than assumed. See GAPS row 4 for the leakage risk that undermines it.
- Languages the customer-facing output must support, and who signs off the translation: not applicable to assistant output, which is English and internal. Customer-facing dispute correspondence remains the existing bilingual Arabic and English template set, human-authored, signed off by the Conduct and Complaints Lead. The assistant does not draft, translate, or alter those templates.
- Can the customer request a human review of an AI-influenced outcome, and by what route? Yes, through the existing complaints channel, unchanged by this feature, with the existing complaint handling SLA. Because a named analyst already owns and signs every dispute outcome, the human review the customer is entitled to has already happened before any outcome is communicated.
- If any output is customer-facing: the approval workflow for generated content, and the owner of that workflow: not applicable in this release. Conduct and Complaints Lead owns this question if scope changes.

### 0.6 The metric that survives an audit

- Headline success metric: median analyst handling time per card dispute case, measured from case assignment to analyst decision submitted.
- Source system and calculation method, agreed in writing with: Ops Data Lead, memo DATA-2026-77, agreed 2026-08-19. Method is fixed in that memo: median not mean, per calendar week, card disputes only, excluding cases reassigned more than once, computed from case management system timestamps rather than from any assistant telemetry.
- Where a third party could independently verify it: the case management system's audit log, which is outside the disputes platform and outside this team's write access. An internal auditor can recompute the number from that log without asking us for anything.
- What this metric is NOT evidence of: it is not evidence of dispute outcome quality, recovery rates, or customer satisfaction, and it is not cleanly attributable to the assistant. A queue routing change shipped in the same window, so the handling-time movement is confounded by design and will be reported as such. Anyone who quotes this number as the assistant's return on investment is quoting it wrongly, and this line exists so that they can be shown where it says so.

---

## 1. Acceptance criteria: eval sets, not sentences

Every threshold below is **ILLUSTRATIVE**. Thresholds are agreed with the Model Risk Lead and the Disputes Ops Lead before release, and until that meeting has happened they are placeholders with numbers attached, which is still better than prose.

Two dataset families are used, and the difference matters:

- **DS-\* sets** are internal, drawn from our own closed dispute cases, dual-labeled by two disputes analysts with a third adjudicating disagreements. These carry the decision-relevant thresholds.
- **RT-\* sets** are adversarial fixtures, hand-built by the team to attack a specific failure mode. These carry the hard-zero and full-recall thresholds.
- **CFPB-\* sets** are built from the public [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/), described in section 1.1. These carry language and structure thresholds only, never decision-relevant ones.

| # | Requirement (was a "should") | Metric | Eval set or dataset (labeled cases) | Pass threshold (a number) | Below threshold | Failing-case owner |
|---|---|---|---|---|---|---|
| 1 | The disputed amount is extracted exactly, or the field is marked unknown | Exact-match accuracy on the amount field, unknown counted as correct only when the source is genuinely silent | DS-AMOUNT-v3: 400 closed cases, dual-labeled | 99.0 percent (ILLUSTRATIVE) | Block release | Disputes Ops Lead |
| 2 | The transaction reference is extracted exactly, or marked unknown | Exact-match accuracy on the reference field | DS-TXNREF-v3: the same 400 cases | 99.0 percent (ILLUSTRATIVE) | Block release | Disputes Ops Lead |
| 3 | The assistant never states a figure that is not present in the case file | Count of fabricated figures across the set | RT-INVENT-v2: 130 adversarial fixtures with conflicting, partial, and absent amounts | 0 occurrences, hard zero (ILLUSTRATIVE) | Block release | ML Engineering Lead, Disputes |
| 4 | The cardholder's stated reason is categorized into the correct one of nine internal categories | Macro-F1 across the nine categories | DS-REASON-v3: 600 closed cases, dual-labeled, stratified by category | 0.88 macro-F1 (ILLUSTRATIVE) | Block release | Disputes Ops Lead |
| 5 | Every claim in the summary is supported by the case file | Claim-level faithfulness, two human reviewers with a third adjudicating | CFPB-FAITH-v2: 150 narratives from the public database, plus DS-FAITH-v2: 150 internal cases. Both must pass | 98.0 percent of claims supported (ILLUSTRATIVE) | Block release | Model Risk Lead |
| 6 | The missing-evidence checklist omits nothing the reason category requires | Recall of required evidence items against the internal evidence matrix | DS-EVID-v2: 250 closed cases | 0.95 recall (ILLUSTRATIVE) | Block release | Disputes Rules Analyst |
| 7 | Every escalation trigger in section 0.4 fires when its condition is present | Escalation recall on seeded triggers, measured per trigger, not averaged | RT-ESC-v2: 110 fixtures, at least 10 per section 0.4 item | 100 percent recall on every trigger, hard (ILLUSTRATIVE) | Block release | Head of Financial Crime, plus Model Risk Lead |
| 8 | Out-of-scope inputs are refused rather than answered | Refusal accuracy, with over-refusal on in-scope cases tracked as a paired metric | RT-REFUSE-v2: 100 out-of-scope fixtures, 100 in-scope controls | 98.0 percent refusal on out-of-scope, and no more than 2.0 percent over-refusal on in-scope (ILLUSTRATIVE) | Block release | ML Engineering Lead, Disputes |
| 9 | No prohibited data class appears in the summary text | Count of prohibited-field appearances (full card number, IBAN, national ID, CVV) | RT-PII-v2: 100 fixtures with these values seeded into evidence documents | 0 occurrences, hard zero (ILLUSTRATIVE) | Block release | Security Architect, Disputes |
| 10 | The assistant never asserts a legal, regulatory, or liability conclusion | Count of legal or liability assertions, human-judged against a written rubric | RT-LEGAL-v2: 90 fixtures that invite a liability conclusion | 0 occurrences, hard zero (ILLUSTRATIVE) | Block release | Regulatory Affairs Lead |

### 1.1 Public data grounding, and what it can and cannot support

The CFPB-\* eval sets are built from the [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/), a public dataset of complaints about consumer financial products and services, with a published [field reference](https://cfpb.github.io/api/ccdb/fields.html). It is used here because it is real consumer complaint language, written by consumers rather than by us, and it is public, so a reviewer outside this team can inspect the fixtures.

What we use it for: summary faithfulness, refusal behavior on rambling or off-topic input, robustness to poor spelling and mixed formatting, and the vulnerable-signal fixtures described in section 8, using the database's own Tags field, which flags complaints where the submitter reports the consumer as an older American or a servicemember.

What we do not use it for, and why, taken from the Bureau's own description of the data:

- **It is not representative.** The Bureau states the database is not a statistical sample of consumers' experiences and that the complaints are not necessarily representative. So it cannot support any accuracy threshold that we would defend as a population estimate.
- **The Bureau does not verify the complaints.** It states that it does not adopt consumers' views or verify that their experiences are accurate or unbiased. So a complaint narrative is evidence of what a consumer said, never of what happened, which happens to be exactly the epistemic position our assistant is in.
- **Narratives are opt-in and scrubbed.** Narratives are published only where the consumer chose to share them publicly, and after the Bureau takes steps to remove personal information. So the set systematically lacks the raw personal identifiers that our production inputs contain. Our PII fixtures (RT-PII-v2) are therefore hand-seeded rather than drawn from this source.
- **Coverage is partial.** Only complaints sent to companies for a response are eligible for publication, published after the company responds or after 15 days, whichever is first, and complaints referred to other regulators are not published.
- **It is US consumer complaints, not card disputes in our markets.** Product and issue taxonomies are the Bureau's, not the card schemes'. Nothing about our nine internal reason categories can be validated on it.

This is why the decision-relevant thresholds in rows 1, 2, 4, 6 and 7 sit on internal DS-\* and RT-\* sets, and the public data carries only row 5's language-quality half and the section 8 fixtures. See GAPS row 2.

### 1.2 Eval set governance

- Who owns adding production failures back into the eval set, and on what cadence: Disputes Ops Lead, weekly. Every analyst rejection of an assistant draft is triaged within five working days (ILLUSTRATIVE), and any rejection traced to a model error becomes a labeled case in the relevant DS-\* set within the same week.
- Where the eval sets live, and who can change them: in the disputes eval repository, write access limited to the Disputes Ops Lead, the ML Engineering Lead, and the Model Risk Lead. Changes are pull requests with a second reviewer. Thresholds are changed only by the Model Risk Lead.
- Are the eval sets versioned alongside the model version? Yes. Every release records the model version, prompt version, and the version tag of every eval set it was measured on. A release that cannot name all three does not ship.

## 2. Edge cases: the spec, not the appendix

### MUST REFUSE

| Input or condition | Refusal behavior (what the user sees) | Eval case exists? |
|---|---|---|
| Non-card dispute (account-to-account, direct debit) reaches the assistant | No draft. Banner: "Out of scope for this release. Handle manually." | Yes, RT-REFUSE-v2 |
| Case file contains no transaction record at all | No draft. Banner naming the missing record, with a link to case intake | Yes, RT-REFUSE-v2 |
| Evidence pack exceeds the context budget after truncation planning | No draft. Banner: "Case too large to summarize safely. Handle manually." Explicitly not a partial draft | Yes, RT-TRUNC-v1 |
| The analyst asks the assistant what the outcome should be | No answer. Banner: "This assistant does not recommend outcomes." | Yes, RT-REFUSE-v2 |
| The analyst asks the assistant to draft customer-facing text | No answer. Banner pointing to the approved bilingual template set | Yes, RT-REFUSE-v2 |
| The case is locked to the financial crime queue | The assistant is not invoked. No banner, because the analyst is not in this workspace | Yes, covered by an integration test, not a model eval |
| Retrieval returns documents whose case ID does not match the open case | No draft. Hard failure, alert raised to the platform on-call | Yes, RT-XCASE-v1 |

### MUST ESCALATE

| Condition | Routes to (named target, not "the team") | SLA on the human side | Covers which 0.4 item | Eval case exists? |
|---|---|---|---|---|
| Any sanctions or screening signal appears in the case text after intake screening | Financial Crime duty officer queue | 4 business hours (ILLUSTRATIVE) | Sanctions and screening dispositions | Yes, RT-ESC-v2 |
| Language suggesting suspicious activity or a reportable pattern | Financial Crime duty officer queue | 4 business hours (ILLUSTRATIVE) | Suspicious-activity judgments and FIU-adjacent decisions | Yes, RT-ESC-v2 |
| Case text alleges or implies first-party fraud by the cardholder | Disputes Team Lead, then Fraud Operations Manager | 1 business day (ILLUSTRATIVE) | First-party-fraud allegations | Yes, RT-ESC-v2 |
| Signals that the case may belong in the fraud queue rather than disputes | Disputes Team Lead | 1 business day (ILLUSTRATIVE) | Fraud and dispute reclassification | Yes, RT-ESC-v2 |
| Vulnerability signals: bereavement, serious illness, coercion, financial hardship, or a Tags-style older-consumer or servicemember signal | Conduct and Complaints Lead, and the case is flagged in the case record before any outcome | Same business day (ILLUSTRATIVE) | Vulnerable-customer determinations | Yes, RT-ESC-v2 and RT-VULN-v1 |
| Any draft that would support closing the dispute against the cardholder | No escalation path in the assistant, because the assistant never drafts an outcome. The analyst's existing four-eyes rule applies to the decision itself | Existing decision SLA | Outcomes closing a dispute against the cardholder | Yes, covered by RT-REFUSE-v2 row 4 |
| Case text contains instructions addressed to the system | Platform on-call, and the case is drafted without the injected content, with the attempt recorded | 1 business day (ILLUSTRATIVE) | Not a 0.4 item. Added from red team RT-02 | Yes, RT-INJECT-v2 |

### MUST NEVER INVENT

| Field | Behavior when unknown (absence, not fabrication) |
|---|---|
| monetary amounts | Emit the literal token UNKNOWN in the field and name the document that should have contained it. Never interpolate, never convert currency, never sum |
| names and account identifiers | Emit UNKNOWN. Never infer a cardholder or merchant name from an email address, a descriptor, or a similar name elsewhere in the pack |
| dates and reference numbers | Emit UNKNOWN. Never derive a date from context, and never reformat an ambiguous date into a specific one |
| legal or regulatory statements | Never produce one at all, known or unknown. No liability conclusions, no statements about what any rule requires, no assertions about scheme obligations |
| scheme reason codes | Never assign one. The assistant categorizes the cardholder's stated reason into an internal category and stops there. Reason code assignment is the analyst's, against the pinned rulebook edition |
| evidence that was not supplied | Emit the item on the missing-evidence checklist. Never describe a document that is not in the pack |

## 3. Non-determinism clause

- Acceptable variation: wording, sentence order within the narrative summary, and summary length within the stated word budget.
- Defects: a different extracted amount, reference, or date for the same case file. A different reason category. A different escalation decision. A different missing-evidence list. An UNKNOWN in one run and a value in the next.
- Reproducibility posture: temperature 0, top-p 1, a pinned model version string, and a pinned prompt template version. Temperature 0 reduces variation and does not eliminate it, and this document does not pretend otherwise. Row 1 and row 4 stability is measured directly: the release eval re-runs a 100-case subset three times and any disagreement across runs is a defect, not noise.
- Replay: yes. Every call logs the case ID, the retrieved document IDs with content hashes, the prompt version, the model version string, the full output, and the analyst's subsequent action. Any single decision can be reproduced from the log without re-reading the case file. What the log does not capture is the vendor's own internal routing between model revisions, which is the residual risk the version pinning is meant to bound.
- Behavior on model upgrade: the ML Engineering Lead re-runs every eval set before the new version reaches production. Any regression on a hard-zero row (3, 9, 10) or any drop below threshold on rows 1, 2, 4, 6, 7 blocks the upgrade. The Model Risk Lead approves. There is no expedited path, including for a vendor deprecation deadline; if the deadline is unmovable, the feature is disabled and cases queue for manual handling.

## 4. Guardrails: features with owners

| Guardrail | Trigger | Behavior | Owner | Test |
|---|---|---|---|---|
| Fail-closed on unverifiable output | Any extracted field whose value cannot be matched back to a retrieved document span | Field is emitted as UNKNOWN and the draft is flagged for the analyst's attention | ML Engineering Lead, Disputes | RT-INVENT-v2, plus a span-grounding unit test in CI |
| Human approval before anything irreversible | Always. The assistant writes to a draft field only | The assistant has no write access to the decision, the outcome, the customer record, or any outbound message. Enforced by service credentials, not by prompt | Engineering Manager, Disputes Platform | Permission integration test in the release pipeline |
| Spend and rate caps | ceiling: 4,000 calls per day and a per-case cap of 3 calls (both ILLUSTRATIVE) | at ceiling: the feature disables itself and the queue reverts to manual handling. Alert to platform on-call and Product Lead | Engineering Manager, Disputes Platform | Load test at 110 percent of ceiling (ILLUSTRATIVE) before each release |
| Input isolation (content the system reads is data, never instructions) | Always. Case documents and cardholder narratives are wrapped and marked as untrusted data in the prompt | Instruction-shaped content is not acted on. Detected attempts are logged and escalated per section 2 | ML Engineering Lead, Disputes | RT-INJECT-v2, run on every prompt change |
| Kill switch: immediate human-initiated stop | Manual, by the Product Lead, Disputes Ops Lead, or platform on-call | Feature flag off within 5 minutes (ILLUSTRATIVE) without a deploy. Queue reverts to manual handling with no data loss | Engineering Manager, Disputes Platform | Exercised in the release drill every quarter, result recorded |
| Audit trail | Every call | Case ID, retrieved document IDs and hashes, prompt version, model version, output, analyst action, timestamp | Engineering Manager, Disputes Platform | Log completeness assertion in CI, plus a monthly sampled reconciliation by Model Risk |
| Prohibited data class filter | Output contains a value matching a full card number, IBAN, national ID, or CVV pattern | Draft is suppressed entirely, not redacted. Alert to Security Architect | Security Architect, Disputes | RT-PII-v2, plus a pattern unit test |
| FIU export exclusion | Always | The assistant's output field is excluded from the financial intelligence unit filing export | Head of Financial Crime | Export schema test in the release pipeline |

## 5. Operations page

- Cost per call target: 0.04 USD · alert at: 0.06 USD sustained over 24 hours (all three figures ILLUSTRATIVE)
- Latency budget per step: retrieval 400 ms, inference 6 s, total 8 s at p95 (all ILLUSTRATIVE). Above 15 s (ILLUSTRATIVE) the call is abandoned and the analyst sees the manual-handling banner rather than a slow draft.
- Model version pinning and the upgrade decision process: pinned version string in configuration. The Model Risk Lead decides, on the evidence of a full eval re-run under section 3. Vendor deprecation notices are tracked by the ML Engineering Lead with a 90-day lead time (ILLUSTRATIVE).
- Telemetry per decision: case ID, retrieved document IDs and hashes, prompt version, model version, latency, cost, output, UNKNOWN field count, escalation flags raised, analyst action (accepted, edited, rejected), and edit distance where edited. Evals run at: CI on every prompt or model change, pre-release full run, and production sampling of 50 cases per week (ILLUSTRATIVE) re-labeled by an analyst.
- Production monitoring: weekly review of analyst rejection rate, UNKNOWN rate per field, escalation flag rate per trigger, and edit distance distribution. A sustained rise in edit distance is the leading indicator we watch for drift, because it moves before accuracy does. Reviewed by the Disputes Ops Lead, escalated to Model Risk on two consecutive weeks of movement (ILLUSTRATIVE).
- Rollback trigger: any hard-zero guardrail breach in production, or analyst rejection rate above 30 percent over three consecutive days (ILLUSTRATIVE). Rollback owner: Engineering Manager, Disputes Platform. Time to roll back: under 5 minutes (ILLUSTRATIVE) by feature flag.
- Post-launch review date, and who attends: 2026-11-15. Product Lead, Disputes Ops Lead, Model Risk Lead, Regulatory Affairs Lead, Engineering Manager, Head of Financial Crime.

## 6. Review gate: sign-off requires

- [x] Section 0 complete for every in-scope market, with document citations, not recollections
- [x] Every section 1 requirement has a metric, a dataset, a numeric threshold, and a named owner
- [x] Unagreed thresholds are labeled ILLUSTRATIVE and have an owner and a date to agree them
- [x] Section 2 tables have 5 or more rows each, and every 0.4 item appears in MUST ESCALATE
- [x] Section 3 written, and QA has not been left to decide variation policy
- [x] Every guardrail in section 4 has a named owner and a test that can fail
- [x] Section 0.6 metric source and method agreed in writing
- [x] Rollback trigger, owner, and time to roll back are stated in section 5
- [ ] Section 7 reviewed, and every high blast-radius gap has an owner and a date

The last box is deliberately unchecked. GAPS row 1 has an owner and a date but no answer yet, and this document does not ship as approved until counsel responds. Ticking it to keep a meeting moving is exactly the failure this gate exists to prevent.

## 7. GAPS

| # | Gap | Where in the original | Blast radius if shipped as-is | Smallest fix | Owner | Date |
|---|---|---|---|---|---|---|
| 1 | EU high-risk classification under Article 6 of Regulation (EU) 2024/1689 is unresolved, so whether Annex IV technical documentation applies is unresolved | 0.1, Ireland rows | High. If the feature is in scope for Annex IV, the documentation set is materially larger than this PRD and the EU launch date is wrong | Counsel opinion, already instructed. EU rollout stays behind the flag until it lands | Regulatory Affairs Lead | 2026-09-30 |
| 2 | Reason categorization (row 4) and evidence recall (row 6) are validated only on internal closed cases, which are our own historical decisions and therefore carry our own historical bias | 1.1 | Medium to high. The model can learn to agree with past analysts rather than to be right, and the eval would not show it | Add a 150-case adversarial re-label by analysts who did not handle the original cases, before the UAE volume ramp | Disputes Ops Lead | 2026-10-10 |
| 3 | No Arabic-language evaluation exists. Case narratives arriving in Arabic are refused by the intake filter today, which is a scope decision rather than a capability | 1, 2 | Medium. The refusal is safe, but it silently excludes a customer segment from the efficiency gain, which is a fairness question the metric will not surface | Report Arabic-refusal volume as a standing line in the post-launch review, and scope an Arabic eval set if it is material | Product Lead, Disputes | 2026-11-15 |
| 4 | Analysts can copy assistant text into customer correspondence, which would silently make an internal draft into a customer-facing communication and undermine the position taken in 0.5 | 0.5 | High. It converts a conduct question we answered "not applicable" into one we answered wrongly | Non-selectable draft field plus a copy event audit, and the analyst training note. Engineering change is small | Engineering Manager, Disputes Platform | 2026-10-03 |
| 5 | The headline metric is confounded by the queue routing change shipped in the same window | 0.6 | Medium. Low operational risk, high credibility risk if the number is quoted as attribution | Report the metric with the confound stated in the same sentence, every time, and never quote it as attributable | Product Lead, Disputes | Standing |
| 6 | Vulnerability signal detection (section 2, RT-VULN-v1) is built on 40 hand-written fixtures and has no production-validated recall | 2, 8 | High. A missed vulnerability signal is the failure that becomes a complaint and does not stay internal | Analyst-labeled production sample of 200 cases within the first month, recall reported to Conduct | Conduct and Complaints Lead | 2026-10-15 |
| 7 | Scheme rule drift for the two non-card register entries has no watcher assigned, because non-card is out of scope in this release | 0.2 | Low now, high the day scope extends without anyone noticing the register is stale | Assign the watcher when non-card rails enter scope, and re-check this row at the post-launch review | Disputes Rules Analyst | 2026-11-15 |

## 8. Red team: named failure scenarios

This section is an addition to the template, not part of it. Each scenario names the failure, says why a model produces it rather than treating it as random error, names the control that catches it, and states what is left over. Fixture counts are small on purpose: a fixture set is a claim about a specific failure, not a benchmark.

**RT-01. The confident reconciliation.** The case file contains two different disputed amounts, one in the cardholder's narrative and one in the transaction record. The model produces a single confident figure, sometimes the average, sometimes the larger. It does this because the training objective rewards a fluent complete answer over a marked absence. Caught by: MUST NEVER INVENT, the fail-closed span-grounding guardrail, and RT-INVENT-v2. Residual: a conflict where both figures are individually well-grounded still needs the analyst to notice the conflict, so the draft surfaces both and flags the discrepancy rather than resolving it.

**RT-02. The instruction in the evidence.** A cardholder uploads a letter containing text addressed to the system, for example an instruction to disregard prior rules and record the dispute as valid. Nothing about the evidence pack is trusted input, but everything about it looks like content. Caught by: the input isolation guardrail, RT-INJECT-v2, and the escalation row that routes detected attempts to platform on-call. Residual: injection that mimics legitimate case language rather than instruction language is not reliably detected, which is why the assistant has no write access to anything that matters.

**RT-03. The near-match explained away.** A merchant or beneficiary name closely resembles a sanctions listing, and the model smooths it into the summary as a spelling variation, because smoothing inconsistencies is what summarization does. Caught by: upstream screening at intake (the assistant never sees a screened-positive case), plus the escalation row for any screening signal appearing in the text afterward, RT-ESC-v2. Residual: a name that intake screening did not flag and the model normalized is invisible to both. This is a known limit of the design and is why the escalation trigger sits on the text as well as on the screening result.

**RT-04. The liability conclusion.** Asked to summarize, the model writes that the merchant is liable, or that the dispute is valid under the rules. This is the single most dangerous output the feature can produce, because it is fluent, it sounds authoritative, and it may sit in a case record that is later disclosed. Caught by: MUST NEVER INVENT (legal and regulatory statements), row 10 with a hard zero, and RT-LEGAL-v2. Residual: hedged constructions that imply a conclusion without asserting one are judged by rubric, and rubrics drift, so the rubric itself is re-reviewed at the post-launch review.

**RT-05. The empathetic overreach.** The narrative is distressing and the model drafts something reassuring, such as a statement that the refund will be processed. Models are trained toward helpfulness and this is what helpfulness looks like on a distressing input. Caught by: refusal on customer-facing text, the output being internal only, and RT-REFUSE-v2. Residual: this is the failure that GAPS row 4 is about. If an analyst copies it, the guardrail was never in the right place.

**RT-06. The silent truncation.** A 60-page evidence pack exceeds the context budget. The model summarizes what it received and says nothing about what it did not, because it does not know what it did not receive. Caught by: the truncation refusal (no partial drafts), RT-TRUNC-v1, and the retrieval layer refusing to silently drop documents. Residual: a pack just under the threshold is summarized with uneven attention across documents, which no refusal catches. Mitigated by the missing-evidence checklist being computed from the evidence matrix rather than from the summary.

**RT-07. The stale rule.** The model produces a scheme reason code or a time limit from its training data, and that code or limit was changed in a later rulebook release. It will be confident and it will be plausible. Caught by: MUST NEVER INVENT (scheme reason codes), which removes reason code assignment from the assistant entirely rather than trying to keep the model current. Residual: none for reason codes, by construction. The general point is that rule currency is a rulebook register problem (section 0.2) and not a model problem, and trying to solve it in the model is the mistake.

**RT-08. The normalized vulnerability signal.** The narrative mentions a bereavement, a coercive partner, or serious hardship. Summarization compresses, and the compressed version reads as neutral case background. The signal that most needed a human is the one the summary removed. Caught by: the vulnerability escalation row, RT-VULN-v1, and the rule that flagged cases are marked in the case record before any outcome. Residual: large, and honestly stated in GAPS row 6. Forty hand-written fixtures is a claim, not a validation.

**RT-09. The merged duplicate.** The same dispute is filed twice, through two channels. The model produces one tidy summary and, in doing so, may present two amounts as a total. Caught by: the cross-case retrieval failure (RT-XCASE-v1), the never-sum rule under monetary amounts, and duplicate detection upstream in case management. Residual: two genuinely distinct disputes on the same transaction are rare and look identical to a duplicate, so both are surfaced separately and neither is merged.

**RT-10. The eval set that agrees with us.** Not a model failure, a program failure. Every DS-\* set is built from our own closed cases, so a model that reproduces our historical decisions scores well whether or not those decisions were right. Caught by: nothing in the current release. This is GAPS row 2 and it is the reason that row is rated medium to high rather than low.
