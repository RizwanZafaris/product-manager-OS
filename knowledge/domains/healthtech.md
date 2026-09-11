---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Healthtech"]
---
# Healthtech

One question sorts everything in this domain: what is the product's intended use? Intended use, the claim you make about what the software does for a patient or clinician, decides whether you built an app or a medical device, which regulator owns you, what evidence you must produce, and how fast you may ship. The second sorting question is who pays, because in healthcare the user (a patient), the decider (a clinician), and the payer (an insurer, employer, or health system) are almost never the same party, and products that delight users while ignoring payers die solvent-user-rich.

**Adjacent industries:** consumer fitness, sleep, meditation and wellness products read this card mainly for its boundary. The PM's standing job is keeping the product on the general-wellness side of the medical-device line under FDA's general wellness policy, which binds marketing copy and AI coaching as much as features. HIPAA usually does not apply, but consumer health-data law does: the FTC Health Breach Notification Rule and state laws such as Washington's My Health My Data Act. Subscriptions fall under state automatic-renewal laws (the FTC's click-to-cancel rule was vacated in 2025), and connected equipment reads [Hardware and IoT](hardware-iot.md). Elder and home-care software reads this card with three additions: Electronic Visit Verification is federally required for Medicaid personal-care and home-health visits under the 21st Century Cures Act; Medicaid waiver billing sets the revenue model; and the payer, the decider (often an adult child) and the user (an older adult, sometimes with reduced capacity) are three people, so proxy access and consent are design problems. Fall detection and remote monitoring sit on the device-classification line again. As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. What is the intended use, in one sentence a regulator would read? Wellness support and diagnosis are different products under the same UI; the sentence decides whether FDA (or an EU notified body under MDR) is in your loop.
2. If it is software as a medical device: which risk class? The IMDRF SaMD framework grades on how serious the condition is and how much the output drives clinical action; the class sets the evidence burden and the pathway (in the US: 510(k), De Novo, or PMA).
3. What clinical evidence will we produce, against what endpoints, and who signs off that the endpoints are the ones clinicians and payers accept? Engagement is not an endpoint; a changed clinical outcome is.
4. Where does PHI flow? Every party touching protected health information needs its HIPAA role defined (covered entity or business associate) and a BAA in place before the first byte, and the equivalent mapping under GDPR for EU patients.
5. How does this fit the clinician's workflow, measured in seconds? A tool that adds clicks to a fifteen-minute appointment will be routed around no matter what it prevents. EHR integration via HL7 FHIR is usually the difference between used and demoed.
6. Who pays, through what mechanism: a reimbursement code, a health-system contract, an employer benefit, or the patient? The mechanism dictates the sales cycle, the evidence bar, and the pricing model.
7. What is the adverse-event story? If the product can be involved in patient harm, who detects it, who reports it, to whom, and on what clock?
8. What happens when the model or the guidance is wrong, and did a clinician help write that answer?

## Gatekeepers

- **Medical device regulators.** FDA in the US, notified bodies under the EU MDR; they gate claims, changes, and marketing, and a "minor" model update can be a regulated change.
- **Privacy enforcement.** HIPAA (enforced by OCR) for US health data, GDPR for EU patients; both reach vendors through contracts, not just hospitals.
- **IRBs and clinical review.** Any study producing your evidence runs through institutional review; timelines are theirs, not yours.
- **Health-system procurement and clinical champions.** Hospital IT security review, integration committees, and the named clinician who vouches internally; without the champion, the committee has no reason to say yes.
- **Payers.** Coverage and coding decisions gate the revenue model; their evidence standards are often stricter than the regulator's.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Clinical endpoint movement | Whether the product does what it claims medically | Surrogate endpoints and unblinded measurement flatter it; pre-register what counts |
| Engagement tied to efficacy | Whether usage produces the outcome, not just sessions | Engagement alone is the domain's most seductive vanity metric |
| Clinician adoption and time-in-workflow | Whether the tool survives contact with a real clinic day | Pilot-site enthusiasm rarely transfers; measure at the skeptical site |
| Integration depth (FHIR live, not planned) | Whether you are in the workflow or beside it | A roadmap slide counts for nothing here |
| Reimbursement rate / contract renewals | Whether the payer mechanism actually pays | Lags everything else by quarters; instrument it anyway |
| Adverse events and near-misses | Safety in operation | Silence can mean safe or unmeasured; only one is acceptable |

