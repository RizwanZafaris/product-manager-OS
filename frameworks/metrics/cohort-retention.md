# Cohort Retention

Based on cohort analysis as brought into product work by Eric Ries, from The Lean Startup (2011), with roots in demography and epidemiology. Explained here in this repository's own words.

## What it is for

Whether the people who arrive keep getting value, measured separately from how many arrive. A cohort table groups users by when they started and shows what share is still active at each age. The shape of that curve is the finding: a curve that flattens means a retained core exists and the product has a habit; a curve that keeps falling means a leaky bucket that acquisition is refilling. The decisions it improves: whether to spend on acquisition or on the product, whether growth in active users is real or a backlog of arrivals, and what lifetime the unit economics may honestly assume.

## Run it when

- Before scaling acquisition, because a loop or campaign multiplies whatever the curve does
- After a launch, at the first three periods, to see whether the new cohorts retain differently from the old
- When active-user counts rise but the team suspects churn underneath
- To compare two onboarding versions or two channels on the same age

**Skip it when:** the product has been live for less time than one retention period, or cohorts hold a few dozen people. A table with one filled cell is not a curve, and a curve drawn through cells of 30 people is noise; run interviews and the PMF survey instead.

## Inputs you need first

- The definition of active: the core action from the [north star input tree](north-star-input-tree.md), never a login
- The cohort key: first core action, with the date, per user
- Channel, segment, and onboarding variant per user
- At least three completed periods; the current period is partial and always looks worse

## The worksheet

### Step 1: definitions

| Field | Answer |
|---|---|
| Active means | [the core action, with its event name] |
| Cohort key | [first core action; not sign-up, which mixes in people who never tried] |
| Period | [week or month, matching the natural cadence of the core action] |
| Segments to cut | [channel, plan, company size, onboarding version, opted-in versus mandated] |
| Denominator rule | [cohort size at period 0; state whether accounts that ended by contract are removed] |

### Step 2: the table

Percent of the cohort active in each period after its start. Rows are cohorts, columns are age, and a diagonal is one calendar period.

| Cohort (start period) | Size | P0 | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|---|---|
| [period] | [n] | 100 | | | | | |
| [period] | [n] | 100 | | | | | |

Flattening test: the drop between consecutive periods shrinks toward zero. Record the plateau level and the period it arrives at; those two numbers are the result.

### Step 3: what to compare

| Comparison | What it tells you | Watch out for |
|---|---|---|
| Same age, successive cohorts (down a column) | Whether the product or the acquisition mix changed | Newer cohorts are younger and often larger |
| Same cohort, by channel | Channel quality, not product quality | Small cells |
| Same cohort, by onboarding variant | Whether the variant retained better | Selection bias unless assignment was random |
| Plateau level against the lifetime the [unit economics](unit-economics.md) assumed | Whether the business case still holds | A plateau read from cohorts too young to have one |

## Reading the result

Three shapes. Flattening: a plateau exists; the level is the retained core, and the period it arrives at is how long onboarding has to earn it. Decaying: no plateau; do not scale acquisition, fix the product or the definition of who gets acquired. Smiling: a rise after a dip, which is seasonality, a re-engagement campaign, or a definition bug, and needs an explanation before it counts as good news. Read down a column before reading across a row: if recent cohorts retain worse at the same age, ask whether the product got worse or the acquisition got broader. Report the plateau and the latest cohort's P1 together; one without the other invites the wrong conclusion.

Common misreads: mixing acquisition channels, so a shift toward paid users looks like product decline; survivorship, where the oldest cohorts contain only the people who survived a product that no longer exists, and their tail cells hold a handful of users; cohorting on sign-up instead of activation, which makes retention look terrible and then "improves" when someone fixes the definition; treating the partial current period as a real drop; and a calendar event (a holiday, an outage) that hits every cohort on one diagonal and reads as an age effect.

## ILLUSTRATIVE example

Invented figures for Ledgerline's expense-report copilot. Monthly cohorts by first submitted copilot draft; active means at least one copilot-drafted report submitted in the month.

| Cohort | Size | P0 | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|---|---|
| January | 410 | 100 | 71 | 63 | 58 | 57 | 56 |
| February | 520 | 100 | 68 | 60 | 55 | 54 | |
| March | 690 | 100 | 74 | 66 | 61 | | |
| April | 880 | 100 | 77 | 70 | | | |
| May | 1,150 | 100 | 66 | | | | |
| June | 1,300 | 100 | | | | | |

Reading: January flattens near 56 by P3. P1 improves from January to April (71 to 77) after the mailbox-connect fix shipped in March. May falls to 66, which coincides with finance mandating the copilot for all employees; cut by opted-in versus mandated, the May P1 is 76 and 55 respectively. The product did not regress; the acquisition got broader. A second finding is the definition: many employees file an expense only every few months, so a monthly "active" counts people with no expenses as churned. The team re-cut the table with active defined as "of employees who filed any report this month, filed it through the copilot", and the plateau moved from 56 to 81.

## The trap

Reading the plateau off the tail. The right-most cells belong to the oldest cohorts, from before the product was what it is now, and they hold the fewest people. Teams read the retained core from those cells and promise a lifetime the current product has not demonstrated. In the example, January's 56 rests on 230 people; the plateau the business case may use is the one the March and April cohorts reach, once they are old enough to reach it. Until then, the honest entry in the assumptions register is a range.

## Feeds

- [Metrics review](../../templates/operate/metrics-review.md), section 2, where the input metric movement is read
- [Growth plan](../../templates/planning/growth-plan.md), section 1 and the leak evidence in section 3
- [Unit economics](unit-economics.md), which takes the plateau as its churn input
- [Post-launch review](../../templates/operate/post-launch-review.md), section 2, goal versus actual
- The [analyst agent](../../agents/analyst-agent.md) reads cohorts before it reads averages
- OPERATE stage, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: [Lean Startup entry in the knowledge index](../../knowledge/INDEX.md)
