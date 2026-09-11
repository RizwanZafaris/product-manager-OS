# AI Interaction Spec: The Expense Copilot Draft-Report Panel

Fills [templates/ai/ai-interaction-spec.md](../templates/ai/ai-interaction-spec.md). Everything here is invented: Ledgerline is a fictional mid-market software company, the Expense Copilot add-on is the fictional product used across this repository, the people are roles filled by invented names, and every count and dollar figure is ILLUSTRATIVE, carried from the [journey data sheet](ledgerline-journey.md) so it can be checked against the AI overlay, the PRD and the stories this surface implements. See the [examples index](README.md).

**Feature:** The customer-account draft-report panel: it streams the drafted report, shows a per-line confidence flag, links each line to the receipt it was drafted from, lets the filer stop or regenerate, and falls back to a blank, flagged draft when the drafting step abstains or fails.
**Interaction owner:** Maya Chen (P1), Product Manager · **Document date:** 2026-11-06 · **Status:** Signed ahead of the add-on Gate 5 on 2026-11-06; feeds Gate 3 (architecture and risks reviewed, alongside the [agent architecture](ledgerline-agent-architecture.md), [context management](ledgerline-context-management.md), [human approval gates](ledgerline-human-approval-gates.md) and [multi-agent workflow](ledgerline-multi-agent-workflow.md)) and Gate 4 (acceptance criteria met). Carries an annotation of 2026-12-11 on the German-language case, the German-language receipts decision (D9), due 2026-12-11 and not taken.

## 1. Disclosure

The drafting step runs on the pinned document model `docmodel-2026-09-30` (LC16) under the `copilot-extract` and `copilot-policy-match` prompts (LC17). Every line on the panel is either user-entered, model-drafted, or model-suggested and user-accepted; the panel must never blur the first two. All figures ILLUSTRATIVE.

| Surface | How AI involvement is disclosed | Persistent or one-time | Test | Owner |
|---|---|---|---|---|
| The drafted report, per line | Each drafted field carries the label "Drafted by copilot" beside the matched policy line; user-entered values carry no such label | shown every turn | AIA-DISC-01 | Maya Chen (P1) |
| The confidence indicator | A field or suggested category under 0.80 model confidence is flagged for the reviewer (LC22) and carries a distinct visual treatment; the flag, not the model's name, is what the reviewer sees first | persistent while flagged and unconfirmed | AIA-DISC-02 | Maya Chen (P1) |
| The model attribution, once per drafted report | A one-time notice under the report's source line: the drafting ran on the pinned model `docmodel-2026-09-30` (LC16); the vendor is not named in product in this story's artifacts (LC16); naming policy owned by the legal lead | shown once per drafted report | AIA-DISC-03 | Maya Chen (P1) |
| The report-level banner | A banner states this report was drafted by the copilot and is pending filer and reviewer confirmation, and that the model cannot submit, approve or bill (the agent-architecture constraint; see the [agent architecture](ledgerline-agent-architecture.md)) | persistent while the report is unsubmitted | AIA-DISC-04 | Maya Chen (P1) |
| The report-level summary | "Drafted from n receipts; m lines flagged for your review," with n and m derived from the actual receipts and flags, not a bare number | persistent until the report is submitted | AIA-DISC-05 | Maya Chen (P1) |

- Wording used nowhere else for a human-authored equivalent: the exact words "Drafted by copilot." A human-completed line carries no copilot label and no copilot banner. This wording is never used for a human-typed value, so a reader never has to work out which side of the line a value is on.
- What happens when the user cannot tell which parts of a mixed document are generated: every drafted field carries the per-line label (AIA-DISC-01), so a mixed report is legible at the field, not only at the banner. A mixed report with a field that has no label and is not visibly user-typed is a bug that fails AIA-DISC-01, not a reading exercise.

## 2. Generation states

One receipt runs the fixed pipeline in the [multi-agent workflow](ledgerline-multi-agent-workflow.md): entitlement check, extraction, policy match, draft assembly, under three steps per receipt and one retry per step (LC26). The four states below are what the filer sees while that pipeline runs. All figures ILLUSTRATIVE.

