---
name: strategy-critic
description: Stress-test a product strategy with two explicit checks, Rumelt's kernel test and the Playing-to-Win "what would have to be true" test, plus a durability check against the seven powers. Use when a strategy draft needs review before signature, when leadership suspects it is a goals slide, when the roadmap contains bets the strategy cannot explain, or before annual planning copies last year's strategy forward. Takes the strategy document and its evidence links; returns a verdict per check, the conditions that would have to be true with their evidence status, and the rewrites needed, in the product strategy template.
---

# Strategy Critic: strategy or slogan, decided in writing

Most strategy documents are goals with adjectives: "be the leading platform", "delight customers", "win the mid-market". They exclude nothing, so they guide nothing, and the roadmap gets decided by whoever argued loudest. This skill runs two named tests that a goals slide cannot pass, and returns the document with its gaps marked rather than its prose polished.

## Files this skill drives

- [../../templates/planning/product-strategy.md](../../templates/planning/product-strategy.md), where the passed strategy lands section by section
- The worksheets for checks 1, 2, and 3, in order: [../../frameworks/strategy/strategy-kernel.md](../../frameworks/strategy/strategy-kernel.md), [../../frameworks/strategy/playing-to-win.md](../../frameworks/strategy/playing-to-win.md), [../../frameworks/strategy/seven-powers-audit.md](../../frameworks/strategy/seven-powers-audit.md)
- Reads [../../templates/planning/roadmap.md](../../templates/planning/roadmap.md) for the bets the strategy must explain; sends unevidenced conditions to [../../templates/execution/risk-register.md](../../templates/execution/risk-register.md)
- See also [../../frameworks/systems/leverage-points.md](../../frameworks/systems/leverage-points.md) (Meadows, 1999) when the strategy passes all three checks and the last two quarters of delivered work still moved nothing. A coherent strategy whose every action is a threshold raised or a limit relaxed is coherent at the weakest end of the system, and no kernel test detects that
- Method background: Richard Rumelt, Good Strategy Bad Strategy (2011); A.G. Lafley and Roger Martin, Playing to Win (2013); Hamilton Helmer, 7 Powers (2016). All indexed in [../../knowledge/INDEX.md](../../knowledge/INDEX.md), explained here in this repository's own words.

## When to use

- A strategy draft exists and someone must sign it
- The roadmap has items the strategy cannot explain, or the strategy names bets the roadmap does not fund
- Annual planning, before last year's document is copied forward
- A competitor move or a market shift has made the diagnosis suspect

## Inputs

The strategy document, at whatever weight it exists, with its evidence links. Ask for these when missing: the diagnosis evidence (discovery documents, win-loss reviews, metrics reviews; the claims must point at something), the current roadmap, the named alternative the customer uses today, and the previous period's strategy with its scored results. If the strategy is a deck with no written sentences, ask for the sentences first; a critique of a slide critiques the designer.

## Workflow

### 1. Check 1: the kernel test (Rumelt)

A strategy has three parts or it is not one. Test each:

- **Diagnosis.** Does the document name the crux, the one obstacle that, if beaten, unlocks the rest? Decision rule: a list of trends with no obstacle fails. A crux that could describe any company in the category fails.
- **Guiding policy.** Does it state an approach to the crux that excludes other approaches? Decision rule: write the opposite policy. If the opposite is absurd ("be worse at onboarding"), the policy is a platitude and fails. If a sane competitor might choose the opposite, it passes.
- **Coherent actions.** Do the actions follow from the policy and reinforce each other, rather than compete for the same capacity? Decision rule: for each action, name the policy sentence it serves. An action serving none is a pet project; three actions that each need the same team in the same quarter are incoherent.

Record pass or fail per part, with the failing sentence quoted.

### 2. Check 2: what would have to be true (Playing to Win)

Lay out the five choices: winning aspiration, where to play, how to win, capabilities required, management systems required. For where to play and how to win, do not argue whether the choice is right. List what would have to be true for it to be right: about customers, the company's capabilities, competitors, costs. Mark each condition: evidence in hand (link it), testable cheaply (name the test and the owner), or untestable. Decision rule: a choice whose load-bearing condition is untestable is a bet the document must call a bet. A choice whose conditions are all evidenced is a strategy the team can defend. Every unevidenced condition becomes a risk register row with an early signal and a watcher.

### 3. Check 3: durability (7 Powers)

For the how-we-win section, ask which of the seven powers the edge rests on: scale economies, network economies, counter-positioning, switching costs, branding, cornered resource, process power. Decision rule: name one, with the barrier that stops a competitor copying it; or write "execution speed only" and plan for the edge to be temporary. "Better UX" is a claim, not a power.

### 4. Check the refusals and the sequencing

At most three bets, each naming what it refuses. Sequencing gates later bets on evidence, not on calendar quarters. Decision rule: a bet with an empty refused column has not been chosen. Then reconcile with the roadmap: every funded item names the bet it serves, and every bet has a funded item or is labeled deferred.

### 5. Deliver the verdict

Three outcomes. Strategy: all three kernel parts pass, the conditions are mostly evidenced or under test, the power is named. Bet dressed as strategy: the kernel passes but the load-bearing conditions are unevidenced; acceptable if the document says so and the sequencing tests them first. Goals slide: the kernel fails; back to the diagnosis, and no roadmap is built on it.

## Output format

1. Kernel table: | Part | Pass or fail | The sentence tested | What is missing |
2. Cascade table: | Choice | What would have to be true | Evidence in hand / cheap test (owner, date) / untestable |
3. Power line: the named power and its barrier, or "execution speed only"
4. Bets table with the refused column filled, and the roadmap reconciliation
5. Verdict: strategy / bet dressed as strategy / goals slide, with the reason in one paragraph
6. Rewrites, section by section, in the product strategy template, and the risk register rows for unevidenced conditions

## Failure modes this skill guards against

- **Goals mistaken for strategy.** Ambition with no diagnosis and no exclusion; the kernel test catches it.
- **Platitude policies.** Policies whose opposite nobody would choose.
- **Seven bets.** Nothing refused, so nothing chosen.
- **Arguing the choice instead of its conditions.** Rooms fight about whether a bet is right; the conditions list turns the fight into a test plan.
- **Durability by adjective.** "Best in class" as a moat.
- **Inertia strategy.** Last year's document with the dates changed and the diagnosis untouched.
- **Critic as author.** This skill marks gaps and never quietly rewrites the bets; a strategy the leaders did not choose is one they will not defend.

## Exit gate

The strategy feeds the PLANNING track of [../../os/OPERATING-LOOP.md](../../os/OPERATING-LOOP.md) and explains the bets in [../../templates/planning/roadmap.md](../../templates/planning/roadmap.md). Do not report it reviewed until the verdict is written, every unevidenced condition sits in the risk register with a signal and an owner, and the product strategy template's exit gate is honestly checkable.
