# Choice Symmetry Audit: Ledgerline Expense Copilot, add-on activate versus cancel, and the offer-page wording swap

Fills [frameworks/design/choice-symmetry-audit.md](../frameworks/design/choice-symmetry-audit.md). Everything here is ILLUSTRATIVE: Ledgerline is a fictional mid-market software company, the Expense Copilot is the fictional product used across this repository, and every person, screen, count and date is fiction built to show the worksheet rather than to describe any real product. It audits the add-on's per-seat activate versus cancel path (N46's activation, shipped 2026-11-19 as LEDGERLINE-S1), and separately reads the 2026-12-21 offer-page wording swap (N94) that D6 made on the pivot date. It takes no figure the [journey data sheet](ledgerline-journey.md) or the [design sheet](ledgerline-design-sheet.md) does not carry, and shows the arithmetic for every derived count. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Date:** 2026-12-23 · **Run against:** the per-seat activation shipped 2026-11-19 (LEDGERLINE-S1), live until D6 killed the price on 2026-12-21, and the offer-page wording N94 switched live the same day · **Legal reviewer to route flags to:** the legal lead (by role) · **As of:** 2026-09-10 review trigger, per [Deceptive Design](../knowledge/design/deceptive-design.md)

## What it is for

This worksheet counts the effort an admin spends activating the per-seat add-on against the effort spent cancelling it, on the same screen, so the design review carries a dated, jurisdiction-tagged table instead of a reviewer's impression that the flow "feels fine." It then reads a second, different kind of change separately: the 2026-12-21 offer-page wording swap that followed D6, which removed the price from the page entirely rather than changing which path costs more.

## Run it when

- A release touches a subscribe, cancel, downgrade or migration-offer flow ahead of [Gate 4](../os/STAGE-GATES.md), as the per-seat activation does here.
- A pricing decision changes what an offer page shows, and the review needs to know whether the change reads as a choice-symmetry defect or as something else entirely (an offer withdrawn, not re-weighted).
- A stakeholder defends a subscribe or exit screen as good conversion design and the review needs a number.

## Inputs you need first

- A walkthrough of both paths for C1 (activate versus cancel), screenshotted to completion.
- The default state each path starts from: no add-on active before the admin acts, on both sides of C1.
- Today's date against the regulation map in [Deceptive Design](../knowledge/design/deceptive-design.md), carried here as the 2026-09-10 review trigger.
- A named legal reviewer to route flags to: the legal lead, by role.

## The worksheet

### 1. Map the choice pair

| Pair ID | Choice | Accept-direction action | Decline-direction action | In this release because |
|---|---|---|---|---|
| C1 | Turn the copilot add-on on for the account, at the per-seat price | Activate: open Expenses settings, review the per-seat charge screen, confirm (LEDGERLINE-S1) | Cancel the same activation: open Expenses settings, open the add-on panel, confirm cancellation | N46's per-seat activation shipped 2026-11-19 and ran until D6 killed the price 2026-12-21; both paths were live for that whole window |

### 2. Effort grid, pair C1 (add-on: activate vs. cancel)

Steps and screens are counted from the admin's first indication of intent to completion of the request, on each path separately, the way California's CCPA regulation 11 CCR 7004(a)(2)(A) counts them (see the [Deceptive Design card](../knowledge/design/deceptive-design.md)).

| Dimension | Accept path | Decline path | Ratio (decline / accept) | Flag |
|---|---|---|---|---|
| Steps | 3 | 3 | 3 / 3 = 1.0 | No |
| Channel | in-app (Expenses settings) | in-app (Expenses settings) | same | No |
| Default state | no add-on active before the admin acts | no add-on active before the admin acts | n/a, see rule below | No |
| Retention prompt or required reason on the way out | none | none | n/a, see rule below | No |

Arithmetic: steps ratio 3 ÷ 3 = 1.0, no flag. Both paths open Expenses settings first; the accept path then reviews the per-seat charge screen and confirms, and the decline path opens the add-on panel and confirms cancellation, each three steps to completion. Channel is in-app on both sides. Neither path starts from a business-favoring default, and the cancel path adds no retention prompt and no required reason field before completing, so no dimension flags on this pair.

### 3. The offer-page wording swap, N94 (a separate reading, not part of C1's grid)

This is not a second choice pair with its own accept and decline paths; it is a single page whose content changed on the pivot date, and the worksheet's ratio arithmetic does not apply to it the way it applies to C1.

| | Before 2026-12-21 | After 2026-12-21 (N94) |
|---|---|---|
| What the page shows | The per-seat price and the $204-a-month median figure for a 34-seat account (N47), shown on the same screen as the accept button | "Copilot pricing is under review; existing activations are unchanged." No price shown |
| Steps to see the price | 1 | 0, because no price is shown |
| Steps to accept | 1 | 0, because there is no accept button for a new price |

Reading: this is not an asymmetry between accepting and declining a single offer on one date; it is a difference between the two dates. An admin visiting before 2026-12-21 could see a price and act on it in one step each way. An admin visiting after cannot see any price at all. The worksheet's ratio and flag rules score effort between two paths available at the same time, and there is no such pair here after the swap: there is nothing to accept. This sheet logs it as a withdrawn-offer state, not a choice-symmetry defect, and raises no flag.

### 4. Tag each flag

