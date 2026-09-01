# PRD: [feature name]

<!-- Regulated AI PRD template, v1.
     Fill every field, or write "N/A because <reason>". A blank field is a decision
     deferred to whoever finds it blank, and "N/A" on its own is a blank with a hat on.

     Structure: section 0 is the regulated overlay (0.1 to 0.6) and is answered BEFORE
     any requirement is written. Sections 1 to 7 are the PRD proper. Appendix A maps
     these sections to the v1 overlay instruments and is reference material, not a
     section you fill in.

     Check completeness with:  python3 lint.py <this-file-once-filled>.md          -->

**Feature:** [one sentence: what the system does, and for whom]
**Markets in scope:** [list each market. Every section below is answered PER MARKET where they differ]
**Implementer type:** [LLM feature / agent / copilot / ML decision]
**Document owner:** [name] · **Regulatory owner:** [name] · **Engineering owner:** [name]
**Status:** Draft / In review / Approved · **Version:** [n] · **Document date:** [YYYY-MM-DD]
**Regulatory references verified as of:** 2026-09-01

---

## What this document is for

This is a question contract between the product owner and the second line.

Every section below is a question the second line, compliance, risk, or internal audit will ask before this feature ships. Answered here, in writing, with a document citation and a name, each one costs a paragraph. Answered in the launch review, each one costs a launch date. Answered nowhere, each one gets decided later by whoever hits it first: a QA engineer filing a bug, an ops agent inventing a workaround, or a customer complaint that arrives with a regulator's reference number attached.

The contract has four terms.

1. **No requirement without a number.** A "should" that cannot be turned into an eval set with a threshold is not a requirement yet. It goes in section 7 as a gap, not in section 1 as a commitment.
2. **No control without an owner and a test.** A guardrail with neither is a sentence. Gates that cannot fail are ceremonies.
3. **No precondition deferred.** Section 0 is answered before section 1 is written, because a license condition beats a sprint plan every time.
4. **No unowned gap.** Anything still unknown at sign-off is a row in section 7 with a name and a date against it. Unknowns are acceptable. Unowned unknowns are not.

---

## 0. Regulated overlay: answer BEFORE writing requirements

<!-- Generic PRD tooling starts at section 1. In a regulated feature the document earns
     its keep here. See Appendix A for what the v1 overlay instruments ask for. -->

### 0.1 Regulatory precondition register

| Market | License condition, approval, or notification that gates this feature | Regulator | Confirmed how (a document, not a conversation) | Confirmed date | Owner |
|---|---|---|---|---|---|
| | | | | | |

<!-- "We believe it is fine" is not a row. A row cites a rulebook section, a license
     condition, or the regulator's written response, and names who holds that document. -->

### 0.2 Scheme-rule constraints

| Rule area touched (authorization, tokenization, disputes, data) | Scheme and rule or bulletin reference | Version pinned at spec time | Who watches the quarterly releases for drift |
|---|---|---|---|
| | | | |

<!-- Scheme rulebooks are licensed documents. Cite the reference and the version you
     read; do not paste the text into this PRD. -->

### 0.3 Data residency and model-vendor terms

- Data classes in the flow, and where each is stored and processed: [table or list, per market]
- Cross-border transfer basis where applicable: [mechanism, per market]
- Model vendor terms verified: does the provider train on our inputs? [yes or no, plus the contract clause reference]
- Vendor audit and information rights secured in contract: [clause reference, or "no" plus the gap row in section 7]
- Retention period per record class, per applicable requirement: [list]
- Model and prompt version pinning: is the exact model version pinned, and who approves a change? [name]

### 0.4 Financial-crime touchpoints

- Screening points in the flow (AML, CTF, sanctions), and what happens on a hit: [where, and the behavior]
- Decisions the AI may NEVER make alone. Every item here becomes a MUST ESCALATE row in section 2: sanctions dispositions, suspicious-activity judgments, [add others]
- Does any output of this feature enter a regulatory report or filing? If yes, name the report and its owner: [report, name]

### 0.5 Customer-communication conduct

