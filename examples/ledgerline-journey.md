# Journey: Pricing and Selling the Expense Copilot at Ledgerline

Fills no template. It is the index and data sheet for the thirteen documents in the artifact map below, each of which fills one template on the PLANNING or OPERATE track. Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional product used across this repository, and the people, customers, vendor, prices, conversion rates and dates are fiction built so that thirteen documents can share one set of facts and be checked against each other. No figure is a benchmark, a target to copy, or a claim about what any real add-on converts at or costs to serve. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-12-22 · **Status:** Journey closed at a PIVOT on packaging, next experiment queued · **Sector cards:** [B2B SaaS](../knowledge/domains/saas-b2b.md) and [AI products](../knowledge/domains/ai-products.md) · **Seeds this journey reconciles with:** the [discovery document](expense-copilot-discovery.md), the [PRD](expense-copilot-prd.md), the [business case](ledgerline-business-case.md), the [strategy kernel](ledgerline-strategy-kernel.md), the [RICE sheet](ledgerline-rice-scoring.md), the [Kano survey](ledgerline-kano-survey.md) and the [north star tree](ledgerline-north-star-tree.md)

## The journey in one page

### The setting

Ledgerline is a fictional software company of about 900 people that sells the Ledgerline platform, invoicing, bills and expenses for small and mid-sized businesses, on three plans: Starter, Business and Enterprise. In the summer of 2026 its own finance team built the Expense Copilot for Ledgerline's own filers: discovery closed with a GO on 2026-08-14, the PRD passed Gate 2 on 2026-08-28, and the business case funded v1 on internal time savings alone. The earlier examples end there. This journey starts on 2026-10-12, the Monday the copilot went live for Ledgerline's 900 employees, and follows what happened when the company asked whether the thing it had built for itself could be sold to the 6,400 customer accounts on the Business plan, whose finance reviewers bounce reports for the same reasons Ledgerline's did.

The two sector cards frame the two halves of the problem. [B2B SaaS](../knowledge/domains/saas-b2b.md) says the user, the buyer and the blocker are three people, that expansion should be a packaging decision rather than an accident, and that pipeline blocked on a security review is a tax nobody logs unless the PM asks. [AI products](../knowledge/domains/ai-products.md) says wrong answers and model calls are cost of goods sold, so the price has to carry a per-receipt cost that the internal business case only had to absorb. Both cards are visible in what follows: the margin argument that rejected the free bundle came from the second card, and the customer DPA that blocked two Enterprise deals came from the first.

### The people

Three names carry over from the PRD and discovery examples, which the [examples index](README.md) already identifies as the same people the Ledgerline sheets call by role. Maya Chen is the product manager and owns most of the documents. Priya Nair leads engineering and owns billing integration and the extraction guardrail. Daniel Okafor is the finance lead who sponsored the internal build and who, in this journey, supplies the margin rule. New to this journey: Isabel Ferreira, chief product officer, the one person who can approve a price; Tomas Lindqvist, head of product marketing, who owns positioning and the sales one-pager; Ruth Adeyemi, VP sales, who holds the discount authority; Kwame Boateng, the data analyst who sized the experiment and built the dashboard; Hana Sato, head of customer success, who runs the advisory board and interviews the buyers in the win-loss reviews; and Marcus Webb, the mid-market account executive who read the one-pager and fed it its objections. The legal lead and the billing lead appear by role. Every customer, and the seat-priced receipt-capture vendor called Cinderwick, is invented.

### The stages, with dates

**OPERATE, internal product (2026-10-12 to 2026-11-09).** The copilot ran for four weeks on Ledgerline's own reports. At the first metrics review on 2026-11-09, 38% of eligible reports had gone through the draft flow and 74% of drafted reports were approved first time, against a 62% baseline. Gate 6 returned PERSIST (D4), which retired the business case's adoption kill line and became the entry condition for anything customer-facing.

**DISCOVER, commercial pass (2026-10-15 to 2026-10-28).** The trigger was written down on 2026-10-15: the Q3 win-loss batch showed 9 of 31 lost Business-plan deals naming receipt capture as the primary reason, and 7 of those had chosen Cinderwick. Isabel Ferreira recorded D1: run a second pass of the loop for an add-on, reusing the internal evidence only where a written reason says it transfers. Maya and Tomas interviewed six customer finance leads, and Kwame pulled the platform data: 2,900 Business accounts active in Expenses, median first-submission approval of 66%, and 1,240 accounts with approval under 75% and five or more filers, which became the best-fit segment.

**PLANNING (2026-10-30 to 2026-11-05).** Positioning was signed on 2026-10-30, pricing and packaging on 2026-11-03, the OKR sheet the same day, the metrics dictionary on 2026-11-04, and the experiment brief on 2026-11-05. The pricing document recorded two decisions that this journey turns on: D2 rejected bundling the copilot free into the Business plan, and D3 set a per-seat price of $6 per plan seat per month and accepted, in writing, that seats do not rhyme with the north star.

**DELIVER (2026-11-06 to 2026-11-22).** The GTM plan, the sales enablement one-pager and the dashboard were signed on 2026-11-06 with the add-on's Gate 5, held on the internal PERSIST. Phase 1 put six design partners live on 2026-11-10; four of six met the exit condition by 2026-11-23, with 54% of eligible reports drafted and 77% approved first time. The advisory board was chartered on 2026-11-10. The status report for the week of 2026-11-30 sits inside this stretch and is AMBER overall, with one RED: the customer DPA did not cover the model subprocessor, and two Enterprise deals waited on it until D5 on 2026-12-03.

**OPERATE, add-on (2026-11-23 to 2026-12-22).** Phase 2 was the pricing experiment: the per-seat offer, plain or anchored against the reviewer's hourly cost, shown to 2,748 accounts between 2026-11-23 and 2026-12-04. The advisory board met on 2026-12-02 and six of eight members said seat pricing penalises accounts with few filers. Hana Sato ran six win-loss interviews between 2026-12-07 and 2026-12-16. On 2026-12-18 the experiment's own rule killed the price. The metrics review on 2026-12-21 returned PIVOT on packaging (D6), the OKRs were scored the same day, and the growth plan of 2026-12-22 queued the usage-based re-offer as the next bet (D7).

### The rejected option: free in the base plan

