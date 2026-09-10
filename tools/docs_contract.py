#!/usr/bin/env python3
"""Check operator-document accessibility and evidence-boundary claims."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


KEY_DOCS = ("README.md", "SECURITY.md", "docs/THREAT-MODEL.md",
            "docs/ACCESSIBILITY.md", "docs/ARCHITECTURE.md")
AMBIGUOUS = frozenset({"here", "this", "this link", "link", "more", "read more",
                       "click here", "details"})
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FALSE_LIVE = re.compile(r"(?i)\b(?:100\s*/\s*100|all external gates are green|"
                        r"live sandbox verified|provider certified|regulatory certified|"
                        r"user validated)\b")
REQUIRED_BOUNDARIES = ("local evidence", "external evidence", "does not prove",
                       "live sandbox", "provider", "user", "regulatory")
REQUIRED_PATHS = ("pmos/cli.py", "pmos/domain.py", "pmos/store.py", "pmos/hooks.py",
                  "pmos/openrouter.py")

# The template inventory, which nothing measured. A stale figure survived in
# five files at once because the catalog's per-directory headings were
# self-consistently wrong: they summed to the number the front door claimed, so
# a reader who checked the arithmetic was reassured rather than alerted. The
# only reading that can catch that is a count taken from the tree.
TEMPLATES_DIR = "templates"
CATALOG = "templates/README.md"
# "## discovery (16 templates)": one heading per directory under templates/.
CATALOG_SECTION = re.compile(r"^##\s+([A-Za-z0-9_.-]+)\s+\((\d+)\s+templates?\)\s*$")
# Any count of templates or blanks. Inside the catalog every one of these is
# either a section heading, checked against that directory, or the whole total.
COUNT = re.compile(r"\b(\d+)\s+(?:templates?|blanks?)\b", re.I)
# An inventory claim in an operator document, as opposed to a count of some
# subset of the templates. "all 100 templates" and "all 100 blanks" say the
# figure covers the whole tree; "the 55 templates that name the knowledge
# index" counts something else and is not read here. That is a stated limit:
# a subset figure in these documents is checked by a reader, not by this gate.
INVENTORY = re.compile(r"\ball\s+(\d+)\s+(?:templates?|blanks?)\b", re.I)
# Where the front-door inventory claim lives. CHANGELOG.md is deliberately not
# in this set: it records what was true on the day of an entry, so its older
# figures are correct history and would fail a check against today's tree.
INVENTORY_DOCS = ("README.md", "docs/ARCHITECTURE.md")


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    line: int
    message: str

    def as_dict(self):
        return {"severity": self.severity, "code": self.code, "path": self.path,
                "line": self.line, "message": self.message}


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _local_target(root: Path, source: Path, raw: str) -> bool:
    target = raw.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith("#") or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return True
    target = target.split("#", 1)[0]
    candidate = (source.parent / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    return candidate.exists()


def _template_blanks(root: Path) -> dict:
    """Every blank under templates/, keyed by the directory that holds it.

    templates/README.md is the catalog rather than a blank, so it is not
    counted; anything at the top level of templates/ is in the same position
    and is excluded the same way.
    """
    base = root / TEMPLATES_DIR
    grouped: dict = {}
    for path in sorted(base.rglob("*.md")):
        relative = path.relative_to(base)
        if len(relative.parts) < 2 or relative.name.startswith("._"):
            continue
        grouped.setdefault(relative.parts[0], set()).add(relative.as_posix())
    return grouped


def _catalog_sections(text: str) -> dict:
    """Each catalog section: its line, its declared count, its linked blanks.

    A link that climbs out of templates/ is context the section cites, not a
    row of the catalog, so only targets inside the directory are collected.
    """
    sections: dict = {}
    current = None
    for number, raw in enumerate(text.splitlines(), 1):
        match = CATALOG_SECTION.match(raw)
        if match:
            current = match.group(1)
            sections[current] = [number, int(match.group(2)), set()]
            continue
        if raw.startswith("## "):
            current = None
        if current is None:
            continue
        for link in LINK.finditer(raw):
            target = link.group(2).strip().split("#", 1)[0].strip("<>")
            if target.endswith(".md") and not target.startswith(("../", "/")) \
                    and "://" not in target:
                sections[current][2].add(target)
    return sections


def check_inventory(root: Path) -> list[Issue]:
    """The template count, taken from the tree and compared with what is said.

    Three readings, in order of how far a wrong number travels: the catalog's
    per-directory headings and link tables against the directories themselves,
    every other count in the catalog against the total, and the front-door
    inventory figures against the same total. A tree with no templates/ makes
    no inventory claim and is not checked; this file is run against fixture
    roots as well as this repository.

    What this does not read: a spelled-out number ("Eight directories"), and a
    figure that counts some subset of the templates rather than all of them.
    """
    issues: list[Issue] = []
    if not (root / TEMPLATES_DIR).is_dir():
        return issues
    grouped = _template_blanks(root)
    total = sum(len(names) for names in grouped.values())

    catalog = root / CATALOG
    if not catalog.is_file():
        issues.append(Issue("error", "missing-doc", CATALOG, 1,
                            "the template catalog is missing, so nothing "
                            "states the inventory it is the front door for"))
        return issues
    text = catalog.read_text(encoding="utf-8")
    sections = _catalog_sections(text)

    for name in sorted(set(grouped) - set(sections)):
        issues.append(Issue("error", "inventory-count", CATALOG, 1,
                            "templates/%s holds %d blank(s) and the catalog "
                            "has no section for it" % (name, len(grouped[name]))))
    for name in sorted(set(sections) - set(grouped)):
        issues.append(Issue("error", "inventory-count", CATALOG,
                            sections[name][0],
                            "the catalog has a section for templates/%s, which "
                            "holds no blanks" % name))
    for name in sorted(set(sections) & set(grouped)):
        line, declared, linked = sections[name]
        actual = grouped[name]
        if declared != len(actual):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "the %s section says %d template(s) and the "
                                "directory holds %d"
                                % (name, declared, len(actual))))
        for missing in sorted(actual - linked):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "templates/%s is in the tree and not in the "
                                "catalog" % missing))
        for absent in sorted(linked - actual):
            issues.append(Issue("error", "inventory-count", CATALOG, line,
                                "the catalog lists templates/%s, which is not "
                                "in the tree" % absent))

    for number, raw in enumerate(text.splitlines(), 1):
        if CATALOG_SECTION.match(raw):
            continue
        for match in COUNT.finditer(raw):
            if int(match.group(1)) != total:
                issues.append(Issue("error", "inventory-count", CATALOG, number,
                                    "the catalog says %r and templates/ holds "
                                    "%d blank(s)" % (match.group(0), total)))

    claims = 0
    for name in INVENTORY_DOCS:
        path = root / name
        if not path.is_file():
            continue
        document = path.read_text(encoding="utf-8")
        for match in INVENTORY.finditer(document):
            claims += 1
            if int(match.group(1)) != total:
                issues.append(Issue("error", "inventory-count", name,
                                    _line(document, match.start()),
                                    "this says %r and templates/ holds %d "
                                    "blank(s)" % (match.group(0), total)))
    if not claims:
        issues.append(Issue("error", "inventory-count", INVENTORY_DOCS[0], 1,
                            "no operator document states the template "
                            "inventory. One of %s has to carry it as \"all N "
                            "templates\" or \"all N blanks\", or the figure "
                            "the front door shows a reader is measured by "
                            "nobody" % ", ".join(INVENTORY_DOCS)))
    return issues


def check(root: Path) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    combined = []
    for name in KEY_DOCS:
        path = root / name
        if not path.exists():
            issues.append(Issue("error", "missing-doc", name, 1,
                                "required operator document is missing"))
            continue
        text = path.read_text(encoding="utf-8")
        combined.append(text.lower())
        previous = 0
        for number, raw in enumerate(text.splitlines(), 1):
            heading = HEADING.match(raw)
            if heading:
                level = len(heading.group(1))
                if previous and level > previous + 1:
                    issues.append(Issue("error", "heading-order", name, number,
                                        "heading level jumps from H%d to H%d" % (previous, level)))
                previous = level
        for match in IMAGE.finditer(text):
            if not match.group(1).strip():
                issues.append(Issue("error", "image-alt", name, _line(text, match.start()),
                                    "images need non-empty alternative text"))
        for match in LINK.finditer(text):
            label, target = match.groups()
            line = _line(text, match.start())
            if label.strip().lower() in AMBIGUOUS:
                issues.append(Issue("error", "ambiguous-link", name, line,
                                    "link text must describe its destination"))
            if not _local_target(root, path, target):
                issues.append(Issue("error", "broken-local-link", name, line,
                                    "local link does not resolve inside the repository"))
        for match in FALSE_LIVE.finditer(text):
            issues.append(Issue("error", "overclaim", name, _line(text, match.start()),
                                "operator docs must not claim unverified external evidence"))
    all_text = "\n".join(combined)
    for phrase in REQUIRED_BOUNDARIES:
        if phrase not in all_text:
            issues.append(Issue("error", "evidence-boundary", "docs/THREAT-MODEL.md", 1,
                                "missing explicit boundary: %s" % phrase))
    for name in REQUIRED_PATHS:
        if not (root / name).is_file():
            issues.append(Issue("error", "missing-runtime-path", name, 1,
                                "documented CLI/API runtime path is absent"))
    readme = root / "README.md"
    if readme.exists() and "local evidence is not external evidence" not in readme.read_text(encoding="utf-8").lower():
        issues.append(Issue("warning", "readme-boundary", "README.md", 1,
                            "add: 'Local evidence is not external evidence.'"))
    issues.extend(check_inventory(root))
    return sorted(issues, key=lambda item: (item.severity, item.path, item.line,
                                             item.code, item.message))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    issues = check(args.root)
    if args.json:
        print(json.dumps([issue.as_dict() for issue in issues], sort_keys=True))
    else:
        for issue in issues:
            print("%s:%d: %s %s: %s" % (issue.path, issue.line, issue.severity,
                                           issue.code, issue.message))
        print("docs contract: %d error(s), %d warning(s)" %
              (sum(issue.severity == "error" for issue in issues),
               sum(issue.severity == "warning" for issue in issues)))
    return 1 if any(item.severity == "error" or args.strict for item in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
