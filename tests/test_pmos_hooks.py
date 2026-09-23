"""Negative and positive contract tests for development/runtime hooks."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pmos.hooks import (HookBus, HookDecision, _sed_program_is_read_only,
                        claude_output, contains_secret, decide)

REPO = Path(__file__).resolve().parent.parent


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

    def test_case_variant_protected_destinations_are_denied(self):
        variants = ("modules/Regulated/policy.md", "MODULES/REGULATED/policy.md",
                    ".GIT/config", ".Git/hooks/pre-commit", ".ENV.production",
                    "secrets/server.PEM")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in variants:
                with self.subTest(path=relative):
                    decision = decide("PreToolUse", {
                        "tool_name": "Write",
                        "tool_input": {"file_path": relative}}, root)
                    self.assertEqual(decision.action, "deny")
            self.assertTrue(decide("PreToolUse", {
                "tool_name": "Write",
                "tool_input": {"file_path": "docs/Regulated-notes.md"}},
                root).allowed)

    def test_private_key_material_is_blocked_like_other_secrets(self):
        # Assembled rather than written out so the file itself carries no
        # literal key block for the repository's own secret scanner to flag.
        fence = "-" * 5
        key = (fence + "BEGIN OPENSSH PRIVATE KEY" + fence + "\n" +
               "b3BlbnNzaC1rZXktdjEAAAAABG5vbmU=\n" +
               fence + "END OPENSSH PRIVATE KEY" + fence + "\n")
        self.assertTrue(contains_secret({"content": key}))
        decision = decide("PreToolUse", {
            "tool_name": "Write",
            "tool_input": {"file_path": "notes/key.txt", "content": key}})
        self.assertEqual(decision.action, "deny")
        rendered = claude_output("PreToolUse", decision)
        self.assertEqual(
            rendered["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_encrypted_dsa_and_pgp_key_headers_are_also_blocked(self):
        # The three detectors in this repository (this module, the security
        # gate, and lint.py's tree gate) used to disagree on which key header
        # prefixes counted: an ENCRYPTED PKCS#8 key passed here and passed the
        # security gate, and DSA/PGP passed the security gate too. All three
        # now share lint.py's `[A-Z ]*PRIVATE KEY` shape. Fixtures assembled
        # rather than written out so this file carries no literal key block
        # for the repository's own secret scanner to flag.
        fence = "-" * 5
        for prefix in ("ENCRYPTED ", "DSA ", "PGP "):
            with self.subTest(prefix=prefix.strip()):
                key = (fence + "BEGIN " + prefix + "PRIVATE KEY" + fence +
                       "\n" + "b3BlbnNzaC1rZXktdjEAAAAABG5vbmU=\n" +
                       fence + "END " + prefix + "PRIVATE KEY" + fence + "\n")
                self.assertTrue(contains_secret({"content": key}), prefix)
                decision = decide("PreToolUse", {
                    "tool_name": "Write",
                    "tool_input": {"file_path": "notes/key.txt",
                                   "content": key}})
                self.assertEqual(decision.action, "deny", prefix)

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

    def test_force_push_is_denied_only_as_a_standalone_option_token(self):
        """Regression: DESTRUCTIVE_COMMANDS used to match "-f" as a bare
        substring, so a branch name that merely ends in "-f" (no leading
        space before the "-") was denied as though it were a forced push.
        "-f" and "--force" now have to appear as their own shell token.
        "--force" still matches as a prefix, so "--force-with-lease" (a
        real, if gentler, rewrite of remote history) stays denied exactly
        as it did before this fix; only the untethered "-f" substring match
        was the defect.
        """
        denied = (
            "git push -f origin main",
            "git push origin main -f",
            "git push --force",
            "git push --force-with-lease origin main",
        )
        for command in denied:
            with self.subTest(command=command):
                decision = decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command}})
                self.assertEqual(decision.action, "deny")
                self.assertEqual(decision.reason, "destructive command is blocked")

        not_denied_as_destructive = (
            "git push origin feat-f",
            "git push origin fix-force-flag",
        )
        for command in not_denied_as_destructive:
            with self.subTest(command=command):
                decision = decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command}})
                # Same outcome as any other ordinary, non-forced push: it
                # still needs a human's approval, it is just no longer
                # misclassified as a destructive command outright.
                self.assertEqual(decision.action, "ask")

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
            "git status",
            "rg -n readiness README.md",
            "pwd",
            "cat README.md | head -5",
            # Each wrapper below is itself off the read-only allowlist, so these
            # are allowed only when the wrapper is actually stripped. None of
            # them carries ``-C``: pointing git at a caller-chosen repository
            # is a redirect, tested for its own sake below.
            "sudo git status",
            "env MODE=safe git status",
            "timeout 5 rg -n readiness README.md",
            "nice -n 5 cat README.md",
            "time git status",
        )
        for command in safe_commands:
            with self.subTest(safe=command):
                self.assertTrue(decide("PreToolUse", {
                    "tool_name": "Bash", "tool_input": {"command": command},
                }).allowed)

    def test_shell_classification_fails_closed_on_ambiguous_or_destructive_text(self):
        denied = (
            "git -C /tmp reset --hard",
            # A -C prefix hides the clean subcommand from
            # DESTRUCTIVE_COMMANDS, and the --force spelling is unreachable for
            # that regex with or without a prefix, so both of these depend on
            # the git subcommand check alone.
            "git -C /tmp clean -x -f -d",
            "git clean --force -d",
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

    def test_a_labeled_example_credential_in_documentation_is_also_blocked(self):
        """F35 false positive: SECRET_PATTERNS matches shape, not intent.

        A docs or fixture line that explicitly labels a value as an example,
        not a real credential, still trips the same pattern a leaked secret
        would: the word "password" (or key/secret/token) immediately
        followed by ":" or "=" and 20+ unbroken shape-matching characters is
        enough, regardless of the sentence around it. This is the fail-closed
        direction a shape-only scanner should err in: teaching the pattern to
        trust a nearby word like "example" would make it trivial to smuggle a
        real secret past the same check, so pmos/hooks.py is left unchanged
        and this test pins the current, over-broad-but-safe behavior as a
        known limitation rather than treating it as a defect to fix.
        """
        doc_line = ("The fixture below shows an example password: "
                    "cf23df2207d99a74fbe169e3eba035e633b65d94 for illustration only.")
        self.assertTrue(contains_secret({"content": doc_line}))
        decision = decide("PreToolUse", {
            "tool_name": "Write",
            "tool_input": {"file_path": "docs/example.md", "content": doc_line}})
        self.assertEqual(decision.action, "deny")
        self.assertEqual(decision.reason,
                         "secret-like material must be removed and rotated")

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

    def test_hook_bus_rejects_duplicates_and_orders_same_priority_by_name(self):
        calls = []
        bus = HookBus()
        bus.register("before_commit", "beta", lambda event, payload:
                     calls.append("beta") or HookDecision("allow"))
        bus.register("before_commit", "alpha", lambda event, payload:
                     calls.append("alpha") or HookDecision("allow"))
        decisions = bus.emit("before_commit", {"paths": ["x"]})
        self.assertEqual(calls, ["alpha", "beta"])
        self.assertEqual([decision.action for decision in decisions],
                         ["allow", "allow"])
        with self.assertRaises(ValueError):
            bus.register("before_commit", "alpha", lambda event, payload:
                         HookDecision("allow"))


class ReadOnlyAllowlistIsArgumentAwareTests(unittest.TestCase):
    """The read-only allowlist classifies arguments, not executable names.

    An external audit of 49ca7e8 ran three commands through ``decide`` and then
    ran them for real in a disposable directory. All three were classified
    "allow" and all three mutated that directory: ``sort input -o output`` wrote
    a file, ``sed -n "w written" input`` wrote a file, and
    ``git remote add ...`` rewrote the repository's configuration. The policy
    looked only at the executable's basename, so every write-capable option and
    subcommand of an allow-listed program was invisible to it.

    These tests fail if the argument checks are removed: reverting any one of
    them puts its probe back on the "allow" path.
    """

    def classify(self, command):
        return decide("PreToolUse", {
            "tool_name": "Bash", "tool_input": {"command": command}}).action

    def test_the_three_audited_probes_are_no_longer_allowed(self):
        for command in ("sort input -o output",
                        'sed -n "w written" input',
                        "git remote add audit https://example.invalid/repo.git"):
            with self.subTest(command=command):
                self.assertNotEqual(self.classify(command), "allow")

    def test_write_capable_options_of_allowlisted_programs_require_approval(self):
        probes = (
            # sort's output file, spelled every way the option can be written.
            "sort input -o output",
            "sort -o output input",
            "sort --output=output input",
            "sort --output output input",
            "sort -bo output input",
            # uniq's second file operand is the file it overwrites.
            "uniq input output",
            "uniq -f 1 input output",
            # yq edits in place and splits into files.
            "yq -i '.a = 1' config.yaml",
            "yq --inplace '.a = 1' config.yaml",
            "yq -s '.name' config.yaml",
            # find writes through its own output actions.
            "find . -fprint listing",
            "find . -fprintf listing %p",
            # A long destination spelling is refused whichever program carries it.
            "cat --output=copy input",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

    def test_sed_is_classified_by_its_script_not_by_its_name(self):
        writes_or_executes = (
            'sed -n "w written" input',
            'sed "1w written" input',
            'sed -e "w written" input',
            'sed -ew written input',
            'sed "s/a/b/w written" input',
            'sed "s/a/b/gw written" input',
            'sed -n "W part" input',
            'sed "1e date" input',
            'sed "s/a/b/e" input',
            'sed "r /etc/passwd" input',
            'sed "R /etc/passwd" input',
            # An in-place edit, bundled or suffixed.
            "sed -i.bak s/a/b/ input",
            "sed --in-place s/a/b/ input",
            "sed -ni s/a/b/ input",
            # A script this classifier cannot read before the command runs.
            "sed -f script.sed input",
            "sed --file=script.sed input",
            # An option the classifier does not recognise fails closed.
            "sed --unknown-option p input",
        )
        for command in writes_or_executes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        read_only_scripts = (
            "sed -n '1,5p' input",
            "sed -n '/heading/p' input",
            "sed 's/were/was/g' input",
            "sed -e '1d' -e '$d' input",
            "sed -ne '2p' input",
            "sed -n '2{p;q}' input",
            "sed 'y/abc/xyz/' input",
            "sed '/^# /d' input",
            "sed -E 's/(a)(b)/\\2\\1/' input",
        )
        for command in read_only_scripts:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "allow")

    def test_git_remote_mutations_and_output_options_require_approval(self):
        probes = (
            "git remote add audit https://example.invalid/repo.git",
            "git remote remove origin",
            "git remote rm origin",
            "git remote rename origin upstream",
            "git remote set-url origin https://example.invalid/repo.git",
            "git remote set-head origin main",
            "git remote prune origin",
            "git remote update",
            # show contacts the remote, so it is network access, not a local read.
            "git remote show origin",
            # A global option before the subcommand must not hide the
            # sub-subcommand. --no-pager is used rather than -C because -C is
            # now refused in its own right, which would let this probe pass
            # without the remote check running at all.
            "git --no-pager remote add audit https://example.invalid/repo.git",
            # Read-only subcommands can still be told to write or to run a pager.
            "git diff --output=patch.txt",
            "git grep -O cat needle",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        for command in ("git remote", "git remote -v", "git remote get-url origin",
                        "git status", "git log --oneline -5"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_wrappers_cannot_smuggle_a_write_past_the_classifier(self):
        probes = (
            # The wrapper is stripped, so the inner write is what gets seen.
            "env MODE=safe sort input -o output",
            "nice -n 5 sort input -o output",
            "timeout 5 sort input -o output",
            "sudo sort input -o output",
            "bash -c 'sort input -o output'",
            # These wrappers write or re-parse a command line themselves.
            "time -o timing.txt git status",
            "env -S 'sort input -o output'",
            "nohup sort input -o output",
            "busybox sed -i s/a/b/ input",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

    def test_each_wrapper_guard_is_individually_load_bearing(self):
        """Probes that depend on one wrapper guard and on nothing else.

        ``env -S`` re-splits one token into a whole command line and ``nohup``
        appends its child's output to ./nohup.out, so neither is a transparent
        wrapper. With a harmless child, no other check fires, so these probes
        fail the moment either guard is removed.
        """
        for command in ("env -S ls", "env --split-string=ls", "nohup ls -la"):
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

    def test_environment_assignments_that_redirect_execution_require_approval(self):
        # A variable that names a program, a library, a configuration file or a
        # home directory makes an allow-listed read-only command execute
        # something else; git runs GIT_EXTERNAL_DIFF itself.
        probes = (
            "GIT_EXTERNAL_DIFF=./ext.sh git diff",
            "GIT_PAGER=./ext.sh git --paginate log",
            "GIT_CONFIG_GLOBAL=/tmp/evil git log",
            "LD_PRELOAD=./evil.so ls",
            "PAGER=./ext.sh git log -p",
            "HOME=/tmp/evil git log",
            # The assignment is equally live behind a stripped wrapper.
            "env GIT_PAGER=./ext.sh git log",
            "sudo GIT_PAGER=./ext.sh git log",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        # An assignment that cannot name a program stays read-only.
        for command in ("env MODE=safe git status", "MODE=safe sort input"):
            with self.subTest(inert=command):
                self.assertEqual(self.classify(command), "allow")

    def test_git_arguments_are_checked_for_command_substitution(self):
        # The subcommand is not the only place substitution can hide: the shell
        # runs the backticked text to build the argument, and that text is
        # never seen by this classifier.
        for command in (r"git log `./ext.sh`", r"git show `cat payload`"):
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "deny")
        self.assertEqual(self.classify("git log --oneline -5"), "allow")

    def test_git_global_options_that_redirect_git_require_approval(self):
        # --config-env names an environment variable to read a config value
        # from, which is the -c injection path under a spelling that does not
        # begin with -c.
        self.assertEqual(
            self.classify("git --config-env=core.pager=EVILVAR --paginate log"),
            "deny")

        # These point git at a caller-chosen directory, or turn on the
        # external programs named by the repository's own configuration.
        probes = (
            "git --exec-path=/tmp/evil status",
            "git --git-dir=/tmp/evil/.git status",
            "git --work-tree=/tmp status",
            "git log --ext-diff",
            "git show --textconv HEAD",
            "git cat-file --filters HEAD:file",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        # The --no- spellings switch the external programs off rather than
        # on; after the subcommand --git-dir is a read-only query that prints a
        # path, not a redirect; and -C after the subcommand is copy detection.
        for command in ("git log --no-ext-diff", "git log --no-textconv",
                        "git rev-parse --git-dir", "git log -C --oneline",
                        "git log --text"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_glued_short_options_cannot_hide_a_git_pager_program(self):
        # git grep's -O<program> starts that program, and the option name test
        # cannot see a value glued to the letter.
        probes = ("git grep -O./ext.sh alpha", "git grep -nO./ext.sh alpha",
                  "git diff -Otouch")
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")
        # Lowercase o is ordinary read-only usage and is not part of the test.
        self.assertEqual(self.classify("git status -uno"), "allow")

    def test_options_whose_value_names_a_program_require_approval(self):
        # --pre, --hostname-bin and --compress-program each run the program
        # named by their value, so the read-only basename decides nothing.
        probes = (
            "rg --pre touch pattern .",
            "rg --pre=/bin/sh pattern .",
            "rg --hostname-bin ./ext.sh pattern .",
            "sort --compress-program=touch bigfile",
            "find . -name x --pre touch",
            # A file operand built by running a program is the same defect
            # arriving through the argument rather than through the option.
            r"sed -n 1p `./ext.sh`",
            r"find . -newer `./ext.sh`",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        # A "$" inside a sed script is a line address, not an expansion.
        for command in ("rg -n pattern .", "sed -e '1d' -e '$d' input"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_git_chdir_is_a_repository_redirect_like_git_dir(self):
        """``git -C <dir>`` loads that directory's repository configuration.

        Measured on git 2.50.1: ``git -C evil diff`` against a repository whose
        config set ``diff.external``, and ``git -C evil status`` against one
        whose config set ``core.fsmonitor``, each executed the named program.
        ``git status`` needs no options at all for that, so the subcommand
        cannot decide it; only the redirect can. The same attack spelled
        ``--git-dir``/``--work-tree`` is refused one test above, so leaving
        ``-C`` out was an internal inconsistency as well as a hole.
        """
        probes = ("git -C evil diff", "git -C evil status",
                  "git -C evil show HEAD", "git -C evil log",
                  "git -C evil grep pattern", "git -C /tmp status",
                  "/usr/bin/git -C evil diff", "command git -C evil diff",
                  "timeout 10 git -C evil status",
                  # Glued and bundled spellings are refused by shape: git
                  # 2.50.1 rejects them, and this guard does not rest on that.
                  "git -Cevil status", "git -pCevil status",
                  # The wrapper stack does not launder it either.
                  "timeout 10 env -C evil git status")
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

    def test_a_wrapper_that_changes_directory_requires_approval(self):
        """The same redirect spelled on the wrapper instead of on git.

        ``env -C <dir>`` and ``sudo --chdir=<dir>`` put the child in a
        caller-chosen repository, which is the ``git -C`` hole one layer out:
        the child's own argument list carries no trace of it. Both wrappers
        were being stripped silently.
        """
        probes = ("env -C evil git status", "env --chdir=evil git status",
                  "env -Cevil git status", "sudo --chdir=evil git status",
                  "sudo -D evil git status", "sudo -Devil git status")
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")
        # A wrapper that does not change directory is still transparent.
        for command in ("env ls -la", "sudo -u nobody git status",
                        "timeout 10 git status"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_abbreviated_long_options_cannot_walk_past_the_guards(self):
        """A guard that matches exact spellings is not a guard on GNU tools.

        GNU ``getopt_long`` and git's ``parse-options`` accept any unambiguous
        abbreviation, so every exact-spelling frozenset in this module was
        reachable under a shorter name. ``git grep --open-files-in-pag=./ext.sh``
        was measured starting that program on git 2.50.1 while the unabbreviated
        spelling was already refused.
        """
        probes = (
            # value names a program
            "sort --compress-prog=./ext.sh input",
            "sort --compress-progra=./ext.sh input",
            "rg --pr ./ext.sh pattern .",
            # value names a written file
            "sort --outp=/tmp/x input",
            "git diff --outpu=/tmp/x",
            # git's own pager option, the one that was measured executing
            "git grep --open-files-in-pag=./ext.sh alpha",
            # git global redirects, refused by shape whether or not this git
            # build happens to accept the abbreviation
            "git --git-di=/tmp/evil/.git status",
            "git --work-tre=/tmp status",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")

        # A full option spelling that merely shares a prefix with a guarded
        # one is not an abbreviation of it and stays read-only.
        for command in ("git log --oneline -5", "rg --files", "git log --text",
                        "git ls-files --others"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_abbreviated_wrapper_and_config_options_are_guarded_too(self):
        """The crossing the previous round left open: abbreviation x wrapper.

        ``test_abbreviated_long_options_cannot_walk_past_the_guards`` probes
        the option sets that are read through ``_option_abbreviates``, and
        ``test_a_wrapper_that_changes_directory_requires_approval`` probes the
        full ``--chdir`` spelling. Nothing crossed them, so
        ``env --chd=<dir> git status`` and ``sudo --chd=<dir> git status``
        were an ``allow`` while ``--chdir=`` was an ``ask``. Every long option
        this policy compares now goes through one helper, ``_matches_option``,
        and this test is the crossing.

        ``sudo`` accepting the abbreviation was measured on this host:
        ``sudo -n --chd=/tmp true`` reaches authentication, while
        ``sudo -n --zzz=/tmp true`` is rejected as an unrecognised option.
        The same sweep found ``time`` naming a file it truncates in three
        spellings the wrapper scan could not see, including the short
        ``-o`` with its value glued to the letter, which is a shape and
        not an abbreviation: the two are the same miss looked at from
        different sides, so they are probed together.
        """
        probes = (
            # the redirect spelled short on the wrapper
            "env --chd=evil git status", "env --ch=evil git status",
            "sudo --chd=evil git status", "sudo --chdi=evil git status",
            # the next spelling of the same wrapper idea: sudo also has a
            # directory option that is not --chdir
            "sudo --chroot=evil git status", "sudo --chro=evil git status",
            "sudo -Revil git status",
            # ``time`` names a file it truncates. The full spelling was an
            # allow as well, because the wrapper and its option had already
            # been consumed when the scan stopped, so the child alone was
            # classified.
            "time --output=f git status", "time --append=f git status",
            "time --outp=f git status", "time --out=f git status",
            "time --app=f git status",
            # and the same option written short, with its value glued or
            # bundled, which an option-name test cannot see at all
            "time -of git status", "time -o/tmp/f git status",
            "time -ao/tmp/f git status",
            "timeout 10 time --outp=f git status",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")
        # Configuration injection is a deny, not an ask, and the abbreviation
        # has to reach the same answer as the full spelling.
        for command in ("git --config-env=core.pager=EVIL log",
                        "git --config-en=core.pager=EVIL log",
                        "git --conf=core.pager=EVIL log"):
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "deny")
        # Options that merely start with the same letters are not
        # abbreviations of a guarded spelling and stay read-only.
        for command in ("time git status", "time -f %e git status",
                        "time -p git status", "time -l git status",
                        "sudo -u nobody git status", "env ls -la",
                        "nice -n 5 git log", "timeout 10 git status",
                        "git log --color=always", "git status --column",
                        "git diff --cc"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_a_wrapper_option_that_redirects_execution_requires_approval(self):
        """Where the child runs and which binary it is are one class.

        The previous round guarded the wrapper option that changes DIRECTORY
        and only that one. A review then proved three more, all executing:
        ``env --C<dir> git status`` and ``env --C<dir> git diff`` reach the
        pointed-at repository's ``core.fsmonitor`` and ``diff.external``, and
        ``env --P<dir> git status`` and ``env -P<dir> git status`` run an
        attacker's ``./git`` outright, because ``-P`` names the directory env
        resolves the utility from. An option that says WHERE the child runs
        and one that says WHICH binary runs are the same hole, so they are
        guarded and probed as one.

        Measured on this host with a planted ``./git``: ``env -P/tmp/x/bin git
        status`` and ``env --P/tmp/x/bin git status`` both printed the planted
        program's output, and ``env --Path=/tmp/x/bin git status`` was read by
        env as ``-P`` carrying the value ``ath=/tmp/x/bin``. This env is BSD
        env with no long options at all, which is why ``--chdir=`` is rejected
        outright and why a ``--`` token is read as a short cluster.

        sudo's parser was measured accepting ``-s``, ``-E`` and
        ``--preserve-env=PATH`` - each reaches authentication - and rejecting
        ``--D/tmp`` as an unrecognised option, so that last spelling is a
        refusal by shape rather than a closed exploit.
        """
        probes = (
            # the directory spelling written with two dashes, which the
            # previous round's letter test could not see at all
            "env --C/tmp/evil git status", "env --C/tmp/evil git diff",
            # the utility-path option: the new half of the class
            "env --P/tmp/evil/bin git status", "env -P/tmp/evil/bin git status",
            "env -P /tmp/evil/bin git status",
            "env --Path=/tmp/evil/bin git status",
            "env -iP/tmp/evil/bin git status",
            # the re-split option, whose glued spelling was an allow
            "env -Ssort git status",
            # sudo's shell and environment options: each changes which binary
            # runs rather than where it runs
            "sudo -s git status", "sudo -i git status", "sudo -E git status",
            "sudo --preserve-env=PATH git status", "sudo --login git status",
            "sudo --shell git status",
            # sudo's root option written short and glued, spelled so that no
            # other guarded letter appears anywhere in the token
            "sudo -R/tmp/root git status",
            # refused by shape: sudo rejects this spelling itself
            "sudo --D/tmp/evil git status",
            # the wrapper stack does not launder any of it
            "timeout 10 env -P/tmp/evil/bin git status",
            "nice -n 5 env --C/tmp/evil git status",
        )
        for command in probes:
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "ask")
        # A wrapper option that redirects nothing is still transparent, and a
        # long option whose letters happen to include a guarded lower-case one
        # is not read as a cluster.
        for command in ("env ls -la", "env MODE=safe git status",
                        "sudo -u nobody git status",
                        "sudo --non-interactive git status",
                        "sudo --stdin git status",
                        "timeout 10 git status", "nice -n 5 git log",
                        "git status"):
            with self.subTest(read_only=command):
                self.assertEqual(self.classify(command), "allow")

    def test_the_read_only_path_still_works(self):
        """The positive controls the audit required to keep working."""
        for command in ("sort input", "sed -n '1,5p' input", "git status",
                        "git log", "grep -r needle .", "ls -la", "pwd",
                        "rg -n readiness README.md", "cat README.md | head -5",
                        "wc -l README.md", "uniq sorted", "sort -nr input",
                        "find . -name '*.py'", "diff left right",
                        "jq '.name' package.json", "yq '.name' config.yaml"):
            with self.subTest(command=command):
                self.assertEqual(self.classify(command), "allow")


class SedScriptScannerTests(unittest.TestCase):
    """The sed scanner reports anything it cannot account for as unsafe."""

    def test_unparsable_scripts_are_not_read_only(self):
        for script in ("s/a/b", "s/a/b/q", "/unterminated", "\\", "K",
                       "s/a/b/w out", "w out", "e date"):
            with self.subTest(script=script):
                self.assertFalse(_sed_program_is_read_only(script))
        self.assertFalse(_sed_program_is_read_only(None))
        # An empty script is a genuine no-op; sed with no script at all is
        # refused one level up, in _classify_sed.
        self.assertTrue(_sed_program_is_read_only(""))

    def test_ordinary_print_and_delete_scripts_are_read_only(self):
        for script in ("1,5p", "/x/p", "$p", "s/a/b/g", "2{p;q}", "y/abc/xyz/",
                       "/^# /d", "s|a|b|g", "# comment\n1p"):
            with self.subTest(script=script):
                self.assertTrue(_sed_program_is_read_only(script))


if __name__ == "__main__":
    unittest.main()
