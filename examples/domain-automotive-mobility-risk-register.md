# Risk Register: Calderun Systems Lane-Assist OTA Campaign

Fills [templates/execution/risk-register.md](../templates/execution/risk-register.md). Everything here is invented: Calderun Systems is a fictional Tier-1 automotive software supplier, its customer Marrowbank Motors is a fictional mid-size automaker, the people are roles filled by invented names, and every number, date and identifier is ILLUSTRATIVE, this example's own illustrative assumptions rather than drawn from any internal data sheet, real supplier, automaker or fleet. See the [examples index](README.md). Regulatory statements are stated as of 2026-09-11 and are not legal advice; confirm with counsel before relying on them. This register should be read alongside the [automotive and mobility domain card](../knowledge/domains/automotive-mobility.md).

**Initiative:** Marrowbank lane-assist OTA campaign, Calderun release OTA-LA-2.4 · **Register owner:** Priya Raghunathan, campaign risk owner · **Review cadence:** weekly, Tuesdays at the OTA campaign stand-up
**Last reviewed:** 2026-09-11 · **Premortem run:** 2026-08-14

**People on this register (all ILLUSTRATIVE):** J. Okonkwo, Head of Functional Safety; D. Halloran, CTO, Calderun Systems; M. Bhatt, Cybersecurity Manager; S. Ferreira, Homologation Lead; A. Nkemelu, Campaign Manager; T. Voss, Staff Engineer, Vehicle Motion.

## 1. Scoring

Likelihood and impact each score 1 to 3 (low, medium, high). Score = L x I, range 1 to 9. At 6 or above the risk needs an active mitigation with a date, not a watching brief.

| Score | Meaning | What it binds |
|---|---|---|
| 1 | Low | Watch at the weekly review; no action dated |
| 2 | Medium | Mitigation named, owner assigned, no hard date |
| 3 | High | Active mitigation with a trigger and a date, or a signed acceptance in section 3 |
| Product 6 to 9 | At or above the threshold | Mitigation must name an action, an owner and a date; logging alone is not enough and the row records who was told and when |

The scale stays coarse on purpose. A 5-point scale would invent precision these estimates do not have: an ISO 26262 change-impact assessment reports a safety level or it reports nothing, and UN Regulation No. 156 reports a processing outcome, not a probability.

## 2. The register

Response is one of: mitigate (act to reduce), accept (named person accepts it in writing), transfer (contract or insurance), avoid (change the plan). "Monitor" is not a response; it is a synonym for accept without the signature. All scores, dates and names ILLUSTRATIVE.

| # | Risk (event, not a vague noun) | Category | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| 1 | The OTA-LA-2.4 steering-torque limiter change, filed by engineering as a tuning change, is reclassified by the functional-safety assessor as ASIL C under ISO 26262, which triggers UN Regulation No. 156 software-update management review before rollout | feasibility | 3 | 3 | 9 | mitigate | row carried unchanged from the campaign risk card: re-classify the change as safety-relevant; hold the fleet rollout for a full ISO 26262 change-impact assessment; if the assessor confirms ASIL C, no vehicle receives the update until the UN R156 software-update-management process has been applied and the re-homologation path is agreed with the type-approval authority. Trigger: assessor's written finding lands, expected 2026-09-25 (ILLUSTRATIVE). Escalation above threshold: CTO D. Halloran told 2026-09-02, three days after the assessor's first verbal flag | J. Okonkwo | 2026-09-18 |
| 2 | The campaign cannot produce the UN Regulation No. 155 cybersecurity-management-system evidence the type-approval authority asks for, so the update cannot be pushed to vehicles in the market that adopted the regulation | security | 2 | 3 | 6 | mitigate | M. Bhatt runs the CSMS evidence pack against ISO/SAE 21434 work products; the campaign's threat analysis and risk assessment is scheduled for 2026-09-26. Trigger: the evidence pack is incomplete at the 2026-09-26 review, at which point the round of updates to the affected fleet is sliced out and pushed after the homologation review | M. Bhatt | 2026-09-25 |
| 3 | The change touches the type approval of Marrowbank vehicles already sold, and pushing the update without the re-approval path agreed can decertify them for their owners | viability | 3 | 3 | 9 | mitigate | S. Ferreira maps the affected type-approval variant set since 2026-09-04 and holds an evidence pack for the authority; no update ships to a named variant until that variant's re-approval position is signed off. Trigger: any variant left un-mapped at the 2026-09-25 homologation review | S. Ferreira | 2026-09-25 |
| 4 | An update that is pushed while a vehicle is mid-drive cannot roll back, leaving the lane-assist function unavailable or degraded until the vehicle is parked and re-flashed | delivery | 2 | 3 | 6 | mitigate | A. Nkemelu gates every push so no vehicle begins a download while in motion, and the in-vehicle installer holds the flash until standstill; rollback is defined to the previous known-good image (OTA-LA-2.3.5, ILLUSTRATIVE) and verified in the fleet lab. Trigger: any push attempt logged against a moving vehicle in the OTA telemetry | A. Nkemelu | 2026-09-18 |
| 5 | Dealer-installed hardware variants on some vehicles in the fleet do not match the steering-torque limiter assumptions the software was tested against, so a subset of the fleet receives an update calibrated for a configuration it does not have | feasibility | 2 | 2 | 4 | mitigate | T. Voss enumerates the dealer-installed hardware variants against the tested configuration matrix; the push is sliced by variant until each variant's calibration is confirmed or excluded. Trigger: a variant found outside the tested matrix | T. Voss | 2026-10-02 |
| 6 | The assessor's finding slips past the campaign's late-September window, so the rollout is held without a re-entry plan and the fleet update window moves into the winter period | delivery | 2 | 2 | 4 | mitigate | A. Nkemelu holds a re-entry plan for a rollout that resumes after the assessor's finding; the plan names who re-opens the release and what evidence it waits on. Trigger: no written finding by 2026-10-09 | A. Nkemelu | 2026-10-09 |
| 7 | Connectivity drops mid-download across a slice of the fleet, so a vehicle is left with a partially applied image and the lane-assist function is unavailable until re-flashed | delivery | 3 | 2 | 6 | mitigate | the in-vehicle installer keeps the previous image intact until the new one verifies; A. Nkemelu tracks the OTA update success and rollback rate weekly, and the update is paused for any vehicle that reports a partial image. Trigger: rollback rate above 0.5 percent (ILLUSTRATIVE) in any seven-day window | A. Nkemelu | 2026-09-18 |

