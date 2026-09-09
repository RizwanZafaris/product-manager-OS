---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Public sector", "GovTech", "government technology", "civic tech", "public-sector-govtech"]
---
# Public sector and GovTech

A government product's users did not choose it and often cannot choose an alternative. Renewing a passport, claiming a benefit, or paying a local tax has exactly one supplier, which inverts the usual product logic: you cannot lose a user to churn, so the pressure that keeps most digital products honest is missing, and something else, statute, audit, and a free press, has to supply it instead. Failure here is public by design. A broken checkout costs a company revenue quietly; a broken benefits system makes the evening news.

The second distinctive fact is that the buyer, the builder, and the person the system acts on are three different parties who rarely sit in the same room. Procurement rules decide who may build it, a service standard decides whether it is good enough to launch, and the citizen discovers whether it works only when they have no other option left.

## Questions a PM must ask

1. Who cannot use a digital-only version of this service, and what is their path? Digital exclusion is not an edge case here; it is a population, and a service standard usually makes an assisted channel mandatory.
2. Which procurement route governs this build, and what does it allow you to change once a contract is signed? A procurement framework can lock a technical decision in place for years before anyone touches a keyboard.
3. Does this meet the accessibility standard the law actually requires, commonly WCAG at the AA level, tested with real assistive technology rather than only an automated scanner? A high automated pass rate is not evidence a screen-reader user can complete the task.
4. What is the retention and disposal schedule for the records this system creates, and who decided it? Records law, not your database defaults, decides what must be kept, for how long, and what must eventually be destroyed.
5. Can a request under freedom-of-information or right-to-information law be answered from what this system stores, inside the statutory clock? A system unable to produce or redact its own records on demand has built a liability, not a feature.
6. If this system verifies identity, what happens to the person who cannot pass the check: no documents, no smartphone, no fixed address? That failure case is usually the most vulnerable user, not the rare one.
7. Who owns this politically, and what happens to the program if they are no longer in post? Public programs can be cancelled by an election result that has nothing to do with delivery quality.
8. What is the plan if this fails on the one day everyone needs it: a payment deadline, a renewal cutoff, a benefit payday? Peak-day failure in a government service is a front-page event, not an incident review.

## Gatekeepers

- **The procurement authority.** Regimes such as the EU's public procurement directives, or a national equivalent, decide who may bid and on what terms, and give losing bidders a formal right to challenge an award; a challenge can freeze a program for months.
- **Accessibility auditors and service assessors.** The UK's Government Digital Service runs service assessments against a published standard; many governments require conformance with WCAG under a law such as the EU's Web Accessibility Directive or the equivalent in your own jurisdiction.
- **The national records or archives authority.** Statutory retention and disposal schedules override whatever your team finds convenient, and a records authority can compel transfer of material your team considered internal.
- **The information commissioner or right-to-information authority.** A freedom-of-information regime means your data model has to support disclosure and redaction on a legal clock, not just retrieval for your own dashboards.
- **The data-protection authority.** A government system routinely holds data on an entire population who never opted in and cannot opt out, a different risk shape than a company's customer base.
- **Legislative and audit oversight.** A parliamentary committee or national audit office can end a program publicly over cost or delivery risk, on a political timetable that ignores your sprint plan entirely.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Digital take-up rate | Share of users on the digital channel | Can rise because a phone line was deliberately removed, not because the digital service earned the shift |
| Service completion rate | Whether the digital journey works | Excludes everyone who never attempted the digital path over access or trust, flattering exactly the population already served |
| Cost per transaction | Efficiency of the service | Falls when an uncounted cost, a citizen's time, travel, or printing, quietly rises instead |
| Accessibility conformance (automated scan pass rate) | Technical accessibility coverage | Automated tools catch a minority of real barriers; a page can pass every check and still be unusable with a screen reader |
| Freedom-of-information response time | Statutory disclosure performance | A holding response or a valid exemption stops the clock without answering anything |
| Identity-verification success rate | Whether the identity check works | A high pass rate can mean lax checks, or that people without the required documents were excluded before they ever reached the count |
| Procurement cycle time | Speed to contract | A fast award followed by a legal challenge and re-tender is slower than a careful one, and the clock usually stops at signature, not at working software |
| Uptime during peak demand | Reliability when it counts | An annual average hides the one outage that happened on the single day everyone needed the service |
| Assisted-channel volume | Demand for human help | A falling number can mean self-service improved, or that people gave up and the need went unmet entirely |

## Reading

- **The EU Web Accessibility Directive**, Directive (EU) 2016/2102, and WCAG at the AA level as the standard it points to. Read the exceptions list; it is shorter than most teams assume.
- **US Section 508** of the Rehabilitation Act, the American federal accessibility baseline, useful even outside the US as a second, differently worded version of the same requirements.
- **The UK Government Digital Service Service Standard** and its published service-assessment reports. Read a failed assessment before a passed one; it names the traps more precisely.
- **The eIDAS Regulation**, (EU) 910/2014, and its recent update establishing a European Digital Identity Wallet (verify the current rollout timeline before relying on it), the reference for cross-border digital identity built as a legal framework rather than a login screen.
- **The UK and US Freedom of Information Acts** (1966 for the US, 2000 for the UK), the baseline for what "the public can ask for this" means, and how differently two systems answer it.
- **The UK NHS National Programme for IT**, dismantled after years of delay and cost overrun (verify specific figures before relying on them), the canonical lesson that a single national platform can fail from scale and governance alone, independent of the underlying technology.

**Conductor overlay:** this domain sharpens DEFINE-2 (audience includes political oversight and a population that never opted in), DESIGN-3 (where PII lives becomes population-scale identity data with no consent step), DELIVER-6 (regulated overlay drift, as accessibility and records duties change under a live service), and OPERATE-9 (the kill condition is often a budget or election cycle, not a metric).

**Templates this bends:** [accessibility-checklist](../../templates/architecture/accessibility-checklist.md) (WCAG conformance tested with assistive technology, not only automated scans), [privacy-impact-assessment](../../templates/architecture/privacy-impact-assessment.md) (population-scale data with no opt-out), [stakeholder-map](../../templates/execution/stakeholder-map.md) (political owners and oversight bodies alongside delivery stakeholders), and [release-readiness](../../templates/delivery/release-readiness.md) (accessibility and assisted-channel readiness as go or no-go rows).
