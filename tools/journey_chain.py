#!/usr/bin/env python3
"""Generator for examples/journey-chain.md, the expense copilot chain run through pmos.

    python3 tools/journey_chain.py            # write examples/journey-chain.md
    python3 tools/journey_chain.py --check    # exit 1 when the record differs from a fresh run

It copies the committed expense copilot documents, with the Ledgerline journey sheet, into a
product workspace, answers every Gate 1 to 3 question from the document that question's lands_in
names, or from a named fallback where the chain never wrote that document, and records what the
runtime returned, pmos's check of each answer's quote included. It stops, and
writes no record, when an example declares nothing to fill in its first eight lines or declares a
file that does not exist, when two examples land on one workspace path, when a question has no
written answer or no document to cite, when an answer is written for a question no bank asks,
when a quoted span is not in the section its answer names, when an answer is a verbatim slice of
its document, or when the document does not carry what the answer's evidence class claims (see
CLAIMS below).
"""
import sys
import os
import io
import re
import json
import hashlib
import tempfile
import contextlib
import difflib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))

from pmos.banks import load_contract
from pmos.cli import main as pmos_main
from pmos.conductor import VERIFICATION_LABELS
from pmos.phases import _LANDS_IN_MD_RE
import workspace


def run_cli(args):
    """Run pmos CLI, capture stdout, return (returncode, stdout_text)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ret = pmos_main(args)
    return ret, buf.getvalue()


SLUG = "expense-copilot"
GATE_OF = {"discover": 1, "define": 2, "design": 3}

# What an example fills is what it says it fills, in the phrasing tools/phase_index.py reads
# and in its first eight lines, naming a frameworks/ file as well as the templates/ files
# phase_index reads. This used to be the first templates/ path anywhere in the file,
# so an example that mentioned one template before declaring another was stamped as the one it
# mentioned, and a file declaring nothing was skipped without a word.
FILLS_RE = re.compile(r"(?:Fills|Produced with) \[((?:templates|frameworks)/[^\]\s]+\.md)\]")
HEAD_LINES = 8
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")

# What an evidence class claims, and so what the cited document must show before an answer is
# submitted under it (the ladder in skills/conductor/questions/README.md). pmos checks that the
# class's fields are present and, when the evidence quotes, that the quote occurs in the cited
# file (_validate_answer and _excerpt_problem, pmos/conductor.py); it does not read who the file
# says said or signed what. These are this generator's checks against the document, and each
# class's person and date are copied into the evidence only once they pass. Both checks read
# words, not meaning: they refuse an attribution the document does not carry, and cannot tell
# the right words used about something else from the same words meant.
#
# - interview_claim, a named person's words on a date: one line of the document must name the
#   person and the date together, as an owner-and-date header or a dated sign-off does. Found
#   anywhere in the file separately, the two would not say who said it when.
# - named_commitment, a named person's written yes: the answer's quote, already required to lie
#   in the section the answer names, must hold one clause that names the person and says one of
#   ASSENT, unnegated. The quote is cut into clauses at every '|', every ';' and every full stop
#   followed by whitespace (CLAUSE_RE). An assent word is negated when any earlier word of its
#   clause is one of NEGATORS or ends in n't, with a straight or a curly apostrophe, so "has not,
#   in writing, approved" is refused where a window of the two words before it would have passed
#   it. No other word is read as a negation: "cannot", "without", "neither" or "refused" before
#   an assent word leave it standing. A document that mentions the person, or records someone
#   else's yes, carries no commitment from them.
#
# No answer here is observed behaviour: nothing in these documents records a user's action with
# a date and a place, and pmos refuses that class without a date, so an entry claiming it would
# stop the run at that answer.
CLAIMS = {"interview_claim": ("person", "date"), "named_commitment": ("person",)}
ASSENT = ("approved", "agreed", "acknowledged", "committed", "signed")
NEGATORS = ("not", "never", "no")
CLAUSE_RE = re.compile(r"\||;|\.\s")
# A word, keeping an apostrophe inside it, so "hasn't" is one word and ends in n't.
WORD_RE = re.compile(r"[a-z]+(?:['\u2019][a-z]+)*")

# The one document each question is answered from, when nothing its lands_in names is in the
# workspace: the chain never wrote an assumptions register, a UI state inventory, an integrations
# document, an observability plan, the AI overlay's tables or a design review record, and STATE.md
# is not an artifact. Every entry is named, so a question cannot reach this list by accident, and
# the run refuses an entry whose lands_in document has since appeared.
FALLBACKS = {
    "DISCOVER-8": "discovery/ledgerline-journey.md",
    "DEFINE-7": "definition/prd.md",
    "DEFINE-9": "definition/prd.md",
    "DESIGN-2": "execution/dependency-register.md",
    "DESIGN-6": "definition/prd.md",
    "DESIGN-7": "execution/decision-log.md",
    "DESIGN-8": "definition/acceptance-criteria.md",
}

# One answer per question, written from the named section of the document the question is
# answered from, never cut out of it: the run refuses an answer that is a verbatim slice of that
# document, and a quote that is not in that section. Where the section does not say what the
# question asks, the answer says so rather than supplying it.
#
# An answer is submitted under its question's evidence class unless its entry names another in
# "class", which pmos accepts only when it is stronger. DEFINE-6, DESIGN-2 and DESIGN-5 ask for a
# named commitment, and no clause of the sections they cite records a yes, in the sense CLAIMS
# gives it, from anyone those sections name, so each is submitted as artifact evidence, the
# document itself, and its answer says what the document does not record.
ANSWERS = {
    "DISCOVER-1": {
        "section": "6. Who feels it and how often", "person": "Maya Chen", "date": "2026-08-13",
        "answer": "Maya Chen's framing names Ledgerline's own filers, the employees who travel or spend "
                  "on the company account and file their own reports: a bounced report stays blocked "
                  "until they correct and resubmit it, while the three finance reviewers lose their "
                  "time to mechanical checks.",
        "quote": "Filers who travel or spend against the company account and file their own reports",
    },
    "DISCOVER-2": {
        "section": "4. Evidence",
        "answer": "The evidence table records the pattern rather than one dated occurrence: filers "
                  "re-type what the receipt shows and bounce on a category mismatch. Its source is the "
                  "discovery interviews, and the table itself marks that row weak.",
        "quote": "Filers re-type what the receipt already states and bounce most often on a category "
                 "mismatch against a policy they have never read",
    },
    "DISCOVER-3": {
        "section": "5. Cost of inaction",
        "answer": "Reviewers lose about 30 hours a month, priced at about $1,800, to mechanical checks a "
                  "correct draft would not need, at a loaded reviewer rate of $60 an hour: reviewer "
                  "time, per month, sourced to the business case (N7, N6).",
        "quote": "about 30 hours, about $1,800, a month spent on mechanical checks a correct draft "
                 "would not need (N7)",
    },
    "DISCOVER-4": {
        "section": "5. Cost of inaction",
        "answer": "Doing nothing keeps first-submission approval at 62% of about 800 reports a month, so "
                  "a share of every month's reports costs a second pass at about 30 minutes each by the "
                  "finance lead's estimate. The framing does not multiply those parts into a monthly "
                  "figure for bounces, and it expects no improvement without a change to how reports "
                  "are built.",
        "quote": "Nothing about the current process is self-correcting",
    },
    "DISCOVER-5": {
        "section": "Pain", "person": "Maya Chen", "date": "2026-08-14",
        "answer": "Twelve interviews stand behind it, eight filers and four finance reviewers held from "
                  "2026-07-20 to 2026-08-01, above the floor of five. The document cites them as one "
                  "group rather than one by one, so no single conversation can be traced to its source.",
        "quote": "From twelve interviews (eight filers, four finance reviewers, held 2026-07-20 to "
                 "2026-08-01)",
    },
    "DISCOVER-6": {
        "section": "Success signal",
        "answer": "The initiative is wrong if drafts come back heavily corrected while first-submission "
                  "approval stays flat, however much the flow is used, and the document commits to "
                  "saying so at the metrics review.",
        "quote": "If drafts are heavily corrected but approval does not move, the hypothesis is wrong "
                 "even if usage is high",
    },
    "DISCOVER-7": {
        "section": "Success signal",
        "answer": "First-submission approval on copilot-drafted reports rising from the 62% baseline "
                  "toward 80%, read from the finance system, with a second signal of half of eligible "
                  "reports using the draft flow within two months and no mandate.",
        "quote": "Two signals, agreed with the finance lead on 2026-08-12",
    },
    "DISCOVER-8": {
        "section": "The setting",
        "answer": "No internal-v1 document names a domain card from the index. The only cards on file "
                  "belong to the later commercial add-on, whose own journey applies B2B SaaS and AI "
                  "products to pricing and selling it; nothing here applies them to this internal build.",
        "quote": "The two sector cards frame the two halves of the problem.",
    },
    "DISCOVER-9": {
        "section": "3. Problem statement",
        "answer": "Ledgerline's filers cannot get a report through review the first time (DISCOVER-1), "
                  "because they re-type receipt data and guess at categories against an unread policy "
                  "(DISCOVER-2), which holds first-submission approval at 62% and costs reviewers about "
                  "30 hours a month (DISCOVER-3).",
        "quote": "Filers at Ledgerline need a way to submit an expense report that clears review the "
                 "first time",
    },
    "DEFINE-1": {
        "section": "1. Index",
        "answer": "c) a quarter: the log records a Gate 2 sitting that approved a PRD with its vision, "
                  "strategy, roadmap and acceptance criteria, a weight option c covers, though no entry "
                  "in the log records the stakes call itself.",
        "quote": "the Gate 2 sitting where vision, strategy, roadmap, PRD and acceptance criteria were "
                 "all approved together",
    },
    "DEFINE-2": {
        "section": "D-4: Ship with an ILLUSTRATIVE accuracy threshold in the eval spec, not a "
                   "finance-agreed number",
        "answer": "Maya Chen, Priya Nair and Daniel Okafor, the three who signed the Gate 2 sitting: each "
                  "signs Gate 2, which releases the definition set to DESIGN. The log names them under "
                  "who was told, and no entry names readers for the weight.",
        "quote": "signed by Maya Chen, Priya Nair and Daniel Okafor (V8)",
    },
    "DEFINE-3": {
        "section": "3. Decisions",
        "answer": "Partly one-way: the log files the receipt pipeline, one model call per receipt, as a "
                  "structural ADR rather than a flag, so the call pattern is locked in, while the scope "
                  "calls around it, D-2 and D-3, each name what would reopen them.",
        "quote": "it is structural, the receipt-pipeline call, and D-2 below is the scope half of the "
                 "same decision",
    },
    "DEFINE-4": {
        "section": "Objectives",
        "answer": "Objectives 1 and 2 trace to the Gate 1 problem statement, approval held at 62% and time "
                  "lost re-typing receipts; objective 3, half of eligible reports through the draft flow "
                  "unmandated, traces to discovery's adoption signal rather than to that statement, and "
                  "the section itself writes no trace down for any of them.",
        "quote": "Raise first-submission approval rate for copilot-drafted reports from the 62% baseline "
                 "toward 80% within one quarter of launch",
    },
    "DEFINE-5": {
        "section": "1. Criteria",
        "answer": "Every one of AC-1 to AC-10 is a GIVEN, WHEN and THEN with a binary threshold a tester "
                  "can stage; AC-3, for one, fails the moment an unreadable field comes back populated "
                  "rather than blank and flagged.",
        "quote": "binary outcome, no field is populated without source text on the receipt",
    },
    "DEFINE-6": {
        "section": "Out of scope", "class": "artifact",
        "answer": "Four exclusions are written: auto-submission, card-feed reconciliation with mileage "
                  "and per-diem rules, filing on another person's behalf, and any vendor training on "
                  "expense data. The header records the Gate 2 approval, but nothing in the PRD records "
                  "the sponsor reading the list: it names Daniel Okafor as the finance lead who agreed "
                  "the objective 1 baseline and as that metric's owner, never beside this list.",
        "quote": "The filer submits, always; this is a load-bearing guardrail, not a v2 candidate.",
    },
    "DEFINE-7": {
        "section": "Trade-offs accepted at Gate 2",
        "answer": "No assumptions register exists in this workspace. The nearest record is the "
                  "trade-offs table, whose third row carries an open gap rather than a stated "
                  "assumption: with no extraction baseline the accuracy bar stays ILLUSTRATIVE until "
                  "four weeks of live data, with no confidence or validate-by date attached.",
        "quote": "We had no baseline for machine extraction on our own receipt mix.",
    },
    "DEFINE-8": {
        "section": "1. Index",
        "answer": "Yes to the model half: D-4, taken at the Gate 2 sitting, ships an eval spec with an "
                  "ILLUSTRATIVE accuracy threshold, which only a model producing user-facing drafts "
                  "needs. On the regulator half the log records nothing either way.",
        "quote": "Ship with an ILLUSTRATIVE accuracy threshold in the eval spec, not a finance-agreed "
                 "number",
    },
    "DEFINE-9": {
        "section": "Functional scope",
        "answer": "Yes: the functional scope puts a draft-and-edit surface in front of filers and a "
                  "reviewer view that marks low-confidence fields, but no UI state inventory exists in "
                  "this workspace, so no screen's states or owner are listed anywhere.",
        "quote": "Draft report assembly and edit surface",
    },
    "DEFINE-10": {
        "section": "2. Who this is for",
        "answer": "Ledgerline's own filers, who want a report that clears review the first time without "
                  "re-typing the receipt or guessing at a policy line, which is the Gate 1 problem; the "
                  "reviewers and the parked assistant workflow are named as not served yet. The business "
                  "sponsor, Daniel Okafor, approved it at Gate 2 on 2026-08-28.",
        "quote": "Filers at Ledgerline: individual contributors who travel or spend against the company "
                 "account and file their own expense reports",
    },
    "DEFINE-11": {
        "section": "2. Where to play: the bets",
        "answer": "It plays across all of Ledgerline's own filers as one internal rollout, bets v1 on "
                  "extraction accuracy and first-submission approval, and refuses a pilot-only rollout, "
                  "a learning mapping loop in v1 and building card-feed or payment tools itself; Maya "
                  "Chen and Daniel Okafor both approved it on 2026-08-28.",
        "quote": "Extraction accuracy and first-submission approval as the v1 bet, ahead of a learning "
                 "category-mapping loop",
    },
    "DEFINE-12": {
        "section": "Next (planned, shaped, not yet committed)",
        "answer": "Four Next initiatives follow the close of DEFINE: prove the receipt pipeline, the data "
                  "and interface contracts, close DESIGN, and settle the vendor terms. Each names the "
                  "outcome it serves and what it depends on, but the table has no success-measure "
                  "column, and only the first outcome states a measured target, approval from 62% "
                  "toward 80% and filing time toward under 10 minutes. Maya Chen and Priya Nair "
                  "approved the roadmap on 2026-08-28.",
        "quote": "ADR-0001: one receipt per model call, matched to one uploaded photo or one "
                 "forwarded-email attachment",
    },
    "DESIGN-1": {
        "section": "Rejected option: batch multiple receipts into a single extraction call",
        "answer": "Batching a whole photographed stack into one extraction call was considered and "
                  "rejected, because the eval set could not hold a threshold on overlapping receipts; the "
                  "consequence accepted is that filers photograph one receipt at a time.",
        "quote": "It lost on the same ground the PRD's Trade-offs accepted table already recorded for v1",
    },
    "DESIGN-2": {
        "section": "1. The register", "class": "artifact",
        "answer": "No integrations document exists in this workspace. The dependency register carries "
                  "the two outside systems v1 relies on, the model vendor and the finance system, each "
                  "with an owning team and Daniel Okafor as escalation contact, but no row states an SLA "
                  "or a failure behaviour, and no counterparty's commitment is recorded beyond the "
                  "finance join's committed date.",
        "quote": "All four rows escalate to the same person, Daniel Okafor.",
    },
    "DESIGN-3": {
        "section": "5. PII and classification summary",
        "answer": "Personal data sits in two entities, the receipt and its line item, flagged "
                  "provisionally rather than classified, with sign-off left to Gate 5; the deletion path "
                  "is not yet defined and waits on the legal lead's retention schedule, due before Gate 5.",
        "quote": "Deletion path when a subject requests erasure: not yet defined",
    },
    "DESIGN-4": {
        "section": "2. The register",
        "answer": "Two distinct causes lead the register, both scored 6 with a mitigation and a trigger: "
                  "extraction on crumpled or foreign-language receipts is unproven, and the vendor's "
                  "training-data and retention terms stay unresolved. The second is owned by the legal "
                  "lead, a role with no name on file.",
        "quote": "Extraction quality on crumpled or foreign-language receipts is unproven",
    },
    "DESIGN-5": {
        "section": "1. The register", "class": "artifact",
        "answer": "Four dependencies, each needed by Gate 5 except the contracted price, needed before "
                  "volume outgrows the quoted rate: the legal lead owes the vendor clause and the "
                  "retention schedule, procurement the price, finance the approval-event join. Only the "
                  "finance join is committed, dated 2026-10-09 on Finance's own Gate 5 plan; the register "
                  "names no one inside Finance, lists Priya Nair as the contact, and escalates every row "
                  "to Daniel Okafor.",
        "quote": "Only DEPV-4 is marked committed.",
    },
    "DESIGN-6": {
        "section": "Success metrics",
        "answer": "No observability document exists here, and none of the expense copilot documents "
                  "names an SLO, an alert or a dashboard; the one dashboard in this workspace, with alerts "
                  "agreed per metric owner, is the later commercial add-on's, described in the Ledgerline "
                  "journey sheet. The nearest thing for this build is the PRD's guardrail metric: "
                  "reviewer-caught extraction errors held under 3 per 100 reports, owned by P. Nair and "
                  "read from a reviewer flag button.",
        "quote": "Guardrail: reviewer-caught extraction errors per 100 reports",
    },
    "DESIGN-7": {
        "section": "D-6: Defer the AI overlay's guardrails, eval spec and red-team review to the PRD's "
                   "existing Gate 5 launch criteria rather than duplicate them at Gate 3",
        "answer": "Not at this gate: D-6 defers the AI overlay's guardrails, eval spec and red-team "
                  "review to the PRD's Gate 5 launch criteria, so neither an agent permission table nor "
                  "the overlay's guardrail table exists in this workspace, and no agent's access has "
                  "been written down.",
        "quote": "duplicating any of them in a lighter form at Gate 3 would create two documents that "
                 "could disagree about the same guardrail",
    },
    "DESIGN-8": {
        "section": "AC-7 verifies REQ-5 (happy path)",
        "answer": "Yes, the reviewer view is a user-facing surface: AC-7 requires low-confidence fields to "
                  "stand out there, checked by hand until a UI test exists, with Priya Nair as owner. No "
                  "design review record or accessibility checklist exists in this workspace.",
        "quote": "the visual-distinction check is manual until a UI test asserts the styling",
    },
}


def declared_fill(text):
    """The templates/ or frameworks/ file an example declares it fills, or None."""
    match = FILLS_RE.search("\n".join(text.split("\n")[:HEAD_LINES]))
    return match.group(1) if match else None


def build_workspace(root: Path):
    """Copy example docs into the workspace, rewrite relative links, stamp artifacts."""
    examples_dir = REPO / "examples"
    files = sorted(examples_dir.glob("expense-copilot-*.md"))
    journey = examples_dir / "expense-copilot-journey.md"
    files = [f for f in files if f.name != "expense-copilot-journey.md"]
    JOURNEY_DEST = "discovery/journey.md"

    copied = []  # list of dicts: example, template, path (relative)
    mapping = {}  # example basename -> relative path

    product_root = root

    planned = []
    for f in files:
        text = f.read_text()
        template = declared_fill(text)
        if template is None:
            raise SystemExit("%s declares nothing to fill: none of its first %d lines says "
                             "'Fills [templates/...]' or 'Produced with [templates/...]', so it has "
                             "no workspace path" % (f.name, HEAD_LINES))
        if not (REPO / template).is_file():
            raise SystemExit("%s declares it fills %s, which is not a file" % (f.name, template))
        # The declared file's own text, not the example's: for a frameworks/ declaration the
        # destination is read from that file's stage, and an example carries no frontmatter.
        rel = workspace.destination_for(template, SLUG, workspace.read_text(REPO / template)).replace(
            "products/%s/" % SLUG, "", 1)
        mapping[f.name] = rel
        planned.append((f, template, rel, text))
    # The journey is the chain's data sheet, not an artifact: it fills no template and carries no
    # artifact block, so it is copied for its links to resolve and never stamped.
    mapping[journey.name] = JOURNEY_DEST
    planned.append((journey, None, JOURNEY_DEST, journey.read_text()))
    shared = examples_dir / "ledgerline-journey.md"
    mapping[shared.name] = "discovery/ledgerline-journey.md"
    planned.append((shared, None, "discovery/ledgerline-journey.md", shared.read_text()))

    # Checked before anything is written: the second copy would silently replace the first, and
    # the chain would then cite a document the committed examples say something else about.
    landed = {}
    for f, _template, rel, _text in planned:
        if rel in landed:
            raise SystemExit("%s and %s both land at %s; a workspace path holds one document"
                             % (landed[rel], f.name, rel))
        landed[rel] = f.name

    for f, template, rel, text in planned:
        def link_repl(match, rel=rel):
            target = match.group(1)
            if target in mapping:
                return "](%s)" % os.path.relpath(mapping[target], start=os.path.dirname(rel))
            return match.group(0)
        text = re.sub(r"\]\(([^)]+\.md)\)", link_repl, text)
        if template is not None:
            text = workspace.stamp_artifact(text, template, SLUG)
        copied.append({"example": f.name, "template": template or "fills no template (data sheet)", "path": rel})
        dest_path = product_root / rel
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(text)

    return copied


def section_body(text, heading):
    """The lines under one heading, up to the next heading of its level or higher, or None."""
    lines = text.split("\n")
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or match.group(2) != heading:
            continue
        body = []
        for later in lines[index + 1:]:
            other = HEADING_RE.match(later)
            if other and len(other.group(1)) <= len(match.group(1)):
                break
            body.append(later)
        return "\n".join(body)
    return None


def cite(question, root: Path):
    """(path, fallback) for the document one question is answered from.

    The first document the question's lands_in names that the workspace holds; only when it holds
    none of them, the question's named fallback. Cycling through a list of artifacts, as this did,
    picks by where a counter stands: with DEFINE-10 to DEFINE-12 added it would have answered the
    strategy question from the PRD and the roadmap question from the acceptance criteria.
    """
    qid = question["id"]
    named = _LANDS_IN_MD_RE.findall(question.get("lands_in") or "")
    present = [path for path in named if (root / path).is_file()]
    fallback = FALLBACKS.get(qid)
    if present:
        if fallback:
            raise SystemExit("%s: %s, which its lands_in names, is in the workspace now, so its "
                             "fallback to %s is stale; answer it from %s and drop the fallback"
                             % (qid, present[0], fallback, present[0]))
        return present[0], False
    if fallback and (root / fallback).is_file():
        return fallback, True
    raise SystemExit("%s: its lands_in names %s, none of which this workspace holds, and %s"
                     % (qid, ", ".join(named) or "no document",
                        "its fallback %s is not in it either" % fallback if fallback
                        else "it has no fallback"))


def negates(word):
    """Whether one lower-cased word of a clause negates any assent word after it."""
    return word in NEGATORS or word.endswith("n't") or word.endswith("n\u2019t")


def records_yes(quote, person):
    """Whether one clause of quote names person and says yes, in the sense CLAIMS gives it.

    A table row that names a person in one cell and says committed in another is two clauses,
    and neither is a yes from that person; so are two sentences when one says approved and the
    next names the person, and two halves of a sentence joined by a semicolon.
    """
    for clause in CLAUSE_RE.split(quote):
        if person not in clause:
            continue
        words = WORD_RE.findall(clause.lower())
        for index, word in enumerate(words):
            if word in ASSENT and not any(negates(earlier) for earlier in words[:index]):
                return True
    return False


def claim_problem(evidence_class, entry, text):
    """What text, the whole cited document, lacks for evidence_class's claim, or None.

    entry's quote has already been found in the section the entry names.
    """
    missing = [field for field in CLAIMS.get(evidence_class, ()) if not entry.get(field)]
    if missing:
        return "the answer names no %s" % " and no ".join(missing)
    if evidence_class == "interview_claim":
        person, date = entry["person"], entry["date"]
        if not any(person in line and date in line for line in text.split("\n")):
            return "no line of it names %s together with %s" % (person, date)
    if evidence_class == "named_commitment" and not records_yes(entry["quote"], entry["person"]):
        return ("no clause of the quote names %s and says %s or %s"
                % (entry["person"], ", ".join(ASSENT[:-1]), ASSENT[-1]))
    return None


def evidence_for(question, cited, root: Path):
    """The evidence one answer is submitted with, or SystemExit naming the question."""
    qid = question["id"]
    entry = ANSWERS.get(qid)
    if entry is None:
        raise SystemExit("%s: no answer is written for it in tools/journey_chain.py; write one from "
                         "the section of %s it lands in" % (qid, cited))
    text = (root / cited).read_text(encoding="utf-8")
    body = section_body(text, entry["section"])
    if body is None:
        raise SystemExit("%s: %s has no section headed %r" % (qid, cited, entry["section"]))
    if entry["quote"] not in body:
        raise SystemExit("%s: the quoted span is not in section %r of %s: %r"
                         % (qid, entry["section"], cited, entry["quote"]))
    # A quote cut from the same span as the answer would make the quote check true by
    # construction, so the answer is refused when it is itself a slice of the document.
    if entry["answer"] in text:
        raise SystemExit("%s: the answer is a verbatim slice of %s; write it from the section "
                         "instead of cutting it out" % (qid, cited))
    evidence_class = entry.get("class", question["evidence_class"])
    problem = claim_problem(evidence_class, entry, text)
    if problem is not None:
        raise SystemExit("%s: %s evidence claims what %s does not carry: %s; the run will not "
                         "supply it" % (qid, evidence_class, cited, problem))
    evidence = {"class": evidence_class, "source": cited,
                "location": entry["section"], "quote": entry["quote"]}
    for field in CLAIMS.get(evidence_class, ()):
        evidence[field] = entry[field]
    return evidence


def plan_answers(root: Path, contract):
    """Question id to (cited path, fallback, evidence) for every Gate 1 to 3 question.

    Everything is checked before pmos sees any of it, so a failure names a question rather than
    leaving a half-answered workspace.
    """
    banks = [bank for bank in contract["banks"] if bank["id"] in GATE_OF]
    asked = {question["id"] for bank in banks for question in bank["questions"]}
    unasked = sorted(set(ANSWERS) - asked)
    if unasked:
        raise SystemExit("tools/journey_chain.py answers %s, which no Gate 1 to 3 bank asks"
                         % ", ".join(unasked))
    plan = {}
    for bank in banks:
        for question in bank["questions"]:
            cited, fallback = cite(question, root)
            plan[question["id"]] = (cited, fallback, evidence_for(question, cited, root))
    return plan


def drive_gates(root: Path, plan: dict):
    """Run init, answer all questions, approve gates, generate handoff."""
    product_root = root
    # init
    run_cli(["init", "--path", str(root), "--product-id", SLUG])

    gates = []  # per bank info
    answers = []  # per question: id, cited path, fallback, section, answer
    for bank in ("discover", "define", "design"):
        q_count = 0
        latest_rev = None
        for _guard in range(40):
            st = json.loads(run_cli(["--json", "status", "--path", str(root),
                                     "--product-id", SLUG])[1])
            if st["interview"] != "question":
                latest_rev = st.get("revision_token")
                break
            qid = st["question"]["id"]
            # Belt and braces, unreachable today: init pins pmos/question_banks.json, the file
            # plan_answers read in this same process, so every id pmos asks is planned. It stays
            # so a divergence names the question rather than raising a KeyError below.
            if qid not in plan:
                raise SystemExit("%s: the runtime asked it, and the pinned contract this run planned "
                                 "from does not carry it" % qid)
            cited, fallback, evidence = plan[qid]
            ans_cmd = [
                "answer", "--path", str(root), "--product-id", SLUG,
                "--question-id", qid,
                "--answer", ANSWERS[qid]["answer"],
                "--evidence", json.dumps(evidence),
                "--expected-revision", st["revision_token"],
                "--turn-id", "%s-%d" % (qid.lower(), _guard),
                "--json"
            ]
            _, out = run_cli(ans_cmd)
            ans = json.loads(out)
            outcome = ans.get("outcome") or {}
            if not ans.get("ok", True) or outcome.get("accepted") is False:
                raise SystemExit("answer refused for %s: %s" % (qid, outcome.get("message", ans)))
            q_count += 1
            answers.append({"id": qid, "cited": cited, "fallback": fallback,
                            "section": evidence["location"], "answer": ANSWERS[qid]["answer"],
                            "class": evidence["class"], "asks": st["question"]["evidence_class"]})
            latest_rev = st.get("revision_token")
        else:
            raise SystemExit("bank %s did not finish within 40 turns" % bank)

        # write approval
        approval_rel = f"approvals/gate-{bank}.md"
        approval_path = product_root / approval_rel
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        approval_path.write_text(f"# Gate approval for {bank}\n")
        sha = hashlib.sha256(approval_path.read_bytes()).hexdigest()

        gate_cmd = [
            "gate", "--path", str(root), "--product-id", SLUG,
            "--bank-id", bank,
            "--evidence", json.dumps({
                "source": approval_rel,
                "source_sha256": sha,
                "actor_id": "local-reviewer",
                "requester_id": "local-operator",
                "decision": "approved",
                "approved_at": "2026-09-11T00:00:00Z"
            }),
            "--expected-revision", latest_rev,
            "--turn-id", f"gate-{bank}",
            "--json"
        ]
        _, out = run_cli(gate_cmd)
        gate_data = json.loads(out)
        gate_outcome = (gate_data.get("outcome") or {}).get("status", "unknown")
        gates.append({
            "bank": bank,
            "questions": q_count,
            # The section column is q_count by construction, not a second count: plan_answers
            # stops the run before pmos is reached if any quote fails, so a record that exists
            # can only report every answer's quote as found. The record says so beside it.
            "quoted": q_count,
            "outcome": gate_outcome
        })

    # handoff
    _, handoff_out = run_cli(["handoff", "--path", str(root), "--product-id", SLUG, "--json"])
    handoff_data = json.loads(handoff_out)
    index_path = root / "handoff" / "context-index.json"
    if index_path.is_file():
        index = json.loads(index_path.read_text())
        handoff_data["sections"] = index.get("sections", [])
        handoff_data["approvals"] = index.get("approvals", [])

    return gates, answers, handoff_data


def staleness(root: Path, base_handoff: dict):
    """Edit a cited doc and re-run handoff/status; return updated data."""
    product_root = root
    doc = product_root / "discovery/problem-framing.md"
    with open(doc, "a") as f:
        f.write("\nEdited to make stale.\n")

    _, handoff_out = run_cli(["handoff", "--path", str(root), "--product-id", SLUG, "--json"])
    handoff2 = json.loads(handoff_out)

    _, status_out = run_cli(["--json", "status", "--path", str(root), "--product-id", SLUG])
    status_data = json.loads(status_out)
    stale_banks = [sb.get("bank_id") for sb in status_data.get("stale_banks", [])]

    return handoff2, stale_banks


def generate_markdown(copied, gates, answers, handoff_before, handoff_after, stale_banks_after):
    lines = []
    lines.append("# Journey chain: the expense copilot from discovery to a development-ready handoff")
    lines.append("")
    lines.append("This file fills no template; it is generated by `tools/journey_chain.py`, which builds a product workspace from the committed expense copilot example documents and the Ledgerline journey sheet, runs the pmos command line through Gates 1 to 3 answering every question from a named section of one of those documents, the one that question's lands_in names wherever the chain wrote it, with a verbatim quote from that section, and records what the runtime returned. Everything in the source documents is FICTIONAL, invented for that example journey; this record proves the runtime executes the chain, not anything about a real product. See the [examples index](README.md).")
    lines.append("")
    lines.append("**Generated by:** `python3 tools/journey_chain.py` * **Verified by:** `python3 tools/journey_chain.py --check`")
    lines.append("")
    lines.append("## The workspace")
    lines.append("")
    lines.append("| Artifact | Template it fills | Workspace path |")
    lines.append("|---|---|---|")
    for row in sorted(copied, key=lambda x: x["path"]):
        lines.append(f"| {row['example']} | {row['template']} | {row['path']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    # Every figure but the section column is read from the handoff package the runtime wrote,
    # each approvals row carrying its own bank's labels and the artifacts its approval bound.
    approvals = {item["bank_id"]: item for item in handoff_before["approvals"]}
    labels = " | ".join("pmos %s" % label for label in VERIFICATION_LABELS)
    lines.append(f"| Gate | Bank | Questions answered | {labels} | Quote found in the section its answer names (checked by tools/journey_chain.py, not by pmos) | Artifacts bound to the approval | Gate outcome |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for g in gates:
        approval = approvals[g["bank"]]
        counts = " | ".join(str(approval["evidence"][label]) for label in VERIFICATION_LABELS)
        bound = len(approval.get("artifacts") or [])
        lines.append(f"| {GATE_OF[g['bank']]} | {g['bank']} | {g['questions']} | {counts} | {g['quoted']} | {bound} | {g['outcome']} |")
    lines.append("")
    quoted = sum(approvals[g["bank"]]["evidence"]["quote_verified"] for g in gates)
    answered = sum(g["questions"] for g in gates)
    if quoted == answered:
        recorded = "Every answer here quotes the document it cites, and pmos recorded each one quote_verified."
    else:
        recorded = f"pmos recorded {quoted} of the {answered} answers here quote_verified."
    lines.append("The three pmos columns are the label pmos stored with each accepted answer, one label per answer (`_validate_answer` and `_excerpt_problem`, pmos/conductor.py). quote_verified: the evidence's `quote` occurs in the cited file, a regular file inside the workspace, compared with every run of whitespace collapsed to one space and nothing else folded. source_verified: the cited path is such a file and the evidence quotes nothing, so pmos read nothing inside it. supplied_unverified: neither. " + recorded + " quote_verified says those words occur somewhere in that file; it does not say they sit in the section the answer names, or that the file supports the answer. The section column is this generator's own check, made before any answer reaches pmos: the answer's `quote` must appear verbatim in the section it names of the document it cites, and the answer itself must not be a verbatim slice of that document. A run in which any answer fails either check stops and writes no record, so in every record this generator writes the section column equals the answered column by construction: it says each quote was found there, not how many would have been.")
    lines.append("")
    lines.append("## The answers")
    lines.append("")
    fallbacks = sum(1 for row in answers if row["fallback"])
    lines.append(f"Each question cites the first document its lands_in names that the workspace holds. {fallbacks} of the {len(answers)} name no document the expense copilot chain ever wrote, so each of those cites the one document named for it in `tools/journey_chain.py`, and its row says so.")
    lines.append("")
    lines.append("The evidence class is the one each answer was submitted under. pmos accepts the class a question asks for or a stronger one, and where the two differ the cell names both. Before any answer reaches pmos, this generator checks its class against its document: an interview claim's person and date must be named together on one line of the document, and a named commitment's quote, cut into clauses at every `|`, every `;` and every full stop followed by whitespace, must hold a clause that names the person and says approved, agreed, acknowledged, committed or signed with no \"not\", \"never\" or \"no\", and no word ending in n't, anywhere before that word in the clause. Both checks read words, not meaning.")
    lines.append("")
    lines.append("| Question | Evidence class | Cited file | Section | First 15 words of the answer |")
    lines.append("|---|---|---|---|---|")
    for row in answers:
        cited = f"lands_in target absent, cited {row['cited']}" if row["fallback"] else row["cited"]
        klass = row["class"] if row["class"] == row["asks"] else f"{row['class']} (asks {row['asks']})"
        words = " ".join(row["answer"].split()[:15])
        lines.append(f"| {row['id']} | {klass} | {cited} | {row['section']} | {words} |")
    lines.append("")
    lines.append("## The handoff")
    lines.append("")
    dev_ready = "true" if handoff_before.get("development_ready") else "false"
    missing = handoff_before.get("missing", [])
    missing_str = ", ".join(missing) if missing else "nothing missing"
    sections = handoff_before.get("sections", [])
    total = len(sections)
    status_counts = {}
    for s in sections:
        st = s.get("status", "unknown")
        status_counts[st] = status_counts.get(st, 0) + 1
    status_parts = ", ".join(f"{k}: {v}" for k, v in sorted(status_counts.items()))
    evidence = handoff_before["evidence"]
    evidence_str = ", ".join("%d %s" % (evidence[label], label) for label in VERIFICATION_LABELS)
    lines.append(f"development_ready: {dev_ready}. Sections: {total} ({status_parts}). Missing: {missing_str}. Evidence the package reports, every bank counted: {evidence_str}.")
    lines.append("")
    lines.append("## What changes when a cited document changes")
    lines.append("")
    lines.append("| Step | development_ready | stale banks | first missing entry |")
    lines.append("|---|---|---|---|")
    before_dev = "true" if handoff_before.get("development_ready") else "false"
    before_missing = ", ".join(handoff_before.get("missing", [])) if handoff_before.get("missing") else "nothing missing"
    after_dev = "true" if handoff_after.get("development_ready") else "false"
    stale_str = ", ".join(stale_banks_after) if stale_banks_after else "none"
    after_missing = ", ".join(handoff_after.get("missing", [])) if handoff_after.get("missing") else "nothing missing"
    lines.append(f"| Before edit | {before_dev} | none | {before_missing} |")
    lines.append(f"| After edit | {after_dev} | {stale_str} | {after_missing} |")
    lines.append("")
    lines.append("## Result")
    lines.append("")
    lines.append(f"Before the edit, development_ready was {before_dev}; after the edit it is {after_dev}.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    out_file = "examples/journey-chain.md"
    check = False
    if "--check" in argv:
        check = True
        argv.remove("--check")
    if "--out" in argv:
        i = argv.index("--out")
        out_file = argv[i+1]
        del argv[i:i+2]

    copied = None
    gates = None
    handoff_before = None
    handoff_after = None
    stale_banks = None

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        copied = build_workspace(root)
        plan = plan_answers(root, load_contract())
        gates, answers, handoff_before = drive_gates(root, plan)
        handoff_after, stale_banks = staleness(root, handoff_before)

    content = generate_markdown(copied, gates, answers, handoff_before, handoff_after, stale_banks)

    out_path = REPO / out_file
    if check:
        if out_path.exists():
            old = out_path.read_text()
            if old == content:
                print("journey chain matches a fresh run")
                return 0
            else:
                diff = difflib.unified_diff(old.splitlines(True), content.splitlines(True),
                                            'existing', 'fresh')
                sys.stdout.writelines(diff)
                return 1
        else:
            print("output file does not exist", file=sys.stderr)
            return 1
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