- Is any AI output shown to customers a regulated communication in any in-scope market? [answer per market]
- Is the customer told an AI system is involved, and where in the journey? [answer per market]
- Languages the customer-facing output must support, and who signs off the translation: [list, name]
- Can the customer request a human review of an AI-influenced outcome, and by what route? [route, SLA]
- If any output is customer-facing: the approval workflow for generated content, and the owner of that workflow: [name]

### 0.6 The metric that survives an audit

<!-- Agree this now, not in the launch review. A headline number whose method was never
     written down is a number that will be withdrawn under questioning. -->

- Headline success metric: [metric]
- Source system and calculation method, agreed in writing with: [data owner, date]
- Where a third party could independently verify it: [system or report]
- What this metric is NOT evidence of: [the overclaim you are refusing to make]

---

## 1. Acceptance criteria: eval sets, not sentences

<!-- Every threshold in a document that has not yet been agreed with the metric owner
     is ILLUSTRATIVE and must say so. An unlabeled number gets quoted back at you. -->

| # | Requirement (was a "should") | Metric | Eval set or dataset (labeled cases, min 30 to 50 for v1) | Pass threshold (a number) | Below threshold | Failing-case owner |
|---|---|---|---|---|---|---|
| 1 | | | | | block release | |

<!-- Anything that cannot be turned into an eval is not a requirement yet. Put it in
     section 7 GAPS. The lint gate requires metric, dataset, threshold, below-threshold
     action, and owner on every row; requires the threshold to contain a digit; and
     requires the threshold to say ILLUSTRATIVE or to cite the agreement that set it,
     as "per <agreement> dated YYYY-MM-DD". -->

**Eval set governance**

- Who owns adding production failures back into the eval set, and on what cadence: [name, cadence]
- Where the eval sets live, and who can change them: [location, access rule]
- Are the eval sets versioned alongside the model version? [yes or no]

## 2. Edge cases: the spec, not the appendix

The happy path is what the model does for free. This document earns its keep at the boundaries.

### MUST REFUSE (minimum 5 rows)

| Input or condition | Refusal behavior (what the user sees) | Eval case exists? |
|---|---|---|
| | | |

### MUST ESCALATE (minimum 5 rows, and every section 0.4 item appears here)

| Condition | Routes to (named target, not "the team") | SLA on the human side | Covers which 0.4 item | Eval case exists? |
|---|---|---|---|---|
| | | | | |

### MUST NEVER INVENT

| Field | Behavior when unknown (absence, not fabrication) |
|---|---|
| monetary amounts | |
| names and account identifiers | |
| dates and reference numbers | |
| legal or regulatory statements | |
| [add] | |

## 3. Non-determinism clause

The same input can produce a different output tomorrow. If this document does not say what that means, QA will decide it later, in a bug tracker, angrily.

- Acceptable variation: [wording? ordering? formatting? length?]
- Defects: [a different decision / a different number / different refusal behavior / a changed escalation]
- Reproducibility posture: [temperature and seed policy]
- Replay: do the logs capture enough (input, retrieved context, model version, prompt version, output) to reproduce any single decision on request? [yes or no, plus what is missing]
- Behavior on model upgrade: [who re-runs the eval sets, what result blocks the upgrade]

## 4. Guardrails: features with owners

| Guardrail | Trigger | Behavior | Owner | Test |
|---|---|---|---|---|
| Fail-closed on unverifiable output | | | | |
| Human approval before anything irreversible (payments, sends, deletions, filings) | | | | |
| Spend and rate caps | ceiling: [n] | at ceiling: [behavior] | | |
| Input isolation (content the system reads is data, never instructions) | | | | |
| Kill switch: immediate human-initiated stop of the deployed feature | | | | |
| Audit trail (who or what decided, on which inputs, at which model version) | | | | |
| [add] | | | | |

## 5. Operations page

- Cost per call target: [n] · alert at: [n]
- Latency budget per step: [n]
- Model version pinning and the upgrade decision process: [who decides, on what evidence]
- Telemetry per decision: [fields logged] · Evals run at: [CI / pre-release / production sampling, and sample rate]
- Production monitoring: [what is watched for drift, by whom, at what frequency]
- Rollback trigger: [condition] · Rollback owner: [name] · Time to roll back: [n]
- Post-launch review date, and who attends: [date, names]

