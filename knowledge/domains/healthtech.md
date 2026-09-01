# Healthtech

One question sorts everything in this domain: what is the product's intended use? Intended use, the claim you make about what the software does for a patient or clinician, decides whether you built an app or a medical device, which regulator owns you, what evidence you must produce, and how fast you may ship. The second sorting question is who pays, because in healthcare the user (a patient), the decider (a clinician), and the payer (an insurer, employer, or health system) are almost never the same party, and products that delight users while ignoring payers die solvent-user-rich.

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

**Conductor overlay:** this domain sharpens DISCOVER-1 (name the person: patient, clinician, and payer are three answers), DEFINE-8 (overlays: the regulated and AI overlays both commonly fire), DESIGN-3 (where PII lives becomes where PHI lives, with BAAs), and DELIVER-2 (UAT includes clinical validation, not just functional passes).

**Templates this bends:** [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (PHI categories, BAA rows, device-classification record) and [uat-plan](../../templates/delivery/uat-plan.md) (clinician testers, clinical scenarios, and sign-off from a medical owner).
