---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Regtech", "AML", "KYC", "regtech-aml-kyc"]
---
# Regtech, AML and KYC

This product sells risk reduction to a customer who cannot delegate the underlying legal duty to you, the same asymmetry hr-tech carries for employment law: your bank or fintech customer's compliance officer signs the suspicious activity report, not you, and a false negative your model produces becomes their regulatory finding while you are not in the room for the consequence. That asymmetry shapes this domain's demo-versus-production gap: a screening tool sells on precision and is judged in production on whether an alert-drowned analyst team can still defend a decision.

The second distinctive fact is that "effective" is not a fixed spec your product satisfies once. It is whatever a supervisory exam decides in hindsight, against typologies that evolve faster than any release cycle, so a rule library compliant last year can be this year's finding with no code change on your side. The third is that a country's own status can become every one of its banks' product requirements overnight: Pakistan sat on the FATF grey list from June 2018 to October 2022. FATF's own increased-monitoring statement says it does not call for enhanced due diligence and asks for a risk-based approach, but correspondent banks set their own appetite, and for that period many applied enhanced measures, repriced, or withdrew from Pakistani counterparties, which landed on product roadmaps that had scheduled none of it.

## Questions a PM must ask

1. Who signs the suspicious activity report, and what does that person need from your case-management tool to defend the decision later? The tool serves a signature, not a dashboard.
2. What is your list-refresh latency for sanctions and PEP data, and is it measured against the publisher's own update cadence? A stale list is a compliance failure on its own, independent of match quality.
3. What happens to alert volume when a threshold is tightened, and has anyone modeled the analyst capacity required to review it? A tuning change that improves precision on paper and buries the team in practice has made detection worse.
4. How is a closed alert's reasoning captured, in enough detail that an examiner sampling it months later can follow the decision? An alert closed with no narrative is a finding waiting to be sampled.
5. What tier of due diligence does this product apply at onboarding, and is it justified by an actual risk-based assessment or just by transaction size? A risk-based approach requires the reasoning written down, not just the outcome.
6. Where does the case file live once data crosses into a different country's financial intelligence unit? Cross-border residency questions attach the moment a case escalates, not only at onboarding.
7. What is the false-negative risk behind a falling false-positive rate? Every threshold tightened to reduce noise also reduces sensitivity, and the miss you do not see is the one that matters.
8. Does a model score or triage any alert here, and has that been checked against [the regulated module](../../modules/regulated/README.md) rather than treated as a plain detection feature? A model deciding who gets escalated is a different question from one that only ranks a list.

## Gatekeepers

- **The customer's Money Laundering Reporting Officer or BSA Officer.** The named individual who owns the filing decision and can be held personally accountable for it; your product's value is entirely in what it hands this person.
- **The national Financial Intelligence Unit (FIU).** FinCEN in the US, Pakistan's Financial Monitoring Unit under its AML law, and national FIUs feeding the Egmont Group network elsewhere. They define the filing taxonomy your case management must produce, and never see your product directly.
- **The prudential or AML supervisor running the exam.** Defines "effective" retroactively by sampling closed cases, and a consent order can name remediation your product must now support, on its own timeline.
- **The sanctions and PEP list publishers.** OFAC's SDN list, the UN Consolidated List, the EU's list, and national equivalents each update independently; your screening product's real SLA is refresh latency, not matching cleverness.
- **Correspondent banks in the payment chain.** Can impose their own enhanced due diligence demands on your customer as the price of keeping the account open, and Pakistan's 2018 to 2022 grey-list period is the clearest recent example of that pressure arriving system-wide.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Alerts generated per analyst | Workload and coverage | Rises with a noisier model and reads as thorough monitoring while degrading the quality of every individual review |
| Alert-to-filing conversion rate | Whether alerts translate into real filings | A low rate can mean good tuning or an overwhelmed team closing everything to clear a backlog, and the two look the same on a chart |
| False-positive rate | Screening precision | Improves by narrowing match thresholds, which quietly raises the false-negative rate the dashboard never shows |
| Average alert age or backlog size | Whether review is keeping pace | A healthy average can hide a handful of aged, high-risk alerts past the filing deadline, exactly what an exam samples for |
| Filing timeliness | Whether reports go out on the statutory clock | Can be met by filing thin, boilerplate narratives on time rather than well-investigated ones late, and a regulator judges narrative quality, not just the clock |
| Screening coverage | Share of customers or transactions actually screened | Quoted against the "monitored population" rather than the total customer base, hiding whoever was never screened at all |
| List-refresh latency | Currency of sanctions and PEP data | A same-day average can still mean one source lagged a week without anyone noticing until an examiner asks for evidence |
| Case reopen rate | Whether closures were correct the first time | A near-zero rate looks like quality and can just mean nobody is reauditing closed cases at all |
| Cost per alert resolved | Operational efficiency | Falls as thresholds loosen and volume drops, the same lever that can quietly increase false negatives |
| Enhanced due diligence completion rate | Depth of review where it matters most | A completed EDD form is not the same as one that changed the onboarding decision; the metric counts paperwork, not judgment |

