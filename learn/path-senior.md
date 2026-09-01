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

## Step 1: strategy that survives the kernel test

**Read:** the strategy kernel and Playing to Win entries in the [knowledge index](../knowledge/INDEX.md); Rumelt and Lafley-Martin in full live in [the library](library.md). Grove's leverage lens from [High Output Management](../knowledge/high-output-management.md) is the senior companion, with Drucker's The Effective Executive (library) as the longer read.
**Study:** [the roadmap](../templates/planning/roadmap.md), and reread its expectations-not-commitments preamble as a strategy artifact, not a scheduling one.
**Do:** write Meterly's strategy in kernel form in PROGRESS.md: one diagnosis (invented: the platform's enterprise deals stall on unpredictable API bills), one guiding policy, three coherent actions. Then write the two where-to-play choices you are explicitly declining.
**Done when:** the diagnosis names a cause and not a symptom, every action traces to the policy, and each declined choice would look attractive in a board deck, because a strategy that only declines bad options has decided nothing.

## Step 2: the beachhead, chosen on purpose

**Read:** [Crossing the Chasm](../knowledge/crossing-the-chasm.md). The trap is the beachhead that is secretly everyone; Meterly's temptation is "all API-first companies".
**Study:** [the GTM plan](../templates/planning/gtm-plan.md).
**Do:** fill the GTM plan for Meterly's launch. Pick one first cohort narrow enough to be countable (invented: payment-infrastructure startups with usage-based pricing already live), name the alternative they use today, the channel with invented evidence it reaches them, the one launch metric, and the stop condition.
**Done when:** the cohort has an invented count attached, the positioning names one alternative rather than a category, and the stop condition would genuinely embarrass you to hit, which is how you know it is real.

## Step 3: growth with a mechanism attached

**Read:** [North star metric](../knowledge/north-star-metric.md), and the AARRR entry in the [knowledge index](../knowledge/INDEX.md) for the funnel vocabulary.
**Study:** [the growth plan](../templates/planning/growth-plan.md).
**Do:** fill the growth plan: the input-metric bet (invented: integrations installed per new customer in week one), the cheapest experiment that could move it, the loop or channel behind it, the counter-metric that catches the bet corrupting something, and the kill condition.
**Done when:** the experiment is genuinely the cheapest version you could run, the loop is a mechanism a skeptic could trace actor by actor, and the counter-metric protects something a growth-hungry team would otherwise quietly spend.

## Step 4: the premortem you run on yourself

**Read:** the premortem entry in the [knowledge index](../knowledge/INDEX.md): assume it already failed, write down why, while being right is still cheap.
**Study:** [the risk register](../templates/execution/risk-register.md), and the runner in [skills/program-premortem](../skills/program-premortem/SKILL.md) if your runtime has it.
**Do:** it is eighteen months out and Meterly failed. Write six failure causes in PROGRESS.md: two market, two execution, two political. Convert the four most probable into risk-register rows with likelihood, impact, mitigation, and an owner. At least one cause must implicate a decision you made in steps 1 to 3 of this path.
**Done when:** the self-implicating row exists and its mitigation changed one of your earlier artifacts, with the change actually made; a premortem that edits nothing was theater.

## Step 5: the AI overlay, evidence discipline for models

**Read:** [Empowered product teams](../knowledge/cagan-product-teams.md), the four risks; a model in the product turns feasibility and value risk into moving targets, which is what the overlay exists to pin down.
**Study:** [the eval spec](../templates/ai/eval-spec.md) and [guardrails](../templates/ai/guardrails.md).
**Do:** Meterly adds an invented AI feature: anomaly explanations for usage spikes, in plain language, on the customer dashboard. Fill the eval spec (scenario set, golden dataset shape, metrics, pass threshold, the gate that blocks on failure) and the guardrails file for it. All thresholds invented and labeled.
**Done when:** the eval spec would block a launch on its own authority, every guardrail names its enforcement point, and the failure mode of a wrong explanation shown to a paying customer is priced somewhere, not assumed away.

## Step 6: the honest ending

**Read:** [Shape Up](../knowledge/shape-up.md), the circuit-breaker idea: continuation must be re-earned, never assumed. It applies to whole products, and almost nobody applies it.
**Study:** [the metrics review](../templates/operate/metrics-review.md), the persist-pivot-sunset decision especially.
**Do:** two quarters of invented results for Meterly, and they are mixed: the north star grew, but the beachhead cohort from step 2 is not the cohort using it. Fill the metrics review and make the call: persist, pivot, or sunset. Write the memo for the call you almost made instead, three sentences, so the road not taken is on the record.
**Done when:** the decision follows from the numbers on the page rather than from momentum, and the almost-memo names what evidence would have flipped you.

## Capstone: Gate 6, defended

Run the tutor ([skills/tutor/SKILL.md](skills/tutor/SKILL.md)) with the OPERATE bank ([the questions](../skills/conductor/questions/operate.md)). This capstone is a defense, not a drill: the tutor cross-examines your persist-pivot-sunset call, pushes once per soft spot, and scores every Gate 6 line.

**Done when:** every Gate 6 line scores 2, and your decision survived at least one challenge that forced you to cite a specific artifact from an earlier step rather than your own seniority. Pencil users: argue it in writing against the bank's Accept-when lines, then have a colleague read the memo cold.

After this path: run something real through the loop, and come back only when a step's Done-when line would fail on your actual product, which is the layer telling you where to look.
