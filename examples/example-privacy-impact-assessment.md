# Privacy Impact Assessment: QuietPath Accommodation Check-in

Fills [templates/architecture/privacy-impact-assessment.md](../templates/architecture/privacy-impact-assessment.md). Everything here is invented: Northstar Works is a fictional software company, QuietPath is a fictional workplace check-in feature, the people are fictional reviewers, and every number and date is ILLUSTRATIVE.

**Owner:** Mira Solberg · **Date:** 2026-07-06 · **Status:** Signed
**DPO or privacy lead:** Anneliese Vogt · **Data model reviewed:** [data-model.md](../templates/architecture/data-model.md)

QuietPath is a small feature in Northstar Works' fictional employee scheduling product. It lets an employee privately record an accessibility or health-related accommodation need before a shift. A model groups the request into an operational category for a human workplace coordinator to review. The fictional product team is Mira Solberg, product owner; Tomas Nordin, security reviewer; and Anneliese Vogt, privacy lead. All people, company details and figures in this example are ILLUSTRATIVE.

## 1. Description of the processing

| Field | Value |
|---|---|
| Purpose, in one sentence | Help an employee communicate an accommodation need privately so a human workplace coordinator can arrange a suitable shift or work adjustment. |
| Whose data | Employees of customer organizations, including employees who disclose a health condition or disability-related accommodation need. No minors are in scope. |
| Scale | 12 customer organizations, 4 participating employees per organization per month, which is 12 x 4 = 48 subjects per month; records are retained for 3 months, so the maximum active subject record population is 48 x 3 = 144 records before deletion runs. |
| Where data comes from | Collected from the employee through a private form; a category is inferred by a model from the employee's free-text request; the coordinator records the action taken. |
| Who receives it | The employee's named workplace coordinator and a restricted Northstar Works support group when the employee opens a support case. The hosting provider and model processor receive only the fields required to provide the feature. The employee's line manager does not receive the free text or inferred category by default. |
| New technology or automated decisions | Yes. A language model proposes an operational category, such as schedule adjustment or workspace adjustment. It does not make the accommodation decision, notify a manager, or change a roster without human approval. The human approval gate for model-assisted personal-data processing is required before release. |
| Related assessments | The compliance impact assessment, signed by Priya Khatri on 2026-06-18, records “no statutory DPIA trigger identified” in section 4. This standalone PIA is a voluntary precautionary assessment because the feature profiles people and may process special-category data. It does not change that signed determination. No Harbourgate assessment or journey artifact is extended by this document. |

## 2. Data inventory

| Data category | Data subjects | Source | Purpose | Lawful basis (entered by counsel or DPO) | Special or sensitive category | Retention (from data-model.md) | Stored and processed where | Processors involved |
|---|---|---|---|---|---|---|---|---|
| Employee identifier and customer organization identifier | Employees | Collected from the employee and customer account | Route the request to the correct customer workspace and let the employee retrieve it | [basis to be entered by counsel or DPO] | no | 3 months after submission, then deletion | Northstar Works production environment in the European Economic Area | Fictional hosting provider, Northstar Cloud |
| Free-text accommodation request | Employees | Collected from the employee | Understand what workplace adjustment the employee is asking for | [basis to be entered by counsel or DPO] | yes, the text may reveal health or disability information | 3 months after submission, then deletion | Northstar Works production environment in the European Economic Area; model processing occurs in the same region | Fictional model processor, Oriole Models |
| Model-proposed operational category and confidence flag | Employees | Inferred by a model from the request | Give the human coordinator a suggested starting point without making the accommodation decision | [basis to be entered by counsel or DPO] | potentially yes, because the category can reveal an accommodation need | 3 months after submission, then deletion | Northstar Works production environment in the European Economic Area; no model training use | Oriole Models |
| Human review decision and action note | Employees | Recorded by the workplace coordinator | Record whether the request was handled, returned for clarification, or escalated | [basis to be entered by counsel or DPO] | potentially yes, where the action note describes the need | 3 months after the request is closed, then deletion | Northstar Works production environment in the European Economic Area | Northstar Cloud |
| Security and access logs | Employees and authorized staff | Observed by the application | Detect unauthorized access and investigate a support or security event | [basis to be entered by counsel or DPO] | no, logs contain identifiers and event metadata but not request text | 3 months from the log event, then deletion | Northstar Works logging environment in the European Economic Area | Northstar Cloud |

