# Roadmap: Expense Copilot

Fills [templates/planning/roadmap.md](../templates/planning/roadmap.md). Everything here is invented: Ledgerline is the fictional mid-market software company used across this repository, and this roadmap is the last of the three DEFINE-stage planning documents in the internal-v1 chain the [Expense Copilot journey](expense-copilot-journey.md) indexes, drafted after the [vision](expense-copilot-vision.md) and [product strategy](expense-copilot-product-strategy.md). Every number, date and id below is ILLUSTRATIVE, carried from that journey's own data sheet (V5, V8 to V16) and from [ledgerline-journey.md](ledgerline-journey.md)'s N16, so it can be checked against the strategy this roadmap follows and against the PRD drafted alongside it. See the [examples index](README.md).

**Owner:** Maya Chen, Product Manager · **Last updated:** 2026-08-25 · **Review cadence:** at each remaining gate (Gate 2, Gate 3, Gate 5)
**Linked OKR sheet:** none for this internal build. OKR instances for the internal v1 are out of scope for this chain; the three objectives this roadmap serves are the PRD's own, not a separate OKR sheet.

## Preamble: read this before the tables

> **This roadmap manages expectations, not delivery dates.** Only Now is a commitment, and it is a commitment to the work, not to a date. It says what we are working on now, what we expect to pick up next, and the directions we are holding open for later. It is not a delivery contract and no date on it is a promise.
>
> **Now** is committed and in flight. Confidence is high, and if something here slips you will hear it from us before you notice it yourself.
>
> **Next** is shaped and planned, not started. The order can change when evidence changes. Treat anything here as likely, not scheduled.
>
> **Later** is a set of directions, not features. Anything in Later may never ship, and the entries are deliberately imprecise: a specific feature name written a year out becomes a commitment nobody made.
>
> Things move backward as well as forward, and items get killed. The parked-and-killed table below is part of the roadmap, not an appendix to it. If a decision here affects something you are counting on, ask, and you will get the real answer rather than the reassuring one.

## Now (committed, in flight or next up)

| ID | Theme | Initiative | Owner | Outcome it serves (objective ref) | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|---|---|
| R-1 | Close DEFINE | Vision and product strategy converge with this roadmap, the PRD and the acceptance criteria at Gate 2 on 2026-08-28 | Maya Chen | Unlocks DESIGN; every PRD objective needs a signed scope before build starts (objectives 1 to 3) | August 2026 | 80% | none blocking; vision and strategy are already drafted | In progress |

## Next (planned, shaped, not yet committed)

| ID | Theme | Initiative | Owner | Outcome it serves | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|---|---|
| R-2 | Prove the receipt pipeline | ADR-0001: one receipt per model call, matched to one uploaded photo or one forwarded-email attachment (functional scope rows 1 and 2) | Priya Nair | objective 1, first-submission approval from 62% toward 80% (N3, N4); objective 2, filing time from 25 minutes toward under 10 (N5) | September 2026 | 62% | Gate 2 SIGNED | Shaping |
| R-3 | Data and interface contracts | A data model (Receipt, DraftReport, LineItem, CategoryMapping, CorrectionLogEntry) and an API contract across the PRD's six functional-scope rows | Priya Nair | Unblocks build of every functional-scope row; feeds all three objectives at once | September 2026 | 50% | ADR-0001 accepted | Shaping |
| R-4 | Close DESIGN | Dependency and risk registers from a premortem, and the development handoff itself | Maya Chen | A development-ready package at Gate 3, so BUILD starts with no gap in it | September 2026 | 38% | Data model and API contract drafted | Shaping |
| R-5 | Vendor terms | Close the model vendor's no-training clause and the receipt-retention schedule, both open since discovery | legal lead (role only) | Removes the two risks discovery carried into DEFINE; both must close before Gate 5 | before Gate 5, target October 2026 | 30% | the legal lead, with the model vendor | Not started |

