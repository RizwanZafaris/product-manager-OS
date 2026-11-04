---
layer: frameworks
stage: OPERATE
gate: 6
feeds: ["templates/planning/growth-plan.md", "templates/operate/metrics-review.md", "templates/operate/experiment-brief.md"]
method: "knowledge/INDEX.md"
aliases: ["Activation and Churn Diagnosis", "activation-churn-diagnosis"]
---
# Activation and Churn Diagnosis

No single originator. Comparing the early behaviour of users who stayed against users who left is common growth-analytics practice, built on cohort analysis as brought into product work by Eric Ries in The Lean Startup (2011), see [cohort retention](cohort-retention.md), and on the activation stage of Dave McClure's "Startup Metrics for Pirates" talk (2007), see the [AARRR funnel](aarrr-funnel.md). The inter-coder check in Part 3 uses Jacob Cohen's kappa, from "A Coefficient of Agreement for Nominal Scales", Educational and Psychological Measurement (1960). Explained here in this repository's own words.

## What it is for

Four questions that sit at the two ends of a customer's life and are usually answered by assertion. Which early action separates the people who stay from the people who leave, so that onboarding can aim at it (the activation event, sometimes called the "aha" moment). Where onboarding loses people before they reach it. Why the people who left say they left, coded so that two readers get the same tally. And whether a save flow at the cancel button keeps customers or only delays them. The decisions it improves: what the activation event in the [AARRR funnel](aarrr-funnel.md) and the [growth plan](../../templates/planning/growth-plan.md) should be, which onboarding step gets the next experiment, which churn reason gets product time, and whether a retention offer earns its cost.

## Run it when

- The activation event in the funnel was chosen by a meeting, not by a comparison of retained and churned users
- The [cohort retention](cohort-retention.md) curve decays and nobody can say what the users who stayed did differently in their first week
- A churn number is reported every month with a reason breakdown that reads "price" and "other"
- Someone proposes a cancellation discount, a pause option, or an exit survey, and the plan has no control group

**Skip it when:** fewer than about 200 users or accounts started in the window you would compare, or fewer than 30 churned. Below that, every cell in the Part 1 table is a handful of people and the "activation event" you find is whichever action the last three loyal customers happened to take; run churn interviews through the [user-interview skill](../../skills/user-interview/SKILL.md) and code those instead.

## Inputs you need first

- A retention definition: the core action from the [north star input tree](north-star-input-tree.md) and the period, the same one the [cohort retention](cohort-retention.md) sheet uses, never a login
- An event log per user or account for the first days after the cohort key, with timestamps, from the [analytics instrumentation spec](../../templates/delivery/analytics-instrumentation-spec.md)
- The onboarding steps in order, each with the event that marks it
- Every churn record for the window: cancellation survey answers with free text, billing failure records, CSM or account notes, and support tickets from the 90 days before the churn date
- Cancel-flow traffic, for Part 4, and a legal reviewer named before any save offer is tested, per the [choice symmetry audit](../design/choice-symmetry-audit.md)

## The worksheet

### Part 1: find the activation event

Fix two windows before looking at any data. The action window is when a candidate action counts (for example, days 0 to 7 after the cohort key). The retention window is when retention is measured (for example, active in week 8). The action window must close before the retention window opens; an action that can only happen late, such as a second month's export, is retention measured twice, not a predictor of it.

For each candidate action A, split the cohort of n users (or accounts, for a product bought by teams) into those who did A inside the action window and those who did not, and count who was retained.

| Candidate action (event) | Did A: users n_A | Did A: retained k_A | Did not: users n_notA | Did not: retained k_notA | r_A | r_notA | Lift | Difference (points), 95% interval | Reach | Capture | Passes the floor? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [event] | | | | | | | | | | | |

Arithmetic, written out:

