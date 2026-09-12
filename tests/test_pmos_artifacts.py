#!/usr/bin/env python3
"""Tests for pmos/artifacts.py, the runtime's artifact reader.

    python3 -m unittest test_pmos_artifacts

The runtime ships pmos/ but not tools/, so the reader of the artifact
frontmatter contract lives in pmos/artifacts.py and tools/workspace.py imports
it rather than keeping a copy. These tests check that it does, then build a
small temporary workspace and exercise scan, build_manifest and check_manifest.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
for _entry in (str(REPO), str(REPO / "tools")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import workspace  # noqa: E402

from pmos import artifacts  # noqa: E402
from pmos.store import ValidationError  # noqa: E402


BLOCK_TEMPLATE = """---
artifact_id: {artifact_id}
phase: {phase}
gate: {gate}
status: {status}
depends_on: {depends_on}
template: {template}
---
{body}
"""


def block(artifact_id, phase, gate, status, depends_on, template, body):
    return BLOCK_TEMPLATE.format(
        artifact_id=artifact_id,
        phase=phase,
        gate=gate,
        status=status,
        depends_on=json.dumps(depends_on),
        template=template,
        body=body,
    )


class ArtifactManifestTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "demo" / "discovery").mkdir(parents=True)
        (self.root / "demo" / "planning").mkdir(parents=True)
        (self.root / "gates").mkdir()
        (self.root / ".pmos").mkdir()
        self.problem = block(
            "demo/discovery/problem-framing",
            "DISCOVER",
            1,
            "approved",
            [],
            "templates/discovery/problem-framing.md",
            "Body one.\n",
        )
        self.vision = block(
            "demo/planning/vision",
            "DEFINE",
            2,
            "draft",
            ["demo/discovery/problem-framing"],
            "templates/planning/vision.md",
            "Body two.\n",
        )
        self.strategy = block(
            "demo/planning/product-strategy",
            "DEFINE",
            2,
            "draft",
            ["demo/planning/vision"],
            "templates/planning/product-strategy.md",
            "Body three.\n",
        )
        self._write("demo/discovery/problem-framing.md", self.problem)
        self._write("demo/planning/vision.md", self.vision)
        self._write("demo/planning/product-strategy.md", self.strategy)
        self._write("README.md", block(
            "README",
            "DISCOVER",
            1,
            "draft",
            [],
            "README.md",
            "README body.\n",
        ))
        self._write("gates/gate-1.md", block(
            "gates/gate-1",
            "DISCOVER",
            1,
            "approved",
            [],
            "gates/gate-1.md",
            "Gate body.\n",
        ))
        self._write(".pmos/run.md", block(
            ".pmos/run",
            "DISCOVER",
            1,
            "draft",
            [],
            ".pmos/run.md",
            "Run body.\n",
        ))
        self._write("notes.md", "# Notes\n\nNo block here.\n")

    def _write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _expect_scan_ids(self):
        return {
            "demo/discovery/problem-framing",
            "demo/planning/vision",
            "demo/planning/product-strategy",
        }

    def test_tools_workspace_uses_the_runtime_reader(self):
        # One reader: a local copy in tools/workspace.py could drift from the runtime's.
        for name in ("FRONTMATTER_RE", "ARTIFACT_PHASES", "ARTIFACT_STATUSES",
                     "ARTIFACT_KEYS", "ARTIFACT_FIELD_RE", "parse_artifact",
                     "_parse_artifact_value", "not_an_artifact", "artifact_revision"):
            self.assertIs(getattr(workspace, name), getattr(artifacts, name), name)

    def test_scan_returns_three_artifacts(self):
        found = artifacts.scan(self.root)
        self.assertEqual(set(found), self._expect_scan_ids())
        self.assertEqual(found["demo/discovery/problem-framing"]["path"],
                         "demo/discovery/problem-framing.md")
        self.assertEqual(found["demo/planning/vision"]["path"],
                         "demo/planning/vision.md")
        self.assertEqual(found["demo/planning/product-strategy"]["path"],
                         "demo/planning/product-strategy.md")
        self.assertEqual(found["demo/discovery/problem-framing"]["gate"], 1)
        self.assertEqual(found["demo/planning/vision"]["gate"], 2)
        self.assertEqual(found["demo/planning/product-strategy"]["gate"], 2)
        self.assertEqual(found["demo/discovery/problem-framing"]["depends_on"],
                         [])
        self.assertEqual(found["demo/planning/vision"]["depends_on"],
                         ["demo/discovery/problem-framing"])
        self.assertEqual(
            found["demo/planning/product-strategy"]["depends_on"],
            ["demo/planning/vision"])
        self.assertEqual(found["demo/discovery/problem-framing"]["revision"],
                         artifacts.artifact_revision(self.problem))
        self.assertEqual(found["demo/planning/vision"]["revision"],
                         artifacts.artifact_revision(self.vision))
        self.assertEqual(found["demo/planning/product-strategy"]["revision"],
                         artifacts.artifact_revision(self.strategy))

    def test_build_manifest_gate_two(self):
        manifest = artifacts.build_manifest(self.root, 2)
        ids = [entry["id"] for entry in manifest["artifacts"]]
        dep_ids = [entry["id"] for entry in manifest["dependencies"]]
        self.assertEqual(ids,
                         ["demo/planning/product-strategy",
                          "demo/planning/vision"])
        self.assertEqual(dep_ids, ["demo/discovery/problem-framing"])

    def test_build_manifest_gate_one(self):
        manifest = artifacts.build_manifest(self.root, 1)
        ids = [entry["id"] for entry in manifest["artifacts"]]
        dep_ids = [entry["id"] for entry in manifest["dependencies"]]
        self.assertEqual(ids, ["demo/discovery/problem-framing"])
        self.assertEqual(dep_ids, [])

    def test_build_manifest_gate_five_is_empty(self):
        manifest = artifacts.build_manifest(self.root, 5)
        self.assertEqual(manifest, {"artifacts": [], "dependencies": []})

    def test_missing_dependency_is_validation_error(self):
        self._write("demo/planning/orphan.md", block(
            "demo/planning/orphan",
            "DEFINE",
            2,
            "draft",
            ["demo/discovery/missing"],
            "templates/planning/orphan.md",
            "Orphan body.\n",
        ))
        with self.assertRaises(ValidationError) as ctx:
            artifacts.build_manifest(self.root, 2)
        self.assertIn("depends on demo/discovery/missing and the workspace "
                      "does not have it yet", str(ctx.exception))

    def test_duplicate_artifact_id_is_validation_error(self):
        self._write("demo/discovery/duplicate.md", block(
            "demo/discovery/problem-framing",
            "DISCOVER",
            1,
            "draft",
            [],
            "templates/discovery/problem-framing.md",
            "Duplicate body.\n",
        ))
        with self.assertRaises(ValidationError) as ctx:
            artifacts.scan(self.root)
        self.assertIn("demo/discovery/problem-framing.md", str(ctx.exception))
        self.assertIn("demo/discovery/duplicate.md", str(ctx.exception))
        self.assertIn("artifact_id demo/discovery/problem-framing is carried by more than one file",
                      str(ctx.exception))

    def test_a_missing_dependency_is_named_against_the_file_that_declares_it(self):
        # The gate 3 artifact is fine; the vision it pulls in names an id the workspace lacks.
        self._write("demo/planning/vision.md", block(
            "demo/planning/vision", "DEFINE", 2, "draft",
            ["demo/discovery/problem-framing", "demo/discovery/missing"],
            "templates/planning/vision.md", "Body two.\n"))
        self._write("demo/architecture/design.md", block(
            "demo/architecture/design", "DESIGN", 3, "draft",
            ["demo/planning/vision"], "templates/architecture/design.md", "Design body.\n"))
        with self.assertRaises(ValidationError) as ctx:
            artifacts.build_manifest(self.root, 3)
        self.assertIn("demo/planning/vision depends on demo/discovery/missing", str(ctx.exception))

    def test_a_symlinked_file_is_refused(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        target = Path(outside.name) / "elsewhere.md"
        target.write_text("# Elsewhere\n", encoding="utf-8")
        (self.root / "demo" / "discovery" / "linked.md").symlink_to(target)
        with self.assertRaises(ValidationError) as ctx:
            artifacts.scan(self.root)
        self.assertIn("demo/discovery/linked.md is a symlink", str(ctx.exception))

    def test_check_manifest_unchanged(self):
        manifest = artifacts.build_manifest(self.root, 2)
        result = artifacts.check_manifest(self.root, manifest)
        self.assertEqual(result, {"changed": [], "reconcile": []})

    def test_check_manifest_changed_body(self):
        manifest = artifacts.build_manifest(self.root, 2)
        self._write("demo/discovery/problem-framing.md", block(
            "demo/discovery/problem-framing",
            "DISCOVER",
            1,
            "approved",
            [],
            "templates/discovery/problem-framing.md",
            "Body one changed.\n",
        ))
        result = artifacts.check_manifest(self.root, manifest)
        changed_ids = [entry["id"] for entry in result["changed"]]
        self.assertEqual(changed_ids, ["demo/discovery/problem-framing"])
        self.assertEqual(result["changed"][0]["current"],
                         artifacts.artifact_revision(block(
                             "demo/discovery/problem-framing",
                             "DISCOVER",
                             1,
                             "approved",
                             [],
                             "templates/discovery/problem-framing.md",
                             "Body one changed.\n",
                             )))
        self.assertEqual(result["reconcile"],
                         ["demo/planning/product-strategy",
                          "demo/planning/vision"])

    def test_check_manifest_changed_status_only_is_no_change(self):
        manifest = artifacts.build_manifest(self.root, 2)
        self._write("demo/discovery/problem-framing.md", block(
            "demo/discovery/problem-framing",
            "DISCOVER",
            1,
            "in-review",
            [],
            "templates/discovery/problem-framing.md",
            "Body one.\n",
        ))
        result = artifacts.check_manifest(self.root, manifest)
        self.assertEqual(result, {"changed": [], "reconcile": []})

    def test_check_manifest_deleted_vision(self):
        manifest = artifacts.build_manifest(self.root, 2)
        (self.root / "demo" / "planning" / "vision.md").unlink()
        result = artifacts.check_manifest(self.root, manifest)
        changed_ids = [entry["id"] for entry in result["changed"]]
        self.assertEqual(changed_ids, ["demo/planning/vision"])
        self.assertIsNone(result["changed"][0]["current"])
        self.assertEqual(result["reconcile"], ["demo/planning/product-strategy"])

    def test_cycle_still_gives_manifest(self):
        self._tmp2 = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp2.cleanup)
        root = Path(self._tmp2.name)
        (root / "alpha").mkdir()
        (root / "beta").mkdir()
        (root / "alpha" / "a.md").write_text(block(
            "alpha",
            "DEFINE",
            2,
            "draft",
            ["beta"],
            "templates/alpha.md",
            "Alpha body.\n",
        ), encoding="utf-8")
        (root / "beta" / "b.md").write_text(block(
            "beta",
            "DEFINE",
            2,
            "draft",
            ["alpha"],
            "templates/beta.md",
            "Beta body.\n",
        ), encoding="utf-8")
        manifest = artifacts.build_manifest(root, 2)
        ids = {entry["id"] for entry in manifest["artifacts"]}
        self.assertEqual(ids, {"alpha", "beta"})
        self.assertEqual(manifest["dependencies"], [])


if __name__ == "__main__":
    unittest.main()
