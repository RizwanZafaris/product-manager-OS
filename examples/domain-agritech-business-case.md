# Business Case: Extending Maizeline from one pilot district to four

Fills [templates/planning/business-case.md](../templates/planning/business-case.md). Everything here is invented for this standalone example: Maizeline is a fictional agri-input credit programme in Kenya, the people are roles filled by invented names, and every count, shilling figure and date is ILLUSTRATIVE. This file is self-contained; there is no external Maizeline journey or shared data sheet. The assumptions this case draws on are listed in the table below, each with its own id, so the numbers can be checked against each other and against the sections that use them. See the [examples index](README.md).

**Owner:** Wanjiru Kamau, head of product, Maizeline · **Sponsor:** Daniel Otieno, chief executive · **Finance partner:** Elif Demirci, finance lead · **Date:** 2026-09-11 · **Status:** Draft, in review
**Money unit:** KES, thousands · **Discount rate:** 12 percent, from finance · **Regulatory statements as of 2026-09-11, confirm with counsel; not legal advice**

## 1. The decision

Maizeline lends seed and fertiliser to smallholder maize farmers through farmer cooperatives, repaid in cash at harvest, and the repayment terms and input recommendations are reached and delivered over USSD on feature phones. The pilot district in Nakuru County (Nakuru North, a fictional sub-county for this example) ran the 2025 long-rains season and the 2026 long-rains season. The decision before Daniel Otieno and the Maizeline board, by 2026-10-31, is which of five options to adopt for the 2027 long-rains season: A do nothing, B cooperative-only, C four districts, D buy or partner, or E two districts, each as named and modelled in section 2.

The Gate 1 problem statement cost of inaction is the input-credit gap the pilot addresses: farmers in the pilot district without Maizeline access bought certified seed late or not at all, planted on land they could not top-dress, and sold at the farm gate to a broker at a discount to cover a cash need. The pilot district's own contribution to that cost is KES 8,400 thousand a season, made up of an estimated 1,400 farmers (AS-01) at a conservative KES 6,000 a farmer of lost margin from late or missed input purchase (AS-03). Farm size across the pilot averages 1.4 hectares a farmer (AS-02); that figure is carried for context, not applied as a per-hectare multiplier below, because Maizeline's own records are kept per farmer, not per plot. The KES 8,400 thousand figure is the do-nothing row below and the baseline every other option is measured against.

### Assumptions used in this example

Every number in sections 3 and 5 traces to one of these rows. A formal filing of the same rows into [assumptions-register.md](../templates/definition/assumptions-register.md) is a Gate 2 follow-up; see the exit-gate walk.

| ID | Assumption | Value | Confidence |
|---|---|---|---|
| AS-01 | Pilot-district farmers reached | 1,400 farmers | High, pilot count |
| AS-02 | Average farm size in the pilot | 1.4 hectares a farmer | Medium, context only |
| AS-03 | Lost margin from late or missed input purchase, the do-nothing cost | KES 6,000 a farmer a season | Medium |
| AS-04 | Borrowing shortfall avoided, full Maizeline service (options B and C) | KES 500 a farmer a season | Medium |
| AS-05 | Borrowing shortfall avoided, partner service (option D), lower because partner terms post later | KES 250 a farmer a season | Low |
| AS-06 | Value of the tailored-recommendation yield uplift, weather-adjusted | KES 10,000 a farmer a season | Medium |
| AS-07 | Repayment margin, full Maizeline service (option C) | KES 925 a farmer a season | Medium |
| AS-08 | Repayment margin, partner service (option D), a lower take than Maizeline's own | KES 750 a farmer a season | Low |
| AS-09 | Eligible farmers and adoption | 8,000 eligible across four districts; 70 percent adoption, 5,600 farmers | Medium |
| AS-10 | Base on-time repayment | 96 percent of the season's book, implying a 4 percent base default rate | Medium |
| AS-11 | Rain-scenario yield cut, one district | -30 percent against a normal season | Low, illustrative shock |
| AS-12 | Rain-scenario default rate, one district | Rises from the 4 percent base to 12 percent | Low, illustrative shock |
| AS-13 | Cooperative run cost, option B | KES 525 thousand a cooperative a season, four cooperatives | Medium |
| AS-14 | Maizeline-run district cost | KES 1,400 thousand a district a season | Medium |
| AS-15 | Average input loan a farmer a season | KES 2,545 | Low |
| AS-16 | Interest and fee take a farmer a season, base case | KES 1,027, a stated pricing assumption; AS-16 is the primary assumption here and AS-07's KES 925 margin is the derived figure (1,027 - (0.04 x 2,545) = 925). Note the circularity: the rain-row formula uses AS-16, and AS-07 only ever falls out of AS-16, so treat AS-16 as the input and AS-07 as the output, never the reverse | Low, stated pricing assumption, circular with AS-07 |
| AS-17 | Partner-service yield gap, option D | 0.08, a smaller yield gap than Maizeline's own because the partner's generic recommendation is less tailored | Low |
| AS-18 | Two-district eligible farmers and adoption (option E) | 4,000 eligible across two districts; 70 percent adoption, 2,800 farmers | Medium, derived from AS-09's four-district scope halved |

