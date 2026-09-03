---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["HR tech", "HRMS", "HCM", "hr-tech", "people tech"]
---
# HR technology

Every other domain's product decides what a customer buys. This one decides who gets hired, paid, promoted, scheduled and dismissed, which means a feature that ranks people is a regulated instrument in several jurisdictions and an employment lawsuit in the rest. The distinctive fact is that your customer carries the liability and cannot delegate it to you: an employer using your screening tool owns the discrimination exposure, and that asymmetry shapes what they will let you ship. The second distinctive fact is that the people your product acts on are not your users. Applicants, hourly workers and employees under review have no purchasing power and every reason to care, so a metric that pleases the administrator can be measuring harm.

## Questions a PM must ask

1. Does this feature rank, reject, recommend, promote, discipline, schedule, pay or monitor an identifiable person? If yes, it is a regulated instrument, and the rest of this card applies. If no, most of it does not.
2. Is the output decisive in practice, even where a human nominally approves it? The CJEU held in SCHUFA (C-634/21, 7 December 2023) that an upstream score can itself be the automated decision when the recipient draws strongly on it. A human who rubber-stamps is not a safeguard, and "human in the loop" as a label is not a control.
3. Where is the job, where does the person live, and which establishment employs them? Coverage turns on geography: New York City reaches remote roles tied to an NYC office, and Illinois reaches positions based in Illinois.
4. Can the customer produce the artifacts before the feature is enabled: bias audit, notice, consent, data protection impact assessment, works agreement, and a documented human review path? A signed contract is not permission to process employee data.
5. What is the target variable, and does it encode past managerial decisions rather than performance? A model trained on who was hired learns who was hired.
6. What happens when the model is wrong about a specific person, and how do they find out and contest it?
7. Is there a non-automated alternative and an accommodation path a disabled applicant can actually reach?
8. What does this look like in degraded mode? Payroll and time capture have no acceptable downtime, so the offline path is a requirement rather than a nicety.

## Gatekeepers

- **Employment and labour counsel.** Owns discrimination, wage-and-hour, notice and recordkeeping exposure that the employer cannot outsource to you. This is usually the role that stops a launch.
- **Works councils, where they exist.** In Germany, section 87(1)(6) of the Works Constitution Act gives co-determination over technical systems capable of monitoring conduct or performance, which catches most workforce analytics, timekeeping and scoring features. Absent agreement, a conciliation committee's award substitutes for consent. A customer can buy your software and still be unable to switch a module on.
- **Privacy officer or DPA.** GDPR Article 22 restricts decisions based solely on automated processing with legal or similarly significant effects, and hiring, firing, promotion and pay are the textbook examples. High-risk systematic evaluation normally needs an impact assessment before processing.
- **The NYC bias-audit regime.** Local Law 144 has been enforced since 5 July 2023: an independent bias audit no more than one year old, published selection rates and impact ratios including intersectional categories, and candidate notice generally ten business days before use. The auditor must have no financial interest in the employer or the vendor.
- **The EU AI Act.** Regulation (EU) 2024/1689 puts recruitment, selection, promotion, termination, task allocation and worker monitoring in Annex III as high-risk, with provider duties covering risk management, data governance, logging, human oversight, conformity assessment and registration. Workplace emotion inference has been prohibited since 2 February 2025. Profiling stays high-risk regardless of how narrow the task looks.
- **Payroll controller and finance.** Signs off the parallel run. Payroll errors are wage, tax and employee-relations exposure on the same day, so they will demand reconciled gross-to-net and a manual-pay fallback before go-live.
- **Accessibility and accommodations.** The EEOC's technical assistance of 12 May 2022 warns that an assessment can screen out a qualified person with a disability who could do the job with accommodation. An inaccessible assessment with no alternative is a blocked launch.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Adverse-impact ratio by group and intersection | Whether selection rates diverge across protected groups | The four-fifths threshold of 0.80 is an indicator, not a safe harbour. Small samples swing wildly, a ratio above the line can still be unlawful, and parity says nothing about whether the criterion is job-related |
| Time to fill | Recruiting throughput | Improves by choosing easy roles, lowering the bar, preselecting, or dropping the slow accommodation cases. Silent on retention and on quality of hire |
| Quality of hire | Whether the people you selected worked out | Circular and delayed. Manager ratings carry the same bias the model may have learned, and only the hired produce outcomes, so the sample is selected by the thing being measured |
| Review-cycle completion rate | Whether the performance cycle closed | Rewards rubber-stamping. A completed form is not a useful one, and forced distributions manufacture differentiation that did not exist |
| Payroll accuracy | Share of payslips without error | A high percentage still means many affected workers at scale, and it weights a rounding error the same as a missed wage. Pair it with severity, amount, and time to correct |
| On-time payroll | Statutory and contractual timeliness | A run can be on time and wrong, with the correction pushed to an off-cycle payment the metric never sees |
| Schedule fill rate | Whether shifts are covered | Improves through understaffing, unstable schedules, and pushing unpopular shifts onto the workers least able to refuse |
| Model accuracy or AUC | Predictive performance against historical labels | The labels are past decisions. A strong aggregate can hide poor subgroup calibration, and the labour market it was fitted to may no longer exist |
| Compliance completion | Share of customers with an audit, notice or assessment recorded | Measures paperwork. Local Law 144 requires the audit and does not require you to act on its result, so a completed audit is not evidence of non-discrimination |
| Override rate on automated recommendations | Whether human review is real | Near-zero means the reviewer is a formality; near-total means the model adds nothing. Neither extreme is a working control |

