# Risk Register: DashCrate Q3 Expansion and Cold-Chain Integrity

Fills [templates/execution/risk-register.md](../templates/execution/risk-register.md). Everything here is invented for this standalone example: DashCrate is a fictional quick-commerce operator, Priya Nakamura its only fictional head of legal, and every number, name and date is ILLUSTRATIVE, not drawn from any real company or market. There is no external DashCrate journey or data sheet. See the [examples index](README.md).

**Initiative:** DashCrate Q3 Expansion · **Register owner:** Marcus Chen, VP Operations · **Review cadence:** weekly, Tuesday Ops Review
**Last reviewed:** 2026-09-11 · **Premortem run:** 2026-08-25

## 1. Scoring

Likelihood and impact each score 1 to 3 (low, medium, high). Score = L x I, range 1 to 9. At 6 or above the risk needs an active mitigation with a date, not a watching brief. Keep the scale coarse on purpose: a 5-point scale invents precision the estimates do not have.

## 2. The register

Response is one of: mitigate (act to reduce), accept (named person accepts it in writing), transfer (contract or insurance), avoid (change the plan). "Monitor" is not a response; it is a synonym for accept without the signature. The example row shows the expected precision; delete it once real rows exist.

| # | Risk (event, not a vague noun) | Category (value / usability / feasibility / viability / delivery / security) | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| R1 | DashCrate's dispatch-and-deactivation logic is found to exercise enough direction and control that couriers are presumed employees under the EU platform-work directive in a launched member state | viability | 2 | 3 | 6 | mitigate | Legal review of the dispatch algorithm's control indicators against the transposed national law before entering that market; a published, human-reviewable deactivation-appeal process on a fixed clock, so the presumption's "direction and control" test has a countervailing fact on file | Priya Nakamura, Head of Legal | 2026-11-30 |
| R2 | A cold-chain excursion occurs in a dark store due to equipment failure during peak demand, resulting in spoilage of perishable inventory and potential food-safety complaints | delivery | 2 | 3 | 6 | mitigate | Install redundant cooling units with automated alerts; implement a 15-minute manual check protocol during peak hours; verify temperature logs against local food-safety authority standards (EU markets: national implementation of Regulation (EC) No 852/2004 on the hygiene of foodstuffs) daily | Sarah Jenkins, Dark Store Manager | 2026-10-15 |
| R3 | Per-order unit economics collapse if subsidy rates drop below current levels, as contribution margin per order is negative $0.45 at current courier pay and commission structures | viability | 3 | 3 | 9 | accept | None; see Section 3 for acceptance rationale | Elena Rodriguez, CEO | 2026-09-11 |
| R4 | Algorithmic management practices violate the automated-monitoring and decision-making transparency duties under Chapter III (Articles 6 to 8) of Directive (EU) 2024/2831, distinct from R1's worker-classification exposure | compliance | 2 | 3 | 6 | mitigate | Conduct audit of all automated decision systems against Articles 6 to 8 (transparency, human monitoring, human review of significant decisions); prepare documentation for regulator inquiry; ensure human-in-the-loop review for deactivations | Priya Nakamura, Head of Legal | 2026-12-01 |
| R5 | City zoning authorities revoke or restrict permits for dark stores in new expansion markets due to traffic and noise concerns | feasibility | 2 | 2 | 4 | mitigate | Engage local planning departments early; propose off-peak delivery windows; secure conditional permits with community benefit agreements | David Park, Government Affairs Lead | 2026-10-30 |
| R6 | Rider safety incidents increase due to pressure to meet 15-minute delivery promises, leading to regulatory scrutiny and reputational damage | delivery | 3 | 3 | 9 | mitigate | Adjust promise window to 20 minutes in pilot zones; remove penalty-based incentives for late deliveries; publish safety metrics alongside delivery time metrics | Marcus Chen, VP Operations | 2026-10-01 |

## 3. Accepted risks

Risks someone chose to live with, signed. This section is what makes "accept" honest: acceptance without a name is drift.

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| R3 | Elena Rodriguez, CEO | 2026-09-11 | Growth is prioritized over profitability in this quarter to capture market share before competitors consolidate their own dark-store networks. | When competitor exit signals appear or subsidy burn rate exceeds $2M/month threshold |

## 4. Closed risks

Closed does not mean deleted. The value of this table is the pattern it shows over a year: the same risk closing three times means it was never addressed, only survived.

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| R0 | 2026-08-15 | Did not occur for the Berlin launch itself; closed as a launch-event risk, not as a resolution of the underlying exposure, because Directive (EU) 2024/2831's national transposition deadline (2026-12-02) had not yet passed at launch. R1 stays open because it tracks the same exposure going forward, across all markets and past that deadline. |

## 5. How this register fails

A register that fails this way still looks like a register, which is the expensive part: the team believes the risk is managed because it is written down. Being written down is not a mitigation.

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| No owner | A row with a score and a date and no human attached | Every row has one named owner. Orphans go to the top of the review, not the bottom |
| Scored once, never revisited | Probability and impact unchanged for quarters while the world moved | Re-score at every review, and flag any row not touched in a month |
| Mitigation restates the risk | "Risk: outage. Mitigation: prevent the outage." | A mitigation names an action, an owner and a date, or it is not one |
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

Signed: Marcus Chen, VP Operations, 2026-09-11
