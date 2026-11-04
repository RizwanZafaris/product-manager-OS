---
layer: frameworks
stage: PLANNING
gate: 1
feeds: ["frameworks/strategy/seven-powers-audit.md", "templates/planning/product-strategy.md", "templates/planning/pricing-packaging.md"]
method: "knowledge/domains/marketplaces.md"
aliases: ["Platform ecosystem canvas", "platform-ecosystem-canvas"]
---
# Platform ecosystem canvas

Based on the ideas of Geoffrey G. Parker, Marshall W. Van Alstyne and Sangeet Paul Choudary, from Platform Revolution: How Networked Markets Are Transforming the Economy and How to Make Them Work for You (2016). Explained here in this repository's own words. The scoring scales, the take-rate lines and the disintermediation test below are this repository's own way of running the ideas, not a form taken from the book.

## What it is for

A product becomes a platform when most of its value comes from interactions between groups it does not employ: buyers and sellers, developers and the people who use their apps, hosts and guests, tutors and parents. The pipeline question, "is the product good", stops being enough, because a platform with excellent software and nobody on the other side has nothing to offer. The book's central unit is the core interaction: a producer creates a value unit (a listing, an app, a post, an available slot), the platform's filter decides which value unit reaches which consumer, and the consumer acts on it. Everything else on this canvas is about making that one interaction happen often, keeping a share of it, and keeping it on the platform.

The canvas puts six answers on one page: who the sides are and which one is scarce, which network effects run in which direction with what evidence, how the first interactions happen before either side has a reason to come, what share of each transaction the platform keeps and what that share pays for, who may join and on what enforced rules, and what stops two parties who met here from transacting elsewhere next time. Its output goes to the network economies row of the [Seven Powers audit](seven-powers-audit.md), which is where a claimed network effect has to show it is a barrier and not a hope.

## Run it when

- The strategy names "network effects" or "the ecosystem" as the reason the product will hold, and nobody has written down which side benefits from which
- A product with one kind of user is about to open to a second: third-party developers, sellers, service providers, creators
- A take-rate change is proposed, in either direction
- Repeat transactions between the same pairs are rising while platform revenue per pair is flat, which is what leakage looks like from the inside
- Before a launch in a new city, category or segment, where the cold start has to be solved again

**Skip it when:** the product has one kind of customer and no plan to add a second. A single-sided product with a shared-data feature is not a platform, and filling this canvas for it invents a second side to score. Run the [Seven Powers audit](seven-powers-audit.md) directly and score network economies on its own row; it usually comes back 0, honestly.

## Inputs you need first

- A persona for each side from the [personas](../../templates/discovery/personas.md) template, with the constrained side named, per the [marketplaces domain card](../../knowledge/domains/marketplaces.md)
- Transaction data cut by segment (geography, category, joining cohort), never only in aggregate: liquidity, repeat rate, time to first transaction
- The fee schedule, plus refunds, credits and incentives paid in the same period, from finance
- Retention for each side split by how dense the network was when the member joined, if the data can be cut that way
- Known cases of off-platform transacting: support tickets, removed listings, contact details caught in messages

## The worksheet

### Part 1: sides and the core interaction

<!-- One row per side. Exactly one side is marked constrained: the one that is hard
     to get and that the other side follows. Two "yes" answers means the sheet has
     not made the choice the marketplaces card says decides the business.
     Multi-homing means the side also uses a rival at the same time; it matters in
     Part 2, because a side that multi-homes carries its value to every platform it
     sits on. -->

| Side | Who, precisely | Value unit they bring | What they get | Constrained side (one yes only) | Multi-homes (yes / some / no) |
|---|---|---|---|---|---|
| [side A] | | | | | |
| [side B] | | | | | |

**Core interaction, one sentence:** [producer] creates [value unit]; the filter selects by [the rules that decide which value unit reaches which consumer]; [consumer] [books, buys, installs, rates].

