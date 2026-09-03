# Path: Senior sharpening

Audience: you run products already. Gates, PRDs, and discovery are muscle memory; what dulls at this altitude is strategy under ambiguity, launches into indifferent markets, growth claims without mechanisms, AI features without evidence discipline, and the decision nobody rehearses: ending things. Each step here sharpens one of those.
Fictional product: **Meterly**, usage metering and rate limiting for a developer API platform. B2B, technical buyer, invented end to end; label invented evidence "invented:".
Convention: same ledger discipline as the other paths, and the tutor grades you harder here because the evidence ladder does not care about your title.

Before step 1: create `learn/products/meterly/`, copy the ledger below into `PROGRESS.md` there, per [products/README.md](products/README.md).

## Ledger (copy into learn/products/meterly/PROGRESS.md)

- [ ] Step 1: strategy that survives the kernel test
- [ ] Step 2: the beachhead, chosen on purpose
- [ ] Step 3: growth with a mechanism attached
- [ ] Step 4: the premortem you run on yourself
- [ ] Step 5: the AI overlay, evidence discipline for models
- [ ] Step 6: the honest ending
- [ ] Capstone: Gate 6, defended

## The standing brief

Six steps, one situation, and the later steps are supposed to indict the earlier ones. Copy this into your PROGRESS.md and do not improve it when it becomes inconvenient at step 6; that is where the learning is.

Invented: the platform has 780 paying accounts and 9.4 million in annual recurring revenue. Six enterprise deals stalled in procurement last year over unpredictable API bills, average contract 240,000 a year. Support logs 190 surprise-invoice tickets a quarter, and the finance team issues an average of eleven goodwill credits a month to keep accounts calm. Self-serve accounts churn at 3 percent a month; accounts in the top usage decile churn at 8 percent a year but generate most of the credits. Engineering capacity for the next two quarters is nine people. The board has asked, once, why metering is not already a product.

Everything above is invented and labeled. Treat the numbers as fixed constraints rather than raw material: a senior PM's real skill is being pinned by a situation someone else created, and a brief you can edit teaches nothing about that.

## Step 1: strategy that survives the kernel test

**Read:** the strategy kernel and Playing to Win entries in the [knowledge index](../knowledge/README.md); Rumelt and Lafley-Martin in full live in [the library](library.md). Grove's leverage lens from [High Output Management](../knowledge/high-output-management.md) is the senior companion, with Drucker's The Effective Executive (library) as the longer read.
**Run:** [the strategy kernel worksheet](../frameworks/strategy/strategy-kernel.md), then read the filled [Ledgerline kernel](../examples/ledgerline-strategy-kernel.md) only after your own diagnosis exists, because reading a good diagnosis first anchors you into copying its shape.
**Study:** [the roadmap](../templates/planning/roadmap.md), and reread its expectations-not-commitments preamble as a strategy artifact, not a scheduling one.
**Do:** write Meterly's strategy in kernel form in PROGRESS.md: one diagnosis (invented: the platform's enterprise deals stall on unpredictable API bills), one guiding policy, three coherent actions. Then write the two where-to-play choices you are explicitly declining.
**Done when:** the diagnosis names a cause and not a symptom, every action traces to the policy, and each declined choice would look attractive in a board deck, because a strategy that only declines bad options has decided nothing.

**Why this comes first.** Every later step in this path is a bet placed against this diagnosis: the beachhead is chosen for it, the growth loop is supposed to feed it, and the sunset call at step 6 is judged by whether it was ever true. Senior work goes wrong here more often than anywhere else, and it goes wrong quietly, because a plausible diagnosis produces months of coherent activity aimed at the wrong cause.

**The decision rule.** If your diagnosis can be restated as "we do not have feature X", it is a symptom, because the cause of a missing feature is always a prior decision about where attention went. Push one level down and ask what makes the pain expensive rather than merely present. Stalled deals are not caused by absent metering; they are caused by a buyer having to sign for a cost they cannot forecast and cannot cap, which is a procurement-risk problem that metering happens to be one answer to. Diagnose at that level and the guiding policy writes itself; diagnose at the feature level and you have written a roadmap with a serif font.

