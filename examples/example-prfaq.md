# PR/FAQ: Wrenfield Verified Same-Day

Fills [templates/definition/prfaq.md](../templates/definition/prfaq.md). Everything here is invented: Wrenfield is a fictional home-services marketplace, Verified Same-Day is a fictional feature, every named person is a role filled by an invented name, and every count and dollar figure is ILLUSTRATIVE. This example is self-contained: it does not belong to the Sahulat, Ledgerline, or Harbourgate journeys, and its figures are not drawn from theirs. See the [examples index](README.md).

**Owner:** Devon Okafor, product manager · **Last updated:** 2026-09-08 · **Status:** Draft, prepared for green-light review

## 1. Press release

- **Headline:** Wrenfield now shows a same-day background check before a stranger walks into your home
- **Subheading:** Homeowners booking plumbing, electrical, or HVAC visits see a badge proving the assigned contractor cleared a check within the last 24 hours, not a one-time check from whenever they joined
- **Location and imagined date:** Denver, Colorado, 2027-03-02

Wrenfield, the home-services marketplace, today launched Verified Same-Day, a badge that appears on a contractor's profile the moment a homeowner is matched for an in-home visit, confirming their background check was refreshed within the past 24 hours rather than relying on the check run when they first joined the platform months or years earlier.

Homeowners booking an in-home visit today see a contractor's name, photo, and rating, and nothing about who that person is right now. A rating built on finished jobs says nothing about what changed since. In a survey of 640 households that had booked an in-home job in the last quarter, 41 percent said "not knowing who is actually showing up" was a reason they hesitated or delayed booking, and Wrenfield's own funnel shows a 23 percent abandonment rate at the contractor-reveal step for in-home categories, against 6 percent for jobs that do not require entering the home.

Verified Same-Day closes that gap by pulling a fresh consumer report on the assigned contractor before each in-home job is confirmed, through the same background-check process contractors already consented to at onboarding, extended to cover this recurring use. If a report comes back with a new disqualifying record, the job is reassigned automatically and the homeowner never sees that contractor's profile. Nothing changes for outdoor-only categories like lawn care, where the homeowner is rarely present for the work.

"I almost cancelled the appointment because I realized I knew nothing about the guy coming to fix my water heater. Seeing that his check was run that morning, not two years ago, is the difference between me staying home for it and me asking a neighbor to let him in," said Priya Nathan, a Wrenfield homeowner in Denver, describing the concern the feature is built to answer.

A homeowner sees the badge automatically on the booking confirmation screen for any plumbing, electrical, or HVAC job in Denver, Portland, or Raleigh; there is nothing to turn on and no extra step to complete.

## 2. External FAQ

| Question | Answer |
|---|---|
| How much does it cost? | Nothing. Verified Same-Day is included in every in-home booking in the launch metros; there is no separate fee to the homeowner and no change to contractor payout. |
| Who can use it at launch? | Homeowners booking plumbing, electrical, or HVAC visits in Denver, Portland, or Raleigh. Outdoor-only categories, and metros outside these three, do not show the badge at launch. |
| What happens to my existing data or workflow? | Nothing changes for a homeowner who has already booked or is rebooking a recurring contractor; the badge simply appears on the confirmation screen going forward. No past booking is affected retroactively. |
| What if the contractor assigned to my job does not pass the same-day check? | The job is reassigned to another available contractor in the same category before the homeowner sees a profile; the homeowner is not shown a name that later has to be withdrawn. |
| Does this replace the review and rating system? | No. Ratings describe how a job went; Verified Same-Day describes who is coming today. They answer different questions and both stay on the profile. |

## 3. Internal FAQ

