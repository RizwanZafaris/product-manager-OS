---
layer: knowledge
stage: DESIGN
gate: 3
feeds: ["templates/ai/ai-interaction-spec.md", "templates/ai/hallucination-controls.md", "templates/ai/eval-spec.md"]
method: ""
aliases: ["AI Interaction Patterns", "ai-interaction-patterns"]
---
# AI Interaction Patterns

A set of experience-design decisions inside an AI feature, drawn from the paraphrased release history of one long-running open-source AI chat product, open-webui/open-webui, at commit 0a7c158. Read as a case study, not as a specification, and explained here in this repository's own words. The Open WebUI name and branding are not used as this repository's branding, no text is carried over verbatim beyond the one short quotation this card's own rules allow, and nothing here implies endorsement by that project.

## The essence

A chat window with a model behind it looks like one component. It is actually a dozen or more separate product decisions wearing one skin: what a person sees while a reply is generating, what the stop button actually stops, whether a citation can be trusted, what a rating is for, what memory remembers and what it forgets when asked to. A team that ships the visual shell without writing each of these decisions down has not avoided making them. The provider's default, or whichever engineer touched that file last, makes the decision instead, silently, and it usually surfaces as a support ticket instead of a design review. This card names the recurring decisions so a PM can write them down before a designer or an engineer has to guess.

The pattern across every section below is the same: a feature that reads as one line on a roadmap ("we support streaming," "we show citations," "users can rate replies") is actually a small state machine, a data contract, or a governance question, and the single line hides which one.

## Where it came from

Open WebUI is a self-hosted, extensible interface in front of one or more language models; its own security policy describes it as self-hosted, single-tenant, authenticated, extensible and role-based. Its public CHANGELOG runs to thousands of dated entries across many releases, and read end to end it functions as an unplanned defect-driven inventory of everything that can go wrong in an AI chat surface once real users touch it: a stop button that silently failed to cancel a reply waiting on a tool call, a citation that pointed at the wrong page, a memory toggle that stopped showing memories in the interface without stopping them from reaching the model. Almost none of these behaviors appear designed on a whiteboard first; nearly all of them appear as a fix for something that broke. That history is the evidence this card rests on.

The project's code and documentation are licensed under a layered scheme: contributions from before a certain commit are MIT, a middle range is BSD-3-Clause, and the current code carries the Open WebUI License, a BSD-3-Clause base plus a fourth clause that requires the project's branding to stay visible past a small usage threshold. The prose in its documentation and changelog is not separately open-licensed. This card treats all of it as all rights reserved for wording, paraphrases every insight in its own words, and reproduces no branding.

## When to use it

- When writing the AI interaction spec for a feature that streams, generates, retrieves, remembers, or calls a tool on a person's behalf, before a designer starts on the screen.
- When a design review is asked to approve "AI chat" as a single item, to split it into the named decisions below so each one gets its own owner and its own acceptance criterion.
- When a retrospective traces a support ticket back to an AI surface, to check whether the underlying decision was ever written down anywhere, or whether the product simply inherited whatever the model provider's SDK happened to do.

**Skip it when:** the feature has no user-facing AI surface at all, a backend classifier, a batch scoring job, an internal ranking model with no chat window and no generated text a person reads. These are product decisions about what a person perceives and controls; where nobody ever sees the model's output directly, they have nothing to attach to, and the relevant requirements belong in an NFR instead.

## The patterns

### Streaming and its states

**The decision to write.** Name the full set of states a reply can be in, not just "loading" and "done": idle, submitting, thinking, streaming, waiting on a human decision, stopped, errored, reconnecting, and resumed after a reconnect. For each state, write the affordance a person sees, the copy, and whether the reply in progress survives a page refresh or a dropped connection.

**How it lies.** A demo where tokens appear one at a time looks finished the moment it looks smooth. Streaming is a state machine, not a typing effect, and the states most often missing are the ones nobody demos: what the stop control does to a reply that is waiting on a tool approval rather than actively generating, what a person sees when the live connection drops mid-reply and again when it reconnects, and what happens to a message a person sends while the previous one is still arriving. Each of these was, in the product this card draws on, a defect discovered by a user before it was a named state in anyone's spec.

