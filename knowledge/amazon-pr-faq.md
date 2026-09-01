# Amazon PR/FAQ

Based on Amazon's working backwards practice as described by Colin Bryar and Bill Carr in Working Backwards (2021).

## The essence

Before Amazon builds a product, someone writes the press release announcing it, dated for launch day, one page, in plain customer language: the customer, the problem, how the product solves it, why the customer should care. Attached is the FAQ, several pages of the hardest questions anyone inside or outside the company could ask, answered honestly: what it costs, what it depends on, what could kill it, what the skeptical customer says, what the skeptical CFO says.

The mechanism is deliberate inversion. Most products are built forward, from a capability the company has toward a customer it hopes exists. Working backwards starts at the moment of customer value and refuses to proceed until that moment is vivid and worth the trip. If the press release is boring, the product will be boring; it is vastly cheaper to learn that in a document review than in a launch. Drafts go through many revisions, and killing the idea at PR/FAQ stage is a success of the process, not a failure of the author.

The FAQ is where the intellectual honesty lives. The press release sells; the FAQ confesses. A PR/FAQ with a glowing PR and a thin FAQ has done half its job, the cheap half.

## When to use it

- At discovery stage, before a line of the PRD exists, as the sharpest test of whether the problem and its resolution can be stated in customer language at all.
- When writing the business case: the FAQ's hard questions are the same questions the BRD's sponsor will ask, and it is better to meet them on paper first.
- When a large initiative feels vaguely justified, as a kill test: if six revisions cannot produce an exciting press release, the initiative is the problem.

**Skip it when:** nothing customer-facing changes. A platform migration, an internal tool, or a debt paydown has no press release that is not fiction, and writing one anyway teaches the team to produce marketing copy for engineering work. A system design document and a decision record do that job.

## The trap: selling a decision already made

The instrument assumes the decision is still open. Write the PR/FAQ after the initiative has a budget line, an assigned team, and an executive sponsor's name on it, and the document inverts into marketing collateral for an internal audience: the press release gets polished, the FAQ's hard questions get softened into setups for reassuring answers, and review becomes a table read. The tell is the FAQ. A genuine one contains at least one question the authors cannot yet answer well and says so; a laundering one answers everything smoothly. If no PR/FAQ in your organization has ever killed the idea it described, the tool is being used as a ribbon, and the working backwards is theater performed after working forwards finished.

## Used by

- [Discovery document](../templates/discovery/discovery-document.md)
- [BRD](../templates/definition/brd.md)
- [PRD](../templates/definition/prd.md)
- [PR/FAQ](../templates/definition/prfaq.md)
