# Decision doors: Ledgerline pivot

Fills [frameworks/prioritization/decision-doors.md](../frameworks/prioritization/decision-doors.md). Everything here is ILLUSTRATIVE and invented: Ledgerline, its people, its customers, its vendor, and every count, score, price, date and dollar figure are fiction built so that these files can be checked against the [ledgerline-journey.md](ledgerline-journey.md) data sheet and its [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md).

**Owner:** Maya Chen, Product Manager, with Isabel Ferreira, Chief Product Officer · **Date:** 2026-12-22

## What it is for

This sheet decides how much process the Ledgerline pivot deserves before the decisions are made. It scores three decisions on 2026-12-22:

1. D7, the EXP-2 usage re-offer at $2.40 per drafted report.
2. ADR-008, the product-side drafted-report meter billed in arrears.
3. Moving the 73 held accounts to a successor price when their 12-month holds end.

It also re-scores D3 in hindsight. The team treated D3 as two-way because EXP-1 could kill the price. The re-score recognises that the 12-month holds in N48 landed on customers, making D3 heavier than the team treated it.

The method follows the worksheet's one-way door and two-way door distinction, based on Jeff Bezos's 2015 Amazon shareholder letter and explained here in the repository's own words.

## Run it when

- A decision has been debated for more than ten minutes and needs a process choice.
- Someone wants to escalate or decide alone, and the correct level of involvement is unclear.
- A decision memo is about to be written.

The three pivot decisions are scored because their reversibility is not obvious. The migration decision is scored separately from EXP-2 because its reversal cost falls on the 73 held accounts, not only on Ledgerline.

## Inputs you need first

- **D7:** EXP-2, a single-arm re-offer to about 2,818 to 2,821 S-1 accounts not paying (2,675 exposed non-converters plus 152 never exposed, less the 6 design partners and up to 3 G-1 manual-invoice activations), at $2.40 per drafted report, billed monthly in arrears, with no seat charge and no minimum. Success is 6.0% or more reaching paid status (M-007) within 14 days of exposure. Its reversal trigger is the N92 kill rule: M-009 at most $1.05, M-006 at least 70%, M-010 at most 8 per week, and kill under 4.0% at the analysis date or on 2027-02-12, whichever comes first.
- **ADR-008:** a product-side drafted-report meter, billed in arrears, which supersedes ADR-007 for the add-on. It requires 1 person-month and $10,000 at the N12 engineering cost rate, and is needed by 2027-01-08 under DEP4.
- **Migration of the 73 held accounts:** N93 holds the 73 paying accounts at $6 per seat for 12 months, then migration to a successor price, pending EXP-2. The decision memo is owed by 2027-10-01 under R8.
- **D3 hindsight:** plan seats at $6 per seat per month, with the north star mismatch accepted in writing. N48 says contracted prices hold for 12 months.
- **Decision rights:** D7 is owned by Maya Chen with Isabel Ferreira. ADR-008 is a structural decision recorded as an ADR. The migration decision is owned by Isabel Ferreira.
- **Reversal cost:** customer and commercial impact for the held accounts, billing and engineering impact for ADR-008, and customer, finance and pricing impact for D3.

## The worksheet

### Step 1: score reversibility

#### D7, EXP-2 usage re-offer

| Question | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Can it be undone? | Fully, by us | Partly, or with a workaround | No, or only by starting over | 1, partly, or with a workaround |
| Cost to reverse | Under a team-week and no money | A few team-weeks, or a modest sum | A quarter of a team, or a sum the sponsor would have to approve | 0, under a team-week and no money |
| Time to learn it was wrong | Days | A quarter | A year or more, or never with certainty | 1, the N92 kill rule is checked at the analysis date or on 2027-02-12 |
| Who bears the reversal cost | Us | Us and a partner | Customers, a regulator, or the public record | 0, Ledgerline |
| Does it foreclose options? | No | Narrows some | Locks in a contract, a public commitment, or a data model others build on | 1, narrows some |
| Blast radius | One team or a pilot group | A product line | Every customer, or the company's name | 1, the EXP-2 population is about 2,818 to 2,821 S-1 accounts |
| **Total** | | | | **1 + 0 + 1 + 0 + 1 + 1 = 4** |

#### ADR-008, product-side drafted-report meter

| Question | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Can it be undone? | Fully, by us | Partly, or with a workaround | No, or only by starting over | 1, partly, or with a workaround |
| Cost to reverse | Under a team-week and no money | A few team-weeks, or a modest sum | A quarter of a team, or a sum the sponsor would have to approve | 1, a few team-weeks, or a modest sum |
| Time to learn it was wrong | Days | A quarter | A year or more, or never with certainty | 1, a quarter |
| Who bears the reversal cost | Us | Us and a partner | Customers, a regulator, or the public record | 0, Ledgerline |
| Does it foreclose options? | No | Narrows some | Locks in a contract, a public commitment, or a data model others build on | 1, narrows some |
| Blast radius | One team or a pilot group | A product line | Every customer, or the company's name | 1, the add-on product line |
| **Total** | | | | **1 + 1 + 1 + 0 + 1 + 1 = 5** |

