# Portfolio Review: Tallowmere product group, Q3 2026 results and Q4 2026 allocation

Fills [templates/planning/portfolio-review.md](../templates/planning/portfolio-review.md). Everything here is invented for this standalone example: Tallowmere is a fictional maker of practice software for independent veterinary clinics, its product lines and people are invented, and every count, euro figure and date is ILLUSTRATIVE, not drawn from any real company or market. The allocation arithmetic is the same one worked in the [portfolio allocation worksheet](../frameworks/strategy/portfolio-allocation.md) example. See the [examples index](README.md).

All figures are ILLUSTRATIVE.

**Owner:** Saoirse Brennan, head of product · **Finance partner:** Delphine Marchetti · **Date held:** 2026-10-14 · **Status:** Decided
**Period reviewed:** Q3 2026 · **Period allocated:** Q4 2026 · **Previous review:** held 2026-07-15, in the Tallowmere planning workspace, not in this repository
**Money unit:** EUR thousands, per quarter · **People unit:** people · **Loaded cost per person per quarter:** 35 (ILLUSTRATIVE, from finance)

## 1. Lines and bets in scope

| Line or bet | Loop stage | Horizon | Lifecycle | Line owner | Last review's decision |
|---|---|---|---|---|---|
| Clinic, the practice management suite | OPERATE | H1 | Mature | Hamid Rostami, GM Clinic | Sustain |
| Reminders, the paid SMS add-on | OPERATE | H1 | Declining | Ola Nwosu, PM | Sustain, with a cause to explain at this review |
| Desktop, the on-premise edition | OPERATE | H1 | Declining | Pieter Voss, engineering manager | Sustain, with a migration target of 90 clinics remaining |
| Pay, card payments inside Clinic billing | OPERATE | H2 | Growing | Yuki Tanabe, PM | Invest |
| Owner app, self-booking for pet owners | DISCOVER | H3 | New | Leila Haddad, PM | Tranche 1 granted, E0, 2 people for 6 weeks |
| Claims link, claims data sold to pet insurers | DISCOVER | H3 | New | Tomas Ferreira, PM | Not yet proposed |

Horizons were scored by Delphine Marchetti and the Clinic GM, neither of whom proposes an H3 bet, using the worksheet's Part 1 definitions before section 4 was computed.

## 2. Outcome metric against target

| Line | Outcome metric (dictionary entry) | Target | Actual | Last period | Source system | One sentence of cause, or "unexplained" |
|---|---|---|---|---|---|---|
| Clinic | Gross clinic retention, trailing 12 months | 92 percent | 93 percent | 92 percent | Billing system | Two multi-site groups renewed early after the records-search release |
| Pay | Share of Clinic customers processing card payments through Pay | 30 percent | 28 percent | 24 percent | Pay ledger joined to Clinic accounts | Terminal setup still needs a call with support; the clinics that finish it stay |
| Reminders | Rebooked appointments attributed to an SMS reminder, per subscribing clinic per month | 40 | 31 | 35 | Reminders event log | Clinic's free email reminder, shipped in Q1, now takes the easy rebookings; subscribers fell from 610 to 540 clinics |
| Desktop | Clinics still on Desktop | 90 | 96 | 104 | Licence server | Migration needs a data export Desktop cannot produce for clinics on versions older than 7 |

## 3. Product-line P&L

Definitions as in the template, agreed with Delphine Marchetti on 2026-04-09. Pay revenue is net of card scheme and processor fees.

| Line | Revenue | Cost to serve | Dedicated team cost (people) | Direct cost | Contribution | Contribution margin | Last period contribution |
|---|---|---|---|---|---|---|---|
| Clinic | 4,200 | 520 | 1,750 (50) | 2,270 | 1,930 | 46 percent | 1,880 |
| Pay | 900 | 260 | 350 (10) | 610 | 290 | 32 percent | 210 |
| Reminders | 380 | 150 | 280 (8) | 430 | -50 | -13 percent | -10 |
| Desktop | 240 | 60 | 350 (10) | 410 | -170 | -71 percent | -140 |
| Owner app | 0 | 5 | 70 (2) | 75 | -75 | not meaningful, read in section 5 | -70 |
| Total, lines | 5,720 | 995 | 2,800 (80) | 3,795 | 1,925 | 34 percent | 1,870 |
| Fixed product and engineering work, not allocated | | | 350 (10) | 350 | | | |
| Contribution after fixed product and engineering work | | | | | 1,575 | | |

