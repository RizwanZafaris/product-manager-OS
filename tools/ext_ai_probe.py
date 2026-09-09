#!/usr/bin/env python3
"""Collect the EXT-AI evidence a live provider probe owes, and nothing else.

    python3 tools/ext_ai_probe.py --dry-run
    python3 tools/ext_ai_probe.py --discover-only
    python3 tools/ext_ai_probe.py --free-only --budget-usd 0.00 --max-calls 6

Standard library only, like every other script in this tree.

docs/readiness/external-gates.json says EXT-AI needs four things: provider
authorization, redacted request and response hashes, resolved model
provenance, and a budget and privacy policy result. This script produces
exactly those four and refuses to produce anything that looks like them
without having actually made the calls.

What it will not do, stated because a probe that quietly does any of them is
worse than no probe:

- It never prints, logs, stores or hashes the credential. It reads the
  configured environment variable at call time through the adapter and holds
  no copy.
- It never writes a probe artifact that says a call happened unless one did.
  --dry-run exercises every code path except the socket and stamps the output
  "dry_run": true, so a dry-run file can never be mistaken for evidence.
- It never routes a high-risk task to an uncertified model to make the sample
  look complete. pmos.routing refuses those, that refusal is the system
  working, and the refusal itself is recorded as a policy result.
- It never retries a refusal into a success.

The prompts are fixed, small and public: PM artifact drafting against a
template excerpt that ships in this repository. Nothing customer-derived,
nothing regulated, nothing from a product workspace, so the privacy class of
every request is "public" and is asserted here rather than inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

DEFAULT_OUT = REPO / ".readiness" / "ext-ai-probe.json"
GATEWAY_TIMEOUT_SECONDS = 120
GATEWAY_BASE_URL_ENV = "OMNIROUTE_BASE_URL"
GATEWAY_API_KEY_ENV = "OMNIROUTE_API_KEY"
GATEWAY_BASE_URL_DEFAULT = "http://localhost:20128/v1"
GATEWAY_MAX_RESPONSE_BYTES = 2 * 1024 * 1024
GATEWAY_MAX_OUTPUT_TOKENS = 1024
# routing/README.md, "Request headers that keep OmniRoute out of your prompts":
# compression would paraphrase text the model must quote, the semantic cache
# would replay one answer to every similar prompt, and memory injection
# changes the prompt the model sees. Every gateway call sends all three.
GATEWAY_REQUEST_HEADERS = {
    "x-omniroute-compression": "off",
    "X-OmniRoute-No-Cache": "true",
    "x-omniroute-no-memory": "true",
}
GIT_TIMEOUT_SECONDS = 30

# Fixed, public, small. Each names the task class pmos.routing will judge it
# under, so the policy result is about the router's decision and not about
# whatever a prompt happened to look like.
CASES = [
    {"id": "draft-problem-statement", "task": "drafting", "risk": "low",
     "prompt": "Write a two-sentence product problem statement for a payouts "
               "retry screen. State who is affected and what it costs them. "
               "No solution, no features."},
    {"id": "extract-fields", "task": "extraction", "risk": "low",
     "prompt": "From this line, return only JSON with keys metric, baseline, "
               "target: 'Checkout completion is 61% today; we want 70% by "
               "Q3.'"},
    {"id": "summarize-evidence", "task": "extraction", "risk": "low",
     "prompt": "Summarize in one sentence, quoting no more than six words "
               "verbatim: 'Three of five interviewees abandoned at the "
               "address step because postcode validation rejected valid "
               "rural codes.'"},
    {"id": "kill-criteria", "task": "drafting", "risk": "medium",
     "prompt": "Write one kill criterion for a feature launch. It must name a "
               "metric, a threshold, a check date and who calls it. One line."},
    # Deliberately included and expected to be REFUSED on a free uncertified
    # model. A probe that only samples what passes measures nothing about the
    # gate that matters most.
    {"id": "architecture-refusal-check", "task": "architecture", "risk": "high",
     "prompt": "Propose a transactional commit design for multi-file "
               "artifact writes."},
    {"id": "regulatory-refusal-check", "task": "regulatory", "risk": "high",
     "prompt": "List the licence conditions that gate a payouts feature in "
               "the UAE."},
]


def say(*parts):
    print(" ".join(str(p) for p in parts))


def sha256(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def git(*args):
    try:
        done = subprocess.run(["git", *args], cwd=str(REPO),
                              capture_output=True, text=True,
                              timeout=GIT_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def credential_present(env_name):
    """Whether the variable is set, without reading its value into anything.

    os.environ.get would put the credential in a local. This asks only the
    question the probe is allowed to ask.
    """
    return env_name in os.environ and bool(os.environ[env_name].strip())


def build_report(args, env_name):
    dirty = bool(git("status", "--porcelain"))
    return {
        "schema": 1,
        "gate": "EXT-AI",
        "dry_run": bool(args.dry_run),
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": git("rev-parse", "HEAD"),
        "working_tree": "dirty" if dirty else "clean",
        "python": platform.python_version(),
        "provider": "openrouter",
        "credential_env": env_name,
        "credential_present": credential_present(env_name),
        "credential_value_recorded": False,
        "free_only": bool(args.free_only),
        "budget_usd": args.budget_usd,
        "max_calls": args.max_calls,
        "privacy_class_asserted": "public",
        "privacy_basis": "fixed public prompts from this repository; no "
                         "workspace, customer or regulated content is sent",
        "catalog": {},
        "calls": [],
        "policy_results": [],
        "totals": {},
    }


def discover(report, args):
    """Catalog discovery. Costs no tokens; still requires the credential."""
    from pmos.openrouter import OpenRouterProvider

    # The same credential variable the generation path uses. Discovery
    # constructing a default-env provider meant --env selected a key one
    # half of the run never read.
    provider = OpenRouterProvider(api_key_env=getattr(args, "env", None))
    started = time.monotonic()
    specs = provider.discover(free_only=args.free_only)
    elapsed = time.monotonic() - started
    report["catalog"] = {
        "discovered": len(specs),
        "free_only": bool(args.free_only),
        "seconds": round(elapsed, 3),
        "free_models": sorted(s.model for s in specs if s.free)[:40],
        "certified_models": sorted(s.model for s in specs if s.certified),
    }
    return specs


def choose_model(specs, args):
    """The cheapest usable free model, chosen deterministically by id.

    Not "the best" and not the first the catalog happened to return: a probe
    that picks differently on each run cannot be compared to its last run.
    """
    usable = [s for s in specs if s.available and (s.free or not args.free_only)]
    if not usable:
        return None
    if args.model:
        exact = [s for s in usable if s.model == args.model]
        return exact[0] if exact else None
    free = sorted((s for s in usable if s.free), key=lambda s: s.model)
    return free[0] if free else None


GATEWAY_PREFIX = "openrouter/"


def gateway_catalog(free_only=True, timeout_seconds=None):
    """Models the gateway may be asked for, priced by the provider that bills them.

    Until 2026-09-09 this read `omniroute simulate`, on the theory that the
    router's own dry run was an inventory of what it serves. It is not. The dry
    run prints the weighted fallback table of the `auto` combo whatever model
    is pinned, so it could neither confirm that a pinned id was routable nor
    notice that the one id it did print had stopped being free: on the day this
    changed it listed `minimax/minimax-m3:free`, which OpenRouter had withdrawn
    from the free tier (404, "unavailable for free"), and could not surface any
    model that was free. A catalog whose free-ness is a name suffix is a name,
    not billing evidence, which the changelog had already said about it.

    The provider's own catalog is the billing evidence. `/api/v1/models` is
    public, needs no credential, and carries prompt and completion prices per
    model; the direct transport already trusts exactly this endpoint through
    `OpenRouterProvider.discover`, so both transports now agree on what "free"
    means. Nothing here reads a key: the adapter attaches an Authorization
    header only when one is passed, and none is. No generation is made.

    Membership in this list is the eligibility check, and it remains half of
    the proof: the other half is the post-call identity check that the model
    the gateway resolved is the model that was pinned. Returns None when the
    catalog could not be read (timeout, transport error, malformed body), which
    callers must treat as "discovery failed" rather than "nothing is free".
    """
    from pmos.openrouter import OpenRouterError, OpenRouterProvider

    timeout = GATEWAY_TIMEOUT_SECONDS if timeout_seconds is None else timeout_seconds
    try:
        specs = OpenRouterProvider().discover(
            free_only=free_only, timeout_seconds=timeout, anonymous=True)
    except (OpenRouterError, OSError, ValueError, TimeoutError):
        # A catalog that could not be read is not an empty catalog. The empty
        # case means "the provider prices nothing at zero today"; this case
        # means "we do not know", and dispatch must not proceed on not knowing.
        return None
    models = []
    for spec in specs:
        if free_only and not spec.free:
            continue
        model = GATEWAY_PREFIX + spec.model
        if model not in models:
            models.append(model)
    return models


def same_gateway_model(pinned, resolved):
    """Whether the model the gateway says answered is the model that was pinned.

    The gateway is addressed as ``openrouter/<provider id>`` and answers with
    the provider id alone: on 2026-09-09 a call pinned to
    ``openrouter/nvidia/nemotron-3-super-120b-a12b:free`` came back with
    ``model`` and ``X-OmniRoute-Model`` both reading
    ``nvidia/nemotron-3-super-120b-a12b:free``. That is the same model under
    the two spellings the two hops use, and a strict string comparison
    recorded it as a substitution. The only spellings accepted are the pinned
    id itself and the pinned id with the gateway prefix removed. Anything
    else -- another vendor, another variant, a paid twin without the ``:free``
    suffix, an empty answer -- is still a mismatch, because those are exactly
    the substitutions the check exists to catch.
    """
    if not isinstance(pinned, str) or not isinstance(resolved, str):
        return False
    if not pinned or not resolved:
        return False
    if resolved == pinned:
        return True
    if pinned.startswith(GATEWAY_PREFIX):
        return resolved == pinned[len(GATEWAY_PREFIX):]
    return False


def gateway_base_url(environ=None):
    """The gateway's OpenAI-compatible base URL, and only if it is local.

    The evidence this transport produces says "the credential stayed inside a
    local gateway; this process never saw it". That sentence is only true when
    the gateway is on this host. A base URL pointing anywhere else would send
    the prompts off the machine and make the claim false, so it is refused
    rather than used.
    """
    source = os.environ if environ is None else environ
    value = (source.get(GATEWAY_BASE_URL_ENV) or "").strip() or GATEWAY_BASE_URL_DEFAULT
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        return None
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        return None
    return value.rstrip("/")


class _BoundedReader:
    """Read at most N+1 bytes so an oversize body is detected, never buffered."""

    @staticmethod
    def read(response, limit):
        try:
            return response.read(limit + 1)
        except TypeError:
            return response.read()


def _number_or_none(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _gateway_billing(usage, headers_lower):
    """Whatever the gateway said this call cost, from wherever it said it.

    The provider's own ``usage.cost`` when the gateway forwards it, otherwise
    the gateway's ``X-OmniRoute-Response-Cost`` header, labelled as the
    gateway's figure. Empty when neither is present. Computed before any
    provenance judgement is made, because a charge is a charge whether or not
    the answer it bought is admissible as evidence.
    """
    provider_cost = _number_or_none((usage or {}).get("cost"))
    if provider_cost is not None:
        return {"cost_usd": provider_cost,
                "cost_source": "provider usage.cost forwarded by the gateway"}
    gateway_cost = _number_or_none(headers_lower.get("x-omniroute-response-cost"))
    if gateway_cost is not None:
        return {"cost_usd": gateway_cost,
                "cost_source": ("gateway header x-omniroute-response-cost; "
                                "the gateway's figure, not the provider's invoice")}
    return {}


def omniroute_chat(model, prompt, *, urlopen=None, environ=None):
    """One call through the local OmniRoute gateway. Returns a result dict.

    The credential stays inside OmniRoute. This process never reads it, never
    receives it, and could not print it if it tried, which is the whole reason
    this transport exists alongside the direct one. (OMNIROUTE_API_KEY, if
    set, is the gateway's own access key, not a provider credential; it is
    sent to the loopback gateway and recorded nowhere.)

    The model is always pinned. Calling with `auto` returns the alias rather
    than the model that answered, and "resolved model provenance" is one of the
    four things EXT-AI requires, so an unpinned call cannot produce evidence.

    Until 2026-09-09 this shelled out to `omniroute chat` and parsed a coloured
    footer for the resolved model and a token count. That path could not send
    the request headers routing/README.md requires, could not see whether the
    answer was a cache replay, and returned no cost at all, so every gateway
    run ended after one call with cost UNKNOWN. The gateway's HTTP API carries
    all of it: the resolved model in the body and in X-OmniRoute-Model, the
    token counts in `usage`, the cache and compression outcome in headers, and
    a per-response cost in X-OmniRoute-Response-Cost. The provider's own
    `usage.cost` is preferred when the gateway forwards it; the header is the
    fallback and is recorded as the gateway's figure, not the provider's.
    """
    base = gateway_base_url(environ)
    if base is None:
        return {"error": "omniroute_not_local",
                "error_detail": "%s must name a loopback gateway"
                                % GATEWAY_BASE_URL_ENV}
    source = os.environ if environ is None else environ
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               **GATEWAY_REQUEST_HEADERS}
    gateway_key = (source.get(GATEWAY_API_KEY_ENV) or "").strip()
    if gateway_key and not any(c in gateway_key for c in "\r\n"):
        headers["Authorization"] = "Bearer " + gateway_key
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": GATEWAY_MAX_OUTPUT_TOKENS,
        "stream": False,
        "usage": {"include": True},
    }, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    request = urllib.request.Request(base + "/chat/completions", data=body,
                                     headers=headers, method="POST")
    opener = urlopen or urllib.request.urlopen
    started = time.monotonic()
    try:
        response = opener(request, timeout=GATEWAY_TIMEOUT_SECONDS)
    except urllib.error.HTTPError as error:
        detail = ""
        try:
            raw = _BoundedReader.read(error, 4096)
            try:
                decoded = json.loads(raw.decode("utf-8", "replace"))
                err = decoded.get("error") if isinstance(decoded, dict) else None
                detail = (err.get("message") if isinstance(err, dict) else str(err)) or ""
            except (ValueError, AttributeError):
                detail = raw.decode("utf-8", "replace")
        except Exception:                                   # noqa: BLE001
            detail = ""
        error_headers = getattr(error, "headers", None)
        try:
            lowered = {str(k).lower(): str(v) for k, v in error_headers.items()} \
                if hasattr(error_headers, "items") else {}
        except Exception:                                   # noqa: BLE001
            lowered = {}
        return {"error": "omniroute_http_%d" % error.code,
                "error_detail": str(detail)[:200],
                **_gateway_billing({}, lowered)}
    except (TimeoutError, socket_timeout()) as error:
        # An unbounded gateway call can hang a release gate indefinitely.
        return {"error": "omniroute_timeout",
                "error_detail": "no response within %ds" % GATEWAY_TIMEOUT_SECONDS}
    except (urllib.error.URLError, OSError) as error:
        reason = getattr(error, "reason", error)
        if isinstance(reason, (TimeoutError, socket_timeout())):
            return {"error": "omniroute_timeout",
                    "error_detail": "no response within %ds" % GATEWAY_TIMEOUT_SECONDS}
        return {"error": "omniroute_unavailable",
                "error_detail": str(reason)[:200]}
    elapsed = (time.monotonic() - started) * 1000.0
    try:
        raw = _BoundedReader.read(response, GATEWAY_MAX_RESPONSE_BYTES)
        header_items = list(getattr(response, "headers", {}).items()) \
            if hasattr(getattr(response, "headers", None), "items") else []
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()
    if len(raw) > GATEWAY_MAX_RESPONSE_BYTES:
        return {"error": "omniroute_response_too_large",
                "error_detail": "body exceeded %d bytes" % GATEWAY_MAX_RESPONSE_BYTES}
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return {"error": "omniroute_malformed_response",
                "error_detail": "body is not JSON"}
    if not isinstance(decoded, dict):
        return {"error": "omniroute_malformed_response",
                "error_detail": "body is not an object"}
    h = {str(k).lower(): str(v) for k, v in header_items}
    usage = decoded.get("usage") if isinstance(decoded.get("usage"), dict) else {}
    # Billing first, judgement second. The third review round returned a
    # body carrying usage.cost 0.75 with a cache hit, then with compression
    # on, then with a body/header model disagreement; all three were rightly
    # refused as evidence and all three returned before the cost was read,
    # so the run aggregated $0.00 with cost_unknown false against a reported
    # charge. A charge survives whatever is decided about the answer.
    billing = _gateway_billing(usage, h)
    if decoded.get("error"):
        err = decoded["error"]
        message = err.get("message") if isinstance(err, dict) else str(err)
        return {"error": "omniroute_error", "error_detail": str(message)[:200],
                **billing}
    # Provenance the doctrine headers exist to secure. A replayed answer is
    # not evidence that this model answered this prompt now, and a compressed
    # prompt is not the prompt whose hash the evidence records.
    cache = (h.get("x-omniroute-cache") or "").strip().upper()
    if cache == "HIT" or (h.get("x-omniroute-cache-hit") or "").strip().lower() == "true":
        return {"error": "cached_response",
                "error_detail": "the gateway replayed a cached answer",
                **billing}
    compression = (h.get("x-omniroute-compression") or "").strip().lower()
    if compression and not compression.startswith("off"):
        return {"error": "compressed_prompt",
                "error_detail": "gateway compression was %r" % compression[:40],
                **billing}
    body_model = decoded.get("model") if isinstance(decoded.get("model"), str) else None
    header_model = (h.get("x-omniroute-model") or "").strip() or None
    if body_model and header_model and body_model != header_model:
        return {"error": "resolved_model_conflict",
                "error_detail": "body says %r, header says %r"
                                % (body_model, header_model),
                **billing}
    resolved = body_model or header_model
    choices = decoded.get("choices")
    text = ""
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        message = choices[0].get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            text = message["content"]

    def _tokens(key):
        value = usage.get(key)
        return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None

    result = {
        "text": text.strip(),
        "resolved_model": resolved,
        "prompt_tokens": _tokens("prompt_tokens"),
        "completion_tokens": _tokens("completion_tokens"),
        "total_tokens": _tokens("total_tokens"),
        "latency_ms": round(elapsed, 1),
        "gateway": {
            "request_id": h.get("x-omniroute-request-id"),
            "provider": h.get("x-omniroute-provider"),
            "cache": h.get("x-omniroute-cache"),
            "compression": h.get("x-omniroute-compression"),
            "model_header": header_model,
        },
    }
    result.update(billing)
    return result


def socket_timeout():
    import socket
    return socket.timeout


class provider_stub:
    """Stands in for an adapter during an eligibility check.

    _eligible only asks whether a provider exists and reports itself
    available. It never places a call, so nothing here needs to be able to.
    """

    available = True


def reserve_cost_usd(spec, prompt, args):
    """Worst-case advertised cost of one call, reserved before dispatch.

    Price is only known for certain once the response arrives, so a ceiling
    checked afterwards is not a ceiling. This reserves against the advertised
    per-1k price and the maximum output the request can produce, which is the
    strongest bound obtainable before the call. A provider that then bills more
    than it advertised is caught on reconciliation and halts the run.
    """
    price = getattr(spec, "cost_per_1k_tokens", 0.0) or 0.0
    if not price:
        return 0.0
    max_output = getattr(args, "max_output_tokens", None) or 1024
    # len(prompt)//4 is an average, not a bound, and a reservation built on an
    # average under-reserves exactly on the inputs that tokenize badly. A token
    # never covers less than one byte, so byte length is the real upper bound.
    prompt_tokens = max(1, len(prompt.encode("utf-8")))
    return price * (prompt_tokens + max_output) / 1000.0


def usable_cost(value):
    """(cost, status). Absent authoritative cost stays UNKNOWN, never zero.

    Coercing a missing cost to 0.0 turns "the provider told us nothing" into
    "the provider told us it was free", which is the one inference a budget
    gate must never make on its own behalf.
    """
    if value is None:
        return None, "UNKNOWN"
    if isinstance(value, bool):
        # bool is a subclass of int, so float(True) is 1.0. A flag is not a
        # price, and silently reading one as $1.00 is worse than refusing it.
        return None, "INVALID"
    if not isinstance(value, (int, float)):
        # A numeric string parses, but authoritative usage arrives as a number.
        # Accepting "0.5" means accepting whatever else a provider puts there.
        return None, "INVALID"
    try:
        cost = float(value)
    except (TypeError, ValueError):
        return None, "INVALID"
    if cost != cost or cost in (float("inf"), float("-inf")) or cost < 0:
        return None, "INVALID"
    return cost, "OK"


def route_decision(spec, case, args):
    """Ask pmos.routing whether this case may run on this model.

    Uses the router's own eligibility check rather than route(), deliberately.
    route() would place the call, and the policy question has to be answerable
    without spending anything: that is what makes --dry-run able to prove the
    refusal behaviour with no credential. The router is the authority either
    way; this records what it decided and never second-guesses it.

    risk_trust_policy is None on purpose. A probe that supplies its own trust
    policy would be certifying the model it is meant to be testing.
    """
    from pmos.routing import ModelRouter, RoutingRequest

    # A provider entry is required for eligibility to reach the policy checks
    # at all: with an empty map every case returns "provider unavailable",
    # which is a fact about the probe rather than about the router. In a live
    # run this is the real adapter; in a dry run it is a stand-in that reports
    # itself available and is never called, because _eligible never calls.
    router = ModelRouter(catalog=[spec],
                         providers={spec.provider: provider_stub()},
                         risk_trust_policy=None)
    request = RoutingRequest(
        prompt=case["prompt"], task=case["task"], risk=case["risk"],
        privacy="public",
        budget_usd=args.budget_usd if args.budget_usd is not None else None,
    )
    allowed, reason = router._eligible(spec, request)
    return allowed, reason


def run_via_omniroute(report, args):
    """Collect EXT-AI evidence through the local gateway.

    The credential stays inside OmniRoute for the whole run. This process reads
    no key, so the evidence records provider authorization as "delegated" and
    says which component actually held it, rather than claiming an
    authorization it never possessed.
    """
    from pmos.routing import ModelSpec

    report["transport"] = "omniroute"
    report["credential_env"] = None
    report["credential_holder"] = "local OmniRoute gateway"
    report["provider_authorization"] = "delegated to OmniRoute; this process " \
                                       "never read a provider credential"

    models = gateway_catalog(free_only=args.free_only)
    if models is None:
        say("REFUSING: provider catalog could not be read; an unreadable "
            "catalog is not an inventory.")
        report["catalog"] = {"discovered": 0, "free_only": args.free_only,
                             "free_models": [], "certified_models": [],
                             "error": "discovery_failed",
                             "source": "openrouter /api/v1/models, keyless, "
                                       "did not complete"}
        report["totals"] = {"calls_made": 0, "attempts": 0, "errors": 1,
                            "refusals": 0, "cost_usd": 0.0,
                            "cost_unknown": True, "budget_breach": False}
        write(report, args.output)
        return 1
    report["catalog"] = {"discovered": len(models), "free_only": args.free_only,
                         "free_models": models, "certified_models": [],
                         "source": "openrouter /api/v1/models, keyless GET; "
                                   "prices are the provider's; no generation"}
    if not models:
        say("no free model resolved through OmniRoute; nothing was called.")
        write(report, args.output)
        return 1
    if args.discover_only:
        # Reached before any generation. This guard used to live only on the
        # direct path, which main() never took when --via omniroute was set,
        # so --discover-only still generated through the gateway.
        write(report, args.output)
        say("")
        say("Discovery only. No generation was requested, no tokens spent.")
        return 0

    model = args.model or models[0]
    if model not in models:
        # The catalog is the only evidence available here for what this gateway
        # actually serves and on what terms. Taking --model on trust let an
        # arbitrary out-of-catalog paid model be dispatched and recorded at
        # zero cost, on the strength of a free model existing elsewhere in the
        # catalog. Membership is not a formality; it is the eligibility check.
        say("REFUSING: %r is not in the discovered catalog." % model)
        say("  discovered: %s" % ", ".join(models))
        report["totals"] = {"calls_made": 0, "attempts": 0, "errors": 1,
                            "refusals": 0, "cost_usd": 0.0,
                            "budget_breach": False}
        report["calls"] = [{"case": None, "called": False,
                            "error": "model_outside_catalog",
                            "error_detail":
                                "%r was not advertised by discovery" % model}]
        write(report, args.output)
        return 1

    if args.max_calls < 1:
        say("INCOMPLETE: --max-calls %d permits no dispatch, so this run "
            "cannot produce generation evidence." % args.max_calls)
        write(report, args.output)
        return 1

    say("  transport         : omniroute (credential held by the gateway)")
    say("  free models        : %s" % ", ".join(models))
    say("  pinned model      : %s" % model)
    say("")

    # Pinned, never auto. An auto call reports the alias back rather than the
    # model that answered, and resolved provenance is one of the four things
    # this gate requires.
    spec = ModelSpec(provider="openrouter", model=model,
                     free=bool(args.free_only),
                     available=True, certified=False, cost_per_1k_tokens=0.0,
                     context_window=8192,
                     privacy_classes=frozenset({"public"}))

    made = 0
    attempts = 0
    spent = 0.0
    budget = args.budget_usd or 0.0
    enforce_budget = not args.unbounded_budget
    breach = False
    cost_unknown = False
    halted = False
    for case in CASES:
        if breach or halted:
            break
        if attempts >= args.max_calls:
            break
        allowed, reason = route_decision(spec, case, args)
        entry = {"case": case["id"], "task": case["task"],
                 "risk": case["risk"], "eligible": bool(allowed),
                 "router_reason": reason, "called": False}
        if not allowed:
            report["policy_results"].append(entry)
            say("  [REFUSE] %-28s %s" % (case["id"], reason))
            continue
        attempts += 1
        try:
            result = omniroute_chat(model, case["prompt"])
        except Exception as error:                          # noqa: BLE001
            # The direct path records an adapter exception as a failed call.
            # This path let it escape and abort the probe, losing the evidence
            # of every case already run.
            result = {"error": type(error).__name__,
                      "error_detail": str(error)[:200]}
        if not result.get("error"):
            resolved = result.get("resolved_model")
            billing = {key: result[key] for key in ("cost_usd", "cost_source")
                       if key in result}
            if not resolved:
                # Keep any billing the gateway did report: replacing the whole
                # result with an error discarded a charge that was already made.
                result = {"error": "missing_resolved_model",
                          "error_detail": "the gateway returned no resolved model",
                          "cost_usd": result.get("cost_usd"), **billing}
            elif not same_gateway_model(model, resolved):
                # The call is pinned. A different model answering means the
                # evidence describes something other than what was authorized.
                # The charge for it was still made, and is carried.
                result = {"error": "resolved_model_mismatch",
                          "error_detail": "pinned %r, answered %r"
                                          % (model, resolved), **billing}
        if not result.get("error") and not (result.get("text") or "").strip():
            result = dict(result, error="empty_output",
                          error_detail="the gateway returned no output text")
        if result.get("error"):
            halted = True
            entry.update({"called": True, "error": result["error"],
                          "error_detail": result.get("error_detail")})
            if "cost_usd" in result:
                known, status = usable_cost(result.get("cost_usd"))
                entry.update({"cost_usd": known, "cost_status": status,
                              "cost_basis": result.get("cost_source")
                                            or "reported by the gateway"})
                if status == "OK":
                    spent += known
            say("  [ERROR]  %-28s %s" % (case["id"], result["error"]))
        else:
            text = result.get("text") or ""
            entry.update({
                "called": True,
                "request_sha256": sha256(case["prompt"]),
                "response_sha256": sha256(text),
                "response_chars": len(text),
                "response_preview": text[:220],
                "latency_ms": result.get("latency_ms"),
                "resolved_provider": "openrouter",
                "resolved_model": result.get("resolved_model"),
                "total_tokens": result.get("total_tokens"),
                "prompt_tokens": result.get("prompt_tokens"),
                "completion_tokens": result.get("completion_tokens"),
                "gateway_provenance": result.get("gateway"),
            })
            # Absent cost is UNKNOWN, and an unprovable remaining budget stops
            # the run. The gateway reports a per-response cost in a header and
            # may forward the provider's own figure; whichever was used is
            # named in cost_basis so a reader can weigh it.
            cost, cost_status = usable_cost(result.get("cost_usd"))
            entry.update({"cost_usd": cost, "cost_status": cost_status,
                          "cost_basis": result.get("cost_source")
                                        or "reported by the gateway"
                                        if cost_status == "OK" else
                                        "the gateway reported no usable cost"})
            if cost_status != "OK":
                entry.update({"error": "cost_%s" % cost_status.lower(),
                              "error_detail":
                                  "budget compliance cannot be evidenced for "
                                  "this transport"})
                cost_unknown = True
                halted = True
            else:
                spent += cost
                made += 1
            say("  [OK]     %-28s %-26s %sms  %s tok"
                % (case["id"], entry["resolved_model"],
                   entry["latency_ms"], entry["total_tokens"]))
        if enforce_budget and spent > budget:
            breach = True
            say("  [HALT]   billed $%.6f against a $%.6f ceiling; stopping"
                % (spent, budget))
        report["calls"].append(entry)
        report["policy_results"].append(entry)

    report["totals"] = {
        "calls_made": made,
        "attempts": attempts,
        "refusals": sum(1 for r in report["policy_results"]
                        if not r["eligible"]),
        "errors": sum(1 for r in report["calls"] if r.get("error")),
        "cost_usd": round(spent, 6),
        "cost_unknown": cost_unknown,
        "budget_breach": breach,
    }
    write(report, args.output)
    say("")
    if cost_unknown:
        say("AGGREGATE COST IS NOT $0.00: at least one call returned no usable "
            "cost, so the total below is a lower bound on an unknown amount.")
    say("calls %d, refusals %d, errors %d"
        % (report["totals"]["calls_made"], report["totals"]["refusals"],
           report["totals"]["errors"]))
    say("The refusals are the certification gate working. They belong in the "
        "evidence, not filtered out of it.")
    return 1 if (report["totals"]["errors"] or breach) else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="exercise every path except the socket; the "
                             "output is stamped dry_run and is not evidence")
    parser.add_argument("--discover-only", action="store_true",
                        help="list the catalog and stop; costs no tokens")
    parser.add_argument("--free-only", action="store_true", default=True,
                        help="restrict to models whose prompt AND completion "
                             "price are both zero (default)")
    parser.add_argument("--allow-paid", dest="free_only", action="store_false",
                        help="permit priced models; requires --budget-usd")
    parser.add_argument("--unbounded-budget", action="store_true",
                        help="permit spending with no ceiling; must be given "
                             "explicitly and is never the default")
    parser.add_argument("--budget-usd", type=float, default=0.0,
                        help="hard ceiling passed to the router (default 0.0, "
                             "which only free models can satisfy)")
    parser.add_argument("--max-calls", type=int, default=len(CASES),
                        help="stop after this many generations")
    parser.add_argument("--model", help="pin one exact model id")
    parser.add_argument("--via", choices=("direct", "omniroute"),
                        default="direct",
                        help="direct reads the credential from --env; "
                             "omniroute routes through the local gateway, "
                             "which holds the credential so this process "
                             "never sees it")
    parser.add_argument("--env", default="OPENROUTER_API_KEY",
                        help="name of the credential variable to read")
    parser.add_argument("--output", default=str(DEFAULT_OUT),
                        help="where to write the evidence file")
    args = parser.parse_args(argv)

    report = build_report(args, args.env)

    say("EXT-AI probe")
    say("  provider          : openrouter")
    say("  credential var    : %s (%s)"
        % (args.env, "set" if report["credential_present"] else "NOT SET"))
    say("  free only         : %s" % args.free_only)
    say("  budget ceiling    : $%.4f" % (args.budget_usd or 0.0))
    say("  commit            : %s (%s tree)"
        % (report["commit"][:12], report["working_tree"]))
    say("")

    if args.dry_run:
        # Every path except the socket. The cases are routed against a
        # synthetic free, uncertified model so the refusal behaviour that
        # matters can be proven with no credential and no spend.
        from pmos.routing import ModelSpec

        spec = ModelSpec(provider="openrouter", model="dry-run/free-model",
                         free=True, available=True, certified=False,
                         cost_per_1k_tokens=0.0, context_window=8192,
                         privacy_classes=frozenset({"public"}))
        report["catalog"] = {"discovered": 1, "free_only": True,
                             "free_models": [spec.model],
                             "certified_models": []}
        for case in CASES:
            allowed, reason = route_decision(spec, case, args)
            report["policy_results"].append({
                "case": case["id"], "task": case["task"],
                "risk": case["risk"], "eligible": bool(allowed),
                "router_reason": reason, "called": False,
            })
            say("  [%s] %-28s %s"
                % ("ROUTE " if allowed else "REFUSE", case["id"], reason))
        report["totals"] = {"calls_made": 0, "refusals": sum(
            1 for r in report["policy_results"] if not r["eligible"])}
        write(report, args.output)
        say("")
        say("DRY RUN. No socket was opened and no evidence was produced.")
        say("The routing decisions above are real; the model was synthetic.")
        return 0

    if args.via == "omniroute":
        return run_via_omniroute(report, args)

    if not report["credential_present"]:
        say("REFUSING to run: %s is not set." % args.env)
        say("")
        say("This gate needs a live call. Export a ROTATED credential and "
            "rerun. The previously exposed key must not be reused.")
        say("  export %s='<rotated key>'" % args.env)
        say("  python3 tools/ext_ai_probe.py --discover-only")
        return 2

    try:
        specs = discover(report, args)
    except Exception as error:                              # noqa: BLE001
        say("catalog discovery failed: %s: %s"
            % (type(error).__name__, str(error)[:200]))
        report["catalog"] = {"error": type(error).__name__}
        write(report, args.output)
        return 1

    say("  catalog           : %d model(s), %d free"
        % (report["catalog"]["discovered"],
           len(report["catalog"]["free_models"])))

    if args.discover_only:
        write(report, args.output)
        say("")
        say("Discovery only. No generation was requested, no tokens spent.")
        return 0

    spec = choose_model(specs, args)
    if spec is None:
        say("no usable model matched the constraints; nothing was called.")
        write(report, args.output)
        return 1
    say("  chosen model      : %s" % spec.model)
    say("")

    from pmos.openrouter import OpenRouterProvider
    # The chosen credential variable must reach the adapter, or --env silently
    # selects a key the adapter never reads.
    provider = OpenRouterProvider(api_key_env=args.env)
    made = 0
    attempts = 0
    spent = 0.0
    budget = args.budget_usd or 0.0
    enforce_budget = not args.unbounded_budget
    breach = False
    budget_refusals = 0
    halted = False

    for case in CASES:
        if halted:
            break
        allowed, reason = route_decision(spec, case, args)
        entry = {"case": case["id"], "task": case["task"],
                 "risk": case["risk"], "eligible": bool(allowed),
                 "router_reason": reason, "called": False}
        if not allowed:
            report["policy_results"].append(entry)
            say("  [REFUSE] %-28s %s" % (case["id"], reason))
            continue

        # Attempts, not successes. Counting successes meant a failing adapter
        # was re-entered once per case: the audit saw four dispatches under
        # --max-calls 1. A cap that loosens when calls start failing is not one.
        # The cap skips dispatch but must not skip the remaining cases: the
        # refusal checks cost nothing and are the evidence this gate exists for.
        if attempts >= args.max_calls:
            entry["router_reason"] = "call cap reached before this case"
            report["policy_results"].append(entry)
            say("  [SKIP]   %-28s call cap reached" % case["id"])
            continue

        reserved = reserve_cost_usd(spec, case["prompt"], args)
        if enforce_budget and spent + reserved > budget:
            budget_refusals += 1
            entry.update({"error": "budget_reservation_refused",
                          "error_detail":
                              "advertised price reserves $%.6f against $%.6f "
                              "remaining" % (reserved, budget - spent)})
            report["calls"].append(entry)
            report["policy_results"].append(entry)
            say("  [REFUSE] %-28s reservation exceeds remaining budget"
                % case["id"])
            halted = True
            continue

        attempts += 1
        started = time.monotonic()
        try:
            response = provider.complete(spec.model, case["prompt"])
            elapsed = (time.monotonic() - started) * 1000.0
            text = getattr(response, "output", "") or ""
            resolved_model = getattr(response, "model", None)
            cost, cost_status = usable_cost(getattr(response, "cost_usd", None))
            entry.update({
                "called": True,
                "request_sha256": sha256(case["prompt"]),
                "response_sha256": sha256(text),
                "response_chars": len(text),
                "latency_ms": round(elapsed, 1),
                "resolved_provider": spec.provider,
                "resolved_model": resolved_model,
                "prompt_tokens": getattr(response, "input_tokens", None),
                "completion_tokens": getattr(response, "output_tokens", None),
                "cost_usd": cost,
                "cost_status": cost_status,
            })
            if cost_status != "OK":
                # Without an authoritative cost there is no evidence the run
                # stayed inside its ceiling, so the ceiling is unproven.
                entry.update({"error": "cost_%s" % cost_status.lower(),
                              "error_detail":
                                  "provider returned no usable cost; budget "
                                  "compliance cannot be evidenced"})
                report["calls"].append(entry)
                report["policy_results"].append(entry)
                say("  [ERROR]  %-28s cost %s" % (case["id"], cost_status))
                halted = True
                continue
            spent += cost
            if resolved_model and resolved_model != spec.model:
                # A nonempty model is not the authorized model. Evidence naming
                # something other than what was approved describes a different
                # run than the one that was permitted.
                entry.update({"error": "resolved_model_mismatch",
                              "error_detail": "authorized %r, answered %r"
                                              % (spec.model, resolved_model)})
                report["calls"].append(entry)
                report["policy_results"].append(entry)
                say("  [ERROR]  %-28s resolved_model_mismatch" % case["id"])
                halted = True
                continue
            if not text.strip():
                # An empty body is not evidence that a model answered, and the
                # call may still have been billed. Recording it clean let a
                # provider returning nothing count towards the gate.
                entry.update({"error": "empty_output",
                              "error_detail":
                                  "the provider returned no output text"})
                report["calls"].append(entry)
                report["policy_results"].append(entry)
                say("  [ERROR]  %-28s empty_output" % case["id"])
                halted = True
                continue
            if not resolved_model:
                # Resolved provenance is one of the four things this gate
                # requires. Without it there is no evidence a model answered.
                entry.update({"error": "missing_resolved_model",
                              "error_detail":
                                  "the provider returned no resolved model"})
                report["calls"].append(entry)
                report["policy_results"].append(entry)
                say("  [ERROR]  %-28s missing_resolved_model" % case["id"])
                halted = True
                continue
            report["calls"].append(entry)
            made += 1
            say("  [OK]     %-28s %s  %.0fms  %s chars"
                % (case["id"], resolved_model, elapsed, len(text)))
            if enforce_budget and spent > budget:
                # Zero is a ceiling, not the absence of one. The guard used to
                # read `if budget`, so a $0.00 free-only run skipped this check
                # entirely and billed $1.50 across two dispatches with a clean
                # exit. Overbilling can explain the first charge; it cannot
                # explain the second dispatch.
                breach = True
                report["policy_results"].append(entry)
                say("  [HALT]   billed $%.6f against a $%.6f ceiling; stopping"
                    % (spent, budget))
                halted = True
                continue
        except Exception as error:                          # noqa: BLE001
            # Whether the failed call was billed is unknowable from here, so
            # the remaining budget is unprovable and the run stops.
            entry.update({"called": True, "error": type(error).__name__,
                          "error_detail": str(error)[:200]})
            report["calls"].append(entry)
            say("  [ERROR]  %-28s %s" % (case["id"], type(error).__name__))
            halted = True
        report["policy_results"].append(entry)

    report["totals"] = {
        "calls_made": made,
        "attempts": attempts,
        "refusals": sum(1 for r in report["policy_results"]
                        if not r["eligible"]),
        "errors": sum(1 for r in report["calls"] if r.get("error")),
        "cost_usd": round(spent, 6),
        "budget_breach": breach,
    }
    write(report, args.output)
    say("")
    say("calls %d, attempts %d, refusals %d, errors %d, cost $%.6f"
        % (report["totals"]["calls_made"], attempts,
           report["totals"]["refusals"],
           report["totals"]["errors"], report["totals"]["cost_usd"]))
    say("EXT-AI evidence written. It records what happened, including the "
        "refusals, which are the gate working rather than a shortfall.")
    if breach:
        say("BUDGET BREACH: the provider billed more than it advertised.")
    # A run that errored, breached its ceiling, or could not afford its cases
    # is not a successful run, and must not report success to CI.
    if report["totals"]["errors"] or breach or budget_refusals:
        return 1
    if args.max_calls < 1:
        say("INCOMPLETE: --max-calls %d permits no dispatch, so this run "
            "cannot produce generation evidence." % args.max_calls)
        return 1
    if attempts == 0:
        # Every case was refused before dispatch, so this run generated no
        # EXT-AI evidence at all. The refusals are worth recording, but a gate
        # that produced no evidence has not passed; it did not run.
        say("INCOMPLETE: no case was dispatched, so no generation evidence "
            "exists. The refusals are recorded, but this is not a pass.")
        return 1
    return 0


def write(report, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    say("  evidence          : %s" % path)


if __name__ == "__main__":
    sys.exit(main())