**Worked micro-example.** Weak declined choice: "we will not build a general billing platform", which nobody proposed and nothing turns on. Strong: "we decline the finance-buyer play, selling reconciliation and invoicing to controllers, even though it is the larger budget line and the board would applaud it, because it puts us in a category with entrenched vendors and our distribution is the developer already in the console." A declined choice that costs nothing to decline was never a choice.

**Pass criteria.** A 2: a diagnosis naming a cause that a competitor could suffer from too, three actions each traceable to the policy in one sentence, and two declined choices with the reason each one is attractive. A 1: a sound kernel whose declined choices nobody would have proposed. A 0: a guiding policy that is a target.

**The trap, and its tell.** Goals wearing strategy's clothes. The tell: your guiding policy contains a number. Policy says how you will compete, targets say how much, and a policy with a target inside it usually has no decision inside it at all.

**Time.** Two hours, and half of it belongs to the two declined choices, which most people skip and which the tutor asks about first.

## Step 2: the beachhead, chosen on purpose

**Read:** [Crossing the Chasm](../knowledge/crossing-the-chasm.md). The trap is the beachhead that is secretly everyone; Meterly's temptation is "all API-first companies".
**Run:** [the positioning canvas](../frameworks/strategy/positioning-canvas.md) for the alternative-versus-us framing, and [market sizing](../frameworks/strategy/market-sizing.md) to force a countable cohort rather than a percentage of a market report.
**Study:** [the GTM plan](../templates/planning/gtm-plan.md).
**Do:** fill the GTM plan for Meterly's launch. Pick one first cohort narrow enough to be countable (invented: payment-infrastructure startups with usage-based pricing already live), name the alternative they use today, the channel with invented evidence it reaches them, the one launch metric, and the stop condition.
**Done when:** the cohort has an invented count attached, the positioning names one alternative rather than a category, and the stop condition would genuinely embarrass you to hit, which is how you know it is real.

**Why now.** A kernel with no where-to-play choice is half a strategy, and this step is that choice rendered as something a sales team can act on next Tuesday. It runs second rather than later because everything downstream needs a named cohort: growth loops run inside a population, and step 6's persist-pivot-sunset call turns entirely on whether the cohort you picked is the one that showed up.

**The decision rule.** A beachhead is real when you can write down how many there are and how you would list them by name. If the count comes from a percentage of an analyst's market number, you have sized a market and chosen nothing, because a segment you cannot enumerate cannot be saturated, and saturating one segment is the whole mechanism behind the beachhead idea. Invented and usable: 140 payment-infrastructure companies with public usage-based pricing pages, of which 40 already publish a status page with rate-limit documentation, which is your list.

**What good looks like.** Weak positioning: "the modern metering platform for API-first companies." Strong: "for a payments infrastructure startup whose enterprise prospects demand a spend cap before signing, Meterly is the metering layer that turns usage into a contractual cap, unlike the internal Postgres counter and cron job they wrote in year one, which nobody trusts at audit." The alternative is named, it is real, and it is what you will actually be compared against in the room.

**Pass criteria.** A 2: a cohort with a count and a method for listing its members by name, positioning against one named alternative, one launch metric, and a stop condition with a date on it. A 1: a narrow-sounding cohort sized from a percentage of a market number. A 0: a cohort defined by a technology preference, which is everyone with a budget.

**The trap, and its tell.** The stop condition that cannot fire. The tell: it is expressed in a metric nobody reports weekly, or on a horizon longer than the plan it governs. Strong and uncomfortable: "if fewer than six of the named 40 have completed an integration by the end of quarter two, we stop the paid channel and re-open the diagnosis." You should dislike reading that sentence. Also worth reading here: [stage shift](../knowledge/roles/stage-shift.md), on how the same product needs a different motion at a different company stage.

**Time.** Two hours. The cohort list takes twenty minutes and changes the rest of the plan.

## Step 3: growth with a mechanism attached

**Read:** [North star metric](../knowledge/north-star-metric.md), and the AARRR entry in the [knowledge index](../knowledge/README.md) for the funnel vocabulary.
**Run:** [growth loops](../frameworks/metrics/growth-loops.md) to draw the loop actor by actor, and [cohort retention](../frameworks/metrics/cohort-retention.md) to see whether your bet is retention wearing an acquisition costume.
**Study:** [the growth plan](../templates/planning/growth-plan.md).
**Do:** fill the growth plan: the input-metric bet (invented: integrations installed per new customer in week one), the cheapest experiment that could move it, the loop or channel behind it, the counter-metric that catches the bet corrupting something, and the kill condition.
**Done when:** the experiment is genuinely the cheapest version you could run, the loop is a mechanism a skeptic could trace actor by actor, and the counter-metric protects something a growth-hungry team would otherwise quietly spend.