## 6. Review gate: sign-off requires

<!-- The artifact is approved when every box is checkable, not when the meeting ends.
     Leave a box unchecked and carry it as a section 7 gap rather than ticking it to be
     polite. The lint gate checks these boxes are PRESENT; only a human can honestly
     check one. -->

- [ ] Section 0 complete for every in-scope market, with document citations, not recollections
- [ ] Every section 1 requirement has a metric, a dataset, a numeric threshold, and a named owner
- [ ] Unagreed thresholds are labeled ILLUSTRATIVE and have an owner and a date to agree them
- [ ] Section 2 tables have 5 or more rows each, and every 0.4 item appears in MUST ESCALATE
- [ ] Section 3 written, and QA has not been left to decide variation policy
- [ ] Every guardrail in section 4 has a named owner and a test that can fail
- [ ] Section 0.6 metric source and method agreed in writing
- [ ] Rollback trigger, owner, and time to roll back are stated in section 5
- [ ] Section 7 reviewed, and every high blast-radius gap has an owner and a date

## 7. GAPS

<!-- The one page a reviewer reads first. Rank by blast radius, not by ease of fixing. -->

| # | Gap | Where in the original | Blast radius if shipped as-is | Smallest fix | Owner | Date |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

---

## Appendix A. Regulator mapping, v1 overlay

Reference material, not a section to fill in. The v1 overlay covers two instruments and no others. Both were read against primary text on **2026-09-01**.

**How to read this table.** It says what each instrument expects or asks for, and which section of this template is where you write your answer. It does not tell you what your answer should be, and it is not a statement that any institution falls short of anything. Applying these expectations to your entity, license class, and market is your second line's judgment and your counsel's, not this template's.

