# AGENTS

Single source of truth for any agent runtime operating this repository: Claude Code, Codex, or anything else that reads an agents file. CLAUDE.md is a thin router that defers here.

## What this repository is

Product Manager OS: a document system that runs one product through six stages (DISCOVER, DEFINE, DESIGN, BUILD, DELIVER, OPERATE), each ending at a gate defined in [os/STAGE-GATES.md](os/STAGE-GATES.md). Templates in `templates/` are the artifacts, knowledge cards in `knowledge/` are the methods behind them, and the files here tell you how to drive both. The system works with no agent at all; you are an accelerant, not a dependency.

## Load order on any user request

1. **Read [os/OPERATING-LOOP.md](os/OPERATING-LOOP.md)** and place the request in a stage. A request for "a PRD" is DEFINE work; "why is nobody using this" is OPERATE work feeding a new DISCOVER pass.
2. **Check the overlays.** Product contains a model: the `templates/ai/` overlay applies. Product operates under a financial or data regulator: `modules/regulated/` applies, routed through [skills/reg-gap-check/SKILL.md](skills/reg-gap-check/SKILL.md).
3. **Check the router.** If a skill in `skills/` covers the request, follow that SKILL.md exactly. Triggering lives here and in CLAUDE.md, never inside the skill.
4. **Pick the weight, then open the template.** [os/WHICH-DOCUMENT.md](os/WHICH-DOCUMENT.md) decides between a logged decision, a ticket, a one-pager, a full PRD, and the BRD plus PRD plus FRD stack, by stakes, audience, and reversibility. Defaulting to the heaviest artifact is a real failure mode; so is writing a ticket for a quarter of work. Then open the stage's template in `templates/`. Its three-line header names the stage and gate it feeds, the knowledge card behind it, and the skill or agent that drives it.
5. **Read the knowledge card** the header links before filling the template. The card says when the method misleads; that is the part that prevents bad output.
6. **Fill the template, then take it to its gate** in [os/STAGE-GATES.md](os/STAGE-GATES.md). Report which boxes pass and which do not. Never declare a gate passed; a named human signs it.

## Directory map

| Directory | Contents | You may |
|---|---|---|
| `os/` | The loop, the gates, the walkthrough, the document-weight decision, the workspace convention | Read; quote gate checklists back to the user |
| `knowledge/` | 10 canon cards plus index, each with named attribution | Read; cite cards in drafts |
| `templates/` | Fill-in artifacts for every stage, plus the `ai/` overlay | Copy out and fill; never edit the templates themselves |
| `skills/` | Procedures: ai-prd, roadmap-builder, program-premortem, reg-gap-check, feedback-synthesis | Follow when routed |
| `agents/` | Role instruction files (see below) | Adopt one role per run |
| `system/` | Boot and role prompts for file-less chat models | Read; not for you, you have file access |
| `routing/` | OmniRoute tier config | Read when the user runs Method 4 |
| `modules/regulated/` | Byte-exact regulated overlay, hash-pinned | Read and quote ONLY. Never edit, reformat, or reword anything under it |
| `examples/` | Worked, filled templates | Read as reference answers |

## Agent roles

One role per run, from `agents/`:

| File | Role | Hard rule |
|---|---|---|
| [agents/research-agent.md](agents/research-agent.md) | Gathers evidence for discovery templates | Cites sources; never asserts beyond them |
| [agents/drafting-agent.md](agents/drafting-agent.md) | Fills one named template per run | Marks every unknown as an open field; never invents numbers |
| [agents/validation-agent.md](agents/validation-agent.md) | Checks a draft against its template and gate | Reports misses; does not rewrite |
| [agents/red-team-agent.md](agents/red-team-agent.md) | Attacks a draft as a hostile stakeholder or attacker | Uses `templates/ai/red-team-review.md` when the product contains a model |
| [agents/hermes-agent.md](agents/hermes-agent.md) | Routes Hermes task types onto this repo | Per its own routing table |

## Gate rules (non-negotiable)

- A stage is not done until its gate checklist in `os/STAGE-GATES.md` is filled in and signed by a human. You verify and report; you do not sign.
- Never invent a number, a name, a citation, or an interview quote to make a field look complete. "Open: owner needed" is a valid field value. A plausible fabrication is the one output this system is built to prevent.
- Never skip a stage because the user is in a hurry. Say which gate the request is jumping and what the skip risks, quoting the gate's own warning.
- Regulated products: Gate 2 and Gate 5 include the regulated module's checks. Refuse to paraphrase or invent regulator text; quote `modules/regulated/` files verbatim or point to the primary source they cite.

## Tool expectations

- **Read and edit files; prefer editing a copied template over generating a document from scratch.** The template's guidance comments are the procedure.
- **Keep HTML guidance comments intact** in any copy you fill for a user, until the user asks to strip them for publication.
- **Run the quality gate** (`python3 lint.py --os` at repo root) after any change to repo files, and before telling the user the tree is consistent.
- **Do not write into `templates/`, `knowledge/`, `os/`, or `modules/regulated/`** on a normal product run. Product artifacts belong in the user's own workspace, laid out per [os/PRODUCT-WORKSPACE.md](os/PRODUCT-WORKSPACE.md): one folder per product, one subfolder per stage, filled copies keeping the template's file name. Use `examples/` only when the user wants a worked example kept in this repository.
- **Model routing is not your concern** unless the user invokes Method 4; then read [routing/README.md](routing/README.md) and respect the tier doctrine.
