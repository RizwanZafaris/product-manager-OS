# Kano Model

Based on the ideas of Noriaki Kano and colleagues, from the paper on attractive quality and must-be quality (1984).

## The essence

Not all product attributes buy satisfaction the same way, and treating them as one pool is how teams overspend on the wrong ones. Kano's insight is that attributes fall into classes with different satisfaction curves:

- **Basics (must-be).** Their absence enrages; their presence earns nothing. Nobody praises a banking app for not losing money. Investment past "reliably present" is wasted.
- **Performance (one-dimensional).** More is better, roughly linearly. Speed, battery life, storage. These are the attributes customers can articulate when asked, which is why surveys overweight them.
- **Delighters (attractive).** Their absence costs nothing because nobody expects them; their presence produces disproportionate joy. Customers cannot ask for them, by definition.

Two further classes matter in practice: **indifferent** attributes, which move nothing either way and are pure cost, and **reverse** attributes, where some users actively dislike what others want. Classification is empirical, not intuitive: ask each attribute as a pair of questions, how would you feel if it were present, and how would you feel if it were absent, and let the answer pair place it in a class.

The strategic reading: cover every basic, compete on chosen performance attributes, and hold a small budget for delighters, because that is where differentiation lives.

## When to use it

- When scoping a release: the PRD's functional scope should cover basics completely before any delighter spends a line of the budget.
- When sequencing a roadmap: performance investments compound predictably; delighter investments are bets and should be sized like bets.
- When a stakeholder insists every requirement is critical, as the instrument that forces a classification with the customer's voice rather than the loudest voice.

**Skip it when:** one basic is visibly broken. Classification will tell you what every support ticket already says, and the survey costs a week you could spend fixing the thing. Come back to Kano once the floor holds.

## The trap: delighters decay into basics

The classes are not stable, and the drift runs in one direction. Yesterday's delighter becomes today's performance attribute and tomorrow's basic: cameras in phones, free shipping, autosave. A team that classified its attributes once and filed the result is now defending a differentiator that the market reclassified as table stakes years ago, and wondering why the delight line item stopped producing delight. The decay has a second edge: a competitor's delighter can silently become your missing basic. Reclassify on a cadence, and treat any delighter more than a couple of years old as a suspect basic until the question pair says otherwise.

## Used by

- [PRD](../templates/definition/prd.md)
- [Roadmap](../templates/planning/roadmap.md)
