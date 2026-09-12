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

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import ext_ai_probe as probe  # noqa: E402
from pmos.sidecars import SidecarFilter, is_appledouble_sidecar, is_appledouble_sidecar_path  # noqa: E402


def _calls(source, name):
    """Yield (line, full_call_text) for every `name(` call, parens balanced."""
    for match in re.finditer(re.escape(name) + r"\(", source):
        i, depth = match.end(), 1
        while depth and i < len(source):
            depth += {"(": 1, ")": -1}.get(source[i], 0)
            i += 1
        yield source[:match.start()].count("\n") + 1, source[match.start():i]


def _unbounded_subprocess_calls(directory):
    """Every subprocess.run call under ``directory`` missing a timeout kwarg.

    Shared by the real guard below and by ExfatSidecarsDoNotCrashTheToolsScan,
    so the synthetic-sidecar test exercises this exact code path rather than
    a copy of it. A checkout on exFAT/FAT/SMB carries a macOS AppleDouble
    sidecar (``._name.py``) beside every real script; its body is not UTF-8,
    and read_text() raised UnicodeDecodeError on it before this guard.
    """
    unbounded = []
    sidecars = SidecarFilter(directory)
    for path in sorted(Path(directory).glob("*.py")):
        if sidecars.excused(path):
            continue
        source = path.read_text(encoding="utf-8")
        for line, call in _calls(source, "subprocess.run"):
            if "timeout" not in call:
                unbounded.append("%s:%d" % (path.name, line))
    return unbounded


class SubprocessesAreBounded(unittest.TestCase):
    """R6, second review: gateway discovery ran with no timeout after generation
    had been given one. An unbounded subprocess can hang a release gate."""

    def test_every_subprocess_run_under_tools_passes_a_timeout(self):
        unbounded = _unbounded_subprocess_calls(TOOLS)
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


