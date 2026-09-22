#!/usr/bin/env python3
"""Score every template against the flagship bar, derived from prd.md.

    python3 tools/template_rubric.py
    python3 tools/template_rubric.py --json docs/readiness/template-rubric.json
    python3 tools/template_rubric.py --min 70          # gate mode: fail below
    python3 tools/template_rubric.py --backpointers    # gate mode: see backpointers()

Standard library only, like every other script in this tree.

Why this exists. "Every template should be as good as the PRD" is a real
instruction and an unmeasurable one, so this file turns it into a score a
command produces. The bar is not invented here: it is read off
templates/definition/prd.md, which is the document the rest of the tree is
being held to, and every dimension below is something that document does and
the median template does not.

What flagship is NOT. It is not length. A decision log is legitimately shorter
than a PRD and padding it would make it worse, so nothing here rewards lines
for their own sake. Depth is scored against the template's own section count,
which is a measure of whether each section was actually written out or merely
named.

The seven dimensions, and what each one catches:

1. self-explaining   Every section carries guidance, in a comment or a visible
                     block, saying what goes in it and what a bad answer
                     looks like. The PRD has one per section. A template
                     whose sections are bare headings is a form, and a form
                     teaches nobody.
2. worked example    At least one filled example, marked ILLUSTRATIVE so it can
                     never be mistaken for real evidence. Without one, the
                     first user invents the format and the second disagrees.
3. exit gate         Names the gate it feeds and what must be true to pass. A
                     document that does not know where it goes cannot be
                     checked by anyone downstream.
4. fillable          Has fill-in fields. A template with none is prose.
5. structured        Uses a table wherever it enumerates, because a list of
                     rows with no columns is where owners and dates go missing.
6. traceable         Links or ID-references sibling artifacts. The stack works
                     only if a criterion can name the story it verifies.
7. failure-aware     Names the trap, the failure mode, or what a bad answer
                     looks like. This is the dimension that separates this
                     tree's templates from a generic template pack, and it is
                     the one most often missing.

Alongside the seven scored dimensions, every report also carries an eighth,
informational number: hidden_guidance_share, the fraction of a template's
words that sit inside an HTML comment, invisible in every renderer
docs/RENDERING.md documents (F17). It does not enter WEIGHTS and it does not
move the score: a template can score well and still hide all its guidance,
and the PRD's own migration to a visible <details> convention is what this
number exists to track across the rest of the tree. See hidden_guidance()
below.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "templates"
REFERENCE = TEMPLATES / "definition" / "prd.md"

H2_RE = re.compile(r"^##\s+\S", re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# The visible form of a guidance block, matched whole so it can be stripped
# the same way COMMENT_RE strips the hidden form, below. Anchored to the
# exact convention docs/RENDERING.md documents (open by default, "Guidance"
# as the fixed summary), not to any <details> tag: a template's own worked
# example is free to use <details> for something else without losing points
# here, or gaining them the way the bug below explains.
#
# Without this, migrating a section's guidance from a comment to this form
# moved its score: the opening tags "<details open>" and "<summary>" each
# happen to match FIELD_RE's <angle-bracket> branch, so a template with few
# genuine fields (below the ten that saturate "fillable") could score higher
# for the same content purely because its guidance became visible HTML
# rather than a hidden comment, and a real link inside the guidance prose
# would start counting toward "traceable" the same way. Guidance prose was
# never meant to count toward the fillable-spine dimensions in either form.
GUIDANCE_BLOCK_RE = re.compile(
    r"<details open>\n<summary>Guidance</summary>\n\n.*?\n\n</details>", re.S)
TABLE_ROW_RE = re.compile(r"^\|", re.M)
# A fill-in field, in either convention this tree sanctions. lint.py accepts
# both [square] and <angle> fields, and the first version of this rubric
# counted only the first, so a template written entirely in angle fields
# scored near zero on fillable. It also counted the visible text of a markdown
# link as a field, because [knowledge index](...) matches a bare square
# pattern. Both errors are corrected here: a square field is one NOT followed
# by an opening parenthesis, and angle fields count too.
FIELD_RE = re.compile(r"\[[a-z][^\]]{2,}\](?!\()|<[A-Za-z0-9][^<>]{2,}>")
LINK_RE = re.compile(r"\]\(\s*(?:<[^<>\n]*>|[^\s()]*)")
# Two conventions exist in this tree for marking a filled example, and the
# first version of this rubric recognised only one. That produced false
# negatives: dependency-register.md carries a fully worked row and says "the
# example row shows the precision expected", and was scored as having no
# example at all. Measured across the tree: 46 files use the ILLUSTRATIVE
# convention, 14 use different wording, 38 genuinely have none. Recognising
# both is the honest instrument; making the tree use one of them is a separate
# and worthwhile fix.
ILLUSTRATIVE_RE = re.compile(
    r"illustrative|worked (micro-)?example|the example row|example row shows"
    r"|delete (?:it|the example|this row)|sample row", re.I)
# A third gap sits beside the two ILLUSTRATIVE_RE already closed above, and F21
# is what surfaced it: the tree also has a convention where the worked example
# is not inside the template at all, but a separate filled document under
# examples/, and the template links to it. ILLUSTRATIVE_RE cannot see that,
# because there is nothing illustrative-shaped in the template's own text to
# match; 39 templates carried a real completed example this way and scored as
# having none, which is the false negative F21 asked this file to fix rather
# than paper over with padding. EXAMPLE_LINK_RE and worked_example_link() below
# recognise it: a Markdown link that resolves to a file under examples/, whose
# own first five lines name this template's repo path back, the same
# convention every examples/*.md file opens with ("Fills
# [templates/...](../templates/...)."). A link to some other template's
# example, or to a file that is not there, earns nothing, on purpose: the
# credit is for a real, checkable, completed exercise, not for a link that
# merely looks like one.
EXAMPLE_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
# How many opening lines of an examples/ file are searched for the template's
# path. One constant, because two readers depend on agreeing about it:
# linked_examples() checks a link against this window, and backpointer_rows()
# lists every file a link could point at by the same window. A wider listing
# would offer files the check then refuses; a narrower one would hide files it
# accepts.
NAMES_BACK_WITHIN = 5


def _opening(path):
    """A file's first NAMES_BACK_WITHIN lines, or None when it is unreadable."""
    try:
        head = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    return "\n".join(head.splitlines()[:NAMES_BACK_WITHIN])