- Retention given the action: r_A = k_A / n_A
- Retention given not: r_notA = k_notA / n_notA
- Lift = r_A / r_notA
- Difference = r_A minus r_notA, in percentage points. Its 95% interval is the difference plus or minus 1.96 x the square root of (r_A x (1 minus r_A) / n_A + r_notA x (1 minus r_notA) / n_notA)
- Reach = n_A / n, the share of the cohort that did the action
- Capture = k_A / (k_A + k_notA), the share of all retained users who did the action

**Sample size floor.** A candidate is read only when both groups hold at least 200 users and each group holds at least 20 retained and 20 not retained. A candidate below the floor is written down as "below floor", not dropped silently, because the next cohort may lift it over.

**Selection rule.** Among candidates that pass the floor and whose interval excludes zero, prefer the one with the highest capture among those with reach of at least 25 percent; break a close call on lift. Capture matters more than lift: an action with a lift of 4 that only one retained user in five ever took is a trait of a small group of enthusiasts, not the path most customers take to value.

**Threshold sweep.** For a counted action (teammates invited, records created), repeat the row at thresholds k = 1, 2, 3, 5 and read where r_A stops climbing by more than about 10 points per step or reach falls under the 25 percent floor. That knee is the threshold; above it the action describes the most committed customers rather than a bar a new customer can be helped over.

### Part 2: onboarding step drop-off

One row per onboarding step, in the order the product forces or suggests them, ending at the activation event from Part 1.

| Step | Event | Users reaching it (n_i) | Step conversion | Cumulative | Lost here | Median time from previous step | Required by the user's job, or by our process? | Leak weight |
|---|---|---|---|---|---|---|---|---|
| 0 | [cohort key, e.g. sign-up] | | 100% | 100% | | | | |
| 1 | [event] | | | | | | | |

Arithmetic:

- Step conversion at step i = n_i / n_(i-1); cumulative = n_i / n_0; lost here = n_(i-1) minus n_i
- Leak weight at step i = lost here x (n_final / n_i), where n_final is the count reaching the activation event. It prices each loss by how often the people who did pass that step went on to activate, the same idea the [AARRR funnel](aarrr-funnel.md) leak weight uses, so a large loss at a step from which most people later activate outranks a large loss at a step from which few do

The "required by" column is the one that finds fixes. A step the user's job needs (you cannot schedule staff you have not added) can be made easier; a step only our process needs (payment details, a profile, a tour) can often be moved after the activation event or removed.

### Part 3: churn reasons, coded

**Classify every churn first.** Voluntary: the customer decided to stop, by cancelling, by not renewing at term end, or by telling an account manager so. Involuntary: the subscription ended with no customer decision, through a failed payment, an expired card, retries exhausted with no response, or an account closed by us under policy. A downgrade is contraction, not churn, and is tallied on its own line. The two churn types get different owners: involuntary churn is a billing and dunning problem, and mixing it into a reason chart inflates "other" and hides the cheapest recovery there is.

**The taxonomy.** Start from this list and adapt it once, before coding, never during.

| Code | Reason | Include | Exclude |
|---|---|---|---|
| V1 | No longer needs it | business closed, project ended, seasonal stop | a need met by a competitor (V6) |
| V2 | Value not realised | never set up, too hard to start, did not fit the workflow | a named missing feature (V4) |
| V3 | Price or budget | price named as the reason, budget cut | price named while usage never started (see rule 4) |
| V4 | Missing capability | a specific feature or integration named | general "not good enough" (V2 or V5) |
| V5 | Product quality | bugs, outages, slowness, data errors | a feature that does not exist (V4) |
| V6 | Switched to an alternative | named competitor, built in-house, back to spreadsheets or paper | |
| V7 | Service experience | support, onboarding help, account management | |
| V8 | Organisational change | champion left, acquired, tools consolidated | |
| V9 | No reason given | blank survey, no notes, no reply | anything a coder inferred without a source |
| I1 to I4 | Involuntary | I1 card declined, I2 card expired, I3 retries exhausted, I4 closed by us | |

**Coding rules.**