Arithmetic, Clinic row: dedicated team cost = 50 x 35 = 1,750; direct cost = 520 + 1,750 = 2,270; contribution = 4,200 - 2,270 = 1,930; margin = 1,930 / 4,200 x 100 = 45.95, shown as 46 percent. Totals: contribution = 5,720 - 3,795 = 1,925, which matches the row sum 1,930 + 290 - 50 - 170 - 75 = 1,925. After fixed work: 1,925 - (10 x 35 = 350) = 1,575. Sales, marketing and general costs sit in finance's full P&L and are not allocated here.

## 4. Investment and headcount by horizon

Total pool: 90 people · Fixed work, excluded: 10 · Allocatable: 80 · Move limit this period: 5 points = 4 people

| Horizon | Target share | Why this target | People now | Share now | Gap (points) | Gap (people) | Move this period | People next period | Team cost next period |
|---|---|---|---|---|---|---|---|---|---|
| H1 | 75 percent | Clinic still carries the company; Reminders and Desktop are where H1 gives people back | 68 | 85.0 percent | -10.0 | -8 | -4 | 64 | 2,240 |
| H2 | 15 percent | Pay is the only H2 line and can use two more people this quarter, not the ten 70/20/10 would imply | 10 | 12.5 percent | +2.5 | +2 | +2 | 12 | 420 |
| H3 | 10 percent | Two live bets, and the board asked for a funded second business by 2028 | 2 | 2.5 percent | +7.5 | +6 | +2 | 4 | 140 |
| Total | 100 percent | | 80 | 100 percent | 0 | 0 | 0 | 80 | 2,800 |

Gap arithmetic: -10.0 / 100 x 80 = -8; 2.5 / 100 x 80 = +2; 7.5 / 100 x 80 = +6; sum zero. Positive gaps total 10 points, so at 5 points a quarter the gap closes no sooner than the end of Q1 2027. Team cost next period = people next period x 35.

## 5. Bets judged against a milestone

| Bet | Horizon | Evidence level, dated source | Tranche held | Milestone set last review | Met? | Verdict | Next tranche (within cap) | Kill criterion for the next tranche | Next review |
|---|---|---|---|---|---|---|---|---|---|
| Owner app | H3 | E1: seven owner interviews, 2026-08-24 to 2026-09-11, phone booking named as the alternative; front-desk tickets asking for self-booking | 2 people, 6 weeks | Five or more owner interviews, the alternative named, a prototype walked through with two clinics' front desks | Yes, 2026-10-02 | Continue, now E1 | 3 people, 6 weeks: a three-clinic pilot (E1 cap is 4; the move limit bound) | Fewer than 10 percent of invited owners book through the app at least once during the pilot | 2026-11-26 |
| Claims link | H3 | E0: one insurer's product lead expressed interest at a trade conference, 2026-09-17 | None | None, new this review | Not applicable | New tranche | 1 person, 6 weeks, discovery only (E0 cap is 2 people) | No insurer shares its claim format within the tranche | 2026-11-26 |

## 6. Decision per line

| Line | Decision | Investment change (people, money) | Why, citing sections 2 to 5 | What would reverse it | Owner | Recorded in |
|---|---|---|---|---|---|---|
| Clinic | Sustain | 0 people, 0 | Retention above target (section 2); contribution 1,930, up from 1,880, at a 46 percent margin (section 3) | Retention below 92 percent for two quarters | Hamid Rostami | Decision log D-041 |
| Pay | Invest | +2 people, +70 per quarter | Adoption 28 against a 30 percent milestone, first miss, but up 4 points in a quarter; contribution 210 to 290; the two people build self-serve terminal setup, sized by the Pay business case approved 2026-07-20 (held in the finance workspace, not in this repository) | Adoption below 30 percent at the end of Q4, a second miss, sends the terminal bet back for pivot or kill | Yuki Tanabe | D-042 |
| Reminders | Harvest | -2 people, -70 per quarter | Rebookings falling for three quarters and contribution negative (sections 2 and 3); the free email reminder in Clinic is the better product for most clinics | Revenue below 360 in Q4, which puts contribution back under zero at the new floor and opens a sunset review | Ola Nwosu | D-043 |
| Desktop | Sunset | -2 people this quarter, -70 per quarter; to 2 people by the end of Q2 2027 | Contribution negative two periods running and getting worse, -140 then -170 (section 3); 96 clinics left, and Clinic is the migration path | None planned; this is a one-way door for 96 clinics, taken through a decision memo on 2026-10-07 | Pieter Voss | D-044, and SUNSET in Desktop's Q3 metrics review, section 5 |

