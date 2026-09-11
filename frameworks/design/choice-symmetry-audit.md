---
layer: frameworks
stage: BUILD
gate: 4
feeds: ["templates/architecture/design-review-record.md", "templates/delivery/release-readiness.md", "templates/operate/compliance-impact-assessment.md"]
method: "knowledge/design/deceptive-design.md"
aliases: ["Choice Symmetry Audit", "choice-symmetry-audit"]
---
# Choice symmetry audit

Based on the symmetry principle as three regulators independently state it: the EU Digital Services Act's recital 67 and Article 25(3), California's CCPA regulation 11 CCR 7004(a)(2), and the FTC's 2025 Amazon consent order. The tagging columns draw on Harry Brignull's deceptive.design surface names and, under the Open Government Licence v3.0, the UK Competition and Markets Authority's online choice architecture mechanism groups (evidence class: platform convention). Explained here in this repository's own words.

## What it is for

For every consent, decline, opt-out, downgrade and cancel flow a release touches, this worksheet counts the effort a person spends going the business's way against the effort spent going their own way, in both directions, on the same screen. Steps, screens, channels and time are counted, not felt; a default state, a button's visual weight and a decline label's wording are checked against a fixed rule instead of a reviewer's taste. Any dimension where the decline path costs more than the accept path is flagged. The sheet never rules on whether a flagged flow is lawful. It produces a dated, jurisdiction-tagged evidence table that a named legal reviewer takes from there, per [Deceptive Design](../../knowledge/design/deceptive-design.md).

## Run it when

- A release changes, adds or touches a consent banner, a subscription or add-on flow, a downgrade path, an opt-out mechanism, or a cancellation flow, ahead of [Gate 4](../../os/STAGE-GATES.md).
- A compliance impact assessment has flagged a consent or request-method question and needs a step-by-step count instead of a description.
- A stakeholder defends a flow as "better conversion design" and the review needs a number, not an argument about intent.

**Skip it when:** the flow presents no choice the business profits from either way, such as a status page, a required legal disclosure with no alternative path, or a confirmation screen the person cannot act on. Counting steps on a screen with nothing to be asymmetric about produces a clean table and no finding worth reading.

## Inputs you need first

- A walkthrough of both paths, screenshotted or recorded, for the accept-direction action (subscribe, opt in, upgrade, accept) and the decline-direction action (cancel, opt out, downgrade, decline) of the same choice.
- The default state each path starts from: what is pre-checked, pre-selected or already active before the person does anything.
- Today's date against the regulation map in [Deceptive Design](../../knowledge/design/deceptive-design.md#regulation-map-as-of-2026-09-10-review-trigger-per-row), so the jurisdiction column and the "as of" line are not stale on the day this sheet is filed.
- A named legal reviewer to route flags to; this sheet cannot open with the routing line blank.

## The worksheet

### 1. Map the choice pairs

<!-- One row per choice a release touches. A choice pair is the accept-direction
     action and the decline-direction action of the same decision, not two
     unrelated flows. -->

| Pair ID | Choice | Accept-direction action | Decline-direction action | In this release because |
|---|---|---|---|---|
| C1 | | | | |

### 2. Effort grid per pair

<!-- Fill one grid per pair from step 1. Steps, screens and time are this
     worksheet's own operational counting method, applying the symmetry
     principle 11 CCR 7004(a)(2)(A) states in general terms: count from the
     person's first indication of intent to completion of the request, on
     each path separately. Channel is the medium the path runs on (in-app,
     web form, email, phone call, chat). Default state, visual prominence
     and wording neutrality are checked, not counted; record what is
     actually there. -->

| Dimension | Accept path | Decline path | Ratio (decline / accept) | Flag |
|---|---|---|---|---|
| Steps | | | | |
| Screens | | | | |
| Time (seconds) | | | | |
| Channel | | | n/a, see rule below | |
| Default state | | | n/a, see rule below | |
| Visual prominence (primary / secondary / link) | | | n/a, see rule below | |
| Wording neutrality (confirmshaming check) | | | n/a, see rule below | |

### 3. Ratio and flag rule

Three dimensions carry a number and a ratio; four carry a rule instead, because they are not counts.

**Numeric dimensions (steps, screens, time):**

`asymmetry ratio = decline-path effort ÷ accept-path effort`, computed separately per dimension.

- Ratio greater than 1 on any of the three: flag that dimension.
- Ratio of 1: no flag on that dimension.
- Accept-path effort of 0 (a pre-completed default) makes the ratio undefined; flag it directly rather than dividing by zero, and note it under default state as well, since a 0-step accept path is almost always a default-state finding wearing a step-count disguise.

**Channel:** flag whenever the decline path runs on a different, harder-to-reach channel than the accept path (signed up online, must cancel by phone or in person), regardless of what any ratio says. A channel switch is a flag on its own, per the CMA's choice-structure group and the pattern the FTC's Amazon order names directly.

**Default state:** flag when the default favors the business outcome, such as a box pre-checked to opt in, a subscription pre-selected on the higher tier, or a "continue" that silently carries forward a previous session's opt-in.

**Visual prominence:** flag when the accept path uses a stronger visual treatment (primary button) than the decline path (secondary button or a text link), on the same screen, for the same decision.

**Wording neutrality, the confirmshaming check:** flag any decline-path label that frames the choice as a loss, a mistake, or a lesser option rather than a neutral alternative. A neutral pair reads "Accept" and "Decline," or "Yes" and "No." A pair such as "Yes, keep my discount" against "No, I don't want to save money" fails this check regardless of what the two buttons cost in steps.

