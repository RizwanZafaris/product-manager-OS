#!/usr/bin/env python3
"""Claude Code command-hook adapter for the shared PM OS hook policy."""

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd()).resolve()
sys.path.insert(0, str(PROJECT))

from pmos.hooks import claude_output, decide  # noqa: E402


def stop_gate():
    done = subprocess.run(
        [sys.executable, "tools/ci_gate.py", "--gate", "compile", "--gate",
         "os-tree"], cwd=str(PROJECT), shell=False, capture_output=True,
        text=True, timeout=180)
    tail = ((done.stdout or "") + (done.stderr or "")).strip().splitlines()
    return done.returncode == 0, tail[-1] if tail else "no gate output"


def main():
    try:
        raw = sys.stdin.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError("hook input exceeds 1 MiB")
        payload = json.loads(raw)
        event = payload.get("hook_event_name")
    except (ValueError, json.JSONDecodeError, AttributeError) as error:
        event = "PreToolUse"
        payload = {}
        decision = decide(event, payload, PROJECT)
        output = claude_output(event, decision)
        output["systemMessage"] = "PM OS hook rejected malformed input: %s" % \
            type(error).__name__
        print(json.dumps(output, sort_keys=True))
        return 0
    gate = stop_gate if event in ("Stop", "SubagentStop", "TaskCompleted") \
        else None
    decision = decide(event, payload, PROJECT, gate_runner=gate)
    output = claude_output(event, decision)
    if output:
        print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