## Later (directional themes only)

| Theme | Problem it addresses | Earliest it could enter Next | Signal that would promote it |
|---|---|---|---|
| Ship and learn against Ledgerline's own filers | Objectives 1 to 3 are targets, not results, until the build runs against real reports; the first read on that is an internal metrics review, not part of this chain | October 2026 | Gate 3 REVIEWED AND ACCEPTED, closing DESIGN |
| A reviewed feedback loop for category mappings | Corrections are logged and versioned in v1 but not fed back into suggestions, because the review step a learning loop needs has no owner yet | after go-live | An owner and a design for the review step a learning loop would need |

## Initiative records

Each Now row carries one record. Every figure below is ILLUSTRATIVE, like the rest of this example.

- **ID:** R-1
- **Owner:** Maya Chen
- **Outcome (objective ref):** Unlocks DESIGN: PRD objectives 1 to 3 all need a signed scope before build starts
- **Strategy or OKR ref:** No OKR sheet exists for this internal build; this follows [expense-copilot-product-strategy.md](expense-copilot-product-strategy.md)
- **Evidence ref:** [expense-copilot-problem-framing.md](expense-copilot-problem-framing.md), the framing the three DEFINE documents answer
- **Appetite:** 3 weeks, worth it because this is a review that closes a stage, not a build
- **Dependency IDs:** none
- **Score sheet:** Not RICE scored: closing DEFINE is the gate itself, not a candidate competing for a slot
- **Capacity reservation:** 24 person-days on define squad, reserved in [capacity plan](../templates/planning/capacity-plan.md)
- **Commitment type:** committed
- **Entry rule:** Vision, product strategy, PRD and acceptance criteria all drafted and circulated before the review
- **Exit rule:** 2 signatures on this roadmap's Gate 2 lines, dated 2026-08-28, with the PRD and acceptance criteria carrying the same date
- **Rejected options and override decision:** [expense-copilot-decision-log.md](expense-copilot-decision-log.md), D-2: one receipt per item in v1, multi-receipt capture rejected

## Capacity line

| Team | Period | Plannable (80 percent of net) | Unit | Reserved by Now records | Capacity plan |
|---|---|---|---|---|---|
| define squad | August 2026 | 30 | person-days | 24 | [capacity plan](../templates/planning/capacity-plan.md) |

No filled capacity plan instance exists for this internal build, so the figures are carried here against the blank form rather than copied from a plan of its own.

## Dependency index

| Dependency ID | Deliverable (not a team name) | Owning team | Register row |
|---|---|---|---|
| [DEP-n] | [deliverable] | [team] | [dependency-register.md copy, row n] |

No committed initiative carries a dependency at this roadmap's date. The register opens in DESIGN on 2026-09-08 with DEPV-1 to DEPV-4 ([expense-copilot-dependency-register.md](expense-copilot-dependency-register.md)), and those ids enter this index when a Now row rests on one.

## Quarterly gates

| Period | Entry gate (what must be true to start) | Exit gate (a number, not a demo) | Top risks (owner, trigger) |
|---|---|---|---|
| August 2026 | Vision, product strategy, roadmap, PRD and acceptance criteria all drafted and circulated | 2 signatures on this roadmap's Gate 2 lines, dated 2026-08-28 | Acceptance criteria not agreed in time (Maya Chen, any AC still open three working days before the review); the finance sponsor unavailable to sign (Maya Chen, no confirmed slot by 2026-08-26) |

## Defence page

### Highest-scored items not funded

Nothing was scored against R-1, because closing DEFINE is the gate rather than a candidate for a slot. The four shaped items in Next, from the receipt pipeline proof to the vendor terms, are the queue R-1 unblocks; none competes with it for August.

### Funded despite a lower score

None. The only funded item is the stage close itself, and the vendor terms row is pinned by a date rather than a score: the no-training clause and the retention schedule must close before Gate 5 whatever they would have scored.

