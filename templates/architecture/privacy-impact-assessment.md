---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: ""
aliases: ["Privacy Impact Assessment", "privacy-impact-assessment"]
---
# Privacy Impact Assessment: [product or feature name]

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md); re-confirmed at Gate 5 before the artifact ships
Knowledge: [Risk matrix worksheet](../../frameworks/execution/risk-matrix.md)
Skill: [red-team-agent](../../agents/red-team-agent.md) for the risk walk; [reg-gap-check](../../skills/reg-gap-check/SKILL.md) when a regulator is in scope

> **Delete any section you do not need.** A feature that touches no personal data records that fact in section 1 and stops; a feature that profiles people, processes special-category data at scale, or applies a model to personal data fills every section. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- This document is not legal advice, and a completed copy is not a compliance
     certification. It structures the questions a data protection officer (or
     whoever holds that role for you) signs off on, so the answers exist in one
     place, with owners, before Gate 3. The legal determinations, above all the
     lawful basis for each processing purpose, are entered by counsel or the
     DPO, and are fields here for that reason. Whether an assessment is required
     at all is decided in ../operate/compliance-impact-assessment.md section 4;
     the per-attribute PII classification lives in data-model.md sections 3 and
     5 and is linked, not copied; the threat walk against attackers is
     security-architecture.md. This file owns the description of the processing,
     the necessity and proportionality questions, the risks to the individuals
     whose data it is, the mitigations, and the sign-off. Fill the inventory,
     the risk table, and the DPO's name first. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Signed
**DPO or privacy lead:** [name] · **Data model reviewed:** [link to the filled data-model.md]

## 1. Description of the processing

| Field | Value |
|---|---|
| Purpose, in one sentence | [what the processing achieves, for whom] |
| Whose data | [data subjects: employees, customers' employees, applicants, minors if any] |
| Scale | [subjects per period, records, geographies] |
| Where data comes from | [collected from the subject / observed / inferred by a model / received from a third party] |
| Who receives it | [internal teams, processors, sub-processors, partners] |
| New technology or automated decisions | [yes / no; if a model proposes or decides anything about a person, also complete ../ai/human-approval-gates.md] |
| Related assessments | [compliance-impact-assessment.md section 4 decision; earlier assessments this extends] |

## 2. Data inventory

<!-- One row per data category and purpose pair. The lawful basis column is
     filled by counsel or the DPO, not by the product team; leave it as a field
     until they do. Retention and storage are copied from the data model. -->

| Data category | Data subjects | Source | Purpose | Lawful basis (entered by counsel or DPO) | Special or sensitive category | Retention (from data-model.md) | Stored and processed where | Processors involved |
|---|---|---|---|---|---|---|---|---|
| | | | | [basis] | yes / no | | | |

## 3. Necessity and proportionality

<!-- Answer with a mechanism or an owner, never a bare yes. Each answer is
     something a reviewer could check in the product. -->

| Question | Answer | Evidence or owner |
|---|---|---|
| Could the purpose be achieved with less data, or with data that identifies no one? | | |
| What is collected that the purpose does not need, and why is it kept? | | |
| How are subjects told what is collected and why, at the moment it happens? | | |
| How does a subject see, correct, export, or delete their data, and how long does each take? | | |
| How does a subject object to, or opt out of, the processing? | | |
| How is accuracy maintained, especially for anything a model inferred? | | |
| Who can access the data, and how is access logged and reviewed? | | |
| How long is data kept, and what executes deletion when the period ends? | | |
| Which international transfers happen, and under what mechanism? | | |

## 4. Consultation

<!-- Who was asked, what they said, what changed. Subjects or their
     representatives count; a works council or a customer advisory group is a
     valid row. -->

| Consulted | Date | What they raised | What changed as a result |
|---|---|---|---|
| DPO or privacy lead | | | |
| Security | | | |
| Data subjects or their representatives | | | |
| Processors | | | |

## 5. Risks to individuals

<!-- Risks to the people whose data it is, not to the company; reputational and
     regulatory risk to the company belongs in the risk register. Score
     likelihood and severity on the scales defined in the risk matrix worksheet,
     so this table can be compared with every other risk the product carries.
     The italic row is an invented example on the expense copilot. -->

| Id | Risk to the individual | How it could happen | Likelihood | Severity | Score | Source |
|---|---|---|---|---|---|---|
| PR-1 | | | | | | |
| *PR-0* | *an employee's medical expense reveals a health condition to every manager in the approval chain* | *the copilot extracts and displays merchant and line items to all approvers* | *[per scale]* | *[per scale]* | *[score]* | *data flow review, YYYY-MM-DD* |

## 6. Mitigations

<!-- One row per risk. "Effect" is eliminated, reduced, or accepted; an
     accepted risk above the band the risk matrix names as needing an owner
     gets one here and a row in ../execution/risk-register.md. -->

| Risk id | Measure | Effect (eliminated / reduced / accepted) | Residual score | Owner | In place by | Approved by DPO |
|---|---|---|---|---|---|---|
| PR-1 | | | | | | |

## 7. Sign-off

| Role | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| DPO or privacy lead | | accepted / accepted with conditions / rejected / regulator consultation needed | | |
| Product owner | | | | |
| Security reviewer | | | | |

**Next review:** [YYYY-MM-DD, or the trigger: new data category, new processor, new market, model change]

## Exit gate (feeds Gate 3: architecture and risks reviewed)

A signed assessment supports the PII and retention line at [Gate 3](../../os/STAGE-GATES.md), feeds risk rows into [risk-register.md](../execution/risk-register.md), and is re-confirmed under the regulated overlay at Gate 5.

- [ ] Every data category has a purpose, a retention period copied from the data model, and a lawful basis entered by counsel or the DPO, or a named owner and date for it
- [ ] Every necessity question is answered with a mechanism or an owner, none with a bare yes
- [ ] The DPO was consulted, and the consultation row records what changed
- [ ] Every risk is phrased as harm to a person, scored on the risk matrix scales, and has a mitigation row
- [ ] The ILLUSTRATIVE example rows have been deleted; a signed assessment carrying invented personal-data content is worse than an unsigned one
- [ ] Every accepted residual risk above the named band has an owner and a risk register row
- [ ] The DPO's verdict is recorded by name and date, with conditions written out
- [ ] Signed by [name], [date]
