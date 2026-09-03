#!/usr/bin/env python3
"""Where a filled artifact lands, and what its links say once it lands there.

Standard library only, like every other script in this tree.

The defect this closes. Two callers wrote a template into a product workspace
and each one answered "where does this go" on its own. `tools/init_product.py`
read the mapping `os/PRODUCT-WORKSPACE.md` states in prose. `harness/runner.py`
re-derived it from the template's parent folder name. The two agreed on most
files and disagreed on thirteen, and the disagreements were the expensive kind:
the runner filed `templates/execution/state.md` at `execution/state.md` while
the workspace's STATE lives at `STATE.md`, so a run could create a second state
file and a later resume could read the wrong one. Every `templates/ai/` file
landed a folder too high, outside the DEFINE stage that produced it. A copy
placed by the runner also kept the blank template's relative links, which are
computed from `templates/`, so they pointed at paths that do not exist from the
workspace.

The rule now is that neither caller decides. This module decides, both import
it, and a disagreement between them is a failing test rather than a field
report. `os/PRODUCT-WORKSPACE.md` remains the prose statement of the same
mapping; the tables below are that document in executable form.

What lives here: the product slug rule, the template-to-workspace destination
map, and the link rewriter that makes a copy's relative links resolve from
where the copy actually sits. What does not: anything about calling a model,
which is the runner's business alone, and anything about the CLI, which each
caller keeps.
"""

from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = REPO / "products"
TEMPLATES_DIR = REPO / "templates"
STATE_TEMPLATE = TEMPLATES_DIR / "execution" / "state.md"


class WorkspaceError(Exception):
    """A condition the operator has to fix. Printed without a traceback."""


# A product is a name, not a location. One segment of letters, digits,
# underscore and hyphen, because a slug pasted straight into a path lets
# "../../../../private/tmp/x" resolve outside the repository entirely. Both
# callers used to carry their own copy of this rule with a comment saying it
# was copied from the other; now there is one.
PRODUCT_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

# The same link pattern the repository gate reads. Not a copy of it: the copy
# was the defect. lint.py's pattern understands an angle-bracket destination
# and a link title, and this module's did not, so `](<a b.md>)` was a link the
# gate judged and the rewriter never saw. A workspace could pass
# `init_product --check` and fail `lint --workspace` on the same file.
#
# Imported rather than restated, so the two cannot drift again. tools/ may not
# import harness/, which is deletable; lint.py sits at the root and is not.
sys.path.insert(0, str(REPO))
import lint as _lint                                       # noqa: E402

LINK_RE = _lint.LINK_RE

# A destination written inside angle brackets, which is how a target with a
# space in it is spelled. The brackets are not part of the path.
ANGLE_RE = re.compile(r"\A<(.*)>\Z", re.S)


def unwrap_target(raw):
    """One captured destination, as (path, was_in_angle_brackets)."""
    match = ANGLE_RE.match(raw or "")
    return (match.group(1), True) if match else (raw or "", False)


def wrap_target(target, was_angled):
    """A destination, re-spelled the way it has to be written to parse.

    Angle brackets go back on when they were there, and go on for the first
    time when a rewrite introduces a space. Dropping them would produce a link
    that no longer parses, which is a worse outcome than the one being fixed.
    """
    return ("<%s>" % target
            if was_angled or " " in target or "(" in target or ")" in target
            else target)

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
STAGE_FIELD_RE = re.compile(r"^stage:\s*(.+?)\s*$", re.M)

# Ten templates write the Stage/Knowledge/Skill header as a bare path rather
# than a markdown link. The repository gate does not read those, because it
# only looks between ]( and ), but a reader follows them and a copy breaks them
# exactly the same way. So they are rewritten and verified too, on the three
# header lines only, where the convention is fixed.
HEADER_LINE_RE = re.compile(r"^(?:Stage|Knowledge|Skill):")
BARE_PATH_RE = re.compile(r"(?<![\w`(/.])((?:\.\./)+[A-Za-z0-9._/-]+)")

LEFT_ALONE = ("http://", "https://", "mailto:", "#")

# The workspace layout, in the order os/PRODUCT-WORKSPACE.md lists it.
STAGE_FOLDERS = ("planning", "discovery", "definition", "definition/ai",
                 "architecture", "execution", "delivery", "operate", "gates")

# One template folder, one workspace folder. This is the mapping
# os/PRODUCT-WORKSPACE.md states in prose.
FOLDER_FOR_TEMPLATE_DIR = {
    "planning": "planning",
    "discovery": "discovery",
    "definition": "definition",
    "ai": "definition/ai",
    "architecture": "architecture",
    "execution": "execution",
    "delivery": "delivery",
    "operate": "operate",
}

