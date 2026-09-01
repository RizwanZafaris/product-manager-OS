# Consumer social

A social product's value is other people, which produces the domain's two permanent facts. First, growth is a designed loop, not a funnel: users create content or invitations that pull in the next users, and the product team owns the loop's arithmetic. Second, the same openness that powers the loop imports every form of human misbehavior, so trust and safety is a standing cost of doing business, not a feature to schedule. The products that fail here usually optimized the loop and deferred the misbehavior.

## Questions a PM must ask

1. What is the growth loop, drawn as a circle with a number on each arc? If invitations, shares, or content exposure do not lead back to new contributing users, you have a funnel with social features, and it will price like one.
2. What does the network look like at zero? Every social product faces the cold start: the first user sees an empty room. What is the single-player value, the seeded community, or the imported graph that survives day one?
3. What is the moderation model, and what does it cost per thousand pieces of content at ten times today's volume? Machine-first with human escalation is the standard answer; the honest question is what the escalation queue does under growth.
4. Which abuse cases has the team written down before launch: harassment, spam, CSAM, scams, coordinated manipulation? The list you did not write is the incident you will handle live.
5. Will anyone under 13 use this, and anyone under 18? COPPA governs the first; age-assurance and design codes increasingly govern the second; both bind data, defaults, and recommender behavior.
6. Which legal regime carries our obligations in each market: the DSA in the EU (notice-and-action, transparency, systemic-risk duties at scale), Section 230's shield and its limits in the US, the UK Online Safety Act? The answers differ enough to shape the feature, not just the policy page.
7. What is the counter-metric to engagement? A recommender judged on time spent alone will find the content that maximizes it, and that discovery has a public record now.
8. Who are the power creators, and what happens if the top slice leaves? Content supply concentrates the way payers do in gaming; supply-side churn is a metric.

## Gatekeepers

- **App stores.** Apple and Google require working UGC moderation, reporting, and blocking mechanisms as a condition of listing; an unmoderated social app is removable, not just criticized.
- **Platform regulators.** The EU DSA (with heavier duties for very large platforms), the UK Online Safety Act, and equivalents impose notice, transparency, and risk-assessment obligations with real deadlines.
- **Child-protection regimes.** COPPA for under-13 data in the US, age-appropriate design codes elsewhere; they reach into defaults, notifications, and recommendation logic for minors.
- **Ad platforms and payment rails**, if monetized: ad policy and brand-safety demands feed straight back into content policy.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| DAU/MAU ratio | Habit strength: how much of the base returns daily | Notification pressure inflates it while quietly burning goodwill |
| Retention curve shape by cohort | Whether the product finds a durable base | Only the flattening matters; early height is marketing |
| K-factor / invite loop conversion | Whether growth compounds without paid spend | Above-one k rarely lasts; treat it as a phase, not a property |
| Contribution rate | Share of users who create, not just consume | Falling contribution with rising consumption predicts a slow emptying |
| Time-to-report and moderation queue latency | Whether safety keeps pace with growth | Averages hide the worst-content tail, which is the tail that ends up in the press |
| Counter-metric (regret, blocks, reports per session) | What engagement is costing users | Nobody instruments it unless the PM insists; insist |

## Reading

- **The Cold Start Problem**, Andrew Chen (2021). Network effects as a lifecycle: the atomic network you must fill first, the tipping point, and the less-discussed ceiling where the same network effects reverse into context collapse and spam. The book's discipline, name the smallest network that is self-sustaining, is this domain's beachhead rule.
- **Hooked**, Nir Eyal (2014). The trigger-action-reward-investment loop that most engagement design quietly runs on. Read it for the mechanism and keep the ethics question open on purpose: the same loop builds habits users thank you for and habits they resent, and the counter-metric row above is where that difference shows up.

**Conductor overlay:** this domain sharpens DISCOVER-5 (conversation count: talk to lurkers and creators separately), DESIGN-6 (seeing it misbehave means abuse rehearsal, not just error states), OPERATE-7 (the loop behind the metric is the growth loop itself), and OPERATE-8 (the counter-metric is mandatory in spirit).

**Templates this bends:** [failure-scenarios](../../templates/delivery/failure-scenarios.md) (abuse and moderation-overload scenarios join the outage scenarios) and [compliance-impact-assessment](../../templates/operate/compliance-impact-assessment.md) (minors, DSA duties, and data-of-children rows).