Bundling the copilot into the Business plan at no charge was argued twice, by sales in the positioning session and by a design partner at the pricing review, on the grounds that it would win the Cinderwick deals outright. It lost in both documents on margin. Every drafted report costs about $0.92 in model calls at the quoted rate, and a free bundle across the 2,900 active accounts at the business case's own 60% adoption assumption is about 965,000 receipts a year, roughly $212,000 of model cost with no revenue line beside it, about 1.9 points of Business-plan gross margin at the quote and 3.1 points if adoption reaches everyone. Daniel Okafor's rule, recorded at D2, is that no feature costing more than one point of gross margin ships without its own revenue line. The positioning document adds the second reason: a free feature cannot be positioned against a vendor charging $8 a seat, because it announces that the value is zero. A ten-report free allowance was also rejected, because the accounts that most need the product are exactly the accounts that would exhaust it.

### The failed hypothesis and what it cost

The team believed that a per-seat price, anchored on the offer page against the reviewer's hourly cost, would convert at least 6.0% of exposed accounts within 14 days. The brief predeclared the rule on 2026-11-05: ship at 6.0% or better in the anchored arm, iterate between 4.0% and 6.0%, kill below 4.0% in both arms. The anchored arm converted 2.9% and the plain arm 2.4%, a difference inside the noise. The metrics review put the cause on the page: the anchor was Ledgerline's own reviewer cost, 30 hours a month at a 900-person company, shown to buyers whose reviewer is one person on Friday afternoons; and $6 across a median of 34 seats is $204 a month for an add-on to a $149 plan. Four of six win-loss interviews said one or both of those things unprompted, and the advisory board had said it three weeks earlier. The value metric was wrong, and the pricing document had said so on 2026-11-03 and accepted it because billing meters seats.

What it cost, all ILLUSTRATIVE: 1.5 person-months of seat-metering work, about $15,000, that the usage model does not reuse, plus 1 person-month for the usage meter it needs instead; six weeks of the launch cycle between D3 and D6; two Enterprise quotes withdrawn; the phase 3 rollout held; a one-pager reprinted; a KR1 result of 79 active accounts against a target of 180; and 73 paying accounts holding a seat price for twelve months that the company no longer believes in. The growth plan pivots to $2.40 per drafted report, no seat charge, and sets the same 6.0% bar for the re-offer, on purpose, so that the pivot has to clear the line the first price could not.

## Data sheet (ILLUSTRATIVE)

Every number any of the thirteen artifacts uses is here, with its unit, its source inside the fiction, and its firmness (measured, estimate, target, assumption, quoted, derived, decided or date). All of it is ILLUSTRATIVE and invented. An artifact that needs a number not on this sheet is wrong, or this sheet is; either way the sheet is corrected first and the artifact second. Rows N1 to N15 are carried unchanged from the earlier Ledgerline examples, and any figure derived from them shows the arithmetic.

### Numbers

