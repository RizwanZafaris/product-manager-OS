# RICE Prioritization

Based on the ideas of Sean McBride, developed at Intercom and published on the Intercom blog (2016).

## The essence

RICE exists to solve a specific meeting: five initiatives, four advocates, and no shared basis for comparison. It scores each initiative on four factors and produces one comparable number.

- **Reach.** How many people does this touch per time period? A count from real data: users per quarter, transactions per month. Not a percentage of an imagined market.
- **Impact.** How much does it move the goal for each person reached? Scored on a coarse scale (3 for massive, 2 for high, 1 for medium, 0.5 for low, 0.25 for minimal), coarse on purpose, because finer claims to precision would be fiction.
- **Confidence.** How much of the above do you actually believe? 100 percent for shipped-and-measured certainty, 80 percent for evidence, 50 percent for educated hope. Below 50 percent, the honest move is to go get evidence, not to score.
- **Effort.** Person-months, from the people who would do the work.

Score = (Reach x Impact x Confidence) / Effort. The confidence factor is the quiet genius of the scheme: it taxes enthusiasm. A gigantic reach estimate built on air gets multiplied by the air.

## When to use it

- When a roadmap has more candidates than capacity and the ordering debate has gone circular.
- When two initiatives feel equally urgent, as a forcing function to write down the beliefs behind each and see which one is built on measurement and which on adrenaline.
- When saying no: a low score with visible inputs is a kinder and more durable rejection than a manager's mood.

**Skip it when:** the list is under five items, or the items are not comparable. A compliance mandate scored against a revenue feature produces a number that looks like a decision and is not one; mandates get a deadline lane instead. Two obvious priorities and a clear third do not need arithmetic to sort them.

## The trap: false precision

The output is a number, and numbers borrow authority they have not earned. A score of 47.3 beats a score of 45.1 on the spreadsheet, but three of the four inputs were estimates with error bars wider than the gap, so the ranking of those two rows is noise presented as arithmetic. Teams then defend the number instead of the beliefs behind it, and the tool built to expose assumptions starts laundering them. The discipline: treat scores as buckets, not rankings; near scores are ties, and ties get resolved by judgment, in the open. The score's real product was never the number. It was the argument you had to have about reach and confidence to produce it.

## Used by

- [Roadmap](../templates/planning/roadmap.md)
- [Discovery document](../templates/discovery/discovery-document.md)

**Run it:** the worksheet form of this method lives in the [frameworks layer](../frameworks/README.md).

- [RICE scoring sheet](../frameworks/prioritization/rice-scoring-sheet.md), the sheet that runs this method, with the arithmetic written out