### Part 2: network effects, direction and evidence

<!-- Four effects exist on a two-sided platform: one same-side effect per side and
     one cross-side effect in each direction. Each is positive (more of them makes
     it better) or negative (more of them makes it worse: congestion, noise, price
     competition). Fill all four rows, and write at least one negative row or the
     reason there is none. Evidence scores: 0 asserted, no data; 1 a proxy consistent
     with the effect, such as an aggregate correlation; 2 demonstrated by a
     within-segment comparison, members of the same type who joined at the same
     time into denser and thinner segments, with the counts written down. -->

| Effect | More [X] makes the product [better / worse] for [Y], because [mechanism] | Positive or negative | Evidence (with counts) | Score 0 to 2 |
|---|---|---|---|---|
| Same-side, side A | | | | |
| Same-side, side B | | | | |
| Cross-side, A to B | | | | |
| Cross-side, B to A | | | | |

**Arithmetic for a score of 2.** Pick segments matched on joining period. Relative lift = (rate in dense segments minus rate in thin segments) / rate in thin segments, where the rate is the outcome the effect promises (a search that ends in a booking, 90-day retention). Write both counts beside both rates. A lift that would vanish if a few dozen members changed their behaviour, given those counts, scores 1, not 2.

**Decision rule.** A network effect is claimed in the strategy only at score 2. The benefit cell of the Seven Powers network economies row takes its evidence from here; the barrier cell still needs that sheet's own test, and multi-homing usually answers it. If the side that carries the effect sits freely on a rival as well, the effect helps the rival as much as you, and the barrier scores 0; if only some of that side multi-homes, the barrier scores 1 at most.

### Part 3: the chicken-and-egg plan

<!-- Neither side comes without the other, so one side gets a reason to come first.
     Among the launch approaches the book describes are the platform supplying one
     side itself, piggybacking on a network that already exists, signing one marquee
     participant, offering single-side utility worth using alone, and starting in a
     micromarket small enough to saturate. Name the one in use. The end condition is
     a liquidity number in the smallest self-sustaining unit, never a date: a
     subsidy that ends on a date ends whether or not the unit can stand on its own. -->

| Question | Answer |
|---|---|
| Which side first, and why that one | |
| Smallest self-sustaining unit (place, category, time window) | |
| How the first side is seeded | [supply it ourselves / piggyback on [network] / marquee participant / single-side utility / micromarket] |
| What the first side gets before the second arrives | |
| Liquidity threshold that ends seeding in the unit, as a probability with a window | |
| Seeding cost per unit, and the line it sits on in the business case | |

### Part 4: take rate and its arithmetic

<!-- The take rate is the platform's price. The headline rate is what the fee
     schedule says; the effective rate is what the platform keeps after paying for
     refunds and incentives out of its own share. The gap between them is where the
     margin went, and it is invisible in a GTV chart. Use one period throughout. -->

| Line | This period | Source |
|---|---|---|
| Gross transaction value (GTV): the total value of transactions through the platform | | |
| Fees charged to side A | | |
| Fees charged to side B | | |
| Refunds and credits the platform absorbed | | |
| Incentives and subsidies paid to either side | | |
| **Headline take rate** = (fees A + fees B) / GTV | | |
| **Effective take rate** = (fees A + fees B minus absorbed refunds minus incentives) / GTV | | |

**What the fee pays for.** List each thing the platform provides inside a transaction that the two parties cannot get as cheaply by going direct: payment collection, a guarantee, dispute handling, insurance, scheduling, records, reputation that accrues only on the platform. The ceiling on the take rate is set by that list, not by what a competitor charges. Part 6 tests the list against the repeat transaction.

### Part 5: governance

<!-- Every rule gets an enforcement action and a capacity: how many cases the team
     can review in a week. A rule with no enforcement is a suggestion, and the side
     that reads it first learns that. Where a rule protects one side at the other's
     expense, write the cost in the rule's row so the trade is visible. -->

