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
