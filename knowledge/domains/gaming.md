---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Gaming"]
---
# Gaming

A game is a retention machine: a core loop players repeat because it feels good, wrapped in a meta loop that gives the repetition a direction. Monetization only works downstream of those loops, and the fastest way to kill both is to let the monetization design reach back and bend them. This domain also carries two gates most software never meets: platform certification, where a console or store holder can fail your build for reasons in a checklist you must read, and a shifting body of law around paid randomized rewards.

**Real-money play is a different domain:** if a player can stake money on a sporting or random outcome for a cash prize (a sportsbook, online casino, daily fantasy, sweepstakes casino or lottery), read [Sports betting and iGaming](sports-betting-igaming.md) instead of this card. There, a licence per jurisdiction, geolocation, self-exclusion and responsible-gambling duties decide whether the product may operate at all, and D1/D7/D30 retention is the wrong headline metric. Paid loot boxes stay on this card because no cash prize leaves the game; where items can be cashed out through a market, read both cards.

## Questions a PM must ask

1. What is the core loop in one sentence, and what does session data say about where players fall out of it? A pitch that needs three sentences for the loop usually has no loop.
2. What do D1, D7, and D30 retention look like against genre benchmarks, and which of the three is the design actually weak at? Day-one loss is onboarding; day-thirty loss is the meta loop.
3. Where does revenue concentrate across the paying population? When a small share of payers carries the business, every economy change is a high-stakes conversation with people you can name.
4. Does any purchasable item have a randomized outcome? If yes, which markets treat that as gambling, what disclosure of odds is required where, and has counsel looked at each launch market? Belgium has treated paid loot boxes as gambling; several markets require published drop rates; the map keeps moving, so verify per market at each launch.
5. Who under 18 will play this, and what does that do to monetization design, chat, ratings (ESRB, PEGI), and data collection under COPPA and its equivalents?
6. What is the certification plan? Console cert and store review are dated, failable gates with resubmission queues; a launch date that ignores the resubmission case is a wish.
7. What does the update cadence cost? Live-ops games are content treadmills; commit to a cadence the team can hold for years, not for the launch quarter.
8. Which monetization mechanics are we refusing on purpose? Writing the refusals down is the only durable defense against the quarter someone proposes them.

## Gatekeepers

- **Platform holders.** Sony, Microsoft, and Nintendo certification, plus Apple and Google review, each with technical requirements, content rules, and payment mandates. Cert failure is a schedule event; plan the resubmission loop.
- **Ratings boards.** ESRB, PEGI, and national equivalents; the rating constrains marketing, store placement, and in some markets what mechanics are legal to include.
- **Gambling and consumer regulators.** Loot-box and paid-random-reward law differs by country and changes; child-protection rules (COPPA and equivalents) bind chat, ads, and data for younger audiences.
- **Payment and store policy.** Store payment rules, refund policies, and regional pricing rules shape the economy design more than most economy designers admit.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| D1/D7/D30 retention | Whether the loops hold at each horizon | Only meaningful against genre and platform baselines; a raw number is noise |
| ARPDAU | Revenue per daily active, the live-ops heartbeat | Spikes on sales events; trend it against the event calendar |
| Conversion to payer | Whether the free experience sells the paid one | Pushing it up with friction poisons the retention that funds everything |
| Payer concentration | Business fragility in a few wallets | An average revenue per payer hides the shape entirely |
| Session length and frequency | Loop health, split by player age cohort | More is not better past the point where it signals obligation, not joy |
| Update-to-update retention delta | Whether live-ops content earns its cost | Confounded by seasonality; compare like weeks |

## Reading

- **The Art of Game Design**, Jesse Schell (2008). The lens method: dozens of small, pointed questions to interrogate a design from the player's side. The habit it builds, examining the same feature through many single-question passes, is the closest thing this domain has to a review discipline.
- **Free-to-Play: Making Money From Games You Give Away**, Will Luton (2013). The economy-design canon in its own words: monetization as a service to committed players rather than a toll on new ones, and the arithmetic connecting retention curves to sustainable revenue.

**Conductor overlay:** this domain sharpens DELIVER-8 (the launch sequence must contain the cert and resubmission path), OPERATE-7 (the loop behind the metric is literal here), and OPERATE-8 (the counter-metric guards player wellbeing and payer fairness while revenue climbs).

**Templates this bends:** [release-readiness](../../templates/delivery/release-readiness.md) (cert passes become checklist rows with dates) and [growth-plan](../../templates/planning/growth-plan.md) (the input-metric bet is a loop change, and the counter-metric line is mandatory in spirit).

**Filled in this repo:** [domain-gaming-release-readiness.md](../../examples/domain-gaming-release-readiness.md) fills the [release-readiness](../../templates/delivery/release-readiness.md) template directly for this domain, for Emberfall Tactics: the certification checkbox and known-issue row (Apple accepted the build, Google flagged the storefront odds disclosure, resubmission, launch held), rating certificates (IARC, PEGI, ESRB), a per-market loot-box posture with the crate disabled where paid random rewards are treated as gambling, the under-13 posture, payer-concentration telemetry, and a server-side flag to roll back crate odds, decided GO WITH CONDITIONS. For the growth-plan template, [ledgerline-growth-plan.md](../../examples/ledgerline-growth-plan.md) remains the nearest reading, for linking a metrics review and an OKR sheet to a signed target, though its loop is a B2B add-on's activation funnel, not a session-retention core loop.

**Worked example (ILLUSTRATIVE):** a filled release-readiness pass for a fictional mobile game, "Emberfall Tactics," following the [release-readiness](../../templates/delivery/release-readiness.md) shape used in [harbourgate-release-readiness.md](../../examples/harbourgate-release-readiness.md), whose own certification-style check is a checkbox under section 1 or 2, not a per-row status column: the document's decision is GO WITH CONDITIONS, a single document-level verdict, and the failed check becomes a named row in section 3's known-issues table rather than its own "status."

**Section 1 or 2 checkbox:** "- [ ] Platform certification: build 4.2.1 passes Apple App Store review and Google Play policy review, including the drop-rate disclosure for the Tactician Crate paid loot mechanic. CONDITIONAL, see known issue #1."

**Section 3, known issues:**

| # | Issue | Severity | Why it is acceptable to ship | Fix owner | Fix date |
|---|---|---|---|---|---|
| 1 | Apple accepted the build 2026-11-03; Google's review flagged the Tactician Crate's odds disclosure as not visible on the storefront listing pre-purchase (the in-app screen already discloses it) | medium | The in-app disclosure is live before any purchase completes, so no player buys the crate without seeing its odds; only the storefront-listing copy is missing the same text | Noor Bashir, Release Manager | Resubmission queued 2026-11-10; launch date held 2026-11-14 pending that pass, with a same-week resubmission slot reserved |

A generic release-readiness row checks "app store approval, done"; this one names the specific policy clause that failed (pre-purchase odds disclosure on the storefront listing, not the in-app one, which already discloses it) and books the resubmission queue's own lead time against the launch date, because in this sector a cert failure is a dated, failable gate with its own retry cost, not a one-time checkbox, and the template's own vocabulary for that is a checkbox plus a known-issues row, not an invented per-row "CONDITIONAL GO."
