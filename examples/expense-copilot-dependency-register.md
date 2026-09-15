# Dependency Register: Expense Copilot

Fills [templates/execution/dependency-register.md](../templates/execution/dependency-register.md). Part of the [Ledgerline Expense Copilot journey](expense-copilot-journey.md): the internal v1 Ledgerline's own finance team commissioned for Ledgerline's own filers, from the understood problem to a development-ready handoff at Gate 3. Everything here is invented and ILLUSTRATIVE, drawn from that journey's data sheet and from [ledgerline-journey.md](ledgerline-journey.md)'s data sheet; no figure is a target to copy. See the [examples index](README.md).

Stage: DESIGN, feeds [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md), first filled 2026-09-08 (V13), the same review that ran the premortem, governed weekly through DELIVER
Knowledge: [knowledge index](../knowledge/INDEX.md)
Skill: [program-premortem](../skills/program-premortem/SKILL.md)

**Initiative:** Expense Copilot (Ledgerline internal v1) · **Register owner:** Maya Chen, Product Manager · **Review cadence:** weekly, `<day and meeting>` (neither data sheet fixes a day or a standing meeting; this chain closes at Gate 3 on 2026-09-11, before DELIVER's weekly cadence begins)
**Last reviewed:** 2026-09-08

## 1. The register

| # | Dependency (deliverable, not a team name) | Owning team | Their named contact | Needed by (our date) | Their committed date | Status | Escalation contact (their manager or ours) |
|---|---|---|---|---|---|---|---|
| DEPV-1 | Vendor clause forbidding training on Ledgerline data | Legal, with the model vendor | the legal lead (role only; no personal name on either data sheet, and the model vendor names no contact either) | before Gate 5 | not committed; requested only | requested | Daniel Okafor, finance lead and sponsor |
| DEPV-2 | Receipt image retention and deletion schedule | Legal | the legal lead (role only) | before Gate 5, per the PRD's Launch criteria | not committed; requested only | requested | Daniel Okafor, finance lead and sponsor |
| DEPV-3 | Model vendor's per-receipt price contracted, not only quoted | Procurement, with Priya Nair | Priya Nair, engineering lead (Procurement's own contact is not named on either sheet) | before volume outgrows the quoted-rate assumption | not committed; still quoted, not contracted, even after launch, per [ledgerline-journey.md](ledgerline-journey.md) N9 | requested | Daniel Okafor, finance lead and sponsor |
| DEPV-4 | Finance system's approval events joined to draft ids, so objective 1 can be measured | Finance, with Priya Nair | Priya Nair, engineering lead (Finance's own contact is not named on either sheet) | 2026-10-09 (Gate 5) | 2026-10-09, tied to the fixed Gate 5 date itself, signed per function, not a separate promise ([ledgerline-journey.md](ledgerline-journey.md) N16) | committed; delivered 2026-10-09 per [ledgerline-journey.md](ledgerline-journey.md) N20 | Daniel Okafor, finance lead and sponsor |

DEPV-1 to DEPV-4 are exactly the four rows [expense-copilot-journey.md](expense-copilot-journey.md)'s data sheet names; this register adds no fifth. Their descriptions, owners and needed-by text above reproduce that sheet's Dependencies table word for word; the columns the sheet does not carry, a named contact, a committed date, an escalation contact, are filled in below from what the two sheets say around each row, never from a guess.

DEPV-1's and DEPV-2's contact columns read "the legal lead (role only)" for the same reason DEPV-3's and DEPV-4's name Priya Nair rather than a separate contact inside Procurement or Finance: the journey's own People section gives the legal lead no personal name, and names nobody inside Procurement or Finance beyond Priya Nair's own coordinating role. That is the data sheet's own choice, not a placeholder this register left blank.

All four rows escalate to the same person, Daniel Okafor. The named cast behind this chain is three people plus one role-only legal lead; Gate 3's own signature line already records Priya Nair carrying both the architect and the security-reviewer role for the same reason. A one-name escalation column is a fact about the team's size, not a gap this register should paper over with an invented second name. Daniel Okafor fits each row on its own terms besides: he supplies the finance-system baselines both the discovery document and the PRD already cite, which is exactly what DEPV-4 depends on, and as the sponsor who can stop the build he is the natural escalation for a vendor-cost or legal item Legal and Procurement cannot close alone.

Only DEPV-4 is marked committed. Its committed date is the Gate 5 milestone itself, 2026-10-09, signed per function including finance, which is Finance's own plan with a date rather than a verbal yes in a meeting; N20 shows the join delivered against exactly that date. DEPV-1 to DEPV-3 stay at requested: the data sheet records status "open" for all four rows at Gate 3 (2026-09-11), and this register reads "open" as requested wherever no committed date from the owning party exists, per the escalation ladder's own rule below. DEPV-3 stays requested even in [ledgerline-journey.md](ledgerline-journey.md)'s own account of what happened later: N9 records the per-receipt rate as still quoted, not contracted, even after launch, so this row would still read requested if this register were reopened on that later date.

## 2. Escalation ladder

1. Slip detected at weekly review: register owner (Maya Chen) contacts the named contact within one working day. Where the named contact is a role rather than a person, as on DEPV-1 and DEPV-2, the register owner contacts Daniel Okafor as the internal relationship owner instead.
2. No recovery plan within `<n>` working days: escalate to the escalation contact on the row.
3. Still unresolved and the needed-by date is inside `<n>` weeks: raise with Daniel Okafor and Maya Chen together, and the dependency becomes a risk register row with a mitigation.