def linked_examples(path, text):
    """Every examples/ file `text` links to whose opening names this template.

    `path` must already be the resolved, absolute path score_template() reads,
    so a relative link can be resolved against its directory the way a reader
    (or lint.py's own link gate) would resolve it.
    """
    try:
        repo_relative = path.relative_to(REPO).as_posix()
    except ValueError:
        return []
    examples_root = (REPO / "examples").resolve()
    found = []
    for match in EXAMPLE_LINK_RE.finditer(text):
        target = match.group(1).strip().strip("<>").split("#", 1)[0].strip()
        if not target or "://" in target:
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(examples_root)
        except ValueError:
            continue
        if not candidate.is_file():
            continue
        opening = _opening(candidate)
        if opening is not None and repo_relative in opening:
            found.append(candidate)
    return found


def worked_example_link(path, text):
    """True when `text` links to an examples/ file that names this template."""
    return bool(linked_examples(path, text))


EXIT_GATE_RE = re.compile(r"^##\s*Exit gate", re.M | re.I)
# The vocabulary this tree uses when it tells you how a thing goes wrong.
FAILURE_RE = re.compile(
    r"\btrap\b|\bfails?\b|failure mode|bad answer|goes wrong|how it lies|"
    r"skip it when|do not\b|never\b|is not a\b|red flag|smell\b",
    re.I)

