---
layer: templates
stage: DESIGN
gate: 3
feeds: []
method: "knowledge/cagan-product-teams.md"
aliases: ["Risk Register", "risk-register"]
---
# Risk Register: `<initiative name>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md), reviewed weekly through DELIVER
Knowledge: [Cagan on the four risks](../../knowledge/cagan-product-teams.md)
Skill: [program-premortem](../../skills/program-premortem/SKILL.md)

<!-- A risk register that is written once and read never is a rain dance. This one is
     a living table with a weekly review slot and a premortem pass before Gate 3.
     Seed it from the four product risk categories described in Marty Cagan's work
     (value, usability, feasibility, viability), plus delivery and security risks
     from the registers that feed this document. The premortem skill runs against
     this file: it assumes the initiative has failed and asks what killed it. -->

**Initiative:** `<name>` · **Register owner:** `<name>` · **Review cadence:** weekly, `<day and meeting>`
**Last reviewed:** `<YYYY-MM-DD>` · **Premortem run:** `<YYYY-MM-DD, or "not yet">`

## 1. Scoring

<!-- Likelihood and impact each score 1 to 3 (low, medium, high). Score = L x I,
     range 1 to 9. At 6 or above the risk needs an active mitigation with a date, not
     a watching brief. Keep the scale coarse on purpose: a 5-point scale invents
     precision the estimates do not have. -->

## 2. The register

<!-- Response is one of: mitigate (act to reduce), accept (named person accepts it in
     writing), transfer (contract or insurance), avoid (change the plan). "Monitor"
     is not a response; it is a synonym for accept without the signature. The
     example row shows the expected precision; delete it once real rows exist. -->

| # | Risk (event, not a vague noun) | Category (value / usability / feasibility / viability / delivery / security) | L | I | Score | Response | Mitigation and its trigger | Owner | Review date |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Counterparty sandbox not available before integration testing starts | delivery | 2 | 3 | 6 | mitigate | build against recorded fixtures; escalate to vendor account manager if sandbox absent by `<date>` | `<name>` | `<date>` |
| | | | | | | | | | |

## 3. Accepted risks

<!-- Risks someone chose to live with, signed. This section is what makes "accept"
     honest: acceptance without a name is drift. -->

| Register # | Accepted by (name, role) | Date | Rationale in one sentence | Revisit when |
|---|---|---|---|---|
| | | | | |

## 4. Closed risks

| Register # | Closed on | How it resolved (did not occur / occurred, impact was ... / mitigated away) |
|---|---|---|
| | | |

## Exit gate

- [ ] Every risk is written as an event that could happen, not a topic heading
- [ ] Every open risk has a score, an owner, and a review date in the future
- [ ] Every score of 6 or higher has an active mitigation with a trigger, not "monitor"
- [ ] Every accepted risk is signed by name in section 3
- [ ] Findings from the security architecture checklist and dependency register appear here
- [ ] A premortem has been run before Gate 3, and its findings are rows above
- [ ] The example row has been deleted