| State | Trigger | What the user sees | Can the user act during it | Test |
|---|---|---|---|---|
| Idle | Receipt attached or forwarded, entitlement confirmed, before the first extraction token | "Ready to draft from this receipt." No draft text, no confidence, no citations | yes, start drafting or send to a person | AIA-GEN-01 |
| Generating | Extraction in flight; per-line fields and the policy match stream in | Partial fields arrive line by line, plus a live "drafting" status; the stop control is live from the first token | yes: stop (section 4) | AIA-GEN-02 |
| Abstained | The model withdrew on this receipt: the extract abstained on amount or date because the receipt language is not English (the extract v8 rule, LC17, the RT-07 fix, LC28); or the account policy excerpt is stale beyond 24 hours and the policy-match step abstained (LC25); or a cost cap halted the run | The exact abstain wording, not a generic error: "The copilot could not read this receipt. A blank line item is waiting for you to enter it. This is not an error." For a non-English receipt it names that it could not read the language; for stale policy it says the account policy needs a refresh and alerts Priya Nair's on-call rota (LC25). The draft assembly step hands over a blank, flagged draft | yes: enter the line manually, or send to a person | AIA-GEN-03 |
| Failed | Request errored: timeout, rate limit, or upstream model outage | Distinct wording from an abstain: "The copilot could not reach its model. The line item is blank. You can enter it now, or try drafting again." It offers a retry and a fallback to manual entry, and never implies the model refused | yes: retry, or enter manually | AIA-GEN-04 |

- Streaming partial output is shown before completion: yes, per-line fields stream so the filer can start reading before the policy match lands. The trade-off is that an abstain or failure on a later receipt or step must replace, not append to, the partial output (section 3 worked example and AIA-GEN-03), so a discarded partial never lingers as an error the user has to spot.
- Latency budget before the user sees a state change: first token within 3000 ms, and a stall notice at 8000 ms. Both are ILLUSTRATIVE UI budgets with no source on the data sheet, chosen to surface a stall before the client's own timeout, keyed to the streaming state machine; they are not the model's guaranteed latency, which is not on the sheet.

## 3. Grounding shown at the point of use

The drafting step may state a fact only from a grounding source (the hallucination-controls rule; this section is where each source becomes visible, claim by claim, never in a settings page). All figures ILLUSTRATIVE.

| Claim type | Source shown | Presentation (inline citation, footnote, expandable panel) | What clicking it does | Test | Owner |
|---|---|---|---|---|---|
| A drafted field value (merchant, amount, date, category) | The source receipt image the field was extracted from | An inline receipt marker on the line | Opens the receipt with the matched region highlighted (receipt-line citation) | AIA-GRND-01 | Priya Nair (P2) |
| A matched policy line | The account's own policy excerpt that the policy-match step retrieved | An inline citation beside the matched line | Opens the policy document at that section | AIA-GRND-02 | Priya Nair (P2) |
| A computed or summarized value (receipts per report, cost per drafted report) | The inputs the computation used, for example receipts per report (N10) and the per-receipt quote (N9) | Expandable "how this was calculated" | Shows the inputs and the arithmetic, for example N10 x N9 = 4.2 x $0.22 = $0.92 (N11) | AIA-GRND-03 | Priya Nair (P2) |
| The model confidence flag | The confidence threshold (0.80, LC22) and which fields fell below it | A flagged indicator with an expandable basis (illustrative UI decision, not a data-sheet string) | Names the flagged fields and shows the threshold they were measured against | AIA-GRND-04 | Priya Nair (P2) |

- A claim with no source row here falls under the abstain policy, not a generic footer disclaimer: if the policy-match step found no matching account policy line, it produces no suggestion and flags the field (illustrative UI rule, not a data-sheet string). There is no "the copilot believes" line on this panel, because every claim on it is either cited to a receipt or a policy line or it is a blank flagged line awaiting a person.
- Confidence, when shown, is expressed as a stated basis, never a bare percentage: the flag tells the reviewer which fields fell under the 0.80 threshold (LC22) and which were kept, for example "2 of 6 lines flagged under the review threshold" (an illustrative UI string, not a data-sheet fact). A number such as 0.94 or 86% is never printed as a per-line score on its own. (The measured 86% of extracted fields accepted without edit, N21, is a metric on the review and the dashboard, not a disclosure a filer sees per line.)