### What would change this sequence

Two assumptions carry it. First, that Gate 2 signs on 2026-08-28; a slip moves every Next row with it. Second, that one receipt per item is enough for v1 (D-2). Evidence that filers photograph receipts in batches would reopen the parked multi-receipt item and re-sequence the pipeline work.

## Parked and killed

| Initiative | Parked or Killed | Reason | Date |
|---|---|---|---|
| Multi-receipt capture in one photo | Parked | The PRD's functional scope for v1 is one receipt per item; the extraction eval set cannot yet hold a threshold on overlapping receipts in a single frame | 2026-08-25 |

## Change log

| Date | Change | Why | Who decided |
|---|---|---|---|
| 2026-08-25 | First roadmap published, alongside the vision and product strategy, ahead of Gate 2 | DEFINE converges all three planning documents plus the PRD and acceptance criteria for one joint review | Maya Chen |

## How this roadmap fails

| Failure mode | What it looks like | The rule that stops it |
|---|---|---|
| Dates read as promises | A month appears next to an item, and someone downstream is told it as a commitment | The preamble states these are targets, not delivery dates, before any table appears |
| Features with no outcome | Rows of things to build, none tied to an objective or a metric | Every Now and Next row names the objective it serves, referencing the PRD's own three objectives |
| Later is a graveyard | Half the items sit in Later permanently and nobody revisits them | Two rows in Later, each with a specific promotion signal tied to a named gate or a named owner, not a calendar date alone |
| Nothing moves | The same items sit in Now for months while work happens elsewhere | This is a new roadmap with one Now row three days from its own gate; the change log exists to catch drift from here forward |
| Killed work vanishes | An item disappears and later somebody asks what happened to it | Multi-receipt capture is named in the parked-and-killed table with a reason, not silently dropped from the functional scope |
| Confidence set once | The confidence column was filled at planning and never touched again | Confidence is stated per row now; the review cadence re-enters it at each remaining gate |

## Exit gate

This roadmap is fit to share when:

- [x] Every Now and Next initiative carries a stable ID and exactly one accountable owner. R-1 to R-5, owned by Maya Chen, Priya Nair and the legal lead by role; the journey's People section gives the legal lead no personal name, so the role stands in its place
- [x] Every Now initiative has one record under Initiative records. R-1 is the only Now row, and its record carries the appetite, the 24 person-day reservation, the commitment type, the entry and exit rules and D-2, the decision that chose one receipt per item
- [x] The capacity line holds and every period in Now has an entry and an exit gate. 24 person-days reserved against a plannable 30 for August 2026, and August 2026 carries both gates
- [x] Every Now and Next initiative names the objective it serves, and that objective exists in the OKR sheet. No separate OKR sheet exists for this internal build; every row instead names the PRD objective (1, 2 or 3) it serves, which this roadmap's header states explicitly as the substitute
- [x] Confidence is stated per row, and nothing under 70% sits in Now. The one Now row carries 80%; Next rows carry 62%, 50%, 38% and 30%, none of them claimed as Now
- [x] Later contains themes, not dated features. Two rows, each a direction with a named promotion signal, no feature described precisely enough to be quoted back in six months
- [x] Dependencies are named, and each appears in the dependency register. The formal dependency register is drafted later in DESIGN, 2026-09-08; until it exists, this roadmap's own Dependencies column names its gate-sequencing preconditions honestly rather than pointing at a register that is not there yet
- [x] At least one thing has been parked or killed since the last review, or the owner has written why not. Multi-receipt capture is parked, with a reason and a date
- [x] The change log shows the roadmap is alive, not laminated. One entry, dated to this roadmap's own publication; a roadmap with no history yet is not the same as a roadmap that hides one

Product roadmap, approved at Gate 2 by the product owner: Maya Chen, 2026-08-28
Product roadmap, approved at Gate 2 by the engineering lead: Priya Nair, 2026-08-28