1. One primary code per churned account, and at most two secondary codes
2. Code from a source, never from a coder's opinion: the survey answer, the free text, a ticket, a note. Record which source each code came from
3. Keep two fields. The stated reason is what the customer said. The observed reason is what the usage record shows: never reached the activation event, usage fell months before the cancel, a quality incident in the last 90 days. Disagreement between the two is a finding, not an error to resolve
4. When the stated reason is price and the account never reached the activation event, the stated code stays V3 and the observed code is V2. Report both counts
5. Randomise the order of reasons in a cancellation survey, and keep the free-text box. A fixed list collects its first option and its quickest option more often than its truest one
6. A lost renewal on a sales-led account also gets a [win-loss review](../../templates/operate/win-loss-review.md); this sheet tallies it, that template explains it

**Inter-coder check.** Two people code the same random sample of at least 50 voluntary records, or 20 percent of the period's voluntary churn if that is larger, without seeing each other's codes. Compute Cohen's kappa on the primary codes:

- Observed agreement p_o = records where both coders chose the same primary code / records in the sample
- Chance agreement p_e = the sum, over every code, of (coder 1's share of records given that code x coder 2's share of records given that code)
- kappa = (p_o minus p_e) / (1 minus p_e)

The floor here is kappa of 0.6. Below it, the definitions are ambiguous: read the pairs the coders disagreed on, tighten the include and exclude columns, and recode the sample before tallying the period. The 0.6 floor is this sheet's rule; Cohen proposed the statistic, not the threshold.

| Period | Churned | Involuntary | Voluntary | Top stated code (count) | Top observed code (count) | Sample coded twice | p_o | p_e | kappa |
|---|---|---|---|---|---|---|---|---|---|
| [period] | | | | | | | | | |

### Part 4: save flows and cancellation tests

A save flow is whatever stands between the cancel button and the cancellation: a pause, a downgrade, a discount, an offer of help. Test it as an experiment, written up in an [experiment brief](../../templates/operate/experiment-brief.md), never by switching it on and watching the cancel count fall.

| Field | Answer |
|---|---|
| Offer | [pause for n weeks / downgrade to tier / discount of n for n months / help call] |
| Who is eligible | [all cancel-intent sessions, or a named segment] |
| Assignment | [random, at the moment of cancel intent; the unit is the account, not the session] |
| Primary measure | [share still paying at day 60 or 90 after cancel intent, per arm] |
| Offer cost | [revenue given away per accepted offer] |
| Guardrail | [cancellation completes in no more steps than sign-up did; the decline is as prominent as the offer] |
| Legal reviewer | [name] |

Arithmetic:

- Saved at day 0 = cancel-intent accounts that did not cancel that day / cancel-intent accounts, per arm. Reported, never decided on
- Retained at horizon s = cancel-intent accounts still paying at day 60 or 90 / cancel-intent accounts, per arm
- Net saved accounts = (s_treatment minus s_control) x n_treatment, with the same 95% interval formula as Part 1
- Break-even months = offer cost across all accepted offers / (net saved accounts x monthly price). The offer pays for itself only if a net saved account stays at least that many months after the offer ends

The guardrail is not optional. A save flow that wins because declining it takes four screens and cancelling takes a phone call is the obstruction the [choice symmetry audit](../design/choice-symmetry-audit.md) counts and [Deceptive Design](../../knowledge/design/deceptive-design.md) describes, and it is a regulatory exposure before it is a retention result. Run that audit on both arms before the test starts.

## Reading the result

The activation event is a hypothesis until an experiment moves it. Part 1 finds the action that retained users took; it cannot say whether taking the action made them stay or whether motivated customers simply do more of everything. Promote the winner to the funnel's activation event, then write the experiment that helps more new users reach it, and compare the retention it actually produces with the retention the lift predicted. If retention moves by much less than predicted, the action was partly a trait of the people who stay.