class ExfatSidecarsDoNotCrashTheToolsScan(unittest.TestCase):
    """P0-EXFAT: a macOS AppleDouble sidecar (``._name.py``) beside a real
    script under tools/ used to crash this file's own subprocess-timeout scan
    with UnicodeDecodeError, because TOOLS.glob("*.py") picked it up and
    read_text() assumed UTF-8. Synthesized here so the guard runs on Linux CI,
    which never grows a real one."""

    def test_a_synthetic_appledouble_sidecar_is_skipped_not_read(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            fake_tools = Path(directory)
            real = fake_tools / "demo.py"
            real.write_text("import subprocess\nsubprocess.run([], timeout=1)\n",
                            encoding="utf-8")
            sidecar = fake_tools / "._demo.py"
            sidecar.write_bytes(b"\x00\x05\x16\x07" + b"\xb0" * 12)

            # Calls the exact function test_every_subprocess_run_under_tools_
            # passes_a_timeout uses, so this test exercises the real guard
            # rather than a copy of it.
            self.assertEqual(_unbounded_subprocess_calls(fake_tools), [])

    def test_a_dotfile_with_no_magic_header_is_still_read(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            fake_tools = Path(directory)
            (fake_tools / "demo.py").write_text("x = 1\n", encoding="utf-8")
            plain_dotfile = fake_tools / "._demo.py"
            plain_dotfile.write_text("not a sidecar\n", encoding="utf-8")
            self.assertFalse(is_appledouble_sidecar_path(plain_dotfile),
                             "a dotfile with no AppleDouble magic must not "
                             "be excused")

    def test_a_directory_named_dot_underscore_is_never_a_sidecar(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            fake_tools = Path(directory)
            weird_dir = fake_tools / "._notasidecar"
            weird_dir.mkdir()
            self.assertFalse(is_appledouble_sidecar_path(weird_dir),
                             "a directory can never be an AppleDouble sidecar")


class SidecarPredicatesAgree(unittest.TestCase):
    """The policy names two copies of this judgement: pmos/sidecars.py
    (magic-byte, positive recognition) and tools/review_gate.py's
    is_excluded_sidecar (name-only, gated by git tracked-ness elsewhere).
    Whenever pmos/sidecars.py positively proves a name is a real AppleDouble
    sidecar, review_gate's name-only check must also flag that same name --
    otherwise a real sidecar could be excluded from a loader here and still
    hashed into a review digest there, or vice versa in a way that widens
    review_gate's git-safety net rather than narrowing it."""

    def test_every_real_sidecar_is_also_recognized_by_name_by_review_gate(self):
        import tempfile

        tools_dir = str(REPO / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import review_gate  # noqa: E402

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "real.md").write_text("content\n", encoding="utf-8")
            sidecar = base / "._real.md"
            sidecar.write_bytes(b"\x00\x05\x16\x07" + b"\x00" * 12)
            self.assertTrue(is_appledouble_sidecar(base, "._real.md"))
            self.assertTrue(review_gate.is_excluded_sidecar("._real.md"))


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
        source = (REPO / "tests" / "test_pmos_probe.py").read_text(encoding="utf-8")
        self.assertIn("def _direct(case)", source)
        self.assertIn("def _gateway(case)", source)
        self.assertIn("test_both_transports_agree_on_every_row", source)

    def test_the_matrix_covers_the_reviewed_conditions(self):
        source = (REPO / "tests" / "test_pmos_probe.py").read_text(encoding="utf-8")
        rows = set(re.findall(r'\{"id":\s*"([a-z0-9-]+)"', source))
        required = {"cost-missing", "cost-null", "cost-negative", "cost-nan",
                    "cost-infinite", "overcharge-on-zero-budget",
                    "model-substituted", "model-missing", "provider-raises",
                    "empty-output", "clean-free-call"}
        self.assertTrue(required <= rows, "matrix lost rows: %s" % (required - rows))


class TestClassesCannotVanish(unittest.TestCase):
    """Fourth review round: commit a92cefa deleted four tests from
    test_pmos_skills.py by slicing to a moved __main__ block, no gate noticed,
    and a grep found the loss five merges later. The module-in-CI guard below
    cannot see a class go missing from a module that is still run. This one
    can: the classes each root module defines must equal the committed
    inventory, so a deletion, a rename or an addition has to touch
    docs/readiness/test-classes.json in the same change.
    """

    INVENTORY = REPO / "docs" / "readiness" / "test-classes.json"

    def test_every_root_test_module_defines_exactly_its_inventoried_classes(self):
        import json
        inventory = json.loads(self.INVENTORY.read_text(encoding="utf-8"))["modules"]
        on_disk = {}
        for path in sorted((REPO / "tests").glob("test_*.py")):
            source = path.read_text(encoding="utf-8")
            on_disk[path.stem] = sorted(re.findall(
                r"^class (\w+)\((?:unittest\.)?TestCase\):", source, re.M))
        self.assertEqual(sorted(on_disk), sorted(inventory),
                         "root test modules differ from the inventory")
        for module in sorted(on_disk):
            missing = sorted(set(inventory[module]) - set(on_disk[module]))
            extra = sorted(set(on_disk[module]) - set(inventory[module]))
            self.assertEqual(missing, [], "%s lost test classes: %s" % (module, missing))
            self.assertEqual(extra, [], "%s gained classes not in the inventory "
                                        "(add them to docs/readiness/test-classes.json): %s"
                             % (module, extra))

    def test_the_inventory_names_the_classes_that_went_missing_once(self):
        import json
        inventory = json.loads(self.INVENTORY.read_text(encoding="utf-8"))["modules"]
        self.assertIn("UnpriceableCatalogRowsTests", inventory["test_pmos_skills"])


class RegressionsReachHostedCI(unittest.TestCase):
    """Finding 7, first probe review: 346 tests passed locally and none of the
    new ones ran in CI, because the module was not in the canonical list."""

    def test_every_root_test_module_is_in_the_canonical_gate(self):
        import ci_gate
        argv = {a for gate in ci_gate.GATES for a in gate.argv}
        on_disk = {p.stem for p in (REPO / "tests").glob("test_*.py")}
        missing = sorted(on_disk - argv)
        self.assertEqual(missing, [],
                         "test modules CI never runs: %s" % missing)

    def test_the_full_suite_criterion_runs_every_root_test_module(self):
        """CI-1, 2026-09-10: the full-suite probe kept its own list of root
        modules, three shipped modules were never on it, and the criterion
        "every shipped root test runs" counted 371 root tests while the
        release gate ran 516. Nothing compared the two lists."""
        import ci_gate
        import readiness_probe
        on_disk = sorted(p.stem for p in (REPO / "tests").glob("test_*.py"))
        self.assertEqual(readiness_probe.root_test_modules(), on_disk)
        gate = next(g for g in ci_gate.GATES if g.gate_id == "root-tests")
        self.assertEqual(sorted(a for a in gate.argv if a.startswith("test_")),
                         on_disk,
                         "the release gate and the full-suite criterion must "
                         "run the same root modules")


if __name__ == "__main__":
    unittest.main()
