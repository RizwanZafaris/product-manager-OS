#!/usr/bin/env python3
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

from pmos.cli import main as pmos_main
import workspace


def run_cli(args):
    """Run pmos CLI, capture stdout, return (returncode, stdout_text)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ret = pmos_main(args)
    return ret, buf.getvalue()


GATE_OF = {"discover": 1, "define": 2, "design": 3}

ARTIFACT_SETS = {
    "discover": ["discovery/problem-framing.md", "discovery/discovery-document.md"],
    "define": ["definition/prd.md", "definition/acceptance-criteria.md", "planning/vision.md",
               "planning/product-strategy.md", "planning/roadmap.md"],
    "design": ["architecture/adr.md", "architecture/data-model.md", "architecture/api-contract.md",
               "execution/risk-register.md", "execution/dependency-register.md"],
}


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
        m = re.search(r"templates/[a-z]+/[a-z0-9-]+\.md", text)
        if not m:
            continue
        template = m.group(0)
        rel = workspace.destination_for(template, "expense-copilot", text).replace(
            "products/expense-copilot/", "", 1)
        mapping[f.name] = rel
        planned.append((f, template, rel, text))
    # The journey is the chain's data sheet, not an artifact: it fills no template and carries no
    # artifact block, so it is copied for its links to resolve and never stamped.
    mapping[journey.name] = JOURNEY_DEST
    planned.append((journey, None, JOURNEY_DEST, journey.read_text()))
    shared = examples_dir / "ledgerline-journey.md"
    mapping[shared.name] = "discovery/ledgerline-journey.md"
    planned.append((shared, None, "discovery/ledgerline-journey.md", shared.read_text()))

    for f, template, rel, text in planned:
        def link_repl(match, rel=rel):
            target = match.group(1)
            if target in mapping:
                return "](%s)" % os.path.relpath(mapping[target], start=os.path.dirname(rel))
            return match.group(0)
        text = re.sub(r"\]\(([^)]+\.md)\)", link_repl, text)
        if template is not None:
            text = workspace.stamp_artifact(text, template, "expense-copilot")
        copied.append({"example": f.name, "template": template or "fills no template (data sheet)", "path": rel})
        dest_path = product_root / rel
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(text)

    # Every cited artifact must be a real, stamped copy. A placeholder here would prove nothing.
    for artifacts in ARTIFACT_SETS.values():
        for art in artifacts:
            if not (product_root / art).is_file():
                raise SystemExit("expected artifact missing from the workspace: %s" % art)

    return copied


def drive_gates(root: Path, bank_artifacts: dict):
    """Run init, answer all questions, approve gates, generate handoff."""
    product_root = root
    # init
    run_cli(["init", "--path", str(root), "--product-id", "expense-copilot"])

    gates = []  # per bank info
    for bank in ("discover", "define", "design"):
        q_count = 0
        v_count = 0
        latest_rev = None
        for _guard in range(40):
            st = json.loads(run_cli(["--json", "status", "--path", str(root),
                                     "--product-id", "expense-copilot"])[1])
            if st["interview"] != "question":
                latest_rev = st.get("revision_token")
                break
            q = st["question"]
            qid = q["id"]
            ev_class = q["evidence_class"]
            # pick artifact cycling
            artifacts = bank_artifacts[bank]
            idx = q_count % len(artifacts)
            art = artifacts[idx]

            ans_cmd = [
                "answer", "--path", str(root), "--product-id", "expense-copilot",
                "--question-id", qid,
                "--answer", f"Recorded in {art}, which this workspace carries as a stamped artifact.",
                # Each evidence class demands its own fields (pmos/conductor.py): a person for an
                # interview claim or a named commitment, a location for an artifact, a date for
                # observed behaviour. Supply all of them, sourced at the artifact this cites.
                "--evidence", json.dumps({
                    "class": ev_class,
                    "source": art,
                    "person": "Maya Chen",
                    "date": "2026-09-11",
                    "location": art,
                }),
                "--expected-revision", st["revision_token"],
                "--turn-id", "%s-%d" % (qid.lower(), _guard),
                "--json"
            ]
            _, out = run_cli(ans_cmd)
            ans = json.loads(out)
            outcome = ans.get("outcome") or {}
            if not ans.get("ok", True) or outcome.get("accepted") is False:
                raise SystemExit("answer refused for %s: %s" % (qid, outcome.get("message", ans)))
            # check verification
            verified = False
            if "source_verified" in ans:
                verified = bool(ans["source_verified"])
            elif "source" in ans and isinstance(ans["source"], dict):
                verified = bool(ans["source"].get("verified", False))
            q_count += 1
            v_count += 1 if verified else 0
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
            "gate", "--path", str(root), "--product-id", "expense-copilot",
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
            "verified": v_count,
            "outcome": gate_outcome
        })

        _, st_out = run_cli(["--json", "status", "--path", str(root), "--product-id", "expense-copilot"])
        running = json.loads(st_out).get("source_verified", 0)
        gates[-1]["verified"] = running - sum(g["verified"] for g in gates[:-1])

    # handoff
    _, handoff_out = run_cli(["handoff", "--path", str(root), "--product-id", "expense-copilot", "--json"])
    handoff_data = json.loads(handoff_out)
    index_path = root / "handoff" / "context-index.json"
    if index_path.is_file():
        handoff_data["sections"] = json.loads(index_path.read_text()).get("sections", [])

    return gates, handoff_data


def staleness(root: Path, base_handoff: dict):
    """Edit a cited doc and re-run handoff/status; return updated data."""
    product_root = root
    doc = product_root / "discovery/problem-framing.md"
    with open(doc, "a") as f:
        f.write("\nEdited to make stale.\n")

    _, handoff_out = run_cli(["handoff", "--path", str(root), "--product-id", "expense-copilot", "--json"])
    handoff2 = json.loads(handoff_out)

    _, status_out = run_cli(["--json", "status", "--path", str(root), "--product-id", "expense-copilot"])
    status_data = json.loads(status_out)
    stale_banks = [sb.get("bank_id") for sb in status_data.get("stale_banks", [])]

    return handoff2, stale_banks


def generate_markdown(copied, gates, handoff_before, handoff_after, stale_banks_after):
    lines = []
    lines.append("# Journey chain: the expense copilot from discovery to a development-ready handoff")
    lines.append("")
    lines.append("This file fills no template; it is generated by `tools/journey_chain.py`, which builds a product workspace from the committed expense copilot example documents, runs the pmos command line through Gates 1 to 3 answering every question with evidence that cites those documents, and records what the runtime returned. Everything in the source documents is FICTIONAL, invented for that example journey; this record proves the runtime executes the chain, not anything about a real product. See the [examples index](README.md).")
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
    lines.append("| Gate | Bank | Questions answered | Evidence citing a workspace file | Gate outcome |")
    lines.append("|---|---|---|---|---|")
    for g in gates:
        lines.append(f"| {GATE_OF[g['bank']]} | {g['bank']} | {g['questions']} | {g['verified']} | {g['outcome']} |")
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
    lines.append(f"development_ready: {dev_ready}. Sections: {total} ({status_parts}). Missing: {missing_str}.")
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
        bank_artifacts = {
            "discover": ["discovery/problem-framing.md", "discovery/discovery-document.md"],
            "define": ["definition/prd.md", "definition/acceptance-criteria.md", "planning/vision.md",
                       "planning/product-strategy.md", "planning/roadmap.md"],
            "design": ["architecture/adr.md", "architecture/data-model.md", "architecture/api-contract.md",
                       "execution/risk-register.md", "execution/dependency-register.md"]
        }
        gates, handoff_before = drive_gates(root, bank_artifacts)
        handoff_after, stale_banks = staleness(root, handoff_before)

    content = generate_markdown(copied, gates, handoff_before, handoff_after, stale_banks)

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
