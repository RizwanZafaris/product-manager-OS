---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Manufacturing", "Industrial software", "OT", "MES", "manufacturing-industrial"]
---
# Manufacturing and industrial

A plant runs on two networks that were never meant to talk to each other: an IT network built to be patched constantly, and an operational-technology network built to run unchanged for twenty years because the equipment on it controls something that can hurt someone. The distinctive fact of this domain is that connecting them, exactly what a modern MES or analytics platform wants to do, turns a security boundary into a product requirement. The segmentation model has to be a design decision, not an afterthought bolted on before an audit.

The second distinctive fact is that a safety-rated system does not get a normal deploy. A change to software that performs or influences a safety function requires documented revalidation under a recognized functional-safety standard, on a timeline set by an assessor, not a sprint. Traceability follows the same logic: a customer or a regulator will eventually ask for the full genealogy of one unit, and the answer has to exist before the question is asked.

## Questions a PM must ask

1. Does this feature sit inside, or communicate with, a safety-rated function? If so, a change here needs documented revalidation, not a standard release process.
2. Which side of the OT and IT boundary does this feature live on, and what segmentation model governs the connection between them? A single unreviewed data pull from the plant floor can undo years of segmentation discipline.
3. Can this system produce full genealogy for one unit, one lot, or one batch on demand? A traceability system nobody has tested against a real recall request does not really exist yet.
4. What is the change-control and validation path for a software update to equipment on the line, and how long does it actually take? A validated process treats an update as a change requiring sign-off, not a deploy.
5. What quality standard does the customer or the market require, and does this feature touch anything that standard's audit will ask about? A customer's own audit can be stricter than any regulator's.
6. What happens to the line when this system fails: does the process stop safely, or continue on stale data? A fail-open industrial system is a hazard, not an inconvenience.
7. Who is accountable if this software contributes to a product defect that reaches a customer? Product-liability regimes increasingly treat software the same as a physical part.
8. What monitoring exists on the OT network, and would an intrusion actually be seen? A segmented network with no monitoring reports zero incidents because it cannot see any.

## Gatekeepers

- **The machinery or functional-safety certifying body.** A notified body under a machinery safety regime, or a national equivalent, can require re-certification for a change to a safety function, including one implemented purely in software.
- **OT security and plant IT.** Network segmentation and change control under a recognized industrial-control-system security standard give this function the standing to refuse a connection between an analytics layer and a control network, however useful the integration seems.
- **Quality management and quality assurance.** Certification audits against a management-systems standard gate whether nonconformances get caught before they leave the plant, and the audit record is what gets asked for after a defect.
- **National workplace-safety regulators.** A national safety regulator can stop a line for an unsafe condition regardless of production targets or a release date.
- **Large customers' own traceability requirements.** Automotive, aerospace, and pharmaceutical customers impose inbound traceability standards, lot codes, and certificates of conformance contractually, on top of anything a regulator requires.
- **Product-liability counsel and insurers.** An updated EU product-liability regime brings software explicitly into scope, so a defect in plant software can now sit at the center of a liability claim rather than beside it.
- **The change-control or configuration-management board on the floor.** In validated manufacturing environments, a software update is a documented change requiring revalidation, and this board decides when the line may restart.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Overall Equipment Effectiveness | Combined availability, performance, and quality | Multiplies three ratios together, so a plant can improve the number by reclassifying planned downtime without shipping one extra unit |
| First-pass yield | Process quality without rework | An off-line rework loop can be excluded from the count, so a part that fails and is fixed later never shows as a failure |
| Scrap rate / defects per million opportunities | Output quality | Sampling-based inspection undercounts whatever the sampling plan itself has a known blind spot for |
| Unplanned downtime on OT or control systems | Line availability | Downtime attributed to operator error instead of a system root cause hides a design or software problem that will recur |
| Mean time to detect an OT security event | Security visibility | A segmented network with no monitoring reports zero incidents because it has no way to see one |
| Traceability query time | Recall readiness | A fast answer on a well-instrumented line says nothing about the manual, paper-backed process on an older line in the same plant |
| Validation cycle time for a safety-rated change | Change-control discipline | Teams learn to route a change through a faster path meant for non-safety configuration, to avoid the slower, correct one |
| Time to contain a defect once found | Containment speed | Time to notify internally is not time to contain in the field; inventory already shipped is the real exposure |
| Cost of quality (prevention, appraisal, failure) | Where quality spend goes | Spending more on appraisal, meaning inspection, can improve the ratio while process capability has not changed at all |

## Reading

- **The ISA/IEC 62443 series**, security for industrial automation and control systems, the reference for what a zone-and-conduit segmentation model actually has to contain.
- **IEC 61508**, functional safety of electrical, electronic, and programmable electronic safety-related systems, the parent standard behind most machine-specific safety standards on a plant floor.
- **ANSI/ISA-95**, enterprise-control system integration, the standard defining where an MES ends and an ERP begins, and therefore where your integration actually has to be built.
- **The EU Machinery Regulation**, replacing the older Machinery Directive and, notably, explicitly covering safety functions performed by software (verify the exact application date before relying on it).
- **The EU's modernized Product Liability Directive**, bringing software and AI-caused defects within the scope of product liability (verify the transposition timeline in your market before relying on it).
- **Stuxnet**, discovered in 2010, the standing lesson that a control system can be attacked without the corporate network its operators trusted as the perimeter ever being touched.
- **The Triton (Trisis) malware**, discovered in 2017, which targeted a plant's safety instrumented system directly, the case that moved OT security from protecting the process to protecting the thing that protects people.

**Conductor overlay:** this domain sharpens DESIGN-2 (integrations are the MES-to-ERP boundary and the OT and IT segmentation model, both gatekept), DEFINE-3 (reversibility is limited: a safety-rated change needs revalidation before it can go live or be rolled back), BUILD-6 (what the red team broke on the OT side matters as much as the application layer), and DELIVER-6 (regulated overlay drift, as machinery and product-liability rules update under a running plant).

**Templates this bends:** [security-architecture](../../templates/architecture/security-architecture.md) (OT and IT segmentation as a named zone-and-conduit model), [change-request](../../templates/execution/change-request.md) (validated change control for safety-rated software), [incident-postmortem](../../templates/operate/incident-postmortem.md) (containment time and field exposure as required fields), and [nfr](../../templates/definition/nfr.md) (safety-rated and traceability requirements stated as numbered thresholds).
