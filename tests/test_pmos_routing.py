import datetime as _dt
import json
import os
import subprocess
import sys
import time
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from pmos.routing import (
    EnvironmentSecrets,
    ModelRouter,
    ModelSpec,
    ProviderRateLimit,
    ProviderNetworkError,
    ProviderRefusal,
    ProviderResponse,
    ProviderTimeout,
    RiskTrustPolicy,
    RouteStatus,
    RoutingRequest,
)
from pmos.spend import (
    BudgetExceeded,
    SpendLedger,
    UnresolvedCharge,
    cost_certainty,
    day_scope,
    default_path,
)

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import usage_report  # noqa: E402  (path set above)


class FakeProvider:
    def __init__(self, response=None, error=None, available=True):
        self.response = response if response is not None else ProviderResponse("ok")
        self.error = error
        self.available = available
        self.calls = []

    def complete(self, model, prompt, request=None, api_key=None):
        self.calls.append((model, prompt, request, api_key))
        if self.error:
            raise self.error
        if isinstance(self.response, ProviderResponse) and self.response.actual_model is None:
            return replace(self.response, actual_model=model)
        return self.response


def spec(provider, model, **kwargs):
    defaults = dict(
        capabilities={"text"},
        tools=set(),
        context_window=1000,
        latency_ms=50,
        cost_per_1k_tokens=0.01,
        privacy_classes={"public", "internal"},
    )
    defaults.update(kwargs)
    return ModelSpec(provider, model, **defaults)