| Rule area | The rule | Who decides | How it is enforced, and weekly review capacity | Appeal path | Published to both sides (yes / no) |
|---|---|---|---|---|---|
| Who may join, side A | | | | | |
| Who may join, side B | | | | | |
| What may be listed or built | | | | | |
| Quality floor, and what happens below it | | | | | |
| The filter: what moves a value unit up or down | | | | | |
| Contact and payment outside the platform | | | | | |
| What each side may see about the other | | | | | |

### Part 6: the disintermediation test

<!-- Run it on the repeat transaction, not the first one. The first match is where
     the platform's value is obvious; the second booking between two people who
     already trust each other is where it has to be earned again. -->

| Question | yes / no |
|---|---|
| Q1. After the first transaction, can the two parties reach each other directly? | |
| Q2. Is the fee on a repeat transaction large enough that either party would notice saving it? | |
| Q3. Does the platform provide something on the repeat transaction that the pair cannot replace cheaply off it? | |
| Q4. If Q3 is yes: is that something a value the pair would choose to pay for, rather than a rule the platform enforces? | |

**Leakage risk.** HIGH when Q1 and Q2 are yes and Q3 is no. MEDIUM when Q3 is yes but Q4 is no, because a retention rule holds only until it is tested. LOW when Q3 and Q4 are both yes, or Q1 is no.

**Arithmetic.** Exposed GTV = GTV from repeat pairs × the share of those pairs for whom Q3 is no. Revenue at risk per period = exposed GTV × effective take rate. Write it into the [risk register](../../templates/execution/risk-register.md) whenever the risk is HIGH.

## Reading the result

- **One constrained side, a cross-side effect at 2, a seeding plan that ends on a liquidity number, leakage LOW.** The platform has a mechanism worth defending. Take the evidence into the Seven Powers network economies row and run that sheet's barrier test; a demonstrated effect is still not a barrier while the scarce side multi-homes.
- **Every effect at 1 or below.** The strategy may name a network effect as a candidate to build, with the comparison that would score it 2, never as the reason the product holds.
- **A negative same-side effect on the constrained side at 2.** More supply is now making each supplier worse off. Acquisition on that side is a cost until bookings per supplier recover; the filter and the quality floor are the levers, not the acquisition budget.
- **Leakage HIGH.** The take rate is above what the repeat transaction will bear. Either add value the pair would pay for on the repeat transaction, or charge the repeat transaction differently, before the constrained side leaves with its best customers.
- **Effective take rate well below headline.** Find which incentive line opened the gap and whether it buys anything on the constrained side.

## ILLUSTRATIVE example

Invented. Brackenford Tutors is a fictional marketplace matching independent maths tutors with parents of secondary-school students in two cities. Every figure below is ILLUSTRATIVE, for one fictional quarter.

**Sides.** Tutors: constrained, yes; multi-home, some (most keep private clients). Parents: not constrained; multi-home, yes. **Core interaction:** a tutor publishes subjects and open slots; the filter ranks tutors by subject match, distance, a free slot within 72 hours, and rating; a parent books and pays for a session.

| Effect | Statement | Positive or negative | Evidence | Score |
|---|---|---|---|---|
| Cross-side, tutors to parents | More tutors in a postcode means a parent finds a slot within 72 hours | Positive | Searches in postcodes with 12 or more active tutors ended in a booking 56% of the time (n = 410 searches) against 35% in postcodes with fewer than 5 (n = 290), same quarter | 2 |
| Cross-side, parents to tutors | More parents means fuller calendars, so tutors stay | Positive | Tutor 90-day retention is 72% above 6 bookings a week and 41% below 3, but busier tutors may simply be better tutors; no matched comparison yet | 1 |
| Same-side, tutors | More tutors in a postcode lowers each tutor's bookings | Negative | Bookings per tutor fell from 7.1 to 5.4 a week in the city where tutor count doubled in eight weeks | 2 |
| Same-side, parents | Other parents' reviews help a parent choose | Positive | Asserted, no data | 0 |