## Reading

- **The FATF 40 Recommendations, especially Recommendation 10 on customer due diligence and Recommendation 16 on the travel rule.** The standard nearly every national AML law implements in its own words; read the source before a vendor's paraphrase.
- **FATF's grey-list and black-list process, and Pakistan's listing from June 2018 to October 2022.** Read for how a sovereign designation becomes a product requirement for every bank in that corridor, instantly and without a release cycle.
- **FinCEN's Customer Due Diligence Final Rule, finalized 2016, compliance date 2018.** Sets the 25 percent beneficial-ownership threshold shaping onboarding logic across most AML products, US-built or not.
- **The Wolfsberg Group's AML Principles and its Correspondent Banking Due Diligence Questionnaire.** What major banks actually ask each other and their vendors; closer to the real procurement bar than most public regulation text.
- **Basel Committee guidance on the sound management of risks related to money laundering and terrorist financing.** Read for the supervisory expectations layered on top of the FATF standard for prudentially regulated banks.
- **AUSTRAC v. Westpac Banking Corporation, settled with a civil penalty in September 2020 (verify the exact amount before relying).** Read for how a monitoring gap, not a single failure, becomes a penalty sized by the count of contraventions.

**Conductor overlay:** this domain sharpens DEFINE-2 (the audience for the case file is the MLRO who signs, not the analyst who clicks close), DEFINE-5 (a requirement fails here as a missed typology or a stale list, not a generic defect class), DESIGN-3 (PEP and case data crossing an FIU boundary is a residency question with a named destination), and OPERATE-8 (the counter-metric behind a falling false-positive rate is the false-negative risk nobody tracks on the same dashboard).

**Templates this bends:** [business-rules](../../templates/definition/business-rules.md) (typology rules are the business rules, versioned and auditable the way code is), [nfr](../../templates/definition/nfr.md) (list-refresh latency is a hard requirement with an examiner behind it, not a target), [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (cross-border data sharing with an FIU triggers this before a feature ships), and [decision-log](../../templates/execution/decision-log.md) (every threshold-tuning change needs a decision an examiner can sample later, with a name attached).

**Filled in this repo:** [domain-regtech-aml-kyc-business-rules.md](../../examples/domain-regtech-aml-kyc-business-rules.md) fills the [business-rules](../../templates/definition/business-rules.md) template directly for this domain, for Beacon at Fernhollow Trust: a structuring typology threshold, a sanctions fuzzy-match threshold, a PEP enhanced-due-diligence trigger, and a ban on auto-closing alerts above a risk score, held by the MLRO, with below-the-line testing and MLRO approval required for any threshold change and a logged change history an examiner can sample. For the other three bent templates, [harbourgate-nfr.md](../../examples/harbourgate-nfr.md), [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) and [sahulat-decision-log.md](../../examples/sahulat-decision-log.md) remain the nearest reading for revision-log, automated-decision, and indexed-entry shapes, though none carries an AML typology, an FIU data share, or a threshold-tuning entry.

**Worked example (ILLUSTRATIVE):** a slice of [business-rules](../../templates/definition/business-rules.md) for a fictional AML screening product, Beacon, used by a fictional bank, Fernhollow Trust. Every name, number, and date is invented.

| ID | Rule statement (WHEN...THEN...) | Trigger point | Source of truth | Business owner | Exceptions | Test traceability |
|---|---|---|---|---|---|---|
| BR-014 | WHEN a customer's transaction volume exceeds 3x their onboarding-declared range in a rolling 30 days THEN generate an alert and freeze the risk tier at "enhanced" until an analyst closes it with a narrative | Nightly monitoring batch | Fernhollow Trust AML typology library v9, held by the MLRO | Farrukh Aslam, MLRO | None on the 3x threshold itself; a documented seasonal-business list (BR-014-EXC) suppresses the alert for the 40 pre-approved merchant accounts on it, reviewed quarterly | AC-22 |

**Threshold change log (feeds decision-log):** 3x was 5x until 2026-06-02, tightened under decision D-041 after an examiner's finding on missed structuring cases; alert volume rose 38 percent the following week, logged against analyst capacity in the same decision entry so a later examiner can sample the reasoning, not just the outcome.