## 3. Necessity and proportionality

| Question | Answer | Evidence or owner |
|---|---|---|
| Could the purpose be achieved with less data, or with data that identifies no one? | Yes, the initial routing step can use an employee identifier and a broad operational category rather than a diagnosis or medical detail. The form tells the employee not to enter a diagnosis, treatment, medication, or medical record. The free-text field remains because a fixed list cannot cover every adjustment request, but the employee may submit a category without free text. | Mira Solberg owns the form design and the pre-submission warning. Tomas Nordin verifies that the model payload excludes unused account fields. |
| What is collected that the purpose does not need, and why is it kept? | A name, diagnosis, medical documentation, manager identity, and full employment history are not needed and are not collected. Free text is retained only because the coordinator needs the employee's own description when the category is insufficient. Model confidence is kept for review quality and is deleted with the request. | Mira Solberg owns the field inventory. The release checklist blocks new fields unless this PIA is updated. |
| How are subjects told what is collected and why, at the moment it happens? | The form shows a short notice before submission stating that the request, employee identifier, and model-proposed category will be shared with the named workplace coordinator for arranging an adjustment. It says that the model proposes a category and that a person makes the decision. A longer privacy notice is available from the same screen. | Anneliese Vogt reviews the short notice before release. The notice text and display event are retained in the product change record. |
| How does a subject see, correct, export, or delete their data, and how long does each take? | The employee can view the submitted request and proposed category in QuietPath, correct the request before a coordinator closes it, and export the displayed record from the feature. The employee can request deletion through the privacy contact shown in the notice. The product team acknowledges the request within the existing privacy operations process and executes deletion through the same deletion job that removes records after 3 months. | Anneliese Vogt owns the privacy contact and deletion procedure. Mira Solberg owns the in-product view, correction and export actions. |
| How does a subject object to, or opt out of, the processing? | The form offers a non-model route to contact the workplace coordinator. An employee can object to model categorization and ask for human-only handling. The coordinator can disable the model suggestion for that request without deleting the employee's message. | Mira Solberg owns the human-only route. The support runbook records the employee's choice without recording a reason. |
| How is accuracy maintained, especially for anything a model inferred? | The model output is labelled “suggestion,” is never shown as a fact about the employee, and cannot trigger a roster change. The coordinator must confirm, change, or reject the category before acting. The employee can correct the request and the category. The model version and suggestion are logged so a wrong suggestion can be investigated. | Tomas Nordin owns model version logging. The workplace coordinator owns the substantive accuracy decision. |
| Who can access the data, and how is access logged and reviewed? | Only the named workplace coordinator for the customer workspace, the employee who submitted the request, and a restricted support group with an approved case can access request content. Product engineers receive redacted diagnostics only. Every content access is logged with actor, purpose and record identifier. Anneliese Vogt reviews the access report monthly. | Tomas Nordin owns role permissions and access logging. Anneliese Vogt owns the monthly review. |
| How long is data kept, and what executes deletion when the period ends? | Request content, model output, action notes and related access records are kept for 3 months. A scheduled deletion job removes the content and identifiers at the end of that period. Failed deletion jobs create an alert for the privacy lead and cannot be silently dismissed. | Tomas Nordin owns the deletion job and failure alert. Anneliese Vogt verifies the first deletion run before release. |
| Which international transfers happen, and under what mechanism? | None are planned. Production data and model processing remain in the European Economic Area. A new processor, region, or support route outside that area requires a new transfer review and an update to this PIA before use. | Anneliese Vogt owns the transfer review. Tomas Nordin blocks processor configuration outside the approved region. |

