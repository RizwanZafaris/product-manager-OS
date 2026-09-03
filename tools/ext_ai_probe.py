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
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

DEFAULT_OUT = REPO / ".readiness" / "ext-ai-probe.json"

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
    done = subprocess.run(["git", *args], cwd=str(REPO), capture_output=True,
                          text=True)
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

    provider = OpenRouterProvider()
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


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def omniroute_models(free_only=True):
    """Free models OmniRoute would route to, from its own dry-run simulation.

    Read out of `omniroute simulate`, which resolves the provider chain without
    calling upstream. This never asks OmniRoute for the credential it holds.
    """
    done = subprocess.run(["omniroute", "simulate", "probe"],
                          capture_output=True, text=True)
    models = []
    for line in (done.stdout or "").splitlines():
        for token in re.findall(r"openrouter/[A-Za-z0-9._/-]+(?::free)?", line):
            token = token.rstrip(".…")
            if token not in models and (not free_only or token.endswith(":free")):
                models.append(token)
    return models


def omniroute_chat(model, prompt):
    """One call through the local OmniRoute gateway. Returns a result dict.

    The credential stays inside OmniRoute. This process never reads it, never
    receives it, and could not print it if it tried, which is the whole reason
    this transport exists alongside the direct one.

    The model is always pinned. Calling with `auto` returns the alias rather
    than the model that answered, and "resolved model provenance" is one of the
    four things EXT-AI requires, so an unpinned call cannot produce evidence.
    """
    started = time.monotonic()
    done = subprocess.run(
        ["omniroute", "chat", "--no-history", "-m", model, prompt],
        capture_output=True, text=True)
    elapsed = (time.monotonic() - started) * 1000.0
    if done.returncode != 0:
        return {"error": "omniroute_exit_%d" % done.returncode,
                "error_detail": (done.stderr or "")[-200:]}
    # The answer goes to stdout; the provenance footer goes to stderr. Reading
    # only stdout loses the resolved model, which is the one field this whole
    # transport exists to capture.
    body, resolved, tokens = [], None, None
    for line in ((done.stdout or "") + "\n" + (done.stderr or "")).splitlines():
        # The CLI colours its footer, and a colour code between the bracket and
        # the model name is enough to make the footer unparseable. Strip the
        # escapes before matching rather than widening the pattern to tolerate
        # them, because a pattern that tolerates junk also matches junk.
        line = ANSI_RE.sub("", line)
        stripped = line.strip()
        if "Loaded env" in line or "STORAGE_ENCRYPTION" in line:
            continue
        footer = re.match(r"^\[(.+?)\s+·\s+(\d+)ms\s+·\s+(\d+)\s+tok\]$",
                          stripped)
        if footer:
            resolved, tokens = footer.group(1), int(footer.group(3))
            continue
        body.append(line)
    return {"text": "\n".join(body).strip(), "resolved_model": resolved,
            "total_tokens": tokens, "latency_ms": round(elapsed, 1)}


