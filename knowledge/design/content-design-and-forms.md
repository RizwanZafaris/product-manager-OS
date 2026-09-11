---
layer: knowledge
stage: DEFINE
gate: 2
feeds: ["templates/definition/ux-writing-guide.md", "frameworks/design/content-microcopy-audit.md", "templates/definition/acceptance-criteria.md"]
method: ""
aliases: ["Content Design", "content-design-and-forms"]
---
# Content Design

This is a card about experience design in words: what a product says on an error, an empty screen, a form or a confirmation prompt, at the moment something has not gone as planned. It does not stand for the DESIGN stage or for Gate 3 in this repository's loop; the decisions below start as early as a first drafted label and get tested long after DESIGN closes.

Based on the content design guidance in the GOV.UK Design System and the GOV.UK content and publishing guidance (Government Digital Service), the Nielsen Norman Group's writing on error messages, confirmation dialogs, progressive disclosure and empty states, IBM's Carbon Design System empty state and notification patterns, Luke Wroblewski's 2009 inline validation study and Matteo Penzo's 2006 label placement study, and react hook form's validation timing vocabulary. Explained here in this repository's own words; GOV.UK material is adapted under the Open Government Licence, with the attribution statement at the foot of this card.

## The essence

Content design starts in an unusual place for a discipline people associate with wordsmithing: not with a sentence, but with a user need, something a person must do or find out, checked rather than assumed. Only once that need is real does content design ask how much to say, in what format, and where on the screen to put it, and only after that does it reach for a house style. A product that skips straight to wording is not doing content design yet; it is copyediting a decision nobody checked.

That ordering matters more once the surfaces get functional rather than descriptive. An error message, an empty state, a confirmation prompt and a form's validation behaviour are not decoration around a working interface, they are the interface, for the specific and common moment when something has not gone as the user expected. A screen that behaves correctly but explains itself badly fails the same users a broken screen fails, only later, and with more blame attached, because the failure now reads as the user's mistake rather than the product's.

## Where it came from

Two traditions meet in this card, from different starting conditions. GOV.UK's content design discipline was built inside the Government Digital Service to write GOV.UK in one voice for a whole population's transactions, whatever a citizen's reading level, first language or stakes at the time, which is why its rules read like operating instructions rather than style preferences: say what went wrong and how to fix it, ask one question per page, use the actual label as the heading. Nielsen Norman Group's error message, confirmation dialog, progressive disclosure and empty state guidance descends from Jakob Nielsen's original usability heuristics and has been extended and re tested by later NN/g writers against modern interfaces; it reads as consultancy grade synthesis across many products' failures rather than one team's house style.

IBM's Carbon Design System sits between the two: an enterprise product design system, published openly, that turns both traditions' advice into a stated anatomy an engineering team can actually build against, an empty state's image, title, body and action, a notification's status and type. The two smaller studies this card carries, Wroblewski's on validation timing and Penzo's on label placement, come from a narrower place still: single research efforts on forms built for the study, not standing institutions, cited here because they are the most concrete evidence either tradition offers for a genuinely contested question, not because they carry equal institutional weight with the rest.

## When to use it

- Writing or reviewing an error message, an empty state, a notification, a confirmation prompt or a form's validation behaviour, at any point from a first draft to a pre launch content audit.
- Deciding what a screen shows first and what it defers behind a "show more", so the decision is made once rather than renegotiated screen by screen.
- Turning a content rule into a testable acceptance criterion: "the rule enforces exactly what its message promises" only works once someone has stated the rule and the message together.
- Building or checking a product's own [UX writing guide](../../templates/definition/ux-writing-guide.md), or running a [content and microcopy audit](../../frameworks/design/content-microcopy-audit.md), both of which use this card as their method.