## 4. Consultation

| Consulted | Date | What they raised | What changed as a result |
|---|---|---|---|
| DPO or privacy lead, Anneliese Vogt | 2026-07-06 | The signed compliance impact assessment records “no statutory DPIA trigger identified” in section 4, but the feature still warrants a documented privacy review because free text may reveal health or disability information and the model profiles the request. | The team kept this standalone PIA as a precautionary design record. It does not restate the compliance determination as “required.” The model is limited to a suggestion and the human-only route is mandatory. |
| Security, Tomas Nordin | 2026-07-06 | A coordinator must not see requests outside the assigned customer workspace, and support access must not become a general troubleshooting permission. | Workspace-scoped authorization, purpose-recorded support access, redacted diagnostics and monthly access review were added as release conditions. |
| Data subjects or their representatives, fictional employee advisory group led by Leena Saar | 2026-07-06 | Employees may not want to disclose a diagnosis, may not trust a model category, and may need to correct a request without explaining why. | The form now discourages diagnosis and medical detail, offers category-only submission, labels the model output as a suggestion, and provides human-only handling plus correction. |
| Processors, fictional Northstar Cloud and Oriole Models | 2026-07-06 | The model processor must not retain prompts for training, and neither processor should receive unused customer or employee fields. | The payload is allow-listed, model training use is disabled, the processing region is restricted to the European Economic Area, and processor configuration changes require a new review. |

## 5. Risks to individuals

Likelihood and severity use the illustrative 1 to 5 scales in the [Risk matrix worksheet](../frameworks/execution/risk-matrix.md). The score is likelihood x severity. A score of 12 or more is treated here as requiring a named mitigation owner and explicit DPO approval.

| Id | Risk to the individual | How it could happen | Likelihood | Severity | Score | Source |
|---|---|---|---:|---:|---:|---|
| PR-1 | An employee's health or disability information is disclosed to a manager or colleague who does not need it. | A coordinator forwards the free text, a workspace permission is mis-scoped, or a support user opens the request without an approved case. | 3 of 5 | 5 of 5 | 3 x 5 = 15 | Privacy and access review, 2026-07-06 |
| PR-2 | An employee is denied or delayed an appropriate accommodation because the model proposes the wrong category. | The coordinator treats the suggestion as a decision, does not read the free text, or the employee cannot correct the result. | 3 of 5 | 5 of 5 | 3 x 5 = 15 | Model-assisted workflow review, 2026-07-06 |
| PR-3 | An employee is discouraged from requesting an accommodation because the notice or workflow makes the model appear mandatory. | The employee believes they must provide sensitive detail or accept the model category to submit a request. | 3 of 5 | 4 of 5 | 3 x 4 = 12 | Employee advisory group, 2026-07-06 |
| PR-4 | Sensitive request content remains available after the employee expects it to be deleted. | The scheduled deletion job fails, deletes the main record but leaves a copy in logs, or a processor retains a prompt. | 2 of 5 | 5 of 5 | 2 x 5 = 10 | Retention and processor review, 2026-07-06 |
| PR-5 | An employee cannot exercise access, correction, objection, or deletion rights because the request cannot be reliably found or exported. | The request is indexed only by an internal identifier or the privacy contact cannot connect the request to the employee's record. | 2 of 5 | 4 of 5 | 2 x 4 = 8 | Rights handling review, 2026-07-06 |

## 6. Mitigations