Harvest floors: Reminders at 6 people, covering SMS delivery, carrier registration renewals, billing and second-line support. No new features. At flat revenue, contribution = 380 - 150 - (6 x 35 = 210) = +20.
Invest rows above the E2 cap, each with its approved business case: Pay, the Pay business case approved 2026-07-20, held in the finance workspace.
Sunset plans opened, each a copy of the sunset plan with that line's metrics review as its decision source: Desktop, from [templates/operate/sunset-eol-plan.md](../templates/operate/sunset-eol-plan.md), owner Pieter Voss; first customer notice 2026-11-16; shutdown target 2027-06-30. The 8 people staying on Desktop this quarter include the export tool for pre-version-7 clinics, without which the migration path in that plan does not exist.

## 7. Dissent and open items

| Item | Raised by | Resolution, or owner and due date |
|---|---|---|
| Dissent: moving two Desktop engineers before the export tool ships risks the sunset date | Pieter Voss | Accepted with a condition: the two who move come from Desktop feature work, which stops; the export tool keeps its four engineers. Recorded in D-044 |
| Dissent: the owner app should get its full E1 cap of 4 | Leila Haddad | Declined this quarter because of the move limit, not the evidence; she may ask again at the 2026-11-26 tranche review |
| [OPEN: Pay's September revenue is finance's estimate until the processor's reconciled statement arrives. If it moves by more than 40, sections 3 and 6 are reissued for Pay] | Delphine Marchetti | Delphine Marchetti, 2026-10-28 |
| [OPEN: H3 discovery shortfall. The two bets' caps total 4 + 2 = 6 people against an H3 target of 8, so H3 cannot reach target even without the move limit. The two-person difference is lent to H1 this quarter and reported as a loan] | Saoirse Brennan | Saoirse Brennan brings at least one more H3 candidate at E1 or better to the Q1 2027 review, 2027-01-12 |

## Exit gate

Done when every box is honestly ticked. This file declares no gate; its decisions travel to the gates of the lines they touch.

- [x] Every line and bet drawing on the pool appears in section 1, and the people in section 4 sum to the allocatable pool (50 + 8 + 10 + 10 + 2 = 80)
- [x] Every row in section 2 carries its target, its source system and a cause or "unexplained"
- [x] Section 3 uses recognized revenue reconciled with the finance partner, or the gap is an open item with an owner; no shared cost is allocated; contribution = revenue - direct cost checks on every row (Pay's September revenue is the open item in section 7, owned by Delphine Marchetti, due 2026-10-28)
- [x] Every horizon target has a written reason, and the three gaps sum to zero
- [x] This period's move is within the move limit, or the exception is recorded with its reason (4 people, exactly the limit)
- [x] Every bet in section 5 has an evidence level with a dated source, a tranche within its cap, and a kill criterion written before the tranche starts
- [x] Every line that earns revenue in section 3 has exactly one of invest, sustain, harvest or sunset, with an owner and a reversal condition (the owner app earns nothing yet and takes its verdict from section 5)
- [x] Every invest above the E2 cap names its business case, every harvest names its floor, and every sunset names its metrics review and its sunset plan (Pay is E3 and names its business case)
- [x] Dissent is recorded with names, and every decision is in the decision log (D-041 to D-044)
- [x] The portfolio-level roadmap and the capacity plan have been updated to match section 6, or the date they will be is written here (not yet updated; both due 2026-10-21, owner Saoirse Brennan)

Signed: Saoirse Brennan, head of product, 2026-10-14
