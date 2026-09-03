import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from pmos.openrouter import (
    OpenRouterAuthMissing,
    OpenRouterConfig,
    OpenRouterMalformedResponse,
    OpenRouterProvider,
    OpenRouterRedirectError,
    OpenRouterResponseTooLarge,
)
from pmos.routing import (
    EnvironmentSecrets,
    ModelRouter,
    ModelSpec,
    ProviderNetworkError,
    RouteStatus,
    RoutingRequest,
)
from pmos.skills import SkillContractError, SkillRegistry


class FakeResponse:
    def __init__(self, body, status=200, url=None):
        self.body = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.status = status
        self.url = url
        self.closed = False

    def read(self, size=-1):
        return self.body if size < 0 else self.body[:size]

    def close(self):
        self.closed = True

    def geturl(self):
        return self.url


class OpenRouterTests(unittest.TestCase):
    def setUp(self):
        self.environ = {"TEST_OPENROUTER_KEY": "secret-value-that-must-not-leak"}
        self.requests = []
        self.timeouts = []

    def opener(self, response):
        def open_request(request, timeout=None):
            self.requests.append(request)
            self.timeouts.append(timeout)
            return response if isinstance(response, FakeResponse) else FakeResponse(response)
        return open_request

    def provider(self, response):
        return OpenRouterProvider(
            OpenRouterConfig(api_key_env="TEST_OPENROUTER_KEY", base_url="https://router.test",
                             attribution_headers={"X-Title": "PMOS tests"},
                             trusted_hosts={"router.test"}),
            environ=self.environ, urlopen=self.opener(response))

    def test_catalog_parses_models_and_free_pricing(self):
        provider = self.provider({"data": [{
            "id": "vendor/exact-id", "context_length": 8192,
            "supported_parameters": ["tools", "temperature"],
            "architecture": {"input_modalities": ["text"], "output_modalities": ["text"]},
            "pricing": {"prompt": "0", "completion": "0"},
        }]})
        models = provider.discover()
        self.assertEqual(models[0].model, "vendor/exact-id")
        self.assertTrue(models[0].free)
        self.assertEqual(models[0].context_window, 8192)
        self.assertIn("tools", models[0].capabilities)
        self.assertEqual(self.requests[0].get_method(), "GET")

    def test_chat_uses_exact_id_and_actual_model(self):
        provider = self.provider({
            "model": "vendor/actual-id", "choices": [{"message": {"content": "hello"}}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
        })
        response = provider.complete("vendor/requested-id", "private prompt")
        self.assertEqual(response.output, "hello")
        self.assertEqual(response.actual_model, "vendor/actual-id")
        self.assertEqual(response.total_tokens, 5)
        self.assertNotIn("private prompt", repr(provider))
        self.assertNotIn(self.environ["TEST_OPENROUTER_KEY"], repr(provider))
        sent = json.loads(self.requests[0].data.decode())
        self.assertEqual(sent["model"], "vendor/requested-id")
        self.assertEqual(sent["max_tokens"], 1024)

    def test_auth_absence_429_malformed_and_oversize_are_safe(self):
        missing = OpenRouterProvider(OpenRouterConfig(api_key_env="MISSING"), environ={})
        with self.assertRaises(OpenRouterAuthMissing):
            missing.discover()
        limited = self.provider({"error": {"code": "429", "type": "rate_limit"}})
        with self.assertRaises(Exception) as raised:
            limited.discover()
        self.assertEqual(getattr(raised.exception, "code", None), "rate_limited")
        malformed = self.provider({"not": "a catalog"})
        with self.assertRaises(OpenRouterMalformedResponse):
            malformed.discover()
        huge = self.provider({"data": []})
        huge.config = OpenRouterConfig(api_key_env="TEST_OPENROUTER_KEY", max_response_bytes=1024)
        huge._urlopen = self.opener(b"x" * 2048)
        with self.assertRaises(OpenRouterResponseTooLarge):
            huge.discover()

    def test_base_url_override_requires_an_exact_trusted_https_host(self):
        with self.assertRaises(ValueError):
            OpenRouterConfig(base_url="https://router.test")
        with self.assertRaises(ValueError):
            OpenRouterConfig(base_url="https://openrouter.ai.attacker.test")
        with self.assertRaises(ValueError):
            OpenRouterConfig(base_url="https://user@openrouter.ai")
        trusted = OpenRouterConfig(
            base_url="https://router.test", trusted_hosts={"router.test"})
        self.assertEqual(trusted.base_url, "https://router.test")

    def test_insecure_test_transport_is_loopback_injected_and_credential_free(self):
        requests = []

        def opener(request, timeout=None):
            requests.append(request)
            return FakeResponse({"data": []})

        class NoCredentialAccess(dict):
            def get(self, key, default=None):
                raise AssertionError("credential must not be read for plaintext test transport")

        config = OpenRouterConfig(
            base_url="http://127.0.0.1:8765",
            trusted_hosts={"127.0.0.1"},
            allow_insecure_test_transport=True,
        )
        with self.assertRaises(ValueError):
            OpenRouterProvider(config, environ=NoCredentialAccess())
        provider = OpenRouterProvider(
            config, environ=NoCredentialAccess(), urlopen=opener)
        self.assertEqual(provider.discover(), [])
        self.assertIsNone(requests[0].get_header("Authorization"))

        with self.assertRaises(ValueError):
            OpenRouterConfig(
                base_url="http://router.test", trusted_hosts={"router.test"},
                allow_insecure_test_transport=True,
            )

    def test_cross_origin_or_redirect_response_is_rejected(self):
        provider = OpenRouterProvider(
            OpenRouterConfig(
                api_key_env="TEST_OPENROUTER_KEY", base_url="https://router.test",
                trusted_hosts={"router.test"},
            ),
            environ=self.environ,
            urlopen=self.opener(FakeResponse(
                {"data": []}, url="https://attacker.test/api/v1/models")),
        )
        with self.assertRaises(OpenRouterRedirectError):
            provider.discover()

    def test_dynamic_discovery_failure_is_safe_and_honors_request_timeout(self):
        secret = "malicious-discovery-detail"
        seen_timeouts = []

        def fail(request, timeout=None):
            seen_timeouts.append(timeout)
            raise ProviderNetworkError(secret)

        provider = OpenRouterProvider(
            OpenRouterConfig(
                api_key_env="TEST_OPENROUTER_KEY", base_url="https://router.test",
                trusted_hosts={"router.test"},
            ),
            environ=self.environ,
            urlopen=fail,
        )
        decision = ModelRouter(provider.discover, {"openrouter": provider}).route(
            RoutingRequest(max_latency_ms=50))
        self.assertEqual(decision.status, RouteStatus.ERROR)
        self.assertEqual(decision.error_code, "catalog_discovery_failed")
        self.assertLessEqual(seen_timeouts[0], 0.05)
        self.assertNotIn(secret, repr(decision))

    def test_completion_requires_usage_and_enforces_output_and_timeout_caps(self):
        missing_usage = self.provider({
            "model": "vendor/exact", "choices": [{"message": {"content": "x"}}],
        })
        with self.assertRaises(OpenRouterMalformedResponse):
            missing_usage.complete("vendor/exact", "prompt")

        oversized = self.provider({
            "model": "vendor/exact", "choices": [{"message": {"content": "xx"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 2,
                      "total_tokens": 3},
        })
        with self.assertRaises(OpenRouterResponseTooLarge):
            oversized.complete(
                "vendor/exact", "prompt",
                request=RoutingRequest(max_output_tokens=1, max_latency_ms=25),
            )
        self.assertLessEqual(self.timeouts[-1], 0.025)

    def test_router_supplied_environment_secret_is_used_without_retention(self):
        provider = OpenRouterProvider(
            OpenRouterConfig(
                api_key_env="PROVIDER_ENV_IS_EMPTY", base_url="https://router.test",
                trusted_hosts={"router.test"},
            ),
            environ={},
            urlopen=self.opener({
                "model": "vendor/exact", "choices": [{"message": {"content": "ok"}}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1,
                          "total_tokens": 2},
            }),
        )
        secret = "fixture-credential-value"
        decision = ModelRouter(
            [ModelSpec("openrouter", "vendor/exact", context_window=100,
                       credential_env="ROUTER_TEST_KEY")],
            {"openrouter": provider},
            secrets=EnvironmentSecrets({"ROUTER_TEST_KEY": secret}),
        ).route(RoutingRequest(prompt="hello", max_output_tokens=2))
        self.assertTrue(decision.ok)
        self.assertEqual(self.requests[-1].get_header("Authorization"),
                         "Bearer " + secret)
        self.assertNotIn(secret, repr(provider))
        self.assertNotIn(secret, repr(decision))


class SkillRegistryTests(unittest.TestCase):
    def test_shipped_runtime_contracts_are_complete_and_deterministic(self):
        registry = SkillRegistry(Path(__file__).parent / "skills" / "runtime")
        self.assertEqual(registry.names, ())
        loaded = registry.load()
        self.assertEqual(set(loaded), {
            "lifecycle-conductor", "evidence-research", "product-definition",
            "experiment-analysis", "release-governance", "portfolio-planning",
            "independent-review",
        })
        self.assertEqual(registry.names, tuple(sorted(loaded)))
        for contract in loaded.values():
            self.assertTrue(contract.path.name == "contract.json")
            self.assertTrue(contract.source_hash)
            self.assertTrue(contract.template_hashes)

    def test_unknown_field_and_hash_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "runtime"
            skill = root / "demo"
            skill.mkdir(parents=True)
            source = skill / "SKILL.md"
            graph = skill / "SKILL.graph.yml"
            template = skill / "template.md"
            source.write_text("# demo\n", encoding="utf-8")
            graph.write_text('layer: skills\nstage: DEFINE\ngate: 2\nfeeds: []\nmethod: ""\naliases: ["Demo"]\n', encoding="utf-8")
            template.write_text("# template\n", encoding="utf-8")
            contract = {
                "version": "1.0", "id": "demo", "name": "Demo", "description": "demo",
                "inputs": {}, "outputs": {}, "capabilities": [], "side_effects": [],
                "risk": "low", "privacy": "public", "allowed_hooks": [],
                "resume": {"supported": False}, "completion": {"terminal": "done"},
                "source_hash": hashlib.sha256(source.read_bytes()).hexdigest(),
                "template_hashes": {"template.md": hashlib.sha256(template.read_bytes()).hexdigest()},
            }
            contract["unexpected"] = True
            (skill / "contract.json").write_text(json.dumps(contract), encoding="utf-8")
            trusted = Path(directory) / "trusted.json"
            trusted.write_text(json.dumps({
                "format": "pmos.skill-manifest/v1", "schema": "pmos.skills.v1",
                "skills": {"demo": {
                    name: hashlib.sha256((skill / name).read_bytes()).hexdigest()
                    for name in ("contract.json", "SKILL.graph.yml", "SKILL.md", "template.md")}}}),
                encoding="utf-8")
            with self.assertRaises(SkillContractError):
                SkillRegistry(root, trusted).load()
            contract.pop("unexpected")
            source.write_text("changed\n", encoding="utf-8")
            (skill / "contract.json").write_text(json.dumps(contract), encoding="utf-8")
            with self.assertRaises(SkillContractError):
                SkillRegistry(root, trusted).load()

    def test_trusted_manifest_blocks_self_approved_graph_contract_and_risk_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "runtime"
            skill = root / "demo"
            skill.mkdir(parents=True)
            graph = 'layer: skills\nstage: DEFINE\ngate: 2\nfeeds: []\nmethod: ""\naliases: ["Demo"]\n'
            source = "# demo\n"
            template = "# template\n"
            skill.joinpath("SKILL.md").write_text(source, encoding="utf-8")
            skill.joinpath("SKILL.graph.yml").write_text(graph, encoding="utf-8")
            skill.joinpath("template.md").write_text(template, encoding="utf-8")
            contract = {
                "version": "1.0", "id": "demo", "name": "Demo", "description": "demo",
                "inputs": {}, "outputs": {}, "capabilities": [], "side_effects": [],
                "risk": "low", "privacy": "public", "allowed_hooks": [],
                "resume": {"supported": False}, "completion": {"terminal": "done"},
                "source_hash": hashlib.sha256(source.encode()).hexdigest(),
                "template_hashes": {"template.md": hashlib.sha256(template.encode()).hexdigest()},
            }
            skill.joinpath("contract.json").write_text(json.dumps(contract), encoding="utf-8")
            trusted = Path(directory) / "trusted.json"
            trusted.write_text(json.dumps({
                "format": "pmos.skill-manifest/v1", "schema": "pmos.skills.v1",
                "skills": {"demo": {name: hashlib.sha256((skill / name).read_bytes()).hexdigest()
                                      for name in ("contract.json", "SKILL.graph.yml", "SKILL.md", "template.md")}}}),
                encoding="utf-8")
            registry = SkillRegistry(root, trusted)
            registry.load()
            for filename, edit in (("SKILL.graph.yml", graph.replace("gate: 2", "gate: 5")),
                                   ("contract.json", json.dumps({**contract, "risk": "critical",
                                                                  "side_effects": ["external_write"]}))):
                skill.joinpath(filename).write_text(edit, encoding="utf-8")
                with self.assertRaises(SkillContractError):
                    registry.load()
                with self.assertRaises(SkillContractError):
                    registry.get("demo")
                # Restore the original asset before the next independent edit.
                skill.joinpath(filename).write_text(graph if filename.endswith("graph.yml") else json.dumps(contract),
                                                     encoding="utf-8")
            skill.joinpath("template.md").write_text("# altered\n", encoding="utf-8")
            with self.assertRaises(SkillContractError):
                registry.load()

    def test_unknown_extra_skill_asset_and_symlink_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "runtime"
            skill = root / "demo"
            skill.mkdir(parents=True)
            for filename, contents in (("SKILL.md", "# demo\n"),
                                       ("SKILL.graph.yml", 'layer: skills\nstage: DEFINE\ngate: 2\nfeeds: []\nmethod: ""\naliases: ["Demo"]\n'),
                                       ("template.md", "# template\n")):
                skill.joinpath(filename).write_text(contents, encoding="utf-8")
            contract = {"version": "1.0", "id": "demo", "name": "Demo", "description": "demo",
                        "inputs": {}, "outputs": {}, "capabilities": [], "side_effects": [], "risk": "low",
                        "privacy": "public", "allowed_hooks": [], "resume": {}, "completion": {},
                        "source_hash": hashlib.sha256(skill.joinpath("SKILL.md").read_bytes()).hexdigest(),
                        "template_hashes": {"template.md": hashlib.sha256(skill.joinpath("template.md").read_bytes()).hexdigest()}}
            skill.joinpath("contract.json").write_text(json.dumps(contract), encoding="utf-8")
            trusted = Path(directory) / "trusted.json"
            trusted.write_text(json.dumps({"format": "pmos.skill-manifest/v1", "schema": "pmos.skills.v1",
                                           "skills": {"demo": {name: hashlib.sha256((skill / name).read_bytes()).hexdigest()
                                                                 for name in ("contract.json", "SKILL.graph.yml", "SKILL.md", "template.md")}}}), encoding="utf-8")
            registry = SkillRegistry(root, trusted)
            (skill / "extra.md").write_text("extra", encoding="utf-8")
            with self.assertRaises(SkillContractError):
                registry.load()
            (skill / "extra.md").unlink()
            (root / "unknown").mkdir()
            with self.assertRaises(SkillContractError):
                registry.load()
            (root / "unknown").rmdir()
            (skill / "empty").mkdir()
            with self.assertRaises(SkillContractError):
                registry.load()
            (skill / "empty").rmdir()
            (skill / "link.md").symlink_to(skill / "SKILL.md")
            with self.assertRaises(SkillContractError):
                registry.load()

    def test_trusted_manifest_symlink_and_path_escape_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "runtime"
            skill = root / "demo"
            skill.mkdir(parents=True)
            files = {
                "SKILL.md": "# demo\n",
                "SKILL.graph.yml": 'layer: skills\nstage: DEFINE\ngate: 2\nfeeds: []\nmethod: ""\naliases: ["Demo"]\n',
                "template.md": "# template\n",
            }
            for name, contents in files.items():
                skill.joinpath(name).write_text(contents, encoding="utf-8")
            contract = {"version": "1.0", "id": "demo", "name": "Demo", "description": "demo",
                        "inputs": {}, "outputs": {}, "capabilities": [], "side_effects": [], "risk": "low",
                        "privacy": "public", "allowed_hooks": [], "resume": {}, "completion": {},
                        "source_hash": hashlib.sha256(files["SKILL.md"].encode()).hexdigest(),
                        "template_hashes": {"template.md": hashlib.sha256(files["template.md"].encode()).hexdigest()}}
            skill.joinpath("contract.json").write_text(json.dumps(contract), encoding="utf-8")
            trusted = Path(directory) / "trusted.json"
            trusted.write_text(json.dumps({"format": "pmos.skill-manifest/v1", "schema": "pmos.skills.v1",
                                           "skills": {"demo": {name: hashlib.sha256(skill.joinpath(name).read_bytes()).hexdigest()
                                                                 for name in (*files, "contract.json")}}}), encoding="utf-8")
            SkillRegistry(root, trusted).load()
            linked = Path(directory) / "linked-trusted.json"
            linked.symlink_to(trusted)
            with self.assertRaises(SkillContractError):
                SkillRegistry(root, linked).load()
            escaped = json.loads(trusted.read_text(encoding="utf-8"))
            escaped["skills"]["demo"]["../outside"] = "0" * 64
            trusted.write_text(json.dumps(escaped), encoding="utf-8")
            with self.assertRaises(SkillContractError):
                SkillRegistry(root, trusted).load()
            root_link = Path(directory) / "runtime-link"
            root_link.symlink_to(root, target_is_directory=True)
            with self.assertRaises(SkillContractError):
                SkillRegistry(root_link, trusted).load()


if __name__ == "__main__":
    unittest.main()