| # | Name | Value, with unit | Source inside the fiction | Firmness |
|---|---|---|---|---|
| N1 | Ledgerline headcount | about 900 employees | [discovery document](expense-copilot-discovery.md) | measured |
| N2 | Internal expense reports | 9,600 a year; 2,400 a quarter; about 800 a month | finance system, quarter ending 2026-06-30, via the [business case](ledgerline-business-case.md) | measured |
| N3 | Internal first-submission approval, baseline | 62% of reports | finance system, via the [PRD](expense-copilot-prd.md) | measured |
| N4 | Internal approval target on drafted reports | 80% | PRD objective 1 | target |
| N5 | Median filing time, five-receipt report | 25 minutes baseline; under 10 minutes target | discovery timed sessions, n=8; PRD objective 2 | directional; target |
| N6 | Loaded hourly rates | $55 an hour filer; $60 an hour reviewer | finance planning rates, carried as an Open item in the business case | assumption |
| N7 | Reviewer mechanical checks, internal | 30 hours a month across three reviewers; $1,800 a month at $60 | business case | estimate |
| N8 | Internal run cost | $2,500 a month, of which model API $733, hosting $1,100, on-call share $667 | business case total (quoted); the three-way split is this journey's decomposition | quoted; split is an estimate |
| N9 | Model API price | $0.22 per receipt, quoted at about 40,000 receipts a year | business case Open item; procurement owns the contracted price (DEP2) | quoted, not contracted |
| N10 | Receipts per report | 4.2 receipts | 40,000 receipts over 9,600 reports | derived estimate |
| N11 | Model cost per drafted report at the quoted rate | $0.92 | N9 x N10 = 4.2 x $0.22 | derived estimate |
| N12 | Engineering cost rate | $10,000 per person-month | business case build-effort line | estimate |
| N13 | Seat-priced receipt-capture vendor, called Cinderwick (invented) | $8 per seat per month, quoted 2026-08-13 for 900 seats | business case option 3 | quoted |
| N14 | Cost of a bounce | 30 minutes across filer and reviewer | business case inputs | estimate |
| N15 | Filing time saved per drafted report | 15 minutes, about $13.75 at $55 an hour | business case arithmetic, line 1 | target, not evidence |
| N16 | Internal Gate 5 | signed 2026-10-09 per function; live 2026-10-12 | internal release readiness doc | date |
| N17 | Internal metrics review 1 | window 2026-10-12 to 2026-11-08; reviewed 2026-11-09 | internal metrics review | date |
| N18 | Internal eligible reports in the window | 740 reports | product analytics | measured |
| N19 | Internal drafted share | 281 of 740 = 38%; target 50% by month two; kill line 30% | product analytics; PRD objective 3; business case kill condition | measured; target |
| N20 | Internal approval on drafted reports | 208 of 281 = 74% | finance approval events joined to draft ids (the join shipped with Gate 5 on 2026-10-09) | measured |
| N21 | Internal extracted fields accepted without edit | 86% of fields | product analytics | measured |
| N22 | Internal suggested category kept | 81% of suggestions | product analytics | measured |
| N23 | Internal median minutes, first receipt to submit | 12 minutes | in-product timing | measured |
| N24 | Internal reviewer-caught extraction errors | 2.1 per 100 drafted reports | reviewer flag button | measured |
| N25 | Internal Gate 6 decision | PERSIST (D4), 2026-11-09 | internal metrics review | decided |
| N26 | Business-plan accounts | 6,400 accounts | billing system, 2026-09-30 | measured |
| N27 | Business plan price | $149 per account per month | price list dated 2026-01-05 | measured |
| N28 | Business-plan gross margin | 78% | finance planning | estimate |
| N29 | Business-plan ARR | about $11.4M = 6,400 x $149 x 12 | derived from N26 and N27 | estimate |
| N30 | Starter accounts | 21,000 accounts, no reviewer workflow, out of scope | billing system | measured |
| N31 | Enterprise accounts | 310 accounts, sales-led, outside EXP-1 | billing system | measured |
| N32 | Business accounts active in Expenses (segment S-1) | 2,900 accounts with 10 or more reports in Q3 | platform data pull, EV-C07 | measured |
| N33 | Reports filed by S-1 in Q3 | 96,000 reports; mean 33 per account per quarter (11 a month); median 21 per quarter (7 a month) | EV-C07 | measured |
| N34 | Seats and filers per S-1 account | median 34 plan seats; median 11 filers | EV-C07 | measured |
| N35 | Customer approval baseline | 66% median first-submission approval across S-1, all reports | EV-C07 | measured |
| N36 | Best-fit segment (S-5) | 1,240 accounts with approval under 75% and 5 or more filers | EV-C07 | measured |
| N37 | Q3 lost Business-plan deals | 31 lost; 9 named receipt capture as the primary reason; 7 of the 9 chose Cinderwick | sales ops win-loss batch, EV-C08 | measured, rep-sourced |
| N38 | Customer support tickets on Expenses, Q3 | 610 tagged category or receipt | support system, EV-C09 | measured |
| N39 | Prior add-on conversion (Bills Automation, launched 2026-03-02) | 4.1% of exposed accounts paid within 14 days | billing data | measured |
| N40 | Design-partner interviews | 6 finance leads, 2026-10-19 to 2026-10-28; 6 of 6 named bounces; 4 of 6 keep a spreadsheet; 2 had trialled Cinderwick; 5 of 6 would pay "something"; 0 of 6 were asked a price | EV-C01 to EV-C06 | measured (interview counts) |
| N41 | Design partners (all invented) | Bramblewood Freight (48 seats, 31 filers); Tessellate Consulting (60, 44); Marlowe Field Services (40, 26); Corrigan and Vale (30, 18); Oakhurst Dental Partners (22, 6); Wrenfield Labs (28, 12); 228 seats in total | pilot agreements | measured |
| N42 | Design-partner terms | 25% off list for 12 months; approver Isabel Ferreira; offer expires 2026-12-31 for new partners | pricing doc section 5 | decided |
| N43 | Phase 1 window | 2026-11-10 to 2026-11-22 | GTM plan | date |
| N44 | Phase 1 results | 412 eligible reports; 224 drafted (54%); 173 approved first time (77%); partners' own Q3 baseline 64% | product analytics; platform approval events | measured |
| N45 | Phase 1 exit | 4 of 6 partners met the condition on 2026-11-23; Oakhurst not evaluable on 11 reports; Wrenfield at 61% approval on 33 drafted reports, mostly German-language receipts (R3) | GTM plan phase table | measured |
| N46 | Per-seat add-on price (D3) | $6 per plan seat per month; 25% under Cinderwick | pricing doc section 3 | decided |
| N47 | Per-seat price for the median account | 34 x $6 = $204 a month, against a $149 plan | derived from N34, N46, N27 | derived |
| N48 | Discount rules | annual prepay 15%, approver Ruth Adeyemi; design partners 25% for 12 months, approver Isabel Ferreira; anything else needs Isabel Ferreira and a decision-log entry; contracted prices hold for 12 months | pricing doc section 5 | decided |
| N49 | Margin floor for the add-on | 60% gross margin on the model line | finance planning floor, Daniel Okafor | assumption |
| N50 | Margin rule for bundled features | no feature costing more than one point of Business-plan gross margin ships without its own revenue line | Daniel Okafor, recorded at D2 | decided |
| N51 | Free-bundle model cost at 60% drafted share | 2,900 x 11 x 12 = 382,800 reports a year; 229,680 drafted; x 4.2 = about 965,000 receipts; x $0.22 = about $212,000 a year; about 1.9 points of N29 | derived from N9, N10, N32, N33 | estimate |
| N52 | Free-bundle model cost at 100% drafted share | about 1,608,000 receipts; about $354,000 a year; about 3.1 points of N29 | derived | estimate |
| N53 | Free-bundle model cost at an assumed re-quote | $0.14 per receipt gives about $135,000 a year at 60%; about 1.2 points of N29 | assumption; the re-quote is DEP2 | assumption |
| N54 | EXP-1 population and arms | S-1, 2,900 accounts, split 1,450 per arm by account id; control is the plain per-seat offer; anchored is the per-seat offer with the N7 reviewer-cost anchor | experiment brief | decided |
| N55 | EXP-1 sizing | baseline 4.1% (N39); minimum detectable effect 2.5 points; two-sided 5%, 80% power; about 1,270 accounts per arm | Kwame Boateng, arithmetic in the brief | computed 2026-11-05 |
| N56 | EXP-1 dates | exposure 2026-11-23 to 2026-12-04; 14-day conversion window per account; analysis 2026-12-18 | experiment brief | date |
| N57 | EXP-1 decision rule | ship: anchored arm at 6.0% or better with guardrails intact; iterate: either arm between 4.0% and 6.0%; kill: both arms under 4.0%, or a guardrail breached | experiment brief section 5 | pre-declared 2026-11-05 |
| N58 | EXP-1 guardrails | M-006 at least 70% in converted accounts; M-008 under 3 per 100 drafted reports | experiment brief section 2 | pre-declared |
| N59 | EXP-1 exposure | 2,748 of 2,900 accounts; control 1,371; anchored 1,377 | product analytics exposure events | measured |
| N60 | EXP-1 funnel | 1,044 opened the offer (38% of exposed); 302 reached the price step (11%); 73 paid | product analytics | measured |
| N61 | EXP-1 result | control 33 of 1,371 = 2.4%; anchored 40 of 1,377 = 2.9%; pooled 73 of 2,748 = 2.7%; the 0.5-point difference sits inside a standard error of about 0.6 points | billing joined to exposure events | measured |
| N62 | EXP-1 outcome | KILL per N57, executed 2026-12-18 by Maya Chen; ratified as D6 on 2026-12-21 | experiment brief; metrics review | decided |
| N63 | Add-on review window | 2026-11-23 to 2026-12-18 | metrics review | date |
| N64 | Active add-on accounts (M-002) at 2026-12-18 | 79 = 73 paid + 6 design partners | billing | measured |
| N65 | Reports in active add-on accounts, window | 1,180 eligible; 555 drafted (47%, M-003); 422 approved first time (76%, M-006); north star M-001 = 422; companion M-012 = 422 / 1,180 = 36% | product analytics joined to platform approval events | measured |
| N66 | M-004 and M-005, window | 87% of extracted fields accepted without edit; 82% of suggested categories kept | product analytics | measured |
| N67 | M-008, M-009, M-010, window | 2.4 errors per 100 drafted reports; $0.93 model cost per drafted report; 5.1 support tickets per 100 add-on accounts per week | reviewer flags; vendor invoice over drafted count; support system | measured |
| N68 | Add-on MRR (M-011) at 2026-12-18 | $15,900 = 73 paid accounts, 2,480 seats x $6 = $14,880, plus 6 partners, 228 seats x $6 x 0.75 = $1,026 | billing | measured |
| N69 | OKR cycle | 2026-11-02 to 2026-12-31; scored 2026-12-21 on data to 2026-12-18, as agreed at planning on 2026-11-03 | OKR sheet | date |
| N70 | KR1, accounts with the add-on active | baseline 0; target 180; actual 79; score 0.44; aspirational | OKR sheet | target; measured |
| N71 | KR2, first-submission approval on drafted reports, customer accounts | baseline 66% (N35); target 78%; actual 76%; score 0.83; committed | OKR sheet | target; measured |
| N72 | KR3, share of eligible reports drafted in active accounts | baseline 0; target 50%; actual 47%; score 0.94; committed | OKR sheet | target; measured |
| N73 | KR4, add-on MRR | baseline $0; target $30,000; actual $15,900; score 0.53; aspirational | OKR sheet | target; measured |
| N74 | Guardrail floors and ceilings | M-008 under 3; M-009 at most $1.05; M-006 at least 70%; M-010 at most 8 per week; discounts outside N48: 0 (actual 0) | OKR sheet and metrics dictionary | agreed 2026-11-03 |
| N75 | OKR check-ins | 2026-11-16, 2026-11-30, 2026-12-14 | calendar | date |
| N76 | Win-loss batch | 6 buyer interviews 2026-12-07 to 2026-12-16 by Hana Sato: WL-01 Redfern Heating and Air, NO DECISION (48 seats, 9 filers); WL-02 Larkspur Media, WON (26, 19); WL-03 Penrose Surveying, WON (40, 30); WL-04 Hollowell Clinics, NO DECISION (72, 8); WL-05 Dunmore Logistics, NO DECISION (55, 35); WL-06 Ashgrove Property Management, LOST to Cinderwick (38, 14) | win-loss review | measured |
| N77 | Win-loss pattern | 4 of 6 named seats billed for people who never file, or an add-on priced above the plan; both wins had filers at 70% or more of seats | win-loss review section 4 | measured |
| N78 | Advisory board | 9 seats; session 1 on 2026-12-02 with 8 present; 6 of 8 said seat pricing penalises accounts with few filers; 5 of 8 asked for a per-report price | EV-AB01 | measured |
| N79 | Enterprise prospects blocked on the DPA | 2 (Halvard Marine, Ostrander Group, invented); about 400 seats each; about $2,400 MRR each at N46 | sales pipeline | estimate |
| N80 | Status report | week of 2026-11-30; overall AMBER, previous week GREEN | status report | date |
| N81 | EXP-1 exposure by 2026-11-29 | 1,885 of 2,900 accounts | product analytics | measured |
| N82 | Legacy annual-invoice accounts (R2) | 214 Business accounts cannot be charged mid-term; 3 activated through manual invoice lines in the window (G-1) | billing | measured |
| N83 | German-language receipt eval set (DEP5) | 300 labeled receipts; scored 2026-12-11; field accuracy 71% against the 90% eval threshold | eval run | measured |
| N84 | Account executives briefed | 14 account executives on 2026-11-05 | sign-off list | measured |
| N85 | Slip on the phase 1 start | 1 day: baseline 2026-11-09, actual 2026-11-10, because the internal review ran on the 9th; accepted by Maya Chen | status report milestones | measured |
| N86 | Seat-metering engineering (DEP1, ADR-007) | 1.5 person-months, $15,000 at N12; not reused by the usage model | engineering lead | estimate |
| N87 | Usage meter (DEP4, ADR-008) | 1 person-month, $10,000 at N12; needed by 2027-01-08 | engineering lead | estimate |
| N88 | Calendar cost of the failed price | 6 weeks from D3 (2026-11-03) to D6 (2026-12-21); phase 3 held; 2 Enterprise quotes withdrawn | decision log | measured |
| N89 | Usage price proposed (EXP-2, D7) | $2.40 per drafted report, billed monthly in arrears, no seat charge, no minimum; margin at N11 cost is ($2.40 minus $0.92) / $2.40 = about 62%, above the N49 floor | growth plan | proposed |
| N90 | Usage price for the median account | 11 x $2.40 = about $26 a month, about 18% of the plan price | derived from N33 and N89 | derived |
| N91 | EXP-2 design | re-offer to the 2,827 S-1 accounts not paying (2,675 exposed non-converters plus 152 never exposed); single arm; success at 6.0% or more activated within 14 days of exposure; planned exposure from 2027-01-11 once DEP4 lands | growth plan section 4 | pre-declared 2026-12-22 |
| N92 | EXP-2 counter-metrics and kill | M-009 at most $1.05; M-006 at least 70%; M-010 at most 8 per week; kill under 4.0% at the analysis date or on 2027-02-12, whichever comes first; decider Maya Chen | growth plan sections 5 and 6 | pre-declared 2026-12-22 |
| N93 | Price hold for the 73 paid accounts | 12 months at $6 per seat, then migration to the usage price; per N48 | pricing doc | decided |
| N94 | Offer-page alternate wording | "Copilot pricing is under review; existing activations are unchanged", drafted 2026-11-06, switched on 2026-12-21 | GTM plan section 5 | decided |

