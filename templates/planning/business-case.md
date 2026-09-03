---
layer: templates
stage: PLANNING
gate: 1
feeds: []
method: ""
aliases: ["Business Case", "business-case"]
---
# Business Case: [initiative name]

Stage: PLANNING track, feeds [Gate 1: problem worth solving](../../os/STAGE-GATES.md) and the [roadmap](roadmap.md)
Knowledge: [market sizing worksheet](../../frameworks/strategy/market-sizing.md)
Skill: [market-sizing](../../skills/market-sizing/SKILL.md) for the benefit side; [estimator agent](../../agents/estimator-agent.md) for the cost side

> **Delete any section you do not need.** A one-quarter bet by one squad needs sections 2, 3, and 6 on one page; the full form is for money or headcount allocated across years, the top rung of [os/WHICH-DOCUMENT.md](../../os/WHICH-DOCUMENT.md).

<!-- Compares options in money over time and recommends one. It is not the
     opportunity assessment (../discovery/opportunity-assessment.md), which decides
     whether an idea earns discovery time, and not the BRD (../definition/brd.md),
     which states the funded initiative's objectives and scope for Gate 2. The BRD's
     financial case copies the winning option from here; it never recomputes it.

     Fill first: the options table (section 2), costs and benefits by year
     (section 3), sensitivities (section 5). Every number is ILLUSTRATIVE until the
     finance partner named below has agreed the method. -->

**Owner:** [name] · **Sponsor:** [name] · **Finance partner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / In review / Approved
**Money unit:** [currency, thousands] · **Discount rate:** [n percent, from finance]

## 1. The decision

[Two to four sentences: what is being decided, by whom, by when. Copy the Gate 1 problem statement and its cost of inaction; the inaction figure becomes the do-nothing row below.]

## 2. Options, including doing nothing

<!-- Do nothing is never zero: it costs the inaction figure every year and is the
     baseline every other row is measured against. Three or four options is right;
     one option is a request, not a case. -->

| Option | What it is, in one sentence | Cost, one line | Benefit, one line | Main risk |
|---|---|---|---|---|
| A. Do nothing | Keep the current process and absorb the cost of inaction | | | |
| B. [smallest option] | | | | |
| C. [full option] | | | | |
| D. [buy or partner] | | | | |

## 3. Costs and benefits by year

<!-- One table per surviving option, incremental to option A. Year 0 is the build
     period. Every benefit line names its method: units times value, hours saved
     times loaded rate, expected loss times reduction. Build cost is the estimator's
     likely figure; the range goes to section 5. -->

**Option [letter]: [name]**, ILLUSTRATIVE until the method is agreed with [finance partner] on [date]

| Line | Year 0 | Year 1 | Year 2 | Year 3 | Total | Method |
|---|---|---|---|---|---|---|
| Build cost | [n] | | | | | estimator, likely figure |
| Run cost | | | | | | |
| Benefit: revenue | | | | | | [units times price] |
| Benefit: cost saved or risk avoided | | | | | | [hours times rate] |
| Net | | | | | | |
| Cumulative net | | | | | | |

## 4. Payback and NPV

<!-- Payback is the first year in which cumulative net turns positive. NPV sums each
     year's net divided by (1 + rate) to the power of the year. Show the arithmetic;
     a figure with no arithmetic gets withdrawn under questioning. -->

ILLUSTRATIVE worked line on invented inputs for Ledgerline's expense copilot, option C, rate 10 percent, thousands: net by year is -300, +140, +260, +300. Cumulative net is -300, -160, +100, +400, so payback lands in year 2. NPV = -300 + 140 / 1.1 + 260 / 1.21 + 300 / 1.331 = -300 + 127 + 215 + 225 = about +267.

- **Option A:** payback never; NPV [the inaction cost, discounted, as a negative]
- **Option [B, C, D]:** payback [year]; NPV [n]; 3-year net [n]

## 5. Sensitivities: what breaks the case

<!-- Change one input at a time to its pessimistic value and recompute. The case is
     honest when at least one row flips the recommendation, or the document says why
     none does. Every input here is also a row in the assumptions register. -->

| Input | Base | Pessimistic | NPV becomes | Payback becomes | Flips the recommendation? |
|---|---|---|---|---|---|
| *adoption share of submitters (ILLUSTRATIVE)* | *60 percent* | *30 percent* | *about -16* | *year 3* | *yes* |
| *build cost (ILLUSTRATIVE)* | *300* | *450* | *about +118* | *year 3* | *no* |
| | | | | | |

*Adoption-row arithmetic, disclosed so it can be checked: in this ILLUSTRATIVE example, the year 1 to 3 net flows (140, 260, 300) are revenue benefit net of a fixed run cost, and revenue benefit scales with adoption. Year 0 (-300) is the build cost, fixed and not adoption-linked. Halving adoption halves only the benefit component of each year 1 to 3 flow, giving new net flows of 70, 130, 150. NPV = -300 + 70 / 1.1 + 130 / 1.21 + 150 / 1.331 = -300 + 64 + 107 + 113 = about -16. Cumulative net is -300, -230, -100, +50, so payback lands in year 3, not beyond it. State your own benefit-versus-fixed-cost split here; a sensitivity row with no disclosed split is not reproducible and should not ship.*

**The case survives when:** [the one or two conditions that must hold, in plain words].

## 6. Recommendation

- **Option:** [letter and name], because [two sentences].
- **What we give up:** [the option that lost and what it offered].
- **Door type:** [one-way or two-way, per the decision doors worksheet], so the evidence bar is [high / ordinary].
- **Conditions:** [what must be true before money is spent, with owners and dates].
- **What would reverse this:** [the trigger, and who watches for it].
- **The ask:** [money, people, and the roadmap slot, stated once].

---

## Exit gate (feeds Gate 1: problem worth solving)

Done when every box is honestly ticked. The signed copy goes to [Gate 1](../../os/STAGE-GATES.md), and the recommended option becomes a row in [roadmap.md](roadmap.md).

- [ ] Do nothing is a row with a cost, not a zero
- [ ] Every benefit line names a method the finance partner has read
- [ ] Build cost comes from a range, and the range appears in section 5
- [ ] Payback or NPV is computed on stated inputs, labeled ILLUSTRATIVE until the method is agreed
- [ ] At least one sensitivity flips the recommendation, or the document says why none does
- [ ] The ILLUSTRATIVE example rows have been deleted, so every row left is this initiative's own
- [ ] The recommendation names what it gives up, its door type, and its reversal trigger
- [ ] Every input in sections 3 and 5 has a row in [assumptions-register.md](../definition/assumptions-register.md) with a source and a confidence
- [ ] The BRD's financial case copies the winning option's numbers rather than recomputing them
- [ ] Signed by [name], [date]
