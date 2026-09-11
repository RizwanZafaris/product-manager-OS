# Release Readiness: Renew, national benefits renewal

Fills [templates/delivery/release-readiness.md](../templates/delivery/release-readiness.md). Everything here is invented: Renew is a fictional national benefits-renewal service run by a fictional agency, the Directorate of Social Support; every name, role, date, service level and count is ILLUSTRATIVE, carried from the domain card's worked Renew slice so it can be checked against [public-sector-govtech](../knowledge/domains/public-sector-govtech.md), and not describing any real service. See the [examples index](README.md).

**Owner:** Adaeze Nnamdi, service owner · **Date:** 2026-09-11 · **Status:** This file carries the domain card's Renew slice unchanged, plus the rows that slice leaves out: identity-proofing failure fallback, records retention and freedom-of-information, plain-language reading age, and phased regional rollout

**Release:** Rel-1, Renew digital renewal service · **Target date:** 2026-09-28
**Decider:** Adaeze Nnamdi, service owner · **Decision:** NO-GO at 2026-09-11 · **Decision date:** 2026-09-11 · **Held before any production rollout:** yes

The decision at this reading is NO-GO. The renewal service has three open NO-GO rows against it. No flag has been flipped; nothing runs in production; this file is the working document, not a record of a launch.

## 1. Features

- [x] Everything in the PRD's launch scope is built, and nothing extra shipped unreviewed
- [x] Scope cuts since sign-off are listed here: none
- [x] Acceptance criteria all pass (Gate 4 evidence: shared drive, Renew/Renewals/Gate4-acceptance, last updated 2026-09-08)

The Renew digital renewal service did not exist before Rel-1. There was no earlier digital channel to cut scope against. The slice in the domain card is the whole of Rel-1: digital renewal for the main benefit type, the assisted phone channel for those who cannot use it, and the identity, records and language duties that attach to a population-scale service.

## 2. Tests

- [x] Every blocking level in the [testing strategy](../templates/delivery/testing-strategy.md) ran and passed
- [x] The [edge-case register](../templates/delivery/edge-cases.md) has no open rows
- [ ] [UAT](../templates/delivery/uat-plan.md) is signed off, conditions listed below if any: NOT signed off. Two screen-reader users completed 6 of 8 tasks on 2026-08-14 with two blocking findings on the payment-confirmation step, carried unchanged from the domain card. UAT cannot sign until those two findings are fixed and retested
- [x] For AI features: not applicable. Renew contains no AI or machine-learning feature. Section 7 answers the regulated question on that basis

Accessibility testing under this gate is tested with assistive-technology users, screen reader, voice control and switch access, against WCAG 2.2 level AA. An automated scanner alone is not accepted as evidence at any blocking level here, per the domain card: a page can pass every automated check and still be unusable with a screen reader. The manual session of 2026-08-14 is the record that matters, and it recorded two blocking failures. Those failures stop the launch, not merely the accessibility line.

## 3. Known issues shipping with this release

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| 1 | Screen-reader users hit the payment-confirmation step: 6 of 8 tasks completed, two blocking findings (domain card row, 2026-08-14) | high | Not acceptable. This is a condition, not a known issue | Accessibility lead, name to be confirmed | Fixed and retested before any rollout |
| 2 | No failover rehearsal has been held for the peak renewal-deadline day | high | Not acceptable. This is a condition, not a known issue | Engineering lead, name to be confirmed | Rehearsal held and timed before any rollout |
| 3 | Caseworker notes field untested for freedom-of-information redaction | medium | The records export itself works and redaction is confirmed for three of four protected fields. The fourth is a gap with an owner and a dated fix, and no request has yet reached the live service because nothing is live | Records officer, name to be confirmed | Before the system carries any live record |
| 4 | Assisted phone channel capacity is a separate go/no-go row, not yet staffed for launch week | high | Not acceptable. This is a condition, not a known issue | Service delivery lead, name to be confirmed | Staffing confirmed at 3x normal call volume before any rollout |

## 4. Rollback

- [ ] Rollback procedure exists and was tested: NOT yet. No rehearsal has been executed. The peak-day load test held on 2026-08-18 reached 4x average traffic with p95 under 2 seconds, but a load test is not a failover rehearsal, and until that rehearsal runs the rollback line is a document, not evidence
- Rollback trigger, agreed in advance: any of the following forces rollback without further discussion: reported duplicate benefit renewals per thousand submissions above the level recorded at the last rehearsal; any confirmed material disclosure of personal data; or the assisted phone channel dropping below the answer target for two consecutive hours on a renewal-deadline day. The numbers that make those rows checkable are set at the failover rehearsal, which is a condition on this gate and has not yet happened
- Rollback owner: Engineering lead, name to be confirmed · Time to roll back: not yet recorded, because the rehearsal that produces the number has not been run
- Data written between release and rollback: any renewal submission accepted before rollback must be reconciled. Because the failing rows here already block launch outright, no case exists yet where a citizen's record could be stranded, which is the reason a NO-GO at this reading is cheaper than a conditioned GO