### Shared identifiers

Every id below is used by more than one artifact and is spelled the same way everywhere. An artifact that needs a new id adds it here first.

**People (P), all fictional.** P1 Maya Chen, product manager, Expense Copilot. P2 Priya Nair, engineering lead. P3 Daniel Okafor, finance lead and internal sponsor. P4 Isabel Ferreira, chief product officer and pricing owner. P5 Tomas Lindqvist, head of product marketing. P6 Ruth Adeyemi, VP sales. P7 Kwame Boateng, data analyst. P8 Hana Sato, head of customer success. P9 Marcus Webb, account executive, mid-market. By role only: the legal lead, the billing lead, the finance admin, the sales engineer who resets the demo environment.

**Stories (LEDGERLINE-S).** These are the add-on's stories, numbered after the internal PRD's five user stories, which they extend rather than replace.

| Id | Story | Status at 2026-12-22 |
|---|---|---|
| LEDGERLINE-S1 | As an account admin, I can activate the copilot add-on from the Expenses settings page and see the charge before I confirm it | shipped 2026-11-19 (DEP1); charge line to change with the pivot |
| LEDGERLINE-S2 | As a filer at a customer account, I photograph or forward a receipt and get a drafted line item with the matched policy line from my own company's policy | shipped 2026-11-10 |
| LEDGERLINE-S3 | As a finance reviewer at a customer account, drafted fields arrive flagged with the model's confidence so I spend judgment where it is needed | shipped 2026-11-10 |
| LEDGERLINE-S4 | As an account admin, I can see how many seats will be billed and which users filed a report last quarter, before I activate | proposed 2026-12-17 from WL-01 and WL-04; superseded by S6 if the usage price ships |
| LEDGERLINE-S5 | As an account admin, I can see my account's first-submission approval rate before and after activation | shipped 2026-11-13 with the dashboard's customer-facing tile |
| LEDGERLINE-S6 | As an account admin, I am billed per drafted report in arrears and can see the running count and the month's cost so far | proposed 2026-12-22 (D7, DEP4, ADR-008) |

