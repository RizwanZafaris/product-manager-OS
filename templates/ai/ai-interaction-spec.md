---
layer: templates
stage: AI OVERLAY
gate: 4
feeds: ["templates/ai/eval-spec.md", "templates/architecture/accessibility-checklist.md"]
method: "knowledge/INDEX.md"
aliases: ["AI Interaction Spec", "ai-interaction-spec"]
---
# AI Interaction Spec: [feature name]

Stage: AI overlay, active whenever the product contains a model; feeds Gate 4 (acceptance criteria met)
Knowledge: ../../knowledge/design/ai-interaction-patterns.md
Skill: ../../skills/ai-prd/SKILL.md

<!-- Guardrails and hallucination-controls.md specify what the system is allowed to
     do. This document specifies what the user sees while it does it: how generation
     is disclosed, what a loading state looks like versus a wrong one, where a claim's
     source is shown, and how the user pulls the plug. A control nobody can see is a
     control nobody can use; this is the half of the overlay that makes the other
     half legible. Design intent for the surface as a whole lives in
     ../definition/design-brief.md; this file is the AI-specific layer on top of it.
     "feeds" in the frontmatter lists downstream consumers of this spec's outputs. -->

**Feature:** [one sentence]
**Interaction owner:** [name] · **Document date:** [YYYY-MM-DD]

## 1. Disclosure

<!-- A user forms different trust judgements about a human-written sentence and a
     generated one. Disclosure is not a badge for its own sake; it is the fact the
     rest of this document depends on being visible. -->

| Surface | How AI involvement is disclosed | Persistent or one-time | Test | Owner |
|---|---|---|---|---|
| [e.g. chat response] | [label, icon, or framing copy; exact wording] | [shown every turn / shown once per session] | [test ID] | [name] |
| [e.g. AI-suggested field value] | [visual treatment distinct from user-entered values] | [persistent while unconfirmed] | [test ID] | [name] |
| [add] | | | | |

- Wording used nowhere else for a human-authored equivalent: [exact copy]
- What happens when the user cannot tell which parts of a mixed document are generated: [answer, not a gap]

## 2. Generation states

<!-- The full set of states a generation-driven surface must design for, from
     ../../knowledge/design/ai-interaction-patterns.md, named because "loading"
     and "wrong" are usually built by different people who never compare notes. -->

| State | Trigger | What the user sees | Can the user act during it | Test |
|---|---|---|---|---|
| Idle | [before a request is sent] | [empty state copy, suggested prompts] | yes | [test ID] |
| Submitting | [request sent, no token received yet] | [sent indicator, request visible and editable] | [queue or edit behavior] | [test ID] |
| Thinking | [model processing before output, or reasoning trace visible] | [reasoning or thinking indicator, per reasoning-display section] | [stop control, see section 4] | [test ID] |
| Streaming | [tokens arriving] | [streaming text / progress indicator, elapsed time if over n seconds] | [stop control, see section 4] | [test ID] |
| Waiting on a human decision | [tool approval or other decision required] | [approval prompt or decision affordance] | yes | [test ID] |
| Stopped | [user pressed stop or equivalent] | [partial output kept or discarded, stated] | [regenerate, edit, or fork] | [test ID] |
| Errored | [request errored: timeout, rate limit, upstream outage] | [distinguishable from an abstain; retry affordance] | [retry, or fallback path] | [test ID] |
| Reconnecting | [connection dropped mid-reply] | [connection notice] | [wait, or retry] | [test ID] |
| Resumed | [reply restored after a reconnect] | [continuation of in-progress reply] | [stop control, see section 4] | [test ID] |
| Completed | [full reply delivered with no further changes] | [final answer with citations and controls] | [feedback, regenerate, edit, fork] | [test ID] |

- Streaming partial output is shown before completion: [yes/no, and why]
- Latency budget before the user sees a state change: [n ms to first token, n s to a stall notice]
- What happens to a message sent while a previous reply is still arriving: [queued and editable / queued and locked / sent immediately into a new turn]
- What happens to a reply in progress when the page refreshes or the connection drops: [survives / does not survive / restored on reconnect]

