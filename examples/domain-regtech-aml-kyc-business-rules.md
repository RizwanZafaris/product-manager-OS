# Business Rules Register: Beacon AML Screening and Transaction Monitoring

Fills [templates/definition/business-rules.md](../templates/definition/business-rules.md). Everything here is invented for this standalone example: Beacon is a fictional AML screening and transaction-monitoring product, Fernhollow Trust is the fictional bank that runs it, Farrukh Aslam is its fictional MLRO, and every number, name, date, threshold, and regulatory reference is ILLUSTRATIVE, not drawn from any real institution or market. There is no external regtech-aml-kyc journey or data sheet. See the [examples index](README.md).

**Owner:** Camille Duval, Product Manager, Beacon · **Date:** 2026-09-11 · **Status:** Approved at Gate 2 attempt 1
**Applies to:** PRD and FRD not filled for this example (ILLUSTRATIVE)

## 1. Active rules

| ID | Rule statement (WHEN ... THEN ...) | Trigger point in the product | Source of truth | Business owner | Exceptions | Enforced by (FR ID) | Test traceability |
|---|---|---|---|---|---|---|---|
| BR-001 | WHEN a customer's aggregate cash-equivalent transaction volume exceeds USD 10,000 in a rolling 30-day window AND the transactions are split across two or more days with individual amounts below USD 5,000 THEN generate a structuring typology alert and route it to the enhanced-review queue | Nightly monitoring batch (02:00 UTC) | Fernhollow Trust AML Typology Library v12, section 4.1 "Structuring and Smurfing", held by the MLRO | Farrukh Aslam, MLRO, Fernhollow Trust | None on the USD 10,000 / 30-day threshold itself; a documented seasonal-business list (BR-001-EXC) suppresses the alert for 40 pre-approved merchant accounts with verified high-cash seasonality, reviewed quarterly by the MLRO | FR-101 | AC-42 |
| BR-002 | WHEN a customer name or alias produces a fuzzy-match score of 85 percent or higher against the OFAC SDN List or the UN Consolidated List THEN block the transaction pending manual review and escalate to the sanctions officer within 15 minutes | Real-time payment authorization API call | OFAC SDN List update policy and UN Security Council Consolidated List refresh schedule, as implemented in Fernhollow Trust Sanctions Policy v7, section 2.3 | Farrukh Aslam, MLRO, Fernhollow Trust | None; no auto-release permitted without sanctions officer sign-off | FR-102 | AC-43 |
| BR-003a | WHEN a customer is identified as a Politically Exposed Person (PEP) or a close associate/family member of a PEP during onboarding OR via list-refresh re-screening THEN trigger Enhanced Due Diligence (EDD) workflow | Onboarding KYC completion event OR daily PEP list-refresh diff | FATF Recommendation 12 (as implemented in Fernhollow Trust CDD Policy v5, section 3.4) and FinCEN CDD Final Rule beneficial ownership provisions | Farrukh Aslam, MLRO, Fernhollow Trust | None on the PEP identification trigger; a documented "low-risk PEP" exception (BR-003-EXC) allows standard due diligence for PEPs in jurisdictions rated low-risk under Fernhollow Trust's own Country Risk Model (built per Wolfsberg Group country-risk guidance; the Wolfsberg Group publishes methodology, not a public jurisdiction-tier list), but requires MLRO written approval per case | FR-103 | AC-44 |
| BR-003b | WHEN a customer is identified as a Politically Exposed Person (PEP) or a close associate/family member of a PEP during onboarding OR via list-refresh re-screening THEN require source-of-wealth documentation | Onboarding KYC completion event OR daily PEP list-refresh diff | FATF Recommendation 12 (as implemented in Fernhollow Trust CDD Policy v5, section 3.4) and FinCEN CDD Final Rule beneficial ownership provisions | Farrukh Aslam, MLRO, Fernhollow Trust | None on the PEP identification trigger; a documented "low-risk PEP" exception (BR-003-EXC) allows standard due diligence for PEPs in jurisdictions rated low-risk under Fernhollow Trust's own Country Risk Model (built per Wolfsberg Group country-risk guidance; the Wolfsberg Group publishes methodology, not a public jurisdiction-tier list), but requires MLRO written approval per case | FR-103 | AC-44 |
| BR-003c | WHEN a customer is identified as a Politically Exposed Person (PEP) or a close associate/family member of a PEP during onboarding OR via list-refresh re-screening THEN set risk tier to "High" until EDD closure is approved by the MLRO | Onboarding KYC completion event OR daily PEP list-refresh diff | FATF Recommendation 12 (as implemented in Fernhollow Trust CDD Policy v5, section 3.4) and FinCEN CDD Final Rule beneficial ownership provisions | Farrukh Aslam, MLRO, Fernhollow Trust | None on the PEP identification trigger; a documented "low-risk PEP" exception (BR-003-EXC) allows standard due diligence for PEPs in jurisdictions rated low-risk under Fernhollow Trust's own Country Risk Model (built per Wolfsberg Group country-risk guidance; the Wolfsberg Group publishes methodology, not a public jurisdiction-tier list), but requires MLRO written approval per case | FR-103 | AC-44 |
| BR-004 | WHEN an alert's calculated risk score is 75 or above THEN prohibit auto-closure of the alert; require analyst narrative justification and secondary reviewer approval before status can change to "Closed" | Alert disposition action (analyst clicks "Close") | Fernhollow Trust Alert Management SOP v3, section 5.2 "High-Risk Closure Controls" | Farrukh Aslam, MLRO, Fernhollow Trust | None; system-enforced hard block | FR-104 | AC-45 |
| BR-005a | WHEN sanctions or PEP list data is older than 24 hours since last successful publisher sync THEN suspend all new customer onboarding | Hourly list-refresh health check job | Fernhollow Trust Data Integrity Policy v2, section 1.1 (aligned with OFAC and UN publisher cadences) | Farrukh Aslam, MLRO, Fernhollow Trust | None; suspension lifts only after successful sync confirmed by compliance ops | FR-105 | AC-46 |
| BR-005b | WHEN sanctions or PEP list data is older than 24 hours since last successful publisher sync THEN flag existing high-risk customers for immediate re-screening | Hourly list-refresh health check job | Fernhollow Trust Data Integrity Policy v2, section 1.1 (aligned with OFAC and UN publisher cadences) | Farrukh Aslam, MLRO, Fernhollow Trust | None; suspension lifts only after successful sync confirmed by compliance ops | FR-105 | AC-46 |

