# Sunset / End-of-Life Plan: [product or feature name]

**Stage:** OPERATE (executes the SUNSET decision from [Gate 6: outcomes verified, learn or sunset](../../os/STAGE-GATES.md))
**Knowledge:** [knowledge index](../../knowledge/INDEX.md)
**Skill:** [drafting agent](../../agents/drafting-agent.md)

<!-- The loop this repository promises runs discovery to sunset, and this is the
     sunset. A shutdown is a launch in reverse and deserves the same discipline:
     users remember how a product ends longer than how it began, and the ones you
     migrate well are the ones who trust the next thing you ship.

     The decision itself was made in the metrics review; this file never argues it,
     it executes it. If you find yourself relitigating the decision here, stop and
     take it back to that document. One discipline throughout: dates in this file
     are commitments to users, not roadmap estimates, so pad them once, in private,
     before anything is announced. -->

**Owner:** [name] · **Decision source:** [link to the metrics-review.md copy with the SUNSET decision] · **Decided:** [YYYY-MM-DD]
**Shutdown date (public):** [YYYY-MM-DD] · **Last updated:** [YYYY-MM-DD]

## 1. The decision

- Rationale, two sentences, from the metrics review: [quoted]
- Decider: [name] · What would have reversed it: [the evidence that never arrived]
- What this sunset frees up: [team, spend, roadmap room; the reason worth stating internally]

## 2. Who is affected

| Segment | Count | Revenue or usage at stake | Contractual obligations (notice period, SLA) | Regulator notice needed |
|---|---|---|---|---|
| | | | | yes / no |

- If any regulated obligation applies, run the [compliance impact assessment](compliance-impact-assessment.md) before announcing anything.

## 3. Migration path

<!-- The most important table in the file. "Destination" can be our other product,
     a competitor we name honestly, or a data export and goodbye. An affected
     segment with no row here is a support fire with a date on it. -->

| Segment | Destination | What they must do | By when | Help offered (docs / tooling / humans) | Owner |
|---|---|---|---|---|---|
| | | | | | |

- Data export: [format, where, available until YYYY-MM-DD]
- Pricing or refund handling for prepaid customers: [rule, owner]

## 4. Timeline

<!-- Every stage gets a date and an owner. The gap between announce and shutdown is
     the users' time, not ours; contractual notice periods in section 2 set its floor. -->

| Stage | Date | Owner | Done |
|---|---|---|---|
| Internal announce and support briefing | | | |
| Public announce | | | |
| New signups / sales stop | | | |
| Feature freeze (security fixes only) | | | |
| Read-only mode | | | |
| Shutdown | | | |
| Data deletion complete | | | |

## 5. Comms cascade

<!-- Internal before external, support before everyone; reuse the discipline of the
     [launch comms plan](../delivery/launch-comms-plan.md) in reverse. Every message
     states the shutdown date, the migration path, and the data deadline. -->

| Audience | Message owner | Channel | Date | Sent |
|---|---|---|---|---|
| | | | | |

## 6. Decommission steps

- [ ] Billing stopped and final invoices handled: [owner]
- [ ] Integrations and API consumers notified and disconnected (see ../architecture/integrations.md register): [owner]
- [ ] Infrastructure torn down, recurring costs at zero: [owner, verified how]
- [ ] Monitoring and alerts retired, on-call rotation updated: [owner]
- [ ] Public docs, marketing pages, and app store listings removed or archived: [owner]
- [ ] Contracts and vendor commitments closed out: [owner]

## 7. Post-sunset check

- On [YYYY-MM-DD, 30 days after shutdown]: data deletion verified, costs confirmed at zero, by [name]
- What this product taught us, one paragraph, logged in ../execution/decision-log.md: [link to the entry]

## Exit gate

This plan is done when:

- [ ] Every affected segment has a migration row with a date and an owner
- [ ] The timeline respects every notice period in section 2
- [ ] Support is briefed before the public announcement
- [ ] Every decommission box has a named owner
- [ ] The post-sunset check has a date and a person

Signed: [name], [role], [YYYY-MM-DD]
