---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Pharma and life sciences", "pharmaceutical technology", "life sciences", "pharma-life-sciences"]
---
# Pharma and life sciences

This is not about a patient using an app; [healthtech](healthtech.md) is the primary read when the user is a patient or prescriber. This card covers the systems that produce and control a medicine before it reaches anyone: clinical trial data capture, the signal-detection systems that watch a drug after approval, and the manufacturing and quality systems that decide whether a batch may ship. The distinctive fact is that software is regulated as part of the process it supports, whether or not it makes any medical claim of its own; a database storing a trial's case report forms inherits the validation, audit-trail, and signature obligations of the regulated activity around it. The second distinctive fact is that change is the trigger: a validated system that gets modified is, by definition, no longer proven to be in that state, which is why "minor update" has no safe version here. The EU's GMP Annex 11 on computerised systems and the US FDA's 21 CFR Part 11 cover close to the same ground but are not identical texts, and a system validated against one needs an explicit gap check against the other, not an assumption.

## Questions a PM must ask

1. Is this system used to produce, store, or sign off on a GxP record, a trial record, a pharmacovigilance case, a batch record, or a quality-system document? If yes, it is a regulated computerised system for validation purposes, whatever else it also is.
2. What validated state does this system need to hold, and what proves it stayed there after this specific change ships? Validation is evidence work, planned before the change, not reconstructed after an inspection asks for it.
3. Does the audit trail capture who changed what, when, and why, and is it actually immutable rather than merely inconvenient to edit? Inspectors test this by trying to break it, not by reading the design document.
4. For a clinical trial system: does it meet ICH E6 Good Clinical Practice expectations for data integrity, and can source data be reconstructed years later against what the sponsor eventually files?
5. For a pharmacovigilance system: what is the adverse-event intake-to-report clock, and does the system enforce it or only log it? Expedited-reporting timelines are fixed by regulation, and a missed clock is a compliance finding, not a bug ticket.
6. If a model triages any output here, signal detection, adverse-event coding, batch-anomaly flags, who is the accountable reviewer, and can its reasoning be reconstructed for an inspector? An unexplainable model inside a GxP process is a validation gap wearing a feature.
7. What is the change-control and deviation process, and does the release cadence fit inside it? A weekly deploy cadence built for SaaS collides with a quality system expecting an approved change request per production change.
8. Who is the Qualified Person, or equivalent accountable signatory, and does the system produce what they need to certify a batch or a trial dataset? That person owns the acceptance criteria more than any internal stakeholder does.

## Gatekeepers

- **21 CFR Part 11 (US FDA), electronic records and signatures.** Sets the bar for when an electronic record may substitute for paper: validation, audit trails, and retention are conditions, and an inspector who cannot trust the audit trail can reject the record set it supports.
- **EU GMP Annex 11, computerised systems.** The EU's parallel framework; close to Part 11 but not identical, and a claim of compliance with one still needs a documented gap check against the other.
- **ICH E6 Good Clinical Practice (R2, and the R3 revision as it enters force in different regions).** Governs data integrity and source documentation for trial systems, checked by inspectors from multiple regulators regardless of sponsor headquarters (verify which revision applies in your target regions before relying).
- **National medicines regulators and their GMP inspectorates.** Inspect manufacturing and quality systems directly, can issue a Form 483 or equivalent finding, and can hold a batch or a facility.
- **The Qualified Person (EU) or equivalent accountable role.** A named individual personally certifies that a batch meets its marketing authorization before release; the system has to produce exactly what that person needs, on their terms.
- **Pharmacovigilance authorities and their expedited-reporting clocks.** Post-marketing safety timelines are fixed and enforced separately from the marketing-authorization process; a case-intake tool that misses the clock creates its own finding, independent of the drug's actual safety.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Validation deviation rate | Whether change control is holding | A low rate can mean rigor, or it can mean deviations are resolved informally and never logged |
| Audit-trail completeness | Data-integrity health | Complete does not mean immutable; a trail a privileged user can edit without a trace passes completeness and fails inspection |
| Case-intake to regulatory-report cycle time | Pharmacovigilance clock compliance | An average hides the tail: the cases that missed the expedited deadline are the ones the regulator cares about |
| Batch release cycle time | Manufacturing throughput | Improves by deferring quality investigations into a backlog that has not closed, surfacing later as a much larger release delay |
| CAPA closure rate | Whether quality issues actually get fixed | A high rate with recurring root causes means CAPAs close procedurally; track repeat-root-cause rate alongside it |
| Source data verification match rate | Whether trial data reflects what happened to the patient | Sampling-based SDV can look clean while the fields inspectors care most about were undersampled |
| Uptime for GxP-critical systems | Operational reliability | Uptime with an unlogged manual workaround during an outage is worse than honest downtime; the workaround is the unvalidated path an inspector asks about |
| Training-record completion rate | Whether users are qualified on a validated system | Module completion is not evidence of competence, and both Part 11 and Annex 11 inspections probe this gap directly |
| Model-flagged signal review turnaround | Whether automation accelerates safety review | Fast turnaround with a high undocumented-override rate means reviewers are rubber-stamping the model, a worse posture than a slower manual process |

