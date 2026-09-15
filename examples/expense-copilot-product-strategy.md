# Product Strategy: Expense Copilot

Fills [templates/planning/product-strategy.md](../templates/planning/product-strategy.md). Everything here is invented: Ledgerline is the fictional mid-market software company used across this repository, and this strategy sits between the [vision](expense-copilot-vision.md) and the [roadmap](expense-copilot-roadmap.md) in the internal-v1 chain the [Expense Copilot journey](expense-copilot-journey.md) indexes. Every number, date and id below is ILLUSTRATIVE, carried from that journey's own data sheet (V4, V8, V17) and from [ledgerline-journey.md](ledgerline-journey.md)'s N1 to N7, so it can be checked against the vision this strategy follows and the PRD it is drafted alongside. It may also be read beside [ledgerline-strategy-kernel.md](ledgerline-strategy-kernel.md), the framework sheet written the day before this strategy, and [ledgerline-jtbd-job-map.md](ledgerline-jtbd-job-map.md), the job map built from the same discovery interviews. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Period:** DEFINE through the internal build's go-live target, 2026-08-13 to 2026-10-12 · **Last updated:** 2026-08-21

## 1. Strategic context: the diagnosis

- **The situation:** Ledgerline's own filers file about 800 reports a month, 9,600 a year (N2), against a first-submission approval baseline of 62% (N3). Reviewers spend about 30 hours, about $1,800, a month on mechanical checks instead of judgment (N7). [ledgerline-strategy-kernel.md](ledgerline-strategy-kernel.md)'s own diagnosis, written the day before this strategy, reaches the same reading from the same evidence: filers re-type what the receipt already says, and discovery's interviews named that as the worst part of filing without being asked.
- **The crux:** value gets lost in translation, not in effort. What a receipt already states, merchant, date, amount, currency, gets re-typed by a filer and re-checked by a reviewer, and both passes cost the time the business case already prices (N7, N14, N15). The fix is not a faster form; a faster path to the same re-typed, sometimes-wrong data would cost less time and still bounce at the same rate.
- **What changed recently:** no strategy existed for Ledgerline's own filing process before this quarter. The trigger was the travel-agency switch [expense-copilot-discovery.md](expense-copilot-discovery.md)'s own Trigger section names, which is what turned an unscoped "build a better form" into a bounded, gated build with a sponsor behind it: Daniel Okafor decided GO on 2026-08-14 (D-1), the day discovery closed.

## 1b. The guiding policy

**In one sentence:** extract only what the model can support and show its work, never guess a field to make a draft look more finished than it is, and never trade first-submission approval for filing speed.

| Test | Answer |
|---|---|
| The opposite policy, written out | Autofill every field with the model's best guess, even a low-confidence one, so every draft looks complete and files faster. A plausible build, and the one the extraction pipeline is designed to refuse: a field the model cannot read stays blank and flagged rather than filled |
| What this policy refuses | A field that looks done when it was actually guessed, and any shortcut that trades a filer's trust for a faster-looking draft. This is the same logic the PRD's own out-of-scope list applies to auto-submission: the filer stays the author, not a reviewer of the system's guesses |
| Who has to change what they do on Monday | Priya Nair's build leaves a field blank and flagged whenever the model cannot support an answer, rather than filling it; Maya Chen holds the v1 scope to one receipt per item rather than the multi-receipt capture filers will ask for, per the functional scope this PRD is drafting in parallel |

## 2. Where to play: the bets

| Bet | What we choose | What we thereby refuse | Evidence for the bet |
|---|---|---|---|
| 1 | The whole of Ledgerline's own filer base, about 900 employees (N1), as one internal rollout rather than a single pilot team | A phased pilot-team-only rollout, and any customer-facing version; customers are a separate, later question [ledgerline-journey.md](ledgerline-journey.md) takes up after go-live | Discovery interviewed filers and reviewers across the company and found the pain broadly shared, not confined to one team ([expense-copilot-discovery.md](expense-copilot-discovery.md) Pain section); the business case is funded on internal time savings alone |
| 2 | Extraction accuracy and first-submission approval as the v1 bet, ahead of a learning category-mapping loop | A mapping suggestion that learns from admin corrections in v1; corrections are logged and versioned but not fed back into suggestions yet | The needed review step for a feedback loop has no owner and no design before the launch window; shipping an unreviewed loop is how a wrong mapping becomes policy |
| 3 | A receipt-reading assistant with a narrow model boundary: ingest, extract, suggest, assemble a draft | Building policy-authoring tools, payment rails, or a corporate-card feed integration ourselves | Everything outside this boundary is already out of the PRD's scope: card-feed reconciliation, mileage, per-diem rules, and filing on another person's behalf all sit outside what a receipt-reading assistant needs to do |

## 3. How we win: differentiation

