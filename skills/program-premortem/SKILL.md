---
name: program-premortem
description: Run a premortem on a program plan against the twelve ways program managers actually fail. Use when a program is approaching kickoff, a major cutover, or Gate 3, or when status "feels fine" but nobody can prove it. Takes a plan, status pack, or verbal description and returns which failure modes are already present, with the evidence and the smallest intervention for each.
---

# Program Premortem: the twelve ways program managers fail

Programs rarely die from the risk on the register. They die from patterns everyone has seen and nobody names in time. This skill names them, checks the plan against each, and prescribes the smallest intervention that changes the outcome.

## Files this skill drives

- [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md), where PRESENT findings land as owned risks
- [../../templates/execution/dependency-register.md](../../templates/execution/dependency-register.md), the evidence base for modes 1 and 6
- The premortem runs before Gate 3 of [../../os/STAGE-GATES.md](../../os/STAGE-GATES.md); its findings are inputs to that gate's review

## When to use

- Before kickoff of anything with 3 or more teams or an external dependency
- Before a cutover, migration, or regulated go-live
- Before Gate 3, as the risk half of "architecture and risks reviewed"
- When status has been green for six weeks and your instinct disagrees

## The twelve failure modes

1. **The date list wearing a plan costume.** Milestones exist; the dependency graph does not. Test: pick any milestone and ask what specifically must finish first, owned by whom. If the answer is a meeting, not an artifact, this mode is present. The dependency register is the artifact.
2. **RAID theater.** Risks are logged weekly and escalated never. Test: find one risk that changed a decision in the last month. None found = the register is decoration.
3. **Governance without decision rights.** A steering committee that receives updates but cannot kill, fund, or resequence anything. Test: name the last decision the forum actually made. "Noted" is not a decision.
4. **Watermelon reporting.** Green outside, red inside. Driven by status derived from activity ("workstream engaged") instead of exit criteria ("reconciliation matched at N% on the test file"). Test: does any green line carry a number?
5. **The unrehearsed cutover.** Go-live is a date, not a runbook. No dry run, no rollback criteria, no named abort authority. Programs survive bad plans; they do not survive unrehearsed cutovers of money-moving systems.
6. **Dependencies managed by hope.** The other team "knows about it." Test: is the dependency in THEIR committed plan with a date, or only in yours?
7. **The unowned exceptions queue.** The program builds the happy path; the exception flow (unmatched items, failed callbacks, manual reviews) has no owner and no SLA, and it becomes the operational debt that eats year two.
8. **Scope ratchet without change control.** Every stakeholder ask is absorbed to be agreeable; the baseline no longer describes the program. Test: does a change log exist, and does anything in it say "rejected"?
9. **The launch gate that is a calendar invite.** Readiness review happens because it was scheduled, passes because everyone is in the room. Test: has any gate in this program's history ever failed? Gates that cannot fail are ceremonies.
10. **Vendor risk discovered at go-live.** The third party's leg of the flow was never tested at volume, never included in the incident drill, and its exit clause was never read. The program inherits their outage on day one.
11. **The metric that cannot survive an audit.** A headline number (uptime, success rate, savings) with no agreed source and method. It works in every review until the one review where someone asks how it is measured, and the program's credibility goes with it.
12. **One-shot stakeholder management.** The kickoff was communicated; nothing since. Sponsors drift, and the program discovers it lost support only when it needs air cover. Test: when did each named sponsor last hear anything requiring a reply?

## Workflow

1. Ingest the plan, status pack, or a spoken description (interview if needed: teams, external parties, cutover shape, governance forums, top three headline metrics). Where they exist, read the filled-in risk register and dependency register; their absence is itself evidence for modes 1, 2, and 6.
2. Check all twelve modes. For each return: PRESENT (with the specific evidence), ABSENT (with what proves it absent), or UNKNOWN (with the one question that settles it).
3. For every PRESENT: the smallest intervention that changes the outcome, one artifact, one rule, or one meeting redesign. Not a framework. The smallest thing.
4. Rank the PRESENT modes by time-to-damage: which one hurts first, not which is worst in the abstract.
5. Write every PRESENT mode into the risk register with a likelihood, impact, mitigation (the smallest intervention), owner, and review date.

## Output format

| # | Failure mode | Verdict | Evidence / settling question | Smallest intervention | Hurts by |
|---|---|---|---|---|---|

Close with the premortem sentence, completed: "It is six months from now and the program failed. The most likely cause, given the evidence above, was ______." One cause. Committed.

## Exit gate

Do not report the premortem done until every PRESENT mode has a risk-register row with an owner, and the completed premortem sentence names exactly one cause. A premortem that hedges across three causes has decided nothing.