#### Migration of the 73 held accounts to a successor price

| Question | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Can it be undone? | Fully, by us | Partly, or with a workaround | No, or only by starting over | 2, no, or only by starting over |
| Cost to reverse | Under a team-week and no money | A few team-weeks, or a modest sum | A quarter of a team, or a sum the sponsor would have to approve | 1, a few team-weeks, or a modest sum |
| Time to learn it was wrong | Days | A quarter | A year or more, or never with certainty | 1, a quarter |
| Who bears the reversal cost | Us | Us and a partner | Customers, a regulator, or the public record | 2, the 73 customers with 12-month holds |
| Does it foreclose options? | No | Narrows some | Locks in a contract, a public commitment, or a data model others build on | 2, the 12-month price commitment and successor price affect the customer relationship |
| Blast radius | One team or a pilot group | A product line | Every customer, or the company's name | 1, the 73 held accounts |
| **Total** | | | | **2 + 1 + 1 + 2 + 2 + 1 = 9** |

#### D3, re-scored in hindsight

| Question | 0 | 1 | 2 | Score |
|---|---|---|---|---|
| Can it be undone? | Fully, by us | Partly, or with a workaround | No, or only by starting over | 1, partly, or with a workaround |
| Cost to reverse | Under a team-week and no money | A few team-weeks, or a modest sum | A quarter of a team, or a sum the sponsor would have to approve | 1, a few team-weeks, or a modest sum |
| Time to learn it was wrong | Days | A quarter | A year or more, or never with certainty | 1, a quarter |
| Who bears the reversal cost | Us | Us and a partner | Customers, a regulator, or the public record | 2, customers with contracted prices |
| Does it foreclose options? | No | Narrows some | Locks in a contract, a public commitment, or a data model others build on | 2, the N48 12-month holds narrow the migration path |
| Blast radius | One team or a pilot group | A product line | Every customer, or the company's name | 1, the add-on product line |
| **Total** | | | | **1 + 1 + 1 + 2 + 2 + 1 = 8** |

### Step 2: read the door

| Total | Door | Who decides | Before deciding | Record | Time budget |
|---|---|---|---|---|---|
| 4, D7 | Two-way | Maya Chen with Isabel Ferreira | Name the reversal trigger, the N92 kill rule | One line in the [decision log](../templates/execution/decision-log.md) with the door type and trigger | Same day |
| 5, ADR-008 | Heavy two-way | Priya Nair with the billing lead, with Maya Chen accountable for the product decision | Options, the trial or implementation period, a reversal trigger, and a revisit date | Decision log entry with the trigger and date, plus ADR-008 | One week |
| 9, migration of the 73 held accounts | One-way | Isabel Ferreira, with dissent captured from pricing, finance and customer-facing owners | Decision memo: successor-price options, evidence per option, the customer impact and a conversion move | Decision memo, decision log and the customer pricing record | As long as the evidence takes, with a decision memo due by 2027-10-01 |
| 8, D3 hindsight | Heavy two-way | Isabel Ferreira, with Maya Chen and the owners of the reversal cost | Options, a trial period, a reversal trigger and a revisit date | Decision log entry with the re-score and the 12-month hold consequence | One week |

D7 is a two-way door because the N92 kill rule gives the team a pre-declared reversal trigger. ADR-008 is a heavy two-way door because the meter can be replaced, but it changes billing architecture and supersedes ADR-007 for the add-on. Moving the 73 held accounts is one-way because the decision changes a customer commitment and cannot be cheaply reversed once the successor price is accepted. D3 is heavy two-way in hindsight, not a simple two-way door, because the 12-month holds in N48 made the consequences customer-facing.

### Step 3: try to make it a two-way door

The conversion move applies to the one-way migration decision. It reduces the score from 9 to 7:

**2 + 1 + 1 + 1 + 1 + 1 = 7**

The customer-facing reversal-cost score falls from 2 to 1 because the customer is offered a choice for one more term. The foreclosure score falls from 2 to 1 because the choice preserves an additional path.

| Conversion move | What it costs | Converts it? |
|---|---|---|
| Feature flag or staged rollout | Not selected for the migration decision; the decision concerns the 73 held accounts at term end | No |
| Pilot with a stated end date | Not selected; the 12-month holds already define the customer timing | No |
| Contract clause: exit terms, data return, shorter term | Not selected for the existing N48 holds | No |
| Reversible migration: keep the old path alive for a period | Offer each held account the choice of its seat price or the successor price for one more term | **Yes, score becomes 7, heavy two-way** |
| Announce internally first, publicly later | Not selected; the customer choice is the conversion move, not an announcement sequence | No |