The repayment-margin rows (AS-07, AS-08) are a farmer's interest and fee take (AS-16) less expected default (default rate x loan a farmer, AS-15): at the 4 percent base, 1,027 - (0.04 x 2,545) = 1,027 - 102 = 925, AS-07. Section 5's rain row uses the same formula at the 12 percent shock default rate (AS-12).

## 2. Options, including doing nothing

The five options are measured against option A, which costs the inaction figure every year. All figures ILLUSTRATIVE.

| Option | What it is, in one sentence | Cost, one line | Benefit, one line | Main risk |
|---|---|---|---|---|
| A. Do nothing | Stop Maizeline after the pilot and let the input-credit gap stand | KES 8,400 thousand a season in lost farmer margin, every season | None credited to the product | The gap widens as input prices rise; doing nothing is not free |
| B. Cooperative-only | Fund the four cooperatives to run a paper input-advance scheme with no Maizeline USSD or scoring layer | KES 6,300 thousand over three seasons (KES 2,100 a season across four cooperatives, AS-13), born by the cooperatives and their members | Farmers reach seed and fertiliser earlier in the season | Repayment discipline is whatever the cooperative can enforce face to face; no weather or default signal |
| C. Four districts | Extend Maizeline to Nakuru, Kakamega, Bungoma and Trans Nzoia counties for the 2027 long-rains season | KES 11,200 thousand build and season cost across four districts | The pilot's weather-adjusted yield gap applied at four-district scale | Below-normal rain in one district cuts yield and lifts default together; the case cannot fund the shortfall from the other three |
| D. Buy or partner with an existing input-credit provider | White-label a working input-credit book from a licensed Kenyan lender and run Maizeline as the front end | KES 3,600 thousand a season in licence and servicing fees | Faster route to four districts without building the scoring and collections layer | The partner's terms and turnaround times, not Maizeline's, are the farmer experience; the product's differentiating tailoring is lost |
| E. Two districts | Extend Maizeline to the pilot district, Nakuru, plus Kakamega County for the 2027 long-rains season | KES 3,400 thousand build plus KES 2,800 thousand a season across two districts | The pilot's weather-adjusted yield gap applied at two-district scale, with a second rainfall regime to test it before committing four | A single bad season still touches half the book, but only two cooperative carry the exposure rather than four |

## 3. Costs and benefits by year

Each table below is incremental to option A. Year 0 is the 2026 short-rains build period (no lending), Year 1 is the 2027 long-rains season, Year 2 is the 2028 long-rains season, and Year 3 is the 2029 long-rains season. Every benefit line names its method. Build cost is the estimator's likely figure; the range is in section 5. The repayment-margin benefit line is net of expected defaults at the season's base default rate; section 5's default-rate sensitivity is what moves it.

The weather-adjustment column is the reason the yield row is smaller than the headline: the raw pilot figure is less the same-district control figure, and only the difference is credited to the product, as the [agritech domain card](../knowledge/domains/agritech.md) question 5 requires. The 0.13 gap and the pilot's +34% against the control's +21% are locally stated illustrative assumptions for this case, not figures drawn from any supplied data sheet.

**Option B: Cooperative-only**, ILLUSTRATIVE until the method is agreed with Elif Demirci on 2026-10-02