# Files under templates/ that this rubric must not be applied to, each with the
# reason written out. An exemption list is a place dishonesty hides, so three
# rules bind it: it is short, every entry says why in a sentence a reader can
# disagree with, and exempt files are reported in their own block with their
# score still visible rather than dropped from the output.
#
# Being short is not a reason. Nothing here scores length, so a small template
# is simply a small template. Being weak is not a reason either. The only
# reason that qualifies is that the document is not a fill-in template at all,
# and applying the dimensions below would make the file worse while making its
# number better.
EXEMPT = {
    "templates/execution/state.md":
        "Not a fill-in template. It is the Conductor's memory protocol, and "
        "its binding rules are stated once in a preamble because they govern "
        "the whole file rather than any section of it. Scoring it on "
        "per-section guidance would reward breaking one set of rules into "
        "seven partial restatements, which is how a protocol stops being "
        "readable as one.",
}

# Templates allowed to have no verified back-pointer, each with a one-line
# reason. --backpointers fails unless the templates with none are exactly these
# rather than holding a floor on how many have one: a floor of 107 still passes
# when a 109th template lands with no pointer, because the count it floors does
# not move, and this list turns that into a failure naming the file. The
# equality runs the other way too, so an entry fails once its template links a
# filled example. It also fails once any examples/ file names the template
# back, because the one reason an entry may give is that there is nothing to
# link. Scoring is a separate question: EXEMPT above takes
# templates/execution/state.md out of the statistics, and that template still
# needs its pointer here.
BACKPOINTER_EXCEPTIONS = {
    "templates/definition/assumptions-register.md":
        "No file under examples/ names it back in its first five lines, which "
        "is what this gate counts as a filled example: other examples mention it "
        "and examples/example-brd.md carries a labelled excerpt of it inside a "
        "BRD, but none is a filled copy of it.",
}

WEIGHTS = {
    "self_explaining": 25,
    "failure_aware": 20,
    "worked_example": 15,
    "exit_gate": 15,
    "structured": 10,
    "traceable": 10,
    "fillable": 5,
}

# The visible form docs/RENDERING.md documents as the convention: a
# collapsible block whose summary is the fixed word "Guidance", open by
# default. A section carrying this counts as explaining itself exactly like a
# section carrying an HTML comment does; only hidden_guidance() below cares
# which of the two forms a template actually used.
VISIBLE_GUIDANCE_MARKER = "<summary>Guidance</summary>"


def sections_with_guidance(text):
    """How many h2 sections are followed by guidance before the next.

    Measured per section rather than by counting guidance anywhere, because a
    template can carry one long preamble and leave twelve sections
    unexplained, and that is the shape this dimension exists to catch.

    Guidance counts whether it is still hidden in an HTML comment, the form
    every template but the PRD uses while F17's migration is deferred for
    them, or already visible in the <details>/<summary>Guidance</summary>
    convention the PRD migrated to. Which form a section uses does not change
    whether it explains itself; hidden_guidance() is the number that tracks
    the form.
    """
    parts = re.split(r"(?m)^##\s+", text)
    if len(parts) < 2:
        return 0, 0
    bodies = parts[1:]
    explained = sum(1 for body in bodies
                    if "<!--" in body or VISIBLE_GUIDANCE_MARKER in body)
    return explained, len(bodies)


def hidden_guidance(text):
    """(hidden words, total words, hidden share) for one template.

    F17's own evidence was a hand count: the PRD held 3,111 whitespace-
    separated words and about 1,555 of them sat inside HTML comments, which
    every renderer docs/RENDERING.md documents hides in reading mode. This is
    that same count, mechanized so every template carries the number rather
    than only the one an audit happened to read by hand: whitespace-separated
    words inside <!-- --> spans, divided by whitespace-separated words in the
    whole file.

    Purely informational, like the module docstring says. It is not one of
    the seven WEIGHTS dimensions and does not move score: folding it in would
    make a migration that only changes where guidance sits also move a number
    that is supposed to measure something else.
    """
    total = len(text.split())
    if not total:
        return 0, 0, 0.0
    hidden = sum(len(m.group(0).split()) for m in COMMENT_RE.finditer(text))
    return hidden, total, round(hidden / total, 3)


