#!/usr/bin/env python3
"""Create a product workspace and copy templates into it with working links.

    python3 tools/init_product.py my-product
    python3 tools/init_product.py my-product --add templates/discovery/personas.md
    python3 tools/init_product.py my-product --check

Standard library only, like every other script in this tree.

The defect this fixes. A template carries links computed from where the blank
lives. `templates/discovery/discovery-document.md` reaches the knowledge layer
as `../../knowledge/torres-continuous-discovery.md`, which is correct from
`templates/discovery/`. Copy that file by hand into
`products/my-product/discovery/` and the same text now points at
`products/knowledge/...`, which has never existed. Measured before this tool
was written: that one copy broke all four of its relative links, and the tree
holds 317 `../../` links across 88 templates waiting to break the same way.

So a copy is not a copy. Every relative link is recomputed from the real depth
of the destination, and then re-resolved from the destination and checked to
exist. A copy tool that produces broken links is the defect, not the fix, so a
failed check refuses the copy and says which link failed.

Where a copy lands. `os/PRODUCT-WORKSPACE.md` defines each workspace folder as
the filled copies of one template folder, so the template's own folder decides
the destination: `templates/discovery/` to `discovery/`, `templates/ai/` to
`definition/ai/` (the overlay attached at DEFINE, so it lives inside the stage
that produced it). A template from outside `templates/` falls back to the stage
named in its frontmatter. `templates/execution/state.md` is the one file with a
destination of its own: `STATE.md` at the workspace root.

Limits, stated rather than hidden. Links are found with the same pattern the
repository gate uses, so a link written with a title or a space in the target is
not seen by either. A link that is already broken in the template is copied
through untouched and reported, because rewriting it would invent a target.
Anchors, absolute URLs and mailto: targets are left exactly as written. And a
link to a sibling template resolves to the workspace copy once that copy exists
and to the blank template until then, so the order you add templates in changes
which of the two a link points at. Both resolve; only one is your own work.
"""

import argparse
import posixpath
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = REPO / "products"
TEMPLATES_DIR = REPO / "templates"

# The slug rule, copied from harness/runner.py's safe_product_slug so that a
# workspace this tool creates is one the runner will agree to open. A product
# is a name, not a location.
PRODUCT_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

# The same link pattern the repository gate reads, so this tool rewrites
# exactly the set of links the gate later judges.
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
STAGE_FIELD_RE = re.compile(r"^stage:\s*(.+?)\s*$", re.M)

# Ten templates write the Stage/Knowledge/Skill header as a bare path rather
# than a markdown link. The repository gate does not read those, because it
# only looks between ]( and ), but a reader follows them and a copy breaks them
# exactly the same way. So they are rewritten and verified here too, on the
# three header lines only, where the convention is fixed.
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

# The one template whose filled copy does not keep its template folder.
SPECIAL_DESTINATIONS = {"templates/execution/state.md": "STATE.md"}

SEED_TEMPLATE = "templates/execution/state.md"


class InitError(Exception):
    """A condition the operator has to fix. Printed without a traceback."""


def say(*parts):
    print(" ".join(str(p) for p in parts))


def safe_product_slug(value):
    """One product slug, or a refusal.

    The rule is harness/runner.py's, reused rather than restated: a slug pasted
    straight into a path lets "../../../../private/tmp/x" resolve outside the
    repository entirely. One segment of letters, digits, underscore and hyphen,
    and the resolved directory has to sit directly under products/.
    """
    raw = str(value or "")
    text = raw.strip()
    if not text:
        raise InitError("the product slug is empty. Give the name of a "
                        "workspace under products/, for example ledgerline.")
    if text in (".", "..") or ".." in text or text.startswith("."):
        raise InitError("slug %r contains a dot segment. It is a name, not a "
                        "path." % raw)
    if "/" in text or "\\" in text or Path(text).is_absolute():
        raise InitError("slug %r contains a path separator. Pass one slug, for "
                        "example ledgerline, and this tool resolves it under "
                        "products/." % raw)
    if not PRODUCT_SLUG_RE.match(text):
        raise InitError("slug %r is not usable. Use letters, digits, "
                        "underscore and hyphen, starting with a letter or a "
                        "digit, up to 64 characters." % raw)
    root = PRODUCTS_DIR.resolve()
    resolved = (PRODUCTS_DIR / text).resolve()
    if resolved.parent != root:
        raise InitError("slug %r resolves to %s, which is not directly under "
                        "products/. Refusing." % (raw, resolved))
    return text