| Line | Year 0 | Year 1 | Year 2 | Year 3 | Total | Method |
|---|---|---|---|---|---|---|
| Build cost | 0 | | | | 0 | cooperatives run the scheme; no Maizeline build |
| Run cost | | 2,100 | 2,100 | 2,100 | 6,300 | four cooperatives at KES 525 thousand each a season (AS-13) |
| Benefit: yield uplift, weather-adjusted | | 1,820 | 1,820 | 1,820 | 5,460 | 1,400 farmers x 0.13 yield gap x KES 10,000 margin a farmer (AS-06), cooperative-run only |
| Benefit: cost saved or risk avoided | | 700 | 700 | 700 | 2,100 | earlier planting avoids an estimated KES 500 a farmer in distress-sale discount (AS-04) |
| Net | 0 | 420 | 420 | 420 | 1,260 | |
| Cumulative net | 0 | 420 | 840 | 1,260 | | |

**Option C: Four districts**, ILLUSTRATIVE until the method is agreed with Elif Demirci on 2026-10-02

| Line | Year 0 | Year 1 | Year 2 | Year 3 | Total | Method |
|---|---|---|---|---|---|---|
| Build cost | 4,200 | | | | 4,200 | estimator, likely figure; range 3,400 to 5,600 |
| Run cost | | 5,600 | 5,600 | 5,600 | 16,800 | four districts at KES 1,400 thousand each a season (AS-14) |
| Benefit: revenue, repayment margin | | 5,180 | 5,180 | 5,180 | 15,540 | 5,600 farmers x KES 925 net margin a farmer a season (AS-07) |
| Benefit: yield uplift, weather-adjusted | | 7,280 | 7,280 | 7,280 | 21,840 | 5,600 farmers x 0.13 yield gap x KES 10,000 margin a farmer (AS-06) |
| Benefit: cost saved or risk avoided | | 2,800 | 2,800 | 2,800 | 8,400 | earlier planting avoids an estimated KES 500 a farmer in distress-sale discount (AS-04) |
| Net | -4,200 | 9,660 | 9,660 | 9,660 | 24,780 | |
| Cumulative net | -4,200 | 5,460 | 15,120 | 24,780 | | |

**Option D: Buy or partner**, ILLUSTRATIVE until the method is agreed with Elif Demirci on 2026-10-02

| Line | Year 0 | Year 1 | Year 2 | Year 3 | Total | Method |
|---|---|---|---|---|---|---|
| Build cost | 2,800 | | | | 2,800 | front-end integration to the partner's book |
| Run cost | | 3,600 | 3,600 | 3,600 | 10,800 | licence and servicing fees |
| Benefit: revenue, repayment margin | | 4,200 | 4,200 | 4,200 | 12,600 | 5,600 farmers x KES 750 net margin a farmer a season (AS-08), a lower take than option C |
| Benefit: yield uplift, weather-adjusted | | 4,480 | 4,480 | 4,480 | 13,440 | 5,600 farmers x 0.08 yield gap x KES 10,000 margin a farmer (AS-06, AS-17), the partner's generic recommendation is less tailored than Maizeline's own |
| Benefit: cost saved or risk avoided | | 1,400 | 1,400 | 1,400 | 4,200 | 5,600 farmers x KES 250 in distress-sale discount avoided a season (AS-05), lower than C because partner terms post later |
| Net | -2,800 | 6,480 | 6,480 | 6,480 | 16,640 | |
| Cumulative net | -2,800 | 3,680 | 10,160 | 16,640 | | |

**Option E: Two districts (the pilot district plus Kakamega County)**, ILLUSTRATIVE until the method is agreed with Elif Demirci on 2026-10-02

| Line | Year 0 | Year 1 | Year 2 | Year 3 | Total | Method |
|---|---|---|---|---|---|---|
| Build cost | 3,400 | | | | 3,400 | fixed core platform build plus one incremental district |
| Run cost | | 2,800 | 2,800 | 2,800 | 8,400 | two districts at KES 1,400 thousand each a season (AS-14) |
| Benefit: revenue, repayment margin | | 2,590 | 2,590 | 2,590 | 7,770 | 2,800 farmers x KES 925 net margin a farmer a season (AS-07), at two-district scale (AS-18) |
| Benefit: yield uplift, weather-adjusted | | 3,640 | 3,640 | 3,640 | 10,920 | 2,800 farmers x 0.13 yield gap x KES 10,000 margin a farmer (AS-06) |
| Benefit: cost saved or risk avoided | | 1,400 | 1,400 | 1,400 | 4,200 | 2,800 farmers x KES 500 in distress-sale discount avoided a season (AS-04) |
| Net | -3,400 | 4,830 | 4,830 | 4,830 | 11,090 | |
| Cumulative net | -3,400 | 1,430 | 6,260 | 11,090 | | |