**Why now.** Because a growth plan written before a beachhead is a funnel with no population inside it. This step exists at senior level for one reason: at this altitude you will be asked for a growth number by someone who does not want the mechanism, and the discipline being trained is producing the mechanism anyway, in writing, before the number.

**The decision rule.** A loop is a mechanism only if each arrow is an action performed by a named actor with a reason to perform it. If any arrow is a verb without an actor, such as "usage grows", the loop is a diagram of your hopes. Traceable version, invented: a platform engineer sets a spend cap, the cap appears on the account's monthly report, their finance counterpart sees a forecast they trust, procurement clears the next tier upgrade, the upgrade raises usage volume, higher volume makes caps matter more to the next team in the same company. Six arrows, six actors, each with a motive.

**What good looks like.** A counter-metric protects the thing the bet would cannibalize. Weak: support ticket count, which moves for a dozen unrelated reasons. Strong, given the bet is week-one integrations: goodwill credits issued per month, held at or below the current eleven, because the fastest way to install integrations quickly is to loosen default limits, and loose defaults are what generate surprise invoices and then credits. The counter-metric should make you slightly nervous about your own bet.

**Pass criteria.** A 2: every arrow in the loop has an actor and a motive, the experiment could run this week without engineering, the counter-metric protects something the bet endangers, and the kill condition carries a date. A 1: a real loop with a counter-metric that is a general health measure. A 0: a bet with no mechanism underneath it.

**The trap, and its tell.** The experiment that is really the feature. The tell: your cheapest experiment needs engineering capacity to start. The cheapest version of the integration bet is a scripted setup call with five of the named 40 accounts and a template repository, run by a human, measured the same way. If that moves nothing, no amount of build was going to.

**Time.** Two hours, the loop diagram taking most of it. Draw it twice.

## Step 4: the premortem you run on yourself

**Read:** the premortem entry in the [knowledge index](../knowledge/README.md): assume it already failed, write down why, while being right is still cheap.
**Run:** [the premortem worksheet](../frameworks/execution/premortem-worksheet.md) for the causes, then [the risk matrix](../frameworks/execution/risk-matrix.md) to place them, because likelihood and impact scored in your head are scored to make your plan look good.
**Study:** [the risk register](../templates/execution/risk-register.md), and the runner in [skills/program-premortem](../skills/program-premortem/SKILL.md) if your runtime has it.
**Do:** it is eighteen months out and Meterly failed. Write six failure causes in PROGRESS.md: two market, two execution, two political. Convert the four most probable into risk-register rows with likelihood, impact, mitigation, and an owner. At least one cause must implicate a decision you made in steps 1 to 3 of this path.
**Done when:** the self-implicating row exists and its mitigation changed one of your earlier artifacts, with the change actually made; a premortem that edits nothing was theater.

**Why now.** Steps 1 through 3 are three linked bets, which is exactly the point at which a plan becomes too coherent to doubt. The self-implicating row is the whole exercise: a premortem run on the parts of the plan you inherited is a complaint, and a premortem run on the parts you authored is the only version that has ever changed anything.

**Worked micro-example.** A political cause worth writing, invented: finance owns the goodwill credits budget, metering makes overage predictable, predictable overage means fewer credits and a smaller finance discretionary line, so the controller becomes a quiet blocker at exactly the moment the enterprise motion needs a friendly finance reference. Likelihood medium, impact high, mitigation is to co-author the cap policy with the controller before launch and give her the reporting, owner named. That row is worth more than four market rows, because market causes get discussed in every review and political ones never make it onto paper.

**Pass criteria.** A 2: six causes spread across market, execution, and politics, four scored rows with named owners, one cause implicating your own work in steps 1 to 3, and the resulting edit visible in the earlier artifact. A 1: six honest causes and mitigations that name changes nobody has made yet. A 0: a mitigation column made of attention.

**The trap, and its tell.** Mitigations that are vigilance. The tell: the mitigation column contains the words monitor, watch, or ensure. Monitoring is detection, not mitigation, and a risk whose only treatment is attention will be treated with attention right up until the week attention is expensive. Every mitigation should name a change to an artifact, a schedule, or a person's commitments.

