# AARRR Funnel: Sahulat Bill Pay

Fills [frameworks/metrics/aarrr-funnel.md](../frameworks/metrics/aarrr-funnel.md). Everything here is invented and every number is ILLUSTRATIVE: Sahulat, its people, agents, customers, billers, bank, aggregator and telco are fiction, and the values below were chosen so that this funnel agrees with the [Sahulat journey data sheet](sahulat-journey.md) and the [Sahulat coverage sheet](sahulat-coverage-sheet.md), not to describe any real wallet, market or regulator.

**Owner:** Sara Lodhi, Data Analyst · **Prepared:** 2026-09-17 · **First recurring review:** 2026-09-21

## What it is for

This funnel defines the five bill-pay stages for Sahulat and locates the largest measurable leak before the first recurring metrics review.

The funnel uses:

- **Acquisition:** a wallet completes a bill lookup.
- **Activation:** the wallet pays the looked-up bill.
- **Retention:** the wallet pays again in the next four-week window.
- **Referral:** another user arrives through an invitation, introduction or agent referral.
- **Revenue:** a bill payment creates PKR 7 net revenue for Sahulat, with a PKR 0 customer fee.

The two comparison windows are:

- **FW-1:** the four weeks to 2026-08-16.
- **FW-2:** the four weeks to 2026-09-13.

FW-1 and FW-2 are defined in the coverage sheet as **FW-1** and **FW-2**. Counts come from query **FN-01**, using the channel of the wallet's first lookup in each window. FW-1 uses the same review window as N42 and N53.

The value used for leak weighting is CN27:

- 31,200 bills / 24,600 paying wallets = 1.27 bills per paying wallet in four weeks.
- 1.27 x 13 = about 16.5 bills per year.
- 16.5 x PKR 7 = PKR 115.5 revenue per paying wallet per year.

The customer fee remains PKR 0 per bill under N33. Sahulat's net is PKR 7 per bill under N32.

## Run it when

- A metrics review needs to identify where bill-pay growth leaks.
- Lookup volume and paid bills move differently.
- The team is considering more acquisition before understanding activation or retention.
- A recurring review needs channel-specific counts rather than a blended rate.
- A new event is needed for referral or another stage is not instrumented.

**Skip it when:** the available evidence cannot identify a person or wallet across the stages. In this read, referral is reported as not instrumented rather than assigned a guessed conversion rate.

## Inputs you need first

- The event definitions and bill-pay data in [sahulat-journey.md](sahulat-journey.md).
- The funnel-specific rows in [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md), especially CN27 to CN31.
- A four-week window for acquisition to activation.
- A following four-week window for retention.
- Channel on the first lookup, so USSD and app are not blended.
- The net revenue value of PKR 7 per bill and the PKR 0 customer fee.
- A referral event definition. Sahulat does not yet have one: CN31 records that no invite, introduction or agent-referral event exists in the ledger or USSD logs.

## The worksheet

### Step 1: define the stages

| Stage | Meaning in this product | The one event that marks it | Window after the previous stage | Source |
|---|---|---|---|---|
| Acquisition | A wallet starts the bill-pay journey by looking up at least one bill | `bill_lookup_completed` | Within FW-1 or FW-2, each four weeks | CN28, CN29, FN-01 |
| Activation | The wallet receives the bill result and pays at least one bill | `bill_payment_posted` | In the same four-week window as the lookup | N42, N53, CN28, CN29 |
| Retention | The wallet that paid in FW-1 pays again in FW-2 | `bill_payment_posted` by an FW-1 payer in the next window | The next four-week window | CN30, FN-01 |
| Referral | Another user arrives because of this wallet through an invitation, introduction or agent referral | No event instrumented | Not measurable | CN31, FN-01 build notes |
| Revenue | A posted bill payment generates PKR 7 net revenue for Sahulat while the customer fee is PKR 0 | `bill_payment_posted` with the BillBridge net fee recorded | At the payment event | N32, N33 |

