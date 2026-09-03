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
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = REPO / "products"
TEMPLATES_DIR = REPO / "templates"

# Every constant and every function below this line used to live here in a
# second copy. They now live in tools/workspace.py, which harness/runner.py
# imports too, so the initializer and the runner can no longer disagree about
# where a filled artifact lands or what its links say once it lands there.
from workspace import (                                   # noqa: E402
    BARE_PATH_RE, FOLDER_FOR_STAGE, FOLDER_FOR_TEMPLATE_DIR, HEADER_LINE_RE,
    LEFT_ALONE, LINK_RE, PRODUCT_SLUG_RE, SPECIAL_DESTINATIONS, STAGE_FOLDERS,
    WorkspaceError, broken_links, declared_stage, destination_for, read_text,
    rewrite_links, rewrite_target, safe_product_slug,
)

SEED_TEMPLATE = "templates/execution/state.md"


# The initializer's own name for the shared error, so every raise and every
# except in this file still reads as it did and a caller catching either one
# catches both.
InitError = WorkspaceError


def say(*parts):
    print(" ".join(str(p) for p in parts))


def repo_relative(path):
    """A path inside the repository as a posix repo-relative string."""
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(REPO):
        raise InitError("%s sits outside the repository. This tool only copies "
                        "templates that ship with the tree." % path)
    return resolved.relative_to(REPO).as_posix()


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


def add_template(slug, template, force=False, quiet=False):
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

    if not quiet:
        say("copied:", template_rel, "->", dest_rel)
        say("  ", "%d link(s) rewritten, %d relative link(s) re-resolved from "
            "the destination and found"
            % (len(rewrites), relative_links(rewritten)))
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


def every_shipped_template():
    """Every template this tool can place, as repo-relative paths.

    Everything under templates/, plus the byte-exact regulated import, which
    lives outside templates/ and is routed to by check-regulatory-gaps. A
    template the manifest can send a run to and this tool cannot place is a
    hole in the workspace contract, so the two lists are kept the same shape.
    """
    found = sorted(p.relative_to(REPO).as_posix()
                   for p in (TEMPLATES_DIR).rglob("*.md") if p.is_file())
    for extra in sorted(SPECIAL_DESTINATIONS):
        if extra not in found and (REPO / extra).is_file():
            found.append(extra)
    return found


def relink_workspace(slug, quiet=False):
    """Repoint every link in a workspace at the workspace's own copies.

    The drift this closes. A link is rewritten when its file is copied, and at
    that moment it can only prefer a workspace copy that already exists. Copy
    the discovery document before the personas it links to and the link lands
    on the blank template in templates/, which resolves, reports as fine, and
    is the wrong file: it points a reader at the empty form instead of at the
    work. Measured on a workspace with all templates installed: 99 links
    across 41 files still aimed at templates/.

    So placement is not the last word. This pass runs with every copy already
    present and asks each link the same question again. It is idempotent, and
    running it twice changes nothing the first run did not.
    """
    workspace = PRODUCTS_DIR / slug
    if not workspace.is_dir():
        raise InitError("products/%s/ does not exist. Create it first: "
                        "python3 tools/init_product.py %s" % (slug, slug))
    moved, touched = 0, 0
    for path in sorted(p for p in workspace.rglob("*.md") if p.is_file()):
        text = read_text(path)
        here = posixpath.dirname(path.relative_to(REPO).as_posix())
        rewritten, rewrites, _skipped = rewrite_links(text, here, here, slug)
        if rewrites:
            path.write_text(rewritten, encoding="utf-8")
            moved += len(rewrites)
            touched += 1
            if not quiet:
                say("  relinked %s (%d link(s) now point at this workspace)"
                    % (path.relative_to(REPO).as_posix(), len(rewrites)))
    say("relink: %d link(s) across %d file(s) repointed at products/%s/."
        % (moved, touched, slug))
    return moved


def add_every_template(slug, force=False):
    """Install every shipped template, then settle the links between them."""
    installed, skipped = 0, 0
    for template in every_shipped_template():
        destination = REPO / destination_for(template, slug,
                                             read_text(REPO / template))
        if destination.exists() and not force:
            skipped += 1
            continue
        add_template(slug, REPO / template, force=force, quiet=True)
        installed += 1
    say("installed %d template(s), left %d already-present file(s) alone."
        % (installed, skipped))
    # Second pass, with every copy present. Without it the links between them
    # point at the blank templates rather than at each other.
    relink_workspace(slug, quiet=True)
    return installed


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
    parser.add_argument("--add-all", action="store_true",
                        help="copy every shipped template into the workspace, "
                             "then repoint the links between them at this "
                             "workspace's own copies")
    parser.add_argument("--relink", action="store_true",
                        help="repoint every link in an existing workspace at "
                             "this workspace's own copies, where one exists. "
                             "Idempotent; copies nothing")
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
        if args.relink:
            relink_workspace(slug)
        elif args.add_all:
            if not (PRODUCTS_DIR / slug).is_dir():
                create_workspace(slug, force=args.force)
            add_every_template(slug, force=args.force)
        elif args.add:
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