**Risks (R).**

| Id | Risk | Owner | Opened | Status at 2026-12-22 |
|---|---|---|---|---|
| R1 | Internal adoption falls under the 30% kill line by month two, and the business case does not pay back | P1 Maya Chen | 2026-08-13 (business case) | retired 2026-11-09 at 38% (N19) |
| R2 | Seat metering cannot bill the 214 legacy annual-invoice accounts mid-term | P2 Priya Nair with the billing lead | 2026-11-16 | mitigated 2026-12-04 by manual invoice lines; retired if S6 ships |
| R3 | Foreign-language receipts fail extraction; the RICE sheet's row 7 open item | P2 Priya Nair | 2026-09-01 (RICE) | realised at Wrenfield (N45); eval set scored 2026-12-11 (N83); open |
| R4 | The customer DPA does not name the model vendor as a subprocessor; Enterprise pipeline blocked | the legal lead | 2026-11-23 | closed by D5 on 2026-12-03 |
| R5 | The per-seat value metric mismatches the north star and the price fails to convert | P1 Maya Chen | 2026-11-03 (accepted at D3) | realised 2026-12-18 (N61); becomes the pivot |
| R6 | Model cost per drafted report exceeds the margin floor once volume moves off the 40,000-receipt quote | P3 Daniel Okafor with procurement | 2026-11-03 | open; DEP2 |

**Decisions (D).**

| Id | Decision | Decider | Date | Options that lost |
|---|---|---|---|---|
| D1 | Run a second pass of the loop for the add-on; reuse internal evidence only where a written reason says it transfers | P4 Isabel Ferreira | 2026-10-15 | "ship the internal build to customers as is, with a price"; "wait for two quarters of internal data" |
| D2 | Do not bundle the copilot free into the Business plan; it needs its own revenue line | P4 Isabel Ferreira, argued by P3 Daniel Okafor | 2026-10-30, reaffirmed 2026-11-03 | free bundle (N51 to N53 against N50); a ten-report free allowance |
| D3 | Value metric is plan seats at $6 per seat per month; north star mismatch accepted because billing meters seats and sales forecasts seats; reopens on the EXP-1 kill rule or a win-loss pattern naming seats | P4 Isabel Ferreira | 2026-11-03 | per drafted report (no meter existed, DEP4); per active filer (no definition agreed) |
| D4 | Internal Gate 6: PERSIST | P1 Maya Chen and P3 Daniel Okafor | 2026-11-09 | pivot, sunset, both argued and recorded |
| D5 | Accept the model vendor's standard subprocessor terms in the customer DPA, with 30-day prompt retention and the existing no-training clause | P4 Isabel Ferreira with the legal lead | 2026-12-03 | negotiate bespoke terms first (cost: both Enterprise deals slip past year end) |
| D6 | Kill the per-seat price per the EXP-1 rule; PIVOT packaging to a usage metric; hold phase 3; swap the offer page to N94; reopen the pricing doc; withdraw the one-pager's pricing section | P4 Isabel Ferreira, on the metrics review | 2026-12-21 | iterate the anchor copy (rejected: both arms were under the kill line); persist with discounts (rejected: N48 forbids it) |
| D7 | Next growth bet is EXP-2, the usage re-offer at $2.40 per drafted report, with the same 6.0% bar | P1 Maya Chen with P4 Isabel Ferreira | 2026-12-22 | a two-price test at $1.60 and $2.40 (rejected: $1.60 is under the N49 floor at the quoted cost) |

**Dependencies (DEP).**

| Id | Dependency | Owning team | Needed by | Status |
|---|---|---|---|---|
| DEP1 | Seat metering for add-ons in the billing system | billing | 2026-11-20 | delivered 2026-11-19 with the R2 gap |
| DEP2 | Model vendor volume re-quote at customer scale | procurement | 2026-12-11 | Open: procurement owns the date |
| DEP3 | Customer DPA subprocessor addendum | legal | 2026-11-06 | delivered 2026-12-03, late, via D5 |
| DEP4 | Usage meter: drafted reports counted per account and billed in arrears | billing with P2 Priya Nair | 2027-01-08 | open; blocks EXP-2 |
| DEP5 | Labeled German-language receipt eval set | P2 Priya Nair with Wrenfield Labs | 2026-12-11 | delivered 2026-12-11 (N83) |

**Architecture decision records.** ADR-001 to ADR-006 belong to the internal build and are not reproduced here. ADR-007 (2026-11-04): the add-on's entitlement and charge are computed from the billing system's seat count, not from a product-side counter. ADR-008 (proposed 2026-12-22): a product-side drafted-report meter, billed in arrears, supersedes ADR-007 for the add-on; ADR-007 is never edited.

**Metric ids (M), defined in the metrics dictionary and cited everywhere else.**