**Skip it when:** the text in question is a regulator's required wording that has to ship verbatim. Quote it and route it through `modules/regulated/` rather than rewriting it under this card's rules. Skip it too when there is no user facing text decision left to make, a purely internal job with nobody reading its output, or when fewer than a handful of strings are actually changing; [content and microcopy audit](../../frameworks/design/content-microcopy-audit.md) itself skips below five changed strings for the same reason.

## Start from the user need

GOV.UK's own definition of content design starts before any sentence exists: something a user needs to do, or needs to find out. Only once that need is confirmed, not assumed from a stakeholder's request, does the discipline move to its next three questions, in order: how much to say, what format serves it best (a paragraph, a table, a single line of hint text), and where on the page it belongs. House style and voice come last, applied to a decision that is already sound rather than used to dress one up. GOV.UK adds a maintenance duty most teams drop once a screen ships: content is kept up to date against the service it describes, because a correct sentence about a process that has since changed is a wrong sentence with good grammar.

## Error messages: say what went wrong and how to fix it

The rule, adapted from the GOV.UK Design System's error message component under the Open Government Licence: explain what went wrong and how to fix it, in plain English, and never reach for an error message when the real problem is that the user cannot use the service at all. If a user cannot fix the problem by changing what they typed, the fix is not a better error message, it is a page that says why and what to do next, because the fault sits with the service rather than with the answer given.

Within that, GOV.UK bans a specific set of words and habits, because each one either blames the user, hides behind jargon, or adds nothing a user can act on: technical jargon such as an unexplained error code; "forbidden", "illegal", "you forgot" and "prohibited", because each one accuses; "please", because it implies refusing is a choice; "sorry", because an apology does not fix the field; "valid" and "invalid", because they describe the system's judgement rather than the user's next step; and jokes such as "oops", because a user who meets the same joke twice stops finding it funny. Match the error message's own wording to the question's label, so a user can find the field the message is about without translating between two vocabularies, and never clear the fields that failed: keeping the user's original answers on the page lets them see what went wrong, edit it, and avoid retyping everything else.

The Nielsen Norman Group's separate guidance, cited rather than adapted since its own text is not openly licensed, organizes the same discipline into three groups. Visibility: put the message next to the field it concerns rather than in a banner far away, and do not show it before the user has had a genuine chance to answer, which the group treats as designing an unfinished field to look like a wrong one. Communication: describe the exact problem in the reader's language rather than a generic "an error occurred", and hold a tone that does not blame the user for a system the user did not design; as the group puts it, "the true culprit is the designer" when an interface makes a mistake easy to make. Efficiency: let a person fix the mistake in place rather than starting over, and where possible narrow a broad failure to a short list of likely fixes instead of leaving the user to guess.

## One question per page

GOV.UK's question pages pattern turns "ask one thing per page" into a specific, testable instruction: set the question's own label or legend as the page's heading, so a screen reader user hears the question exactly once instead of a generic page title followed by the same question repeated as a separate line. Keep a back link at the top of every question page, because some users do not trust a browser's own back control while filling in a form, and make sure that control still returns to the page the user actually saw rather than a reset one. Mark optional fields as "(optional)" in the label itself, never mark a required field with an asterisk, and let a user answer "I do not know" when that is a genuinely valid response, rather than forcing a guess just to clear a required field check.

## Notification banners, used sparingly

A notification banner tells a user something that is not directly about what they are doing on that page: a service wide problem, a personal deadline, or the outcome of an action taken on an earlier page. GOV.UK's instruction is to use them sparingly, citing the Nielsen Norman Group's research into banner blindness as the reason: users habitually stop scanning anything sitting in a banner's usual position, so the more often a banner carries routine information, the less any one banner actually gets read. Two firm boundaries follow. Never use a notification banner to report a validation error, that is the error message and error summary components' job, and never show a banner and an error summary on the same page together. Show at most one banner per page; where two things are true at once, combine them into a single message rather than stacking two banners a user will read as one regardless.

## Confirmation dialogs, only before something serious