## 5. Operations and monitoring

- [ ] Dashboards and alerts for this release are live (see [observability](../templates/architecture/observability.md)): NOT yet live. The assisted phone channel needs its own alert, not an inference from system health. A dashboard that shows the digital service green through an outage on the phone line is not evidence the service is working
- [ ] [Failure scenarios](../templates/delivery/failure-scenarios.md) reviewed with the on-call owner: NOT yet reviewed. The domain card names peak-day failure at a renewal deadline as a front-page event, so this review is a condition on this gate, not a later task
- [ ] The [operational readiness review](../templates/operate/operational-readiness-review.md) is NOT complete

The assisted phone channel is staffed and monitored as its own go/no-go row, in section 1 and section 3 alongside the digital rows. The domain card's assisted-channel volume metric can fall because self-service improved or because people gave up and the need went unmet, so the channel is measured for whether it can absorb launch-week demand, not only for how many calls it takes.

## 6. Communications

| Audience | What they get | Owner | Sent |
|---|---|---|---|
| Support team (caseworkers and phone-channel staff) | Briefing on the two open accessibility findings, the assisted channel staffing, and the escalation path for anyone who cannot complete identity proofing | Service delivery lead, name to be confirmed | Before any rollout, condition on the gate |
| Internal stakeholders | Release note covering digital renewal, the assisted channel, and the phased regional rollout plan | Adaeze Nnamdi | Before the first regional wave |
| Citizens (benefit recipients) | Phased regional announcement, region by region, with the phone and assisted routes named in every region alongside the digital route | Service owner, with the communications lead | Before each regional wave, phased by region, not one national announcement |

The national records or archives authority and the information commissioner are named under section 7, not here, since they are oversight bodies with a statutory relationship to the service rather than an audience to be briefed on a release date.

## 7. Regulated overlay

- [x] This release does not touch a product that contains an AI or machine-learning feature. Renew has no model in it. The question of whether the reg-gap-check skill and the compliance impact assessment apply on that basis is answered by the domain card, which records that a regulated release with no model in it records what the regulatory owner used instead. Here: no model, so section 7 records the duties that do apply

The duties this release does carry, all stated as of 2026-09-11 and each to be confirmed with counsel before rollout, and not legal advice:

- **Accessibility:** tested with assistive-technology users against WCAG 2.2 level AA, not with a scanner alone. WCAG is a conformance standard, not a self-declaration. A failed test blocks launch outright, which is the rule this gate holds to. Match to your own jurisdiction's accessibility law, whether that is the EU's Web Accessibility Directive, Directive (EU) 2016/2102, and EN 301 549, US Section 508 of the Rehabilitation Act, or the national equivalent. Confirm with counsel which instrument applies to Renew
- **Records retention and disposal:** a retention and disposal schedule decided by the national records or archives authority governs, not database defaults. Renew's schedule is set against the agency's own records policy; the fields and their retention periods are held on the schedule owned by the records officer. Confirm with counsel and the records authority
- **Freedom of information:** the system must be able to produce and redact its own records on the statutory clock. The records export was tested against a sample request on 2026-08-10, with redaction confirmed for three of four protected fields; the caseworker notes field is the one gap, carried in section 3. Whether that gap is material to the statutory clock is a question for counsel. The UK and US Freedom of Information Acts (2000 for the UK, 1966 for the US) are the named baselines the domain card points at; Renew's regime is to be confirmed
- **Identity proofing:** if the identity check fails, what happens to the person who cannot pass it, no documents, no smartphone, no fixed address. This is written as a fallback, not an error state: a person who cannot pass proofing is routed to the assisted phone channel, which must be staffed to receive them. That route is a condition on this gate, tied to row 4 of section 3, and it is the reason the identity-proofing fallback and the assisted-channel capacity row cannot be signed separately
- **Plain-language reading age:** the renewal journey is checked for the reading age the agency's own content standard requires. This is tested as a requirement on this gate, not a nicety. A reading-age check that fails is a fallback-design issue, since the whole point of the fallback above is that someone who cannot read the digital page can still renew. Confirm with counsel

## 8. Sign-offs per function

