---
layer: knowledge
stage: ALL STAGES
gate: 1
feeds: []
method: ""
aliases: ["Streaming and OTT", "streaming-ott"]
---
# Streaming and OTT

A streaming service is a subscription business wrapped around content it mostly does not own forever. Licensing windows decide what you can show, where, and until when; churn decides whether any of it was worth the check. Product work here splits into two loops that share one budget: the content loop (what to license or make, judged in cost per hour actually watched) and the experience loop (discovery, playback quality, and the cancel flow), and the second loop exists to protect the first loop's spend.

**Adjacent industries:** music streaming, distribution and royalty tools read this card, with one structural difference from film and television. Each recording splits into master and publishing rights, and performance and mechanical royalties are paid through different bodies: labels and distributors, performing-rights organisations, and in the US the Mechanical Licensing Collective's blanket licence under the Music Modernization Act, with some rates set by the Copyright Royalty Board rather than negotiated. The payout model (pro-rata, user-centric or artist-centric, and any minimum-stream threshold) is therefore a product decision with legal and industry-political exposure, and royalty accounting is an audited obligation: the statement a rights holder receives deserves the care of a customer's bill. Podcasts read [Media and publishing](media-publishing.md). As of 2026-09-11; verify and confirm with counsel.

## Questions a PM must ask

1. Which titles drive signups and which drive retention, and does the content team's valuation model separate the two? A title that acquires subscribers who leave in month two has a different worth than one nobody joins for but everyone finishes.
2. What are the window and territory terms on the catalog this feature depends on? A watchlist, a download feature, or a launch market can be legal in one territory and a contract breach in the next.
3. What is our churn decomposed into voluntary and involuntary? Payment failures are a solvable engineering problem hiding inside a number everyone treats as a sentiment problem.
4. What does quality of experience look like at the ugly edge: rebuffering ratio, time to first frame, start failures, on the worst devices we support? Subscribers do not file bugs; they cancel.
5. How much of our distribution do the app stores and TV platforms own, and what does their cut plus their subscription rules do to ARPU by signup channel?
6. What is the cost per hour watched for each content category, and who is allowed to see that number? A catalog decision made on total views subsidizes expensive prestige with cheap library.
7. What is the plan when a major licensor pulls out? Output deals end; a product built assuming a permanent catalog has no answer for the quarter the catalog shrinks.
8. If ads enter the model: what does the ad tier do to churn, ARPU mix, and the engineering cost of two experiences?

## Gatekeepers

- **Rights holders.** Studios and labels set windows, territories, hold-backs, and usage terms (offline, concurrent streams, resolution caps). Their contracts are requirements documents you did not write.
- **App stores and TV platforms.** Apple, Google, Roku, and smart-TV vendors each run certification, billing rules, and revenue cuts; a TV app release train moves at the platform's pace, not yours.
- **Content and media regulators.** The EU AVMS directive imposes European-works quotas and prominence duties; local content and ratings regimes vary by market and can block a launch.
- **Payment processors.** Involuntary churn runs through retry and dunning rules; card-network rules on subscriptions and free-trial disclosure bind the cancel and trial flows.

## Metrics that matter

| Metric | What it tells you | How it lies |
|---|---|---|
| Monthly churn, split voluntary/involuntary | The business's survival rate and which team owns fixing it | A blended rate lets everyone blame the content |
| ARPU by plan and signup channel | What a subscriber is worth after platform cuts | Blends hide that app-store subscribers may be structurally cheaper to lose |
| Hours watched per account per month | Engagement as a leading indicator of renewal | Autoplay inflates it; hours chosen beat hours defaulted |
| Cost per hour watched, by title category | Whether the content budget buys retention | Needs honest amortization; a hit's tail flatters this for years |
| QoE: rebuffer ratio, time to first frame, start failure rate | Whether the pipes are quietly causing churn | Averages hide device and network tails; measure the worst decile |
| Content-driven signup attribution | Which titles acquire | First-title-watched is correlation; treat it as a hint, not a valuation |

## Reading

- **Streaming, Sharing, Stealing**, Michael D. Smith and Rahul Telang (2016). The economics of why distribution moved from scheduled channels to on-demand catalogs, and why data on what people actually watch shifts power toward whoever holds it. The book's core claim, that content decisions become analytics decisions, is this domain's operating assumption.
- **Doug Shapiro's essays on streaming economics** (The Mediator, ongoing). Working analyst material on why the streaming transition broke television's bundling margins and what scale actually buys; read for the cost-side discipline most product decks in this domain skip.

**Conductor overlay:** this domain sharpens DESIGN-5 (who we wait on: rights holders and platform certification are the waits), OPERATE-3 (did the drivers move: churn decomposition), and OPERATE-9 (the kill condition for a content bet, set before the premiere).

**Templates this bends:** [dependency-register](../../templates/execution/dependency-register.md) (licenses and windows enter as dated dependencies with owners) and [metrics-review](../../templates/operate/metrics-review.md) (input metrics split into content and experience loops).

**Filled in this repo:** [domain-streaming-ott-dependency-register.md](../../examples/domain-streaming-ott-dependency-register.md) fills the [dependency-register](../../templates/execution/dependency-register.md) template directly for this domain, for Northlight Streaming: the DEP-4 row on Studio Corvid's 300-title UK and Ireland output-deal renewal needed by 2026-12-01 and not yet committed, a sports rights blackout feed, a localisation vendor's subtitle delivery, age classification for new titles, DRM licence-server certification, and the ad-tier measurement partner, escalated through content partnerships rather than engineering, with reverse dependencies showing ad sales sold against titles that are leaving. For the metrics-review template, [ledgerline-metrics-review.md](../../examples/ledgerline-metrics-review.md) remains the nearest reading, for tracing which input metric drives which key result, though its inputs are SaaS adoption metrics, not hours watched or rebuffer ratio.

**Worked example (ILLUSTRATIVE):** a slice of [dependency-register](../../templates/execution/dependency-register.md) section 1, showing how a content licence reads as a dependency row. Names, studio and numbers are fiction.

| # | Dependency (deliverable, not a team name) | Owning team | Their named contact | Needed by (our date) | Their committed date | Status | Escalation contact (their manager or ours) |
|---|---|---|---|---|---|---|---|
| DEP-4 | Renewed output-deal licence for Studio Corvid's catalogue, 300 titles, UK and Ireland territory only | Studio Corvid, rights licensing | Elena Voss (ILLUSTRATIVE) | 2026-12-01, 60 days before the current window expires | not yet committed, in renewal negotiation | at risk | Head of Content Partnerships |

Unlike a vendor SLA row, "their committed date" here is a renewal decision, and "at risk" means titles leave the catalogue on the window's own expiry date whether or not anyone escalates; the row's escalation contact needs to be a content-partnerships owner, not an engineering one, because no amount of engineering effort moves a licence date.