Jakob Nielsen's 2018 guidance treats a confirmation dialog as a tool with one honest job: give a user a second chance to check their work before a command with serious consequences runs. That honesty has a cost. A dialog that interrupts a routine action teaches a user to click through without reading, and a generic "are you sure" with no specifics gives that reflexive click nothing to catch, because the only sensible answer to a question with no detail is that yes, of course, that was the request just made.

The rule that survives contact with real use is narrow: reserve a confirmation dialog for actions that are destructive, expensive or genuinely hard to reverse, name the specific thing about to happen rather than a generic warning, so the user can actually recognize whether it is the right thing, and prefer undo over confirmation wherever the action can truly be undone, because undo protects the user without training them to stop reading dialogs.

## Empty states and notifications, compared

Two surfaces get confused because both fill a space with feedback instead of content, but they answer different questions. An empty state answers "what would normally be here", almost always because nothing has happened yet: no data collected, no search match, or something failed to load. IBM's Carbon Design System sorts empty states into three types: a no data or first use state that explains what the space will hold and how to fill it, a user action state that responds to something the user just did such as a search with no results, and an error management state that explains why data cannot be shown and what corrective step is available. The Nielsen Norman Group's separate empty state guidance gives the surface the same three jobs from a different angle: communicate the system's actual status so an empty panel does not read as a stalled one, teach users a feature they have not tried yet, and offer a direct route into the task the empty space exists to support, rather than leaving a blank container to explain itself.

A notification, by contrast, answers "something changed, and you should know", independent of whatever space it sits in. Carbon is useful here for a dimension most content design advice skips over: persistence and interruption are two separate settings, not one dial marked how loud. An inline notification sits beside the thing it concerns and stays until the user resolves or dismisses it, low interruption, high persistence. A toast slides in, says its piece, and if it carries no action, disappears on its own, low interruption and low persistence. A banner sits above the page's content and stays until dismissed; it interrupts by claiming space rather than by blocking anything, and it persists until the user acts. A modal blocks the task entirely until the user answers it, the only type built for high interruption and full persistence together, which is exactly why the serious or irreversible cases from the previous section are the only ones that should reach for it. Choosing a notification's format is choosing a point on those two axes, not choosing how urgent the copy sounds.

## Progressive disclosure, two levels or fewer

Progressive disclosure resolves a genuine conflict rather than hiding it: every user wants enough options to cover a special case, and every user also wants to learn the interface quickly, and those two wants trade off directly against each other. The resolution is to show only the handful of options most people need on the first screen and put everything else one step away, disclosed on request.

Two decisions carry all of the risk. Getting the split wrong either buries something most users actually need behind a click they will never make, or crowds the first screen with options meant to stay secondary. And the route from the first level to the second has to be obvious: a clearly placed control, labelled so its destination is predictable before the click, not a mystery button that only experienced users find. The two level ceiling in this card's title is not a house preference: the Nielsen Norman Group's own guidance is that designs pushed past two disclosure levels typically become hard to use, because users lose track of where they are while moving between levels. When a feature set genuinely needs more, the fix is not a third click through, it is grouping the second level's options so a user checks one place rather than several.

## Forms

The following rules apply to a working form rather than a single labelled field, and each one is a product decision a spec has to make explicitly rather than one an engineer discovers while wiring up a submit button.

### Validation timing is two decisions, not one

Treat validation timing as two separate settings rather than one, a split borrowed as vocabulary, not doctrine, from react hook form's own API: a "mode" option controls when a field is first checked, on blur, on change, on submit, or once the field has been touched, and a separate "reValidateMode" option controls when a field already showing an error gets checked again. Most product specs name only the first setting, if either, and the second is where a frustrating form actually lives: an error that appeared once but will not clear until the whole form is resubmitted is worse than one that vanishes the moment the user fixes it. A common pairing is to wait before showing an error, on blur or on submit, and to re check on every keystroke once an error is already showing, so correction feels immediate even though detection did not. Where a field is validated on every keystroke at all, pair it with a short delay before the message appears; validating the instant a character lands punishes a user for being mid answer rather than for being wrong.

