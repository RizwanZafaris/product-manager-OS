#!/usr/bin/env python3
"""Generator for the executable-surface inventory inside SECURITY.md.

    python3 tools/exec_surface.py            # rewrite the block in SECURITY.md
    python3 tools/exec_surface.py --check    # exit 1 when the committed block is stale

Standard library only, like every other script in this tree.

SECURITY.md used to say "`tools/` holds eighteen scripts in all" and to name
the one that leaves the manual path. Both were typed by hand and both were true
on the day they were typed: the directory held 27 scripts when an external audit
read that sentence, and a second script had grown a network call in the
meantime. A number a reader cannot check is a number nothing re-measures, so the
count and the exceptions are now read from the tree and written between two
markers in SECURITY.md, and `--check` fails the build when the committed block
no longer matches what this script renders.

What it reads and what it does not: each script's source, parsed, for two
facts -- whether it names an environment variable and whether it names a
network primitive. That is a reading of the text, not of a run. A script that
reaches the network through another module is attributed to the module that
spells the call, and a script that merely mentions `os.environ` in a comment is
not counted, because a comment is not parsed. Nothing here says what a script
does with either capability; the prose around the block says that, and the
provider section below it states the credential path in full.

The network half is a fixed recognition list -- the modules, calls and program
names in NETWORK_MODULES, NETWORK_CALLS and NETWORK_BINARIES below -- and the
block prints that list, because the claim it lets the block make is only ever
"this source names nothing on this list". It is not, and the block does not
say, that a script cannot reach the network: a package nobody thought of, a
name assembled at run time, or a module imported through importlib is outside
what a reading of the syntax can see. An earlier version of this file said
"names no network primitive" flatly, and a reviewer walked through it with
`import http.server` and `asyncio.open_connection`.

A module ON the list is read however the source spells it -- `import
http.server`, `from http import server`, `from http.server import HTTPServer`,
or `import http` with `http.server` at the point of use -- because a list that
recognises one spelling and not another says "names nothing on this list" of a
script that names something on it. A second reviewer walked `from http import
server`, `from http import client` and `from xmlrpc import client` past the
version that special-cased urllib alone.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = "SECURITY.md"
TOOLS = "tools"
BEGIN = "<!-- BEGIN GENERATED executable-surface: written by tools/exec_surface.py. Never hand-edit; run `python3 tools/exec_surface.py` and commit the result. -->"
END = "<!-- END GENERATED executable-surface -->"

# An environment read, as the syntax spells it: `os.environ`, `os.getenv`, or
# the same two imported by name. The attribute is matched on any object, so
# `import os as _os` and `_os.environ` counts, which is how tools/model_matrix.py
# spells it; the cost of that breadth is that a `config.environ` would count too,
# and no script in this tree has one.
ENVIRONMENT_ATTRS = frozenset({"environ", "getenv", "environb"})
# A network primitive, by the module it comes from, the call it makes, or the
# program it hands to a subprocess. The list is fixed and closed, and the block
# this script writes says so and prints it, because "no network primitive" is
# only ever a statement about what is on this list: a reviewer defeated the
# first version of it with a script that spelled `import http.server` and
# `asyncio.open_connection`, and the generated sentence then said that script
# named none.
#
# urllib.parse is deliberately absent: it is string handling, and
# tools/workspace.py imports it only to quote and unquote link targets. asyncio
# is absent as a module for the same reason -- a script that uses it to run a
# subprocess reaches nothing -- and is covered by its stream and server
# constructors below instead. "git" is absent from the binaries although `git
# push` calls out: every script here runs it to read the local index, and a
# list that names it would say "yes" of the whole tree and mean nothing.
NETWORK_MODULES = ("urllib.request", "urllib.error", "http.client",
                   "http.server", "http.cookiejar", "socket", "socketserver",
                   "ssl", "ftplib", "smtplib", "smtpd", "imaplib", "poplib",
                   "nntplib", "telnetlib", "xmlrpc.client", "xmlrpc.server",
                   "webbrowser", "requests", "httpx", "aiohttp", "urllib3",
                   "httplib2", "websockets", "websocket", "paramiko", "boto3",
                   "botocore", "grpc", "pycurl")
NETWORK_CALLS = frozenset({"urlopen", "urlretrieve", "create_connection",
                           "open_connection", "start_server", "create_server",
                           "start_unix_server", "getaddrinfo", "gethostbyname",
                           "gethostbyaddr", "create_unix_connection"})
# A program that leaves the machine, named as a string this script hands to
# another process. Only a string that IS the program, standing in a call's
# arguments or in a list or tuple inside them, is read: the word "curl" in a
# docstring is prose, and this is the same posture the environment read takes
# toward a comment.
NETWORK_BINARIES = frozenset({"curl", "wget", "nc", "ncat", "netcat", "ssh",
                              "scp", "sftp", "rsync", "telnet", "ftp",
                              "openssl"})


def scripts(root: Path) -> list[Path]:
    """Every *.py directly under tools/, sorted, sidecars left out.

    A name beginning "._" is an AppleDouble sidecar: this tree is edited from an
    exFAT drive that writes one beside every file, it is not UTF-8, and it is
    not a script. Nothing below tools/ is read, because the directory has no
    sub-packages; a tree with no tools/ returns nothing rather than raising.
    """
    base = root / TOOLS
    if not base.is_dir():
        return []
    return sorted((path for path in base.glob("*.py")
                   if not path.name.startswith("._")),
                  key=lambda path: path.name)


def _dotted(node) -> str:
    """The dotted name an attribute chain spells, or "" when it spells none.

    `http.server.HTTPServer` is read from a chain of ast.Attribute nodes
    standing on an ast.Name, and only such a chain is a module name: `self.x.y`
    and `open(p).read` are rooted somewhere else and return "". Requiring the
    root to be a Name is what keeps the reading narrow -- a `config.socket`
    attribute spells "config.socket", which is on no list, rather than "socket".
    """
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return ""
    parts.append(node.id)
    return ".".join(reversed(parts))


def _names_a_network_module(name: str) -> bool:
    """True when a dotted name IS a module on the list, or sits inside one.

    The list holds dotted module names, and a source can spell the same module
    four ways: `import http.server`, `from http import server`, `from
    http.server import HTTPServer`, and `import http` with `http.server` where
    it is used. All four spell "http.server" once the name is assembled, and
    this is the one place that comparison is made, so the list the block prints
    is the list every spelling is read against. An earlier version compared
    only the two spellings an `import` statement gives and special-cased
    urllib; a reviewer walked `from http import server` straight past it.

    The suffix test is on a dot, so "sslcheck" is not "ssl" and
    "urllib.parse.quote" is not "urllib.request".
    """
    return any(name == module or name.startswith(module + ".")
               for module in NETWORK_MODULES)


def facts(path: Path) -> tuple[bool, bool]:
    """(names an environment variable, names a network primitive), parsed.

    Parsed rather than searched, so this file's own detector constants -- the
    strings "os.environ" and "urlopen" a few lines above -- do not classify this
    file as doing either. A script that does not parse is reported by the
    compile gate long before this one, so a SyntaxError is raised rather than
    swallowed into a false "no".
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    environment = network = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr in ENVIRONMENT_ATTRS:
                environment = True
            # `import http` followed by `http.server.HTTPServer(...)`: the
            # import names only the package, and the module on the list is
            # spelled where it is used.
            if _names_a_network_module(_dotted(node)):
                network = True
        elif isinstance(node, ast.Name) and node.id in ENVIRONMENT_ATTRS:
            environment = True
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if _names_a_network_module(alias.name):
                    network = True
        elif isinstance(node, ast.ImportFrom):
            # A relative import names a module inside this tree, never one on
            # the list, and its `module` is a sibling path rather than a
            # package: `from . import server` is tools/server.py.
            if node.level:
                continue
            module = node.module or ""
            if _names_a_network_module(module):
                network = True
            elif any(_names_a_network_module("%s.%s" % (module, alias.name))
                     for alias in node.names):
                network = True
        elif isinstance(node, ast.Call):
            called = node.func
            name = called.attr if isinstance(called, ast.Attribute) else \
                getattr(called, "id", None)
            if name in NETWORK_CALLS:
                network = True
            elif _hands_over_a_network_binary(node):
                network = True
    return environment, network


