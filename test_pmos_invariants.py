"""Guards against defect classes that have already recurred.

Three review rounds each found a fresh instance of a defect class the previous
round had fixed one example of. A unit test pins the example; it does nothing
for the next instance. Each guard here scans the code for the CLASS, so a
regression fails CI before it reaches a reviewer.

Every guard names the finding that motivated it.
"""

from __future__ import annotations

import math
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ext_ai_probe as probe  # noqa: E402


def _calls(source, name):
    """Yield (line, full_call_text) for every `name(` call, parens balanced."""
    for match in re.finditer(re.escape(name) + r"\(", source):
        i, depth = match.end(), 1
        while depth and i < len(source):
            depth += {"(": 1, ")": -1}.get(source[i], 0)
            i += 1
        yield source[:match.start()].count("\n") + 1, source[match.start():i]


class SubprocessesAreBounded(unittest.TestCase):
    """R6, second review: gateway discovery ran with no timeout after generation
    had been given one. An unbounded subprocess can hang a release gate."""

    def test_every_subprocess_run_under_tools_passes_a_timeout(self):
        unbounded = []
        for path in sorted(TOOLS.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for line, call in _calls(source, "subprocess.run"):
                if "timeout" not in call:
                    unbounded.append("%s:%d" % (path.name, line))
        self.assertEqual(unbounded, [],
                         "subprocess.run without timeout: %s" % unbounded)


class CostIsNeverManufactured(unittest.TestCase):
    """R2/R5 and the audit's aggregate-budget case: absent cost became $0.00.
    This enumerates the value domain rather than sampling it, because sampling
    is how None was fixed while NaN, absent-key and bool each shipped later."""

    TABLE = (
        (None, "UNKNOWN"),
        (0, "OK"), (0.0, "OK"), (0.75, "OK"), (1, "OK"),
        (-0.01, "INVALID"), (-1, "INVALID"),
        (float("nan"), "INVALID"),
        (float("inf"), "INVALID"), (float("-inf"), "INVALID"),
        (True, "INVALID"), (False, "INVALID"),
        ("0.5", "INVALID"), ("free", "INVALID"), ("", "INVALID"),
        ([1], "INVALID"), ({}, "INVALID"), (object(), "INVALID"),
    )

    def test_usable_cost_over_the_whole_value_domain(self):
        for value, expected in self.TABLE:
            with self.subTest(value=repr(value)):
                cost, status = probe.usable_cost(value)
                self.assertEqual(status, expected)
                if status == "OK":
                    self.assertIsInstance(cost, float)
                    self.assertTrue(math.isfinite(cost) and cost >= 0)
                else:
                    self.assertIsNone(cost)

    def test_no_billed_cost_is_coerced_with_or_zero(self):
        """`x or 0.0` on a cost field is the exact idiom that manufactured $0.00.
        Advertised *price* for reservation is exempt and named explicitly."""
        source = (TOOLS / "ext_ai_probe.py").read_text(encoding="utf-8")
        offenders = []
        for line_no, line in enumerate(source.splitlines(), 1):
            if re.search(r"cost_usd[^\n]*\bor\s+0(\.0)?\b", line):
                offenders.append("%d: %s" % (line_no, line.strip()))
        self.assertEqual(offenders, [], offenders)

    def test_cost_status_vocabulary_is_closed(self):
        source = (TOOLS / "ext_ai_probe.py").read_text(encoding="utf-8")
        found = set(re.findall(r'"cost_status":\s*"?([A-Z]+)"?', source))
        found |= set(re.findall(r'return None, "([A-Z]+)"', source))
        self.assertTrue(found <= {"OK", "UNKNOWN", "INVALID"}, found)


class GitPathsKeepTheirBytes(unittest.TestCase):
    """Finding 1, first review of the gate: text=True rewrote a CR inside a
    tracked filename and the file vanished from the review."""

    def test_the_review_gate_never_reads_git_path_output_as_text(self):
        source = (REPO / "tools" / "review_gate.py").read_text(encoding="utf-8")
        for line, call in _calls(source, "subprocess.run"):
            if '"ls-files"' in call or "ls-files" in call:
                self.assertNotIn("text=True", call,
                                 "review_gate.py:%d reads paths as text" % line)


class TransportsShareOneContract(unittest.TestCase):
    """R2/R3/R4: each was found on one transport after the other was fixed.
    The matrix in test_pmos_probe is the contract; this guards that it stays
    two-sided and does not quietly shrink."""

    def test_the_matrix_is_asserted_on_both_transports(self):
        source = (REPO / "test_pmos_probe.py").read_text(encoding="utf-8")
        self.assertIn("def _direct(case)", source)
        self.assertIn("def _gateway(case)", source)
        self.assertIn("test_both_transports_agree_on_every_row", source)

    def test_the_matrix_covers_the_reviewed_conditions(self):
        source = (REPO / "test_pmos_probe.py").read_text(encoding="utf-8")
        rows = set(re.findall(r'\{"id":\s*"([a-z0-9-]+)"', source))
        required = {"cost-missing", "cost-null", "cost-negative", "cost-nan",
                    "cost-infinite", "overcharge-on-zero-budget",
                    "model-substituted", "model-missing", "provider-raises",
                    "empty-output", "clean-free-call"}
        self.assertTrue(required <= rows, "matrix lost rows: %s" % (required - rows))


class RegressionsReachHostedCI(unittest.TestCase):
    """Finding 7, first probe review: 346 tests passed locally and none of the
    new ones ran in CI, because the module was not in the canonical list."""

    def test_every_root_test_module_is_in_the_canonical_gate(self):
        import ci_gate
        argv = {a for gate in ci_gate.GATES for a in gate.argv}
        on_disk = {p.stem for p in REPO.glob("test_*.py")}
        missing = sorted(on_disk - argv)
        self.assertEqual(missing, [],
                         "test modules CI never runs: %s" % missing)


if __name__ == "__main__":
    unittest.main()