## Reading

- **NYC Department of Consumer and Worker Protection, automated employment decision tools** (the rule and its published FAQ, enforced from 5 July 2023). Read the FAQ rather than a summary: what counts as substantially assisting a discretionary decision is narrower than most vendors assume, and resume-bank search and candidate outreach fall outside it.
- **Regulation (EU) 2024/1689, the AI Act**, Annex III on employment and worker management, published 13 June 2024. Read Annex III and the provider obligations directly; the exemption for narrow procedural tasks does not survive profiling.
- **EEOC technical assistance on algorithms, software and the ADA**, 12 May 2022. Short, and the clearest statement of why an accommodation path is a product requirement rather than a support process.
- **Reuters on Amazon's scrapped recruiting model**, 10 October 2018. The canonical proxy-substitution story: removing gendered terms did not stop the model finding correlated signals. Reported rather than published as a technical account, which is itself worth noting about how much of this field's evidence exists only as journalism.
- **Mobley v. Workday** (N.D. Cal., filed 21 February 2023; agent-liability order 2024; ADEA collective preliminarily certified 16 May 2025). Live and undecided. It matters here because a court accepted that a vendor supplying screening can be treated as the employer's agent, which is the theory that puts a PM's design choices in front of a judge. Certification permits notice and discovery and is not a finding that discrimination occurred.
- **EEOC v. iTutorGroup**, consent decree 8 September 2023. A hard-coded age cut-off, not a model. Test the business rules and the configuration, not only the machine learning.
- **ICO enforcement against Serco Leisure**, 23 February 2024, on biometric attendance monitoring without a workable alternative. Consent given by an employee who has no other way to clock in is not freely given.

**Conductor overlay:** this domain sharpens DISCOVER-1 (the person affected is often not the buyer, so name both), DISCOVER-3 (evidence from applicants and hourly workers, who are the hardest population to reach and the one the product acts on), DEFINE-2 (the audience includes counsel, the works council and the accommodations team), and DELIVER-4 (go-live is gated on a parallel run and on artifacts the customer must hold, not on your readiness).

**Templates this bends:** [prd](../../templates/definition/prd.md) (section 10's four risks acquire a fifth in practice, which is whether the customer can lawfully switch the feature on), [eval-spec](../../templates/ai/eval-spec.md) (subgroup and intersectional slices are the acceptance criteria, not a fairness appendix), [human-approval-gates](../../templates/ai/human-approval-gates.md) (the override has to carry authority, time and source information, or it is decoration), and [release-readiness](../../templates/delivery/release-readiness.md) (the readiness table gains a row per jurisdiction the customer operates in).