**Skip it when:** every response is a single fixed-latency return with nothing to watch arrive, for example a short classification label. Most of the state list collapses to loading, done, and errored, and naming nine states for that case is overhead with no payoff.

### Stop, regenerate, edit, fork, continue, queue

**The decision to write.** Each control on a reply is a separate contract, not a generic button row. Decide precisely what stop guarantees, including whether it also cancels a call still waiting on tool approval; what continue is allowed to expose, since resuming a truncated reply can surface content that was meant to stay hidden; what fork or branch preserves from the original thread; and what happens to a message typed while a reply is still generating, whether it is queued and editable, queued and locked, or sent immediately into a new turn.

**How it lies.** These read as one row of icons that a single accessibility pass and a single permission check can cover together. They are not. A product can correctly hide the delete control while a reply streams and still leave continue reachable through a different entry point that was never checked against the same rule, so the same content becomes visible through a side door that nobody closed.

**Skip it when:** the interaction is a single complete request and a single complete response with nothing to interrupt, edit, or resume, a one-shot lookup rather than a conversation.

### Reasoning display

**The decision to write.** Decide whether a model's intermediate reasoning is shown at all, whether it is collapsed by default, whether a person can export it, whether it is read aloud in a voice mode, and how it is kept visually distinct from the final answer for every provider whose output format differs.

**How it lies.** A reasoning panel that fades out as a visual flourish can make a model that is still working look like it has finished, and reasoning text that arrives late relative to the final answer needs an explicit rule about where it is placed, or it reads as an afterthought contradicting the answer above it. Trust calibration, whether a person believes the reasoning explains the answer, is set by exactly these small timing and layout choices, not by a policy document about transparency.

**Skip it when:** the provider exposes no reasoning trace at all, a closed completion endpoint with only a final answer. There is nothing to disclose or collapse until that changes.

### Sources and citations

**The decision to write.** Define what counts as a source before any citation ships: only content the system actually retrieved or fetched, never a link the model produced from memory. Set the citation's granularity, document, page, or the specific passage, decide what clicking a citation must land on, and decide what the product shows when there is nothing to cite.

**How it lies.** A citation that resolves to a document and a citation that resolves to the exact passage that supports the sentence look identical to the person reading them: a small numbered marker next to a claim. A citation count is not evidence of grounding, and a marker that opens the right file at the wrong page teaches a person to trust citations that do not actually support what they were attached to.

**Skip it when:** the product never quotes or references retrieved content back to the person, pure generation with no retrieval and no browsing. There is nothing to attribute.

### Model choice and fallback on removal

**The decision to write.** Decide whether a person chooses a model at all, and at what scope, an organization default, a per-conversation choice, or a per-message override. Decide what the picker discloses about each option, capability, cost, whether it runs locally or in the cloud, and deprecation status. Decide what happens to an open conversation when its model is withdrawn, and which model a reopened conversation selects by default.

**How it lies.** A model dropdown reads as a preference, a matter of taste like a color theme. It is actually a lifecycle commitment: removing a model without a stated fallback silently reassigns a conversation's history to a different model that may answer very differently, and a person rereading an old thread has no way to tell which model actually produced which reply unless that is recorded and shown.

**Skip it when:** the product offers exactly one model, with no version or provider ever exposed to the person using it. There is no picker to specify.

### In-product ratings

**The decision to write.** Write the rating schema: who is permitted to rate, what is captured beyond the thumbs, and how the rater's identity is taken from the authenticated session rather than trusted from whatever the client submits, so a forged identity cannot skew the aggregate. State explicitly, as a rule, that ratings and any resulting leaderboard feed the dataset used to refresh evaluations, and never substitute for a validated grader at release time.

**How it lies.** A rising thumbs-up rate looks exactly like rising quality, and it is neither reliable nor representative: it is trivially game-able, and the people most frustrated by a bad answer are also among the least likely to leave any rating at all, so the visible signal skews toward whoever bothered to click. Treat a rating as a directional input into a labeled dataset, never as a metric with authority on its own, and never as the thing that gates a release in place of a validated grader.