GOV.UK's own default sits at the conservative end of this spectrum: validate at submission, not as the user leaves each field, and turn off a browser's built in HTML5 validation entirely, because its styling and behaviour cannot be made consistent or reliably accessible across browsers and assistive technology. GOV.UK adds earlier, per keystroke validation only where user research shows it solves more problems than it causes, a character count limit being its own worked example, since a user should not discover the limit only after writing a whole answer.

Luke Wroblewski's 2009 inline validation study, run with the usability firm Etre on account creation forms and published in A List Apart, points toward a different answer for a different kind of form. Compared with validating only at submission, showing feedback right after each answer (validating "on blur", in the study's own terms) produced, on that particular form, a twenty-two percent increase in success rate, a twenty-two percent decrease in errors, a 31 percent increase in satisfaction, a 42 percent decrease in completion time and a 47 percent decrease in the number of eye fixations recorded. That same study also found that validating while the user was still typing, before they had finished an answer, made completion slower and satisfaction worse than either the after the fact or the submit only approach; participants described a field that flashed an error mid keystroke as unhelpful rather than helpful, which is the evidence behind the delay rule above. This is research evidence from a small, single study sample of twenty-two participants across six form variants, not a large or randomized trial, and read against GOV.UK's own caution it does not actually contradict GOV.UK's position: both treat premature, mid keystroke validation as the failure to avoid, and both make validation timing a decision to justify for the form in front of you, never a default inherited from someone else's form.

### One failing rule, or all of them

A second, separate decision, again borrowed as vocabulary rather than doctrine from react hook form's "criteriaMode" option: when a field fails more than one rule at once, a password missing both a number and a capital letter is the common case, does the user see the first failing rule, or the whole list at once? Showing only the first keeps the message short but forces fail, fix, resubmit, fail again on the next rule, and repeat. Showing every failing rule at once, the pattern behind a password requirements checklist, costs more space but tells the user everything to fix in a single pass. Pick this per field, not per form: a single required text field has nothing to gain from an all rules list, while a password field usually does.

### Async availability checks need a pending state

A field that has to ask a server whether an answer is available, a username or a merchant identifier are the common cases, introduces a race a purely local rule never has: the user can type a second answer before the check on the first one returns. The product decision has three parts, whatever the implementation underneath it: show a pending state while the check is running, so the user knows a check is in progress rather than assuming the field has simply gone quiet; resolve races by keeping only the latest request's result and discarding anything still in flight from an earlier one; and decide, explicitly, what happens if the user submits the form while a check is still pending, block the submit, or let it through and reconcile the result afterward. Leaving that third case undecided is how a form ships a race condition disguised as an edge case.

### Four kinds of error, and where each belongs

Every validation failure fits one of four kinds, and the kind decides where its message appears. A field error belongs to one input and shows next to it. A cross field error, a password confirmation that does not match its original, or an end date before a start date, belongs to neither field alone and shows once, near the fields it concerns or gathered into the error summary that names both. A form error is not about any one answer but about the submission as a whole, nothing was filled in at all, or a required combination of answers is missing, and shows at the top of the page rather than pretending to belong to a field it does not. A server error is different again in kind: the form was valid and the server still failed to process it, for a reason the user's own answers cannot fix by editing them, so it needs its own page level or banner level treatment precisely because retyping the form will not help. Mixing these up, showing a server failure as though it were a field error, is a common way a form quietly misdescribes what actually went wrong.

### Never lose the user's input

On any failure, field, cross field, form or server, keep every answer the user already gave on the page, exactly as entered, rather than clearing the form back to blank. This is the same instruction GOV.UK gives for its own error message component, and the same lesson the Nielsen Norman Group draws from watching users hit a wall: a person correcting one mistake should not also have to remember and retype everything that was already correct. A server failure is the case most specs forget, because it happens after the client side has already decided the answers were valid; the fix is identical regardless of which layer caught the problem.

