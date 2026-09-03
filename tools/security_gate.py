#!/usr/bin/env python3
"""Deterministic, standard-library security gate for the PM OS source tree.

This is a source/configuration gate, not a penetration test or an attestation
about a provider.  It fails on committed credential-shaped values and unsafe
execution primitives, and makes the dependency and threat-model boundaries
machine-checkable.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = frozenset({".py", ".json", ".toml", ".yaml", ".yml", ".ini",
                           ".cfg", ".md", ".txt", ".sh"})
SOURCE_SUFFIXES = frozenset({".py"})
SECRET_PATTERNS = (
    ("openrouter", re.compile(r"\bsk-or-v1-[A-Za-z0-9_-]{20,}\b")),
    ("openai", re.compile(r"\bsk-(?!or-v1-)[A-Za-z0-9_-]{20,}\b")),
    ("anthropic", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("github", re.compile(r"\bgh[pous]_[A-Za-z0-9_]{20,}\b")),
    ("aws", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
ASSIGNMENT_SECRET = re.compile(
    r"(?i)\b(?:openrouter|api[_-]?key|secret|token|password)\b\s*[:=]\s*"
    r"[\"']?(?=[A-Za-z0-9_+/=-]{24,}[\"']?)(?=[A-Za-z0-9_+/=-]*\d)"
    r"[A-Za-z0-9_+/=-]{24,}[\"']?")
REQUIRED_THREAT_TERMS = (
    "local evidence", "external evidence", "does not prove", "sandbox",
    "provider", "user", "regulatory", "dependency surface", "exception inventory",
)


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    message: str

    def as_dict(self):
        return {"code": self.code, "path": self.path, "line": self.line,
                "message": self.message}


def _tracked(root: Path) -> list[Path]:
    """Return committed paths plus unstaged candidates; fixtures are walked safely.

    The committed set is authoritative for a release.  Including non-ignored
    candidates makes the same gate useful before ``git add`` and prevents a
    credential from becoming invisible merely because it is new.
    """
    try:
        done = subprocess.run(["git", "ls-files", "-z", "--cached", "--others",
                               "--exclude-standard"], cwd=root,
                              shell=False, capture_output=True, check=True)
        names = [part for part in done.stdout.decode("utf-8").split("\0") if part]
        return [root / name for name in names if (root / name).is_file()]
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError):
        return [path for path in root.rglob("*")
                if path.is_file() and ".git" not in path.parts]


class _UnsafeAst(ast.NodeVisitor):
    """Conservatively resolve local imports and aliases before rejecting calls.

    This is intentionally a small, intraprocedural resolver, not an attempt to
    execute or fully model Python.  When a call reaches a dangerous module via
    an import alias, an assignment alias, or a literal ``getattr`` dispatch,
    the gate treats it exactly as its spelling.  For ``shell=`` the only
    accepted spelling is the literal ``False``; a value that could be truthy
    must be reviewed rather than guessed safe by static analysis.
    """

    _EXECUTION = frozenset({"builtins.eval", "builtins.exec", "os.system", "os.popen"})
    _PICKLE_PREFIX = "pickle."
    _SUBPROCESS = frozenset({
        "subprocess.run", "subprocess.Popen", "subprocess.call",
        "subprocess.check_call", "subprocess.check_output",
    })
    _GETATTR = frozenset({"getattr", "builtins.getattr"})
    _DYNAMIC_MODULES = frozenset({"builtins", "os", "subprocess", "pickle"})

    def __init__(self, path: Path):
        self.path = path
        self.findings: list[Finding] = []
        self._finding_keys: set[tuple[str, int, str]] = set()
        # A name can have more than one possible target after a conditional
        # assignment.  Retain every possible target and reject if *any* one is
        # a forbidden primitive; choosing the final syntactic assignment would
        # let a branch-only safe overwrite hide a dangerous alias.
        self._scopes: list[dict[str, frozenset[str]]] = [{}]

    def _add(self, code: str, node: ast.AST, message: str) -> None:
        line = getattr(node, "lineno", 1)
        key = (code, line, message)
        if key not in self._finding_keys:
            self._finding_keys.add(key)
            self.findings.append(Finding(code, self.path.as_posix(), line, message))

    def _lookup(self, name: str) -> frozenset[str]:
        bound = self._bound(name)
        if bound:
            return bound
        if name in {"eval", "exec", "getattr", "vars", "__import__"}:
            return frozenset({"builtins." + name})
        if name == "__builtins__":
            return frozenset({"builtins"})
        return frozenset({name})

    def _bound(self, name: str) -> frozenset[str]:
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return frozenset()

    def _bind(self, name: str, values: Iterable[str] | str | None) -> None:
        if values is None:
            self._scopes[-1].pop(name, None)
            return
        if isinstance(values, str):
            values = (values,)
        resolved = frozenset(value for value in values if isinstance(value, str) and value)
        if resolved:
            self._scopes[-1][name] = resolved
        else:
            self._scopes[-1].pop(name, None)

    def _callable_names(self, node: ast.AST) -> frozenset[str]:
        if isinstance(node, ast.Name):
            return self._lookup(node.id)
        if isinstance(node, ast.Attribute):
            candidates = frozenset(head + "." + node.attr
                                   for head in self._callable_names(node.value) if head)
            bound = frozenset(target for candidate in candidates
                              for target in self._bound(candidate))
            return bound or candidates
        if isinstance(node, ast.Call):
            targets = self._literal_getattr_targets(node) | self._literal_import_targets(node)
            if self._callable_names(node.func) & {"builtins.vars"} and node.args:
                targets |= frozenset(base + ".__dict__"
                                     for base in self._callable_names(node.args[0])
                                     if base in self._DYNAMIC_MODULES)
            return targets
        if isinstance(node, ast.Subscript):
            key = self._literal_string(node.slice)
            bases = self._subscript_bases(node.value)
            if key is None:
                return frozenset(base + ".__dynamic_subscript__" for base in bases)
            return frozenset(base + "." + key for base in bases)
        if isinstance(node, ast.IfExp):
            return self._callable_names(node.body) | self._callable_names(node.orelse)
        return frozenset()

    @staticmethod
    def _literal_string(node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return None

    def _literal_getattr_targets(self, node: ast.Call) -> frozenset[str]:
        if not (self._callable_names(node.func) & self._GETATTR) or len(node.args) < 2:
            return frozenset()
        attribute = self._literal_string(node.args[1])
        if attribute is None:
            return frozenset()
        return frozenset(base + "." + attribute
                         for base in self._callable_names(node.args[0]) if base)

    def _literal_import_targets(self, node: ast.Call) -> frozenset[str]:
        """Resolve only the literal dynamic-import form that Python exposes."""
        if not (self._callable_names(node.func) & {"builtins.__import__"}) or not node.args:
            return frozenset()
        module = self._literal_string(node.args[0])
        if module in self._DYNAMIC_MODULES:
            return frozenset({module})
        return frozenset()

    def _dynamic_getattr_bases(self, node: ast.Call) -> frozenset[str]:
        if not (self._callable_names(node.func) & self._GETATTR) or len(node.args) < 2:
            return frozenset()
        if self._literal_string(node.args[1]) is not None:
            return frozenset()
        return self._callable_names(node.args[0]) & self._DYNAMIC_MODULES

    def _subscript_bases(self, node: ast.AST) -> frozenset[str]:
        """Return dynamic module mappings reached through __dict__ or vars()."""
        bases = set(self._callable_names(node))
        if isinstance(node, ast.Call) and self._callable_names(node.func) & {"builtins.vars"} \
                and node.args:
            bases.update(self._callable_names(node.args[0]))
        normalized = set()
        for base in bases:
            if base.endswith(".__dict__"):
                base = base[:-len(".__dict__")]
            if base in self._DYNAMIC_MODULES:
                normalized.add(base)
        return frozenset(normalized)

    def _dynamic_subscript_bases(self, node: ast.AST) -> frozenset[str]:
        if not isinstance(node, ast.Subscript):
            return frozenset()
        return self._subscript_bases(node.value)

    def _set_assignment_aliases(self, targets: Iterable[ast.expr], value: ast.AST) -> None:
        for target in targets:
            self._set_target_alias(target, value)

    def _set_target_alias(self, target: ast.expr, value: ast.AST) -> None:
        if isinstance(target, ast.Name):
            self._bind(target.id, self._callable_names(value) or None)
            return
        if isinstance(target, ast.Attribute):
            # Resolve the value but keep the syntactic attribute name as the
            # binding key.  Resolving ``Launcher.run`` here would yield its
            # previous target and let a conditional rebind mutate that target
            # instead of merging the attribute's possible values.
            for name in self._attribute_target_names(target):
                self._bind(name, self._callable_names(value) or None)
            return
        if isinstance(target, (ast.Tuple, ast.List)):
            values = value.elts if isinstance(value, (ast.Tuple, ast.List)) else ()
            for index, member in enumerate(target.elts):
                self._set_target_alias(member, values[index] if index < len(values) else ast.Constant(None))

    def _attribute_target_names(self, target: ast.Attribute) -> frozenset[str]:
        return frozenset(head + "." + target.attr
                         for head in self._callable_names(target.value) if head)

    def _copy_scope(self) -> dict[str, frozenset[str]]:
        return dict(self._scopes[-1])

    @staticmethod
    def _merge_scopes(*scopes: dict[str, frozenset[str]]) -> dict[str, frozenset[str]]:
        merged: dict[str, set[str]] = {}
        for scope in scopes:
            for name, values in scope.items():
                merged.setdefault(name, set()).update(values)
        return {name: frozenset(values) for name, values in merged.items()}

    def _visit_branch(self, statements: Iterable[ast.stmt], base: dict[str, frozenset[str]]) \
            -> dict[str, frozenset[str]]:
        self._scopes[-1] = dict(base)
        for statement in statements:
            self.visit(statement)
        return self._copy_scope()

    def _enter_scope(self) -> None:
        self._scopes.append({})

    def _leave_scope(self) -> None:
        self._scopes.pop()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            local = alias.asname or alias.name.split(".", 1)[0]
            resolved = alias.name if alias.asname else alias.name.split(".", 1)[0]
            self._bind(local, resolved)
            if alias.name == "pickle" or alias.name.startswith("pickle."):
                self._add("unsafe-pickle", node, "pickle is forbidden in runtime code")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "pickle" or (node.module or "").startswith("pickle."):
            self._add("unsafe-pickle", node, "pickle is forbidden in runtime code")
        module = node.module or ""
        for alias in node.names:
            if alias.name == "*":
                if module in self._DYNAMIC_MODULES:
                    self._add("unsafe-dynamic-import", node,
                              "star import from a dynamic runtime module is forbidden")
                continue
            self._bind(alias.asname or alias.name,
                       (module + "." + alias.name) if module else alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.generic_visit(node)
        self._set_assignment_aliases(node.targets, node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.generic_visit(node)
        if node.value is not None:
            self._set_assignment_aliases((node.target,), node.value)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.generic_visit(node)
        self._set_assignment_aliases((node.target,), node.value)

    def visit_If(self, node: ast.If) -> None:
        # Both arms are possible at a later call site.  Visit them against the
        # same pre-branch aliases and retain the union, rather than allowing a
        # branch-local reassignment to erase a dangerous outer alias.
        self.visit(node.test)
        base = self._copy_scope()
        body = self._visit_branch(node.body, base)
        otherwise = self._visit_branch(node.orelse, base)
        self._scopes[-1] = self._merge_scopes(body, otherwise)

    def _visit_loop(self, node: ast.For | ast.AsyncFor | ast.While) -> None:
        if isinstance(node, (ast.For, ast.AsyncFor)):
            self.visit(node.iter)
            loop_target = node.target
        else:
            self.visit(node.test)
            loop_target = None
        base = self._copy_scope()
        self._scopes[-1] = dict(base)
        if loop_target is not None:
            self._set_assignment_aliases((loop_target,), ast.Constant(None))
        for statement in node.body:
            self.visit(statement)
        body = self._copy_scope()
        # A loop can execute zero times, so the pre-loop aliases remain live.
        outcomes = self._merge_scopes(base, body)
        if node.orelse:
            outcomes = self._merge_scopes(outcomes, self._visit_branch(node.orelse, outcomes))
        self._scopes[-1] = outcomes

    def visit_For(self, node: ast.For) -> None:
        self._visit_loop(node)

    visit_AsyncFor = visit_For

    def visit_While(self, node: ast.While) -> None:
        self._visit_loop(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.visit(node.subject)
        base = self._copy_scope()
        outcomes = [base]
        for case in node.cases:
            self._scopes[-1] = dict(base)
            if case.guard is not None:
                self.visit(case.guard)
            outcomes.append(self._visit_branch(case.body, self._copy_scope()))
        self._scopes[-1] = self._merge_scopes(*outcomes)

    def visit_Try(self, node: ast.Try) -> None:
        # An exception can choose any handler or skip directly to ``finally``;
        # retain all resulting aliases.  This is intentionally conservative.
        base = self._copy_scope()
        outcomes = [self._visit_branch(node.body, base)]
        outcomes.extend(self._visit_branch(handler.body, base) for handler in node.handlers)
        if node.orelse:
            outcomes.append(self._visit_branch(node.orelse, outcomes[0]))
        merged = self._merge_scopes(*outcomes)
        if node.finalbody:
            merged = self._visit_branch(node.finalbody, merged)
        self._scopes[-1] = merged

    def visit_Subscript(self, node: ast.Subscript) -> None:
        # Module dictionaries and vars(module) are mutable dispatch tables.
        # Even a literal key is not a safe execution boundary, so reject the
        # dispatch itself before an alias can conceal it in a later statement.
        for base in self._dynamic_subscript_bases(node):
            self._add("unsafe-dynamic-dispatch", node,
                      "subscript dispatch from %s is forbidden" % base)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # A function name overwrites a same-scope alias, while the body gets
        # an independent local-alias map. Decorators/defaults use outer names.
        self._bind(node.name, None)
        for decorator in node.decorator_list:
            self.visit(decorator)
        for default in (*node.args.defaults, *(item for item in node.args.kw_defaults if item is not None)):
            self.visit(default)
        self._enter_scope()
        self.visit(node.args)
        for statement in node.body:
            self.visit(statement)
        self._leave_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # Capture aliases declared in a class body under the class-qualified
        # attribute name, so ``class X: run = subprocess.run; X.run(...)``
        # cannot evade the resolver.
        self._bind(node.name, None)
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)
        self._enter_scope()
        for statement in node.body:
            self.visit(statement)
        attributes = self._copy_scope()
        self._leave_scope()
        for attribute, values in attributes.items():
            self._bind(node.name + "." + attribute, values)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self._enter_scope()
        self.visit(node.args)
        self.visit(node.body)
        self._leave_scope()

    def visit_Call(self, node: ast.Call) -> None:
        names = self._callable_names(node.func)
        # Flag a dynamic lookup at creation time as well as an immediately
        # invoked lookup, so ``fn = getattr(builtins, name); fn(...)`` cannot
        # lose the finding between statements.
        dynamic_bases = self._dynamic_getattr_bases(node)
        if isinstance(node.func, ast.Call):
            dynamic_bases |= self._dynamic_getattr_bases(node.func)
        dynamic_bases |= self._dynamic_subscript_bases(node.func)
        for dynamic_base in dynamic_bases:
            self._add("unsafe-dynamic-dispatch", node,
                      "dynamic dispatch from %s is forbidden" % dynamic_base)
        for name in names:
            if name in self._EXECUTION:
                self._add("unsafe-execution", node, "%s is forbidden" % name)
            if name.startswith(self._PICKLE_PREFIX):
                self._add("unsafe-pickle", node, "pickle deserialization is forbidden")
            if name in self._SUBPROCESS:
                self._check_subprocess_shell(node, name)
        if names & {"open", "Path.write_text", "Path.write_bytes", "Path.unlink",
                    "os.remove", "os.unlink", "shutil.rmtree"}:
            for argument in node.args[:1]:
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str) \
                        and ".." in Path(argument.value).parts:
                    self._add("path-escape", node,
                              "literal path traversal must be rejected before I/O")
        self.generic_visit(node)

    @staticmethod
    def _literal_false(node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and node.value is False

    def _check_subprocess_shell(self, node: ast.Call, name: str) -> None:
        """Enforce literal ``shell=False`` across normal, expanded, and Popen calls."""
        for keyword in node.keywords:
            if keyword.arg == "shell":
                if not self._literal_false(keyword.value):
                    self._add("unsafe-shell", node,
                              "subprocess shell must be the literal False")
                continue
            if keyword.arg is None:
                if not isinstance(keyword.value, ast.Dict):
                    self._add("unsafe-shell", node,
                              "expanded subprocess keyword arguments cannot prove shell is False")
                    continue
                for key, value in zip(keyword.value.keys, keyword.value.values):
                    if self._literal_string(key) == "shell" and not self._literal_false(value):
                        self._add("unsafe-shell", node,
                                  "subprocess shell must be the literal False")
                    elif self._literal_string(key) is None:
                        self._add("unsafe-shell", node,
                                  "expanded subprocess keyword arguments cannot prove shell is False")
        if name != "subprocess.Popen":
            return
        # Popen's positional shell parameter is index 8.  A starred argument
        # can shift into that slot, so it is rejected rather than inferred.
        if any(isinstance(argument, ast.Starred) for argument in node.args):
            self._add("unsafe-shell", node,
                      "starred Popen arguments cannot prove shell is False")
        elif len(node.args) > 8 and not self._literal_false(node.args[8]):
            self._add("unsafe-shell", node,
                      "subprocess shell must be the literal False")


def _dependency_findings(root: Path, paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        findings.append(Finding("dependency-surface", "pyproject.toml", 1,
                                "a package manifest is required"))
    else:
        text = pyproject.read_text(encoding="utf-8")
        if "dependencies" not in text:
            findings.append(Finding("dependency-surface", "pyproject.toml", 1,
                                    "project dependencies must be explicit"))
    forbidden = {"requirements.txt", "requirements-dev.txt", "Pipfile.lock",
                 "poetry.lock", "uv.lock"}
    names = {path.relative_to(root).as_posix() for path in paths}
    for name in sorted(forbidden & names):
        findings.append(Finding("dependency-surface", name, 1,
                                "unreviewed dependency lock/surface is not allowed"))
    threat = root / "docs" / "THREAT-MODEL.md"
    if not threat.exists():
        findings.append(Finding("threat-model", "docs/THREAT-MODEL.md", 1,
                                "threat model is required"))
    else:
        words = threat.read_text(encoding="utf-8").lower()
        for term in REQUIRED_THREAT_TERMS:
            if term not in words:
                findings.append(Finding("threat-model", "docs/THREAT-MODEL.md", 1,
                                        "missing required boundary: %s" % term))
    return findings


def scan(root: Path) -> list[Finding]:
    root = root.resolve()
    paths = _tracked(root)
    findings: list[Finding] = []
    for path in paths:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("undecodable-source", rel, 1,
                                    "text source/config must decode as UTF-8"))
            continue
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(Finding("committed-secret", rel, line,
                                        "credential-shaped %s value" % label))
        for match in ASSIGNMENT_SECRET.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(Finding("committed-secret", rel, line,
                                    "credential-shaped assignment"))
        if path.suffix in SOURCE_SUFFIXES and not path.name.startswith("test_"):
            try:
                tree = ast.parse(text, filename=rel)
            except SyntaxError as exc:
                findings.append(Finding("syntax", rel, exc.lineno or 1,
                                        "cannot safely inspect Python source"))
            else:
                visitor = _UnsafeAst(Path(rel))
                visitor.visit(tree)
                findings.extend(visitor.findings)
    findings.extend(_dependency_findings(root, paths))
    return sorted(findings, key=lambda item: (item.path, item.line, item.code,
                                               item.message))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings = scan(args.root)
    if args.json:
        print(json.dumps([item.as_dict() for item in findings], sort_keys=True))
    else:
        for item in findings:
            print("%s:%d: %s: %s" % (item.path, item.line, item.code, item.message))
        print("security gate: %d finding(s)" % len(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