## 2. Retired rules

| ID | Rule statement | Retired on | Retired by | Why | Replaced by |
|---|---|---|---|---|---|
| BR-006 | WHEN a customer's transaction volume exceeds 5x their onboarding-declared range in a rolling 30 days THEN generate an alert and freeze the risk tier at "enhanced" until an analyst closes it with a narrative | 2026-06-02 | Decision D-041, signed by Farrukh Aslam, MLRO | Tightened under examiner finding on missed structuring cases; alert volume rose 38 percent the following week, logged against analyst capacity in the same decision entry so a later examiner can sample the reasoning, not just the outcome | BR-001 (restructured thresholds and added explicit splitting logic) |

## 3. Exception handling

| Rule ID | Exception | Who may grant it | Recorded where |
|---|---|---|---|
| BR-001 | Seasonal-business suppression for 40 pre-approved merchant accounts with verified high-cash seasonality | Farrukh Aslam, MLRO (quarterly review required) | Exception Log EL-2026-Q3, row 14; linked to decision D-041 appendix |
| BR-003a, BR-003b, BR-003c | Low-risk PEP standard-due-diligence override for PEPs in jurisdictions rated low-risk under the internal Country Risk Model | Farrukh Aslam, MLRO (written approval per case) | Case File CF-[ID], section "Override Justification"; audited monthly by Compliance QA |

## 4. Change control

- **Who may change a rule:** Farrukh Aslam, MLRO, Fernhollow Trust. The product team may propose changes based on tuning data or regulatory updates, but only the MLRO holds the source of truth and approves threshold modifications. Tuning a monitoring threshold is itself an auditable compliance decision.
- **How a change lands:**
  1. Request submitted via Change Control Form CC-AML-[YYYY]-[NN] with proposed threshold, rationale, and impact analysis (alert volume delta, false-positive/false-negative projections).
  2. Below-the-line testing executed in staging environment using historical transaction dataset (minimum 90 days); results attached to form.
  3. MLRO reviews proposal, test results, and analyst capacity impact model; signs off or rejects within 5 business days.
  4. Approved changes enter production via versioned rule-library deployment (not code release); effective date recorded in change log.
  5. All changes logged in Decision Log DL-AML with unique ID, approver name, date, old/new values, and test evidence link. An examiner must be able to sample this history to verify that threshold changes were deliberate, tested, and capacity-aware.
- **Review cadence:** Quarterly re-confirmation of all active rules against current regulatory guidance, typology evolution reports, and alert-quality metrics. Annual full audit by internal compliance function. Ad hoc reviews triggered by regulatory exam findings, significant false-negative incidents, or list-publisher policy changes.

---

### Worked micro-example (illustrative, invented)

> **BR-001:** WHEN a customer's aggregate cash-equivalent transaction volume exceeds USD 10,000 in a rolling 30-day window AND the transactions are split across two or more days with individual amounts below USD 5,000 THEN generate a structuring typology alert and route it to the enhanced-review queue. Trigger: nightly monitoring batch. Source of truth: Fernhollow Trust AML Typology Library v12, section 4.1. Business owner: Farrukh Aslam, MLRO. Exceptions: seasonal-business list (BR-001-EXC), reviewed quarterly. Enforced by FR-101. Test: AC-42.
> Six months later, an examiner notes that structuring alerts are missing multi-account patterns within the same household. The MLRO proposes tightening BR-001 to include related-party aggregation. This enters through section 4: below-the-line testing shows alert volume would rise 24 percent, requiring 1.5 additional FTEs in the review team. The MLRO approves the change on 2026-12-15 under decision D-052, logs it in DL-AML with test evidence and capacity note, and deploys rule-library v13. BR-001 is updated in place (not retired, since the core trigger remains); the change history explains why December alerts differ from June alerts, and an examiner sampling DL-AML sees the deliberate, tested, capacity-aware decision.

---

## Exit gate (feeds Gate 2: requirements signed off)

- [x] Every rule is atomic: one trigger, one outcome. BR-001, BR-002, BR-003a, BR-003b, BR-003c, BR-004, BR-005a, and BR-005b each specify a single condition set and a single required action.
- [x] Every rule names a source of truth a reviewer could open. Each row cites a specific policy document, section, and version held by the MLRO.
- [x] Every rule has a business owner outside the product team. Farrukh Aslam, MLRO at Fernhollow Trust, owns all active rules.
- [x] Exceptions are enumerated with a decider, or marked "none". Section 3 lists two exceptions with named deciders and recording locations; BR-002, BR-004, BR-005a, and BR-005b carry "None" in the exceptions column.
- [x] Every rule maps to an enforcing FR and a test ID, or carries an owner and date to close the gap. All rules have FR IDs and AC IDs populated.
- [x] Change control names who may change rules and how changes reach production. Section 4 specifies the MLRO as sole approver, details the five-step landing process including below-the-line testing and decision-log requirement, and sets quarterly/annual/ad-hoc review cadences.

Signed: Farrukh Aslam, MLRO, Fernhollow Trust, 2026-09-11
