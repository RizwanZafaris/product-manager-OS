# Worked Examples

Four examples. Two take one fictional product, an expense-report copilot at a fictional mid-market software company, through the front half of the [operating loop](../os/OPERATING-LOOP.md). The third takes the templates in the other direction: onto a product that was already live, already messy, and already carrying nine years of undocumented decisions. The fourth is a transcript rather than a filled template: the Conductor interviewing a PM, shown at the two moments interviews earn their keep, a vague answer challenged into evidence and a stage advance refused with the gate checklist as the reason. Read them before filling the templates: a template shows the questions, an example shows what an answer that survives a gate review looks like, including the places where the honest answer is a gap with an owner.

Everything in these examples is invented. The company, the people, the interview counts, and every number are fiction built to illustrate the format. Nothing here is evidence about any real product, and none of the figures are targets to copy.

| Example | Template it fills | Stage and gate |
|---|---|---|
| [expense-copilot-discovery.md](expense-copilot-discovery.md) | [templates/discovery/discovery-document.md](../templates/discovery/discovery-document.md) | DISCOVER, taken to Gate 1 |
| [expense-copilot-prd.md](expense-copilot-prd.md) | [templates/definition/prd.md](../templates/definition/prd.md) | DEFINE, taken to Gate 2 |
| [checkout-modernization-brownfield.md](checkout-modernization-brownfield.md) | Extracts from problem framing, competitive analysis, PRD, data model, and the decision log | Entered mid-flight, currently at Gate 4 |
| [conductor-transcript.md](conductor-transcript.md) | [templates/execution/state.md](../templates/execution/state.md), plus the Gate 1 checklist from [os/STAGE-GATES.md](../os/STAGE-GATES.md) | DISCOVER into DEFINE, refused once at Gate 1 |

The brownfield example exists because clean examples teach the easy case. It shows a reconstructed Gate 1 labeled as reconstructed, an out-of-scope table doing the load-bearing work, a coupling the team wrote into the architecture rather than designing around, and one decision that was made in April and reversed in May, with both log entries kept.

## How these were produced

The first three follow Method 1 from the README: the template was copied unchanged, every field was filled by hand, and the exit gate at the bottom was walked box by box. No AI runtime was involved, which is the point; the documents stand on their own. The conductor transcript is the deliberate exception: it illustrates an interactive runtime driving the interview, and every STATE.md excerpt in it was produced by the rules the transcript itself demonstrates. The PRD cross-references the discovery document the way a real Gate 2 artifact cites its Gate 1 evidence, and because the product contains a model, it points into the AI overlay under [templates/ai/](../templates/ai/eval-spec.md) for the parts a conventional PRD cannot carry.

## The regulated worked example

A third, fully worked example exists for teams under a financial regulator: the dispute-summary PRD inside the regulated module, at `modules/regulated/examples/dispute-summary/PRD.md`. It is a byte-exact copy from its canonical source repository and is never edited here; the module's own README states the policy.
