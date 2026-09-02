# SWOT and TOWS

Based on the ideas attributed to Albert Humphrey, from his Stanford Research Institute planning work (1960s; the origin of SWOT is disputed and no single source exists), and of Heinz Weihrich, from "The TOWS Matrix: A Tool for Situational Analysis", Long Range Planning (1982). Explained here in this repository's own words.

## What it is for

SWOT sorts what you know into four boxes: strengths and weaknesses inside the team, opportunities and threats outside it. On its own it produces a list, and a list changes nothing. The TOWS matrix is the second step most teams skip: pair each internal item with an external one and ask what move the pair implies. Four kinds of move come out: use a strength to take an opportunity, fix a weakness to take an opportunity, use a strength to blunt a threat, shrink a weakness a threat would exploit. Run both halves or neither. The output is three moves with owners, which is what a strategy's sequencing section needs.

## Run it when

- At the start of a strategy refresh, to get the known facts on one page before the kernel work
- When a threat is being discussed as news rather than as something with a response
- When a team lists strengths without saying compared to whom

**Skip it when:** the strategy already has a diagnosis with evidence. SWOT is a pre-diagnosis sorting tool; running it after the [strategy kernel](strategy-kernel.md) passes produces a slower restatement of section 1.

## Inputs you need first

- Competitive analysis, sections 4 to 6: the comparator for every strength and weakness (a vendor tool, the current process, doing nothing)
- A [PESTLE scan](pestle.md) or equivalent for the external rows
- Metrics review or discovery evidence for any claim about the product
- Capacity facts: who is on the team and for how long

## The worksheet

### Part 1: SWOT, with rules

<!-- At most four rows per box, ranked. A strength or weakness is relative: name the comparator in the row. An opportunity or threat is external and dated: name the horizon. Every row links evidence; an unlinked row is an opinion and is cut before Part 2. -->

| ID | Strength (internal, relative to [comparator]) | Evidence | Rank |
|---|---|---|---|
| S1 | | | |
| S2 | | | |

| ID | Weakness (internal, relative to [comparator]) | Evidence | Rank |
|---|---|---|---|
| W1 | | | |
| W2 | | | |

| ID | Opportunity (external, horizon in quarters) | Evidence | Rank |
|---|---|---|---|
| O1 | | | |
| O2 | | | |

| ID | Threat (external, horizon in quarters) | Evidence | Rank |
|---|---|---|---|
| T1 | | | |
| T2 | | | |

### Part 2: TOWS, the moves

<!-- Each move cites exactly one internal ID and one external ID. Cost band: S (under a sprint), M (a quarter of one team), L (more). -->

| Cell | Move | Internal ID | External ID | Cost band | Owner | Feeds |
|---|---|---|---|---|---|---|
| SO: strength takes opportunity | | | | | | |
| WO: fix weakness to take opportunity | | | | | | |
| ST: strength blunts threat | | | | | | |
| WT: shrink weakness a threat would exploit | | | | | | |

**Decision rule.** A SWOT row cited by no move is deleted; it was decoration. A move with no internal ID is a wish; with no external ID it is a chore. Of the moves that survive, pick at most three for the period, ranked by external horizon (nearest first) and then by cost band (smallest first). Every threat inside four quarters that gets no move becomes a risk register row with an owner.

## Reading the result

- **Three moves, each cited, each owned.** Feed them into the strategy's sequencing table and the roadmap's Next column.
- **Every move is SO.** The team is only playing offence. Check the threats again; a threat with no ST or WT move is one you have decided to absorb, so say so in writing.
- **The weakness rows all read "small team" and "no budget".** Those are conditions of the stage, not weaknesses relative to a comparator. Replace them with the specific gap the comparator does not have.
- **More than eight moves.** The SWOT was not ranked. Cut to the top two per box and rerun.

## ILLUSTRATIVE example

Invented, for Ledgerline's expense-report copilot; comparator: the vendor expense tool the finance lead priced.

| ID | Row | Evidence (invented) |
|---|---|---|
| S1 | The draft shows the policy line it matched; the vendor tool drafts without one | Vendor demo notes, dated |
| S2 | Twelve interviews and a sponsor who signed the cost of inaction | Discovery document |
| W1 | Extraction on foreign-language receipts unproven; the vendor tool publishes accuracy claims for forty languages | Eval set not yet run |
| O1 | The finance system's vendor opens an API for policy fields next quarter | Vendor roadmap, linked |
| T1 | The finance system's next release may bundle an expense module | Two release notes, a sales conversation |
| T2 | A model provider changed its data-retention terms last quarter | Terms page, dated |

Moves. SO: read policy fields from the finance system's API so the policy line is always current (S1 plus O1, cost M, engineering lead). ST: measure first-submission approval from week one so the bundled module has a number to beat, not a feeling (S2 plus T1, cost S, PM). WO: run the eval set on foreign-language receipts before Gate 2, using the API opening as the deadline (W1 plus O1, cost S, engineering lead). WT: none; W1 against T2 is accepted for the period and recorded as a risk with the vendor-terms clause as its mitigation.

## The trap

The thirty-item SWOT. Every strength is "great team", every threat is "competition", nothing is ranked, and the meeting ends before TOWS begins. The list gets pasted into the strategy appendix and nobody reads it again. The specific failure is a strength with no comparator: "strong extraction" is a feeling until the row says stronger than what, on what evidence. Cap each box at four, require the comparator in the row itself, and do not let the meeting close without Part 2.

## Feeds

- [Product strategy](../../templates/planning/product-strategy.md): section 1 (the situation facts) and section 4 (sequencing takes the moves)
- [Risk register](../../templates/execution/risk-register.md): section 2, every un-moved threat inside four quarters
- [Roadmap](../../templates/planning/roadmap.md): Next column for the chosen moves
- PLANNING track, ahead of the strategy kernel worksheet
- Method background: none in the knowledge layer; the [knowledge index](../../knowledge/INDEX.md) strategy kernel entry is the nearest neighbour, and a SWOT feeds a diagnosis rather than replacing one