def repo_relative(path):
    """A path inside the repository as a posix repo-relative string."""
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(REPO):
        raise InitError("%s sits outside the repository. This tool only copies "
                        "templates that ship with the tree." % path)
    return resolved.relative_to(REPO).as_posix()


def declared_stage(text):
    """The stage a file's frontmatter declares, uppercased, or None."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    field = STAGE_FIELD_RE.search(match.group(1))
    return field.group(1).strip().strip('"').upper() if field else None


def destination_for(template_rel, slug, text=None):
    """Where one template's filled copy belongs, as a repo-relative path."""
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
        raise InitError("%s is not under a templates/ folder this tool knows, "
                        "and its frontmatter declares stage %r, which maps to "
                        "no workspace folder. Copy it by hand and say where it "
                        "belongs." % (template_rel, stage))
    return "products/%s/%s/%s" % (slug, folder, name)


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
    if resolved.startswith("templates/"):
        try:
            local = destination_for(resolved, slug,
                                    read_text(REPO / resolved))
        except InitError:
            local = None
        if local and (REPO / local).exists():
            resolved = local
    return posixpath.relpath(resolved, dest_dir), None


def rewrite_links(text, source_dir, dest_dir, slug):
    """The file's text with every relative link recomputed. Returns notes."""
    rewrites = []
    skipped = []

    def replace(match):
        raw = match.group(1)
        target, _, fragment = raw.partition("#")
        if not target or raw.startswith(LEFT_ALONE):
            return match.group(0)
        if target.startswith("/"):
            skipped.append((raw, "is an absolute path"))
            return match.group(0)
        new_target, why = rewrite_target(target, source_dir, dest_dir, slug)
        if new_target is None:
            skipped.append((raw, why))
            return match.group(0)
        rebuilt = new_target + ("#" + fragment if fragment else "")
        if rebuilt != raw:
            rewrites.append((raw, rebuilt))
        return "](%s)" % rebuilt

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


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def broken_links(path):
    """Every relative link in one file that does not resolve. As tuples.

    This is the verification step, and it is deliberately dumb: it does not
    trust the rewrite, it re-reads the written file and asks the filesystem
    whether each target is there. A copy tool that produces broken links is the
    defect rather than the fix, so nothing is reported as copied until this
    returns empty.
    """
    broken = []
    for number, line in enumerate(read_text(path).splitlines(), 1):
        targets = [m.group(1) for m in LINK_RE.finditer(line)]
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


def create_workspace(slug, force=False):
    """The folders, then the STATE.md seed. Returns the workspace path."""
    workspace = PRODUCTS_DIR / slug
    existed = workspace.is_dir()
    for folder in STAGE_FOLDERS:
        (workspace / folder).mkdir(parents=True, exist_ok=True)
    say("workspace:", "products/%s/" % slug,
        "(already present, folders confirmed)" if existed else "(created)")
    for folder in STAGE_FOLDERS:
        say("  ", folder + "/")
    add_template(slug, REPO / SEED_TEMPLATE, force=force)
    return workspace