Revenue is defined at the bill level. Where this worksheet shows a paying-wallet revenue proxy, it uses CN27's PKR 115.5 annual value per paying wallet. It does not treat the proxy as booked bill revenue.

### Step 2: measure the transitions, cut by channel and segment

The first two rows compare acquisition to activation in FW-1 and FW-2. Retention compares FW-1 payers with their repeat payment in FW-2. The revenue rows use the retention event as the revenue-producing payment, so the wallet-level conversion is 100 percent by definition for that proxy. This proxy assumes that a lost activated user generates zero future revenue within the measured window, and therefore assigns them the full PKR 115.5 they *would have* generated if they had retained. This makes the math defensible as a maximum potential loss metric.

| Transition | Channel or segment | Entered | Converted | Conversion (%) | Same figure last period | Change |
|---|---|---:|---:|---:|---|---:|
| Acquisition to activation | FW-1, USSD | 56,300 lookups | 23,200 payers | 23,200 / 56,300 = 41.2 percent | FW-2 USSD: 25,700 / 53,600 = 47.9 percent | 47.9 percent - 41.2 percent = +6.7 percentage points |
| Acquisition to activation | FW-1, app | 5,200 lookups | 1,400 payers | 1,400 / 5,200 = 26.9 percent | FW-2 app: 1,400 / 5,300 = 26.4 percent | 26.4 percent - 26.9 percent = -0.5 percentage points |
| Acquisition to activation | FW-2, USSD | 53,600 lookups | 25,700 payers | 25,700 / 53,600 = 47.9 percent | FW-1 USSD: 23,200 / 56,300 = 41.2 percent | +6.7 percentage points |
| Acquisition to activation | FW-2, app | 5,300 lookups | 1,400 payers | 1,400 / 5,300 = 26.4 percent | FW-1 app: 1,400 / 5,200 = 26.9 percent | -0.5 percentage points |
| Activation to retention | USSD, FW-1 payers to FW-2 repeat payers | 23,200 FW-1 payers | 13,600 repeat payers | 13,600 / 23,200 = 58.6 percent | No earlier paired four-week read is available | Not available |
| Activation to retention | App, FW-1 payers to FW-2 repeat payers | 1,400 FW-1 payers | 700 repeat payers | 700 / 1,400 = 50.0 percent | No earlier paired four-week read is available | Not available |
| Retention to referral | USSD | Not instrumented | Not instrumented | Not measurable | Not instrumented | Not measurable |
| Retention to referral | App | Not instrumented | Not instrumented | Not measurable | Not instrumented | Not measurable |
| Retention to revenue | USSD, retained-wallet proxy | 13,600 repeat payers | 13,600 revenue-stage wallets | 13,600 / 13,600 = 100 percent | No earlier paired four-week read is available | Not available |
| Retention to revenue | App, retained-wallet proxy | 700 repeat payers | 700 revenue-stage wallets | 700 / 700 = 100 percent | No earlier paired four-week read is available | Not available |

FW-1 revenue proxy arithmetic:

- USSD: 13,600 retained wallets x PKR 115.5 annual value per paying wallet = PKR 1,570,800 annualized proxy.
- App: 700 retained wallets x PKR 115.5 annual value per paying wallet = PKR 80,850 annualized proxy.
- Combined: 14,300 retained wallets x PKR 115.5 = PKR 1,651,650 annualized proxy.

This is a value proxy, not a separate revenue ledger total. CN27 supplies the value per paying wallet. N32 supplies PKR 7 net per bill, and N33 supplies the PKR 0 customer fee.

### Step 3: rank the leaks

The first complete paired read is FW-1 to FW-2. Because referral is not instrumented, any leak weight requiring a referral conversion product is not computable and is not ranked.

For the measurable lookup-to-pay leak, the downstream product is the channel's FW-1 to FW-2 retention rate multiplied by the revenue-stage proxy rate of 100 percent. For the activation-to-retention leak, the downstream product is the revenue-stage proxy rate of 100 percent, reflecting the assumption that a lost activated user generates zero future revenue within the measured window and thus represents the full PKR 115.5 potential loss.