class RoutingTests(unittest.TestCase):
    def test_success_and_allowlisted_provenance(self):
        secret = "do-not-publish-credential"
        provider = FakeProvider({"output": "answer", "input_tokens": 10,
                                 "output_tokens": 5, "total_tokens": 15,
                                 "cost_usd": 0.004, "latency_ms": 21,
                                 "actual_model": "acme/fast"})
        catalog = [spec("acme", "acme/fast", credential_env="PMOS_TEST_SECRET")]
        old = os.environ.get("PMOS_TEST_SECRET")
        os.environ["PMOS_TEST_SECRET"] = secret
        try:
            decision = ModelRouter(catalog, {"acme": provider}).route(
                RoutingRequest("private prompt with secret", capabilities={"text"})
            )
        finally:
            if old is None:
                os.environ.pop("PMOS_TEST_SECRET", None)
            else:
                os.environ["PMOS_TEST_SECRET"] = old
        self.assertEqual(decision.status, RouteStatus.ROUTED)
        self.assertEqual((decision.provider, decision.model), ("acme", "acme/fast"))
        self.assertEqual(decision.provenance["requested_model"], "acme/fast")
        self.assertEqual(decision.provenance["model"], "acme/fast")
        self.assertEqual(decision.provenance["total_tokens"], 15)
        self.assertNotIn(secret, repr(decision))
        self.assertNotIn("private prompt", repr(decision))
        empty = ModelRouter(
            [spec("empty", "empty/model")],
            {"empty": FakeProvider({"output": ""})}).route(RoutingRequest())
        self.assertEqual(empty.status, RouteStatus.ERROR)

    def test_provider_reported_substitution_fails_before_confidential_data_is_accepted(self):
        provider = FakeProvider({"output": "unsafe", "actual_model": "unreviewed/public"})
        restricted = spec("p", "reviewed/restricted", privacy_classes={"restricted"})
        decision = ModelRouter([restricted], {"p": provider}).route(
            RoutingRequest(prompt="confidential customer evidence", task="summarize",
                           risk="low", privacy="confidential")
        )
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertIn("policy_violation", [attempt.reason for attempt in decision.attempts])

    def test_provider_missing_actual_model_identity_fails_closed(self):
        provider = FakeProvider({"output": "identity not proven"})
        decision = ModelRouter([spec("p", "p/exact")], {"p": provider}).route(
            RoutingRequest()
        )
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertIn("policy_violation", [attempt.reason for attempt in decision.attempts])

    def test_refusal_rate_limit_timeout_and_network_use_bounded_fallback(self):
        p1 = FakeProvider(error=ProviderRefusal())
        p2 = FakeProvider(error=ProviderRateLimit())
        p3 = FakeProvider(error=ProviderTimeout())
        p4 = FakeProvider(error=ConnectionError("network detail"))
        models = [spec("p1", "m1", priority=0), spec("p2", "m2", priority=1),
                  spec("p3", "m3", priority=2), spec("p4", "m4", priority=3)]
        decision = ModelRouter(models, {"p1": p1, "p2": p2, "p3": p3, "p4": p4}, max_attempts=3).route(
            RoutingRequest()
        )
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertEqual(decision.error_code, "fallback_exhausted")
        self.assertEqual(sum(bool(p.calls) for p in (p1, p2, p3, p4)), 3)
        self.assertEqual([a.reason for a in decision.attempts if a.outcome == "failed"],
                         ["refusal", "rate_limited", "timeout"])

    def test_unavailable_provider_and_model_are_skipped(self):
        unavailable = FakeProvider(available=False)
        healthy = FakeProvider(ProviderResponse("healthy"))
        models = [spec("offline", "missing", priority=0),
                  spec("gone", "gone-model", priority=1, available=False),
                  spec("healthy", "live", priority=2)]
        decision = ModelRouter(models, {"offline": unavailable, "healthy": healthy}).route(RoutingRequest())
        self.assertTrue(decision.ok)
        self.assertEqual(decision.model, "live")
        self.assertIn("provider unavailable", [a.reason for a in decision.attempts])
        self.assertIn("model unavailable", [a.reason for a in decision.attempts])

    def test_privacy_capability_tool_context_latency_and_budget_are_policy_filters(self):
        provider = FakeProvider()
        models = [spec("p", "wrong-privacy", privacy_classes={"public"}, tools={"search"}, latency_ms=10),
                  spec("p", "wrong-tools", privacy_classes={"confidential"}),
                  spec("p", "right", privacy_classes={"confidential"}, tools={"search"},
                       context_window=500, latency_ms=10, cost_per_1k_tokens=0.01)]
        request = RoutingRequest(privacy="confidential", capabilities={"text"}, required_tools={"search"},
                                 context_tokens=400, max_output_tokens=100,
                                 max_latency_ms=20, estimated_tokens=100)
        decision = ModelRouter(models, {"p": provider}).route(request)
        self.assertTrue(decision.ok)
        self.assertEqual(decision.model, "right")
        self.assertIn("privacy permission rejected", [a.reason for a in decision.attempts])

        blocked = ModelRouter([spec("p", "too-expensive", cost_per_1k_tokens=10)], {"p": provider}).route(
            RoutingRequest(estimated_tokens=100, budget_usd=0.1)
        )
        self.assertEqual(blocked.status, RouteStatus.BLOCKED)
        self.assertIn("budget exhausted", blocked.reason)
        with self.assertRaises(ValueError):
            spec("p", "negative-cost", cost_per_1k_tokens=-1)
        with self.assertRaises(ValueError):
            RoutingRequest(budget_usd=-1)

    def test_budget_reserves_fallbacks_and_rejects_provider_overspend(self):
        overspend = FakeProvider({"output": "not accepted", "cost_usd": 999.0,
                                  "output_tokens": 1,
                                  "actual_model": "cheap/model"})
        cheap = spec("cheap", "cheap/model", cost_per_1k_tokens=0.001)
        decision = ModelRouter([cheap], {"cheap": overspend}).route(
            RoutingRequest(budget_usd=0.01, estimated_tokens=1,
                           max_output_tokens=10)
        )
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertIn("policy_violation",
                      [attempt.reason for attempt in decision.attempts])

        first = FakeProvider(error=ProviderRateLimit())
        second = FakeProvider()
        models = [spec("first", "first/model", cost_per_1k_tokens=1.0),
                  spec("second", "second/model", cost_per_1k_tokens=1.0,
                       priority=1)]
        bounded = ModelRouter(models, {"first": first, "second": second},
                              max_attempts=2).route(
            RoutingRequest(budget_usd=0.015, max_output_tokens=10)
        )
        self.assertEqual(bounded.status, RouteStatus.ERROR)
        self.assertEqual(len(first.calls), 1)
        self.assertEqual(len(second.calls), 0)
        self.assertIn("fallback budget exhausted",
                      [attempt.reason for attempt in bounded.attempts])

    def test_spend_reservation_fit_succeeds_and_exceed_records_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("fit", 0.4, {"day:2026-09-12": 1.0})
            self.assertAlmostEqual(ledger.committed("day:2026-09-12"), 0.4)
            ledger.settle("fit", 0.35)
            self.assertAlmostEqual(ledger.committed("day:2026-09-12"), 0.35)
            with self.assertRaises(BudgetExceeded):
                ledger.reserve("overflow", 0.9, {"day:2026-09-12": 1.0})
            ledger.close()
            reopen = SpendLedger(path)
            self.assertAlmostEqual(reopen.committed("day:2026-09-12"), 0.35)
            reopen.close()

    def test_spend_two_objects_on_one_file_cannot_together_exceed_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            first = SpendLedger(path)
            second = SpendLedger(path)
            first.reserve("first", 0.6, {"day:2026-09-12": 1.0})
            with self.assertRaises(BudgetExceeded):
                second.reserve("second", 0.6, {"day:2026-09-12": 1.0})
            self.assertAlmostEqual(second.committed("day:2026-09-12"), 0.6)
            first.close()
            second.close()

    def test_spend_two_processes_started_together_share_cap(self):
        script = (
            "import sys, time\n"
            "from pathlib import Path\n"
            "from pmos.spend import SpendLedger\n"
            "path = Path(sys.argv[1])\n"
            "release = Path(sys.argv[2])\n"
            "timeout = float(sys.argv[3])\n"
            "deadline = time.time() + timeout\n"
            "while not release.exists() and time.time() < deadline:\n"
            "    time.sleep(0.01)\n"
            "if not release.exists():\n"
            "    sys.exit(2)\n"
            "try:\n"
            "    ledger = SpendLedger(str(path))\n"
            "    ledger.reserve('worker-' + str(sys.argv[4]), 0.6, "
            "{'day:2026-09-12': 1.0})\n"
            "    ledger.close()\n"
            "    sys.exit(0)\n"
            "except Exception as exc:\n"
            "    sys.stderr.write(str(exc) + '\\n')\n"
            "    sys.exit(1)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            release = Path(tmp) / "release"
            env = dict(os.environ)
            root = Path(__file__).resolve().parents[1]
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = str(root) + (os.pathsep + existing if existing else "")
            procs = [subprocess.Popen(
                [sys.executable, "-c", script, str(path), str(release), "30", name],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) for name in ("a", "b")]
            time.sleep(0.1)
            release.touch()
            results = [proc.communicate(timeout=60) for proc in procs]
            err_a, err_b = (err.decode("utf-8", "replace") for _out, err in results)
            outcomes = [proc.returncode for proc in procs]
            self.assertIn("exceeded", err_a + err_b)
            self.assertIn(0, outcomes)
            self.assertIn(1, outcomes)
            self.assertEqual(outcomes.count(0), 1)
            self.assertEqual(outcomes.count(1), 1)
            self.assertNotEqual(err_a + err_b, "")

    def test_spend_settle_with_real_cost_charges_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("call", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("call", 0.08)
            self.assertAlmostEqual(ledger.committed("day:2026-09-12"), 0.08)
            ledger.close()

    def test_spend_settle_none_keeps_reservation_and_blocks_until_reconcile(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("unknown", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("unknown", None)
            self.assertAlmostEqual(ledger.committed("day:2026-09-12"), 0.1)
            with self.assertRaises(UnresolvedCharge):
                ledger.reserve("next", 0.1, {"day:2026-09-12": 1.0})
            ledger.reconcile("unknown", 0.07)
            ledger.reserve("next", 0.1, {"day:2026-09-12": 1.0})
            ledger.close()

    def test_spend_reservation_never_settled_still_counts_after_reopen(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("abandoned", 0.4, {"day:2026-09-12": 1.0})
            ledger.close()
            reopen = SpendLedger(path)
            self.assertAlmostEqual(reopen.committed("day:2026-09-12"), 0.4)
            reopen.close()

    def test_spend_invalid_amounts_raise_value_error(self):
        cases = [float("nan"), float("inf"), float("-inf"), -0.1, True, False]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            for value in cases:
                with self.assertRaises(ValueError):
                    ledger.reserve("k-%s" % id(value), value, {"day:2026-09-12": 1.0})
                with self.assertRaises(ValueError):
                    ledger.reserve("k-cap-%s" % id(value), 0.1,
                                   {"day:2026-09-12": value})
                with self.assertRaises(ValueError):
                    ledger.reserve("k-ext-%s" % id(value), 0.1,
                                   {"day:2026-09-12": 1.0},
                                   external={"day:2026-09-12": value})
            ledger.reserve("good", 0.1, {"day:2026-09-12": 1.0})
            for value in cases:
                with self.assertRaises(ValueError):
                    ledger.settle("good", value)
            ledger.close()

    def test_spend_default_path_honours_env_and_avoids_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ledger.sqlite"
            with mock.patch.dict(os.environ, {"PMOS_SPEND_LEDGER": str(target)}):
                self.assertEqual(default_path(), target)
            with mock.patch.dict(os.environ):
                os.environ.pop("PMOS_SPEND_LEDGER", None)
                self.assertTrue(default_path().is_absolute())
                repo = Path(__file__).resolve().parents[1]
                self.assertFalse(str(default_path()).startswith(str(repo)))

    def test_spend_day_and_task_scopes_refuse_when_either_exceeded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            scope = day_scope(_dt.datetime(2026, 9, 12, 12, 0, 0,
                                           tzinfo=_dt.timezone.utc))
            self.assertEqual(scope, "day:2026-09-12")
            limits = {scope: 1.0, "task:build": 0.5}
            ledger.reserve("first", 0.4, limits)
            with self.assertRaises(BudgetExceeded) as ctx1:
                ledger.reserve("day-breach", 0.7, limits)
            self.assertIn(scope, str(ctx1.exception))
            with self.assertRaises(BudgetExceeded) as ctx2:
                ledger.reserve("task-breach", 0.2, limits)
            self.assertIn("task:build", str(ctx2.exception))
            ledger.close()
        self.assertEqual(day_scope(_dt.datetime(2026, 9, 12)), "day:2026-09-12")

    def _run_spend_cli(self, args, env):
        proc = subprocess.run(
            [sys.executable, "-m", "pmos.spend"] + list(args),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        return proc.returncode, (proc.stdout or b"").decode("utf-8", "replace"), \
            (proc.stderr or b"").decode("utf-8", "replace")

    def _spend_env(self):
        env = dict(os.environ)
        root = Path(__file__).resolve().parents[1]
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(root) + (os.pathsep + existing if existing else "")
        return env

    def _run_usage_report(self, args, env):
        proc = subprocess.run(
            [sys.executable, str(TOOLS / "usage_report.py")] + list(args),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        return proc.returncode, (proc.stdout or b"").decode("utf-8", "replace"), \
            (proc.stderr or b"").decode("utf-8", "replace")

    def test_spend_cli_status_missing_ledger_reports_without_creating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            env = self._spend_env()
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "status"], env)
            self.assertEqual(code, 0, err)
            self.assertIn("no ledger exists", out)
            self.assertIn(str(path), out)
            self.assertFalse(path.exists())

    def test_spend_cli_status_lists_unknown_and_open_reservations(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("unknown", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("unknown", None)
            ledger.reserve("open", 0.2, {"task:build": 1.0})
            ledger.close()
            env = self._spend_env()
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "status"], env)
            self.assertEqual(code, 0, err)
            lines = out.splitlines()
            # The ledger path, one line per reservation, then the two counts.
            self.assertEqual(len(lines), 5, out)
            self.assertIn("ledger: %s" % path, lines[0])
            self.assertIn("unknown", lines[1])
            self.assertIn("open", lines[2])
            self.assertIn("unresolved: 1", lines)
            self.assertIn("open: 1", lines)
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "status", "--json"], env)
            self.assertEqual(code, 0, err)
            payload = json.loads(out)
            self.assertEqual(payload["path"], str(path))
            self.assertEqual(len(payload["unresolved"]), 1)
            self.assertEqual(len(payload["open"]), 1)
            self.assertEqual(payload["unresolved"][0]["key"], "unknown")
            self.assertEqual(payload["open"][0]["key"], "open")

    def test_spend_cli_reconcile_with_evidence_settles_reservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("unknown", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("unknown", None)
            ledger.close()
            env = self._spend_env()
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "reconcile", "unknown", "0.07",
                 "invoice", "2026-09", "shows", "seven", "cents"], env)
            self.assertEqual(code, 0, err)
            self.assertIn("unknown", out)
            self.assertIn("0.07", out)
            reopen = SpendLedger(path)
            self.assertEqual(reopen.unresolved(), [])
            entries = reopen.reservations("settled")
            self.assertEqual(len(entries), 1)
            self.assertIn("invoice 2026-09 shows seven cents", entries[0]["note"])
            reopen.close()

    def test_spend_cli_reconcile_rejects_bad_amounts_evidence_and_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("unknown", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("unknown", None)
            ledger.reserve("openly", 0.2, {"task:build": 1.0})
            ledger.close()
            env = self._spend_env()
            evidence = "invoice 2026-09"
            bad_cases = [
                ("unknown", "nan", evidence),
                ("unknown", "-0.5", evidence),
                ("unknown", "0.07", "short"),
                ("openly", "0.07", evidence),
            ]
            for key, usd, evidence_value in bad_cases:
                words = evidence_value.split(" ")
                code, out, err = self._run_spend_cli(
                    ["--ledger", str(path), "reconcile", key, usd] + words, env)
                self.assertEqual(code, 2, (key, usd, evidence_value, out, err))
                self.assertNotEqual(err, "")
                reopen = SpendLedger(path)
                entry = reopen.reservations()[0]
                self.assertEqual(entry["state"], "unknown")
                reopen.close()
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "reconcile", "missing", "0.07"] +
                evidence.split(" "), env)
            self.assertEqual(code, 2, err)
            reopen = SpendLedger(path)
            self.assertEqual(len(reopen.reservations("unknown")), 1)
            reopen.close()

    def test_spend_cli_reconcile_refuses_a_missing_ledger_without_creating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            code, out, err = self._run_spend_cli(
                ["--ledger", str(path), "reconcile", "missing", "0.07",
                 "invoice", "2026-09", "total"], self._spend_env())
            self.assertEqual(code, 2, err)
            self.assertIn("no ledger exists", err)
            self.assertFalse(path.exists())

    def test_spend_reservations_rejects_unknown_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("call", 0.1, {"day:2026-09-12": 1.0})
            with self.assertRaises(ValueError):
                ledger.reservations(state="bogus")
            ledger.close()

    # ------------------------------------------------------- S08: usage report

    def test_spend_reserve_and_settle_accept_optional_usage_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("billed", 0.10, {"task:S08": 1.0},
                           operation="task_dispatch", task_id="S08",
                           context_version="v1")
            ledger.settle("billed", 0.05, resolved_model="glm-5.2",
                          provider="openrouter", cache_disposition="miss",
                          success=True)
            ledger.reserve("open-call", 0.20, {"task:S08": 1.0},
                           operation="probe", task_id="S08",
                           context_version="v1")
            entries = {entry["key"]: entry for entry in ledger.reservations()}
            billed = entries["billed"]
            self.assertEqual(billed["operation"], "task_dispatch")
            self.assertEqual(billed["task_id"], "S08")
            self.assertEqual(billed["context_version"], "v1")
            self.assertEqual(billed["resolved_model"], "glm-5.2")
            self.assertEqual(billed["provider"], "openrouter")
            self.assertEqual(billed["cache_disposition"], "miss")
            self.assertIs(billed["success"], True)
            self.assertEqual(billed["cost_certainty"], "billed")
            open_entry = entries["open-call"]
            self.assertIsNone(open_entry["resolved_model"])
            self.assertIsNone(open_entry["success"])
            self.assertEqual(open_entry["cost_certainty"],
                             "reserved worst case, not yet settled")
            ledger.settle("open-call", None, resolved_model="minimax-m3",
                          provider="openrouter", cache_disposition="hit",
                          success=False)
            unknown_entry = ledger.reservations("unknown")[0]
            self.assertEqual(unknown_entry["resolved_model"], "minimax-m3")
            self.assertIs(unknown_entry["success"], False)
            self.assertEqual(unknown_entry["cost_certainty"], "unknown")
            ledger.close()

    def test_spend_optional_usage_fields_default_to_none_and_reject_bad_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("bare", 0.1, {"day:2026-09-12": 1.0})
            ledger.settle("bare", 0.05)
            entry = ledger.reservations()[0]
            for field in ("operation", "task_id", "context_version",
                         "resolved_model", "provider", "cache_disposition",
                         "success"):
                self.assertIsNone(entry[field])
            with self.assertRaises(ValueError):
                ledger.reserve("bad-op", 0.1, {"day:2026-09-12": 1.0},
                               operation="")
            with self.assertRaises(ValueError):
                ledger.reserve("bad-task", 0.1, {"day:2026-09-12": 1.0},
                               task_id=123)
            ledger.reserve("ok", 0.1, {"day:2026-09-12": 1.0})
            with self.assertRaises(ValueError):
                ledger.settle("ok", 0.05, success="yes")
            ledger.close()

    def test_spend_ledger_migration_adds_usage_columns_to_an_old_schema_file(self):
        import sqlite3 as _sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            raw = _sqlite3.connect(str(path))
            raw.execute(
                "CREATE TABLE reservations ("
                "key TEXT PRIMARY KEY,"
                "reserved_usd REAL NOT NULL,"
                "charged_usd REAL,"
                "state TEXT NOT NULL CHECK (state IN ('open','settled','unknown')),"
                "created_at REAL NOT NULL,"
                "note TEXT NOT NULL DEFAULT ''"
                ")"
            )
            raw.execute(
                "CREATE TABLE reservation_scopes ("
                "key TEXT NOT NULL, scope TEXT NOT NULL, "
                "PRIMARY KEY (key, scope))"
            )
            raw.execute(
                "INSERT INTO reservations (key, reserved_usd, charged_usd, "
                "state, created_at, note) VALUES "
                "('legacy', 0.2, 0.2, 'settled', 1700000000.0, '')"
            )
            raw.execute(
                "INSERT INTO reservation_scopes (key, scope) VALUES "
                "('legacy', 'day:2026-09-12')"
            )
            raw.commit()
            raw.close()

            ledger = SpendLedger(path)
            entries = {entry["key"]: entry for entry in ledger.reservations()}
            legacy = entries["legacy"]
            self.assertEqual(legacy["state"], "settled")
            self.assertEqual(legacy["cost_certainty"], "billed")
            for field in ("operation", "task_id", "context_version",
                         "resolved_model", "provider", "cache_disposition",
                         "success"):
                self.assertIsNone(legacy[field])
            ledger.reserve("new", 0.1, {"day:2026-09-12": 1.0},
                           operation="task_dispatch", task_id="S08")
            ledger.settle("new", 0.05, resolved_model="glm-5.2", success=True)
            entries_after = {entry["key"]: entry
                             for entry in ledger.reservations()}
            new_entry = entries_after["new"]
            self.assertEqual(new_entry["operation"], "task_dispatch")
            self.assertEqual(new_entry["resolved_model"], "glm-5.2")
            ledger.close()

    def test_spend_ledger_migration_tolerates_a_column_another_process_added(self):
        # Two processes opening one old ledger can both read the schema before
        # either adds a column; the slower ALTER must not fail the open, and
        # any other ALTER failure must still surface.
        import sqlite3 as _sqlite3
        from pmos import spend as _spend

        class StaleSchema:
            def __init__(self, conn):
                self.conn = conn

            def execute(self, sql, *args):
                if sql.startswith("PRAGMA table_info"):
                    return iter([(0, "key"), (1, "reserved_usd")])
                return self.conn.execute(sql, *args)

        class LockedAlter(StaleSchema):
            def execute(self, sql, *args):
                if sql.startswith("ALTER"):
                    raise _sqlite3.OperationalError("database is locked")
                return super().execute(sql, *args)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            SpendLedger(path).close()
            raw = _sqlite3.connect(str(path))
            try:
                _spend._ensure_optional_columns(StaleSchema(raw))
                with self.assertRaises(_sqlite3.OperationalError):
                    _spend._ensure_optional_columns(LockedAlter(raw))
            finally:
                raw.close()

    def test_pmos_spend_cost_certainty_labels(self):
        self.assertEqual(cost_certainty("open"),
                         "reserved worst case, not yet settled")
        self.assertEqual(cost_certainty("settled"), "billed")
        self.assertEqual(cost_certainty("unknown"), "unknown")
        with self.assertRaises(ValueError):
            cost_certainty("bogus")

    def test_usage_report_summarizes_denominators_cost_certainty_and_groupings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("k1", 0.10, {"task:S08": 5.0},
                           operation="task_dispatch", task_id="S08",
                           context_version="v1")
            ledger.settle("k1", 0.05, resolved_model="glm-5.2",
                          provider="openrouter", cache_disposition="miss",
                          success=True)
            ledger.reserve("k2", 0.20, {"task:S08": 5.0}, operation="probe",
                           task_id="S08", context_version="v1")
            ledger.settle("k2", None, resolved_model="minimax-m3",
                          provider="openrouter", cache_disposition="hit",
                          success=False)
            ledger.reserve("k3", 0.15, {"task:S04": 5.0},
                           operation="task_dispatch", task_id="S04",
                           context_version="v1")
            ledger.close()

            report = usage_report.build_report(path)
            overall = report["sections"]["overall"]
            self.assertEqual(overall["attempted"], 3)
            self.assertEqual(overall["completed"], 2)
            self.assertEqual(overall["denominator"], "2/3")
            self.assertEqual(overall["quality_failures"], 1)
            self.assertAlmostEqual(overall["billed_usd"], 0.05)
            self.assertAlmostEqual(overall["reserved_worst_case_usd"], 0.15)
            self.assertAlmostEqual(overall["unresolved_worst_case_usd"], 0.20)

            by_task = report["sections"]["by_task"]
            self.assertEqual(by_task["S08"]["denominator"], "2/2")
            self.assertEqual(by_task["S04"]["denominator"], "0/1")

            by_cost_certainty = report["sections"]["by_cost_certainty"]
            self.assertIn("billed", by_cost_certainty)
            self.assertIn("unknown", by_cost_certainty)
            self.assertIn("reserved worst case, not yet settled",
                          by_cost_certainty)
            self.assertIsNone(report["suite_coverage"])

    def test_usage_report_marks_unmetered_usage_unavailable_never_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("k1", 0.10, {"task:S08": 5.0},
                           operation="task_dispatch", task_id="S08")
            ledger.settle("k1", 0.05, success=True)
            ledger.close()
            suite = [
                {"task_id": "S08", "operation": "task_dispatch",
                 "metered": True},
                {"task_id": "SUB1", "operation": "task_dispatch",
                 "metered": False, "completed": True, "success": True,
                 "label": "subscription tier"},
                {"task_id": "SUB2", "operation": "task_dispatch",
                 "metered": False},
            ]
            report = usage_report.build_report(path, suite)
            coverage = report["suite_coverage"]
            self.assertEqual(coverage["tasks"]["SUB1"]["billed_usd"],
                             "unavailable")
            self.assertEqual(coverage["tasks"]["SUB1"]["completed"], True)
            self.assertEqual(coverage["tasks"]["SUB1"]["success"], True)
            self.assertEqual(coverage["tasks"]["SUB2"]["billed_usd"],
                             "unavailable")
            self.assertIsNone(coverage["tasks"]["SUB2"]["completed"])
            self.assertIsNone(coverage["tasks"]["SUB2"]["success"])
            self.assertEqual(coverage["tasks"]["S08"]["billed_usd"], 0.05)
            self.assertEqual(coverage["denominator"], "2/3")
            self.assertEqual(coverage["unavailable_cost_tasks"], 2)

    def test_usage_report_task_suite_file_round_trip_and_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            suite_path = Path(tmp) / "suite.json"
            suite_path.write_text(json.dumps([
                {"task_id": "S08", "metered": True},
                {"task_id": "SUB1", "metered": False, "completed": True,
                 "success": True},
            ]), encoding="utf-8")
            suite = usage_report.load_task_suite(suite_path)
            self.assertEqual(len(suite), 2)
            self.assertEqual(suite[0]["task_id"], "S08")
            self.assertTrue(suite[0]["metered"])
            self.assertFalse(suite[1]["metered"])

            dup_path = Path(tmp) / "dup.json"
            dup_path.write_text(json.dumps([
                {"task_id": "S08"}, {"task_id": "S08"},
            ]), encoding="utf-8")
            with self.assertRaises(ValueError):
                usage_report.load_task_suite(dup_path)

            bad_path = Path(tmp) / "bad.json"
            bad_path.write_text(json.dumps([{"operation": "x"}]),
                                encoding="utf-8")
            with self.assertRaises(ValueError):
                usage_report.load_task_suite(bad_path)

            not_list_path = Path(tmp) / "notlist.json"
            not_list_path.write_text(json.dumps({"task_id": "S08"}),
                                     encoding="utf-8")
            with self.assertRaises(ValueError):
                usage_report.load_task_suite(not_list_path)

            self.assertEqual(usage_report.load_task_suite(None), [])

    def test_usage_report_compare_flags_fixed_suite_mismatch_and_matches_savings_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            before_path = Path(tmp) / "before.sqlite"
            before_ledger = SpendLedger(before_path)
            before_ledger.reserve("b1", 0.10, {"task:S08": 5.0},
                                  operation="task_dispatch", task_id="S08")
            before_ledger.settle("b1", 0.08, success=True)
            before_ledger.close()

            after_path = Path(tmp) / "after.sqlite"
            after_ledger = SpendLedger(after_path)
            after_ledger.reserve("a1", 0.10, {"task:S08": 5.0},
                                 operation="task_dispatch", task_id="S08")
            after_ledger.settle("a1", 0.02, success=True)
            after_ledger.close()

            suite = [{"task_id": "S08", "metered": True}]
            before_report = usage_report.build_report(before_path, suite)
            after_report = usage_report.build_report(after_path, suite)
            diff = usage_report.compare_reports(before_report, after_report)
            self.assertTrue(diff["fixed_suite_match"])
            self.assertAlmostEqual(diff["overall"]["delta"]["billed_usd"],
                                   -0.06)
            self.assertEqual(diff["suite_coverage"]["completed_delta"], 0)

            mismatched_suite = [{"task_id": "OTHER", "metered": True}]
            mismatched_after = usage_report.build_report(after_path,
                                                          mismatched_suite)
            mismatched_diff = usage_report.compare_reports(before_report,
                                                            mismatched_after)
            self.assertFalse(mismatched_diff["fixed_suite_match"])

            no_suite_report = usage_report.build_report(after_path)
            unavailable_diff = usage_report.compare_reports(before_report,
                                                             no_suite_report)
            self.assertIsNone(unavailable_diff["fixed_suite_match"])
            self.assertNotIn("suite_coverage", unavailable_diff)

    def test_usage_report_cli_json_and_text_against_a_scratch_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            ledger = SpendLedger(path)
            ledger.reserve("k1", 0.10, {"task:S08": 5.0},
                           operation="task_dispatch", task_id="S08",
                           context_version="v1")
            ledger.settle("k1", 0.05, resolved_model="glm-5.2",
                          provider="openrouter", cache_disposition="miss",
                          success=True)
            ledger.close()
            env = self._spend_env()

            code, out, err = self._run_usage_report(
                ["--ledger", str(path)], env)
            self.assertEqual(code, 0, err)
            self.assertIn("overall totals: 1/1 completed of attempted", out)
            self.assertIn("by_task:", out)

            code, out, err = self._run_usage_report(
                ["--ledger", str(path), "--json"], env)
            self.assertEqual(code, 0, err)
            payload = json.loads(out)
            self.assertEqual(payload["sections"]["overall"]["denominator"],
                             "1/1")
            self.assertIsNone(payload["suite_coverage"])

    def test_usage_report_cli_missing_ledger_reports_empty_without_creating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.sqlite"
            env = self._spend_env()
            code, out, err = self._run_usage_report(
                ["--ledger", str(path)], env)
            self.assertEqual(code, 0, err)
            self.assertIn("0/0 completed of attempted", out)
            self.assertFalse(path.exists())

    def test_usage_report_cli_compare_refuses_a_missing_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            after_path = Path(tmp) / "after.sqlite"
            ledger = SpendLedger(after_path)
            ledger.reserve("k1", 0.10, {"task:S08": 5.0})
            ledger.settle("k1", 0.05)
            ledger.close()
            missing = Path(tmp) / "missing.sqlite"
            env = self._spend_env()
            code, out, err = self._run_usage_report(
                ["--compare", str(missing), str(after_path)], env)
            self.assertEqual(code, 2, out + err)
            self.assertIn("no such ledger or report file", err)

    def test_bounded_budget_call_under_the_cap_is_not_rejected(self):
        provider = FakeProvider({"output": "answer", "input_tokens": 4,
                                 "output_tokens": 2, "total_tokens": 6,
                                 "cost_usd": 0.004, "latency_ms": 5,
                                 "actual_model": "cheap/model"})
        decision = ModelRouter(
            [spec("cheap", "cheap/model", cost_per_1k_tokens=0.5)],
            {"cheap": provider}).route(
                RoutingRequest(budget_usd=0.01, estimated_tokens=1,
                               max_output_tokens=10))
        self.assertTrue(decision.ok)
        self.assertEqual(decision.model, "cheap/model")
        self.assertEqual(len(provider.calls), 1)
        self.assertNotIn("fallback budget exhausted",
                         [attempt.reason for attempt in decision.attempts])
        self.assertNotIn("policy_violation",
                         [attempt.reason for attempt in decision.attempts])

    def test_budget_counts_policy_failed_paid_attempts_before_fallback(self):
        first = FakeProvider({
            "output": "charged but rejected", "output_tokens": 1,
            "total_tokens": 1, "cost_usd": 0.006,
            "actual_model": "unapproved/substitute",
        })
        second = FakeProvider({
            "output": "would exceed aggregate", "output_tokens": 1,
            "total_tokens": 1, "cost_usd": 0.006,
            "actual_model": "second/model",
        })
        decision = ModelRouter([
            spec("first", "first/model", priority=0, cost_per_1k_tokens=0.5),
            spec("second", "second/model", priority=1, cost_per_1k_tokens=0.5),
        ], {"first": first, "second": second}, max_attempts=2).route(
            RoutingRequest(budget_usd=0.01, max_output_tokens=10))
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertEqual(len(first.calls), 1)
        self.assertEqual(len(second.calls), 0)
        self.assertIn("fallback budget exhausted",
                      [attempt.reason for attempt in decision.attempts])

    def test_authoritative_usage_cannot_overrun_context_or_lie_about_total(self):
        too_large = FakeProvider({
            "output": "x", "input_tokens": 1000, "output_tokens": 1,
            "total_tokens": 1001, "actual_model": "p/tiny",
        })
        decision = ModelRouter(
            [spec("p", "p/tiny", context_window=10)], {"p": too_large}).route(
                RoutingRequest(max_output_tokens=1))
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertIn("policy_violation",
                      [attempt.reason for attempt in decision.attempts])

        inconsistent = FakeProvider({
            "output": "x", "input_tokens": 5, "output_tokens": 2,
            "total_tokens": 6, "actual_model": "p/roomy",
        })
        bad_total = ModelRouter(
            [spec("p", "p/roomy", context_window=100)],
            {"p": inconsistent}).route(RoutingRequest(max_output_tokens=2))
        self.assertEqual(bad_total.status, RouteStatus.ERROR)

        prompt_blocked = ModelRouter(
            [spec("p", "p/tiny", context_window=10)],
            {"p": FakeProvider()}).route(
                RoutingRequest(prompt="x" * 10, max_output_tokens=1))
        self.assertEqual(prompt_blocked.status, RouteStatus.BLOCKED)
        self.assertIn("context window too small", prompt_blocked.reason)

    def test_discovery_failure_is_bounded_and_never_leaks_exception_text(self):
        secret = "catalog-secret-that-must-never-escape"

        def failed_catalog():
            raise ProviderNetworkError(secret)

        decision = ModelRouter(failed_catalog, {}).route(RoutingRequest())
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertEqual(decision.error_code, "catalog_discovery_failed")
        self.assertNotIn(secret, repr(decision))

    def test_actual_and_wall_latency_are_enforced_and_timeout_is_forwarded(self):
        class SlowProvider:
            def __init__(self, *, reported=None, sleep_seconds=0):
                self.reported = reported
                self.sleep_seconds = sleep_seconds
                self.timeouts = []

            def complete(self, model, prompt, request=None, timeout_seconds=None,
                         api_key=None):
                self.timeouts.append((timeout_seconds, request.max_latency_ms))
                if self.sleep_seconds:
                    time.sleep(self.sleep_seconds)
                return ProviderResponse(
                    "bounded", output_tokens=1, latency_ms=self.reported,
                    actual_model=model)

        reported = SlowProvider(reported=1000)
        rejected = ModelRouter(
            [spec("p", "p/fast", latency_ms=1)], {"p": reported}).route(
                RoutingRequest(max_latency_ms=20, max_output_tokens=2))
        self.assertEqual(rejected.status, RouteStatus.ERROR)
        self.assertLessEqual(reported.timeouts[0][0], 0.02)
        self.assertLessEqual(reported.timeouts[0][1], 20)

        wall = SlowProvider(sleep_seconds=0.02)
        wall_rejected = ModelRouter(
            [spec("p", "p/fast", latency_ms=1)], {"p": wall}).route(
                RoutingRequest(max_latency_ms=5, max_output_tokens=2))
        self.assertEqual(wall_rejected.status, RouteStatus.ERROR)

    def test_missing_usage_cannot_hide_an_oversized_output(self):
        provider = FakeProvider({"output": "x" * 1000,
                                 "actual_model": "p/exact"})
        decision = ModelRouter(
            [spec("p", "p/exact")], {"p": provider}).route(
                RoutingRequest(max_output_tokens=1))
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertIn("policy_violation",
                      [attempt.reason for attempt in decision.attempts])

    def test_model_metadata_rejects_truthy_strings_and_string_collections(self):
        for field in ("available", "certified", "free"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                spec("p", "m", **{field: "false"})
        for value in ("text", {"text": True}, {"text", 1}):
            with self.subTest(capabilities=value), self.assertRaises(ValueError):
                spec("p", "m", capabilities=value)
        with self.assertRaises(ValueError):
            spec("p", "m", credential_env="NOT-VALID=VALUE")
        with self.assertRaises(ValueError):
            spec("provider\nforged", "m")
        with self.assertRaises(ValueError):
            spec("p", "m", tools={"safe\nforged"})
        for kwargs in ({"risk": True}, {"privacy": 1},
                       {"capabilities": "text"}, {"prompt": b"bytes"},
                       {"task": "forged\nmetadata"}):
            with self.subTest(request=kwargs), self.assertRaises(ValueError):
                RoutingRequest(**kwargs)

    def test_privacy_permission_cannot_downgrade_data_classification(self):
        provider = FakeProvider()
        downgraded = RoutingRequest(privacy="restricted", privacy_permission="public")
        self.assertEqual(downgraded.effective_privacy, "restricted")
        blocked = ModelRouter(
            [spec("p", "public-only", privacy_classes={"public"})], {"p": provider}
        ).route(downgraded)
        self.assertEqual(blocked.status, RouteStatus.BLOCKED)
        self.assertIn("privacy permission rejected", blocked.reason)

        elevated = RoutingRequest(privacy="public", privacy_permission="restricted")
        self.assertEqual(elevated.effective_privacy, "restricted")
        allowed = ModelRouter(
            [spec("p", "restricted", privacy_classes={"restricted"})], {"p": provider}
        ).route(elevated)
        self.assertTrue(allowed.ok)

        unknown = ModelRouter(
            [spec("p", "restricted", privacy_classes={"restricted"})], {"p": provider}
        ).route(RoutingRequest(privacy="restricted", privacy_permission="internet"))
        self.assertEqual(unknown.status, RouteStatus.BLOCKED)
        self.assertIn("unknown privacy class", unknown.reason)

    def test_free_or_uncertified_models_are_rejected_for_high_risk(self):
        free = FakeProvider({"output": "ok", "actual_model": "free"})
        arbitrary_claim = spec("free", "free", free=True, certified=True,
                               certified_for={"architecture"})
        rejected = ModelRouter([arbitrary_claim], {"free": free}).route(
            RoutingRequest(task="architecture", risk="high")
        )
        self.assertEqual(rejected.status, RouteStatus.BLOCKED)
        self.assertIn("explicit model trust policy", rejected.reason)

        policy = RiskTrustPolicy({("free", "free"): {"architecture"}})
        missing_metadata = ModelRouter(
            [spec("free", "free", free=True)], {"free": free},
            risk_trust_policy=policy,
        ).route(RoutingRequest(task="architecture", risk="high"))
        self.assertEqual(missing_metadata.status, RouteStatus.BLOCKED)
        self.assertIn("certified model metadata", missing_metadata.reason)

        certified = ModelRouter(
            [arbitrary_claim], {"free": free}, risk_trust_policy=policy,
        ).route(RoutingRequest(task="architecture", risk="high"))
        self.assertTrue(certified.ok)

        mismatched_policy = RiskTrustPolicy({("free", "another-model"): {"architecture"}})
        mismatch = ModelRouter(
            [arbitrary_claim], {"free": free}, risk_trust_policy=mismatched_policy,
        ).route(RoutingRequest(task="architecture", risk="high"))
        self.assertEqual(mismatch.status, RouteStatus.BLOCKED)

        resolved_elsewhere = FakeProvider({"output": "unsafe", "actual_model": "free/other"})
        changed = ModelRouter(
            [arbitrary_claim], {"free": resolved_elsewhere}, risk_trust_policy=policy,
        ).route(RoutingRequest(task="architecture", risk="high"))
        self.assertEqual(changed.status, RouteStatus.ERROR)
        self.assertIn("policy_violation", [attempt.reason for attempt in changed.attempts])

        with self.assertRaises(ValueError):
            RiskTrustPolicy({("*", "free"): {"architecture"}})

    def test_dynamic_catalog_and_fallback_exhaustion_are_deterministic(self):
        state = [[spec("p", "first"), spec("p", "second", priority=1)]]
        provider = FakeProvider(error=ProviderRefusal())
        router = ModelRouter(lambda: state[0], {"p": provider}, max_attempts=1)
        first = router.route(RoutingRequest())
        self.assertEqual([a.model for a in first.attempts if a.outcome == "failed"], ["first"])
        state[0] = [spec("p", "new")]
        provider.error = None
        provider.response = {"output": "new answer", "actual_model": "new"}
        second = router.route(RoutingRequest())
        self.assertEqual(second.model, "new")

    def test_no_eligible_model_is_explicitly_blocked(self):
        decision = ModelRouter([], {}).route(RoutingRequest())
        self.assertEqual(decision.status, RouteStatus.BLOCKED)
        self.assertEqual(decision.error_code, "no_eligible_model")
        self.assertFalse(decision.ok)

    def test_secret_store_repr_and_provider_failures_never_leak(self):
        secret = "SUPER-SECRET-123"
        secrets = EnvironmentSecrets({"KEY_NAME": secret})
        self.assertNotIn(secret, repr(secrets))
        provider = FakeProvider(error=ProviderRefusal(secret))
        decision = ModelRouter([spec("p", "m", credential_env="KEY_NAME")], {"p": provider}, secrets=secrets).route(
            RoutingRequest("prompt must not appear")
        )
        text = repr(decision)
        self.assertNotIn(secret, text)
        self.assertNotIn("prompt must not appear", text)
        self.assertEqual(decision.error_code, "fallback_exhausted")


if __name__ == "__main__":
    unittest.main()