# The fallback, for a template that lives outside templates/ and so has no
# folder to read. DESIGN produces architecture; BUILD and ALL STAGES produce
# the continuously written files in execution.
FOLDER_FOR_STAGE = {
    "PLANNING": "planning",
    "DISCOVER": "discovery",
    "DEFINE": "definition",
    "AI OVERLAY": "definition/ai",
    "DESIGN": "architecture",
    "BUILD": "execution",
    "ALL STAGES": "execution",
    "DELIVER": "delivery",
    "OPERATE": "operate",
}

# The files whose filled copy does not keep its template folder.
#
# state.md is the workspace's own memory and every skill, prompt and adapter
# addresses it as STATE.md at the root, so that is where it lands.
#
# The regulated AI PRD is a byte-exact import with a pinned hash, which means
# it cannot be given the frontmatter the fallback above reads. Its route is
# check-regulatory-gaps, at DEFINE and Gate 2, and it is an AI PRD, so its
# copy belongs with the rest of the AI overlay. Naming it here rather than
# editing the template is what keeps the hash pin honest.
SPECIAL_DESTINATIONS = {
    "templates/execution/state.md": "STATE.md",
    "modules/regulated/templates/regulated-ai-prd-template.md":
        "definition/ai/regulated-ai-prd.md",
}


def safe_product_slug(value):
    """One product slug, or a refusal."""
    raw = str(value or "")
    text = raw.strip()
    if not text:
        raise WorkspaceError("the product slug is empty. Give the name of a "
                             "workspace under products/, for example "
                             "ledgerline.")
    if text in (".", "..") or ".." in text or text.startswith("."):
        raise WorkspaceError("slug %r contains a dot segment. It is a name, "
                             "not a path." % raw)
    if "/" in text or "\\" in text or Path(text).is_absolute():
        raise WorkspaceError("slug %r contains a path separator. Pass one "
                             "slug, for example ledgerline, and it resolves "
                             "under products/." % raw)
    if not PRODUCT_SLUG_RE.match(text):
        raise WorkspaceError("slug %r is not usable. Use letters, digits, "
                             "underscore and hyphen, starting with a letter "
                             "or a digit, up to 64 characters." % raw)
    root = PRODUCTS_DIR.resolve()
    resolved = (PRODUCTS_DIR / text).resolve()
    if resolved.parent != root:
        raise WorkspaceError("slug %r resolves to %s, which is not directly "
                             "under products/." % (raw, resolved))
    return text


def product_dir(product):
    """The workspace directory for one product slug."""
    return PRODUCTS_DIR / safe_product_slug(product)


def declared_stage(text):
    """The stage a file's frontmatter declares, uppercased, or None."""
    match = FRONTMATTER_RE.match(text or "")
    if not match:
        return None
    field = STAGE_FIELD_RE.search(match.group(1))
    return field.group(1).strip().strip('"').upper() if field else None


def destination_for(template_rel, slug, text=None):
    """Where one template's filled copy belongs, as a repo-relative path.

    The single answer to "where does this go". Ask it with the template's own
    text where you have it, because the fallback for a template outside
    templates/ reads the stage out of that text.
    """
    template_rel = str(template_rel).replace("\\", "/")
    if template_rel in SPECIAL_DESTINATIONS:
        return "products/%s/%s" % (slug, SPECIAL_DESTINATIONS[template_rel])
    parts = template_rel.split("/")
    name = parts[-1]
    if parts[0] == "templates" and len(parts) >= 3:
        folder = FOLDER_FOR_TEMPLATE_DIR.get(parts[1])
        if folder:
            return "products/%s/%s/%s" % (slug, folder, name)
    stage = declared_stage(text or "")
    folder = FOLDER_FOR_STAGE.get(stage or "")
    if not folder:
        raise WorkspaceError(
            "%s is not under a templates/ folder this tool knows, and its "
            "frontmatter declares stage %r, which maps to no workspace "
            "folder. Give it a stage, or name its destination in "
            "SPECIAL_DESTINATIONS in tools/workspace.py."
            % (template_rel, stage))
    return "products/%s/%s/%s" % (slug, folder, name)