def score_template(path):
    # Accept a relative path from the command line as well as an absolute one.
    path = Path(path)
    if not path.is_absolute():
        path = (REPO / path).resolve()
    text = path.read_text(encoding="utf-8")
    stripped = GUIDANCE_BLOCK_RE.sub("", COMMENT_RE.sub("", text))
    explained, total_sections = sections_with_guidance(text)
    hidden_words, total_words, hidden_share = hidden_guidance(text)
    lines = len(text.splitlines())

    marks = {}
    # 1. Every section explains itself.
    marks["self_explaining"] = (explained / total_sections) if total_sections else 0.0
    # 2. A worked example: either inline and marked so it cannot be mistaken
    #    for evidence (ILLUSTRATIVE_RE), or a link to a real, completed one
    #    living under examples/ (worked_example_link, see the comment above
    #    EXAMPLE_LINK_RE for why this second form is credited).
    marks["worked_example"] = 1.0 if (ILLUSTRATIVE_RE.search(text)
                                      or worked_example_link(path, text)) else 0.0
    # 3. An exit gate that names where the output goes.
    marks["exit_gate"] = 1.0 if EXIT_GATE_RE.search(text) else 0.0
    # 4. Fields to fill. Saturates quickly: ten is plenty to prove the point.
    fields = len(FIELD_RE.findall(stripped))
    marks["fillable"] = min(fields / 10.0, 1.0)
    # 5. Tables where it enumerates. Six rows is a real table.
    rows = len(TABLE_ROW_RE.findall(stripped))
    marks["structured"] = min(rows / 6.0, 1.0)
    # 6. References its siblings. Four links is a document wired into a stack.
    links = len(LINK_RE.findall(stripped))
    marks["traceable"] = min(links / 4.0, 1.0)
    # 7. Says how it goes wrong. Scaled per section, because one warning in a
    #    sixteen-section document is not a failure-aware document.
    warnings = len(FAILURE_RE.findall(text))
    marks["failure_aware"] = min(warnings / max(total_sections, 4), 1.0)

    score = sum(WEIGHTS[k] * v for k, v in marks.items())
    return {
        "path": path.relative_to(REPO).as_posix(),
        "lines": lines,
        "sections": total_sections,
        "sections_explained": explained,
        "fields": fields,
        "table_rows": rows,
        "links": links,
        "warnings": warnings,
        "marks": {k: round(v, 3) for k, v in marks.items()},
        "score": round(score, 1),
        # Informational only, from here down: never read by the WEIGHTS sum
        # above, so a change in hidden_guidance_share never moves "score".
        "total_words": total_words,
        "hidden_guidance_words": hidden_words,
        "hidden_guidance_share": hidden_share,
    }


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def template_paths():
    """Every file this module reads as a template: templates/**/*.md but the
    catalog. The scoring run and the back-pointer gate both call this, so the
    two cannot disagree about which files are templates."""
    return sorted(p for p in TEMPLATES.rglob("*.md") if p.name != "README.md")


def backpointer_rows():
    """One row per template: the examples it links, and every one it could.

    "linked" is what linked_examples() verifies, so a template whose list is
    empty has no verified back-pointer. "candidates" is every file under
    examples/ whose opening names the template, which is every file a link
    could point at and be verified. Two or more candidates make the link a
    choice this module can check and cannot judge: any of them passes, and
    whether the linked one is the right example is a reviewer's call.
    """
    examples_root = (REPO / "examples").resolve()
    # Everything under examples/, not only .md files, because a link to any
    # file there is verified the same way. What cannot be read as text, a
    # directory included, has no opening and drops out.
    openings = []
    for candidate in sorted(examples_root.rglob("*")):
        opening = _opening(candidate)
        if opening is not None:
            openings.append((candidate, opening))

    def shown(example):
        return "examples/" + example.relative_to(examples_root).as_posix()

    rows = []
    for path in template_paths():
        rel = path.relative_to(REPO).as_posix()
        linked = linked_examples(path, path.read_text(encoding="utf-8"))
        rows.append({
            "path": rel,
            "linked": [shown(example) for example in linked],
            "candidates": [shown(example) for example, opening in openings
                           if rel in opening],
        })
    return rows