def _hands_over_a_network_binary(node: ast.Call) -> bool:
    """True when a call's arguments name a program that leaves the machine.

    Both shapes a subprocess takes: the program as an argument on its own
    (`run("curl", ...)`) and the program as the first word of an argument
    vector (`run(["curl", url])`). Only a string that is exactly the program
    counts, so a message mentioning curl is not read as running it, and the
    call is not required to be `subprocess.*`: a helper that wraps it spells
    the program in the same place.

    What this does not read: a program named inside a set literal, or built
    from pieces at run time. No call in this tree spells one either way, and
    leaving set literals out is also what keeps this file's own list of program
    names, which is a set inside a `frozenset(...)` call, from classifying this
    file as handing one over.
    """
    for argument in list(node.args) + [keyword.value for keyword in node.keywords]:
        items = argument.elts if isinstance(argument, (ast.List, ast.Tuple)) \
            else [argument]
        for item in items:
            if isinstance(item, ast.Constant) and isinstance(item.value, str) \
                    and item.value in NETWORK_BINARIES:
                return True
    return False


def _spelled(names) -> str:
    """A list of names as backticked prose, so the block reads as a sentence."""
    items = ["`%s`" % name for name in names]
    if len(items) < 3:
        return " and ".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def render(root: Path) -> str:
    """The whole generated block, from the tree, as one string."""
    found = [(path.name, facts(path)) for path in scripts(root)]
    named = [(name, flags) for name, flags in found if any(flags)]
    plain = len(found) - len(named)
    lines = [
        "`%s/` holds %d scripts. %d of them read files and print or write a "
        "report: their source names no environment variable, and nothing on "
        "the network list this generator recognises, printed below the table. "
        "The rest are named here."
        % (TOOLS, len(found), plain),
        "",
    ]
    if named:
        lines += ["| Script | Names an environment variable | Names a network primitive |",
                  "|---|---|---|"]
        for name, (environment, network) in named:
            lines.append("| `%s/%s` | %s | %s |"
                         % (TOOLS, name, "yes" if environment else "no",
                            "yes" if network else "no"))
    else:
        lines.append("No script under `%s/` names either." % TOOLS)
    lines += [
        "",
        "Read from each script's syntax, not from a run: a cell says what the "
        "source spells, and a script that reaches either capability through "
        "another module is counted against the module that spells the call.",
        "",
        "The network list this reading recognises, in full: the modules %s; "
        "the calls %s; and these programs handed to a subprocess as a string, "
        "%s. A module on that list counts however the source spells it -- "
        "`import http.server`, `from http import server`, `from http.server "
        "import HTTPServer`, or `import http` with `http.server` where it is "
        "used all name the same module. A name outside the list is not seen, "
        "so \"names no network primitive\" is a statement about this list and "
        "not about what a script can do."
        % (_spelled(NETWORK_MODULES), _spelled(sorted(NETWORK_CALLS)),
           _spelled(sorted(NETWORK_BINARIES))),
    ]
    return "\n".join(lines)


