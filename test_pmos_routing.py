import os
import time
import unittest
from dataclasses import replace

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
