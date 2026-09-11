# Risk Register: Harrow Credit BNPL Underwriting and Collections

Fills [templates/execution/risk-register.md](../templates/execution/risk-register.md). Everything here is invented for this standalone example: Harrow Credit is a fictional buy-now-pay-later provider, the people are invented names in invented roles, and every number, date and rate is ILLUSTRATIVE. There is no external Harrow Credit journey or data sheet; the numbers here are internal to this register so they can be checked against each other and against the documents this register feeds. See the [examples index](README.md).

**Initiative:** BNPL underwriting and collections platform · **Register owner:** Priya Nkemelu, Head of Credit Risk · **Review cadence:** weekly, Tuesdays at the credit risk stand-up
**Last reviewed:** 2026-09-11 · **Premortem run:** 2026-08-14

## 1. Scoring

Likelihood and impact each score 1 to 3 (low, medium, high). Score = L x I, range 1 to 9. At 6 or above the risk needs an active mitigation with a date, not a watching brief. The scale stays coarse on purpose: a 5-point scale invents precision the estimates do not have. These estimates all carry the uncertainty of a pre-maturity book, and the register is re-scored at the weekly review.

## 2. The register

Response is one of: mitigate (act to reduce), accept (a named person accepts it in writing), transfer (contract or insurance), avoid (change the plan). "Monitor" is not a response; it is a synonym for accept without the signature. Every row names an event that could happen and an owner with a date.

| # | Risk (event, not a vague noun) | Category (value / usability / feasibility / viability / delivery / security) | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| R9 | Adverse-action reason codes chosen from a fixed list do not reflect what the model actually weighted for this applicant | value | 2 | 3 | 6 | mitigate | Map each reason code to the top model feature at decision time; audit a 50-decline sample monthly against Regulation B's specificity standard; escalate to fair-lending review if the sampled mismatch rate exceeds 5% | Priya Nkemelu, Head of Credit Risk | 2026-11-03 |
| R10 | The in-house underwriting model produces a materially higher decline rate for a protected class or a close proxy, and the disparity is only visible in a product tier or geography the aggregate averages away | value | 2 | 3 | 6 | mitigate | Slice approval and loss rates by protected class and by proxy (postcode, device type) each quarter under a documented ECOA and Regulation B fair-lending review; trigger a model-risk review and a decision-policy change if any slice's disparity exceeds the fair-lending tolerance set with counsel | Priya Nkemelu, Head of Credit Risk | 2026-11-03 |
| R11 | An automated reminder or dunning flow contacts a borrower at a frequency or on a channel that breaches collections conduct limits under the FDCPA and Regulation F | viability | 3 | 3 | 9 | mitigate | Contact frequency and channel limits written as testable rules before any new nudge channel ships; collections compliance and legal sign-off is a release gate; cease-and-desist handling is a real path, not decorative | Priya Nkemelu, Head of Credit Risk (collections compliance sign-off: Dana Whitfield, General Counsel) | 2026-11-03 |
| R12 | Repayment performance furnished to a credit bureau is inaccurate or a disputed record is not corrected within the mandated window under the FCRA | viability | 2 | 2 | 4 | mitigate | Furnishing format and dispute-handling obligations mapped to the bureau's specification; a dispute queue with a time-to-correct metric and a human owner; trigger a furnishing freeze if the correction window is missed | Marcus Oyelaran, Head of Credit Operations | 2026-11-03 |
| R13 | The underwriting model drifts against its validation cohort as borrower behaviour and merchant mix change, so the live decision no longer matches the model the fair-lending review passed | feasibility | 2 | 3 | 6 | mitigate | Population-stability and feature-drift monitoring monthly against the validation baseline; trigger a re-validation and a policy freeze if drift crosses the monitored threshold set with model risk | Priya Nkemelu, Head of Credit Risk | 2026-11-03 |
| R14 | The UK FCA's BNPL regulation, with commencement on 15 July 2026 (verify with counsel), imposes affordability and disclosure duties Harrow Credit's UK flow does not yet meet | viability | 3 | 3 | 9 | mitigate | UK BNPL flow mapped against the FCA's affordability and disclosure expectations ahead of commencement; a dated readiness review with counsel before 15 July 2026; trigger pausing UK originations if readiness is not signed off | Dana Whitfield, General Counsel | 2026-06-30 |

## 3. Accepted risks

Risks someone chose to live with, signed. This section is what makes "accept" honest: acceptance without a name is drift. The accepted risks below are signed by the CRO.

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| R12 | Yara Benali, Chief Risk Officer | 2026-09-11 | Residual furnishing-dispute risk sits within the operations team's correction capacity and a furnishing freeze is the fallback. | When the quarterly FCRA dispute rate or correction time exceeds the threshold set with Marcus Oyelaran |
| R14 | Yara Benali, Chief Risk Officer | 2026-09-11 | The UK BNPL readiness work is on a dated plan ahead of the 15 July 2026 commencement, with pausing UK originations as the backstop. | At the dated readiness review with counsel before 15 July 2026 |

## 4. Closed risks

Closed does not mean deleted. The value of this table is the pattern it shows over a year: the same risk closing three times means it was never addressed, only survived.

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| R7 | 2026-08-05 | Merchant settlement sandbox was delivered before UAT; the delivery risk did not occur. |

## 5. How this register fails

A register that fails this way still looks like a register, which is the expensive part: the team believes the risk is managed because it is written down. Being written down is not a mitigation.

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| No owner | A row with a score and a date and no human attached | Every row has one named owner. Orphans go to the top of the review, not the bottom |
| Scored once, never revisited | Probability and impact unchanged for quarters while the world moved | Re-score at every review, and flag any row not touched in a month |
| Mitigation restates the risk | "Risk: inaccurate furnishing. Mitigation: furnish accurately." | A mitigation names an action, an owner and a date, or it is not one |
| Everything is medium | A long list of identical amber rows and no triage | Force a spread. If most rows are medium, nobody has ranked them |
| Closed risks deleted | The history disappears, and the same risk returns next quarter unrecognised | Closed rows are archived, not removed, and reviewed for repeats |
| The register replaces escalation | A serious risk is logged, never raised, and leadership is surprised | Above an agreed threshold, logging is not enough: the row names who was told and when. R11 and R14 above score 9 and are escalated to the CRO at the weekly stand-up |

## Exit gate

Checkable by someone who does not own any of the rows.

- [x] Every risk is written as an event that could happen, not a topic heading
- [x] Every open risk has a score, an owner, and a review date in the future
- [x] Every score of 6 or higher has an active mitigation with a trigger, not "monitor"
- [x] Every accepted risk is signed by name in section 3
- [x] Findings from the security architecture checklist and dependency register appear here
- [x] A premortem has been run before Gate 3, and its findings are rows above
- [x] The example row has been deleted

Signed: Dana Whitfield, General Counsel, 2026-09-11
