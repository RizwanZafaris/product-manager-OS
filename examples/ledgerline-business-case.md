# Business Case: Expense Copilot

Fills [templates/planning/business-case.md](../templates/planning/business-case.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional internal product used across this repository, the people are roles, and every cost, rate, hour and dollar is ILLUSTRATIVE, chosen so the arithmetic can be followed and checked. None of it is a benchmark, a target, or a claim about what such a product costs or returns. The case was written for Gate 1 and read again at Gate 2. See the [examples index](README.md).

**Owner:** the PM · **Sponsor:** the finance lead (budget owner) · **Date:** 2026-08-13 · **Status:** Approved at Gate 1 · **Horizon:** three years, payback measured from launch

## 1. The problem in one paragraph

Filers re-type receipt data and bounce on a policy they have never read; three reviewers spend about 30 hours a month on mechanical checks; expense tickets tripled in two quarters. Evidence and the GO are in the [discovery document](expense-copilot-discovery.md). This case answers the question that document leaves open: is fixing it worth the money, against the alternatives.

## 2. Inputs (all ILLUSTRATIVE)

| Input | Value | Source | Firmness |
|---|---|---|---|
| Reports per year | 9,600 (2,400 a quarter) | finance system, quarter ending 2026-06-30 | measured |
| Median filing time today | 25 minutes | timed sessions in discovery, n=8 | directional |
| Filing time with a draft | 10 minutes | PRD objective 2 | target, not evidence |
| Share of reports through the draft flow, year one | 60% | PRD objective 3 is 50% by month two; 60% assumes it keeps rising | assumption |
| First-submission approval, today and target | 62% and 80% | finance system; PRD objective 1 | measured; target |
| Cost of a bounce | 30 minutes across filer and reviewer | reviewer time logs plus interview estimates | estimate |
| Loaded hourly rate, filer and reviewer | $55 and $60 | finance planning rates | see Open |
| Build effort | 11 person-months at $10,000 each | engineering lead: two engineers for four months, plus design and product time | estimate |
| Run cost | $2,500 a month | hosting, model API at quoted volume pricing, on-call share | quoted, not contracted |

## 3. Options

| Option | What it is | One-off cost | Yearly run cost | Yearly benefit | Payback |
|---|---|---|---|---|---|
| 0. Do nothing | Tickets stay tripled; reviewers keep the mechanical pass | 0 | 0 | 0, while the cost of inaction below keeps accruing | N/A because nothing is spent |
| 1. Better form | Validation rules on the existing form: totals, missing receipt, required fields | $20,000 (2 person-months) | 0 | about $8,000: catches some bounce causes, none of the re-typing | about 30 months |
| 2. Copilot v1 | Draft from the receipt, category with policy line, filer submits | $110,000 | $30,000 | $113,180 gross, $83,180 net | about 16 months |
| 3. Buy a vendor tool | Replace the form with a vendor product that has receipt capture | $30,000 integration (3 person-months) | about $86,400 in licences, at $8 a seat a month for 900 seats | similar to option 2 before licences; about $27,000 net after them | about 13 months on the integration cost, but the licence eats most of the benefit every year |

Cost of inaction, the number Gate 1 asks for with the calculation shown: 9,600 reports x 25 minutes = 4,000 filer hours a year, at $55 = $220,000 of filer time; plus 360 reviewer hours a year on mechanical checks, at $60 = $21,600; plus rework on 3,648 bounces at half an hour each = 1,824 hours, about $100,000 blended. None of this is cash a budget can recover. It is time, and the case says so rather than dressing it up as savings.

## 4. The arithmetic for option 2

Yearly benefit, each line built on the inputs above:

1. Filing time: 9,600 x 60% = 5,760 drafted reports x 15 minutes saved = 1,440 hours x $55 = $79,200.
2. Fewer bounces: approval on drafted reports rises from 62% to 80%, 18 percentage points x 5,760 = about 1,037, rounded down to 1,000 fewer bounces x 30 minutes = 500 hours x $55 = $27,500.
3. Reviewer mechanical pass: 30 hours a month, halved on drafted reports, at 60% adoption = 9 hours a month = 108 hours a year x $60 = $6,480.

Gross: 79,200 + 27,500 + 6,480 = $113,180. Net of run cost: 113,180 minus 30,000 = $83,180 a year, or $6,932 a month.

Payback = 110,000 / 6,932 = 15.9 months.

Three-year NPV at an ILLUSTRATIVE 10% discount rate: minus 110,000, plus 83,180 / 1.1 + 83,180 / 1.21 + 83,180 / 1.331 = minus 110,000 + 75,618 + 68,744 + 62,494 = about $96,900.

## 5. Sensitivities

One input moved at a time, everything else held.

| Input moved | Net yearly benefit | Payback |
|---|---|---|
| Adoption 30% instead of 60% | $26,590 | about 50 months: the case fails inside the horizon |
| Adoption 100% | $158,600 | about 8 months |
| Filing time falls to 15 minutes, not 10 | $56,780 | about 23 months |
| Approval reaches 70%, not 80% | $68,330 | about 19 months |
| Run cost doubles to $5,000 a month | $53,180 | about 25 months |

Adoption is the swing variable by a wide margin, which is why PRD objective 3 is voluntary adoption with a number and a date, and why this case carries a kill condition rather than a promise.

## 6. Recommendation and kill condition

Option 2, funded for v1 only, with adoption as the tripwire: if under 30% of eligible reports use the draft flow by the end of month two, scope growth stops and the persist, pivot, or sunset decision is taken in writing at the first metrics review, because at that adoption the case does not pay back inside the horizon. Option 3 stays on file as the fallback if v1 extraction cannot hold its eval threshold; the vendor's capture quality is the one thing it clearly has that v1 does not. Option 1 is not funded: it is the "better form" the finance lead first asked for, and it attacks the symptom.

Argued against at Gate 1, as the gate requires: the sponsor made the case for option 3 on speed to value. It lost on licence cost and on the vendor-terms question, which was unresolved for both options and is carried as a gap in the [PRD](expense-copilot-prd.md).

## Open

- [OPEN: the $55 and $60 hourly rates are finance planning rates, not measured costs. The finance lead owns confirming them; the case is re-run if either moves by more than a fifth.]
- [OPEN: model API pricing is a quote at an assumed volume of about 40,000 receipts a year. Procurement owns the contracted price, and the run cost line is soft until then.]
- [OPEN: filer time recovered is not a budget line anyone can bank. The sponsor accepted it as the basis for a GO; the QBR must not convert the same evenings into dollars a second time. The PM owns the wording in the first board update.]

## Feeds

- Gate 1 (problem worth solving) in [os/STAGE-GATES.md](../os/STAGE-GATES.md): the cost of inaction line with its calculation, and the no-go argument.
- [templates/planning/roadmap.md](../templates/planning/roadmap.md): the kill condition is the precondition on every Next item.
- [templates/definition/assumptions-register.md](../templates/definition/assumptions-register.md): the adoption and rate assumptions, each with an owner.
- The blank template at `templates/planning/business-case.md`.
