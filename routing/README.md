# Routing: which model runs which task, and why

This directory is the WITH WHICH MODEL layer of the OS. Everything above it (templates, skills, agents) names work; this layer decides how expensive a model that work deserves. The config is [omniroute.config.json](omniroute.config.json); this file is its manual.

## OmniRoute setup

OmniRoute is a local router that fronts many model providers behind one OpenAI-compatible endpoint and picks a concrete model for each request from an auto tier or a fixed list.

```bash
npm install -g omniroute
omniroute start
```

The dashboard runs at `http://localhost:20128`; the API serves OpenAI-compatible chat completions under `http://localhost:20128/v1`. Add your provider keys in the dashboard, then export two variables for anything that reads the config:

```bash
export OMNIROUTE_BASE_URL="http://localhost:20128/v1"
export OMNIROUTE_API_KEY="<the key you set in the OmniRoute dashboard>"
```

The config never contains a key or a resolved URL. It names the environment variables, and the caller resolves them at run time. If you find a literal credential in any config in this repository, that is a defect; the lint gate checks for common key patterns.

## The endpoint contract

Every call is a standard OpenAI chat-completions request. The only OmniRoute-specific part is the model field, which names a tier rather than a vendor model:

```bash
curl "$OMNIROUTE_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/cheap",
    "messages": [{"role": "user", "content": "Extract the owner names from the pasted risk register."}]
  }'
```

Because the contract is plain OpenAI-compatible, any SDK, proxy, or agent runtime that can point at a custom base URL can use this routing without adapter code.

## Tier doctrine

Three tiers, chosen by what a wrong answer costs, not by what the task feels like it deserves.

| Tier | Model | Use for | Never for |
|---|---|---|---|
| extraction | `auto/cheap` | Mechanical, checkable transforms: pulling fields, normalizing backlogs, tagging sources, format conversion, validation-agent runs (checking a draft against a template's field list is lookup, not judgment) | Anything a human will sign, anything that weighs tradeoffs |
| drafting | `auto/coding` | First complete drafts of structured artifacts: drafting-agent runs, ADRs, diagrams-as-code, restructuring a PRD without changing its claims | Prioritization calls, adversarial review |
| judgment | `auto/reasoning:pro` | Work that is expensive to get wrong and hard to verify locally: roadmap scoring and the defense page, premortems, red-team passes, reg gap checks, gate reviews | High-volume extraction; burning the reasoning budget on lookup work |

Three rules bind the doctrine:

1. **Route by blast radius.** If a wrong answer is caught mechanically (a checker, a diff, a template field list), the cheap tier is enough. If a wrong answer survives until a human relies on it, pay for judgment.
2. **Chains split by tier.** An extract-then-draft-then-judge pipeline is three calls on three tiers, not one call on the judgment tier. The `taskMap` block in the config records the standing assignments for this repository's skills and agents.
3. **Degrade by queueing, never by downgrading.** When the judgment tier is capped or down, judgment work waits. Silently rerouting a premortem to the cheap tier produces a document that looks reviewed and is not, which is worse than a late one. This is the `onCapReached: halt-tier-and-queue` setting in the config.

## Conductor stage routing

The Conductor (protocol in [../os/CONDUCTOR.md](../os/CONDUCTOR.md)) splits every stage of its interview across the same three tiers, by blast radius, never by convenience:

| Work | Tier |
|---|---|
| Transcribing accepted answers into STATE.md and template fields; formatting; smart-skip lookups | extraction, `auto/cheap` |
| Drafting a template section from a set of accepted answers; gtm-plan and growth-plan first drafts | drafting, `auto/coding` |
| Cross-examination, gate-checklist evaluation, premortem, red team, the analyst's reconcile-before-handoff pass, persist-pivot-sunset framing | judgment, `auto/reasoning:pro` |

Queue when the judgment tier is capped, per rule 3 above, and never downgrade a cross-examination to the cheap tier: an interrogation that cannot spot a weak answer is worse than a delayed one. The `taskMap` entries prefixed `skill-conductor-` and `skill-product-analyst-` in the config record these assignments.

## Fixed-fallback combo recipe

Auto tiers are the default and the right choice for most users: OmniRoute picks a live, priced model per request. Deployments that must know exactly which model produced an artifact (audit requirements, regulated sign-offs, reproducibility) enable the `fixedFallback` block instead:

1. In the config, set `fixedFallback.enabled` to `true`.
2. For each tier, replace the placeholders with model IDs your OmniRoute instance actually serves, in preference order. The first available model in the list handles the request; the next takes over on outage or rate limit.
3. Record the model ID actually used in each artifact's telemetry. A fixed combo without per-call logging buys nothing at audit time.
4. Re-run any standing eval sets when you change a combo. A model swap is an upgrade decision, not a config edit; the AI templates in `../templates/ai/` treat it as one.

## Note for Hermes users (litellm)

Hermes-style deployments (see [../agents/hermes-agent.md](../agents/hermes-agent.md)) usually already run a litellm proxy in front of their models. Two clean options:

- **Point litellm at OmniRoute.** Add the three tiers as litellm model entries whose `api_base` is `$OMNIROUTE_BASE_URL` and whose model names are `auto/cheap`, `auto/coding`, and `auto/reasoning:pro`. Hermes code keeps calling litellm; OmniRoute does the picking.
- **Skip OmniRoute and map tiers in litellm.** Recreate the three tier names as litellm router model groups with your own provider lists, mirroring the fixed-fallback recipe above. Keep the tier names identical to this config so the `taskMap` and the doctrine still read true.

Either way, the invariants from the Hermes file carry over unchanged: fail closed at the cap, queue rather than downgrade, and log which model actually answered.