- **Our edge:** the policy line shown beside every suggested category, so a bounce, on the rare report that still gets one, becomes a conversation with a rule the filer can read rather than a guess neither of them can check.
- **Why it holds:** this is an internal tool, not a market position, so the edge is trust, not share. A field the system never invents earns a filer's confidence that a blind autofill would not; that confidence is what turns voluntary adoption into something other than a mandate. The mechanism is the never-invent rule itself, not speed: a build that only shipped faster typing would not touch the category-mismatch half of the 62% baseline (N3) at all.
- **The named alternative it beats:** the current Ledgerline expense form, typed by hand, and the finance lead's own first instinct, a faster version of the same form, both named in [expense-copilot-discovery.md](expense-copilot-discovery.md)'s Trigger section.

## 4. Sequencing

| Order | Move | Precondition (evidence, not a date) | Feeds |
|---|---|---|---|
| 1 | Prove the receipt-extraction pipeline will not invent a field it cannot read | ADR-0001 decides the pipeline shape; the eval work behind it is scoped as an ILLUSTRATIVE threshold in v1, revisited after four weeks of live data, an accepted gap rather than a resolved one | objective 1, first-submission approval from 62% toward 80% (N3, N4) |
| 2 | Ship the draft-and-edit surface with confidence flags once extraction is trusted directionally | Order 1 shipped and reviewed | objective 1 and objective 2, filing time from 25 minutes toward under 10 (N5) |
| 3 | Log admin corrections to category mappings without feeding them back into suggestions yet | Orders 1 and 2 shipped; the review step a feedback loop needs still has no owner | objective 3, voluntary adoption, since a wrong mapping repeatedly corrected in the open is what keeps a filer's trust rather than a silent relearning loop nobody reviewed |

## 5. Success metrics

| Metric | Baseline | Target for the period | Tree link |
|---|---|---|---|
| First-submission approval, copilot-drafted reports | 62% (N3) | 80% (N4) | candidate north star, [vision](expense-copilot-vision.md) section 4 |
| Median filing time, five-receipt report | 25 minutes (N5) | under 10 minutes (N5) | objective 2, directional per the discovery document's own timed sessions |
| Eligible reports using the draft flow | 0% before launch | half of eligible reports within two months, the same signal [expense-copilot-discovery.md](expense-copilot-discovery.md) already sets | objective 3, voluntary adoption without a mandate |

## 6. Key risks

| Risk to the strategy | Early signal we would see | Response if seen | Owner |
|---|---|---|---|
| Extraction quality on crumpled or foreign-language receipts is unproven, a risk discovery already carried forward | Eval scores fall below the accepted threshold on non-standard receipts once the eval spec runs | Keep the field blank and flagged rather than guess, per the guiding policy; revisit scope before Gate 3 | Priya Nair |
| The model vendor's training-data and retention terms stay open past DEFINE | No signed clause by the time DESIGN's dependency work starts | The legal lead closes the clause before Gate 5; tracked into DESIGN as a dependency | the legal lead |
| Voluntary adoption undershoots because checking a draft still feels like more work than typing from scratch | Draft-flow usage tracks well under half of eligible reports at the two-month check | Revisit the edit surface and the confidence-flag design before broadening beyond this rollout | Maya Chen |

## How this strategy fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Goals with no diagnosis | Targets and initiatives, and no statement of what is actually in the way | Section 1 names the crux as value lost in translation, not effort; every bet in section 2 removes a piece of that specific translation cost |
| Nothing is refused | Everything is strategic, and no option was given up | Each bet in section 2 names what it refuses by name: a pilot-only rollout, a learning mapping loop in v1, and building payment or card-feed tools ourselves |
| Bets untraceable to the policy | Initiatives in the plan that no stated principle would have produced | Bet 2 and the sequencing in section 4 both trace directly to the guiding policy's never-invent rule; a bet for a faster form with no accuracy story would not derive from it |
| Copying a competitor | The plan mirrors a rival's shipping log, feature for feature | This is an internal build with no competitor to mirror; section 3 names the alternative it beats as Ledgerline's own current form and its own first instinct, not a rival's product |
| Survives any evidence | Unchanged after a win, a loss and a market shift | Section 6 names the early signal for each risk and the response it triggers, including a scope revisit before Gate 3 if extraction quality does not hold |

## Exit gate

This strategy is fit to operate on when:

- [x] The diagnosis names a crux, and every situational claim links to evidence: the crux is value lost in translation; section 1 cites N2, N3, N7, N14, N15 and the strategy kernel
- [x] The guiding policy is one sentence that refuses something, and its opposite is a choice a sane rival could make: the opposite, autofill every field, is exactly what the extraction pipeline exists to refuse, a live alternative rather than a straw man
- [x] There are at most three bets, and each names what it refuses: three, in section 2, each with a refused column
- [x] The differentiation names a mechanism and a real alternative, not an adjective: the never-invent rule as mechanism; the current form and the finance lead's own first instinct as the named alternatives
- [x] Sequencing gates later bets on evidence conditions, not calendar quarters: three orders in section 4, each gated on the order before it shipping and being reviewed, not on a date
- [x] Every success metric traces to the north star tree: all three rows in section 5 trace to the vision's candidate north star or to one of the PRD's three objectives
- [x] Each risk has an early signal someone is actually watching: three risks in section 6, each with a named owner

Approved at Gate 2 by the product owner: Maya Chen, 2026-08-28
Approved at Gate 2 by the business sponsor: Daniel Okafor, 2026-08-28
