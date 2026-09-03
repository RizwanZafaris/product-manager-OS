---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: "knowledge/rice-prioritization.md"
aliases: ["Roadmap"]
---
# Roadmap: [product name]

**Stage:** PLANNING track (feeds every stage of the [operating loop](../../os/OPERATING-LOOP.md))
**Knowledge:** [RICE prioritization](../../knowledge/rice-prioritization.md)
**Skill:** [roadmap builder](../../skills/roadmap-builder/SKILL.md)

<!-- A roadmap is a statement of intent with honesty about uncertainty, not a delivery
     contract. The horizon structure here follows the Now, Next, Later model from
     Janna Bastow's work at ProdPad: certainty decays with distance, so precision must
     too. Dates live only in Now. Later gets themes.

     Two more rules. Every initiative names the outcome it serves, tying back to the
     OKR sheet; an initiative that serves no objective is a pet project with a row.
     And appetite beats estimate for sizing, a discipline drawn from Shape Up by Ryan
     Singer (see ../../knowledge/shape-up.md): state how much time the initiative is
     WORTH before anyone estimates how long it takes.

     The roadmap-builder skill linked above drives this template: it drafts the rows,
     then stress-tests them against dependencies and confidence. -->

**Owner:** [name] · **Last updated:** [YYYY-MM-DD] · **Review cadence:** [e.g. monthly]
**Linked OKR sheet:** [okrs.md copy for this product]

## Preamble: read this before the tables

<!-- Written out rather than left to you, because this paragraph is the difference
     between a roadmap and a promise, and it is the paragraph everyone skips
     writing. Keep it at the top of every copy you share, internal or external.
     Edit the horizon lengths to match your cadence; leave the meaning alone. -->

> **This roadmap manages expectations, not commitments.** It says what we are working on now, what we expect to pick up next, and the directions we are holding open for later. It is not a delivery contract and no date on it is a promise.
>
> **Now** is committed and in flight. Confidence is high, and if something here slips you will hear it from us before you notice it yourself.
>
> **Next** is shaped and planned, not started. The order can change when evidence changes. Treat anything here as likely, not scheduled.
>
> **Later** is a set of directions, not features. Anything in Later may never ship, and the entries are deliberately imprecise: a specific feature name written a year out becomes a commitment nobody made.
>
> Things move backward as well as forward, and items get killed. The parked-and-killed table below is part of the roadmap, not an appendix to it. If a decision here affects something you are counting on, ask, and you will get the real answer rather than the reassuring one.

## Now (committed, in flight or next up)

<!-- Confidence below 70% does not belong in Now. The italic row shows a completed entry. -->

| Theme | Initiative | Outcome it serves (objective ref) | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|
| | | | [month or sprint] | [%] | | Not started / In progress / Done |
| *reduce manual entry* | *receipt auto-extraction v1* | *O1: submission time cut in half* | *[month]* | *85%* | *storage service upgrade* | *In progress* |

## Next (planned, shaped, not yet committed)

| Theme | Initiative | Outcome it serves | Target period | Confidence | Dependencies | Status |
|---|---|---|---|---|---|---|
| | | | [quarter] | [%] | | Shaping / Shaped |

## Later (directional themes only)

<!-- No dates, no feature names precise enough to be quoted back at you in six months. -->

| Theme | Problem it addresses | Earliest it could enter Next | Signal that would promote it |
|---|---|---|---|
| | | [quarter] | [what evidence moves it up] |

## Parked and killed

<!-- A roadmap that only grows is a backlog. Killing an initiative in writing, with a
     reason, is what keeps the rest credible. -->

| Initiative | Parked or Killed | Reason | Date |
|---|---|---|---|
| | | | |

## Change log

| Date | Change | Why | Who decided |
|---|---|---|---|
| | | | |

## Exit gate

This roadmap is fit to share when:

- [ ] Every Now and Next initiative names the objective it serves, and that objective exists in the OKR sheet
- [ ] Confidence is stated per row, and nothing under 70% sits in Now
- [ ] Later contains themes, not dated features
- [ ] Dependencies are named, and each appears in the [dependency register](../execution/dependency-register.md)
- [ ] At least one thing has been parked or killed since the last review, or the owner has written why not
- [ ] The change log shows the roadmap is alive, not laminated

Signed: [name], [role], [YYYY-MM-DD]
