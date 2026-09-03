# Five Whys and Fishbone

Based on the ideas of Taiichi Ohno, from Toyota Production System (1978, English edition 1988), and of Kaoru Ishikawa, whose cause-and-effect diagram dates from the 1960s and appears in Guide to Quality Control (1968). Explained here in this repository's own words.

## What it is for

Two root-cause tools for two shapes of failure. Five whys walks one chain from a symptom to a cause you can change, one verified step at a time; it suits a failure with a single line of causation. The fishbone lays out every condition that had to be true, grouped by branch, and suits a failure with several contributing causes, which is most incidents. Both enforce the same rule: a root cause is something you can change. "Human error", "the vendor", and "bad luck" are not root causes; they are the places where the whys stopped early. The decision they improve is which corrective action actually prevents the next occurrence.

## Run it when

- Filling section 3 of an incident postmortem, before anyone proposes an action
- A metric dropped and the first explanation offered was a person
- A defect has recurred, which means the last fix addressed a symptom
- A gate failed and the team wants to know why the plan did not see it coming

**Skip it when:** the cause is already documented and undisputed. "The deploy pipeline had no canary stage" needs a ticket, not a workshop, and five whys applied to an external outage produces philosophy about cloud regions.

## Inputs you need first

- The timeline from the [incident postmortem](../../templates/operate/incident-postmortem.md), section 1, built from logs and chat, not memory
- The effect stated as an observation with a number, not an interpretation
- The people who were there, and a facilitator who was not
- The rule, agreed aloud before starting: no names in any cause cell

## The worksheet

### Five whys

| Level | Why did it happen? (one cause, stated as a checkable fact) | Evidence (log, document, quote) | Can we change this? | If yes, the change |
|---|---|---|---|---|
| Effect | | | | |
| Why 1 | | | | |
| Why 2 | | | | |
| Why 3 | | | | |
| Why 4 | | | | |
| Why 5 | | | | |

Rules. Stop when the answer is a process, tool, design, or policy that you can change and that would have broken the chain; that may arrive at why 3 or need why 7. Every cell must be verifiable, not merely plausible. When a why has two true answers, do not pick the convenient one: record both, and move to the fishbone.

### Fishbone

Branches: process, people (roles, training, load; never names), tooling, data, design, environment (vendors, timing, load), measurement (alerts, definitions, dashboards).

| Branch | Contributing cause (a condition that had to be true) | Evidence | Changeable? | Weight (1 to 3) |
|---|---|---|---|---|
| Process | | | | |
| People | | | | |
| Tooling | | | | |
| Data | | | | |
| Design | | | | |
| Environment | | | | |
| Measurement | | | | |

Weight: 3, the failure was impossible without it; 2, it made the failure much more likely or much worse; 1, it contributed at the margin. Decision rule: weight 3 and changeable becomes a corrective action; weight 3 and not changeable becomes a control that detects it earlier; weight 1 is recorded and not actioned.

### The root cause test

A candidate passes when all four hold: it is something the team can change; changing it would have prevented this instance; changing it would prevent the class of failure, not just this case; it is stated without a person's name.

## Reading the result

A chain that ends in a person's decision has stopped one why early; ask what made that decision reasonable on the day. A chain that ends in "we lacked time" has also stopped early; ask what consumed the time and who decided the trade. A fishbone with every weight at 3 has not been weighted. A fishbone with nothing under measurement is suspicious, because most incidents include a signal nobody was watching. The output is one corrective action per weight-3 cause, each with an owner, a due date, and a verification method, copied into postmortem section 5.

## ILLUSTRATIVE example

Invented incident at Ledgerline: over one week the expense-report copilot filed 380 meal lines as client entertainment, and accounts payable caught them after manager approval.

| Level | Cause | Evidence | Changeable? |
|---|---|---|---|
| Effect | 380 misfiled lines corrected after approval | AP correction log | |
| Why 1 | The category model's confidence threshold was lowered from 0.85 to 0.70 in a release | Release note | yes |
| Why 2 | The change was made to raise the auto-fill rate the team's key result tracked | OKR sheet | yes |
| Why 3 | The key result had no guardrail on post-approval corrections | OKR sheet, guardrails section empty | yes |
| Why 4 | Corrections were not in the metrics review because the AP system emitted no events | Analytics spec, section 2 | yes |
| Why 5 | The AP integration sat in "phase 2" with no owner or date | Analytics spec | yes |

Two whys had second answers, so the fishbone was run. Measurement, weight 3: no alert on category-distribution shift. Process, weight 3: the threshold change shipped without the finance controller, who is C on model changes in the RACI. Data, weight 2: the training set over-represented the sales team's entertainment spend. Corrective actions: a corrections guardrail on the key result (owner: copilot PM), AP events instrumented (owner: data engineer), and a rule that threshold changes need the controller's review, verified by a blocked test change.

## The trap

The convenient chain. With one line of whys, the team follows the branch that leads to the fix it already wanted (more test coverage, a bigger training set) and never writes down the branch that indicts its own key result. The example above would have ended at "the training data was skewed" and shipped a data fix, and the same incident would have recurred the next time a metric rewarded auto-fill. When a why has two true answers, both are recorded, and the branch not followed is named in the postmortem so a reader can see the choice.

## Feeds

- [Incident postmortem](../../templates/operate/incident-postmortem.md), section 3 (contributing causes) and section 5 (corrective actions)
- [Operational readiness review](../../templates/operate/operational-readiness-review.md), section 6, where verified actions land
- [Risk register](../../templates/execution/risk-register.md): a weight-3 cause that is not yet fixed is an open risk
- [Retrospective](../../templates/execution/retrospective.md), for the team-side learning after the system-side analysis
- The [postmortem facilitator skill](../../skills/postmortem-facilitator/SKILL.md) drives this worksheet
- OPERATE stage, feeding [Gate 6: outcomes verified](../../os/STAGE-GATES.md)
- Method background: [knowledge index](../../knowledge/INDEX.md); no card covers root-cause analysis, so the sources above are the reference
