# Release Readiness: [product or feature name]

**Stage:** DELIVER (this file IS [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- This is the go or no-go working document and the launch checklist in one place.
     The gate passes when every box below is honestly checkable, not when the meeting
     ends. A box you cannot check goes to the known-issues table with an owner, or it
     stops the release. Ticking a box to be polite moves the failure to production. -->

**Release:** [version or milestone] · **Target date:** [YYYY-MM-DD]
**Decider:** [one named person] · **Decision:** GO / NO-GO / GO WITH CONDITIONS
**Decision date:** [YYYY-MM-DD]

## 1. Features

- [ ] Everything in the PRD's launch scope is built, and nothing extra shipped unreviewed
- [ ] Scope cuts since sign-off are listed here: [list, or "none"]
- [ ] Acceptance criteria all pass (Gate 4 evidence: [link or location])

## 2. Tests

- [ ] Every blocking level in the [testing strategy](testing-strategy.md) ran and passed
- [ ] The [edge-case register](edge-cases.md) has no open rows
- [ ] [UAT](uat-plan.md) is signed off, conditions listed below if any
- [ ] For AI features: eval thresholds met per the [eval spec](../ai/eval-spec.md), and the [red-team review](../ai/red-team-review.md) is closed

## 3. Known issues shipping with this release

<!-- An empty table on a real product is a red flag, not a green one. -->

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| | | | | | |

## 4. Rollback

- [ ] Rollback procedure exists and was tested on [environment], on [YYYY-MM-DD]
- Rollback trigger, agreed in advance: [the condition that forces rollback, a number where possible]
- Rollback owner: [name] · Time to roll back: [n minutes]
- Data written between release and rollback: [what happens to it]

## 5. Operations and monitoring

- [ ] Dashboards and alerts for this release are live (see [observability](../architecture/observability.md))
- [ ] [Failure scenarios](failure-scenarios.md) reviewed with the on-call owner
- [ ] The [operational readiness review](../operate/operational-readiness-review.md) is complete

## 6. Communications

| Audience | What they get | Owner | Sent |
|---|---|---|---|
| Support team | [briefing, known issues, escalation path] | | |
| Internal stakeholders | [release note] | | |
| Customers | [announcement or changelog, or "silent release"] | | |

## 7. Regulated overlay

- [ ] Does this release touch a product under a financial or data regulator? If yes, the regulated module was run via the [reg-gap-check skill](../../skills/reg-gap-check/SKILL.md) and the [compliance impact assessment](../operate/compliance-impact-assessment.md) is signed. If no, write why: [reason]

## 8. Sign-offs per function

<!-- A sign-off is a name, not a team. "Engineering" cannot be paged. -->

| Function | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| Product | | | | |
| Engineering | | | | |
| QA | | | | |
| Design | | | | |
| Support | | | | |
| Data | | | | |
| Legal / Compliance (if section 7 is yes) | | | | |

## Exit gate

Gate 5 is green when:

- [ ] Every checklist box above is checked, or its exception sits in the known-issues table with an owner and a date
- [ ] The rollback trigger is a condition a dashboard can show, not a feeling
- [ ] Every sign-off row has a name and a date
- [ ] The decider recorded GO, NO-GO, or GO WITH CONDITIONS, with conditions in writing

Signed: [decider name], [role], [YYYY-MM-DD]