No flag fired on C1, and the N94 reading in section 3 is not a flaggable pair, so this section has no rows to tag for this release. The table structure is kept here, empty, so a later release that does touch this flow with an actual asymmetry has the same columns to fill.

| Flag ID | Pair ID | Dimension flagged | Surface type (deceptive.design, name only) | CMA mechanism group | FTC harm group | Jurisdiction | As of |
|---|---|---|---|---|---|---|---|
| (none this release) | | | | | | | 2026-09-10 |

### 5. Route the finding, rule on nothing

This sheet stops at a tagged, dated table, even when the table is empty.

- Section 2's clean grid and section 3's withdrawn-offer reading are copied into the design review record's live-build section as evidence that this release's activate and cancel paths were checked and that the offer-page change was read against the worksheet before anyone called it a dark pattern.
- [Release readiness](../templates/delivery/release-readiness.md)'s choice-symmetry line is MET for this release: C1 carries no flag, and section 3 explains why the N94 change carries none either.
- Confirm with counsel before a future flag is treated as settled either way; a clean result this release does not exempt the next release that touches this flow from running the grid again.

## Reading the result

C1 is symmetric at 3 steps each with no added friction on exit, which is the finding the audit's own arithmetic is built to surface when a product adds a confirmation step or a retention offer only on the way out; here it did not. The offer-page wording swap is a different kind of event: it is not a product adding friction to a decline path, it is a price disappearing from a page entirely on the date it was killed. Reading that as a choice-symmetry defect would misapply the worksheet; reading it as a withdrawn-offer state is what section 3 is for.

## ILLUSTRATIVE example

Invented, for Tandem, a fictional freelance-contract tool that does not otherwise appear in this repository. Choice pair: upgrading to the Pro add-on against downgrading off it.

**Effort grid, pair C1 (Pro add-on: upgrade vs. downgrade):**

| Dimension | Accept path (upgrade) | Decline path (downgrade) | Ratio | Flag |
|---|---|---|---|---|
| Steps | 2 | 6 | 3.0 | Yes |
| Screens | 1 | 3 | 3.0 | Yes |
| Time (seconds) | 25 | 210 | 8.4 | Yes |
| Channel | in-app | phone call to support | different | Yes |
| Default state | none pre-selected | none pre-selected | | No |
| Visual prominence | primary button, top of screen | text link, bottom of settings page | | Yes |
| Wording neutrality | "Upgrade to Pro" | "Are you sure? You'll lose your saved templates." | | Yes |

**Tag table:**

| Flag ID | Pair ID | Dimension flagged | Surface type | CMA mechanism group | FTC harm group | Jurisdiction | As of |
|---|---|---|---|---|---|---|---|
| F1 | C1 | Steps, screens, time | Hard to cancel | Choice structure | Unauthorized charges | California | 2026-09-10 |
| F2 | C1 | Channel | Hard to cancel | Choice structure | Unauthorized charges | US FTC | 2026-09-10 |
| F3 | C1 | Visual prominence | Visual interference | Choice structure | Obscures privacy or account choices | EU platform | 2026-09-10 |
| F4 | C1 | Wording neutrality | Confirmshaming | Choice information | Induces false beliefs | UK | 2026-09-10 |

Reading: four flags on one pair, spanning every numeric dimension plus a channel switch, a prominence mismatch and a confirmshaming label. This is the compounding case a review has to catch: no single flag decides the outcome, but F1 and F2 together are close to the shape the FTC's Amazon order addresses directly. Routed: the table goes into Tandem's design review record live-build section, a legal-review line opens on the compliance impact assessment tagged California and US FTC, and release readiness carries a NOT MET on its choice-symmetry line until counsel reviews F1 through F4. Tandem's result is the contrast this document's own C1 does not show: a real asymmetry, not a clean grid.

## The trap

The trap on a clean result like C1's is treating "no flag" as "nothing to check next time"; a later release that adds a retention step to the cancel path would need the same grid re-run, not a reference back to this pass. The trap on the N94 reading runs the other way: calling a withdrawn offer a choice-symmetry defect because a price used to be visible and now is not, when the worksheet's ratio arithmetic has nothing to compare it against once there is no accept button on either date's page. Reading a pivot's pricing removal as a dark pattern would send legal review chasing a flag this sheet's own arithmetic does not support; reading a real asymmetry as a pivot artifact, in a release that does have one, makes the opposite mistake.

## Feeds

- [Design review record](../templates/architecture/design-review-record.md): section 2's grid and section 3's reading land in the live-build section as review evidence.
- [Release readiness](../templates/delivery/release-readiness.md): the choice-symmetry line, MET for this release; a future release touching C1 or the offer page reruns the grid.
- [Compliance impact assessment](../templates/operate/compliance-impact-assessment.md): no legal-review line opens this release, since no flag fired.
- BUILD, feeding [Gate 4: Acceptance criteria met](../os/STAGE-GATES.md), for the C1 activate-versus-cancel grid; DELIVER, feeding [Gate 5](../os/STAGE-GATES.md), for the offer-page wording reading, since N94 shipped as part of the GTM-facing pivot messaging D6 set in motion.
- Method background: [Deceptive Design](../knowledge/design/deceptive-design.md); the blank worksheet at `frameworks/design/choice-symmetry-audit.md`.
- Data source: the [journey data sheet](ledgerline-journey.md), rows N46, N47, N94, D6; the [design sheet](ledgerline-design-sheet.md), rows LD24 to LD28.