**Effect, not intent.** Score every dimension against what the interface does, never against what the team meant it to do. A "reduce accidental cancellation" rationale and a flow built to suppress cancellation can be the identical screen on this grid, and the grid does not have a column for intent.

### 4. Tag each flag

<!-- One row per flagged dimension from step 3, not one row per pair. A pair
     can produce more than one flag, and each flag is tagged on its own. -->

| Flag ID | Pair ID | Dimension flagged | Surface type (deceptive.design, name only) | CMA mechanism group | FTC harm group | Jurisdiction | As of |
|---|---|---|---|---|---|---|---|
| F1 | | | | | | EU platform / California / UK / US FTC | 2026-09-10 |

Surface type, mechanism group and harm group are the three descriptive lenses in [Deceptive Design](../../knowledge/design/deceptive-design.md#four-lenses); tag with the name only here; the card carries the definition. Jurisdiction records which instrument's scope the flow actually falls inside, not every instrument in the regulation map: a consent banner on a non-platform product cites no DSA row, and a request-method flow outside California cites no CCPA row. Leave a jurisdiction cell blank, with a one-line reason, rather than tag a flow against an instrument whose scope does not reach it.

### 5. Route the finding, rule on nothing

This sheet stops at a tagged, dated table. It does not decide whether a flagged flow is lawful, and no cell on this sheet is a legal determination.

- Copy the flag table into the design review record's live-build section as evidence for that review.
- Open a legal-review line, named by role, on the [compliance impact assessment](../../templates/operate/compliance-impact-assessment.md) for any flag tagged against a jurisdiction, and on [release readiness](../../templates/delivery/release-readiness.md)'s choice-symmetry line before a GO, NO-GO or CONDITIONAL GO decision.
- Confirm with counsel before a flag is treated as settled either way. This sheet supplies evidence a lawyer can use; it never substitutes for what a lawyer decides.

## Reading the result

A pair with every dimension at ratio 1, a neutral default, matched prominence and neutral wording clears with no flag and needs no legal-review line. A pair with one flag is a design fix first: most single flags (a screen extra, a weaker button) are cheaper to fix in the flow than to defend later. A pair with flags across three or more dimensions, or a channel switch on top of any ratio flag, is the pattern the Amazon order and 11 CCR 7004(a)(2)(A) both describe directly, and it goes to legal review regardless of how small any single ratio looks; asymmetry compounds across dimensions the way it compounds against the person living through the flow. A flag count near zero across every pair in a release is worth a second look at whether the audit actually walked the decline path to completion, rather than trusting that a clean sheet reflects a clean product; the trap below names the most common way a sheet comes back clean while the product does not.

## ILLUSTRATIVE example

Tandem, the invented freelance-contract tool from [knowledge/jobs-to-be-done.md](../../knowledge/jobs-to-be-done.md). Run at BUILD before Gate 4, read at Gate 5 on the release-readiness line. Choice pair: upgrading to the Pro add-on against downgrading off it.

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
| F3 | C1 | Visual prominence | Visual interference | Choice structure | Obscures privacy or account choices | | 2026-09-10 |
| F4 | C1 | Wording neutrality | Confirmshaming | Choice information | Induces false beliefs | UK | 2026-09-10 |

Reading: four flags on one pair, spanning every numeric dimension plus a channel switch, a prominence mismatch and a confirmshaming label. This is the compounding case the Reading section above names: no single flag decides the outcome, but F1 and F2 together are close to the shape the FTC's Amazon order addresses directly (upgrade by app, downgrade by an assisted channel, with wording that frames the downgrade as a loss). Routed: the table goes into Tandem's design review record live-build section, a legal-review line opens on the compliance impact assessment tagged California and US FTC, and release readiness carries a NOT MET on its choice-symmetry line until counsel reviews F1 through F4. F3's jurisdiction cell is blank: Tandem is a freelance-contract tool, not a platform, so the DSA's platform scope does not reach this flow.

## The trap

Fixing the button color while the cancel path stays three screens longer. A team reads this sheet's visual-prominence flag, gives the decline button equal weight, and reports the flow fixed, while the step count, the screen count and the channel switch from the same pair are still sitting at their original ratios. Visual prominence is one of seven rows on the grid, not the whole grid; a review that closes a flag by re-running only the row that was easiest to change, without re-running the ratio arithmetic on every other row for the same pair, produces a flow that looks fixed in a screenshot and still costs three extra screens to walk.

The second version of the same trap is malicious compliance in the other direction: a team reads "decline must cost no more than accept" and slows the accept path down to match, rather than speeding the decline path up. The ratio hits 1 either way, and the sheet cannot tell the two apart on its own; read the absolute effort on both sides, not only the ratio between them, before calling a pair clear.

## Feeds

- [Design review record](../../templates/architecture/design-review-record.md): the flag table lands in the live-build section as review evidence
- [Release readiness](../../templates/delivery/release-readiness.md): the choice-symmetry line, MET only when every flag on a release-touched pair has a routed legal-review answer
- [Compliance impact assessment](../../templates/operate/compliance-impact-assessment.md): a legal-review line, named by role, for every jurisdiction-tagged flag
- BUILD, feeding [Gate 4: Acceptance criteria met](../../os/STAGE-GATES.md)
- Worked fill: [Ledgerline choice symmetry audit example](../../examples/ledgerline-choice-symmetry-audit.md)
- Method background: [Deceptive Design](../../knowledge/design/deceptive-design.md)