def add_template(slug, template, force=False):
    """Copy one template into its workspace folder with rewritten links."""
    template = Path(template)
    if not template.is_absolute():
        template = REPO / template
    if not template.is_file():
        raise InitError("%s does not exist, so there is nothing to copy."
                        % template)
    if template.suffix != ".md":
        raise InitError("%s is not a markdown template." % template)
    template_rel = repo_relative(template)
    text = read_text(template)
    dest_rel = destination_for(template_rel, slug, text)
    dest = REPO / dest_rel
    if dest.exists() and not force:
        raise InitError("%s already exists. Refusing to overwrite your filled "
                        "copy: pass --force if you truly mean to replace it, "
                        "and expect to lose what is in it." % dest_rel)

    source_dir = posixpath.dirname(template_rel)
    dest_dir = posixpath.dirname(dest_rel)
    rewritten, rewrites, skipped = rewrite_links(text, source_dir, dest_dir,
                                                 slug)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(rewritten, encoding="utf-8")

    failures = broken_links(dest)
    if failures:
        dest.unlink()
        lines = ", ".join("line %d: %s" % pair for pair in failures)
        raise InitError("the copy of %s produced %d link(s) that do not "
                        "resolve from %s (%s). The copy was removed rather "
                        "than left broken, which is the whole point of this "
                        "tool." % (template_rel, len(failures), dest_dir,
                                   lines))

    say("copied:", template_rel, "->", dest_rel)
    say("  ", "%d link(s) rewritten, %d relative link(s) re-resolved from the "
        "destination and found" % (len(rewrites), relative_links(rewritten)))
    for old, new in rewrites:
        say("    ", old, "->", new)
    for raw, why in skipped:
        say("    ", "left as written:", raw, "(%s)" % why)
    return dest


def relative_links(text):
    """How many links in one file's text are the kind this tool verifies."""
    total = 0
    for line in text.splitlines():
        targets = [m.group(1) for m in LINK_RE.finditer(line)]
        if HEADER_LINE_RE.match(line):
            targets += [m.group(1) for m in BARE_PATH_RE.finditer(line)]
        for raw in targets:
            if raw and not raw.startswith(LEFT_ALONE) \
                    and not raw.split("#")[0].startswith("/"):
                total += 1
    return total


def check_workspace(slug):
    """Re-resolve every link in an existing workspace. Returns a count."""
    workspace = PRODUCTS_DIR / slug
    if not workspace.is_dir():
        raise InitError("products/%s/ does not exist. Create it first: "
                        "python3 tools/init_product.py %s" % (slug, slug))
    files = sorted(p for p in workspace.rglob("*.md") if p.is_file())
    if not files:
        say("products/%s/: no markdown files yet, so nothing to check." % slug)
        return 0
    total = 0
    for path in files:
        failures = broken_links(path)
        rel = path.relative_to(REPO).as_posix()
        if failures:
            for number, raw in failures:
                say("%s:%d: link %s does not resolve." % (rel, number, raw))
            total += len(failures)
        else:
            say("%s: ok" % rel)
    say("products/%s/: %d file(s), %d broken link(s)."
        % (slug, len(files), total))
    return total


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("slug", help="the product name, one segment, for "
                                     "example ledgerline")
    parser.add_argument("--add", metavar="TEMPLATE",
                        help="copy one template into its stage folder and "
                             "rewrite its links for the destination")
    parser.add_argument("--check", action="store_true",
                        help="re-resolve every link in an existing workspace "
                             "and copy nothing")
    parser.add_argument("--force", action="store_true",
                        help="overwrite a file that is already there. It is "
                             "your filled copy that is lost")
    args = parser.parse_args(argv)

    try:
        slug = safe_product_slug(args.slug)
        if args.check:
            if args.add:
                raise InitError("--check reads a workspace and --add writes to "
                                "one. Run them separately.")
            return 1 if check_workspace(slug) else 0
        if args.add:
            add_template(slug, args.add, force=args.force)
        else:
            create_workspace(slug, force=args.force)
            say("next: write products/%s/README.md, one paragraph plus the "
                "stage and gate table in os/PRODUCT-WORKSPACE.md, then add "
                "the templates this product needs with --add." % slug)
    except InitError as error:
        print("init_product: %s" % error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
