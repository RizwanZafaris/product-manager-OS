# UAT Plan: [product or feature name]

**Stage:** DELIVER (feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- User acceptance testing answers one question the team cannot answer for itself:
     does this work for the people who will actually use it, doing their actual job?
     UAT is not a second QA pass. QA proves the product matches the spec; UAT proves
     the spec matched reality. Recruit testers who own the workflow, not stand-ins. -->

**Owner:** [name] · **Business sponsor:** [name] · **Window:** [YYYY-MM-DD] to [YYYY-MM-DD]

## 1. Scope

- Flows under acceptance: [list the end-to-end jobs, not screens]
- Explicitly out of scope: [list, with reason]
- Basis documents: [../definition/prd.md copy] · [../definition/acceptance-criteria.md copy]

## 2. Entry criteria

UAT starts only when all of these hold:

- [ ] QA exit criteria from the [testing strategy](testing-strategy.md) are met
- [ ] No open S1 or S2 defects on the flows in scope
- [ ] The UAT environment is seeded with realistic, non-production data: [environment name]
- [ ] Testers below are confirmed and have access
- [ ] [add product-specific entry conditions]

## 3. Testers

<!-- Name real people with the real job. "Someone from finance" is not a tester.
     Time commitment is agreed with their manager before the window opens. -->

| Name | Role | Workflow they own | Time committed | Confirmed |
|---|---|---|---|---|
| | | | [hours across the window] | yes / no |

## 4. Test charters

<!-- Charters, not scripts. Tell testers the job to attempt and what "done" looks
     like; let them take their own path. Scripted clicks find what QA already found.
     The italic row shows a completed entry. -->

| # | Charter (the job to attempt) | Done looks like | Tester | Result |
|---|---|---|---|---|
| 1 | | | | Pass / Fail / Blocked |
| *0* | *file last month's expenses end to end, including one foreign-currency receipt* | *report submitted, totals match the receipts, no manual re-entry* | *[name]* | *Pass* |

## 5. Defect handling during UAT

| Severity | Meaning during UAT | Action |
|---|---|---|
| S1 | Tester cannot complete a scoped job at all | UAT pauses, fix before resuming |
| S2 | Scoped job completes only with a workaround | Fix inside the window or sponsor accepts in writing |
| S3 / S4 | Friction or cosmetic | Logged, prioritized after launch |

- Defects logged in: [tracker link or location] · Triage cadence during the window: [daily]

## 6. Exit criteria and sign-off

UAT passes when:

- [ ] Every charter has run, and none is Blocked
- [ ] No open S1; every accepted S2 has the sponsor's written acceptance attached
- [ ] Testers answered "would you use this over the current way?" and the answers are recorded: [location]

**Sign-off form**

| Name | Role | Verdict (Accept / Accept with conditions / Reject) | Conditions, if any | Date |
|---|---|---|---|---|
| | Business sponsor | | | |
| | Product owner | | | |

## Exit gate

This document passes when:

- [ ] Testers are named individuals who own the workflow, with committed time
- [ ] Charters describe jobs, not click scripts
- [ ] Entry and exit criteria are objective enough to be applied without a meeting
- [ ] The sign-off form is complete, including any conditions in writing

Signed: [name], [role], [YYYY-MM-DD]