| Id | Metric | Type |
|---|---|---|
| M-001 | Copilot-drafted reports approved on first submission per month, across customer accounts | north star |
| M-002 | Accounts with the add-on active (paid or design partner) at week end | input, lead |
| M-003 | Share of eligible reports drafted, pooled across active add-on accounts | input, lead |
| M-004 | Extracted fields accepted without edit, share of fields | input, lead |
| M-005 | Suggested category kept by the filer, share of suggestions | input, lead |
| M-006 | First-submission approval rate on drafted reports, pooled across active add-on accounts | input, lag |
| M-007 | Offer-to-paid conversion within 14 days of first exposure, share of exposed accounts | diagnostic; EXP-1 and EXP-2 target |
| M-008 | Reviewer-caught extraction errors per 100 drafted reports | guardrail |
| M-009 | Model cost per drafted report, dollars | guardrail |
| M-010 | Support tickets per 100 add-on accounts per week | guardrail |
| M-011 | Add-on MRR, dollars | diagnostic; KR4 |
| M-012 | M-001 as a share of all eligible reports in active add-on accounts | companion to the north star |

**Segments (S).** S-1 Business accounts active in Expenses, 10 or more reports last quarter (N32). S-2 the six design partners (N41). S-3 EXP-1 control arm. S-4 EXP-1 anchored arm. S-5 best-fit accounts, approval under 75% and 5 or more filers (N36). S-6 Enterprise accounts (N31).

**Dictionary gaps (G).** G-1 legacy annual-invoice accounts emit no activation event until finance ops posts the manual line, so M-002 undercounts by up to 3 in the window (N82). G-2 accounts still on the pre-2026-06 classic approvals workflow send approval events without a draft id, so M-006 excludes them; about 11% of S-1. G-3 receipts in a language the extractor abstains on stay in M-004's denominator, so M-004 undercounts for accounts like Wrenfield.

**Evidence notes and reviews.** EV-C01 to EV-C06 the six design-partner interviews (N40). EV-C07 the platform data pull of 2026-10-22 (N32 to N36). EV-C08 the Q3 win-loss batch from sales ops (N37). EV-C09 the Q3 support ticket pull (N38). EV-AB01 advisory board session 1, 2026-12-02 (N78). WL-01 to WL-06 the win-loss reviews (N76). EXP-1 the per-seat pricing experiment (N54 to N62). EXP-2 the usage re-offer (N89 to N92).

**Customers, all invented.** Design partners: Bramblewood Freight, Tessellate Consulting, Marlowe Field Services, Corrigan and Vale, Oakhurst Dental Partners, Wrenfield Labs. Win-loss accounts: Redfern Heating and Air, Larkspur Media, Penrose Surveying, Hollowell Clinics, Dunmore Logistics, Ashgrove Property Management. Enterprise prospects: Halvard Marine, Ostrander Group. Demo environment company: Larchfield Logistics. Vendor: Cinderwick.

### Timeline

| Date | Event | Artifact that records it |
|---|---|---|
| 2026-07-20 to 2026-08-14 | Internal discovery; GO on 2026-08-14 | [discovery document](expense-copilot-discovery.md) |
| 2026-08-13 | Business case approved at Gate 1 | [business case](ledgerline-business-case.md) |
| 2026-08-28 | PRD approved at Gate 2 | [PRD](expense-copilot-prd.md) |
| 2026-09-01 | RICE sheet and north star tree | [RICE sheet](ledgerline-rice-scoring.md), [north star tree](ledgerline-north-star-tree.md) |
| 2026-10-09 | Internal Gate 5 signed per function; approval-to-draft join shipped | internal release readiness (not reproduced) |
| 2026-10-12 | Copilot live for Ledgerline's own filers | status report, section 4 baseline |
| 2026-10-15 | Commercial trigger recorded (N37, N38); D1 | positioning, section 1 evidence |
| 2026-10-19 to 2026-10-28 | Design-partner interviews EV-C01 to EV-C06; platform pull EV-C07 on 2026-10-22 | positioning, sales one-pager |
| 2026-10-30 | Positioning signed by Tomas Lindqvist; D2 first argued | positioning |
| 2026-11-03 | Pricing and packaging v1 signed by Isabel Ferreira; D2 reaffirmed, D3; R5 and R6 opened; OKR sheet signed | pricing and packaging, OKRs |
| 2026-11-04 | Metrics dictionary agreed; ADR-007 | metrics dictionary |
| 2026-11-05 | Experiment brief signed; sizing computed; 14 account executives briefed | experiment brief, sales one-pager |
| 2026-11-06 | GTM plan signed; sales one-pager approved; dashboard built; add-on Gate 5 signed with phase 1 held on the internal review | GTM plan, sales one-pager, dashboard spec |
| 2026-11-09 | Internal metrics review 1: PERSIST (D4); R1 retired | metrics review (referenced), OKRs |
| 2026-11-10 | Phase 1 live for six design partners (one-day slip, N85); advisory board chartered | GTM plan, feedback program, status report |
| 2026-11-13 | Dashboard verified; LEDGERLINE-S5 shipped | dashboard spec |
| 2026-11-16 | OKR check-in 1; R2 opened | OKRs, status report |
| 2026-11-19 | DEP1 delivered with the R2 gap; LEDGERLINE-S1 shipped | status report |
| 2026-11-23 | Phase 1 exit met (N45); phase 2 begins as EXP-1 exposure; R4 goes red | GTM plan, experiment brief, status report |
| 2026-11-30 | Status report, week of; OKR check-in 2; R4 escalated to Isabel Ferreira | status report, OKRs |
| 2026-12-02 | Advisory board session 1 (EV-AB01) | feedback program |
| 2026-12-03 | D5: DPA terms accepted; R4 closed | status report escalation row, decision log |
| 2026-12-04 | EXP-1 exposure period ends; R2 mitigated | experiment brief, status report |
| 2026-12-07 to 2026-12-16 | Win-loss interviews WL-01 to WL-06 | win-loss review |
| 2026-12-11 | DEP5 delivered; German-language eval set scored 71% (N83) | status report, win-loss action items |
| 2026-12-14 | OKR check-in 3 | OKRs |
| 2026-12-17 | Win-loss batch signed by Hana Sato; LEDGERLINE-S4 proposed | win-loss review |
| 2026-12-18 | EXP-1 analysis: KILL per rule, executed by Maya Chen | experiment brief |
| 2026-12-21 | Metrics review: PIVOT on packaging (D6); OKRs scored; offer page swapped (N94); one-pager pricing section withdrawn; pricing doc reopened | metrics review, OKRs, pricing and packaging, sales one-pager |
| 2026-12-22 | Growth plan signed; D7; ADR-008 proposed; this journey closed | growth plan |
| Scheduled | EXP-2 exposure from 2027-01-11 after DEP4 (2027-01-08); EXP-2 kill date 2027-02-12; next advisory board program review 2027-03-04 | growth plan, feedback program |

