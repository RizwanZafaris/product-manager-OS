# Design System Audit: Expense Copilot screens against Ledgerline UI

Fills [frameworks/design/design-system-audit.md](../frameworks/design/design-system-audit.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the copilot is the fictional product used across this repository, the shared library ("Ledgerline UI") and its inventory are ILLUSTRATIVE figures built so this file and the [design data sheet](ledgerline-design-sheet.md) check against each other, and no count below is a benchmark for any real design system. The journey is silent on a design system: no N row, no S row, no D row names one, so every figure here traces only to the design data sheet's LD1 to LD4, which the sheet states are sheet facts invented for this lane. See the [examples index](README.md).

**Owner:** the design-system lead (LD-P2) · **Date:** 2027-01-18 · **Stage at the time:** DESIGN, feeding [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md)

## What it is for

The copilot's five screens (LEDGERLINE-S1 through S5, with S6 proposed under D7) were built against Ledgerline UI, the company's one shared component library, and this audit is where "we mostly use the system" becomes a number a Gate 3 reviewer can check: how much of the shipped interface is a system component, how mature the library is on its own two ladders, whether its governance is in place, and which failure patterns are already visible. It runs here because the copilot shipped three one-off components ahead of the library (LD4) and Gate 3 needs to know whether those are reasoned snowflakes or unrouted one-offs before the usage-metric screen (S6) adds a fourth.

## Run it when

- Gate 3 needs an evidence-backed adoption number instead of the design-system lead's impression from the library register
- A tech-debt conversation about "design system drift" keeps citing the copilot's one-off components with no inventory behind the claim
- The library has been running long enough, in daily use across three product surfaces plus the add-on, that governance is worth checking rather than assumed

**Skipped here:** step 6, choosing a foundation. Ledgerline UI is the organization's one mandated library across the Starter, Business and Enterprise surfaces and the add-on; there is no candidate foundation under consideration for this product, so step 6 does not run.

## Inputs you need first

- The screens in scope: LEDGERLINE-S1 (activation and charge confirmation), S3 (the drafted-line-item review with the confidence-flag chip), and S5 (the approval-rate tile, reused on the price step), reachable as the shipped build, not a Figma file
- The library's own documentation: the register [LD2](ledgerline-design-sheet.md) cites, current at 2027-01-18
- The design-system lead (LD-P2), who owns the library register and answers the four governance questions below
- No candidate shortlist, since step 6 is skipped

## The worksheet

### 1. Interface inventory per screen

<!-- Full instance-by-instance tagging is not reproduced here; the design
     data sheet (LD2, LD3, LD4) already carries the counts this audit reads
     from, dated 2027-01-10 for the token pass and 2027-01-18 for the
     register. This section names the tagged deviations and snowflakes by
     row rather than re-listing every system-component instance. -->

| Screen | Element | Tag | System component (name and version), if applicable | Notes |
|---|---|---|---|---|
| LEDGERLINE-S1 | Charge-confirmation step | Snowflake, unreasoned | Ledgerline UI has no confirmation-with-charge pattern (LD2 gap) | Shipped as a one-off ahead of the library (LD4) because no pattern existed to build against, not because the team chose to keep it product-specific; no system component was detached or overridden, so the worksheet's own definition places this as a snowflake, not a deviation, and it is routed to the tech-debt register below |
| LEDGERLINE-S3 | Confidence-flag chip | Snowflake, unreasoned | Ledgerline UI has no confidence-flag chip pattern (LD2 gap) | Shipped as a one-off ahead of the library (LD4) for the same reason as the charge-confirmation step above; the screen-reader failure the 2026-11-17 usability round found (LD8) sits on this exact chip |
| LEDGERLINE-S1 | Per-seat price row | Snowflake, reasoned | Ledgerline UI has no per-seat-versus-per-usage price toggle pattern (LD2 gap) | Reused, unchanged, for the per-report price row proposed under D7 (LD4); kept as a snowflake rather than promoted, since a price-toggle pattern serving two pricing models at once is not yet a Ledgerline UI concern beyond this one product |
| LEDGERLINE-S1, S3, S5 | Every other styled property | System component | Ledgerline UI, per the library register (LD1) | 94 percent of styled properties on the copilot's screens reference a library token (LD3); the 6 percent that do not are exactly the three gap components above |

### 2. Arithmetic

**Coverage** = 94 percent of styled properties reference a Ledgerline UI token (LD3), read by property, not by instance count, since the design data sheet's audit (2027-01-10, the design-system lead) was run that way; the distortion the worksheet names, container components dominating visual area, does not apply the same way to a token-coverage pass, but the same caveat holds for state coverage: LD3's pass does not say which states (empty, loading, error) were inventoried, so a hover or error state on the confidence-flag chip could sit outside the 94 percent without the number moving.

**Deviation rate** = 0. None of the copilot's three one-off components started life as a Ledgerline UI component that was then detached, overridden, or hand-modified, and none duplicates a system component instead of importing it, the worksheet's own definition of a deviation. All three fill outright gaps in the library (LD2: no confirmation-with-charge pattern, no confidence-flag chip pattern, no per-seat-versus-per-usage price toggle), so step 1 tags all three as snowflakes, not deviations. Two are unreasoned, shipped ahead of the library only because no pattern existed to build against: the charge-confirmation step and the confidence-flag chip. Counted as two distinct decisions, not three times the number of screens they appear on, per the worksheet's own caveat against treating one copied decision as many; both are routed to the tech-debt register in step 2's action below. The third, the per-seat price row later reused unchanged for the per-report row, is reasoned: kept out of the library by the design-system lead's own call, not a debt item.

**Deprecated instances** = 2 components at LD2 are deprecated with a removal date of 2027-04-01; none of the three copilot screens in scope uses either deprecated component, so the deprecated-instance count on this inventory is 0. The library register's pass (2027-01-18) is 8 days after the token-coverage pass (2027-01-10), close enough that neither count is read as stale against the other.

### 3. Maturity

**Adoption ladder:**

| Level | What it asks | Score (0 to 2) |
|---|---|---|
| Principles | Does the team's design and build process actually apply the system's stated design principles as an evaluative lens, not just cite them? | 1: the copilot's screens were built by the same team that maintains the library, so principles were applied by habit rather than cited as an evaluative lens in a design review; no design-critique row (the [design critique](ledgerline-design-critique.md) outcome log) references a Ledgerline UI principle by name |
| Guidance | Do the product's components follow the system's published UX guidance, whether or not the product uses the system's own code? | 2: every screen in scope follows the library's published UX guidance where a pattern exists; the three gap components were built as one-offs precisely because no guidance existed yet to follow |
| Code | Does the product use the system's design tokens and component code directly, with overrides kept to the settings the system exposes for that purpose? | 2: 94 percent token coverage (LD3), overrides limited to the three logged gaps rather than hand-modified system components |

**System maturity stage:** 3, surviving the teenage years. The library is in daily use across three product surfaces plus the add-on (LD1); the open question this audit surfaces is not whether to adopt it but whether to promote the three one-off gap components into it before a fourth (a usage-versus-seat price toggle for S6) ships the same way.

### 4. Governance

See [knowledge/design/design-systems-and-tokens.md](../knowledge/design/design-systems-and-tokens.md), Governance section, for what each row means before scoring it.

| Governance item | Score | Evidence |
|---|---|---|
| Team model named | 2 | Centralized: the design-system lead (LD-P2) owns the library register and its inventory, named in the design data sheet's cast table |
| Contribution path exists and is known | 1 | The gap log (LD2, LD4) is where a logged gap lives, but the copilot team shipped all three one-off components before routing any of them through it; the path exists, the copilot team did not use it first |
| Lifecycle statuses in use | 2 | LD2's register states stable, trial and deprecated counts with a removal date attached to the deprecated pair, visible at the point of the library register rather than only in a changelog |
| Issue split in use | 0 | The gap log (LD2, LD4) records gaps but does not distinguish a bug, a visual discrepancy, a feature request and a product-owned recipe; all three copilot one-offs sit in the same undifferentiated "logged gap" list |
| Deprecation route with a warning-only phase | 1 | The two deprecated components carry a stated removal date (2027-04-01) ahead of removal, a warning-only phase in form, but nothing on the copilot's own three screens surfaces that date, since neither deprecated component is in scope here to test it against |

Governance total: 6 of 10.

### 5. VanHouten failure-pattern diagnostic

| Pattern | What it looks like | Present / partly / absent | Evidence |
|---|---|---|---|
| No shared, contextual purpose | "Improve the UX of our products" stands in for a purpose nobody can act on; no answer to why this org, why now | Absent | The library register (LD1) names a specific scope, one library shared across three surfaces and the add-on, not a vague "improve the UX" mandate |
| Overbuilding, or scaling too early | The system tried to cover every case for every team (scaling vertically) before proving the smallest shared set works for one team (scaling horizontally) | Absent | 41 components published stable against 6 in trial (LD2), a ratio that reads as steady growth, not an attempt to cover every case before proving the smallest shared set |
| Inability to decide and move | Foundational choices (color, type, a component's first shape) stay open for months because every decision is treated as equally weighty | Partly present | The three gap components (LD4) sat as one-offs long enough that the copilot shipped and reused one of them (the price row) a second time before either was routed for promotion |
| Lack of clear ownership and dedicated resources | The system's champion maintains it as an unstaffed side project on top of another full-time role | Absent | A named lead (LD-P2) owns the register and audits token coverage on a stated date (LD3); this is not an unstaffed side project |
| Lack of cultural alignment | Teams comply with the system on paper while quietly building around it, because nobody outside the system team was brought into why it exists | Partly present | The copilot team built three patterns the library did not have rather than filing a gap request first; the gap log exists and the team used it to log the gaps after the fact, not before building around them |

Two patterns marked partly present, none marked fully present: below this worksheet's two-present threshold, but the two partly-present rows point at the same root as the governance gap above, no issue-type split and no contribution-first habit, worth a fix before the fourth one-off (a price-model toggle for S6) repeats the pattern.

### 6. Choosing a foundation

Skipped. Ledgerline UI is the organization's one mandated library across every surface the copilot's screens run on; there is no candidate foundation under consideration for this product.

## Reading the result

94 percent coverage and a governance total of 6 of 10 read differently once step 3 sets the frame: a stage-3 library, in daily use across three surfaces plus the add-on, is expected to carry high coverage, and it does, but a governance score just above half predicts exactly what step 1 already shows, three one-off components shipped ahead of the library rather than routed through the contribution path that scored a 1. The two partly-present VanHouten patterns (decide-and-move, cultural alignment) do not clear this worksheet's two-pattern threshold on their own, but they name the same mechanism: the copilot team builds first and logs the gap after, which is how a fourth one-off for S6's price-model toggle would ship the same way without a decision changing between now and then. The outcome this audit is built to produce, two unreasoned one-offs routed rather than left as an accumulating tab, is the finding, not the 94 percent.

Outcome recorded: the charge-confirmation step and the confidence-flag chip (LD4) each become one [tech-debt-register](../templates/execution/tech-debt-register.md) row, since neither started as a system component that was detached or overridden, so neither qualifies as a deviation the worksheet would route through component-spec on that basis, and the gap logged against each (LD2) is stated as a fact about the system, not as a request:

| Item (fact about the system) | Interest (cost of diverging, per quarter) | Owner | Notes |
|---|---|---|---|
| Ledgerline UI has no confirmation-with-charge pattern; the copilot's charge-confirmation step (LEDGERLINE-S1) duplicates that logic outside the library | To be estimated by the design-system lead (LD-P2) before the next register review | Design-system lead, LD-P2 | Candidate for a future component-spec proposal if the gap is judged worth closing before S6 ships a fourth one-off |
| Ledgerline UI has no confidence-flag chip pattern; the copilot's confidence-flag chip (LEDGERLINE-S3) duplicates that logic outside the library | To be estimated by the design-system lead (LD-P2) before the next register review | Design-system lead, LD-P2 | Carries the LD8 screen-reader failure; the higher-priority row of the two |

The per-seat price row, reused unchanged for the per-report row, stays a reasoned snowflake rather than a register row: the design-system lead's own read is that a single-product price-toggle pattern is not yet worth the library's shared surface, a deliberate choice rather than an accumulating debt.

## The trap

Reading 94 percent coverage as "the copilot is a system-compliant product, done." The number says how much of the interface references a token; it says nothing about the three components that do not, and one of those three sits exactly where the 2026-11-17 usability round found its worst failure, the confidence-flag chip a screen-reader participant could not locate (LD8). A high coverage figure and an unrouted one-off can point at the same screen at once; this audit reads them together rather than letting the coverage number stand in for a clean bill on the screen it comes from.

## Feeds

- [Component spec](../templates/architecture/component-spec.md): a future proposal for the charge-confirmation step or the confidence-flag chip, if the design-system lead judges either LD2 gap worth closing before S6 ships a fourth one-off; not written yet
- [Tech debt register](../templates/execution/tech-debt-register.md): the charge-confirmation step and the confidence-flag chip become two register rows now, each tracing to its LD2 gap; the per-seat price row stays a reasoned snowflake and gets no row
- [Program charter](../templates/planning/program-charter.md): Ledgerline UI, 94 percent coverage, governance 6 of 10, is the design-system dependency line a program charter for the S6 usage-metric build would name
- DESIGN stage, feeding [Gate 3: architecture and risks reviewed](../os/STAGE-GATES.md)
- Method background: [Design systems and tokens](../knowledge/design/design-systems-and-tokens.md)
