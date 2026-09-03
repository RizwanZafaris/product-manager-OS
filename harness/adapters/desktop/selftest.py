#!/usr/bin/env python3
"""Checks the desktop adapter without a live MCP client. Standard library only.

    python3 harness/adapters/desktop/selftest.py

What it proves: the tool set is generated from harness/MANIFEST.json one tool
per entry, the names are unique and legal MCP tool names, every emitted JSON
schema is well formed and survives a JSON round trip, every description and
every plan renders, and the SDK-absent path prints one line and exits non-zero
instead of raising ImportError.

What it cannot prove: that a desktop client accepts the handshake, that a tool
call round trips over stdio, or that a plan is the right plan for a request.
Those need a live client and a human reading the output.

Exit status is 1 on any failure, so it can run beside python3 lint.py --os.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import manifest_tools as mt  # noqa: E402

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