**Time.** Ninety minutes for the six causes, plus however long the edit back into step 1 or 2 takes. Do not skip the edit; the edit is the deliverable.

## Step 5: the AI overlay, evidence discipline for models

**Read:** [Empowered product teams](../knowledge/cagan-product-teams.md), the four risks; a model in the product turns feasibility and value risk into moving targets, which is what the overlay exists to pin down.
**Run:** [assumption mapping](../frameworks/discovery/assumption-mapping.md) on the feature's beliefs before you write a single threshold, because most bad eval specs are correct measurements of the wrong assumption.
**Study:** [the eval spec](../templates/ai/eval-spec.md) and [guardrails](../templates/ai/guardrails.md).
**Do:** Meterly adds an invented AI feature: anomaly explanations for usage spikes, in plain language, on the customer dashboard. Fill the eval spec (scenario set, golden dataset shape, metrics, pass threshold, the gate that blocks on failure) and the guardrails file for it. All thresholds invented and labeled.
**Done when:** the eval spec would block a launch on its own authority, every guardrail names its enforcement point, and the failure mode of a wrong explanation shown to a paying customer is priced somewhere, not assumed away.

**Why now.** Because this is where senior judgment is most often replaced by vendor enthusiasm, and because the feature is a good trap: explaining a usage spike requires causal information that metering data alone does not contain. Deploy history, customer traffic, and a retry storm in someone else's service all look identical in a metering table. Naming that limit is the senior move; the eval spec is how you make the limit binding rather than merely known.

**The decision rule.** A threshold is real only if you have written what happens on the day it is missed, and that consequence must cost somebody something. Invented and usable: explanations must reach 85 percent agreement with a human reviewer's cause label on a set of 200 historical spikes, and below that the feature ships in an internal-only mode for support agents, who are paid to be skeptical. Compare a threshold with no consequence attached, which is a hope with a decimal point, and which will be renegotiated in the launch meeting by whoever has the most to lose from a delay.

**What good looks like.** A guardrail names its enforcement point, meaning the exact place in the system where a violation is stopped, and who owns that place. Weak: "the model must not speculate about causes it cannot verify." Strong: "explanations may cite only signals present in the account's own metering and deploy webhook data, enforced by a schema check on the generation call, owned by the platform team, and an explanation failing the check renders as the raw spike chart with no narrative." Note that the strong version specifies what the customer sees when the guardrail fires, which is the part teams forget until it fires.

**Pass criteria.** A 2: an eval set containing genuinely ambiguous cases, a threshold with a written consequence for the day it is missed, every guardrail carrying an enforcement point and an owner, and a stated limit on what metering data can support. A 1: thresholds and guardrails present with no consequence attached to failure. A 0: an eval set that cannot fail.

**The trap, and its tell.** The eval set built from examples the feature already handles. The tell: your golden dataset was assembled after the prototype worked, so every row is a spike with a single obvious cause. Real ones are ambiguous, and a set with no ambiguous rows in it cannot fail, which makes the threshold decorative. Reserve at least a fifth of the set for spikes where two engineers disagreed about the cause.

**Time.** Two to three hours. The scenario set is the long part, and it is the part that transfers to real work unchanged.

## Step 6: the honest ending

**Read:** [Shape Up](../knowledge/shape-up.md), the circuit-breaker idea: continuation must be re-earned, never assumed. It applies to whole products, and almost nobody applies it.
**Run:** [cohort retention](../frameworks/metrics/cohort-retention.md) on the invented results, split by the step 2 beachhead versus everyone else, because the headline number is an average and the average is what is hiding the story.
**Study:** [the metrics review](../templates/operate/metrics-review.md), the persist-pivot-sunset decision especially.
**Do:** two quarters of invented results for Meterly, and they are mixed: the north star grew, but the beachhead cohort from step 2 is not the cohort using it. Fill the metrics review and make the call: persist, pivot, or sunset. Write the memo for the call you almost made instead, three sentences, so the road not taken is on the record.
**Done when:** the decision follows from the numbers on the page rather than from momentum, and the almost-memo names what evidence would have flipped you.