Leak weights below carry the unrounded transition ratio through the whole calculation. Percentages shown elsewhere for readability, such as 58.6 percent, are rounded to one decimal; recomputing a leak weight from the rounded percentage instead of the unrounded ratio (13,600 / 23,200) gives a close but not identical figure.

#### USSD lookup-to-pay

- People lost = 56,300 - 23,200 = 33,100.
- Downstream conversion product = (13,600 / 23,200) x 100 percent = 58.6 percent.
- Retained-wallet equivalent lost = 33,100 x (13,600 / 23,200) = 19,403.4.
- Leak weight = 19,403.4 x PKR 115.5 = PKR 2,241,098.3 annualized value proxy.

#### App lookup-to-pay

- People lost = 5,200 - 1,400 = 3,800.
- Downstream conversion product = (700 / 1,400) x 100 percent = 50.0 percent.
- Retained-wallet equivalent lost = 3,800 x (700 / 1,400) = 1,900.
- Leak weight = 1,900 x PKR 115.5 = PKR 219,450 annualized value proxy.

| Transition | People lost | Downstream conversion product | Leak weight | Rank |
|---|---:|---:|---:|---:|
| FW-1 USSD lookup to pay | 56,300 - 23,200 = 33,100 | 13,600 / 23,200 x 100 percent = 58.6 percent | 33,100 x 58.6 percent x PKR 115.5 = PKR 2,241,098.3 | 1 |
| FW-1 app lookup to pay | 5,200 - 1,400 = 3,800 | 700 / 1,400 x 100 percent = 50.0 percent | 3,800 x 50.0 percent x PKR 115.5 = PKR 219,450 | 2 |
| FW-1 USSD activation to retention | 23,200 - 13,600 = 9,600 | Revenue proxy rate = 100 percent | 9,600 x 100 percent x PKR 115.5 = PKR 1,108,800 | 3 |
| FW-1 app activation to retention | 1,400 - 700 = 700 | Revenue proxy rate = 100 percent | 700 x 100 percent x PKR 115.5 = PKR 80,850 | 4 |
| Retention to referral, USSD | Not measurable | Referral conversion not instrumented | Not computable | Not ranked |
| Retention to referral, app | Not measurable | Referral conversion not instrumented | Not computable | Not ranked |

The USSD lookup-to-pay leak ranks first because its calculated weight of PKR 2,241,098.3 is greater than the USSD retention leak of PKR 1,108,800 and the app lookup-to-pay leak of PKR 219,450.

### Step 4: one fix per leak

Only the highest measurable leak receives a fix in this review.

| Leak (rank) | Why it leaks (from evidence, not a guess) | Evidence | The one fix | Expected change in conversion | Experiment brief |
|---|---|---|---|---|---|
| USSD lookup to pay, rank 1 | The USSD path loses 33,100 of 56,300 lookup wallets in FW-1. The available usability evidence shows that customers confused the bill reference with the consumer number, so the first fix targets the lookup result and payment handoff rather than adding acquisition. | CN12: on TK-1, 3 of 5 customers completed the lookup unassisted, and 2 entered the consumer number printed beside the reference. CN28: 23,200 of 56,300 USSD lookup wallets paid, or 41.2 percent. CN29: FW-2 improved to 25,700 of 53,600, or 47.9 percent, but the leak remains the largest weighted leak. | Rewrite the USSD lookup confirmation to label the bill reference as the payment reference, show the returned biller and amount before the pay action, and prevent the payment step until the reference is confirmed. | Not quantified before the experiment. The success measure is the USSD lookup-to-pay conversion, with counts and rate reported against the FW-1 baseline of 23,200 / 56,300 = 41.2 percent. The app conversion is a comparison guardrail, not the target path. | [Experiment brief](../templates/operate/experiment-brief.md) |

Referral remains an instrumentation action, not a product fix. The next event taxonomy must distinguish an invite, an introduction and an agent referral before a referral conversion can be calculated.

## Reading the result

