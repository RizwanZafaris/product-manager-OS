# Which Document

Before you fill anything in, decide how much document this decision deserves. Most teams own one PRD template and use it for everything, so a two-day change gets a twelve-section spec and a two-quarter platform bet gets the same twelve sections, which means neither gets the attention it needed. The weight is a choice. This file makes it an explicit one.

Three questions decide it. Answer them in this order.

1. **Stakes.** What does being wrong cost: an afternoon, a sprint, a quarter, a license?
2. **Audience.** Who has to read this and act on it: you and one engineer, a squad, five functions, a sponsor who signs, a regulator who audits?
3. **Reversibility.** Can you undo it in a day with a flag, or does it set data models, contracts, or public commitments that outlive the team?

Low stakes plus a small audience plus easy reversal means write less. Any one of them going high raises the weight by one step. Two of them going high raises it by two.

## The five weights

```
decide and log        -> reversible, no build, one or two people
ticket only           -> one sprint or less, one team, flag-reversible
one-pager             -> a few sprints, one squad plus a stakeholder or two
full PRD              -> a quarter or more, several functions, a sponsor signs
BRD + PRD + FRD       -> funding decision, contracts, or a regulator in scope
```

| Weight | Use it when | The artifact | What it costs you |
|---|---|---|---|
| Decide and log | The decision is reversible and needs no build, but someone will ask why in six months | One entry in [decision-log.md](../templates/execution/decision-log.md) | Ten minutes |
| Ticket only | Scope fits a sprint, one team owns it end to end, a flag turns it off | Your tracker, plus acceptance criteria pasted from [acceptance-criteria.md](../templates/definition/acceptance-criteria.md) | An hour |
| One-pager | Real user-facing change, one squad, a stakeholder or two who must not be surprised | [one-pager.md](../templates/definition/one-pager.md) | Half a day |
| Full PRD | Multiple functions, a quarter or more of work, a sponsor who signs at Gate 2 | [prd.md](../templates/definition/prd.md), plus FRD and NFR where the detail is load-bearing | Days, spread over the DEFINE stage |
| BRD, PRD, FRD stack | Money is being allocated, external contracts are signed, or a regulator can ask for the file | [brd.md](../templates/definition/brd.md), then [prd.md](../templates/definition/prd.md), then [frd.md](../templates/definition/frd.md) | A DEFINE stage of its own |

## The tree

```
Does anything get built?
  no  -> decide and log
  yes -> Can one team ship it inside a sprint, behind a flag?
           yes -> ticket only, with acceptance criteria attached
           no  -> Does a named sponsor have to sign, or do three or more
                  functions have to agree?
                    no  -> one-pager
                    yes -> Is funding, a contract, or a regulator in scope?
                             no  -> full PRD
                             yes -> BRD + PRD + FRD stack
```

## Overlays sit on top of the weight, not inside it

The weight decides how much specification. The overlays decide what extra questions get answered, and they apply at every weight above ticket-only.

- **The product contains a model.** The AI overlay attaches: eval sets replace prose acceptance criteria, starting at [eval-spec.md](../templates/ai/eval-spec.md). A one-pager with a model in it still needs an eval row; "the summaries should be accurate" is not a criterion.
- **A financial or data regulator governs the product.** The regulated module governs and its own template is used as shipped. See [modules/regulated/README.md](../modules/regulated/README.md). A regulated feature never runs at ticket weight, whatever its size.

## Rules

1. **Delete what you do not need.** Every template here is a superset. An empty section is worse than no section: it reads as an unanswered question and it trains readers to skim. Delete the sections that do not apply, or write "N/A because <reason>". Never leave the heading standing over white space.
2. **Customize the top three fields first.** Every template's header comment names the fields that carry the document. Fill those, then decide whether the rest earns its space.
3. **Upgrading is normal, downgrading is a decision.** A ticket that grows into a quarter gets promoted to a one-pager or a PRD, and the promotion is logged. Cutting a PRD down to a one-pager mid-flight is also allowed, and also logged, because someone signed the heavier version.
4. **The gate does not change with the weight.** Gate 2 in [STAGE-GATES.md](STAGE-GATES.md) asks the same questions of a one-pager and a full PRD: does every requirement have a pass condition, does every assumption have an owner. A lighter document answers them in fewer words, not in fewer answers.
5. **When two answers are defensible, take the lighter one and say so.** Write one line in the decision log naming the weight you chose and why. If the choice was wrong, that line is what tells the next person where the gap came from.