### Show success only on server confirmation

A success state is a claim about the server's response, not about a request having been sent. Showing "saved" the moment a request goes out, ahead of the server actually confirming it, produces a specific and costly failure: the user believes something happened that has not happened yet, closes the tab, and finds out later that it did not save. Tie every success state to a confirmed server response, and give a pending state its own honest label while the request is still in flight, rather than borrowing the success state early to make the interface feel faster than it is.

### Disabled fields quietly drop their data

A disabled form field is not merely unusable, it is invisible to the submission: standard form behaviour, which a library such as react hook form also follows, leaves a disabled field's value out of the data the form actually sends. That can be exactly what a product wants, a read only field that should never be resubmitted, but it has to be a decision the spec states rather than a side effect discovered in testing. Say explicitly, per field, what the product expects to happen to a disabled field's value: nothing sent at all, a stored value carried over unchanged by some other route, or the field re enabled before the form submits.

### The rule must promise only what it enforces

The easiest failure of all to miss in review: a validation rule and its message have to describe exactly the same thing. A field that actually requires digits only, but whose message says "enter a number", will reject a decimal point the user reasonably assumed "a number" allowed. A message that promises "35 characters or less" next to a rule that actually caps the field at 30 fails a user for following the instruction precisely. Write the rule and its message together, and test them together, because a rule and a message drafted at different times by different people is how this mismatch survives all the way to production.

### Label placement carries the same caution

A related and older caveat, Matteo Penzo's 2006 eye tracking study for UXmatters, is also research evidence from a small sample, tested on short, four field forms. Labels placed to the left of their fields produced a reliable single eye movement from label to field, but that movement itself took roughly half a second on average, evidence of real cognitive effort even where the association was easy to see. Labels placed directly above their fields, or immediately to the right, cut both that movement time and the total number of fixations needed to finish the form. The caution is shaped the same as Wroblewski's: four fields, a small sample, and a study built to isolate eye movements rather than to model a whole real product's form, so treat the direction of the finding, labels close to their field beat labels far from it, as far more durable than any specific number from a study this old and this small.

## The trap: copy styled last

The failure that survives every other check in this card is sequencing: content treated as the last coat of paint, added to a screen once the layout, states and flows are already decided, rather than as part of deciding them. A string that reads cleanly in a design review, in English, at whatever length it happened to be typed, can break in two specific ways that only show up later. Translated into a language that commonly runs longer than English, a practitioner's rule of thumb puts the expansion at around 30 percent for German and several Romance languages, the same message can overflow a button, wrap a label onto a second line, or push a fixed height error area into the field below it. Sent as an SMS or a USSD message rather than shown on a screen, a string containing even one character outside the GSM-7 alphabet, a curly quote, certain punctuation such as an em dash, or certain accented letters, silently switches the whole message to UCS-2 encoding, which roughly halves the character budget available per segment and can split one message into two or three without anyone noticing until a delivery report comes back wrong. Neither failure shows up when the person reviewing content is reading their own language, on a wide desktop screen, which is exactly the condition under which every string gets approved.

## How it lies

This card's own sources lie in two matched ways, and both are worth carrying into how confidently you cite it back. First, most of what GOV.UK and Carbon publish is practice distilled from delivery, not measurement. GOV.UK's own error message page makes its strongest claim about the rule above in a single sentence naming no study, no sample size and no comparison condition: that the guidance has been tested with all types of users in live services. Treat GOV.UK's and Carbon's rules as platform convention, hardened by an unusually large number of real deployments, not as controlled research; they are worth following because they have survived contact with millions of users on high stakes government services, and that is a real warrant, just a different and weaker one than a randomized trial.

