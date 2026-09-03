#!/usr/bin/env python3
"""MCP server for product-manager-OS. Standard library plus the MCP SDK.

    python3 harness/adapters/desktop/server.py
    python3 harness/adapters/desktop/server.py --list
    python3 harness/adapters/desktop/server.py --plan conduct-product-journey

Speaks MCP over stdio and exposes one tool per entry in harness/MANIFEST.json,
generated at start from that file. Any desktop client that speaks MCP therefore
gets the same task list, off the same contract, as the CLI and the agent
runtime.

A tool returns the plan and the governing file paths for its route. It runs no
model call, writes no file, sends nothing, and signs no gate. This is a task
list and plan surface, not an autonomous runner.

Two things make it fail closed. The manifest agreement gate
(tools/check_manifest.py) runs before the first tool is generated, and the
server refuses to serve a manifest that disagrees with the router table in
CLAUDE.md or that names a file the tree does not have. If the checker itself
cannot be loaded, that is also a refusal: never skip the check.

Credentials (OMNIROUTE_BASE_URL and OMNIROUTE_API_KEY) are read from the
environment at call time by whatever actually places a model call. This server
places none, reports presence only, and never logs a value.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manifest_tools as mt  # noqa: E402

SDK_MISSING = ("product-manager-OS desktop adapter needs the MCP SDK, which is "
               "not installed for this interpreter (%s). Install it with: "
               "python3 -m pip install mcp (Python 3.10 or newer), then run: "
               "python3 harness/adapters/desktop/server.py. Until then use "
               "--list or --plan, which need only the standard library.")

# The one dependency outside the standard library, and the one place it is
# imported. A missing SDK is a supported state, not a traceback: the plan
# surface below still works, so the failure has to stay legible.
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    SDK_ERROR = None
except ImportError as exc:  # pragma: no cover, exercised by selftest.py
    Server = stdio_server = TextContent = Tool = None
    SDK_ERROR = str(exc)


def agreement_gate(root):
    """Run tools/check_manifest.py. Returns a refusal string, or None when green.

    Fail closed in both directions: a failing checker refuses, and a checker
    that cannot be loaded refuses too. A server that skips its own gate is the
    failure this repository exists to prevent.
    """
    checker = Path(root) / mt.CHECKER_REL
    if not checker.is_file():
        return ("the agreement gate %s is missing, so the manifest cannot be "
                "proven to agree with the router table in CLAUDE.md. Halting "
                "rather than serving an unchecked contract." % mt.CHECKER_REL)
    try:
        spec = importlib.util.spec_from_file_location("pmos_check_manifest", checker)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        problems = module.check_manifest(Path(root))
    except Exception as exc:  # noqa: BLE001, any checker failure is a refusal
        return ("the agreement gate could not run (%s: %s). Halting rather "
                "than serving an unchecked contract."
                % (exc.__class__.__name__, exc))
    if problems:
        first = "; ".join("%s:%s %s %s" % p for p in problems[:3])
        return ("the agreement gate found %d problem(s), so the manifest and "
                "CLAUDE.md disagree: %s. Fix the contract, then start the "
                "server." % (len(problems), first))
    return None


def build(root=None, gate=True):
    """Tools generated from the manifest, after the agreement gate has passed."""
    root = mt.repo_root() if root is None else Path(root)
    if gate:
        refusal = agreement_gate(root)
        if refusal:
            raise SystemExit("product-manager-OS desktop adapter halted: %s"
                             % refusal)
    return root, mt.build_tools(root)


def make_server(root=None, gate=True):
    """Wire the generated tools onto an MCP server. Requires the SDK."""
    if SDK_ERROR is not None:
        raise SystemExit(SDK_MISSING % SDK_ERROR)
    root, tools = build(root, gate=gate)
    by_name = {t["name"]: t["entry"] for t in tools}
    rules = mt.invariant_rules(root)
    server = Server("product-manager-os")

    @server.list_tools()
    async def list_tools():
        return [Tool(name=t["name"], description=t["description"],
                     inputSchema=t["inputSchema"]) for t in tools]

    @server.call_tool()
    async def call_tool(name, arguments):
        entry = by_name.get(name)
        if entry is None:
            known = ", ".join(sorted(by_name))
            return [TextContent(type="text", text=(
                "No route named %s is in harness/MANIFEST.json. The routes "
                "are: %s." % (name, known)))]
        arguments = arguments or {}
        text = mt.plan_text(
            entry, root,
            request=arguments.get("request"),
            include_file_text=bool(arguments.get("include_file_text")),
            rules=rules)
        return [TextContent(type="text", text=text)]

    return server, tools


async def serve(root=None):
    server, tools = make_server(root)
    print("product-manager-os: %d tools generated from %s"
          % (len(tools), mt.MANIFEST_REL), file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream,
                         server.create_initialization_options())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=None,
                        help="repository root (default: the tree holding "
                             "harness/MANIFEST.json)")
    parser.add_argument("--list", action="store_true",
                        help="print the generated tool names and exit")
    parser.add_argument("--plan", metavar="ROUTE",
                        help="print one route's plan and exit")
    parser.add_argument("--no-gate", action="store_true",
                        help="skip the agreement gate. For debugging a broken "
                             "contract only, never for serving")
    args = parser.parse_args(argv)

    root, tools = build(args.root, gate=not args.no_gate)

    if args.list:
        for tool in tools:
            entry = tool["entry"]
            print("%-34s %-9s %s" % (tool["name"], entry.get("tier"),
                                     entry.get("stage") or "no gate"))
        print("%d tools, one per manifest entry." % len(tools))
        return 0

    if args.plan:
        entry = next((t["entry"] for t in tools if t["name"] == args.plan), None)
        if entry is None:
            print("no route named %s. Try --list." % args.plan, file=sys.stderr)
            return 1
        print(mt.plan_text(entry, root))
        return 0

    if SDK_ERROR is not None:
        print(SDK_MISSING % SDK_ERROR, file=sys.stderr)
        return 2

    import asyncio
    asyncio.run(serve(args.root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