| Risk id | Measure | Effect (eliminated / reduced / accepted) | Residual score | Owner | In place by | Approved by DPO |
|---|---|---|---:|---|---|---|
| PR-1 | Enforce customer-workspace and role-scoped access; exclude managers by default; require a support case for support access; log every content access; review the access report monthly. | reduced | Likelihood 1 of 5 x severity 5 of 5 = 5 | Tomas Nordin | 2026-07-06 | Yes, Anneliese Vogt |
| PR-2 | Label the output as a suggestion; require the coordinator to confirm, change, or reject it; block automatic roster or notification changes; provide human-only handling and employee correction. | reduced | Likelihood 1 of 5 x severity 5 of 5 = 5 | Mira Solberg | 2026-07-06 | Yes, Anneliese Vogt |
| PR-3 | Make category-only submission available; tell the employee not to provide diagnosis or medical detail; show that model use is optional; provide a human-only route and correction action. | reduced | Likelihood 1 of 5 x severity 4 of 5 = 4 | Mira Solberg | 2026-07-06 | Yes, Anneliese Vogt |
| PR-4 | Use a 3-month deletion job for content, identifiers and access records; disable model training retention; alert on failed deletion; test processor deletion during release review. | reduced | Likelihood 1 of 5 x severity 5 of 5 = 5 | Tomas Nordin | 2026-07-06 | Yes, Anneliese Vogt |
| PR-5 | Provide an in-product view and export; use the employee identifier and customer workspace to locate the record; route privacy requests to Anneliese Vogt; test correction and deletion with a fictional record before release. | reduced | Likelihood 1 of 5 x severity 4 of 5 = 4 | Anneliese Vogt | 2026-07-06 | Yes, Anneliese Vogt |

## 7. Sign-off

| Role | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| DPO or privacy lead | Anneliese Vogt | accepted with conditions | The compliance impact assessment, signed by Priya Khatri on 2026-06-18, remains the source for whether a DPIA is required and records “no statutory DPIA trigger identified.” QuietPath may proceed only with the human approval step, human-only route, workspace-scoped access, 3-month deletion, European Economic Area processing, and processor no-training setting described here. A new data category, processor, market, processing region or model decision requires review before release. | 2026-07-06 |
| Product owner | Mira Solberg | accepted with conditions | Release is blocked until the employee notice, category-only submission, correction, export, objection and human-only route are visible in the product and tested. | 2026-07-06 |
| Security reviewer | Tomas Nordin | accepted with conditions | Release is blocked until workspace authorization, access logging, deletion failure alerting, redacted diagnostics and processor region controls pass the security review. | 2026-07-06 |

**Next review:** New data category, new processor, new market, new processing region, model change, automated decision, or any request to share content with a manager; otherwise review at the next scheduled product privacy review.

## Exit gate (feeds Gate 3: architecture and risks reviewed)

A signed assessment supports the PII and retention line at Gate 3, feeds risk rows into the risk register, and is re-confirmed under the regulated overlay at Gate 5.

- [x] Every data category has a purpose, a retention period copied from the data model, and a lawful basis entered by counsel or the DPO, or a named owner and date for it. Each row names the DPO as the person to enter the basis, and the DPO condition is recorded in section 7.
- [x] Every necessity question is answered with a mechanism or an owner, none with a bare yes. Section 3 names product controls, security controls, privacy operations and owners.
- [x] The DPO was consulted, and the consultation row records what changed. Anneliese Vogt's 2026-07-06 consultation records the standalone rationale and the added conditions.
- [x] Every risk is phrased as harm to a person, scored on the risk matrix scales, and has a mitigation row. PR-1 to PR-5 each show likelihood x severity arithmetic and a matching mitigation.
- [x] The ILLUSTRATIVE example rows have been deleted; a signed assessment carrying invented personal-data content is worse than an unsigned one. The template's fictional expense row is not carried into this assessment.
- [x] Every accepted residual risk above the named band has an owner and a risk register row. No residual score is above the illustrative threshold of 12, and each residual score has a named owner in section 6.
- [x] The DPO's verdict is recorded by name and date, with conditions written out. Anneliese Vogt accepted with conditions on 2026-07-06.
- [x] Signed by Anneliese Vogt, 2026-07-06