Lift for the first row: (56 minus 35) / 35 = 0.60, a 60% relative lift on 700 searches, which scores 2.

**Take rate,** for the quarter. 9,600 sessions at an average of £40 give GTV of £384,000. Tutor commission at 15% is £57,600 and the parent booking fee of £1.50 a session is £14,400, so fees are £72,000 and the headline take rate is 72,000 / 384,000 = 18.75%. The platform absorbed £4,800 of refunds, paid £11,000 in first-session discounts (1,100 new parents at £10) and £3,000 in tutor sign-up bonuses (60 at £50). Effective take rate = (72,000 minus 4,800 minus 11,000 minus 3,000) / 384,000 = 53,200 / 384,000 = 13.9%. The gap of almost five points is mostly the parent discount, spent on the side that was never scarce.

**Disintermediation.** Q1 yes: tutor and parent meet at every session. Q2 yes: going direct saves £7.50 a session, about £30 a month for a weekly pair. Q3 no for most pairs: the platform's reminders and payment collection matter only to tutors who struggle to collect, about a fifth of repeat pairs. Q4 not reached. Leakage risk HIGH. Repeat pairs carry 70% of GTV, so exposed GTV = 384,000 × 0.70 × 0.80 = £215,040, and revenue at risk = 215,040 × 0.139 = about £29,900 a quarter.

**Governance, the row that mattered.** Contact outside the platform: the terms ban direct booking with a matched parent for 12 months, enforced by nobody, with no review capacity named. That rule is the only thing behind the Q3 answer, which is why Q4 would have come back no even if Q3 had been yes.

**Decision.** Stop the parent first-session discount and move the spend to tutor-side value: automatic termly invoicing and a rebooking commission of 8% after a pair's fifth session. Pause tutor acquisition in the doubled city until bookings per tutor are back above 6.5 a week. Re-run Parts 2 and 6 next quarter. The Seven Powers network economies row takes the tutors-to-parents effect as benefit 2 and barrier 1: the effect is local to a postcode, and a rival that recruits denser tutor supply in one postcode takes that postcode.

## The trap

The network effect claimed from growth. The evidence column holds a chart of total users rising, and the statement reads "the more users we have, the better it gets". Aggregate growth is what a network effect looks like and also what a good marketing budget looks like; only a comparison within segments, matched on when members joined, tells them apart. The second tell travels with the first: no negative row. Every platform that grows its scarce side eventually crowds it, and a canvas with four positive effects has not looked. Hold the line in Part 2: a 2 needs a matched-density comparison with counts, and the sheet is not finished until it has a negative row or a written reason it has none.

## Feeds

- [Seven Powers audit](seven-powers-audit.md): the network economies row, benefit evidence from Part 2 and the multi-homing answer for the barrier
- [Product strategy](../../templates/planning/product-strategy.md): section 3 (how we win), the "why it holds" line, and section 6 (key risks) for a HIGH leakage result
- [Pricing and packaging](../../templates/planning/pricing-packaging.md): section 2 (pricing model), where the take rate is the price and Part 6 sets its ceiling
- [North star metric](../../templates/planning/north-star-metric.md): section 2, liquidity in the smallest self-sustaining unit from Part 3 as an input metric
- [Personas](../../templates/discovery/personas.md): one per side, the constrained side treated in more depth
- [Business case](../../templates/planning/business-case.md): seeding cost and trust-and-safety capacity from Parts 3 and 5 as standing cost lines
- [Risk register](../../templates/execution/risk-register.md): HIGH leakage with its revenue at risk, and every negative effect scored 2
- [Growth loops](../metrics/growth-loops.md): where a cross-side effect at 2 becomes a loop with its own arithmetic
- PLANNING track, feeds Gate 1
- Method background: the [marketplaces domain card](../../knowledge/domains/marketplaces.md)