## Reading

- **The Digital Doctor**, Robert Wachter (2015). The definitive account of why health IT that demos well fails at the bedside: alert fatigue, workflow mismatch, and the gap between data entered for billing and data useful for care. Its case study of a hundredfold pediatric overdose caused by a chain of reasonable-looking interface decisions should be required reading before any healthtech UI review.
- **Deep Medicine**, Eric Topol (2019). The optimistic counterweight, from a clinician: where machine assistance genuinely helps, and the standing warning that every claimed benefit must clear clinical-grade evidence, not app-store-grade evidence.

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: patient, clinician, and payer are three answers), DEFINE-8 (overlays: the data-regulator half is a yes for anything touching PHI, so the regulated overlay turns on the model half alone and fires only where a model is present; the narrowed rule is in [os/STAGE-GATES.md](../../os/STAGE-GATES.md)), DESIGN-3 (where PII lives becomes where PHI lives, with BAAs), and DELIVER-2 (UAT includes clinical validation, not just functional passes).

**Templates this bends:** [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (PHI categories, BAA rows, device-classification record) and [uat-plan](../../templates/delivery/uat-plan.md) (clinician testers, clinical scenarios, and sign-off from a medical owner).

**Filled in this repo:** [domain-healthtech-compliance-impact-assessment.md](../../examples/domain-healthtech-compliance-impact-assessment.md) fills the [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) template directly for this domain, for Cobaltine Health Companion: an honest intended-use self-assessment against the FDA device software function and clinical decision support guidance, the four non-device CDS criteria from 21st Century Cures section 3060, IMDRF risk categories, a HIPAA applicability test, the FTC Health Breach Notification Rule, Washington's My Health My Data Act, a flagged DPIA, and classification left open with regulatory counsel, since 'does not diagnose' in marketing copy does not settle intended use. No filled example in this repository exercises [uat-plan](../../templates/delivery/uat-plan.md) at all; no clinician-tester row or medical sign-off signature appears anywhere in the repository yet.

**Worked example (ILLUSTRATIVE):** a filled compliance-impact-assessment answer for a fictional symptom-triage app, "Cobaltine Health Companion," following the [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) shape used in [harbourgate-compliance-impact-assessment.md](../../examples/harbourgate-compliance-impact-assessment.md):

**Section 1, product and data summary, intended-use line:** "Cobaltine surfaces a ranked list of possible causes for a user-entered symptom and a triage suggestion (self-care, see a doctor within a week, seek emergency care), for informational use; it does not diagnose and does not replace a clinician's evaluation." That single sentence is the fact a regulator reads first, but the class it implies is not a clean win: IMDRF's SaMD framework grades on a "Category I to IV" scale, not FDA's separate "Class I/II/III" device scheme, so the two vocabularies should not be mixed. The category turns on two axes together, the significance of the information (inform / drive / diagnose-or-treat clinical management) and the seriousness of the condition addressed, not on the word "diagnose" alone. Cobaltine's own scope names a "drive clinical management, including triage" function, because its output routes the user toward self-care, a routine visit, or emergency care, and its own "seek emergency care" branch concedes the condition can be critical; an honest reading plausibly lands the emergency-care branch at IMDRF Category II or III, with only the self-care and routine-visit branches supportable at Category I. The product scope should say so explicitly, or be narrowed to non-serious triage only.

**Section 6, third-parties-and-processors row** (the fields a named vendor receives and whether a contract covers them, distinct from section 2's regulation-level table): "Third-party symptom-checker API vendor receives the entered symptom, self-reported age band and sex at birth, and a session identifier for every triage request; no name, date of birth, or contact detail crosses that boundary." Whether that vendor is a HIPAA business associate needing a BAA depends on a fact this worked example must state, not assume: HIPAA binds a covered entity (a hospital, health plan, or provider) and the business associates working on its behalf, not a standalone, direct-to-consumer app that users choose and use on their own. If Cobaltine operates under contract with a named health plan or provider, say so, and the BAA follows; if Cobaltine is sold directly to consumers with no covered entity behind it, HIPAA most likely does not apply to it or its vendor at all, and the governing regime is instead the FTC Health Breach Notification Rule or the relevant state consumer-health-data law, which section 2's regulation table should name and this row's contract clause should cite accordingly, with the EU processor mapping tracked as [OPEN: confirm before the EU launch].