## Artifact map

Thirteen files, each filling one template with the same structure, header shape and exit gate as the earlier examples. The "stage and gate" column is the template's own. The last column is the brief each author works from: what the document decides, and which data-sheet rows and ids it must use and may not contradict.

| File | Template it fills | Stage and gate | What it decides, and which rows it uses |
|---|---|---|---|
| [ledgerline-positioning.md](ledgerline-positioning.md) | [templates/planning/positioning.md](../templates/planning/positioning.md) | PLANNING track, feeds the GTM plan | Decides that the copilot is positioned as an add-on to the finance platform the buyer already runs, for Business accounts whose reviewer bounces more than a quarter of reports, against typing into the Expenses form, a spreadsheet, and Cinderwick, and rejects the "free feature of the plan" frame first on the D2 margin grounds. Uses N13, N32 to N38, N40, N41, N44, N47, N51, the segment S-5, EV-C01 to EV-C09, D1 and D2, and the sector card's user, buyer and blocker; signed by Tomas Lindqvist on 2026-10-30. |
| [ledgerline-pricing-packaging.md](ledgerline-pricing-packaging.md) | [templates/planning/pricing-packaging.md](../templates/planning/pricing-packaging.md) | PLANNING track, feeds Gate 5 readiness | Records D3 as signed on 2026-11-03: plan seats as the value metric at $6 per seat per month, the north star mismatch accepted in writing with the condition that reopens it, the free bundle rejected with the N50 to N53 arithmetic, and discount rules written before the first negotiation. Uses N9 to N13, N26 to N29, N32 to N36, N46 to N53, N93, R5, R6, D2, D3, DEP2, DEP4 and the [good-better-best sheet](../frameworks/pricing/packaging-good-better-best.md); its status line records that D6 reopened section 1 on 2026-12-21, and its willingness-to-pay row is honest that no buyer was asked a price (N40). |
| [ledgerline-growth-plan.md](ledgerline-growth-plan.md) | [templates/planning/growth-plan.md](../templates/planning/growth-plan.md) | OPERATE, feeds Gate 6 | Decides the one bet after the pivot: M-002, active add-on accounts, moved by EXP-2, the usage re-offer at $2.40 per drafted report, with the funnel leak located at the price step, the same 6.0% bar the seat price failed, and counter-metrics and a kill condition written before it starts. Uses N60, N61, N64 to N68, N87, N89 to N92, the M ids, S-1, D6, D7, DEP4, ADR-008 and LEDGERLINE-S6; its ledger carries EXP-1 as a KILL row; signed by Maya Chen on 2026-12-22. |
| [ledgerline-gtm-plan.md](ledgerline-gtm-plan.md) | [templates/planning/gtm-plan.md](../templates/planning/gtm-plan.md) | DELIVER, feeds Gate 5 | Decides that the beachhead is the six named design partners, that phase 2 is EXP-1 itself and phase 3 waits on its result, and that the one launch metric is M-002 with a stop condition tied to M-008 and the rehearsed offer-page swap. Uses N39, N41 to N46, N54, N56, N59, N70, N94, S-2, S-1, D4, R3, R4 and LEDGERLINE-S1 to S3; phase 3 is shown as never entered; signed by Maya Chen on 2026-11-06. |
| [ledgerline-okrs.md](ledgerline-okrs.md) | [templates/planning/okrs.md](../templates/planning/okrs.md) | PLANNING track, scored into Gate 6 | Sets one objective and four key results for the launch cycle, each with a baseline from the data sheet and a commitment type, keeps a check-in log with three dated entries, and scores KR1 at 0.44 on 2026-12-21 without editing the target. Uses N35, N64, N65, N68 to N75, the M ids and D6; the end-of-period section names KR1 and KR4 as the two under 0.5 with the pricing diagnosis; signed by Maya Chen on 2026-11-03 and scored with Isabel Ferreira present. |
| [ledgerline-experiment-brief.md](ledgerline-experiment-brief.md) | [templates/operate/experiment-brief.md](../templates/operate/experiment-brief.md) | OPERATE, feeds Gate 6 | Predeclares EXP-1 on 2026-11-05: the hypothesis that a per-seat price anchored on the N7 reviewer cost converts because the buyer reads the price against a labour bill, the arms, the sizing arithmetic, the ship, iterate and kill rules with owners, and the guardrails; the decided line records the KILL on 2026-12-18. Uses N7, N39, N46, N54 to N62, N65, N67, M-006, M-007, M-008, S-1, S-3, S-4, D3, D6 and LEDGERLINE-S1; signed by Maya Chen on 2026-11-05. |
| [ledgerline-metrics-dictionary.md](ledgerline-metrics-dictionary.md) | [templates/operate/metrics-dictionary.md](../templates/operate/metrics-dictionary.md) | OPERATE, feeds Gate 6; written before the instrumentation | Defines M-001 to M-012 with numerator, denominator, filters, grain, source, owner, refresh and known gap, the entities account, filer, report and drafted report, the segments S-1 to S-6, the lineage from inputs to KRs, and the gaps G-1 to G-3 with fixes. Uses the M, S and G ids, N32, N65 to N68, N82, N83, the owners P1, P2, P3, P7, P8 and one change-log entry dated 2026-12-19 on M-007's window; agreed by Maya Chen and Kwame Boateng on 2026-11-04. |
| [ledgerline-dashboard-spec.md](ledgerline-dashboard-spec.md) | [templates/operate/dashboard-spec.md](../templates/operate/dashboard-spec.md) | OPERATE, feeds Gate 6; specified before launch day | Specifies the add-on launch dashboard for one audience, the launch team: questions tied to decisions, tiles citing only M ids, the EXP-1 funnel tile restricted to the analyst until 2026-12-18 so nobody peeks, alerts agreed with each metric owner, and a verification pass on 2026-11-13 with one explained mismatch on G-2. Uses the M, S and G ids, N58, N74, N65 to N67, and LEDGERLINE-S5; built by Kwame Boateng, owned by Maya Chen, dated 2026-11-06. |
| [ledgerline-metrics-review.md](ledgerline-metrics-review.md) | [templates/operate/metrics-review.md](../templates/operate/metrics-review.md) | OPERATE, feeds Gate 6 | Grades the four KRs number against number for the window 2026-11-23 to 2026-12-18, maps the inputs to the KRs they were meant to drive, reports the guardrails intact, grades six launch assumptions including the two that broke, and records PIVOT on packaging with Isabel Ferreira as decider and the growth plan as the consequence. Uses N35, N61, N63 to N74, N76 to N78, N82, N88, the M ids, D3, D5, D6, R2, R5 and G-1 to G-3; signed by Maya Chen and Isabel Ferreira on 2026-12-21. |
| [ledgerline-sales-enablement-one-pager.md](ledgerline-sales-enablement-one-pager.md) | [templates/delivery/sales-enablement-one-pager.md](../templates/delivery/sales-enablement-one-pager.md) | DELIVER, feeds Gate 5 | Derives a one-page field document from the positioning, GTM and pricing files: the qualifying question built on S-5, pains in the customer's words from EV-C01 to EV-C06, claims with proof or marked unproven, five objections with a "do not say" column, including the seat-count objection answered honestly on 2026-11-06 with the answer that later lost deals, a pricing pointer with no numbers, and a three-step demo that avoids multi-receipt photos and foreign-language receipts. Uses N13, N14, N15, N23, N24, N36, N40, N44, N48, R3, D2, D3, LEDGERLINE-S2, S3 and S5; approved by Tomas Lindqvist on 2026-11-06, read by Marcus Webb, and marked withdrawn on 2026-12-21. |
| [ledgerline-win-loss-review.md](ledgerline-win-loss-review.md) | [templates/operate/win-loss-review.md](../templates/operate/win-loss-review.md) | OPERATE, feeds Gate 6 | Writes up WL-01, the Redfern Heating and Air no-decision, in full from a buyer interview, then reads WL-01 to WL-06 together and finds the pattern that 4 of 6 named seats billed for people who never file or an add-on priced above the plan, landing the finding in the pricing doc's off-cycle review and the growth plan. Uses N13, N34, N46, N47, N76, N77, N90, D3, D6, D7, LEDGERLINE-S4 and S6, and the Cinderwick benchmark; signed by Hana Sato on 2026-12-17. |
| [ledgerline-feedback-program.md](ledgerline-feedback-program.md) | [templates/operate/feedback-program.md](../templates/operate/feedback-program.md) | OPERATE, feeds Gate 6; intake feeds DISCOVER | Charters the Ledgerline Expenses Advisory Board to inform one recurring decision, the pricing and packaging review and each add-on Gate 5 go call, with nine curated seats, non-cash incentives, NDA and data-handling terms, an evidence-note capture rule, and written exit criteria; its first session on 2026-12-02 produced EV-AB01 three weeks before EXP-1 confirmed it. Uses N41, N78, S-5, EV-AB01, D6, D7 and the two dates 2026-11-10 and 2027-03-04; owned by Hana Sato. |
| [ledgerline-status-report.md](ledgerline-status-report.md) | [templates/execution/status-report.md](../templates/execution/status-report.md) | BUILD and DELIVER, weekly; feeds Gate 4 and Gate 5 | Reports the week of 2026-11-30 as AMBER overall with the colour rule applied: design partners and the experiment green with evidence, seat metering and German-language receipts amber with dates, the customer DPA red with the D5 decision named, a decider and a needed-by date, a one-day milestone slip accepted by name, and an escalation row for R4. Uses N43 to N45, N56, N79 to N85, R2, R3, R4, DEP1, DEP3, DEP5, D5, LEDGERLINE-S1 to S3 and the milestones 2026-11-09, 2026-11-23, 2026-12-18 and 2026-12-21; signed by Maya Chen on 2026-11-30. |