Row 1 is carried from the campaign risk card unchanged, including the classification sequence: engineering's tuning-change reading, the assessor's ASIL C finding under ISO 26262, and the UN Regulation No. 156 review the finding triggers. The card's own status line reads "Accepted as blocking by the CTO on 2026-03-12 (ILLUSTRATIVE); fleet rollout held pending assessor sign-off"; that block is the same event this row mitigates, and section 3 records the one risk accepted at executive level on the programme as a whole.

## 3. Accepted risks

Risks someone chose to live with, signed. Acceptance without a name is drift.

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| 1 | D. Halloran, CTO, Calderun Systems (executive sponsor, Marrowbank lane-assist OTA campaign) | 2026-09-02 | The fleet rollout is held pending the functional-safety assessor's written ASIL C finding and a completed UN Regulation No. 156 review, accepting the schedule and the customer cost of the held campaign rather than pushing an update whose safety classification engineering and the assessor still disagree on | The assessor's written finding lands, expected 2026-09-25 (ILLUSTRATIVE); revisit at that review and at every weekly review until it does |

## 4. Closed risks

Closed does not mean deleted. The value of this table is the pattern it shows over a year: the same risk closing three times means it was never addressed, only survived.

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| ILLUSTRATIVE prior row: the pre-campaign OTA-LA-2.3.5 push blocked by the same configuration matrix gap on dealer-installed variants | 2026-07-24 | mitigated away: T. Voss's variant enumeration closed the gap before that push went out, and the enumeration is why row 5's trigger exists in this register |

## 5. How this register fails

A register that fails this way still looks like a register, which is the expensive part: the team believes the risk is managed because it is written down. Being written down is not a mitigation.

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| No owner | A row with a score and a date and no human attached | Every row has one named owner. Orphans go to the top of the review, not the bottom |
| **Engineering self-classification** | The team that wrote the change classifies its own safety level. Engineering filed OTA-LA-2.4 as a tuning change, and only the assessor's independent ASIL C finding under ISO 26262 surfaced rows 1 and 3 at all. A register can look complete and still fail this way, because the change never reaches a row: the classification step decided the register's contents before anyone wrote it down | Any change touching vehicle control is classified by someone who did not write it, and the assessor's finding enters the register as a row on the day it is spoken, not the day it is signed. Row 1 names who was told when: D. Halloran told 2026-09-02, three days after the verbal flag |
| Scored once, never revisited | Probability and impact unchanged for quarters while the world moved | Re-score at every review, and flag any row not touched in a month |
| Mitigation restates the risk | "Risk: update fails. Mitigation: prevent the update failing." | A mitigation names an action, an owner and a date, or it is not one |
| Everything is medium | A long list of identical amber rows and no triage | Force a spread. If most rows are medium, nobody has ranked them |
| Closed risks deleted | The history disappears, and the same risk returns next quarter unrecognised | Closed rows are archived, not removed, and reviewed for repeats |
| The register replaces escalation | A serious risk is logged, never raised, and leadership is surprised | Above an agreed threshold, logging is not enough: the row names who was told and when |

## Exit gate

Checkable by someone who does not own any of the rows.

- [x] Every risk is written as an event that could happen, not a topic heading
- [x] Every open risk has a score, an owner, and a review date in the future
- [x] Every score of 6 or higher has an active mitigation with a trigger, not "monitor"
- [x] Every accepted risk is signed by name in section 3
- [x] Findings from the security architecture checklist and dependency register appear here
- [x] A premortem has been run before Gate 3, and its findings are rows above
- [x] The example row has been deleted

Signed: Priya Raghunathan, campaign risk owner, 2026-09-11. All names and dates in this register are ILLUSTRATIVE. Regulatory statements are stated as of 2026-09-11, are not legal advice, and must be confirmed with counsel before reliance.