## 4. User control affordances

Every row is a way the user overrides or interrupts the drafting. All figures ILLUSTRATIVE.

| Control | Available in which state (section 2) | Effect | Enforcement point | Test |
|---|---|---|---|---|
| Stop generation | Generating | Halts the token stream immediately; the partial output is kept for the lines already completed and discarded for lines not started | client cancels the request, server stops token emission | AIA-CTL-01 |
| Regenerate | Idle, Failed | Re-runs the pipeline on the same receipts with the same prompt version (LC17); the prior draft is kept as a prior version and replaced in the working view | new request, same prompt version | AIA-CTL-02 |
| Edit and resubmit | Idle | The filer edits the receipt attachment or the manual entry before (re)sending; the filer is not editing the model's own output through this control | client | AIA-CTL-03 |
| Accept / reject a suggestion | Wherever the model proposes a value the filer did not type | Accept commits the value as user-entered and clears the reviewer flag (LEDGERLINE-S3); reject discards the model value | client, before the value reaches the reviewer | AIA-CTL-04 |
| Feedback (helpful / not helpful) | After generation completes | Logged with the output, prompt version (LC17), model version (LC16) and an optional free-text reason | feedback store, section 6 | AIA-CTL-05 |
| Send to a person | Any state where the filer cannot get a workable line, most often Abstained or Failed | Hands the draft to a human path, section 5, carrying what already streamed | client; the session context is handed over | AIA-CTL-06 |

- Destructive or irreversible actions proposed by the model route through the human approval gates, not this table: the model cannot submit (no submit tool exists, the RT-05 red-team hold, LC28), so there is no "accept and submit" path here; submission is the filer's own gate (the [human approval gates](ledgerline-human-approval-gates.md), AG-01), and activation of the add-on is the account admin's (LEDGERLINE-S1, AG-04). A model-proposed value is never committed by one control to a state the user cannot reverse.
- Editing the model's own draft in place: the filer and the finance reviewer at the account, and the customer policy is never edited by the model, only quoted (the policy-match v5 quoted-data wrapping, LC17; the RT-02 fix, LC28). A human edit is logged as a human change (the per-line label, AIA-DISC-01, plus the change entry), so a reviewer can tell what the model wrote from what a person corrected.

## 5. Escalation to a human

| Path | Trigger | Context handed over | Response-time promise | Owner | Test |
|---|---|---|---|---|---|
| "Send this to a person" control | System abstains or user requests human | Conversation transcript, draft so far, user ID | value owned by the on-call runbook, not this spec | Priya Nair (P2) | AIA-ESC-01 |

## 6. Feedback and audit trail

