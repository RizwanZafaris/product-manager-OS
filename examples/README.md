# Worked Examples

Ten examples. Two take one fictional product, an expense-report copilot at a fictional mid-market software company, through the front half of the [operating loop](../os/OPERATING-LOOP.md). The third takes the templates in the other direction: onto a product that was already live, already messy, and already carrying nine years of undocumented decisions. The fourth is a transcript rather than a filled template: the Conductor interviewing a PM, shown at the two moments interviews earn their keep, a vague answer challenged into evidence and a stage advance refused with the gate checklist as the reason. The remaining six fill a framework worksheet or a planning template on the same copilot; the section after the table says why they exist. Read them before filling the templates: a template shows the questions, an example shows what an answer that survives a gate review looks like, including the places where the honest answer is a gap with an owner.

Everything in these examples is invented. The company, the people, the interview counts, and every number are fiction built to illustrate the format. Nothing here is evidence about any real product, and none of the figures are targets to copy.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [expense-copilot-discovery.md](expense-copilot-discovery.md) | [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md) | DISCOVER, taken to Gate 1 |
| [expense-copilot-prd.md](expense-copilot-prd.md) | [templates/definition/prd.md](../templates/definition/prd.md) | DEFINE, taken to Gate 2 |
| [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md) | Extracts from problem framing, competitive analysis, PRD, data model, and the decision log | Entered mid-flight, currently at Gate 4 |
| [conductor-transcript.md](conductor-transcript.md) | [templates/execution/state.md](../templates/execution/state.md), plus the Gate 1 checklist from [os/STAGE-GATES.md](../os/STAGE-GATES.md) | DISCOVER into DEFINE, refused once at Gate 1 |
| [ledgerline-jtbd-job-map.md](ledgerline-jtbd-job-map.md) | [frameworks/discovery/jtbd-job-map.md](../frameworks/discovery/jtbd-job-map.md) | DISCOVER, feeds Gate 1 |
| [ledgerline-business-case.md](ledgerline-business-case.md) | [templates/planning/business-case.md](../templates/planning/business-case.md) | DISCOVER and the PLANNING track, feeds Gate 1 and the roadmap |
| [ledgerline-kano-survey.md](ledgerline-kano-survey.md) | [frameworks/discovery/kano-survey.md](../frameworks/discovery/kano-survey.md) | DEFINE, feeds Gate 2 through the PRD scope table |
| [ledgerline-strategy-kernel.md](ledgerline-strategy-kernel.md) | [frameworks/strategy/strategy-kernel.md](../frameworks/strategy/strategy-kernel.md) | PLANNING track, feeds the product strategy |
| [ledgerline-rice-scoring.md](ledgerline-rice-scoring.md) | [frameworks/prioritization/rice-scoring-sheet.md](../frameworks/prioritization/rice-scoring-sheet.md) | PLANNING track, feeds the roadmap |
| [ledgerline-north-star-tree.md](ledgerline-north-star-tree.md) | [frameworks/metrics/north-star-input-tree.md](../frameworks/metrics/north-star-input-tree.md) | PLANNING track, feeds the north star sheet and the OKRs |

The brownfield example exists because clean examples teach the easy case. It shows a reconstructed Gate 1 labeled as reconstructed, an out-of-scope table doing the load-bearing work, a coupling the team wrote into the architecture rather than designing around, and one decision that was made in April and reversed in May, with both log entries kept.

## Why the framework examples exist

A worksheet shows the form. An example shows a filled form: the declarations made before any scoring, the arithmetic done on the page where a reader can check it, the decision rule applied at the point where it actually bites (a Kano tie-break, a RICE row that scores low against the declared goal and is still worth building, a payback that fails at half the assumed adoption), and the cells left open with an owner because the invented team had no evidence for them. The six share one product and one set of invented facts, so a figure in the business case traces to the discovery document and a backlog row in the RICE sheet to a Kano class. A naming note: these six call the company Ledgerline, the repository's standard name for the invented company, and refer to people by role; the earlier pair calls the same company Fernwood Software and gives its people names. Same product, same interviews, same figures.

## How these were produced

The first three follow Method 1 from the README: the template was copied unchanged, every field was filled by hand, and the exit gate at the bottom was walked box by box. No AI runtime was involved, which is the point; the documents stand on their own. The conductor transcript is the deliberate exception: it illustrates an interactive runtime driving the interview, and every STATE.md excerpt in it was produced by the rules the transcript itself demonstrates. The PRD cross-references the discovery document the way a real Gate 2 artifact cites its Gate 1 evidence, and because the product contains a model, it points into the AI overlay under [templates/ai/](../templates/ai/eval-spec.md) for the parts a conventional PRD cannot carry. The six framework examples were filled the same way as the first three: worksheet copied, every input invented and labeled ILLUSTRATIVE, the arithmetic done by hand, and any cell without evidence marked open with an owner rather than filled by guesswork.

## The regulated worked example

A third, fully worked example exists for teams under a financial regulator: the dispute-summary PRD inside the regulated module, at `modules/regulated/examples/dispute-summary/PRD.md`. It is a byte-exact copy from its canonical source repository and is never edited here; the module's own README states the policy.