Second, the two numbers this card does carry, Wroblewski's and Penzo's, come from small, single study, non randomized tests on forms built for the study rather than pulled from production. A sample that size generalizes to shape, validate after rather than during, keep labels close to their fields, far more safely than it generalizes to magnitude: do not promise a stakeholder a specific time saving because one 2009 account creation form produced one. GOV.UK's own validation guidance, notably, stops short of a universal timing default of its own: it validates at submission by default and adds anything earlier only where a team's own user research justifies it for that form, which is itself evidence that no single default survives every form. Present validation timing to a stakeholder as a decision this card helps you justify for the form in front of you, never as a setting this card tells you to ship.

## Where it sits in the loop

Stage: DEFINE, Gate 2, though the discipline runs earlier and later than that gate suggests. A state the product's design brief enumerates needs its content decided before a spec can call itself complete, and a rule written here becomes a testable acceptance criterion long after Gate 2 closes.

Upstream: the [design brief](../../templates/definition/design-brief.md) names who the product writes for and in what tone, and [templates/definition/ui-state-inventory.md](../../templates/definition/ui-state-inventory.md) enumerates the states, default, empty, loading, error, disabled, this card decides the content for.

Downstream: [UX writing guide](../../templates/definition/ux-writing-guide.md) carries a product's own voice, terminology and banned word list, built on the rules above. [Content and microcopy audit](../../frameworks/design/content-microcopy-audit.md) runs this card's rules as a pass or fail check across every string on a screen. [Acceptance criteria](../../templates/definition/acceptance-criteria.md) turns "the rule enforces exactly what its message promises" into a testable case per field.

On trial at Gate 2, where a spec is checked for testability rather than good intentions, and again at Gate 4, where acceptance evidence is checked against what actually shipped.

## Used by

- [UX writing guide](../../templates/definition/ux-writing-guide.md)
- [Content and microcopy audit](../../frameworks/design/content-microcopy-audit.md)
- [Acceptance criteria](../../templates/definition/acceptance-criteria.md)

## Reading

- GOV.UK Design System and GOV.UK content and publishing guidance, Government Digital Service: "Understand content design", the Error message component, the Question pages pattern, the Notification banner component and the Recover from validation errors pattern. Documentation is Crown copyright under the Open Government Licence v3.0; code is MIT. Reuse class: adapt with notice.
- Tim Neusesser and Evan Sunwall, "Error Message Guidelines", Nielsen Norman Group, 14 May 2023. All rights reserved. Reuse class: cite only.
- Jakob Nielsen, "Confirmation Dialogs Can Prevent User Errors: If Not Overused", Nielsen Norman Group, 18 February 2018. All rights reserved. Reuse class: cite only.
- Jakob Nielsen, "Progressive Disclosure", Nielsen Norman Group, 3 December 2006. All rights reserved. Reuse class: cite only.
- Kate Kaplan, "Designing Empty States in Complex Applications: 3 Guidelines", Nielsen Norman Group, 19 September 2021. All rights reserved. Reuse class: cite only.
- IBM Carbon Design System, the Empty states and Notification patterns. Website and code repositories are Apache 2.0. Reuse class: paraphrase with attribution.
- Luke Wroblewski with Etre, "Inline Validation in Web Forms", A List Apart, 2009. All rights reserved. Reuse class: cite only.
- Matteo Penzo, "Label Placement in Forms", UXmatters, 2006. All rights reserved. Reuse class: cite only.
- react hook form (react-hook-form/react-hook-form, commit 65a448d). MIT licensed. Reuse class: vocabulary only, cited for the names of its timing options, never as doctrine or as an API to implement against.

Contains public sector information from the GOV.UK Design System and GOV.UK content and publishing guidance, licensed under the Open Government Licence v3.0 (nationalarchives.gov.uk/doc/open-government-licence/version/3). This card is not endorsed by the Government Digital Service, and carries no Crown or government mark.
