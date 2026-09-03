# Migration Cutover Plan: [migration name]

Stage: DELIVER, feeds [Gate 5: release readiness green](../../os/STAGE-GATES.md)
Knowledge: [Premortem worksheet](../../frameworks/execution/premortem-worksheet.md)
Skill: [release-manager-agent](../../agents/release-manager-agent.md)

> **Delete any section you do not need.** A flag flip with no data movement needs only the rollback section of [release-readiness.md](release-readiness.md); this plan is for cutovers that move data, traffic, or customers from one system to another. Weight rules are in [WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- A cutover is a release with a point of no return in it. This plan owns the
     sequence: phases, the rehearsals that prove the sequence, the rollback and
     where it stops being possible, the reconciliation that proves nothing was
     lost, and the comms around the freeze. It does not own the schema strategy
     (../architecture/data-model.md section 6: expand and contract, backfill), the
     go or no-go itself (release-readiness.md), or retiring the old product from
     customers' hands (../operate/sunset-eol-plan.md). Fill section 1, the point
     of no return in section 4, and the reconciliation checks in section 5 first;
     everything else is scheduling. Run the premortem worksheet on the cutover
     window before you commit a date. -->

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved

## 1. Scope and shape

| Field | Value |
|---|---|
| What moves | [data sets, traffic, integrations, customer accounts] |
| From | [system, version, owner] |
| To | [system, version, owner] |
| Cutover shape | [big bang / phased by cohort / parallel run with dual writes / dark launch then flip] |
| Why that shape | [one sentence; the safer shape you rejected, and why] |
| Cutover window | [start and end, timezone; who agreed the window] |
| Freeze | [what stops being writable, from when, for whom] |
| Cutover lead | [one name with authority to abort] |

## 2. Phases

<!-- Every phase has an entry criterion and an exit criterion that a person can
     check, not a feeling. Duration comes from the rehearsal in section 3, never
     from an estimate. -->

| Phase | Entry criteria | Steps (link to the run sheet) | Owner | Duration (from rehearsal) | Exit criteria |
|---|---|---|---|---|---|
| 0. Pre-checks | | | | | |
| 1. Freeze | | | | | |
| 2. Move | | | | | |
| 3. Verify | | | | | |
| 4. Switch traffic | | | | | |
| 5. Unfreeze and watch | | | | | |

## 3. Rehearsal

<!-- A cutover that has not been rehearsed on production-shaped data is a
     hypothesis. Rehearse at least twice: once to find the problems, once to prove
     they are fixed. Record elapsed time; that is where the durations in section 2
     come from. -->

| Rehearsal | Date | Environment | Data volume vs production | Elapsed time | Issues found | Fixed before next run |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |

**Gaps between rehearsal and production that the rehearsal could not cover:** [list, with what mitigates each]

## 4. Rollback

<!-- The point of no return is the phase after which rollback means restore, not
     undo. Name it. Everything before it is cheap to abort; everything after it
     needs the reconciliation in section 5 to prove the restore worked. -->

- Rollback trigger, agreed in advance: [condition a dashboard or a check can show]
- Decision owner during the window: [name] · Reachable via: [channel]
- Point of no return: [phase and step] · Announced how, when reached: [channel]
- Rollback steps before the point of no return: [link, owner, rehearsed on YYYY-MM-DD]
- Restore steps after the point of no return: [link, owner, last restore test YYYY-MM-DD, time it took]
- Data written to the new system after the switch, if we roll back: [kept and replayed / lost and the customers told / other]

## 5. Data reconciliation

<!-- Counts prove nothing was dropped; checksums or samples prove nothing was
     mangled. Tolerance is a field because a tolerance nobody agreed to is a
     surprise nobody signed. A failed check stops the unfreeze. -->

| Check | Source figure | Target figure | Method (count / checksum / sample of n / business total) | Tolerance | Owner | Result |
|---|---|---|---|---|---|---|
| [entity or total] | | | | [agreed tolerance] | | pass / fail |

**Who signs the reconciliation before traffic switches:** [name, role]

## 6. Comms and freeze notices

<!-- Internal before external, support before everyone. The messages themselves
     live in customer-comms.md; if more than two audiences need different
     messages, launch-comms-plan.md owns the schedule and this table links to it. -->

| When (T-n) | Audience | Message | Channel | Owner | Sent |
|---|---|---|---|---|---|
| | Support and on-call | [window, freeze, expected symptoms, escalation path] | | | |
| | Customers affected by the freeze | [what is read-only, from when, for how long] | | | |
| | Integration partners | [endpoint or data changes, dates] | | | |
| T+0 | All | [done, or rolled back, with the agreed wording from customer-comms.md] | | | |

## 7. Cutover run sheet

<!-- The minute-by-minute version of section 2, filled during the final rehearsal
     and executed live. Each go or no-go checkpoint names who says go. -->

| Time | Step | Owner | Checkpoint (go / no-go, by whom) | Done (time, initials) |
|---|---|---|---|---|
| | | | | |

## Exit gate (feeds Gate 5: release readiness green)

A complete plan is the rollback evidence [Gate 5](../../os/STAGE-GATES.md) asks for, and fills section 4 of [release-readiness.md](release-readiness.md).

- [ ] Every phase has entry and exit criteria a person can check, and a duration taken from a rehearsal
- [ ] At least two rehearsals are recorded, and the last one found no unfixed issue
- [ ] The point of no return is named, and restore after it has been tested with the time recorded
- [ ] Every reconciliation check has an agreed tolerance and a named signer
- [ ] Support and on-call are briefed before any customer notice goes out
- [ ] The premortem on the cutover window ran, and its mitigations appear in the phases or the rollback
- [ ] Signed by [name], [date]