## What this journey teaches

- **Positioning:** choose the alternative before the category. Starting from "what would Redfern do without us" put a spreadsheet and Cinderwick on the page and made the free-bundle frame visibly wrong before any price existed. The silent promise of the add-on shelf, priced as a fraction of the plan, was written down in section 5 and then not read when the price was set; the document was right and the team did not use it.
- **Pricing and packaging:** a mismatch accepted in writing is still a mismatch. D3 recorded that seats do not rhyme with the north star and gave the reason; that honesty is what let the experiment's kill rule reopen the decision in one line instead of a quarter of argument. The benchmark table compared the price to the vendor and the spreadsheet and never to the customer's own plan, which is the row that was missing.
- **Growth plan:** one bet, the same bar. The plan sets EXP-2's success threshold at the 6.0% the seat price failed, so a pivot cannot be declared a success by lowering the line, and it carries the failed experiment as a ledger row rather than deleting it.
- **GTM plan:** phases advance on evidence, and a phase that never starts is a result. Phase 3 is on the page with its entry condition unmet, which is what a stop condition is for.
- **OKRs:** score against the baseline written at planning, not the number that turned out. KR1 at 0.44 is the most useful line in the set because the target was not edited when the price died.
- **Experiment brief:** the rule was written while everyone was still ignorant of the result. The mechanism clause, "because the buyer reads the price against a labour bill", is what the retro examined, and it was the mechanism that was wrong, not the copy.
- **Metrics dictionary:** two people computing M-006 get the same number only because G-2 says which accounts are excluded. The gap column is the dictionary.
- **Dashboard spec:** a tile that exists before the analysis date is a peeking device. Restricting the funnel tile to the analyst until 2026-12-18 is the spec enforcing the brief.
- **Metrics review:** the input tree, not the headline, tells the story. Approval on drafted reports held at 76% while conversion failed, so the product worked and the price did not, which is a pivot on packaging rather than on the product.
- **Sales enablement one-pager:** the honest answer to the seat-count objection was on the page from day one, and it lost deals honestly. A one-pager that traces every line to its source can be withdrawn in a day when the source changes.
- **Win-loss review:** interview the buyer, not the rep. The CRM said "price"; the buyer said "thirty-four seats", and only the second sentence names the fix.
- **Feedback program:** a board with one decision to inform produced the first signal three weeks before the data did, and the capture rule put it in the evidence base where the metrics review could cite it, with no automatic priority and none needed.
- **Status report:** amber needs a date and red needs a decision. The DPA row is red with D5 named, a decider and a needed-by date, and the cost of waiting a week written as two deals; that is the difference between an escalation and a complaint.
