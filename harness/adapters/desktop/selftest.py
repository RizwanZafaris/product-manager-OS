#!/usr/bin/env python3
"""Checks the desktop adapter without a live MCP client. Standard library only.

    python3 harness/adapters/desktop/selftest.py

What it proves: the tool set is generated from harness/MANIFEST.json one tool
per entry, the names are unique and legal MCP tool names, every emitted JSON
schema is well formed and survives a JSON round trip, every description and
every plan renders, and the SDK-absent path prints one line and exits non-zero
instead of raising ImportError. It also proves the runtime tool added beside
the manifest tools: its schema and description pass the same bars a manifest
tool's do, its phases agree with `pmos status --json` for a fresh product and
again after one accepted answer, that agreement still holds when the pinned
contract is stale against the shipped one (so the tool is provably reading
the pin, not the shipped contract), that a symlinked artifact drives both the
CLI and the tool to the same phases: [] plus phases_error fallback instead of
an exception or an {"ok": false} response, that a corrupt (non-JSON) pin
drives the Conductor's own construction into that same phases_error fallback
rather than an {"ok": false} response, that a runtime database which is
present but is not a SQLite file at all comes back as {"ok": false,
"error": ...} rather than an exception, and that a missing runtime comes back
as {"ok": false, "error": ...} rather than a traceback.

What it cannot prove: that a desktop client accepts the handshake, that a tool
call round trips over stdio, or that a plan is the right plan for a request.
Those need a live client and a human reading the output.

Exit status is 1 on any failure, so it can run beside python3 lint.py --os.
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import manifest_tools as mt  # noqa: E402
import runtime_status as rs  # noqa: E402

# runtime_status puts the repository root on sys.path as a side effect of
# being imported, the same way harness/runner.py does it, so pmos.cli and
# pmos.banks are only importable here once the line above has run.
import pmos.cli as pmos_cli  # noqa: E402
from pmos.banks import CONTRACT_PATH  # noqa: E402

# Escaped, so the file that checks for these characters contains none of them.
BANNED_CHARS = {"\u2014": "em dash", "\u2013": "en dash",
                "\u2015": "horizontal bar", "\u2212": "minus sign"}

# The same shapes lint.py check 9 scans for, applied to what a tool returns.
# A route id like risk-assessment is not a credential, so the patterns are
# anchored the way the linter anchors them.
SECRET_SHAPES = (r"AKIA[0-9A-Z]{16}", r"\bsk-[A-Za-z0-9]{20,}",
                 r"\bghp_[A-Za-z0-9]{20,}", r"BEGIN [A-Z ]*PRIVATE KEY",
                 r"OMNIROUTE_API_KEY\s*[=:]\s*\S")


def check_schema(schema, where, fail):
    """A minimal, honest JSON Schema check: shape, types, and serializability."""
    if schema.get("type") != "object":
        fail("%s: schema type is %r, not object" % (where, schema.get("type")))
    props = schema.get("properties")
    if not isinstance(props, dict) or not props:
        fail("%s: schema has no properties object" % where)
        return
    for name, prop in props.items():
        if not isinstance(prop, dict) or "type" not in prop:
            fail("%s: property %s declares no type" % (where, name))
        if not prop.get("description"):
            fail("%s: property %s has no description" % (where, name))
    if not isinstance(schema.get("required", []), list):
        fail("%s: required is not a list" % where)
    if not isinstance(schema.get("additionalProperties", False), bool):
        fail("%s: additionalProperties is not a boolean" % where)
    try:
        if json.loads(json.dumps(schema)) != schema:
            fail("%s: schema does not survive a JSON round trip" % where)
    except (TypeError, ValueError) as exc:
        fail("%s: schema is not JSON serializable (%s)" % (where, exc))


def sdk_absent_output(root):
    """Run server.py with the MCP SDK blocked. Returns (returncode, stderr)."""
    blocker = (
        "import sys\n"
        "class Block:\n"
        "    def find_module(self, name, path=None):\n"
        "        return None\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name == 'mcp' or name.startswith('mcp.'):\n"
        "            raise ImportError(\"No module named 'mcp'\")\n"
        "        return None\n"
        "sys.meta_path.insert(0, Block())\n"
        "sys.argv = ['server.py']\n"
        "sys.path.insert(0, %r)\n"
        "import runpy\n"
        "runpy.run_path(%r, run_name='__main__')\n"
        % (str(HERE), str(HERE / "server.py")))
    proc = subprocess.run([sys.executable, "-c", blocker], cwd=str(root),
                          capture_output=True, text=True)
    return proc.returncode, (proc.stderr or "").strip()


def check_runtime_tool(fail):
    """The runtime tool's schema and description pass the same bars a manifest tool's do.

    Proves: runtime_status.TOOL carries a well formed inputSchema (check_schema)
    and a description that is long enough to route on, says it signs no gate,
    and carries no banned character, placeholder, or credential shape, exactly
    the checks the loop below runs for every manifest tool's own description.
    """
    tool = rs.TOOL
    name = tool["name"]
    check_schema(tool["inputSchema"], name, fail)
    description = tool["description"]
    if len(description) < 80:
        fail("%s: description is too thin to route on" % name)
    if "signs no gate" not in description:
        fail("%s: description does not say it signs no gate" % name)
    for char, label in BANNED_CHARS.items():
        if char in description:
            fail("%s: description contains an %s" % (name, label))
    for banned in ("TBD", "TODO", "FIXME", "XXX"):
        if banned in description:
            fail("%s: description contains the placeholder %s" % (name, banned))
    for pattern in SECRET_SHAPES:
        if re.search(pattern, description):
            fail("%s: description matches a credential shape (%s)" % (name, pattern))


def _cli_status_json(folder, product_id):
    """`pmos status --json` for one product, as a dict. Raises on a nonzero exit."""
    output = io.StringIO()
    with redirect_stdout(output):
        code = pmos_cli.main(["--json", "status", "--path", folder, "--product-id", product_id])
    if code != 0:
        raise RuntimeError("pmos status exited %d: %s" % (code, output.getvalue()))
    return json.loads(output.getvalue())


def check_runtime_parity(fail):
    """runtime_status.status()'s phases match `pmos status --json`'s phases.

    Proves: for a fresh product, and again after one accepted answer given
    through the CLI the way tests/test_pmos_cli.py gives one, the runtime
    tool reports the identical phases array `pmos status --json` reports for
    the same product, against a temporary workspace created with `pmos init`
    through pmos.cli.main.
    """
    with TemporaryDirectory() as folder:
        product_id = "selftest-product"
        output = io.StringIO()
        with redirect_stdout(output):
            code = pmos_cli.main(["init", "--path", folder, "--product-id", product_id])
        if code != 0:
            fail("runtime parity: pmos init exited %d" % code)
            return
        try:
            cli_before = _cli_status_json(folder, product_id)
        except Exception as exc:  # noqa: BLE001, any failure here is the finding
            fail("runtime parity: pmos status failed on a fresh product: %s" % exc)
            return
        runtime_before = rs.status({"path": folder, "product_id": product_id})
        if not runtime_before.get("ok"):
            fail("runtime parity: runtime_status.status failed on a fresh product: %s"
                 % runtime_before.get("error"))
            return
        if runtime_before["phases"] != cli_before["phases"]:
            fail("runtime parity: phases differ from `pmos status --json` on a fresh product")

        question = cli_before.get("question") or {}
        if not question.get("id"):
            fail("runtime parity: a fresh product offered no first question to answer")
            return
        evidence = {"class": "observed_behavior", "source": "selftest interview",
                    "date": "2026-09-12", "location": "selftest"}
        output = io.StringIO()
        with redirect_stdout(output):
            code = pmos_cli.main(["answer", "--path", folder, "--product-id", product_id,
                                  "--question-id", question["id"], "--answer", "A real outcome",
                                  "--evidence", json.dumps(evidence),
                                  "--expected-revision", cli_before["revision_token"],
                                  "--turn-id", "selftest-answer-1", "--json"])
        if code != 0:
            fail("runtime parity: pmos answer exited %d" % code)
            return
        answered = json.loads(output.getvalue())
        if answered.get("outcome", {}).get("status") != "accepted":
            fail("runtime parity: the CLI answer was not accepted: %r" % answered)
            return

        try:
            cli_after = _cli_status_json(folder, product_id)
        except Exception as exc:  # noqa: BLE001
            fail("runtime parity: pmos status failed after one accepted answer: %s" % exc)
            return
        runtime_after = rs.status({"path": folder, "product_id": product_id})
        if not runtime_after.get("ok"):
            fail("runtime parity: runtime_status.status failed after one accepted answer: %s"
                 % runtime_after.get("error"))
            return
        if runtime_after["phases"] != cli_after["phases"]:
            fail("runtime parity: phases differ from `pmos status --json` after one accepted answer")


def check_runtime_parity_with_stale_pin(fail):
    """runtime_status.status() reports phases for the product's pinned contract, not the shipped one.

    Proves: after pinning a contract edited away from the shipped one (a
    bank version and a question's wording changed, as tests/test_pmos_cli.py
    ::test_a_pin_that_differs_from_the_shipped_contract_is_kept does), the
    runtime tool's phases still equal `pmos status --json`'s phases for that
    same pinned, now-stale, contract. Swapping pinned_contract() for
    pmos.banks.load_contract() in the adapter would pass check_runtime_parity
    above (pinned equals shipped there) but fail this one, because only a
    stale pin makes the two contracts differ.
    """
    with TemporaryDirectory() as folder:
        product_id = "selftest-stale-pin-product"
        output = io.StringIO()
        with redirect_stdout(output):
            code = pmos_cli.main(["init", "--path", folder, "--product-id", product_id])
        if code != 0:
            fail("stale pin parity: pmos init exited %d" % code)
            return
        contract = json.loads(CONTRACT_PATH.read_bytes())
        contract["banks"][0]["version"] = "c0000000000000000"
        contract["banks"][0]["questions"][0]["ask"] = "Who has this problem, by name?"
        # phase_report reads "stage" straight into its "phase" field, so this
        # is what actually makes a shipped-contract substitution visible in
        # the phases array rather than only in question_banks.pinned.
        contract["banks"][0]["stage"] = "DISCOVER-STALE-PIN"
        database = Path(folder) / ".pmos" / "runtime.sqlite"
        with rs.Store(database) as store:
            snapshot = store.read_snapshot(product_id)
            files = dict(snapshot.files)
            files[pmos_cli.PIN_PATH] = json.dumps(contract).encode("utf-8")
            committed = store.commit(product_id, files, expected_revision=snapshot.head,
                                     metadata={"reason": "selftest stale pin"})
        if not committed.committed:
            fail("stale pin parity: could not commit a stale pin")
            return
        try:
            cli_status = _cli_status_json(folder, product_id)
        except Exception as exc:  # noqa: BLE001
            fail("stale pin parity: pmos status failed with a stale pin: %s" % exc)
            return
        if cli_status["question_banks"]["pinned"].get(contract["banks"][0]["id"]) != "c0000000000000000":
            fail("stale pin parity: the stale pin did not take")
            return
        if cli_status["phases"][0]["phase"] != "DISCOVER-STALE-PIN":
            fail("stale pin parity: pmos status --json's own phases do not reflect the stale "
                 "pin, so this scenario proves nothing: %r" % cli_status["phases"][0])
            return
        runtime_status = rs.status({"path": folder, "product_id": product_id})
        if not runtime_status.get("ok"):
            fail("stale pin parity: runtime_status.status failed with a stale pin: %s"
                 % runtime_status.get("error"))
            return
        if runtime_status["phases"] != cli_status["phases"]:
            fail("stale pin parity: phases differ from `pmos status --json` with a stale pin")


def check_runtime_parity_phases_error(fail):
    """runtime_status.status() falls back to phases [] plus phases_error exactly as status does.

    Proves: a symlinked *.md file under the workspace drives pmos.artifacts.scan
    (called from phase_report) into raising ValidationError, the same way the
    module's own docstring names a symlinked artifact as an example; both
    `pmos status --json` and the runtime tool must fall back to phases: []
    with a phases_error string rather than letting that exception escape, or
    (for the runtime tool) turning into an {"ok": false} response. Removing
    the try/except around phase_report, or routing it outside the Conductor
    construction's own try/except, would fail this check, because this is the
    one scenario in this file that actually drives phase_report to raise.
    """
    with TemporaryDirectory() as folder:
        product_id = "selftest-symlink-product"
        output = io.StringIO()
        with redirect_stdout(output):
            code = pmos_cli.main(["init", "--path", folder, "--product-id", product_id])
        if code != 0:
            fail("phases_error parity: pmos init exited %d" % code)
            return
        target = Path(folder) / "real.md"
        target.write_text("# Real\n", encoding="utf-8")
        link = Path(folder) / "linked.md"
        try:
            link.symlink_to(target)
        except OSError as exc:
            fail("phases_error parity: could not create a symlink to exercise scan() (%s)" % exc)
            return
        try:
            cli_status = _cli_status_json(folder, product_id)
        except Exception as exc:  # noqa: BLE001
            fail("phases_error parity: pmos status failed with a symlinked artifact: %s" % exc)
            return
        if cli_status.get("phases") != [] or not cli_status.get("phases_error"):
            fail("phases_error parity: pmos status --json did not fall back to phases_error "
                 "for a symlinked artifact: %r" % cli_status)
            return
        runtime_status = rs.status({"path": folder, "product_id": product_id})
        if not runtime_status.get("ok"):
            fail("phases_error parity: runtime_status.status failed with a symlinked artifact: %s"
                 % runtime_status.get("error"))
            return
        if runtime_status.get("phases") != []:
            fail("phases_error parity: runtime_status.status did not return an empty phases "
                 "list for a symlinked artifact: %r" % runtime_status)
        if not runtime_status.get("phases_error"):
            fail("phases_error parity: runtime_status.status did not set phases_error for a "
                 "symlinked artifact: %r" % runtime_status)


def check_runtime_parity_corrupt_pin(fail):
    """runtime_status.status() falls back to phases [] plus phases_error when the pin itself is corrupt.

    Proves: a non-JSON PIN_PATH, the exact corruption
    tests/test_pmos_cli.py::test_a_corrupt_pin_is_reported_rather_than_raised commits with
    self.pin(folder, b"{"), drives product_conductor() itself (not phase_report()) into raising
    ValidationError while building the Conductor from the pinned contract. The runtime tool must
    still come back as {"ok": true, "phases": [], "phases_error": ...}, never {"ok": false, ...}
    and never a traceback. Moving `conductor = product_conductor(...)` back outside status()'s inner
    try/except would leave this check red: the ValidationError would then escape uncaught to the
    outer except tuple, which does not list ValidationError, so it would propagate out of status()
    as an unhandled exception instead of being reported as ok true with a phases_error.
    """
    with TemporaryDirectory() as folder:
        product_id = "selftest-corrupt-pin-product"
        output = io.StringIO()
        with redirect_stdout(output):
            code = pmos_cli.main(["init", "--path", folder, "--product-id", product_id])
        if code != 0:
            fail("corrupt pin parity: pmos init exited %d" % code)
            return
        database = Path(folder) / ".pmos" / "runtime.sqlite"
        with rs.Store(database) as store:
            snapshot = store.read_snapshot(product_id)
            files = dict(snapshot.files)
            files[pmos_cli.PIN_PATH] = b"{"
            committed = store.commit(product_id, files, expected_revision=snapshot.head,
                                     metadata={"reason": "selftest corrupt pin"})
        if not committed.committed:
            fail("corrupt pin parity: could not commit a corrupt pin")
            return
        try:
            runtime_status = rs.status({"path": folder, "product_id": product_id})
        except Exception as exc:  # noqa: BLE001, this is exactly what must not happen
            fail("corrupt pin parity: status() raised %s instead of an ok true phases_error fallback (%s)"
                 % (exc.__class__.__name__, exc))
            return
        if runtime_status.get("ok") is not True:
            fail("corrupt pin parity: expected ok true with a phases_error fallback, got %r"
                 % runtime_status)
            return
        if runtime_status.get("phases") != []:
            fail("corrupt pin parity: expected an empty phases list for a corrupt pin, got %r"
                 % runtime_status)
        if not runtime_status.get("phases_error") or "not valid JSON" not in runtime_status["phases_error"]:
            fail("corrupt pin parity: expected phases_error to name the invalid JSON, got %r"
                 % runtime_status)
            return
        # Parity with the CLI for the same corrupt pin. `pmos status --json` cannot build the
        # Conductor either: it reports the failure as interview_error and carries no phases. The
        # runtime tool reports the same failure as phases [] plus phases_error. The two must carry
        # the same message, and neither may report a phase.
        try:
            cli_status = _cli_status_json(folder, product_id)
        except Exception as exc:  # noqa: BLE001
            fail("corrupt pin parity: pmos status failed with a corrupt pin: %s" % exc)
            return
        if cli_status.get("phases"):
            fail("corrupt pin parity: pmos status --json reported phases for a corrupt pin: %r"
                 % cli_status["phases"])
        if cli_status.get("interview_error") != runtime_status["phases_error"]:
            fail("corrupt pin parity: phases_error %r differs from the interview_error %r that "
                 "`pmos status --json` reports for the same corrupt pin"
                 % (runtime_status["phases_error"], cli_status.get("interview_error")))


def check_corrupt_runtime_database(fail):
    """A non-SQLite runtime database returns ok false with an error, never a traceback.

    Proves: a .pmos/runtime.sqlite that is present but is not a SQLite file at all (plain garbage
    bytes, never created through `pmos init`) drives Store's own migration step into raising
    sqlite3.DatabaseError when status() opens it. That must still come back as {"ok": false,
    "error": ...}, not an unhandled exception. Removing sqlite3.DatabaseError from status()'s outer
    except tuple would leave this check red, because that is the one exception type this scenario
    actually raises; no existing check before this one ever points status() at a corrupt,
    non-SQLite runtime database.
    """
    with TemporaryDirectory() as folder:
        pmos_dir = Path(folder) / ".pmos"
        pmos_dir.mkdir()
        (pmos_dir / "runtime.sqlite").write_bytes(b"not a sqlite database, just garbage bytes")
        try:
            result = rs.status({"path": folder, "product_id": "no-such-product"})
        except Exception as exc:  # noqa: BLE001, this is exactly what must not happen
            fail("corrupt database: status() raised %s instead of returning ok false (%s)"
                 % (exc.__class__.__name__, exc))
            return
        if result.get("ok") is not False or not result.get("error"):
            fail("corrupt database: expected {'ok': False, 'error': ...}, got %r" % result)


def check_missing_runtime(fail):
    """A missing runtime returns ok false with an error, never a traceback.

    Proves: calling runtime_status.status against a workspace that was never
    initialized (a bare temporary folder, no .pmos runtime database) neither
    raises nor returns a success; it comes back as {"ok": false, "error": a
    message naming what to run instead}, the contract every caller of status()
    depends on.
    """
    with TemporaryDirectory() as folder:
        try:
            result = rs.status({"path": folder, "product_id": "no-such-product"})
        except Exception as exc:  # noqa: BLE001, this is exactly what must not happen
            fail("missing runtime: status() raised %s instead of returning ok false (%s)"
                 % (exc.__class__.__name__, exc))
            return
        if result.get("ok") is not False or not result.get("error"):
            fail("missing runtime: expected {'ok': False, 'error': ...}, got %r" % result)


def main():
    failures = []
    fail = failures.append
    root = mt.repo_root()
    manifest = mt.load_manifest(root)
    entries = manifest["tasks"]
    tools = mt.build_tools(root, manifest)

    if len(tools) != len(entries):
        fail("generated %d tools for %d manifest entries"
             % (len(tools), len(entries)))
    if [t["name"] for t in tools] != [e["id"] for e in entries]:
        fail("tool order or naming does not match the manifest entry order")
    if len(set(t["name"] for t in tools)) != len(tools):
        fail("tool names are not unique")

    rules = mt.invariant_rules(root)
    if len(rules) != 7:
        fail("read %d invariant rules from %s, expected the seven"
             % (len(rules), mt.INVARIANTS_REL))

    for tool in tools:
        name = tool["name"]
        if not mt.NAME_RE.match(name):
            fail("%s is not a legal MCP tool name" % name)
        text = tool["description"] + "\n" + mt.plan_text(
            tool["entry"], root, request="a request", rules=rules)
        if len(tool["description"]) < 80:
            fail("%s: description is too thin to route on" % name)
        if "signs no gate" not in tool["description"]:
            fail("%s: description does not say it signs no gate" % name)
        for char, label in BANNED_CHARS.items():
            if char in text:
                fail("%s: output contains an %s" % (name, label))
        for banned in ("TBD", "TODO", "FIXME", "XXX"):
            if banned in text:
                fail("%s: output contains the placeholder %s" % (name, banned))
        for pattern in SECRET_SHAPES:
            if re.search(pattern, text):
                fail("%s: output matches a credential shape (%s)"
                     % (name, pattern))
        check_schema(tool["inputSchema"], name, fail)

    check_runtime_tool(fail)
    check_runtime_parity(fail)
    check_runtime_parity_with_stale_pin(fail)
    check_runtime_parity_phases_error(fail)
    check_runtime_parity_corrupt_pin(fail)
    check_corrupt_runtime_database(fail)
    check_missing_runtime(fail)

    code, stderr = sdk_absent_output(root)
    first_line = stderr.split("\n")[-1] if stderr else ""
    if code == 0:
        fail("SDK-absent run exited 0; it must exit non-zero")
    if "Traceback" in stderr:
        fail("SDK-absent run raised a traceback instead of one clear line")
    if "pip install mcp" not in first_line:
        fail("SDK-absent message does not name what to install: %r" % first_line)

    for problem in failures:
        print("selftest: %s" % problem)
    if failures:
        print("\n%d failure(s)." % len(failures), file=sys.stderr)
        return 1
    print("desktop adapter: ok (%d tools from %d manifest entries, schemas "
          "valid, SDK-absent path exits %d with one line)"
          % (len(tools), len(entries), code))
    print("SDK-absent line: %s" % first_line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
