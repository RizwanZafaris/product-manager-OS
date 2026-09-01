# STATE: <product name>

Stage: all stages, written continuously; read first by any runtime resuming this product, and at every gate in [STAGE-GATES](../../os/STAGE-GATES.md)
Knowledge: [knowledge index](../../knowledge/INDEX.md)
Skill: [the Conductor](../../skills/conductor/SKILL.md)

<!-- The fourth continuously written file in the workspace, alongside the decision
     log, the risk register, and the assumptions register. It is the Conductor's
     memory: where the product stands in the loop, every accepted answer, every
     challenge still open, and the evidence behind all of it. The file format is
     the protocol; the runtime is interchangeable. In a chat with no file access,
     paste this file at session start and save the dictated updates back.

     Rules, binding on every writer, human or agent:

     1. Append-mostly. Accepted answers, open challenges, and the evidence ledger
        only grow. A correction is a new row that names what it corrects, never an
        edit to an old one.
     2. "Landed in" is a workspace-relative path plus a section, so every answer is
        auditable against the artifact it produced. Where this file and the
        artifact disagree, the artifact wins and this file gets a correction row.
     3. The evidence ledger holds the load-bearing sentence of each source
        verbatim, in quotation marks, because paraphrase drifts across sessions
        and a quote is checkable later. Quotation marks are reserved for verbatim
        text.
     4. Confidence is one of: verified (two or more independent sources),
        single-source, contested, unverified. Contested rows name what disagrees.
     5. One journal line per session, always, at session end. -->

Updated: <YYYY-MM-DD> by <runtime or person>

## Position

Stage: <DISCOVER | DEFINE | DESIGN | BUILD | DELIVER | OPERATE>
Gate attempts: <gate n: attempt count and outcome, one line each>
Next question: <bank ID, e.g. DEFINE-5>
Overlays active: <AI: yes/no> <regulated: yes/no> <decided at: date, logged where>

## Accepted answers

| ID | Question (short) | Answer (one line) | Evidence class | Landed in |
|---|---|---|---|---|
| | | | | |

## Open challenges

| ID | Answer offered | Why not accepted | Pushes used (n of 2) | Parked to |
|---|---|---|---|---|
| | | | | |

## Evidence ledger

| E# | Claim | Verbatim quote | Source | Source date | Retrieved | Confidence |
|---|---|---|---|---|---|---|
| | | | | | | |

## Journal

<one line per session: date, runtime, questions covered, artifacts touched>
