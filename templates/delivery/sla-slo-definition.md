# SLA and SLO Definition: [service or feature name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md); the SLOs are rechecked at Gate 6
Knowledge: [Knowledge index](../../knowledge/INDEX.md)
Skill: [release-manager-agent](../../agents/release-manager-agent.md); the first SLO draft is written at DESIGN by the [architect-agent](../../agents/architect-agent.md)

> **Delete any section you do not need.** An internal feature with no customer contract needs sections 2, 3, 5, and 6 only; delete the SLA section and say so. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- Three layers, often confused. An SLI is a measurement from the user's side.
     An SLO is the internal target for that measurement, which the team commits
     to and alerts on. An SLA is the external promise, written into a contract
     with a remedy attached, and it must be looser than the SLO or every budget
     breach becomes a credit. The first draft of the SLOs is written at DESIGN in
     ../architecture/observability.md section 1; this file is where they become
     agreed targets with owners, an error budget policy, and a review cadence
     before first production traffic. The availability requirement itself was
     set at DEFINE in ../definition/nfr.md section 2; do not reopen it here
     without a change request. What to do when an alert fires belongs to
     support-runbook.md and the engineering runbooks listed in
     ../operate/operational-readiness-review.md.

     Every target below is a bracketed field on purpose. A number written here
     before the team has seen a month of measurement is a wish that will be
     quoted back as a promise. The discipline is based on the ideas in Site
     Reliability Engineering (Beyer, Jones, Petoff, and Murphy, Google, 2016), in
     this repo's own words. Fill the SLI definitions first, then the windows;
     targets last. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Service and users

| Field | Value |
|---|---|
| Service or feature | [name, and the user-facing surfaces it covers] |
| Who depends on it | [customer segments, internal teams, integrations] |
| Criticality tier | [tier, per your org's definitions, with the link] |
| Contract holder for the SLA | [name; "none" if there is no external commitment] |
| Measurement source of truth | [the one system that computes the SLIs] |

## 2. Service level indicators

<!-- Phrase each SLI as good events divided by valid events, from the user's
     side. "Valid" excludes what should not count (health checks, requests
     rejected for bad input); write the exclusion down or someone will game it
     later. Two to four SLIs; more than that and nobody can say which one
     matters. -->

| SLI id | What is measured, in user terms | Good event | Valid event, with exclusions | Measured where |
|---|---|---|---|---|
| SLI-1 | [e.g. expense submissions that complete] | [definition] | [definition, exclusions] | [source] |
| SLI-2 | | | | |

## 3. Service level objectives

<!-- One SLO per SLI. The rationale column earns the row: why this target and
     not one tighter or looser, with the evidence (a month of baseline, a
     customer expectation, a cost curve). The window decides how fast a bad day
     shows up; a long window hides a bad week. -->

| SLI id | Target | Window (rolling or calendar) | Rationale and evidence | Owner |
|---|---|---|---|---|
| SLI-1 | [target] | [window] | [why this number; baseline measured YYYY-MM-DD] | |
| SLI-2 | [target] | [window] | | |

**Baseline measured before targets were set:** [yes, from YYYY-MM-DD to YYYY-MM-DD, source / no, and the date a baseline will exist]

## 4. Service level agreement

<!-- Only if a contract or a published commitment exists. Each SLA line maps to
     an SLO that is stricter, so the team hears about trouble before the customer
     can claim a remedy. Remedies and exclusions are contract language; name who
     owns that text and where it lives. This section records the commitment; it
     does not draft the contract. -->

| Commitment | Backed by SLO | SLA threshold | Remedy | Exclusions (maintenance, force majeure, customer-caused) | Where the contract text lives | Owner |
|---|---|---|---|---|---|---|
| [e.g. monthly availability] | SLI-1 | [threshold, looser than the SLO] | [credit or other remedy] | [list] | [link or document id] | |

## 5. Error budget policy

<!-- The budget is the gap between the target and perfection over the window.
     The policy says what changes when it is spent, and who decides. A policy
     nobody will enforce is decoration; name the person who has said yes to
     enforcing it. -->

| Field | Value |
|---|---|
| Budget per window | [derived from the SLO target and window; state the unit: minutes, failed requests] |
| At [share] of budget consumed | [action: review, slow rollouts, add capacity] |
| Budget exhausted | [action: feature freeze, reliability work first, exceptions granted by whom] |
| Who decides exceptions | [name] |
| Who has agreed to enforce this | [engineering lead name, date] |

## 6. Alert thresholds

<!-- Alert on burn rate against the budget, not on machine internals. Two alerts
     per SLO is usually enough: a fast burn that pages, a slow burn that files a
     ticket. Every page links a runbook that exists. -->

| Alert | SLO | Condition (burn rate or error rate) | Lookback window | Severity (page / ticket) | Routes to | Runbook |
|---|---|---|---|---|---|---|
| | SLI-1 | [condition and threshold] | [window] | page | | [link] |
| | SLI-1 | [condition and threshold] | [window] | ticket | | [link] |

## 7. Review cadence

| Review | Cadence | Attendees | Inputs | Decisions it may take |
|---|---|---|---|---|
| SLO review | [monthly / quarterly] | [owner, on-call lead, product] | [budget consumption, incidents, customer complaints] | [tighten, loosen, or retire an SLO; change the policy] |
| SLA review | [per contract cycle] | [owner, contract holder] | [SLA reports sent, remedies paid] | [renegotiate thresholds or exclusions] |
| Post-incident | [after each budget-affecting incident] | [per ../operate/incident-postmortem.md] | [postmortem] | [add or move an alert] |

## Exit gate (feeds Gate 5: release readiness green)

Filled targets feed the observability line at [Gate 5](../../os/STAGE-GATES.md) and section 5 of [release-readiness.md](release-readiness.md); the SLO review feeds [metrics-review.md](../operate/metrics-review.md) at Gate 6.

- [ ] Every SLI states good events, valid events, and the exclusions, and names one measurement source
- [ ] Every SLO has a target, a window, a rationale with evidence, and an owner
- [ ] A baseline was measured before targets were set, or the date one will exist is written down
- [ ] Every SLA threshold is looser than the SLO behind it, and its contract text has an owner and a location
- [ ] The error budget policy names actions at each stage and the person who agreed to enforce it
- [ ] Every paging alert links a runbook that exists
- [ ] Signed by [name], [date]