def backpointers():
    """Gate mode: exit 1 unless the unpointed templates are exactly the list.

    A template is unpointed when linked_examples() verifies none of its links.
    The unpointed set has to equal BACKPOINTER_EXCEPTIONS, and every entry has
    to give a one-line reason and still have no filled example to link. Every
    template that more than one example names back is printed with all of
    them, on a passing run as well, because passing says nothing about whether
    the linked example is the right one.
    """
    rows = backpointer_rows()
    by_path = {row["path"]: row for row in rows}
    unpointed = [row for row in rows if not row["linked"]]
    unexcused = [row for row in unpointed
                 if row["path"] not in BACKPOINTER_EXCEPTIONS]
    stale = []
    for rel, reason in sorted(BACKPOINTER_EXCEPTIONS.items()):
        row = by_path.get(rel)
        if row is None:
            stale.append("%s is not a template in this tree" % rel)
        elif row["linked"]:
            stale.append("%s has a verified back-pointer to %s"
                         % (rel, ", ".join(row["linked"])))
        elif row["candidates"]:
            stale.append("%s is named back by %s, so it has a filled example "
                         "to link" % (rel, ", ".join(row["candidates"])))
        if len(reason.strip().splitlines()) != 1:
            stale.append("%s has no one-line reason" % rel)
    choices = [row for row in rows if len(row["candidates"]) > 1]

    print("template back-pointers, verified the way worked_example_link() "
          "verifies one")
    print("  templates read                  : %d" % len(rows))
    print("  with a verified back-pointer    : %d" % (len(rows) - len(unpointed)))
    print("  without one                     : %d" % len(unpointed))
    print("  named back by more than one file: %d (%d of them link none)"
          % (len(choices), sum(1 for row in choices if not row["linked"])))
    print("")
    print("named back by more than one file under examples/. Any of them "
          "passes this gate, so which one a template should link is a "
          "reviewer's call, not this check's (* marks a linked file):")
    for row in choices:
        print("  " + row["path"])
        for candidate in row["candidates"]:
            print("    %s %s" % ("*" if candidate in row["linked"] else " ",
                                 candidate))
    print("")
    print("without a verified back-pointer. Each needs a link to a file under "
          "examples/ whose first %d lines name it, or an entry on the "
          "exception list with a one-line reason:" % NAMES_BACK_WITHIN)
    for row in unpointed:
        reason = BACKPOINTER_EXCEPTIONS.get(row["path"])
        print("  %s  %s" % (row["path"], "NOT ON THE EXCEPTION LIST"
                            if reason is None else "on the exception list"))
        for line in _wrap(reason or "", 66):
            print("      " + line)
        for candidate in row["candidates"]:
            print("      could link " + candidate)
    if stale:
        print("")
        print("exception list entries that no longer hold:")
        for problem in stale:
            print("  " + problem)
    print("")
    if unexcused or stale:
        print("back-pointer gate failed: %d template(s) without a verified "
              "back-pointer are not on the exception list, and %d exception "
              "list problem(s)." % (len(unexcused), len(stale)))
        return 1
    print("the %d template(s) without a verified back-pointer are exactly the "
          "exception list." % len(unpointed))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", metavar="PATH",
                        help="write the machine-readable report here")
    parser.add_argument("--min", type=float,
                        help="exit 1 if any template scores below this")
    parser.add_argument("--top", type=int, default=25,
                        help="how many of the weakest to print (default 25)")
    parser.add_argument("--hidden-top", type=int, default=10,
                        help="how many of the highest hidden-guidance share "
                             "to print (default 10)")
    parser.add_argument("--path", help="score one file and stop")
    parser.add_argument("--backpointers", action="store_true",
                        help="exit 1 unless the templates with no verified "
                             "filled-example link are exactly "
                             "BACKPOINTER_EXCEPTIONS")
    args = parser.parse_args(argv)

    if args.backpointers:
        return backpointers()

    if args.path:
        report = score_template(Path(args.path))
        print(json.dumps(report, indent=2))
        return 0

    reference = score_template(REFERENCE)
    everything = sorted((score_template(p) for p in template_paths()),
                        key=lambda r: r["score"])
    # Exempt files keep their score and leave the statistics. Dropping them
    # silently would let the median improve by declaring the weak files out of
    # scope, which is the failure this list is most likely to enable.
    exempt = [r for r in everything if r["path"] in EXEMPT]
    scored = [r for r in everything if r["path"] not in EXEMPT]

    values = [r["score"] for r in scored]
    print("flagship rubric, bar read off %s"
          % REFERENCE.relative_to(REPO).as_posix())
    print("  reference score : %.1f  (%d lines, %d sections, %d explained)"
          % (reference["score"], reference["lines"], reference["sections"],
             reference["sections_explained"]))
    print("  reference hidden guidance share: %.1f%%  (%d of %d words inside "
          "<!-- --> comments)"
          % (reference["hidden_guidance_share"] * 100,
             reference["hidden_guidance_words"], reference["total_words"]))
    print("  templates scored: %d" % len(scored))
    if exempt:
        print("  exempt          : %d (listed below, excluded from the "
              "statistics)" % len(exempt))
    print("  median score    : %.1f" % statistics.median(values))
    print("  mean score      : %.1f" % statistics.mean(values))
    for threshold in (90, 75, 60):
        print("  at or above %-3d : %d" % (threshold,
                                           sum(1 for v in values if v >= threshold)))
    print("")
    print("weakest %d:" % min(args.top, len(scored)))
    print("  %-52s %6s %6s %5s %s" % ("template", "score", "lines", "sec",
                                      "biggest gap"))
    for row in scored[:args.top]:
        worst = min(row["marks"], key=lambda k: row["marks"][k] * WEIGHTS[k]
                    if row["marks"][k] < 1 else 99)
        print("  %-52s %6.1f %6d %5d %s"
              % (row["path"], row["score"], row["lines"], row["sections"],
                 worst.replace("_", " ")))

    # F17's informational metric: which templates still hide most of their
    # guidance in HTML comments, ranked over every template this rubric read,
    # exempt ones included, because hiding guidance is a rendering question
    # independent of whether the rubric's seven scored dimensions apply.
    by_hidden = sorted(everything,
                       key=lambda r: (-r["hidden_guidance_share"], r["path"]))
    print("")
    print("highest hidden-guidance share (%d):" % min(args.hidden_top,
                                                       len(by_hidden)))
    print("  %-52s %8s %8s %6s" % ("template", "hidden %", "hidden", "total"))
    for row in by_hidden[:args.hidden_top]:
        print("  %-52s %7.1f%% %8d %6d"
              % (row["path"], row["hidden_guidance_share"] * 100,
                 row["hidden_guidance_words"], row["total_words"]))

    if exempt:
        print("")
        print("exempt from this rubric, with the reason:")
        for row in exempt:
            print("  %-52s %6.1f" % (row["path"], row["score"]))
            for line in _wrap(EXEMPT[row["path"]], 68):
                print("      " + line)

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        hidden_values = [r["hidden_guidance_share"] for r in scored]
        out.write_text(json.dumps({
            "schema": 1,
            "reference": reference,
            "weights": WEIGHTS,
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            # Informational, alongside the score statistics above: never used
            # to compute "median"/"mean" or any WEIGHTS-derived number.
            "hidden_guidance_share_median": statistics.median(hidden_values),
            "hidden_guidance_share_mean": statistics.mean(hidden_values),
            "templates": scored,
        }, indent=2) + "\n", encoding="utf-8")
        print("")
        # An output path outside the repository is a legitimate thing to
        # ask for, and relative_to raises on one. Report what was written.
        try:
            shown = out.relative_to(REPO).as_posix()
        except ValueError:
            shown = str(out)
        print("written to %s" % shown)

    if args.min is not None:
        below = [r for r in scored if r["score"] < args.min]
        print("")
        if below:
            print("%d template(s) below the %.0f bar. The weakest is %s at %.1f."
                  % (len(below), args.min, below[0]["path"], below[0]["score"]))
            return 1
        print("every template is at or above %.0f." % args.min)
    return 0


if __name__ == "__main__":
    sys.exit(main())