The conversion move does not remove the need for a decision memo. It changes the door from one-way to heavy two-way, so the successor-price decision still needs options, evidence, a reversal trigger and a revisit date.

## Reading the result

The scores set the process, not the answer.

- **D7, total 4, two-way:** EXP-2 can proceed with the N92 kill rule as its reversal trigger. The trigger is under 4.0% at the analysis date or on 2027-02-12, whichever comes first. M-009, M-006 and M-010 remain counter-metrics.
- **ADR-008, total 5, heavy two-way:** the product-side meter is not treated as an irreversible architecture commitment. It is recorded as ADR-008, with ADR-007 never edited. The implementation is needed by 2027-01-08 under DEP4 and should carry a revisit date and reversal trigger in the decision log.
- **Migration of the 73 held accounts, total 9, one-way before conversion:** a successor price cannot simply be applied at term end. The choice offered to each held account for one more term reduces the score to 7, heavy two-way. R8 remains open and the decision memo is owed by 2027-10-01.
- **D3, total 8 in hindsight:** EXP-1 could kill the per-seat price, but the 12-month holds meant the decision had already created customer-facing commitments. The team treated D3 as lighter than it was. The correct process would have been heavy two-way, with the customer hold and successor-price path considered before signing.

The result also separates product reversal from customer reversal. D7's re-offer can be stopped through the N92 rule. ADR-008 can be replaced with another meter at a cost to Ledgerline. The 73 held accounts require a deliberate customer migration path because reversal cost is carried by customers as well as Ledgerline.

## ILLUSTRATIVE example

The following ledger records the pivot's three decisions and the D3 hindsight re-score. All values are ILLUSTRATIVE and trace to LC32, LC33, N48, N92 and N93 in the [ledgerline-journey.md](ledgerline-journey.md) and [ledgerline-coverage-sheet.md](ledgerline-coverage-sheet.md).

| Decision | Undo | Cost | Detect | Who bears | Forecloses | Radius | Total | Door |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| D7, EXP-2 usage re-offer | 1 | 0 | 1 | 0 | 1 | 1 | 1 + 0 + 1 + 0 + 1 + 1 = 4 | Two-way |
| ADR-008, product-side drafted-report meter | 1 | 1 | 1 | 0 | 1 | 1 | 1 + 1 + 1 + 0 + 1 + 1 = 5 | Heavy two-way |
| Move the 73 held accounts to a successor price | 2 | 1 | 1 | 2 | 2 | 1 | 2 + 1 + 1 + 2 + 2 + 1 = 9 | One-way |
| Move the 73 held accounts with a choice of the existing seat price or the successor price for one more term | 2 | 1 | 1 | 1 | 1 | 1 | 2 + 1 + 1 + 1 + 1 + 1 = 7 | Heavy two-way |
| D3, hindsight re-score | 1 | 1 | 1 | 2 | 2 | 1 | 1 + 1 + 1 + 2 + 2 + 1 = 8 | Heavy two-way |

D7 receives a one-line decision-log entry with the N92 reversal trigger. ADR-008 receives a decision-log entry and an ADR because it is structural. The 73-account migration receives a decision memo, with Isabel Ferreira as owner and a due date of 2027-10-01 under R8. D3 receives a hindsight note explaining that the 12-month holds in N48 made it heavier than the team treated it.

## The trap

Counting only the cost of changing code or changing a price page. For D3, EXP-1 could kill the seat price, but the 12-month holds meant 73 paying accounts were still held at $6 per seat for 12 months. The reversal cost therefore landed on customers as well as Ledgerline. That is why the hindsight score is:

**1 + 1 + 1 + 2 + 2 + 1 = 8**

The mirror failure would be to score every pricing change as a 9 and miss that D7 has a pre-declared N92 kill rule, or that ADR-008 can be replaced with a different meter. The process must follow the door, not the anxiety around it.

## Feeds

- [Decision log](../templates/execution/decision-log.md): D7 carries the N92 reversal trigger, ADR-008 carries its revisit and reversal details, and D3 carries the hindsight re-score.
- [Decision memo](../templates/planning/decision-memo.md): the one-way migration decision, converted to heavy two-way through the one-more-term customer choice, with the memo owed by 2027-10-01.
- [ADR](../templates/architecture/adr.md): ADR-008 records the product-side drafted-report meter and leaves ADR-007 unchanged.
- [Weighted decision matrix](../frameworks/prioritization/weighted-decision-matrix.md): the earlier D3 value-metric scoring that selected seats.
- [Escalation](../skills/escalation/SKILL.md): use if the migration memo is stuck past 2027-10-01.
- Method background: the decision-door attribution above and [triad decision rights](../knowledge/roles/triad-decision-rights.md).

**Exit-gate walk:** Maya Chen, Product Manager, and Isabel Ferreira, Chief Product Officer, signed the D7, ADR-008, migration and D3 re-score process on 2026-12-22.
