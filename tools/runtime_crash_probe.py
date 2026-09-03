#!/usr/bin/env python3
"""Kill a real process at one explicit PM OS transaction boundary.

This helper is test-only.  It intentionally terminates itself with SIGKILL so
the parent test can reopen SQLite and prove which side of the commit became
durable.  The fault point is selected from a closed allow-list.
"""

from __future__ import annotations

import argparse
import os
import signal
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from pmos.store import MemoryClass, Store  # noqa: E402


POINTS = frozenset({
    "prepare.before_commit", "prepare.after_commit",
    "publish.before_commit", "publish.after_commit",
    "enqueue.before_commit", "enqueue.after_commit",
    "memory.before_commit", "memory.after_commit",
})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("database")
    parser.add_argument("point", choices=sorted(POINTS))
    args = parser.parse_args(argv)

    def crash(point):
        if point == args.point:
            os.kill(os.getpid(), signal.SIGKILL)

    store = Store(Path(args.database), fault_injector=crash)
    try:
        operation = args.point.split(".", 1)[0]
        if operation in ("prepare", "publish"):
            store.create_product("crash-product")
        if operation == "prepare":
            store.prepare_commit(
                "crash-product", {"state.md": "prepared payload"})
        elif operation == "publish":
            prepared = store.prepare_commit(
                "crash-product", {"state.md": "published payload"})
            store.publish(prepared)
        elif operation == "enqueue":
            store.enqueue({"work": "durable"}, idempotency_key="crash-job")
        elif operation == "memory":
            store.append_memory(
                "task", MemoryClass.EVIDENCE, "crash-evidence", "durable",
                task_id="crash-task")
        else:  # pragma: no cover - argparse and POINTS make this unreachable.
            return 2
    finally:
        store.close()
    # Reaching here means a declared fault point disappeared from production
    # code, which must make the parent test fail.
    return 3


if __name__ == "__main__":
    sys.exit(main())