class provider_stub:
    """Stands in for an adapter during an eligibility check.

    _eligible only asks whether a provider exists and reports itself
    available. It never places a call, so nothing here needs to be able to.
    """

    available = True


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

    models = omniroute_models(free_only=args.free_only)
    report["catalog"] = {"discovered": len(models), "free_only": args.free_only,
                         "free_models": models, "certified_models": [],
                         "source": "omniroute simulate, no upstream call"}
    if not models:
        say("no free model resolved through OmniRoute; nothing was called.")
        write(report, args.output)
        return 1
    model = args.model or models[0]
    say("  transport         : omniroute (credential held by the gateway)")
    say("  free models        : %s" % ", ".join(models))
    say("  pinned model      : %s" % model)
    say("")

    # Pinned, never auto. An auto call reports the alias back rather than the
    # model that answered, and resolved provenance is one of the four things
    # this gate requires.
    spec = ModelSpec(provider="openrouter", model=model, free=True,
                     available=True, certified=False, cost_per_1k_tokens=0.0,
                     context_window=8192,
                     privacy_classes=frozenset({"public"}))

    made = 0
    for case in CASES:
        if made >= args.max_calls:
            break
        allowed, reason = route_decision(spec, case, args)
        entry = {"case": case["id"], "task": case["task"],
                 "risk": case["risk"], "eligible": bool(allowed),
                 "router_reason": reason, "called": False}
        if not allowed:
            report["policy_results"].append(entry)
            say("  [REFUSE] %-28s %s" % (case["id"], reason))
            continue
        result = omniroute_chat(model, case["prompt"])
        if result.get("error"):
            entry.update({"called": True, "error": result["error"],
                          "error_detail": result.get("error_detail")})
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
                "cost_usd": 0.0,
                "cost_basis": "model advertises zero prompt and completion "
                              "price; verify against the provider invoice",
            })
            made += 1
            say("  [OK]     %-28s %-26s %sms  %s tok"
                % (case["id"], entry["resolved_model"],
                   entry["latency_ms"], entry["total_tokens"]))
        report["calls"].append(entry)
        report["policy_results"].append(entry)

    report["totals"] = {
        "calls_made": made,
        "refusals": sum(1 for r in report["policy_results"]
                        if not r["eligible"]),
        "errors": sum(1 for r in report["calls"] if r.get("error")),
        "cost_usd": 0.0,
    }
    write(report, args.output)
    say("")
    say("calls %d, refusals %d, errors %d"
        % (report["totals"]["calls_made"], report["totals"]["refusals"],
           report["totals"]["errors"]))
    say("The refusals are the certification gate working. They belong in the "
        "evidence, not filtered out of it.")
    return 0


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
    provider = OpenRouterProvider()
    made = 0

    for case in CASES:
        if made >= args.max_calls:
            break
        allowed, reason = route_decision(spec, case, args)
        entry = {"case": case["id"], "task": case["task"],
                 "risk": case["risk"], "eligible": bool(allowed),
                 "router_reason": reason, "called": False}
        if not allowed:
            report["policy_results"].append(entry)
            say("  [REFUSE] %-28s %s" % (case["id"], reason))
            continue

        started = time.monotonic()
        try:
            response = provider.complete(spec, case["prompt"])
            elapsed = (time.monotonic() - started) * 1000.0
            text = getattr(response, "text", "") or ""
            entry.update({
                "called": True,
                "request_sha256": sha256(case["prompt"]),
                "response_sha256": sha256(text),
                "response_chars": len(text),
                "latency_ms": round(elapsed, 1),
                "resolved_provider": getattr(response, "provider", None),
                "resolved_model": getattr(response, "model", None),
                "prompt_tokens": getattr(response, "prompt_tokens", None),
                "completion_tokens": getattr(response, "completion_tokens", None),
                "cost_usd": getattr(response, "cost_usd", None),
            })
            report["calls"].append(entry)
            made += 1
            say("  [OK]     %-28s %s  %.0fms  %s chars"
                % (case["id"], entry["resolved_model"] or spec.model,
                   elapsed, len(text)))
        except Exception as error:                          # noqa: BLE001
            entry.update({"called": True, "error": type(error).__name__,
                          "error_detail": str(error)[:200]})
            report["calls"].append(entry)
            say("  [ERROR]  %-28s %s" % (case["id"], type(error).__name__))
        report["policy_results"].append(entry)

    report["totals"] = {
        "calls_made": made,
        "refusals": sum(1 for r in report["policy_results"]
                        if not r["eligible"]),
        "errors": sum(1 for r in report["calls"] if r.get("error")),
        "cost_usd": round(sum(c.get("cost_usd") or 0.0
                              for c in report["calls"]), 6),
    }
    write(report, args.output)
    say("")
    say("calls %d, refusals %d, errors %d, cost $%.6f"
        % (report["totals"]["calls_made"], report["totals"]["refusals"],
           report["totals"]["errors"], report["totals"]["cost_usd"]))
    say("EXT-AI evidence written. It records what happened, including the "
        "refusals, which are the gate working rather than a shortfall.")
    return 0


def write(report, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    say("  evidence          : %s" % path)


if __name__ == "__main__":
    sys.exit(main())