**Skip it when:** nobody downstream consumes the ratings collected, no dataset refresh, no leaderboard, no review process reads them. A rating control with no destination is a courtesy button, not a signal, and should be named as one rather than dressed up as measurement.

### Memory and attachments

**The decision to write.** Inventory memory by type, personal memories that persist across conversations and context scoped to one conversation, with the person's own view, edit, and delete controls, and a per-model switch for whether memory applies at all. Separately, inventory the state of every attachment: processing, ready, failed with a stated reason, and, distinctly, whether the model was actually told the attachment exists. Prove revocation by test: when a person turns memory off or deletes an item, a test must show that specific content is gone from what the model actually receives, not merely gone from the settings screen.

**How it lies.** A memory toggle switched off in the interface can still leave stored content reachable through a different path into the model's context, so the setting alone proves nothing; only a test that inspects the actual context sent to the model proves the revocation held. Attachments fail in three ways that all look identical to the user until something goes wrong: the content was never ingested, the content was ingested but arrived empty, or the model was simply never told the file exists at all. None of the three announces itself, and a user who asks a question the model cannot answer from a broken attachment will read the failure as the model being wrong, not the attachment being unreadable.

**Skip it when:** the product has no persistent memory and no file or document attachment surface, a stateless, single-turn text exchange with nothing carried forward and nothing uploaded.

### Ephemeral mode

**The decision to write.** State exactly what a "temporary" or "incognito" mode guarantees, item by item: what is never written to durable storage, what still crosses the network regardless, telemetry, usage analytics, a call to the model provider itself, and what a device keeps locally no matter what, a notification that already fired. Decide whether an administrator can force the mode on, or exempt it from an approval flow that otherwise applies to every conversation.

**How it lies.** "Temporary" reads to a person as a privacy promise, nothing leaves this device. Persistence and egress are two separate axes, and a mode can skip the database entirely while still sending every message to a model provider, an embedding service, or a usage-analytics pipeline. The gap between what a mode is named and what it actually guarantees is exactly where a privacy assessment has to start, not end.

**Skip it when:** the product keeps no persistent record of any conversation under any mode. Every mode is already ephemeral, and the distinction has nothing left to describe.

### Tool approval in the conversation

**The decision to write.** Decide the scope of an approval, whether it applies to one call, is remembered for the rest of the session, or is remembered for that specific tool going forward. Decide what happens to a call still waiting on approval when the person closes the conversation and returns, and whether the stop control can cancel a call in that waiting state. Decide, explicitly and separately, which paths are exempt from the same check, an automation, a scheduled job, an integration replying without a person present, because an exemption left implicit becomes a path that fails open by default.

**How it lies.** An approval prompt sitting in the main conversation window reads as though it governs every way the model can reach a tool. It usually does not: background paths built later, an automation, a scheduled run, a channel integration, commonly skip the same check because nobody re-derived it for a surface that has no person watching. That gap needs a named, explicit decision and a compensating control, not an assumption that the chat window's rule already covers it.

**Skip it when:** the product exposes no tools or function-calling to the model at all, or every tool call available is already read-only and trivially reversible with nothing an approval could meaningfully prevent.

### Moderation stream versus buffer

**The decision to write.** Decide whether safety and moderation checks run against the stream as tokens arrive or against the complete response held back before anything is shown, and write down the trade-off each choice commits to: streaming feels fast but can display a harmful fragment before it is caught and then have to retract it; buffering is safer but reintroduces the latency streaming exists to remove.

**How it lies.** "We stream, and we moderate" sounds like two features stacked on top of each other with no conflict between them. They are in real tension: a filter that inspects the stream and a filter that inspects the final buffered output are two different products with two different failure windows, one that can briefly expose something before catching it and one that adds a visible delay before anything appears. Putting a single "moderated" label on the feature without saying which of the two it is hides exactly where the remaining risk sits.

**Skip it when:** the product surfaces no free-text or ungoverned model output to an end user at all, an internal batch pipeline with no chat interface anyone reads live. There is no stream to choose a moderation point on.

