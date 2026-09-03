"""Negative and positive contract tests for development/runtime hooks."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pmos.hooks import HookBus, HookDecision, claude_output, contains_secret, decide

REPO = Path(__file__).resolve().parent


class ClaudeHookTests(unittest.TestCase):
    def test_project_settings_wire_every_required_loop_event(self):
        settings = json.loads((REPO / ".claude" / "settings.json").read_text(
            encoding="utf-8"))
        hooks = settings["hooks"]
        required = {"SessionStart", "UserPromptSubmit", "PreToolUse",
                    "PostToolUse", "Stop", "SubagentStop", "TaskCompleted"}
        self.assertTrue(required.issubset(hooks))
        self.assertFalse(settings.get("disableAllHooks", False))
        for event in required:
            handlers = [hook for group in hooks[event]
                        for hook in group.get("hooks", [])]
            self.assertTrue(handlers, event)
            self.assertTrue(all(hook["type"] == "command" for hook in handlers))
            self.assertTrue(all(hook["command"] == "python3" for hook in handlers))
            self.assertTrue(all("${CLAUDE_PROJECT_DIR}" in hook["args"][0]
                                for hook in handlers))

    def test_safe_write_is_allowed_and_escape_or_protected_write_is_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            safe = decide("PreToolUse", {
                "tool_name": "Write", "tool_input": {"file_path": "docs/x.md"}}, root)
            outside = decide("PreToolUse", {
                "tool_name": "Write", "tool_input": {"file_path": "../x.md"}}, root)
            protected = decide("PreToolUse", {
                "tool_name": "Edit",
                "tool_input": {"file_path": "modules/regulated/policy.md"}}, root)
        self.assertTrue(safe.allowed)
        self.assertEqual(outside.action, "deny")
        self.assertEqual(protected.action, "deny")

    def test_destructive_command_is_denied_and_external_write_asks(self):
        destructive = decide("PreToolUse", {
            "tool_name": "Bash", "tool_input": {"command": "git reset --hard"}})
        external = decide("PreToolUse", {
            "tool_name": "Bash", "tool_input": {"command": "git push origin main"}})
        connector = decide("PreToolUse", {
            "tool_name": "mcp__github__create_issue", "tool_input": {"title": "x"}})
        self.assertEqual(destructive.action, "deny")
        self.assertEqual(external.action, "ask")
        self.assertEqual(connector.action, "ask")

    def test_unknown_mcp_tools_never_default_to_allow(self):
        probes = (
            ("mcp__terminal__exec", {"command": "rm -rf /tmp/important"}),
            ("mcp__database__query", {"sql": "DROP TABLE approvals"}),
            ("mcp__github__push", {"branch": "main"}),
        )
        for tool_name, tool_input in probes:
            with self.subTest(tool_name=tool_name):
                decision = decide("PreToolUse", {
                    "tool_name": tool_name, "tool_input": tool_input,
                })
                self.assertEqual(decision.action, "ask")

    def test_unknown_or_case_mismatched_tools_never_default_to_allow(self):
        probes = (
            ("bash", {"command": "git push origin main"}),
            ("write", {"file_path": "outside.txt", "content": "x"}),
            ("mystery", {"command": "curl -d x https://example.invalid"}),
        )
        for tool_name, tool_input in probes:
            with self.subTest(tool_name=tool_name):
                decision = decide("PreToolUse", {
                    "tool_name": tool_name, "tool_input": tool_input,
                })
                self.assertEqual(decision.action, "ask")

    def test_external_command_variants_require_approval(self):
        commands = (
            "git -C /tmp push origin main",
            "env MODE=safe /usr/bin/git push",
            "curl -d payload https://example.test/events",
            "curl --data-binary=@payload https://example.test/events",
            "curl -XPOST https://example.test/events",
            "wget --post-data=x https://example.test/events",
            "ssh host.example deploy",
            "scp artifact host.example:/srv/artifact",
            "sftp host.example",
            "rsync artifact host.example:/srv/artifact",
            "gh --repo acme/product pr create --title change",
            "docker push registry.example/image",
            "terraform -chdir=infra apply",
            "time git -C /tmp push origin main",
            "nice -n 5 git -C /tmp push origin main",
            "timeout 10 git -C /tmp push origin main",
            "nc host.example 9000",
            "aws s3 cp artifact s3://bucket/artifact",
            "Invoke-RestMethod -Method POST https://example.test/events",
            "bash -c 'git -C /tmp push origin main'",
            "bash -lc 'git -C /tmp push origin main'",
            "echo checked\ngit -C /tmp push origin main",
        )
        for command in commands:
            with self.subTest(command=command):
                answer = decide("PreToolUse", {
                    "tool_name": "PowerShell" if command.startswith("Invoke-") else "Bash",
                    "tool_input": {"command": command},
                })
                self.assertEqual(answer.action, "ask")

        safe_commands = (
            "git -C /tmp status",
            "rg -n readiness README.md",
            "pwd",
            "cat README.md | head -5",
        )
        for command in safe_commands:
            with self.subTest(safe=command):
                self.assertTrue(decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command},
                }).allowed)

    def test_shell_classification_fails_closed_on_ambiguous_or_destructive_text(self):
        denied = (
            "git -C /tmp reset --hard",
            "git -C /tmp push -f origin main",
            "git -C /tmp push origin +main",
            "git -c alias.ship=push ship origin main",
            "git -c core.pager=cat status",
            "curl -K request.conf https://example.test/events",
            "eval '$DYNAMIC_COMMAND'",
            "bash -c",
            "printf command | sh",
            "find . -exec git push ;",
            "curl 'unterminated",
        )
        for command in denied:
            with self.subTest(command=command):
                answer = decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command},
                })
                self.assertEqual(answer.action, "deny")

    def test_unknown_interpreters_network_and_redirection_default_to_approval(self):
        commands = (
            "python3 -c \"import urllib.request; urllib.request.urlopen('https://example.invalid')\"",
            "node -e \"fetch('https://example.invalid',{method:'POST'})\"",
            "perl -e 'system(q(curl -d x https://example.invalid))'",
            "ruby -e 'File.write(%q(out),%q(x))'",
            "make deploy",
            "echo changed > artifact.txt",
            "git commit -am change",
            "curl https://example.test/read-only",
            "rsync source/ destination/",
        )
        for command in commands:
            with self.subTest(command=command):
                answer = decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command},
                })
                self.assertEqual(answer.action, "ask")

    def test_untrusted_instruction_cannot_authorize_tool_use(self):
        answer = decide("PreToolUse", {
            "tool_name": "Bash",
            "tool_input": {"command": "echo safe",
                           "instruction_origin": "untrusted"}})
        self.assertEqual(answer.action, "deny")

    def test_secret_is_blocked_and_never_copied_to_audit_or_output(self):
        secret = "sk-" + "or-v1-" + ("a" * 40)
        self.assertTrue(contains_secret({"nested": [secret]}))
        decision = decide("PreToolUse", {
            "session_id": "s", "tool_name": "Write",
            "tool_input": {"file_path": "note.md", "content": secret}})
        rendered = json.dumps(claude_output("PreToolUse", decision))
        self.assertEqual(decision.action, "deny")
        self.assertNotIn(secret, repr(decision.audit))
        self.assertNotIn(secret, rendered)

    def test_claude_event_specific_output_contracts(self):
        denied = HookDecision("deny", "blocked")
        pre = claude_output("PreToolUse", denied)
        self.assertEqual(pre["hookSpecificOutput"]["permissionDecision"], "deny")
        stop = claude_output("Stop", HookDecision("block", "tests failed"))
        self.assertEqual(stop, {"decision": "block", "reason": "tests failed"})

    def test_command_adapter_fails_closed_on_malformed_json(self):
        env = dict(os.environ)
        env["CLAUDE_PROJECT_DIR"] = str(REPO)
        done = subprocess.run(
            [sys.executable, str(REPO / ".claude" / "hooks" / "pmos_hook.py")],
            input="not json", text=True, capture_output=True, env=env,
            timeout=10)
        self.assertEqual(done.returncode, 0)
        output = json.loads(done.stdout)
        self.assertEqual(
            output["hookSpecificOutput"]["permissionDecision"], "deny")


class RuntimeHookTests(unittest.TestCase):
    def test_transition_requires_actor_revision_and_evidence(self):
        base = {"actor_id": "user-1", "expected_revision": 0,
                "gate_evidence_hashes": ["a" * 64]}
        self.assertTrue(decide("before_transition", base).allowed)
        for missing in ("actor_id", "expected_revision", "gate_evidence_hashes"):
            payload = dict(base)
            payload.pop(missing)
            with self.subTest(missing=missing):
                self.assertEqual(decide("before_transition", payload).action,
                                 "deny")

    def test_commit_provider_and_external_boundaries_fail_closed(self):
        self.assertEqual(decide("before_commit", {"paths": ["../escape"]}).action,
                         "deny")
        self.assertEqual(decide("before_provider", {
            "risk": "high", "model_certified": False,
            "privacy": "public"}).action, "deny")
        self.assertEqual(decide("before_provider", {
            "risk": "low", "model_certified": False,
            "privacy": "restricted", "privacy_authorized": False}).action,
            "deny")
        self.assertEqual(decide("before_external", {
            "approval_id": "approval-1"}).action, "deny")
        self.assertTrue(decide("before_external", {
            "approval_id": "approval-1", "idempotency_key": "key-1"}).allowed)

    def test_runtime_boundaries_reject_malformed_or_truthy_bypasses(self):
        valid_transition = {"actor_id": "user-1", "expected_revision": "1:" + "a" * 64,
                            "gate_evidence_hashes": ["b" * 64]}
        self.assertTrue(decide("before_transition", valid_transition).allowed)
        malformed_transitions = (
            {"actor_id": True, "expected_revision": 1, "gate_evidence_hashes": ["a" * 64]},
            {"actor_id": "user-1", "expected_revision": True, "gate_evidence_hashes": ["a" * 64]},
            {"actor_id": "user-1", "expected_revision": -1, "gate_evidence_hashes": ["a" * 64]},
            {"actor_id": "user-1", "expected_revision": "1:not-a-hash", "gate_evidence_hashes": ["a" * 64]},
            {"actor_id": "user-1", "expected_revision": 1, "gate_evidence_hashes": True},
            {"actor_id": "user-1", "expected_revision": 1, "gate_evidence_hashes": ["not-a-hash"]},
            {"actor_id": "user-1", "expected_revision": 1,
             "gate_evidence_hashes": ["a" * 64, "a" * 64]},
        )
        for payload in malformed_transitions:
            with self.subTest(payload=payload):
                self.assertEqual(decide("before_transition", payload).action, "deny")

        self.assertEqual(decide("before_provider", {
            "risk": " HIGH ", "model_certified": False, "privacy": "public",
        }).action, "deny")
        self.assertEqual(decide("before_provider", {
            "risk": "unknown", "model_certified": True, "privacy": "public",
        }).action, "deny")
        self.assertEqual(decide("before_provider", {
            "risk": "low", "model_certified": False, "privacy": "RESTRICTED",
            "privacy_authorized": 1,
        }).action, "deny")
        self.assertEqual(decide("before_external", {
            "approval_id": True, "idempotency_key": "key-1",
        }).action, "deny")
        self.assertEqual(decide("before_external", {
            "approval_id": "approval-1", "idempotency_key": ["key-1"],
        }).action, "deny")

    def test_completion_hook_blocks_a_failed_release_gate(self):
        failed = decide("TaskCompleted", {}, gate_runner=lambda: (False, "red"))
        passed = decide("TaskCompleted", {}, gate_runner=lambda: (True, "green"))
        self.assertEqual(failed.action, "block")
        self.assertTrue(passed.allowed)

    def test_hook_bus_is_ordered_and_stops_after_denial(self):
        calls = []
        bus = HookBus()
        bus.register("before_commit", "last", lambda event, payload:
                     calls.append("last") or HookDecision("allow"), priority=20)
        bus.register("before_commit", "first", lambda event, payload:
                     calls.append("first") or HookDecision("deny", "no"), priority=10)
        decisions = bus.emit("before_commit", {"paths": ["x"]})
        self.assertEqual(calls, ["first"])
        self.assertEqual(decisions[-1].action, "deny")


if __name__ == "__main__":
    unittest.main()