| Function | Name | Verdict | Conditions | Date |
|---|---|---|---|---|
| Product | Adaeze Nnamdi | NO-GO | Not conditional. Three open rows, one condition per row, listed below | 2026-09-11 |
| Engineering | Name to be confirmed | NO-GO | Failover rehearsal held and timed before any rollout | 2026-09-11 |
| QA | Name to be confirmed | NO-GO pending retest | The two blocking accessibility findings fixed and retested before UAT signs | 2026-09-11 |
| Design | Name to be confirmed | GO with conditions | Plain-language reading-age check passed, and the identity-proofing fallback route reviewed with the service delivery lead | 2026-09-11 |
| Support | Name to be confirmed | NO-GO | Assisted phone channel staffing confirmed at 3x normal call volume before rollout, per row 4 of section 3 | 2026-09-11 |
| Data | Name to be confirmed | GO with conditions | Caseworker notes field redaction tested before the system carries any live record | 2026-09-11 |
| Legal / Compliance | Name to be confirmed | GO with conditions | Records retention schedule and freedom-of-information export signed off with counsel and the records authority before rollout; this is the regulatory-owner role, signed on the no-model basis recorded in section 7 | 2026-09-11 |
| Senior responsible owner | Name to be confirmed | NO-GO | Accountable for the program to the department and its audit committee. Will not authorise any rollout wave while any section 3 condition is open | 2026-09-11 |
| Service assessment panel | By role, panel chair | GO with conditions | Assessment to be re-run before the phased regional rollout begins and after the two accessibility findings are closed. Assessed against the published service standard, and this row is the panel's verdict by role, not a personal sign-off | 2026-09-11 |

The senior responsible owner and the service assessment panel sign by role, which is the accountability structure this service runs on. Every other row is a named person who can be paged, because a role cannot be asked what it meant six months later.

## 9. How this gate fails while looking like it passed

| Failure mode | What it looks like in the room | The rule that stops it |
|---|---|---|
| Accessibility accepted from a scanner | "The automated tool passes at 98 percent, so accessibility is fine" | Assistive-technology testing against WCAG 2.2 AA is required, and a failed test blocks launch outright, per section 2 |
| Assisted channel assumed, not staffed | "People can always phone us" said while the phone line is unstaffed for launch week | Assisted channel capacity is its own go/no-go row, per section 3 row 4 |
| Identity-proofing failure treated as an error | The person who cannot pass the check is shown a generic error with no route out | A named fallback: route to the assisted phone channel, which must be staffed to receive them, per section 7 |
| Records duty treated as a database default | Retention and disposal decided by what is convenient to store | A schedule set by the national records or archives authority, per section 7 |
| Freedom-of-information readiness checked on one field | Redaction confirmed for some fields and assumed for the rest | The export must produce and redact on the statutory clock; the gap lands as a dated row in section 3, per section 7 |
| Rollback as a document | "We have a rollback plan" on a slide, no rehearsal, no timing | A rehearsal in a real environment, with the elapsed time recorded, per section 4, and this gate does not clear without it |
| Green dashboard, wrong metric | Every tile green while the phone line is dropping calls | Name the indicators tied to the assisted channel and this release's user-visible behaviour, per section 5 |
| Sign-off by team, not person | "The panel approves," written by whoever held the document | Named sign-offs with role and date, with the senior responsible owner and the panel signing by role on the terms above, per section 8 |
| Gate held after the release | The flag was flipped, notes to be backfilled | Held before any production rollout, and the header says so, per the header block |

## Exit gate

Gate 5 is green when:

- [ ] Every checklist box above is checked, or its exception sits in the known-issues table with an owner and a date: NOT yet. Four rows sit in section 3, three of them conditions rather than known issues, and the failover rehearsal, the operational readiness review, and the UAT sign-off all remain open
- [x] The known-issues table is not empty, and its emptiness is not explained away: four rows, three of them conditions, one a dated gap
- [x] Every known issue distinguishes itself from a condition: rows 1, 2 and 4 are conditions and may not ship open; row 3 is a dated gap with an owner and a fix date
- [ ] The rollback trigger is a condition a dashboard can show, not a feeling, and the procedure was executed on a dated environment: NOT yet. The trigger is written, but the rehearsal has not run
- [x] Every sign-off row has a name or a role with a date, and every conditional verdict has its condition written in the row
- [x] The decider recorded GO, NO-GO, or GO WITH CONDITIONS, with conditions in writing: NO-GO at 2026-09-11
- [x] This gate was held before any production rollout, and the header says so
- [x] Section 7 is answered even where the answer is no, with the reason written: no model, so the duties that do apply are recorded, with confirm-with-counsel noted

Signed: Adaeze Nnamdi, service owner and decider, 2026-09-11. NO-GO. The gate is held before any production rollout; nothing runs in production, and no sign-off here is retroactive. The senior responsible owner and the service assessment panel signed the same date by role, on the conditions recorded in section 8.