**Instrument 1.** CBUAE Guidance Note on the Consumer Protection and Responsible Adoption and Use of Artificial Intelligence and Machine Learning by Licensed Financial Institutions in the U.A.E., **issued 11 February 2026** (the CBUAE announced it by press release on 23 February 2026). Text: [CBUAE Rulebook](https://rulebook.centralbank.ae/en/rulebook/guidance-note-consumer-protection-and-responsible-adoption-and-use-artificial-intelligence). The note states that it supplements and does not replace laws, regulations, or directives, and it directs readers to the CBUAE [Model Management Standards](https://rulebook.centralbank.ae/en/node/4881) and the [Consumer Protection Regulation](https://rulebook.centralbank.ae/en/node/2757). Its defined term **High-impact decision** means a determination by a licensed financial institution using AI that materially affects a customer's access to financial products or services. Read it as what it is: a guidance note phrased in "should" language, supplementing rather than replacing the law and regulation already in force. Completing section 0 of this template is not compliance with it, and the binding obligations sit in the instruments it points back to.

**Instrument 2.** EU AI Act, Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024, published at OJ L, 2024/1689, 12.7.2024. **Annex IV** is titled "Technical documentation referred to in Article 11(1)". Text: [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689). Annex IV applies to high-risk AI systems through Article 11(1); whether a given feature is in that class is a scoping question this template does not answer for you.

| Template section | What the instrument expects or asks for | Reference |
|---|---|---|
| 0.1, and the owner fields in the header | The note expects a documented AI and ML governance framework proportionate to the size, nature, and complexity of operations, with senior management and the board accountable for AI systems and outcomes | CBUAE Guidance Note (11 Feb 2026), section 2(a), 2(b) |
| 0.1 | The note expects an inventory of all AI models developed or deployed, holding at minimum model name, purpose, and risk rating, including third-party hosted models | CBUAE Guidance Note (11 Feb 2026), section 2(f), 9(c) |
| 0.3 | The note expects policies ensuring models use accurate, relevant, up-to-date data with clear provenance and audit trails, and compliance with rules on data being retained in the country | CBUAE Guidance Note (11 Feb 2026), section 5(a), 5(c) |
| 0.3 | Annex IV asks for the training data sets used, including their provenance, scope, and main characteristics, how the data was obtained and selected, and the labeling and cleaning procedures | EU AI Act Annex IV, point 2(d) |
| 0.3 (vendor terms) | The note expects due diligence on third-party AI and cloud providers, and contract provisions securing access to information, audit rights, and compliance with CBUAE requirements | CBUAE Guidance Note (11 Feb 2026), section 9(a) |
| 0.4 | The note expects institutions to assess and, where feasible, use AI to identify potential fraud, criminal activity, money-laundering issues, and suspicious activity, and to comply with their reporting requirements where material findings arise | CBUAE Guidance Note (11 Feb 2026), section 5(e) |
| 0.5 | The note expects transparency with customers about the use of AI, particularly for high-impact decisions and when the customer is interacting with an AI application, with plain-language disclosures in both Arabic and English and telephone support in all major languages of the UAE | CBUAE Guidance Note (11 Feb 2026), section 4(a), 4(b) |
| 0.5 | The note expects institutions to consider opt-out rights for customers, particularly for high-impact decisions, taking account of risk, fairness, and feasibility | CBUAE Guidance Note (11 Feb 2026), section 4(c) |
| 0.6, 1 | Annex IV asks for the validation and testing procedures used, the validation and testing data and its main characteristics, and the metrics used to measure accuracy and robustness, with dated and signed test logs and reports | EU AI Act Annex IV, point 2(g) |
| 0.6 | Annex IV asks for a description of the appropriateness of the performance metrics for the specific AI system | EU AI Act Annex IV, point 4 |
| 1, 4 | The note expects periodic testing, at least annually and on every upgrade, material change, or new model, to identify and remediate unintended bias or discriminatory outcomes | CBUAE Guidance Note (11 Feb 2026), section 3(c) |
| 2 (MUST ESCALATE) | The note expects meaningful human oversight and judgment, sets out human-in-the-loop, human-on-the-loop, and human-out-of-the-loop models, and states that human-out-of-the-loop should be used only for low-risk, non-material processes with appropriate controls | CBUAE Guidance Note (11 Feb 2026), section 7(a) |
| 2 (MUST ESCALATE), 0.5 | The note expects consumers to be able to request human review or an explanation of AI-generated decisions, with alternative arrangements available, and clear channels for complaints and redress | CBUAE Guidance Note (11 Feb 2026), section 7(c) |
| 2, 4 | Annex IV asks for an assessment of the human oversight measures needed under Article 14, including the technical measures that help deployers interpret the system's outputs | EU AI Act Annex IV, point 2(e) |
| 4 (kill switch) | The note expects institutions to retain the clear and immediate ability, with human intervention, to cease use of any deployed AI model, system, technology, or application | CBUAE Guidance Note (11 Feb 2026), section 6(f) |
| 4, 7 | Annex IV asks for a detailed description of the risk management system under Article 9 | EU AI Act Annex IV, point 5 |
| 5 | The note expects continuous monitoring of AI for reliability, relevance, and alignment with consumer protection objectives, testing of automatic updates before implementation, and mechanisms to detect, report, and remediate performance issues and bias over time | CBUAE Guidance Note (11 Feb 2026), section 6(a), 6(c), 6(d) |
| 5 | Annex IV asks for the system in place to evaluate performance in the post-market phase under Article 72, including the post-market monitoring plan referred to in Article 72(3) | EU AI Act Annex IV, point 9 |
| 5 (telemetry), 3 (replay) | Annex IV asks for detailed information about the monitoring, functioning, and control of the system, its capabilities and limitations in performance, foreseeable unintended outcomes, and specifications on input data | EU AI Act Annex IV, point 3 |
| Header (feature, markets, implementer type) | Annex IV asks for a general description of the system including its intended purpose, the provider, and the version | EU AI Act Annex IV, point 1(a) |
| 3 (non-determinism clause) | Neither instrument addresses output variance directly. This section is this template's own requirement, and it exists because the absence is what causes the argument after launch | No instrument reference |

**Out of scope in v1.** Other GCC regulators, the FCA and PRA, MAS, US federal and state requirements, PCI DSS, DORA, GDPR beyond what Annex IV itself references, and card scheme rulebooks. Section 0.2 asks you to pin the scheme rule and version yourself.