## 3. Grounding shown at the point of use

<!-- hallucination-controls.md section 1 names what the system may state facts from.
     This section is where that source becomes visible to the user, claim by claim,
     not buried in a settings page. -->

| Claim type | Source shown | Presentation (inline citation, footnote, expandable panel) | What clicking it does | Test | Owner |
|---|---|---|---|---|---|
| [e.g. factual answer] | [document, database row, web result] | [inline marker + panel] | [opens the source at the matched passage] | [test ID] | [name] |
| [e.g. computed or summarized value] | [inputs the computation used] | [expandable "how this was calculated"] | [shows inputs and formula] | [test ID] | [name] |
| [add] | | | | | |

- A claim with no source row here falls under the abstain policy in hallucination-controls.md, not under a generic disclaimer footer
- Confidence, when shown, is expressed as: [a stated basis, e.g. "matched 3 of 3 required fields", never a bare percentage with no meaning behind it]
- A source is only content actually retrieved or fetched, never a link the model produced from memory

## 4. User control affordances

<!-- Every row here is a way the user overrides or interrupts the system. A generation
     surface with no stop control and no edit path is a surface the user cannot trust,
     whatever the guardrails behind it say. -->

| Control | Available in which state (section 2) | Effect | Enforcement point | Test |
|---|---|---|---|---|
| Stop generation | Generating | [halts the stream immediately; partial output kept or discarded] | [client cancels request; server stops token emission] | [test ID] |
| Regenerate | Idle, Failed | [re-runs with same input; prior output kept or replaced, state it] | [new request, same prompt version] | [test ID] |
| Edit and resubmit | Idle | [user edits their own input before re-sending, not the model's output] | [client] | [test ID] |
| Accept / reject a suggestion | [wherever the model proposes a value the user did not type] | [accept commits the value as user-entered; reject discards it] | [client, before the value is used downstream] | [test ID] |
| Feedback (helpful / not helpful) | Completed | [logged with the output, prompt version, and an optional free-text reason] | [feedback store, see section 6] | [test ID] |

- Destructive or irreversible actions proposed by the model route through ../../templates/ai/human-approval-gates.md, not through this table
- Editing the model's own draft in place, where allowed: [who can, and whether the edit is logged as a human change]

## 5. Escalation to a human

| Path | Trigger | Context handed over | Response-time promise | Owner | Test |
|---|---|---|---|---|---|
| [e.g. "Talk to a person" link] | [system abstains or user requests human] | [conversation transcript, feature context, user ID] | [e.g. < 15 min, ILLUSTRATIVE] | [name/role] | [test ID] |
| [add] | | | | | |

## 5a. Model choice and fallback on removal

| Decision | Value | Owner | Test |
|---|---|---|---|
| Scope of model choice | [no choice / organization default / per-conversation / per-message] | [name] | [test ID] |
| What the picker discloses per option | [capability, cost, local vs cloud, deprecation status] | [name] | [test ID] |
| Fallback when a model is withdrawn | [which model takes over mid-conversation] | [name] | [test ID] |
| Model shown on a reopened conversation | [the model each prior reply came from / only the current model] | [name] | [test ID] |

## 5b. Memory and attachments

| Item | State the user sees | User control | Owner | Test |
|---|---|---|---|---|
| [personal memory, cross-conversation] | | | | |
| [context scoped to one conversation] | | | | |
| [attachment state: processing, ready, failed] | | | | |
| [whether the model was told the attachment exists] | | | | |

- Revocation is proven by test, not by the settings screen: when a user turns memory off or deletes an item, a test shows that specific content is gone from what the model actually receives

## 5c. Ephemeral mode

| Axis | What the mode guarantees | Owner | Test |
|---|---|---|---|
| Durable storage | [what is never written] | [name] | [test ID] |
| Network egress | [what still crosses the network: model provider, telemetry, usage analytics] | [name] | [test ID] |
| Local device | [what the device keeps regardless] | [name] | [test ID] |
| Administrator control | [can the mode be forced on or exempted] | [name] | [test ID] |

## 5d. Tool approval scope and exemptions

| Question | Decision | Owner | Test |
|---|---|---|---|
| Scope of an approval | [one call / rest of session / that tool going forward] | [name] | [test ID] |
| A call still waiting on approval when the user leaves | [what happens when they return] | [name] | [test ID] |
| Can stop cancel a call waiting on approval | [yes/no] | [name] | [test ID] |
| Paths explicitly exempt from the approval check | [automation, scheduled job, integration; with a compensating control] | [name] | [test ID] |

## 5e. Moderation stream versus buffer

| Question | Decision | Owner | Test |
|---|---|---|---|
| Where moderation checks run | [against the stream as tokens arrive / against the complete buffered response] | [name] | [test ID] |
| Stream trade-off accepted | [harmful fragment may display before retraction] | [name] | [test ID] |
| Buffer trade-off accepted | [latency added before anything is shown] | [name] | [test ID] |

## 6. Feedback and audit trail

<!-- What section 4's feedback control actually writes down, and who reads it. Without
     this, "thumbs down" is theatre. -->

- Each feedback event records: [output shown, prompt version, model version, timestamp, user action, free-text reason if given]
- Review cadence and owner: [name, cadence, e.g. weekly review by Product Owner]
- Feedback volume and rate feed: [the error taxonomy in hallucination-controls.md section 4 / the eval set in eval-spec.md / add]

## 7. Accessibility for generated content

<!-- Generated content breaks assumptions a static accessibility checklist does not
     carry: text that arrives token by token, a source panel that opens and closes,
     a stop control that must be reachable mid-stream. Walk these against
     ../architecture/accessibility-checklist.md section 8 (dialogs, overlays, toasts)
     for the citation panel and section 4 (controls) for stop and regenerate; the rows
     below are the AI-specific additions that checklist does not cover. -->

| Check | How to verify | Evidence | Result | Owner |
|---|---|---|---|---|
| Streaming text is announced to assistive technology without re-reading the whole response on every token | screen reader pass during generation | | | |
| The stop control is reachable and operable while streaming, not only once generation ends | keyboard and screen reader walk mid-stream | | | |
| Citation markers are operable and their target is announced, not just visually distinguishable | screen reader pass on a cited response | | | |
| A generating state has a text equivalent, not only a spinner | inspect with styles off | | | |
| The reasoning disclosure and citation popover are fully keyboard-operable | keyboard pass | | | |
| Rating controls and the model picker keep a visible, sufficiently contrasted focus state | keyboard and contrast pass | | | |

## Worked micro-example

A user asks a support assistant for their account's renewal date. The system streams a partial sentence, then finds no renewal date in the grounding source and abstains mid-stream: the partial text is replaced, not appended to, by "I could not find your renewal date; here is where to check your account" with a link. The stop control was live for the duration of the partial stream before the abstain; the user did not need it. The abstain is logged as a feedback-adjacent event even though the user gave no thumbs signal, if hallucination-controls.md requires abstains to be logged.

## Exit gate

Gate 4: acceptance criteria met

- [ ] Every surface that shows generated content discloses it, with wording no human-authored equivalent uses
- [ ] Every generation state in section 2 has been designed, not only the happy path
- [ ] Every claim type traces to a grounding source shown at the point of use, per hallucination-controls.md section 1
- [ ] Stop, regenerate, and reject controls exist and are tested, not assumed from the framework's defaults
- [ ] Feedback writes a record with prompt version and model version, and someone reads it on a stated cadence
- [ ] The AI-specific accessibility rows in section 7 were walked with a screen reader during live generation, not only on a static screenshot
- [ ] Model fallback, memory revocation, ephemeral-mode guarantees, tool-approval exemptions, and moderation stream-versus-buffer are each written and tested, not assumed from the provider's defaults

**Signed by [name], [date]**
