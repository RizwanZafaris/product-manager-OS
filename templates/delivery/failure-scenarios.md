# Failure Scenarios: [product or feature name]

**Stage:** DELIVER (feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- Edge cases are inputs the product must handle. Failure scenarios are the ways the
     system around the product breaks: a dependency goes down, a queue backs up, a
     deploy half-lands. Write this before launch, because the first production incident
     is a bad time to discover nobody knows the recovery steps.

     Sourcing rule: every external dependency in the integration map gets at least one
     row here, and every single point of failure in the system design gets one. Start
     from ../execution/dependency-register.md and ../architecture/integrations.md. -->

**Owner:** [name] · **Reviewed with:** [on-call lead name] · **Date:** [YYYY-MM-DD]

## 1. Scenario table

<!-- Detection means "how we know within minutes, without a customer telling us".
     If the honest answer is "a customer tells us", write that, and open a monitoring
     gap in section 2. Recovery names steps, an owner, and a time estimate.
     The italic row shows a completed entry. -->

| ID | Scenario | Blast radius | Detection | Recovery | Data loss risk |
|---|---|---|---|---|---|
| FS-1 | | [who and what is affected, worst case] | [alert, dashboard, or "customer report"] | [steps, owner, time to recover] | [none / possible: which data] |
| FS-2 | | | | | |
| *FS-0* | *receipt-storage service unavailable* | *new uploads fail for all users, existing data unaffected* | *upload error rate alert at 5% over 5 minutes* | *queue uploads client-side, retry on recovery; owner: platform on-call; expected under 30 minutes* | *none, retries are durable* |

## 2. Monitoring gaps found while writing this

<!-- Every "we would not know" discovered above becomes a row here and a change
     request against ../architecture/observability.md. -->

| Gap | Fix | Owner | Date |
|---|---|---|---|
| | | | |

## 3. Rehearsal

- Scenarios rehearsed (game day or tabletop), with dates: [list, or "none yet" plus a scheduled date]
- The scenario we most doubt our recovery steps for: [ID plus one sentence why]

## Exit gate

This document passes when:

- [ ] Every external dependency has at least one scenario row
- [ ] Every row states detection, and "customer report" answers created a section 2 gap
- [ ] Every recovery names an owner and a time estimate, not just steps
- [ ] Data loss risk is stated per row, including "none"
- [ ] At least the highest blast-radius scenario has a rehearsal date

Signed: [name], [role], [YYYY-MM-DD]