def _bounds(text: str):
    """(index after the BEGIN line, index at the start of the END line), or None."""
    begin = text.find(BEGIN)
    end = text.find(END)
    if begin < 0 or end < 0 or end < begin:
        return None
    after = text.find("\n", begin)
    if after < 0:
        return None
    return after + 1, text.rfind("\n", 0, end) + 1


def replace(text: str, block: str) -> str:
    """SECURITY.md's text with the block between the markers replaced."""
    span = _bounds(text)
    if span is None:
        raise SystemExit("%s does not carry both markers in order. Restore "
                         "them, or run this script against a tree that has "
                         "them." % TARGET)
    start, end = span
    return text[:start] + block + "\n" + text[end:]


def compare(root: Path):
    """(what is wrong with the committed block, the text it should hold).

    The problem is None only when the committed block is exactly what this
    script renders. A missing file or a missing marker is a problem and not a
    pass: deleting the block is otherwise the cheapest way to drop the claim it
    makes, which is the failure this generator exists to prevent. A tree with no
    tools/ makes no claim and is not checked, the same posture the other
    generators take toward fixture roots.
    """
    block = render(root)
    if not scripts(root):
        return None, block
    path = root / TARGET
    if not path.is_file():
        return "%s is missing" % TARGET, block
    text = path.read_text(encoding="utf-8")
    span = _bounds(text)
    if span is None:
        return ("%s no longer carries the executable-surface markers" % TARGET,
                block)
    start, end = span
    if text[start:end].rstrip("\n") != block:
        return ("%s's executable-surface block does not match the tree" % TARGET,
                block)
    return None, block


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="regenerate in memory and fail when the committed "
                             "block in SECURITY.md is stale")
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="repository root (defaults to this script's repo)")
    args = parser.parse_args(argv)
    root = args.root

    if args.check:
        problem, _block = compare(root)
        if problem is not None:
            print("%s. Run: python3 tools/exec_surface.py, then commit the "
                  "result." % problem, file=sys.stderr)
            return 1
        print("%s: ok (executable surface up to date, %d scripts)"
              % (TARGET, len(scripts(root))))
        return 0

    path = root / TARGET
    if not path.is_file():
        print("%s is missing" % TARGET, file=sys.stderr)
        return 1
    # explicit LF: no newline translation, ever
    payload = replace(path.read_text(encoding="utf-8"), render(root))
    path.write_bytes(payload.encode("utf-8"))
    print("%s: executable-surface block written (%d scripts)"
          % (TARGET, len(scripts(root))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
