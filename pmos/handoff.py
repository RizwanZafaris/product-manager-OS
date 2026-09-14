"""Build a development handoff package from the workspace and the Conductor.

The builder never writes and never claims authenticated approval.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Mapping

from .artifacts import scan

SECTIONS = (
    "1. Problem",
    "2. Vision and strategy",
    "3. Outcomes and success measures",
    "4. Scope and exclusions",
    "5. Requirements and acceptance criteria",
    "6. Evidence and decisions",
    "7. Dependencies",
    "8. Interface and data contracts",
    "9. Unresolved risks and constraints",
)

_SECTION_RE = re.compile(r"^##\s*(\d\.\s+.*)$")
_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\n]+)\)")


def _collect_sections(text: str) -> tuple[dict[str, list[str]], set[str]]:
    by_title = {title: [] for title in SECTIONS}
    seen: set[str] = set()
    current: str | None = None
    for raw in text.splitlines():
        heading = _SECTION_RE.match(raw.strip())
        if heading:
            label = heading.group(1).strip()
            if label in by_title:
                current = label
                seen.add(label)
            else:
                current = None
            continue
        if current is not None:
            by_title[current].append(raw)
    return by_title, seen


def _gap_and_na(lines: list[str]) -> tuple[list[str], list[str]]:
    gaps: list[str] = []
    not_applicable: list[str] = []
    for raw in lines:
        text = raw.lstrip()
        if text.startswith("- "):
            text = text[2:].lstrip()
        if text.startswith("Gap:"):
            gaps.append(text[len("Gap:"):].strip())
        if text.startswith("N/A because"):
            not_applicable.append(text[len("N/A because"):].strip())
    return gaps, not_applicable


def _link_target(value: str) -> str:
    text = value.strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    if " " in text:
        text = text.split(" ", 1)[0]
    return text


def _relative_path(base: Path, target: str, root: Path) -> tuple[str, bool]:
    target = target.split("#", 1)[0]
    candidate = (base / target).resolve()
    root_path = root.resolve()
    relative = os.path.relpath(str(candidate), str(root_path)).replace(os.sep, "/")
    exists = _links_to_real_file_below_root(base, target, root_path, candidate)
    return relative, exists


def _links_to_real_file_below_root(base: Path, target: str, root_path: Path, candidate: Path) -> bool:
    """A link exists only if it names a real, non-symlink file below root_path.

    The walk is lexical: target is normalized against root_path as given,
    never against a resolved form of it, because the workspace root can
    itself sit under a symlink (macOS routes tempfile directories through
    /var -> /private/var). Only components BELOW root_path are subject to
    the symlink ban; root_path itself is never lstat-checked.

    Each surviving component is pushed onto a stack and is_symlink()-checked
    the instant it is pushed, before a later ".." can pop it back off.
    Collapsing ".." first (for example with os.path.normpath) and only then
    checking the final path would let a symlinked directory slip through
    unnoticed: "symdir/../file.md" would collapse straight to "file.md" and
    never reveal that the walk passed through the symlinked "symdir" on the
    way.
    """
    target_path = Path(target)
    if target_path.is_absolute():
        # An absolute target replaces base entirely, mirroring (base / target).
        try:
            components = target_path.relative_to(root_path).parts
        except ValueError:
            return False  # lexically outside the workspace root
        stack: list[str] = []
    else:
        try:
            stack = list(base.relative_to(root_path).parts)
        except ValueError:
            return False  # base itself is outside the workspace root
        components = target_path.parts

    for part in components:
        if part == "..":
            if not stack:
                return False  # a lexical ".." walked above the workspace root
            stack.pop()
            continue
        stack.append(part)
        if root_path.joinpath(*stack).is_symlink():
            return False

    final = root_path.joinpath(*stack)
    if not final.is_file():
        return False
    try:
        return final.resolve() == candidate
    except OSError:
        return False


def _links(lines: list[str], handoff_folder: Path, root: Path,
           by_path: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for line in lines:
        for match in _LINK_RE.finditer(line):
            target = _link_target(match.group(1))
            lower = target.lower()
            if not target or target.startswith("#") or lower.startswith("http:") or \
                    lower.startswith("https:") or lower.startswith("mailto:"):
                continue
            # An absolute link is still a link: it resolves outside the workspace and so counts as broken.
            relative, exists = _relative_path(handoff_folder, target, root)
            info = by_path.get(relative)
            found.append({
                "target": target,
                "path": relative,
                "exists": bool(exists),
                "artifact_id": info["artifact_id"] if info else None,
                "revision": info["revision"] if info else None,
            })
    return found


def _section_status(lines: list[str], links: list[dict[str, Any]]) -> str:
    for raw in lines:
        text = raw.lstrip()
        if text.startswith("- "):
            text = text[2:].lstrip()
        if text.startswith("Gap:"):
            return "gap"
    if any(not item["exists"] for item in links):
        return "broken"
    if links:
        return "linked"
    for raw in lines:
        text = raw.lstrip()
        if text.startswith("- "):
            text = text[2:].lstrip()
        if text.startswith("N/A because"):
            return "not_applicable"
    return "empty"


def build_handoff(conductor, contract: dict[str, Any] | None, root) -> dict[str, Any]:
    state = conductor.state()
    stale = {item["bank_id"] for item in conductor.stale_gates() if "bank_id" in item}
    scanned = scan(root)
    source_revision = conductor.store.head(conductor.product_id).token

    by_path = {
        record["path"]: {"artifact_id": artifact_id, "revision": record["revision"]}
        for artifact_id, record in scanned.items()
    }

    bank_gates: dict[str, int] = {}
    if isinstance(contract, dict):
        for entry in contract.get("banks", ()):
            if not isinstance(entry, dict):
                continue
            bank_id = entry.get("id")
            gate = entry.get("gate")
            if isinstance(bank_id, str) and isinstance(gate, int) and not isinstance(gate, bool):
                bank_gates[bank_id] = gate

    gates_by_number = {gate: bank_id for bank_id, gate in bank_gates.items() if gate in (1, 2, 3)}

    handoff = None
    for artifact_id, record in scanned.items():
        if record["path"] == "development-handoff.md" or record["path"].endswith("/development-handoff.md"):
            handoff = {
                "path": record["path"],
                "artifact_id": artifact_id,
                "revision": record["revision"],
            }
            break
    if handoff is None:
        handoff = None
    root_path = Path(root).resolve()
    handoff_text = ""
    handoff_folder = root_path
    if handoff is not None:
        handoff_text = (root_path / handoff["path"]).read_text(encoding="utf-8")
        folder = os.path.dirname(handoff["path"])
        handoff_folder = (root_path / folder).resolve() if folder else root_path

    rows, present = _collect_sections(handoff_text)
    sections = []
    for title in SECTIONS:
        lines = rows[title]
        is_present = handoff is not None and title in present
        links = _links(lines, handoff_folder, root_path, by_path) if is_present else []
        gaps, not_applicable = _gap_and_na(lines)
        status = "missing" if not is_present else _section_status(lines, links)
        sections.append({
            "title": title,
            "status": status,
            "links": links,
            "gaps": gaps,
            "not_applicable": not_applicable,
        })

    gates = state.get("gates", {})
    approvals = []
    for bank in conductor.banks:
        gate = bank_gates.get(bank.id)
        if gate not in (1, 2, 3):
            continue
        record = gates.get(bank.id, {})
        approved = bank.id in gates
        manifest = record.get("manifest") if isinstance(record, dict) else None
        if isinstance(manifest, dict):
            artifacts_payload = [{"id": item["id"], "revision": item["revision"]} for item in manifest.get("artifacts", [])]
            dependencies_payload = [{"id": item["id"], "revision": item["revision"]} for item in manifest.get("dependencies", [])]
        else:
            artifacts_payload = None
            dependencies_payload = None
        approvals.append({
            "bank_id": bank.id,
            "gate": gate,
            "approved": approved,
            "stale": bank.id in stale,
            "actor_id": record.get("proof", {}).get("actor_id") if approved else None,
            "approved_at": record.get("proof", {}).get("approved_at") if approved else None,
            "attestation": record.get("attestation", "local") if approved else None,
            "artifacts": artifacts_payload,
            "dependencies": dependencies_payload,
            "superseded": len(state.get("superseded_gates", {}).get(bank.id, [])),
        })

    development_ready = True
    missing: list[str] = []
    for gate in (1, 2, 3):
        if gate not in gates_by_number:
            development_ready = False
            missing.append("Contract is missing a bank for gate %d" % gate)

    if handoff is None:
        development_ready = False
        missing.append("development-handoff.md artifact is missing")

    for item in approvals:
        if not item["approved"]:
            development_ready = False
            missing.append("Gate %d is not approved" % item["gate"])
        if item["stale"]:
            development_ready = False
            missing.append("Gate %d approval is stale" % item["gate"])

    for section in sections:
        if section["status"] in {"linked", "not_applicable"}:
            continue
        development_ready = False
        if section["status"] == "broken":
            missing_links = [link["target"] for link in section["links"] if not link["exists"]]
            if missing_links:
                missing.append("Section %s has broken link %s" % (section["title"], missing_links[0]))
            else:
                missing.append("Section %s is broken" % section["title"])
        elif section["status"] == "missing":
            missing.append("Section %s is missing" % section["title"])
        elif section["status"] == "gap":
            missing.append("Section %s has a gap" % section["title"])
        elif section["status"] == "empty":
            missing.append("Section %s is empty" % section["title"])
        else:
            missing.append("Section %s is %s" % (section["title"], section["status"]))

    return {
        "product_id": conductor.product_id,
        "source_revision": source_revision,
        "handoff": handoff,
        "sections": sections,
        "approvals": approvals,
        "development_ready": development_ready,
        "missing": missing,
    }