def destination_path(template, slug, text=None):
    """destination_for as an absolute Path, from a Path or a repo-relative str.

    The form the runner wants: it holds resolved Paths, not repo-relative
    strings, and it must not answer this question its own way.
    """
    template = Path(template)
    try:
        relative = template.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        raise WorkspaceError(
            "%s is outside this repository, so no workspace destination can "
            "be computed for it." % template)
    if text is None:
        try:
            text = template.read_text(encoding="utf-8")
        except OSError:
            text = ""
    return REPO / destination_for(relative, safe_product_slug(slug), text)


def rewrite_target(target, source_dir, dest_dir, slug):
    """One link target, recomputed for the destination.

    The rule, in one sentence: resolve the link against the template it was
    written in, then express that same file relative to where the copy lands,
    and prefer the workspace's own filled copy when one already exists. The
    depth is computed from the two real paths, never assumed, which is why a
    file in products/x/discovery/ gets ../../../ and STATE.md at the workspace
    root gets ../../ from the identical template text.
    """
    resolved = posixpath.normpath(posixpath.join(source_dir, target))
    if resolved.startswith(".."):
        return None, "climbs out of the repository"
    if not (REPO / resolved).exists():
        return None, "does not resolve from the template either"
    if resolved.startswith("templates/") or resolved in SPECIAL_DESTINATIONS:
        try:
            local = destination_for(resolved, slug,
                                    read_text(REPO / resolved))
        except WorkspaceError:
            local = None
        if local and (REPO / local).exists():
            resolved = local
    return posixpath.relpath(resolved, dest_dir), None


def rewrite_links(text, source_dir, dest_dir, slug):
    """The file's text with every relative link recomputed. Returns notes."""
    rewrites = []
    skipped = []

    def replace(match):
        captured = match.group(1)
        inner, angled = unwrap_target(captured)
        target, _, fragment = inner.partition("#")
        if not target or inner.startswith(LEFT_ALONE):
            return match.group(0)
        if target.startswith("/"):
            skipped.append((inner, "is an absolute path"))
            return match.group(0)
        new_target, why = rewrite_target(target, source_dir, dest_dir, slug)
        if new_target is None:
            skipped.append((inner, why))
            return match.group(0)
        rebuilt = new_target + ("#" + fragment if fragment else "")
        if rebuilt != inner:
            rewrites.append((inner, rebuilt))
        # Any title the link carried is dropped with the rest of match.group(0)
        # and re-emitted below, so a rewritten link keeps only what it needs to
        # resolve. Titles are rare in this tree and none is load bearing.
        return "](%s)" % wrap_target(rebuilt, angled)

    def replace_bare(match):
        target = match.group(1)
        new_target, why = rewrite_target(target, source_dir, dest_dir, slug)
        if new_target is None:
            skipped.append((target, why))
            return target
        if new_target != target:
            rewrites.append((target, new_target))
        return new_target

    out = []
    for line in LINK_RE.sub(replace, text).splitlines(True):
        stripped = line.rstrip("\r\n")
        ending = line[len(stripped):]
        if HEADER_LINE_RE.match(stripped):
            stripped = BARE_PATH_RE.sub(replace_bare, stripped)
        out.append(stripped + ending)
    return "".join(out), rewrites, skipped


def relocate(text, template, destination, slug):
    """One template's text, with its links recomputed for where it lands.

    The whole rewrite in one call, for a caller that holds two absolute paths
    and does not want to think about posix directory arithmetic. Both callers
    use this, which is why a copy the runner writes and a copy the initializer
    writes now carry identical links.
    """
    template = Path(template)
    destination = Path(destination)
    source_dir = posixpath.dirname(
        template.resolve().relative_to(REPO.resolve()).as_posix())
    dest_dir = posixpath.dirname(
        destination.resolve().relative_to(REPO.resolve()).as_posix())
    return rewrite_links(text, source_dir, dest_dir, slug)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def broken_links(path):
    """Every relative link in one file that does not resolve, as (line, raw).

    This is the verification step, and it is deliberately dumb: it does not
    trust the rewrite, it re-reads the written file and asks the filesystem
    whether each target is there. A copy tool that produces broken links is the
    defect rather than the fix, so nothing is reported as copied until this
    returns empty.
    """
    path = Path(path)
    broken = []
    for number, line in enumerate(read_text(path).splitlines(), 1):
        targets = [unwrap_target(m.group(1))[0]
                   for m in LINK_RE.finditer(line)]
        if HEADER_LINE_RE.match(line):
            targets += [m.group(1) for m in BARE_PATH_RE.finditer(line)]
        for raw in targets:
            target = raw.split("#")[0]
            if not target or raw.startswith(LEFT_ALONE) \
                    or target.startswith("/"):
                continue
            if not (path.parent / target).exists():
                broken.append((number, raw))
    return broken