The largest measurable weighted leak is USSD lookup to pay, not the lowest raw percentage. The USSD path has a 41.2 percent FW-1 lookup-to-pay conversion, compared with 26.9 percent for app, but it has 56,300 entered wallets. Its larger entered population produces the larger weighted opportunity:

- USSD lookup-to-pay loss: 33,100 wallets.
- USSD leak weight: PKR 2,241,098.3 annualized value proxy.
- App lookup-to-pay loss: 3,800 wallets.
- App leak weight: PKR 219,450 annualized value proxy.

The FW-2 comparison shows:

- USSD lookup-to-pay: 41.2 percent in FW-1 to 47.9 percent in FW-2.
- App lookup-to-pay: 26.9 percent in FW-1 to 26.4 percent in FW-2.
- The USSD rate improved by 6.7 percentage points, while the app rate declined by 0.5 percentage points.
- FW-1 retention to FW-2 repeat payment was 58.6 percent for USSD and 50.0 percent for app.

The retention read is directional for the first recurring review because it has one paired comparison only. Referral cannot be read as zero. It is not instrumented under CN31.

Revenue is PKR 7 net per bill with a PKR 0 customer fee. The annualized paying-wallet value used in leak weighting is CN27's PKR 115.5. The customer fee is not added to revenue.

## ILLUSTRATIVE example

The Sahulat funnel is measured using fictional data from FN-01. The figures are ILLUSTRATIVE and are not industry benchmarks.

| Transition | Channel | Entered | Converted | Conversion |
|---|---|---:|---:|---:|
| Acquisition to activation, FW-1 | USSD | 56,300 | 23,200 | 23,200 / 56,300 = 41.2 percent |
| Acquisition to activation, FW-1 | App | 5,200 | 1,400 | 1,400 / 5,200 = 26.9 percent |
| Activation to retention, FW-1 to FW-2 | USSD | 23,200 | 13,600 | 13,600 / 23,200 = 58.6 percent |
| Activation to retention, FW-1 to FW-2 | App | 1,400 | 700 | 700 / 1,400 = 50.0 percent |
| Retention to referral | USSD and app | Not instrumented | Not instrumented | Not measurable |
| Retention to revenue proxy | USSD | 13,600 | 13,600 | 100 percent |
| Retention to revenue proxy | App | 700 | 700 | 100 percent |

The one fix targets the USSD reference-number confusion. The experiment must report the lookup count, paid count and conversion rate, rather than only a percentage. It must also retain the app rate as a channel comparison and keep referral out of the calculation until the missing event exists.

## The trap

The trap is a blended funnel that hides the channel difference. Combining FW-1 USSD and app produces:

- Lookups = 56,300 + 5,200 = 61,500.
- Payers = 23,200 + 1,400 = 24,600.
- Blended lookup-to-pay = 24,600 / 61,500 = 40.0 percent.

That blended 40.0 percent does not show:

- USSD: 23,200 / 56,300 = 41.2 percent.
- App: 1,400 / 5,200 = 26.9 percent.

A second trap is treating referral as zero. CN31 says no referral event is instrumented, so the correct result is not zero percent. The correct result is not measurable.

A third trap is treating the PKR 115.5 value per paying wallet as booked revenue. It is CN27's annualized value proxy, calculated from:

- 31,200 bills / 24,600 wallets = 1.27 bills in four weeks.
- 1.27 x 13 = about 16.5 bills per year.
- 16.5 x PKR 7 = PKR 115.5 per paying wallet per year.

## Feeds

- [sahulat-journey.md](sahulat-journey.md), the canonical Sahulat data sheet, identifiers and timeline.
- [sahulat-coverage-sheet.md](sahulat-coverage-sheet.md), CN27 to CN31 and the FN-01 definitions for FW-1 and FW-2.
- [Experiment brief](../templates/operate/experiment-brief.md), for the USSD lookup-to-pay fix.
- The 2026-09-21 first recurring metrics review.
- The AARRR method is based on the ideas of Dave McClure, from the talk "Startup Metrics for Pirates" (2007), explained in the repository's own words.
