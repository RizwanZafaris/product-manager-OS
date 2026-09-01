# ADR `<number>`: `<decision title, stated as the decision itself>`

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: manual

<!-- Architecture Decision Record. Based on the format described by Michael Nygard
     (2011): short, numbered, immutable documents that capture one significant
     decision each. Keep all ADRs in one directory, numbered sequentially (adr-0001,
     adr-0002, ...). The title states the decision, not the topic: "Use event
     sourcing for the ledger", never "Ledger storage".

     The immutability rule is the whole point. An accepted ADR is never edited into
     a different decision. To reverse one, write a new ADR that supersedes it and
     update the old one's status line to "Superseded by ADR-NNNN". The trail of
     superseded records is the institutional memory; teams that edit in place are
     doomed to relitigate the same decision with worse attendance.

     Product and process decisions do not belong here; they go in the decision log
     (templates/execution/decision-log.md). This file is for decisions that shape
     the system's structure and are expensive to reverse. -->

**Status:** Proposed / Accepted / Superseded by ADR-`<NNNN>` / Deprecated
**Date:** `<YYYY-MM-DD>` · **Deciders:** `<names, the people who can commit the team>`

## Context

<!-- The forces at play: the requirement driving this, the constraints, what makes
     the decision hard. Written so a new joiner in two years understands why this
     was ever a question. Three to eight sentences. -->

`<context>`

## Decision

<!-- One or two sentences, active voice, present tense: "We will ..." -->

We will `<the decision>`.

## Consequences

<!-- All of them, good and bad. The bad consequences are the reason this section
     exists; an ADR listing only upsides is an advertisement. Include what becomes
     harder, what we now depend on, and what future choice this forecloses. -->

- `<positive consequence>`
- `<negative consequence, stated plainly>`
- `<follow-on work this creates, with the register or backlog it now lives in>`

---

## Worked micro-example

<!-- Delete this section when filling in the template. -->

> **ADR 0007: Store audit events in an append-only table, not in application logs**
>
> **Status:** Accepted · **Date:** 2026-05-14 · **Deciders:** A. Rahman, J. Okafor
>
> **Context:** Compliance review needs a replayable record of every state change
> for seven years. Application logs rotate at 90 days, are mutable at the
> infrastructure layer, and mix operational noise with business events. Extending
> log retention was costed and would still not give immutability guarantees.
>
> **Decision:** We will write every business state change to an append-only audit
> table in the primary database, with writes in the same transaction as the change.
>
> **Consequences:** Auditors query one table with SQL. Write latency rises by one
> insert per transaction. The audit table becomes the largest table in the
> database within a year; a partitioning task is now in the backlog. Log-based
> analytics dashboards must migrate to the new table, tracked as dependency
> register row 12.

## Exit gate

- [ ] The title states the decision, not the topic
- [ ] Status, date, and deciders are filled in
- [ ] Context explains the forces, not just the requirement
- [ ] The decision is one or two sentences in active voice
- [ ] At least one negative consequence is recorded
- [ ] If this supersedes an earlier ADR, that ADR's status line now points here