- Each feedback event records: the output shown, the prompt version (LC17), the model version (LC16), a timestamp, the user action, and a free-text reason if given.
- Where it is reviewed, by whom, on a stated cadence: Maya Chen (P1) and Priya Nair (P2) review abstains, flags and feedback weekly through the launch metrics review (design decision, not a data-sheet row). Daniel Okafor (P3) reads the weekly model-spend report (LC26).
- Feedback volume and rate feed: the error taxonomy in the hallucination-controls layer and the eval set (the coverage sheet's EVAL-1, EVAL-2 and EVAL-3 rows, and the model card). The reviewer-caught extraction-error metric M-008 (the N67 window value of 2.4 errors per 100 drafted reports; the guardrail line is N58 under 3 and N74) and the German-language field-accuracy eval (LC20; the DEP5 set, N83) are the two places this stream lands, so a "not helpful" click can move a guardrail or a threshold rather than only filling a log.

## 7. Accessibility for generated content

The AI-specific rows below are the additions the static accessibility checklist does not cover, walked against its section 8 (dialogs, overlays, toasts) for the receipt-citation and policy panels and its section 4 (controls) for stop and regenerate. All results are the 2026-11-05 pre-Gate-5 walk; the live-generation pass is re-run before the next phase.

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| Streaming text is announced to assistive technology without re-reading the whole response on every token | screen reader pass during generation | 2026-11-05 pre-Gate-5 walk on the demo environment (Larchfield Logistics); this spec's own walk note, not a data-sheet row | Pass | Maya Chen (P1) |
| The stop control is reachable and operable while streaming, not only once generation ends | keyboard and screen reader walk mid-stream | 2026-11-05 pre-Gate-5 walk; this spec's own walk note, not a data-sheet row | Pass | Priya Nair (P2) |
| Citation markers are operable and their target is announced, not just visually distinguishable | screen reader pass on a cited response | 2026-11-05 pre-Gate-5 walk; this spec's own walk note, not a data-sheet row | Pass | Maya Chen (P1) |
| A generating state has a text equivalent, not only a spinner | inspect with styles off | 2026-11-05 pre-Gate-5 walk; this spec's own walk note, not a data-sheet row | Pass | Priya Nair (P2) |

## Worked micro-example

A filer at Larchfield Logistics, a demo-environment account, attaches a single English-language receipt and taps draft. The panel moves to Generating: the merchant and amount fields stream in line by line (AIA-GEN-02), and the stop control is live from the first token, though the filer does not use it. The policy-match step then lands a matched policy line, cited inline (AIA-GRND-02), with a confidence flag on the date field under the 0.80 threshold (LC22, AIA-DISC-02). On the next receipt in the same report the extract v8 rule (LC17) finds a non-English receipt and abstains. Per section 2, the panel flags this specific line item as blank with the exact abstain wording, "The copilot could not read this receipt. A blank line item is waiting for you to enter it. This is not an error." (AIA-GEN-03). The English fields from the previous receipt remain drafted and cited. The abstain is logged as a feedback-adjacent event even though no thumbs signal was given, because abstains are counted whether or not the user reacts to them (section 6). (This is the single-receipt case; the German-language receipt pattern Wrenfield surfaced (N45, R3) is the same abstain reason at scale, and section 2's wording is what a Wrenfield Labs filer would read only for the receipts the extract abstains on.)

## Exit gate

- [x] Every surface that shows generated content discloses it, with wording no human-authored equivalent uses. The per-line label and banner use "Drafted by copilot" (AIA-DISC-01, AIA-DISC-04), a string a human-typed value never carries.
- [x] Every generation state in section 2 has been designed, not only the happy path. Idle, Generating, Abstained and Failed each have distinct wording and a distinct fallback (AIA-GEN-01 to AIA-GEN-04); abstain and failure wording are distinguishable and both offer a fallback path.
- [x] Every claim type traces to a grounding source shown at the point of use, per the hallucination-controls grounding rule. Field values cite the receipt, policy matches cite the account policy (AIA-GRND-01, AIA-GRND-02), and a claim with no source produces no suggestion but a flagged blank, never a disclaimer footer.
- [x] Stop, regenerate, and reject controls exist and are tested, not assumed from the framework's defaults. Stop, regenerate and the accept/reject flag are each named with an enforcement point and a test (AIA-CTL-01, AIA-CTL-02, AIA-CTL-04), and destructive or irreversible model actions route through the human approval gates instead of this surface.
- [x] Feedback writes a record with prompt version and model version, and someone reads it on a stated cadence. Each event carries the prompt version (LC17) and the model version (LC16); Maya Chen and Priya Nair read the stream weekly beside Daniel Okafor's spend report.
- [ ] The AI-specific accessibility rows in section 7 were walked on the demo environment ahead of Gate 5 on 2026-11-05, and the live-generation pass is scheduled before the next phase rather than completed: section 7 records the 2026-11-05 pre-Gate-5 walk and states the live-generation pass is re-run before the next phase, so this criterion is deferred, not signed.
- Annotation, 2026-12-11: the German-language case is the German-language receipts decision (D9), due 2026-12-11 and not taken. EVAL-3 scored the DEP5 set at 71% field accuracy against the 90% threshold (N83), and the decision on the German-language receipts was due 2026-12-11 and not taken (D9); this spec does not resolve it. This spec carries no model withdrawal, no re-quote, no EXP-2 or successor-price figure, and no per-line bare-confidence number, because none of those are on the sheet this document is bound to.

Signed: Maya Chen (P1), Product Manager, interaction owner, 2026-11-06