A big loss at a step the user's job needs is a design problem; a big loss at a step only our process needs is a sequencing decision, and usually the cheaper fix. A step whose median time is days rather than minutes is a step people leave to do elsewhere (find staff details, ask a colleague, fetch a card) and should be designed as a return visit, with a reminder, not as a screen.

In the churn tally, read involuntary first: it is the cheapest share to check, and its fix sits in billing settings and payment retries rather than on the roadmap. Then read the gap between stated and observed codes. A tally where price leads the stated column and value-not-realised leads the observed column is a tally about onboarding, whatever the survey says. A V9 share above about a quarter means the collection, not the customers, is the problem.

A save flow judged on day-0 saves will always look better than it is. Discounted and paused accounts often cancel at the end of the offer, which is why the horizon measure decides and the break-even line has to clear the lifetime the [unit economics](unit-economics.md) assumes.

## ILLUSTRATIVE example

Invented. Ottergrid is a fictional shift-scheduling app for independent cafes, sold self-serve at a fictional $29 a month. All figures are ILLUSTRATIVE. Cohort: 1,800 cafes that signed up in one quarter. Retained means a rota published in week 8. Action window: days 0 to 7. Overall, 612 cafes were retained (34 percent).

**Part 1.**

| Candidate action | n_A | k_A | n_notA | k_notA | r_A | r_notA | Lift | Difference, 95% interval | Reach | Capture | Floor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Published first rota | 1,080 | 540 | 720 | 72 | 50.0% | 10.0% | 5.0 | 40.0 points, 36.3 to 43.7 | 60% | 88% | passes |
| Invited 3 or more staff | 630 | 410 | 1,170 | 202 | 65.1% | 17.3% | 3.8 | 47.8 points, 43.5 to 52.1 | 35% | 67% | passes |
| Set up shift templates | 900 | 360 | 900 | 252 | 40.0% | 28.0% | 1.4 | 12.0 points, 7.7 to 16.3 | 50% | 59% | passes |
| Connected payroll export | 90 | 72 | 1,710 | 540 | 80.0% | 31.6% | 2.5 | not read | 5% | 12% | below floor |

The interval for the first row: 1.96 x the square root of (0.5 x 0.5 / 1,080 + 0.1 x 0.9 / 720) = 1.96 x 0.0189 = 3.7 points either side of 40.0. Publishing the first rota captures 88 percent of retained cafes at 60 percent reach, so it becomes the activation candidate, even though inviting staff shows the larger difference. Payroll export has the most striking retention given the action and is below the floor at 90 cafes; it is logged, not chosen.

Threshold sweep on staff invited: at 1 or more, r_A is 44.4 percent (560 of 1,260) at 70 percent reach; at 3 or more, 65.1 percent at 35 percent reach; at 5 or more, 74.1 percent (215 of 290) at 16 percent reach. The climb from 1 to 3 is 20.7 points and from 3 to 5 is 9.0 points while reach falls under 25 percent, so 3 is the knee and "3 or more staff invited" becomes the secondary signal.

**Part 2.**

| Step | Event | n_i | Step conversion | Cumulative | Lost here | Median time from previous | Required by | Leak weight |
|---|---|---|---|---|---|---|---|---|
| 0 | Signed up | 1,800 | 100% | 100% | | | | |
| 1 | Created venue | 1,640 | 91.1% | 91.1% | 160 | 6 minutes | user's job | 160 x (1,080 / 1,640) = 105 |
| 2 | Added first staff member | 1,260 | 76.8% | 70.0% | 380 | 26 hours | user's job | 380 x (1,080 / 1,260) = 326 |
| 3 | Built first shift | 1,190 | 94.4% | 66.1% | 70 | 24 minutes | user's job | 70 x (1,080 / 1,190) = 64 |
| 4 | Published first rota | 1,080 | 90.8% | 60.0% | 110 | 3 hours | user's job | 110 x 1 = 110 |

Step 2 leads by weight, and its 26-hour median says owners leave to collect staff names and phone numbers. The fix proposed: let an owner build and publish a draft rota with placeholder staff, then invite real staff from the published rota.