### Repayments timed to harvest months

The maize long-rains harvest in these districts falls in October and November, and the loan is repaid out of the harvest sale in those months, not on a calendar quarter. This is where the payback arithmetic in section 4 differs from a ledger built on quarters: money leaves in the planting months and comes back in the harvest months of the same season, so a season is one annual cycle from March to November, not four calendar quarters.

## 4. Payback and NPV

Payback is the first year in which cumulative net turns positive. NPV sums each year's net divided by (1 + rate) to the power of the year. Rate is 12 percent. All figures ILLUSTRATIVE.

Worked line on option C: net by year is -4,200, +9,660, +9,660 and +9,660. Cumulative net is -4,200, +5,460, +15,120 and +24,780, so payback lands in year 1, the 2027 long-rains season. NPV = -4,200 + 9,660 / 1.12 + 9,660 / 1.2544 + 9,660 / 1.404928 = -4,200 + 8,625 + 7,701 + 6,876 = about +19,002.

Worked line on option D: net by year is -2,800, +6,480, +6,480 and +6,480. Cumulative net is -2,800, +3,680, +10,160 and +16,640, so payback lands in year 1. NPV = -2,800 + 6,480 / 1.12 + 6,480 / 1.2544 + 6,480 / 1.404928 = -2,800 + 5,786 + 5,166 + 4,613 = about +12,764.

Worked line on option B: net by year is 0, +420, +420 and +420. Cumulative net is 0, +420, +840 and +1,260, so payback lands in year 1 with no Year 0 build to recover. NPV = 420 / 1.12 + 420 / 1.2544 + 420 / 1.404928 = 375 + 335 + 299 = about +1,009.

Worked line on option E: net by year is -3,400, +4,830, +4,830 and +4,830. Cumulative net is -3,400, +1,430, +6,260 and +11,090, so payback lands in year 1. NPV = -3,400 + 4,830 / 1.12 + 4,830 / 1.2544 + 4,830 / 1.404928 = -3,400 + 4,313 + 3,850 + 3,438 = about +8,201.

- **Option A:** payback never; NPV = -8,400 / 1.12 + -8,400 / 1.2544 + -8,400 / 1.404928 = -7,500 + -6,697 + -5,979 = about -20,176 (the inaction cost, discounted, as a negative)
- **Option B:** payback year 1; NPV +1,009; 3-year net +1,260
- **Option C:** payback year 1; NPV +19,002; 3-year net +24,780
- **Option D:** payback year 1; NPV +12,764; 3-year net +16,640
- **Option E:** payback year 1; NPV +8,201; 3-year net +11,090

## 5. Sensitivities: what breaks the case

Each row changes one input to its pessimistic value and recomputes on option C, the full option, unless stated. The first row is the domain's defining risk: below-normal rain cuts yield and raises input-credit default together, and the two move in the same direction rather than offsetting.

| Input | Base | Pessimistic | NPV becomes | Payback becomes | Flips the recommendation? |
|---|---|---|---|---|---|
| *Rainfall: a below-normal long-rains season in one of four districts (ILLUSTRATIVE)* | *normal season yield and default (AS-06, AS-07)* | *one district at -30% yield and default up from an assumed 4% to 12% (AS-11, AS-12), carried for all three years* | *about +16,502* | *year 1* | *no, but it eats about an eighth of the NPV and makes four districts uncomfortable* |
| *Adoption share of eligible farmers (ILLUSTRATIVE)* | *70 percent, 5,600 of 8,000 eligible (AS-09)* | *40 percent, 3,200 of 8,000 eligible* | *about +7,494 plus the -4,200 Year 0, so about +3,294* | *year 2* | *no, but payback slips to year 2 and two districts become the safer entry* |
| *Build cost (ILLUSTRATIVE)* | *4,200* | *5,600, top of the estimator range* | *about +17,602* | *year 1* | *no* |
| *Repayment rate (ILLUSTRATIVE)* | *96 percent of the season's book repaid on time (AS-10)* | *82 percent repaid in time, the pilot's own worst-case in the 2025 season* | *about +14,200* | *year 1* | *no, but it removes the margin buffer for one bad district* |

