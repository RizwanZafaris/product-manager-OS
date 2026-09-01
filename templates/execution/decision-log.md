# Decision Log: `<initiative name>`

Stage: all stages, read at every gate in [STAGE-GATES](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: manual

<!-- The decision log answers the most expensive recurring question on any team:
     "why did we do it this way?" Asked without a log, it costs a meeting and gets a
     guess. Asked with one, it costs thirty seconds and gets the truth, including
     the options that lost.

     Division of labor: decisions that shape system structure go in an ADR
     (../architecture/adr.md); everything else that closes a debate goes here:
     scope calls, pricing calls, sequencing, naming, a vendor shortlist, a metric
     definition. Same immutability rule as ADRs: a decision is never edited into a
     different one. Reversals get a new numbered entry that names the old one. -->

**Initiative:** `<name>` · **Log owner:** `<name>` · **Started:** `<YYYY-MM-DD>`

## How to write an entry

<!-- The bar for logging: if two people debated it for more than ten minutes, or
     anyone might reasonably reopen it later, log it. Log within a day of deciding;
     a reconstructed rationale is a rationalization. The worked entry below shows
     the expected size; keep entries near that length. -->

## Decisions

<!-- Newest first. Copy the block. -->

### D-`<number>`: `<decision, stated as the decision itself>`

- **Date:** `<YYYY-MM-DD>` · **Decider:** `<the one name that made the call>`
- **Context:** `<what forced a decision now, two or three sentences>`
- **Options considered:** `<option A; option B; option C>`
- **Decision and rationale:** `<which option and the reason it won, including what was given up>`
- **Reverses or is reversed by:** `<D-number, or "none">`
- **Who was told:** `<channel and date the decision was announced>`

---

### Worked micro-example (delete once real entries exist)

### D-004: Launch in one market, not three

- **Date:** 2026-04-02 · **Decider:** Product lead (R. Ali)
- **Context:** Engineering can support one localized rollout per quarter. Sales
  asked for three markets at once; support has headcount for one queue.
- **Options considered:** all three markets at reduced support depth; one market
  fully supported; delay launch a quarter and do two.
- **Decision and rationale:** One market, fully supported. A weak first market
  costs references we need for the other two; the delay option loses a committed
  customer. Given up: two quarters of revenue from markets two and three.
- **Reverses or is reversed by:** none
- **Who was told:** initiative channel and sales weekly, 2026-04-03

## Exit gate

- [ ] Every entry has exactly one decider by name
- [ ] Every entry lists the options that lost, not only the winner
- [ ] Rationales include what was given up, not only what was gained
- [ ] No entry has been edited into a different decision; reversals are new entries
- [ ] Entries were logged within a day or two of the decision, per their dates
- [ ] Structural technology decisions live in ADRs, and this log links to them rather than duplicating them