**Part 3.** 260 cafes churned in the following quarter: 70 involuntary (44 card declined, 21 card expired, 5 retries exhausted) and 190 voluntary. Stated primary codes for the 190: V3 price 68, V1 no longer needs it 46, V2 value not realised 30, V6 switched 22, V4 missing capability 14, V9 no reason 10. Of the 68 who said price, 41 never published a rota, so the observed column moves 41 records from V3 to V2: observed V2 is 71, observed V3 is 27.

Inter-coder check on a random 60 of the 190. The coders agreed on 48, so p_o = 48 / 60 = 0.80. Their primary-code counts were, coder 1 then coder 2: V3 22 and 18, V1 14 and 15, V2 10 and 13, V6 7 and 7, V4 4 and 4, V9 3 and 3. p_e = (22 x 18 + 14 x 15 + 10 x 13 + 7 x 7 + 4 x 4 + 3 x 3) / (60 x 60) = 810 / 3,600 = 0.225. kappa = (0.80 minus 0.225) / (1 minus 0.225) = 0.575 / 0.775 = 0.74, above the 0.6 floor. Most disagreements were V3 against V2, the same boundary rule 4 addresses.

**Part 4.** A pause offer of eight weeks, tested on 400 cancel-intent accounts over two months, 200 per arm. Saved at day 0: control 12 (6 percent), treatment 70 accepted the pause (35 percent). Still paying at day 90: control 8 (4 percent), treatment 42 (21 percent). Net saved = (0.21 minus 0.04) x 200 = 34 accounts, interval 10.7 to 23.3 points. The day-0 view claimed 29 points; the horizon shows 17. Offer cost = 70 accepted x 2 months x $29 = $4,060 of revenue paused. Break-even = 4,060 / (34 x 29) = 4.1 months after resuming. The choice symmetry audit passed both arms: "Continue to cancel" sat beside the offer at equal weight, and cancellation took two steps in both arms.

## The trap

Treating the Part 1 winner as a lever because the lift is large. Customers who meant to stay do more of everything in their first week, so almost every early action shows lift, and the most effortful actions, inviting colleagues or connecting another system, show the most. The tell: an activation event chosen on lift alone, no capture column, and no experiment that pushed the action and measured retention afterwards. In the example, Ottergrid's later onboarding experiment raised first-week publishing from 60 to 71 percent. The Part 1 lift predicted retention near 34 + 11 x 0.40 = 38.4 percent; the treatment arm retained at 37 percent. The event was real, and part of its lift was the kind of cafe that publishes. Write the predicted and observed numbers side by side every time, and size the next bet on the observed one.

## Feeds

- [Growth plan](../../templates/planning/growth-plan.md), section 3 (the mechanism and where it leaks) and section 4 (the cheapest experiment)
- [Metrics review](../../templates/operate/metrics-review.md), section 2, where the activation and churn inputs are read, with the involuntary share on its own line
- [Experiment brief](../../templates/operate/experiment-brief.md), one per onboarding fix and one per save offer
- [AARRR funnel](aarrr-funnel.md), whose activation stage takes the Part 1 event, and [cohort retention](cohort-retention.md), which takes the activation event as its cohort key
- [Customer health score](customer-health-score.md), which uses the activation event and the churn codes as candidate signals and as the outcome a back-test is scored against
- [Customer success handoff](../../templates/operate/customer-success-handoff.md), which carries the activation event into the adoption plan per segment
- [Choice symmetry audit](../design/choice-symmetry-audit.md), run on every save flow before it is tested
- The [analyst agent](../../agents/analyst-agent.md) runs Parts 1 and 2; the [feedback-synthesis skill](../../skills/feedback-synthesis/SKILL.md) supplies the free text Part 3 codes
- OPERATE stage, reviewed at [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: none in the knowledge layer; see the [knowledge index](../../knowledge/INDEX.md)
