#!/usr/bin/env python3
"""Canonical local/CI release gate for the PM OS.

The workflow invokes this file; it does not carry a second hand-maintained
list of release checks. ``--manifest`` is machine-readable so the readiness
evaluator can prove which gates that active invocation owns.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Gate:
    gate_id: str
    argv: tuple
    cwd: str = "."
    expects_tests: bool = False
    required_output: str = ""
    timeout: int = 1200


GATES = (
    Gate("compile", ("python3", "tools/readiness_probe.py", "compile-all")),
    Gate("root-tests", ("python3", "-m", "unittest", "-v",
         "test_lint", "test_readiness", "test_pmos_routing",
         "test_pmos_store", "test_pmos_domain", "test_pmos_operations",
         "test_pmos_hooks", "test_pmos_usecases", "test_pmos_conductor",
         "test_pmos_skills", "test_pmos_cli", "test_pmos_release",
         "test_pmos_security", "test_pmos_review"), expects_tests=True,
         timeout=1800),
    Gate("harness-tests", ("python3", "-m", "unittest", "discover", "-s",
         "harness", "-p", "test_*.py", "-v"), expects_tests=True,
         timeout=1800),
    Gate("regulated-tests", ("python3", "-m", "unittest", "test_lint", "-v"),
         cwd="modules/regulated", expects_tests=True),
    Gate("claude-adapter", ("python3",
         "harness/adapters/claude-code/generate.py", "--check")),
    Gate("desktop-adapter", ("python3",
         "harness/adapters/desktop/selftest.py")),
    Gate("workspace-lifecycle", ("python3", "tools/readiness_probe.py",
         "workspace-lifecycle")),
    Gate("workspace-links", ("python3", "tools/readiness_probe.py",
         "workspace-links")),
    Gate("workspace-contract", ("python3",
         "tools/check_workspace_contract.py", "--quiet")),
    Gate("regulated-example", ("python3", "lint.py",
         "modules/regulated/examples/dispute-summary/PRD.md")),
    Gate("os-tree", ("python3", "lint.py", "--os")),
    Gate("json-syntax", ("python3", "lint.py", "--json-syntax")),
    Gate("graph-freshness", ("python3", "tools/graph.py", "--check")),
    Gate("manifest-contract", ("python3", "tools/check_manifest.py",
         "--quiet")),
    Gate("frontmatter", ("python3", "tools/frontmatter_init.py", "--dry-run"),
         required_output="created: 0, extended: 0"),
    Gate("security-policy", ("python3", "tools/security_gate.py")),
    Gate("docs-contract", ("python3", "tools/docs_contract.py", "--strict")),
    Gate("readiness-local", ("python3", "tools/readiness.py", "--local"),
         timeout=3600),
)


def environment():
    allowed = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR", "TEMP",
               "TMP", "SYSTEMROOT")
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    return env


def manifest():
    return {
        "schema": 1,
        "gates": [
            {"id": gate.gate_id, "argv": list(gate.argv), "cwd": gate.cwd,
             "expects_tests": gate.expects_tests,
             "required_output": gate.required_output}
            for gate in GATES
        ],
    }


def run_gate(gate):
    argv = list(gate.argv)
    if argv[0] == "python3":
        argv[0] = sys.executable
    started = time.monotonic()
    try:
        done = subprocess.run(
            argv, cwd=str(REPO / gate.cwd), shell=False, capture_output=True,
            text=True, env=environment(), timeout=gate.timeout)
        output = (done.stdout or "") + (done.stderr or "")
        code = done.returncode
    except subprocess.TimeoutExpired:
        output = "timed out after %d seconds" % gate.timeout
        code = None
    reasons = []
    if code != 0:
        reasons.append("exit %s" % code)
    tests = None
    if gate.expects_tests:
        found = re.search(r"^Ran (\d+) tests?", output, re.M)
        tests = int(found.group(1)) if found else 0
        if tests == 0:
            reasons.append("zero tests")
        if any(token in output for token in
               ("skipped=", "expected failures=", "unexpected successes=")):
            reasons.append("non-passing test disposition")
    if gate.required_output and gate.required_output not in output:
        reasons.append("required output missing")
    return {
        "id": gate.gate_id,
        "passed": not reasons,
        "exit_code": code,
        "tests": tests,
        "seconds": round(time.monotonic() - started, 3),
        "reasons": reasons,
        "output_tail": output.strip()[-1200:] if reasons else "",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--manifest", action="store_true")
    parser.add_argument("--gate", action="append", default=[],
                        help="run only this exact gate id (repeatable)")
    args = parser.parse_args(argv)
    if args.manifest:
        print(json.dumps(manifest(), sort_keys=True))
        return 0
    selected = set(args.gate)
    known = {gate.gate_id for gate in GATES}
    unknown = selected - known
    if unknown:
        print("unknown gate(s): %s" % ", ".join(sorted(unknown)))
        return 2
    rows = []
    for gate in GATES:
        if selected and gate.gate_id not in selected:
            continue
        row = run_gate(gate)
        rows.append(row)
        print("[%s] %-22s %.2fs" %
              ("PASS" if row["passed"] else "FAIL", row["id"],
               row["seconds"]))
        if not row["passed"]:
            print("       %s" % "; ".join(row["reasons"]))
            if row["output_tail"]:
                print(row["output_tail"])
    passed = sum(row["passed"] for row in rows)
    print("release gates: %d/%d passed" % (passed, len(rows)))
    return 0 if rows and passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