Rungs 2 and 3 keep the template's `<n>` placeholders rather than a filled number: neither data sheet states a working-day or week count for this ladder, and setting one is a decision for Maya Chen and Daniel Okafor to make once DELIVER's weekly cadence starts, not a number this register may invent. Rung 1's "one working day" reproduces the template's own fixed wording and needs no data-sheet citation.

None of the four rows has reached rung 2 or 3 through this ladder: the register is three days old at last review, and every needed-by date on it still sits in the future of 2026-09-08. DEPV-1 and DEPV-2 already correspond to risk register rows regardless, [expense-copilot-risk-register.md](expense-copilot-risk-register.md) RV-2 and RV-3, both opened at the same 2026-09-08 premortem that opened this register. That is the more usual way the two registers meet at this early stage: the same session populates both, rather than one escalating into the other.

## 3. Reverse dependencies

| Deliverable we owe | To team | Their needed-by | Our committed date | Status |
|---|---|---|---|---|
| Stable draft ids on every drafted report, for Finance's own approval-events join (the join DEPV-4 needs from this side) | Finance | 2026-10-09 (Gate 5) | 2026-10-09 | delivered, per [ledgerline-journey.md](ledgerline-journey.md) N20: the join shipped with Gate 5 on 2026-10-09 |

DEPV-4 reads as a dependency from Finance when the copilot needs their join; the same fact reads as a dependency the copilot owes to Finance when the direction reverses, since Finance's join cannot run without a stable draft id on this side to join against (the api contract's report and line-item resources, per V11). Neither data sheet records a second deliverable owed to another team by Gate 3, so this table holds the one row it supports rather than a courtesy blank stretched to look fuller than the sheets allow.

## 4. Weekly review notes

| Date | Rows that changed status | Escalations opened or closed |
|---|---|---|
| 2026-09-08 | Register opened at the same review that ran the premortem behind [expense-copilot-risk-register.md](expense-copilot-risk-register.md). DEPV-1 to DEPV-4 logged at their Gate 3 status: DEPV-1 to DEPV-3 requested, DEPV-4 committed against the fixed Gate 5 date | none |

Gate 3 falls on 2026-09-11, three days into the same week as this opening entry, so the exit gate's "current or previous week" box below is satisfied by it. This chain closes at Gate 3; a weekly cadence proper, with a named day and meeting, starts once DELIVER begins, which is beyond this journey (see [expense-copilot-journey.md](expense-copilot-journey.md), "Beyond this chain").

## How this register fails

| Failure mode | What it looks like here | The rule that stops it |
|---|---|---|
| A verbal yes recorded as committed | Legal and Procurement have given no date for DEPV-1 to DEPV-3 as of Gate 3 | Committed means on their plan with their date; this register calls all three requested rather than rounding "we asked" up to "they agreed" |
| No named human | The legal lead, and Procurement's and Finance's own contacts, carry no personal name on either data sheet | The register says so in plain words in section 1's note, rather than inventing a name to fill the cell |
| At risk is felt, not computed | Not yet tested: every needed-by date on this register still sits in the future of the 2026-09-08 last-reviewed date, so no row has had the chance to read at risk yet | The comparison is mechanical once DELIVER's weekly reviews begin: their date against our needed-by, every week, not a feeling about how the vendor or Legal sounded on the call |
| Escalation avoided | Not yet tested, for the same reason | The ladder in section 2 is agreed before the first slip, not improvised at the first one |
| Reverse dependencies left as a courtesy blank | A register like this one could easily track only what the chain needs from others | Section 3 fills the one reverse dependency the two sheets support, rather than leaving the section empty because it is smaller than section 1 |

## Exit gate

- [x] Every dependency names a deliverable, a human contact, and an escalation contact: DEPV-1 to DEPV-4 in section 1. DEPV-1 and DEPV-2 name the legal lead by role, not a person, because that is what the data sheet itself gives; each still carries a named escalation contact, Daniel Okafor.
- [x] Every row shows both our needed-by date and their committed date: all four rows in section 1.
- [x] No row claims "committed" without the work on the owning team's own plan: DEPV-1 to DEPV-3 are marked requested, with no committed date from Legal or Procurement on either sheet. DEPV-4 alone is marked committed, and its committed date is the Gate 5 milestone itself, signed per function including Finance, which is Finance's own plan with a date; N20 shows the join delivered against exactly that date.
- [x] Every at-risk or blocked row has a corresponding risk register entry: none of the four rows is at risk or blocked under the template's fixed vocabulary (all are requested or committed), so this box's trigger has not fired for any row through the ladder itself. DEPV-1 and DEPV-2 already correspond to risk register rows regardless: [expense-copilot-risk-register.md](expense-copilot-risk-register.md) RV-2 and RV-3.
- [x] Reverse dependencies are filled in, not left as a courtesy blank: section 3.
- [x] The weekly review has an entry from the current or previous week: 2026-09-08, the week Gate 3 (2026-09-11) falls in.
- [x] The example row has been deleted: section 1 holds only DEPV-1 to DEPV-4.

Reviewed and current as of 2026-09-08: Maya Chen, Product Manager and register owner, ahead of Gate 3 on 2026-09-11. Open: DEPV-1 to DEPV-3, all due before Gate 5 (2026-10-09); DEPV-4 committed against that same date and, per [ledgerline-journey.md](ledgerline-journey.md) N20, delivered on it.