| Question | Answer, with evidence or an honest "judgment call" |
|---|---|
| How big is this, and how do we know? | In-home categories were 61 percent of Wrenfield's trailing twelve-month GMV: 46,000 completed jobs at an average ticket of $504, or roughly $23.18M (finance ledger extract, 2026-08-30, ILLUSTRATIVE). The in-home contractor-reveal step ran about 64,000 sessions in the same period at 23 percent abandonment, against 6 percent for non-in-home jobs (product analytics, funnel step FUN-CR, 2026-08-30). If Verified Same-Day cuts in-home abandonment from 23 percent to 15 percent, an 8-point improvement that is a judgment call, not a measured result, that recovers roughly 5,120 bookings a year (8 percent of 64,000), or about $2.58M in incremental GMV a year at the current average ticket. At Wrenfield's 18 percent take rate, that is roughly $464K in incremental annual revenue. |
| Why are we the right team to build it? | Every contractor already signs a standalone background-check authorization at onboarding as a condition of joining the marketplace, and Wrenfield already has a live integration with Cobalt Screening, its Fair Credit Reporting Act (FCRA) consumer reporting agency. This is an extension of an existing, working pipeline, not a new vendor relationship or a new consent flow built from nothing. |
| What must be true for the launch story above to happen? | Three things. First, Cobalt Screening's instant-file product must return a same-day result for at least 95 percent of pulls; anything slower forces a fallback to the contractor's last check, which quietly turns the badge back into today's stale guarantee. Second, contractors in the three launch metros must not decline the recurring authorization in numbers large enough to shrink same-day supply; we do not have a number for this yet, which is the open question in section 4 below the fold, restated as the risk row it actually is. Third, legal has to sign off that a single authorization signed once can lawfully cover recurring same-day pulls rather than requiring a fresh signature every time; see the next row. |
| What are we choosing not to do to fund this? | Verified Same-Day is funded by pausing the planned "verified reviews" filter for this quarter; both were scored roughly equal in the last roadmap pass, and this one has a funnel number behind it where that one had only a stakeholder preference. Marcus Feld, legal counsel, flagged this trade explicitly rather than letting the roadmap absorb it silently. |
| What is the most likely way this fails? | Not the technology. The most likely failure is contractor attrition: a contractor who is asked to authorize a daily-capable background pull, on top of the one-time check they already accepted, may read that as surveillance rather than as the badge that gets them booked, and decline or churn. We have not tested the authorization language with contractors; Priya Nathan, trust and safety lead, owns a message test with 40 contractors before this goes past the design partner metros, and until that test runs this line is a judgment call, not a measured risk. |

Section 4 below carries the one open question this internal FAQ has not resolved: whether the existing onboarding authorization covers a recurring, same-day pull under the Fair Credit Reporting Act, or whether Wrenfield needs a renewed, separately dated authorization for this use. Marcus Feld's answer, filed as a judgment call rather than a citation, is that a single authorization can cover periodic reports if the disclosure states the report may be obtained periodically during the working relationship; Cobalt Screening's own onboarding language does not yet say that, so it needs updating before green-light regardless of which reading holds.

Whichever reading holds, the FCRA's adverse action sequence does not change: before Wrenfield suspends a contractor over a new disqualifying record, it must send a pre-adverse action notice with a copy of the report and a summary of consumer rights, hold for a reasonable review period (Wrenfield's current practice, unchanged by this launch, is five business days), and only then send a final adverse action notice if the suspension proceeds. Verified Same-Day's automatic reassignment does not shortcut this: reassignment happens immediately so the homeowner is protected, but the contractor's standing on the platform follows the existing adverse action process, not an instant ban.

## 4. Availability

| Field | Answer |
|---|---|
| Imagined launch window | Q1 2027, targeting 2027-03-02 |
| Launch scope | Denver, Portland, and Raleigh; plumbing, electrical, and HVAC categories only |
| Explicitly not at launch | Outdoor-only categories (lawn care, snow removal), metros outside the three named above, and any contractor who has not re-signed the periodic-pull authorization described in section 3 |

## Exit gate

This PR/FAQ is fit for a green-light review when:

- [x] The press release fits one page and leads with the customer's problem
- [x] The customer quote describes progress a real customer could plausibly claim
- [x] Every external FAQ answer is honest enough to publish as written
- [x] The internal FAQ contains at least two questions the authors would rather not answer. The "most likely way this fails" and the recurring-authorization question in section 3 are both open, not softened into reassurance.
- [ ] Every internal answer cites evidence or is marked a judgment call. Four of five internal FAQ rows meet this; the authorization-scope answer is Marcus Feld's judgment call pending outside counsel review, tracked as an open item rather than presented as settled.
- [x] A reviewer who read only this document could argue against the product, which means it gave them the material to. A reviewer could argue Verified Same-Day is funded by cutting a feature with equal roadmap standing, on a target abandonment improvement that is stated as a guess, against a contractor-attrition risk that has not been tested.

Signed: Devon Okafor, product manager, 2026-09-08. Not yet green-lit: legal sign-off on the recurring-authorization question and Priya Nathan's contractor message test are both outstanding, and this document records that rather than presenting the gate as cleared.