**Why last.** Because it is the only step that can indict all five before it, and because ending things is the decision seniority makes worse rather than better: the more senior you are, the more of the plan is yours, and the more expensive it feels to say the diagnosis was wrong. Rehearsing that on a product that does not exist is the cheapest rehearsal you will ever get.

**The decision rule.** Persist when the mechanism worked in the cohort you chose. Pivot when the mechanism worked somewhere you did not choose, because that is evidence about where-to-play rather than evidence against the diagnosis. Sunset when neither the cohort nor the mechanism showed up and the cost to serve keeps arriving anyway. The Meterly result is deliberately the middle case: invented, 23 of the named 40 payments startups evaluated and 5 integrated, while 60 accounts integrated from a cohort nobody targeted, mid-sized analytics vendors whose own customers demand spend caps. That is a where-to-play correction, and calling it a success dressed as growth is the failure this step exists to catch.

**What good looks like.** The almost-memo is graded harder than the decision. Weak: "we almost sunset it." Strong: "we almost persisted with the payments cohort, and one piece of evidence would have justified it: two of the five integrated accounts expanding to a second team without a sales touch, which would have shown the loop from step 3 running in the cohort we chose rather than merely running somewhere. Neither expanded. We pivot the beachhead and keep the kernel." That memo tells the next reader exactly what you were watching, which means they can check your judgment rather than merely inherit it.

**Pass criteria.** A 2: the decision named as one of the three, the cohort split visible on the page, a scheduled consequence with dates and an owner, and an almost-memo naming the evidence that would have flipped you. A 1: the defensible call with the split evidence missing, so nobody can check the reasoning. A 0: a cohort redefined after the numbers arrived.

**The trap, and its tell.** Redefining the cohort to include whoever showed up. The tell: your metrics review contains a sentence starting "we now think of our segment as", written after the numbers arrived. Redefining a cohort after the fact makes every launch a success and makes the whole apparatus, gates included, unfalsifiable. Log the pivot as a pivot in [the decision log](../templates/execution/decision-log.md), name what changed, and keep the original cohort definition visible next to it.

**Time.** Two hours, plus a night between the review and the call. Do not make the decision in the same sitting that produced the numbers.

## Capstone: Gate 6, defended

Run the tutor ([skills/tutor/SKILL.md](skills/tutor/SKILL.md)) with the OPERATE bank ([the questions](../skills/conductor/questions/operate.md)). This capstone is a defense, not a drill: the tutor cross-examines your persist-pivot-sunset call, pushes once per soft spot, and scores every Gate 6 line.

**Done when:** every Gate 6 line scores 2, and your decision survived at least one challenge that forced you to cite a specific artifact from an earlier step rather than your own seniority. Pencil users: argue it in writing against the bank's Accept-when lines, then have a colleague read the memo cold.

**Where each gate line comes from.** Gate 6 in [STAGE-GATES.md](../os/STAGE-GATES.md) asks whether the Gate 1 success signal was measured with its source and calculation stated, whether every key result is scored number against number, whether the input metrics moved or only the headline, what the operational load was, which of the three decisions was taken, whether its consequence is scheduled with dates and an owner, and what the pass taught, in three sentences. The input-metric line is the one this path aims at: your headline grew and your chosen cohort did not, which is exactly the case that line was written to catch.

**Pass criteria for the session itself.** A 2 on every Gate 6 line; the persist, pivot or sunset call defended by citing a named artifact from steps 1 to 6 rather than your judgment; the input-metric line answered with the cohort split visible on the page; and the scheduled consequence carrying dates and an owner before the session closes. A 1 on the input-metric line is the expected first-pass result, and it sends step 6's review back for a rerun rather than a rearguing. A clean 2 across the board on a first attempt is the outcome to distrust most in this layer, because the failure the whole path is built around, a headline that grew while the chosen cohort did not, is one a confident reader talks past rather than fails.

**The trap, and its tell.** Seniority offered as evidence. The tell: an answer that begins with how long you have done this, or with a pattern you have seen before. Pattern recognition is a hypothesis generator, never a citation, and the tutor is instructed to treat it as a class-five team belief and route it accordingly. Answer with the artifact and its line instead, even when your instinct is right, because the instinct is not what the next reader inherits.

**Time.** Ninety minutes, and it is the least comfortable session in this layer by design.

After this path: run something real through the loop, and come back only when a step's Done-when line would fail on your actual product, which is the layer telling you where to look.
