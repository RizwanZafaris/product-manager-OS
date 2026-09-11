# Compliance Impact Assessment: Brightpath Learning K-12 Literacy Platform

Fills [templates/operate/compliance-impact-assessment.md](../templates/operate/compliance-impact-assessment.md). Everything here is invented: Brightpath Learning is a fictional K-12 literacy platform, the school districts and people named are roles filled by invented names, and every date, count and dollar figure is ILLUSTRATIVE. Regulatory statements are current as of 2026-09-11, require confirmation with counsel, and this document is not legal advice nor a compliance certification. See the [examples index](README.md) and the [edtech domain card](../knowledge/domains/edtech.md).

**Owner:** Kalinda Perera, VP Product · **Legal or compliance counterpart:** Jordan Lee, General Counsel
**Status:** In review · **Date:** 2026-09-11

## 1. Product and data summary

- What the feature does and who uses it: Brightpath delivers adaptive reading exercises to students in grades K through 8 within US public-school districts; teachers assign curricula and view dashboards while district procurement buys the license via RFP. The student is the user, the teacher is the daily decider, and the district is the buyer, reflecting the three-constituency tension named in the [edtech domain card](../knowledge/domains/edtech.md).
- Markets and jurisdictions in scope: United States, specifically California (SOPIPA applies), New York (Ed Law 2-d), and Illinois (SIPA applies); FERPA and COPPA apply federally across all states.
- Does the product contain an AI model making or influencing decisions about people? Yes, an adaptive engine sequences lesson difficulty based on student performance. Per the template's own question 3, this triggers the AI overlay (`templates/ai/human-approval-gates.md` onward), completed separately and not restated in this standalone example; it does not trigger the `modules/regulated/` overlay, which also requires a financial regulator, and for K-12 edtech the primary regulatory lens is student privacy rather than financial conduct rules.

## 2. Applicable regulations and regimes

| Regulation or regime | Applies because | Obligations triggered | Evidence and holder | Owner |
|---|---|---|---|---|
| FERPA | Brightpath receives education records from districts under a "school official" exception designated in each District Data Privacy Agreement (DPA). | Ensure legitimate educational interest; no unauthorized disclosure; annual notification rights handled by district. | Signed DPAs held by Jordan Lee (GC); District Board Policy references. | Jordan Lee |
| COPPA | Students under age 13 provide personal information (DOB, name) at account creation. | Verifiable parental consent OR valid school authorization where DPA clause explicitly covers COPPA school-consent exception. | DPA Clause 4.2 (Consent Mechanism); Counsel memo confirming amended rule interpretation. | Jordan Lee |
| SOPIPA (California) | Brightpath serves California districts; prohibits targeted advertising based on student data. | No ad targeting; no profiling for commercial purposes unrelated to learning outcomes. | Contractual warranty in CA District Master Service Agreements. | Kalinda Perera |
| PPRA | Surveys administered to parents/guardians regarding home environment or political affiliation. | Parental right to inspect surveys and opt out; notice required before administration. | Survey Protocol Document v2.1; Opt-out form template. | Kalinda Perera |

*Note: COPPA's amended rule compliance date is verified as 22 April 2026 per Federal Register notices current as of 2026-09-11; confirm final enforcement guidance with counsel.*

## 3. Data categories

| Data category | Personal data? | Special or sensitive category? | Stored where | Retention period | Lawful basis or ground |
|---|---|---|---|---|---|
| Student name, grade, assignment scores | yes | no | AWS us-east-1 (encrypted at rest) | Deleted or returned to the district within 30 days of contract end, per the DPA | FERPA school-official use |
| Student date of birth, collected at account creation for a student under 13 | yes | yes | AWS us-east-1 (encrypted at rest) | Deleted at account closure, not retained for analytics | COPPA school consent under the district's DPA |

## 4. DPIA flag

Answer each honestly:

- Systematic profiling or automated decisions with significant effects? yes (adaptive sequencing influences learning path, but not life-altering decisions like credit or housing)
- Large-scale processing of special category data? yes (date of birth for under-13s across thousands of students)
- Systematic monitoring of a publicly accessible area? no
- New technology applied to personal data in a novel way? no (standard LMS architecture)

**DPIA required:** yes · If yes: run by Jordan Lee, due 2026-10-01, filed at Legal Repository / Privacy Office

## 5. Cross-border transfers

| Transfer (from, to) | Data involved | Mechanism relied on | Evidence |
|---|---|---|---|
| None | N/A | N/A | All student data processed and stored within US borders (AWS us-east-1). |

## 6. Third parties and processors

| Party | Role (processor / sub-processor / controller) | Contract clause covering this use | Audit or information rights |
|---|---|---|---|
| AWS | Processor | DPA Addendum A (Sub-processors) | SOC 2 Type II report provided annually; Brightpath holds audit rights. |
| LearnModel Inc. | Sub-processor (AI Engine) | Clause 7.1: "Vendor is contractually barred from training models on student data." | Annual security questionnaire; no direct access to raw PII, only hashed IDs. |
| SchoolDistrict X | Controller | Master Service Agreement | District retains ultimate control over data lifecycle and deletion requests. |

## 7. Retention and deletion

- Retention schedule per category is complete in section 3: confirmed
- Deletion is implemented, not just promised: how a deletion request actually executes: Automated script triggers upon contract termination status change in CRM; purges production DB and backups within 30 days. Owner: DevOps Lead.
- What survives deletion (backups, logs, aggregates) and for how long: Anonymized aggregate usage metrics survive indefinitely for efficacy reporting; transactional logs deleted after 90 days.

## 8. Gaps

| # | Gap | Risk if shipped as is | Owner | Date |
|---|---|---|---|---|
| 1 | District Y's DPA addendum lacks explicit language satisfying COPPA's school-consent exception for DOB collection. | Pilot launch delayed to next semester (Spring 2027) instead of Fall 2026; revenue impact ILLUSTRATIVE $45,000. | Jordan Lee | 2026-09-20 |

## 9. Sign-off

| Name | Role | Verdict | Conditions | Date |
|---|---|---|---|---|
| Jordan Lee | Legal counsel or DPO | Conditional Pass | Gap 1 must be closed before District Y pilot starts. | 2026-09-11 |
| Priya Patel | Second line / compliance | Pass | DPIA completion required by 2026-10-01. | 2026-09-11 |
| Kalinda Perera | Product owner | Accepted | Launch sequence adjusted for District Y delay. | 2026-09-11 |

## Exit gate

This document passes when:

- [x] Every regulation row cites evidence and names its holder, no "we believe it is fine" rows
- [x] Every data category has a stated retention period and lawful ground
- [x] The DPIA decision is recorded either way, with a named runner if yes
- [x] Deletion is described as a mechanism that executes, not a policy that exists
- [ ] For financially regulated products, the reg-gap-check skill was run and its output is attached (N/A: Not a financial regulator product, though AI overlay applies)
- [x] Legal sign-off is a name and a date, not a forwarded email

Signed: Jordan Lee, General Counsel, 2026-09-11