## Reading

- **21 CFR Part 11**, alongside FDA's guidance on Computer Software Assurance as a risk-based evolution of traditional validation (verify current guidance status before relying).
- **EU GMP, Annex 11.** Read side by side with Part 11 rather than assuming one covers the other; risk-assessment and supplier-qualification expectations differ in emphasis.
- **ICH E6(R2) Good Clinical Practice**, and, where in force in your target regions, the E6(R3) revision (verify which revision applies before relying on specific provisions).
- **A published FDA Form 483 or warning letter concerning data integrity** in manufacturing or a clinical trial. Reading one closely teaches more about what "audit trail" means in practice than any internal policy.
- **The WHO's guidance on data integrity for regulated systems**, a globally referenced framework many emerging-market regulators lean on where their own detailed rules are thinner.
- **A published account of a drug-safety signal that pharmacovigilance systems caught late.** The failure is almost always in case triage and escalation timing, not the absence of raw safety data.

**Conductor overlay:** this domain sharpens DEFINE-8 (overlays: a model that triages adverse-event signals or flags manufacturing anomalies activates the AI overlay, and the regulated overlay as well wherever a financial or data regulator applies to it, per the rule in [os/STAGE-GATES.md](../../os/STAGE-GATES.md); where it fires, its preconditions freeze at Gate 2), BUILD-1 (criteria demonstrated: validation protocol execution records, IQ/OQ/PQ or their risk-based equivalent, are the acceptance evidence, not a passing test suite alone), BUILD-3 (failure rehearsal: a deviation and CAPA path has to be exercised, dated, and shown to close), and DELIVER-6 (regulated overlay drift: any change to a validated system requires the validated-state answers to be re-verified before release, which is revalidation in the Conductor's own language).

**Templates this bends:** [eval-spec](../../templates/ai/eval-spec.md) (a signal-detection model's thresholds are validation acceptance criteria reviewed by the accountable signatory, not a data-science metric alone), [testing-strategy](../../templates/delivery/testing-strategy.md) (validation protocol execution replaces generic test-pass reporting), [failure-scenarios](../../templates/delivery/failure-scenarios.md) (deviations and CAPAs are failure scenarios with a regulatory clock on closure), [release-readiness](../../templates/delivery/release-readiness.md) (a revalidation line gates release whenever the validated system changed), and [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (Part 11, Annex 11, and GCP rows sit beside the privacy rows).

**Filled in this repo:** [domain-pharma-life-sciences-eval-spec.md](../../examples/domain-pharma-life-sciences-eval-spec.md) fills the [eval-spec](../../templates/ai/eval-spec.md) template directly for this domain, for Sentinel at Ostrava Biosciences: a sensitivity slice held at or above 0.98 on the labelled validation set, error analysis on missed serious cases, a scenario set covering seriousness criteria, expedited 15-day cases under 21 CFR 314.80 and ICH E2D, non-English narratives and duplicates, a golden set labelled by two qualified safety physicians with adjudication, and a release gate requiring FDA Computer Software Assurance validation evidence and 21 CFR Part 11 audit trails with a named clinician signatory. For the other four bent templates, [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md) and [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md) remain the nearest reading for the GO WITH CONDITIONS and automated-decision-question shapes. testing-strategy and failure-scenarios have no filled example in the repository yet for this domain; check examples/README.md before assuming a link is dead.

**Worked example (ILLUSTRATIVE):** a slice of [eval-spec](../../templates/ai/eval-spec.md), the template this domain bends hardest, for a fictional pharmacovigilance triage model, Sentinel, at a fictional biotech, Ostrava Biosciences. Every name, number, and date is invented.

| Field | Entry |
|---|---|
| Model | Sentinel v2.3, adverse-event case triage: routes cases to expedited or standard review |
| Validated use | Triage only; the expedited-reporting determination is made and signed by the accountable Pharmacovigilance Physician, never by the model |
| Acceptance criterion | Sensitivity of at least 0.98 on the labeled validation set for cases meeting expedited-reporting criteria (fewer than 1 in 50 missed), reviewed and signed by the QPPV before go-live, not by the model team alone |
| Evidence required | IQ/OQ/PQ execution records, not an offline data-science metric alone; the validation run must reproduce on the production environment, dated and archived |
| Override logging | Every reviewer override of a Sentinel flag captured with a reason code and reviewer ID, feeding the undocumented-override rate this card's metrics table warns against |
| Revalidation trigger | Any retrain, feature change, or threshold change requires this acceptance criterion re-run and re-signed before the new version may triage a live case; "patch to fix a bug" is not exempt |
| Status | [OPEN: Sentinel v2.3 acceptance run scheduled 2026-11-03; owner Priyamvada Rao, QPPV] |
