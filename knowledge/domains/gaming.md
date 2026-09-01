# Gaming

A game is a retention machine: a core loop players repeat because it feels good, wrapped in a meta loop that gives the repetition a direction. Monetization only works downstream of those loops, and the fastest way to kill both is to let the monetization design reach back and bend them. This domain also carries two gates most software never meets: platform certification, where a console or store holder can fail your build for reasons in a checklist you must read, and a shifting body of law around paid randomized rewards.

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