*Build-cost row arithmetic, disclosed so it can be checked: the higher build cost increases the Year 0 outflow from 4,200 to 5,600, so NPV = -5,600 + 9,660 / 1.12 + 9,660 / 1.2544 + 9,660 / 1.404928 = -5,600 + 8,625 + 7,701 + 6,876 = about +17,602 (Year 0 is the only undiscounted term in section 4's method, so the whole extra 1,400 lands in the Year 0 term and nothing else moves). Cumulative net at Year 1 is -5,600 + 9,660 = 4,060, still positive, so payback stays in year 1. State your own benefit-versus-fixed-cost split and default formula for any sensitivity row; a row with no disclosed arithmetic is not reproducible and should not ship.*

*Repayment-rate row arithmetic, disclosed so it can be checked: at 82 percent repayment, the default rate is 18 percent. Margin a farmer = interest and fee take (AS-16, KES 1,027) minus (default rate x loan a farmer, AS-15's KES 2,545). At 18 percent default that is 1,027 - 458 = 569, a fall of 356 a farmer from AS-07's 925. Across 5,600 farmers that is 1,994 a year. Year 1 to 3 net becomes 9,660 - 1,994 = 7,666. NPV = -4,200 + 7,666 / 1.12 + 7,666 / 1.2544 + 7,666 / 1.404928 = -4,200 + 6,845 + 6,111 + 5,456 = about +14,212, rounded to about +14,200. Cumulative net at Year 1 is -4,200 + 7,666 = 3,466, still positive, so payback stays in year 1. State your own benefit-versus-fixed-cost split and default formula for any sensitivity row; a row with no disclosed arithmetic is not reproducible and should not ship.*

*Below-normal-rain-row arithmetic, disclosed so it can be checked: the affected district contributes about a quarter of the four-district benefit. Its weather-adjusted yield uplift row falls from 1,820 to 1,274 (a 30 percent cut, AS-11), and its distress-sale-avoided row falls from 700 to 490 (the same 30 percent cut). Its repayment-margin row falls under the formula set out with AS-16 above: margin a farmer = interest and fee take (AS-16, KES 1,027) minus (default rate x loan a farmer, AS-15's KES 2,545). At the 4 percent base (AS-10) that is 1,027 - 102 = 925, AS-07; at the rain scenario's 12 percent default (AS-12) it is 1,027 - 305 = 722, a fall of about 203 a farmer, or about 284 across option C's 1,400 farmers in one affected district, the district being a quarter of the 5,600 farmers across four districts (5,600 / 4 = 1,400; 1,400 x 203 = 284,200, rounded to 284). The other three districts are unchanged. The row carries this one-district shortfall for all three years, not only year 1: it models a permanent rain regime for that district, not a single-season shock. Year 1 net becomes 9,660 - (1,820 - 1,274) - 284 - (700 - 490) = 9,660 - 546 - 284 - 210 = 8,620. Applying the same year 1 to 3 flow of 8,620, NPV = -4,200 + 8,620 / 1.12 + 8,620 / 1.2544 + 8,620 / 1.404928 = -4,200 + 7,696 + 6,871 + 6,135 = about +16,502, a drop of about an eighth from option C's base +19,002. State your own benefit-versus-fixed-cost split and default formula here; a sensitivity row with no disclosed formula is not reproducible and should not ship.*

The adoption-row arithmetic follows the same shape: year 1 to 3 benefit scales with the eligible farmers reached, and the build and run cost do not. At 70 percent adoption, option C's three benefit lines total 15,260 a year across 5,600 farmers, KES 2,725 a farmer (the ratio is in KES, not KES thousands: 15,260 thousand / 5,600 = about KES 2,725 a farmer). At the pessimistic 40 percent adoption, 3,200 farmers x 2.725 = 8,720 a year; net is 8,720 - 5,600 run cost = 3,120 a year. Cumulative net is -4,200, -1,080, +2,040 and +5,160, so payback slips to year 2. NPV = -4,200 + 3,120 / 1.12 + 3,120 / 1.2544 + 3,120 / 1.404928 = -4,200 + 2,786 + 2,487 + 2,221 = about +3,294, which is about +7,494 on the three-year flow before the -4,200 Year 0. Halving the cooperative count under option B reduces both benefit and run cost, but the base case for section 4 remains option C at 70 percent adoption, and the sensitivity shows what a 40 percent start does to it.

**The case survives when:** at least three of the four districts come in at normal rain and at least 60 percent of the eligible farmers in each take the offer in year 1. If fewer than 60 percent take it, or if any one district has a below-normal season in year 1, the case recommends two districts with a staged year-2 extension rather than four.

## 6. Recommendation

- **Option:** Option E, two districts rather than four, because the below-normal-rain sensitivity is the domain's defining risk and a single bad district at four-district scale eats about an eighth of the NPV while leaving the team no cash discipline margin for the next season, and two districts let the pilot's weather-adjusted claim be tested on a second rainfall regime before the programme commits four cooperatives.
- **What we give up:** Option C's NPV of about KES 19,002 thousand less option E's two-district NPV of about KES 8,201 thousand, roughly KES 10,801 thousand, or about 57 percent of option C's NPV, and the faster learning that four districts would give on which cooperative drives adoption best. The "about an eighth" language above belongs to the rain-sensitivity row only, where the below-normal-rain scenario drops option C's NPV by about 2,500 of 19,002; the option E versus C gap is a much larger give-up, and the team holds option E because the rain risk is not yet priced into a four-district commitment. Option E is the pilot district plus one new district, Kakamega County, chosen for a wetter long-rains profile than Nakuru so the two districts give the programme two rainfall regimes to learn from.
- **Door type:** two-way, per the decision doors worksheet, so the evidence bar is ordinary. The money is a season of input credit, not a multi-year capital commitment, and stopping after one season leaves the county cooperatives with a working paper process rather than a stranded asset.
- **Conditions:** (1) the 2027 long-rains season input purchase is confirmed with the two cooperatives by 2026-12-15, owner Wanjiru Kamau; (2) the licensed input supplier's seed and fertiliser lots are confirmed registered for use in Kenya: seed through KEPHIS, the Kenya Plant Health Inspectorate Service, under the Seeds and Plant Varieties Act, Cap. 326, and fertiliser under Kenya's own input-approval regime. Note that EU Regulation (EC) No 1107/2009 covers plant protection products (pesticides), not seed or fertiliser, so the seed and fertiliser approvals above are governed by the separate Kenyan regimes named, not by 1107/2009. VERIFY with counsel that Cap. 326 is the current citation, as it is the pre-revision chapter number and may have been renumbered in Kenya's 2022 revised edition of the Laws of Kenya. Owner Elif Demirci, confirmed with counsel, not legal advice, as of 2026-09-11; (3) the mobile-money rail terms under the telco's mobile-money scheme are confirmed to hold for the 2027 season, owner Daniel Otieno, by 2026-11-30.
- **What would reverse this:** a below-normal long-rains forecast for Kakamega County, or a default rate above 12 percent in the first two months after harvest, watched by Elif Demirci each season, reverses the extension and holds the programme at the pilot district, with no second district.
- **The ask:** KES 3,400 thousand build and KES 2,800 thousand season cost for two districts, per option E in section 3, two field agronomists (one per district), and the roadmap slot for the 2027 long-rains season, stated once in [templates/planning/roadmap.md](../templates/planning/roadmap.md).

---

## How this case fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Benefits without cost to deliver | A yield uplift line and no agronomist, input or collections cost beneath it | Each benefit carries the cost of producing it |
| Nobody agreed the assumed assumptions | A yield gap or a default rate taken from a spreadsheet default | The model rests on data, which the finance partner and field agronomists agree before the model runs |
| Doing nothing is never costed | The inaction figure stated as zero | The pilot district's KES 8,400 thousand a season is the option A row, and options B, C, D and E are measured against it |
| Benefits with no owner | "Adoption will grow", with no name against it | Every benefit names Wanjiru Kamau or Elif Demirci and the metric it lands in |
| A good season credited to the product | The pilot's +34% quoted as the product's own result | The control-group adjustment is in the yield row and section 5's first row |
| False precision | An NPV to the nearest thousand on a high-uncertainty assumption such as the yield gap | Round to the confidence held, and state the range in section 5 |

## Exit gate (feeds Gate 1: problem worth solving)

- [x] Do nothing is a row with a cost, not a zero. Option A carries KES 8,400 thousand a season, the pilot district's own contribution to the input-credit gap.
- [x] Every benefit line names a method the finance partner has read. The yield rows name the 0.13 weather-adjusted gap and its control baseline; the repayment-margin rows name the per-farmer net margin; the cost-saved rows name the per-farmer distress-sale discount.
- [x] Build cost comes from a range, and the range appears in section 5. Section 3 carries the estimator's likely 4,200; section 5 runs the top of the range, 5,600.
- [x] Payback or NPV is computed on stated inputs, labeled ILLUSTRATIVE until the method is agreed. Section 4 computes all four modelled options (B, C, D and E), and option A, on the page, at a 12 percent rate.
- [x] At least one sensitivity flips the recommendation, or the document says why none does. The build-cost row would flip the recommendation only if Year 0 cost were above 28,980; no single row here does, and the document says why: the two-district recommendation is already the cautious option and the only row that flips it is a sub-60-percent adoption, which it watched as the case-survives condition, not the modelled option C.
- [x] The ILLUSTRATIVE example row has been deleted, so every row left is this initiative's own.
- [x] The recommendation names what it gives up, its door type, and its reversal trigger. Section 6 gives up option C's higher NPV, names the door two-way, and names the below-normal forecast or 12 percent default as the reversal trigger, watched by Elif Demirci.
- [x] Every input in sections 3 and 5 has a row in the assumptions table in section 1 (AS-01 to AS-18), each with a value and a confidence; the 12 percent rate and the repayment timing are named where they are used in sections 3 to 5. A formal filing of the same rows into [assumptions-register.md](../templates/definition/assumptions-register.md) is a Gate 2 follow-up, owner Elif Demirci.
- [ ] The BRD's financial case copies the option's numbers rather than recomputing them. This becomes a ticked action when the BRD is written; the two-district numbers in section 6 are the ones the BRD will carry.
- [ ] Signed by Wanjiru Kamau, 2026-09-11. Elif Demirci's signature is pending her final pass on the assumptions register.

---

## Exit-gate walk, signed

I have walked every box above and the evidence behind each one.

Boxes 1 through 4 rest on the pilot district's own figures: the KES 8,400 thousand inaction cost, the 0.13 weather-adjusted yield gap stated locally as an illustrative assumption for this case (not drawn from any supplied data sheet), the estimator's 4,200 likely and 5,600 top-of-range build cost, and the on-page NPVs at a 12 percent rate. Box 5 is not the build-cost row for flip: the only row that flips the recommendation is a sub-60-percent year-one adoption, and that row is stated as the case-survives condition, not counted as a sensitivity row. Boxes 6 and 7 are clean. Box 8 is clean because the assumptions table in section 1 carries a value and a confidence next to every row (AS-01 to AS-18); filing those rows into the formal [assumptions-register.md](../templates/definition/assumptions-register.md) is still pending Elif Demirci's final pass on the repayment-timing derivation, AS-12 and AS-16, and is tracked as a Gate 2 follow-up, not a Gate 1 blocker. Box 9 is marked open because the BRD is not written; it will be a fact for the BRD writer to carry when the BRD is. Box 10 is signed only by Wanjiru Kamau; Elif Demirci is named as the second signature on the assumptions register pass, dated 2026-09-11, and her signature is pending.

The headline claim this case turns on is the 0.13 gap, and it is a locally stated illustrative assumption, given its own row in the assumptions table rather than cited to any external source: only the difference against a same-season, same-district control group is defensible, the pilot customer saw +34% against prior-season self-report, and the control group of 40 non-pilot farms in the same district, tracked by the same agronomist, saw +21% over the same period with no product access, so only the 13 percentage points between them are credited to Maizeline here. The two named evidence holders for that claim are Elif Demirci and the pilot district's cooperative chair, and both have confirmed the arithmetic to me: they are the ones to ask if the gap is ever challenged.

Signed: Wanjiru Kamau, head of product, Maizeline, 2026-09-11. Elif Demirci, finance lead, named as the second signature on the assumptions register pass, 2026-09-11.