### Accessibility of streaming regions

**The decision to write.** Decide the ARIA live-region politeness setting for the region where a reply streams in, whether the reasoning disclosure and any citation popover are fully keyboard-operable, whether rating controls and the model picker keep a visible, sufficiently contrasted focus state, and whether keyboard shortcuts across the interface can be turned off entirely for a person who needs different bindings.

**How it lies.** A chat interface that passes a page-level accessibility scan run after a reply has finished can still be unusable with a screen reader while that reply is arriving, because a live region set to the wrong politeness either interrupts the person on every single token or says nothing until the entire reply is complete. Both failures are invisible to a static audit that runs on a settled page, which is exactly when the interface is easiest to test and least representative of how it behaves in use.

**Skip it when:** the interface has no live-updating region at all, the full response renders once, complete, with nothing arriving incrementally for an assistive technology to announce mid-stream.

## The trap: the feature list as the finished decision

Every pattern above has the same shape of failure. A team writes "streaming: done," "citations: done," "ratings: done" on a feature list, and each line reads as complete because a box got checked, a demo worked, and a screenshot looked right. None of those three things is evidence that the underlying decision, the state list, the failure modes, the owner, the revocation test, was ever written down anywhere a reviewer could read it later. The missing fundamental is not a missing feature; it is a missing specification for a feature that already shipped. The tell is asking a simple, specific question about any line on that list, what happens to a stop press while a tool call is pending, whether a temporary chat still calls the model provider, and getting a shrug instead of a citable answer. A feature with a citable answer to its hard cases was designed. A feature with a shrug was assembled from whatever the provider's default did, and the gap between the two is invisible until someone hits the edge case in production.

## How it lies

This card is built from one product's public defect history, read end to end, not from a research literature or a controlled comparison across products. That has two specific weaknesses worth naming rather than hiding. First, a changelog shows what broke and then got fixed; it says nothing about a pattern a team tried, watched fail silently, and abandoned without ever writing a fix entry, so this card's inventory of decisions is a floor, not a ceiling, on what a real AI interface has to specify. Second, it carries survivorship bias in the other direction too: a defect that drove people away quietly, with no bug report and no support ticket, leaves no trace in a changelog at all, so the sharpest failures may be exactly the ones missing from this list. Treat every pattern here as a decision worth writing down, and treat the absence of a pattern here as no evidence that the decision does not also apply to a different product's users.

## Where it sits in the loop

- Stage: DESIGN, gate 4, written into the [AI interaction spec](../../templates/ai/ai-interaction-spec.md) that names each state, control, and owner for the surface in scope.
- Upstream: the model card and the agent's declared autonomy from `templates/ai/model-card.md` and `templates/ai/agent-architecture.md`, which settle what the model is and what it is allowed to do before this card asks what a person sees and controls.
- Downstream: the citation contract inside the [hallucination controls](../../templates/ai/hallucination-controls.md) template, and the in-product feedback signal inside the [eval spec](../../templates/ai/eval-spec.md) template, both of which turn one pattern above into a testable row rather than a design opinion.
- On trial at Gate 4, where an AI interaction spec that leaves a named pattern's decision unwritten, no state list, no revocation test, no exemption list for tool approval, is sent back rather than waved through because the feature demoed correctly.

## Used by

- [AI interaction spec](../../templates/ai/ai-interaction-spec.md)
- [Hallucination controls](../../templates/ai/hallucination-controls.md)
- [Eval spec](../../templates/ai/eval-spec.md)

## Reading

- open-webui/open-webui, commit 0a7c158, GitHub. Reuse class: paraphrase only, no branding element carried over, no claim of endorsement by the project, per [docs/REFERENCES-DESIGN.md](../../docs/REFERENCES-DESIGN.md). Licensed under the Open WebUI License, a BSD-3-Clause base with an added branding clause; earlier code in the same history is MIT or plain BSD-3-Clause, and the documentation prose itself carries no separate open license. This card paraphrases the product's public defect history throughout and does not quote its documentation, its changelog, or its branding.
