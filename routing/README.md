# Routing: which model runs which task, and why

This directory is the optional WITH WHICH MODEL layer of the OS. Everything above it (templates, skills, agents) names work; this layer decides how expensive a model that work deserves when an operator chooses to make a provider call. The document path and the `pmos` local runtime do not require OmniRoute or any model. The config is [omniroute.config.json](omniroute.config.json); this file is its manual.

## OmniRoute setup

OmniRoute is a local router that fronts many model providers behind one OpenAI-compatible endpoint and picks a concrete model for each request from an auto tier or a fixed list.

```bash
npm install -g omniroute
omniroute serve
```

The dashboard runs at `http://localhost:20128`; the API serves OpenAI-compatible chat completions under `http://localhost:20128/v1`. Connect at least one provider (dashboard, or `omniroute providers add <provider> --oauth` for the Claude Code, Codex and Gemini subscriptions; `omniroute providers add ollama-local --name ollama --credential ollama --provider-specific-data '{"baseUrl":"http://localhost:11434/v1"}'` for a local Ollama), create an API key on the dashboard's Endpoints page, then export two variables for anything that reads the config:

```bash
export OMNIROUTE_BASE_URL="http://localhost:20128/v1"
export OMNIROUTE_API_KEY="<the key you created in the OmniRoute dashboard>"
```

The config never contains a key or a resolved URL. It names the environment variables, and the caller resolves them at run time. If you find a literal credential in any config in this repository, that is a defect; the lint gate checks for common key patterns.

### Verify the tiers before trusting them

A tier name is a promise about which models may answer, not a guarantee that one is connected. On a fresh install only the keyless free provider is wired, so `auto/cheap`, `auto/coding` and `auto/reasoning` all resolve to the same free model, and `auto/reasoning:pro` answers `404 Combo has no executable targets` until a provider that serves a pro reasoning model is connected. Probe all three before running anything that matters:

```bash
for tier in auto/cheap auto/coding auto/reasoning:pro; do
  printf '%-20s ' "$tier"
  curl -s "$OMNIROUTE_BASE_URL/chat/completions" \
    -H "Authorization: Bearer $OMNIROUTE_API_KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"$tier\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with exactly: PONG\"}],\"max_tokens\":300}" \
    | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("model") or d["error"]["message"])'
done
```

Each line should print the concrete model that answered. If the judgment line prints the error instead, the tier has no executable target: connect a provider, or queue the judgment work (rule 3 below). Do not point the judgment tier at the free model to make the error go away; the config carries an explicit, off-by-default `keylessFallback` for people who accept that trade knowingly, and every artifact produced under it must say so.

### Request headers that keep OmniRoute out of your prompts

OmniRoute can rewrite prompts (RTK and Caveman compression), replay cached answers for temperature-0 requests (semantic cache) and inject conversational memory and skills. All three are useful for chat and harmful for this OS's extraction and transcription work, where a model is supposed to copy text verbatim and a replayed bad answer would repeat forever. The `endpoint.requestHeaders` block in the config lists the headers every caller should send:

| Header | Value | Why |
|---|---|---|
| `x-omniroute-compression` | `off` | never let the router paraphrase a document the model must quote |
| `X-OmniRoute-No-Cache` | `true` | the caller keeps its own exact-match cache; the router's semantic cache would serve one wrong answer to every similar prompt |
| `x-omniroute-no-memory` | `true` | no memory or skill injection, so the prompt the model sees is the prompt you wrote |

The response echoes `X-OmniRoute-Compression`, `X-OmniRoute-Cache` and `X-OmniRoute-Model`; log them next to every artifact.

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

## OpenRouter and free models

OmniRoute is optional. The local runtime also supplies `pmos.openrouter.OpenRouterProvider`, a standard-library adapter that discovers the current OpenRouter catalog at runtime and sends OpenAI-compatible chat-completions requests only when the caller asks it to. It reads `OPENROUTER_API_KEY` (or a configured environment-variable name) at request time. Never put that value in a config file, shell history, artifact, or repository.

The adapter classifies a model as free only from the current catalog's prompt and completion pricing metadata. That is a routing input, not a promise: the free catalog, availability, rate limits, capabilities, and resolved model can change without notice. Do not hard-code a model name from this file or call a free model a permanent tier.

Use a bounded operator workflow instead:

1. Discover the current catalog and filter for the needed context window, modalities, tools, privacy permission, budget, and latency. Discovery failures become a bounded, secret-free error rather than escaping the routing boundary. Every runtime request carries a bounded `max_output_tokens`; the router conservatively includes prompt bytes in its context/cost reservation, then checks authoritative usage when returned. Budgeted fallback reserves the worst-case capped catalog cost across every permitted attempt before the first call.
2. Put only eligible models in a bounded fallback order. A provider response that
   omits or reports a different resolved model is rejected: its privacy, cost,
   capability, and certification metadata were not the metadata used to admit
   the requested model. Reported output beyond the token cap, output beyond the
   conservative byte backstop, reported spend beyond the request budget, or
   actual/reported latency beyond the remaining request boundary is also
   rejected. Reported and usage-derived spend is accumulated even for a paid
   response later rejected by another policy check; a fallback runs only when
   its full reservation still fits the remaining budget. The OpenRouter adapter requires authoritative usage fields, caps
   the response body from the requested output allowance, and receives the
   remaining timeout from the router. Generic adapters receive the same
   remaining timeout/request contract and are checked again on return. Safe
   provenance therefore records the exact accepted model, never an unapproved
   substitution or an estimate presented as actual behavior.
3. Run an approved smoke test before relying on an integration. A local unit test or a dynamic catalog response does not prove live behavior, vendor terms, or availability.
4. Require explicit certification for high-risk work. Reachability, zero price, a friendly name, or a successful ping never makes a model judgment-grade. If no certified model is eligible, queue or block the work rather than silently downgrading it.

The runtime's OpenRouter adapter is intentionally separate from OmniRoute: use either, both through an adapter boundary, or neither. An OmniRoute deployment may still use the same tier doctrine and fixed-fallback recipe above, but it does not become a dependency of the local runtime.

## Note for Hermes users (litellm)

Hermes-style deployments (see [../agents/hermes-agent.md](../agents/hermes-agent.md)) usually already run a litellm proxy in front of their models. Two clean options:

- **Point litellm at OmniRoute.** Add the three tiers as litellm model entries whose `api_base` is `$OMNIROUTE_BASE_URL` and whose model names are `auto/cheap`, `auto/coding`, and `auto/reasoning:pro`. Hermes code keeps calling litellm; OmniRoute does the picking.
- **Skip OmniRoute and map tiers in litellm.** Recreate the three tier names as litellm router model groups with your own provider lists, mirroring the fixed-fallback recipe above. Keep the tier names identical to this config so the `taskMap` and the doctrine still read true.

Either way, the invariants from the Hermes file carry over unchanged: fail closed at the cap, queue rather than downgrade, and log which model actually answered.
