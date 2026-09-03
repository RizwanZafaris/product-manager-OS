# North Star Sheet: [product name]

**Stage:** PLANNING track (feeds every stage of the [operating loop](../../os/OPERATING-LOOP.md))
**Knowledge:** [north star metric](../../knowledge/north-star-metric.md)
**Skill:** [metrics-tree](../../skills/metrics-tree/SKILL.md)

<!-- The knowledge card explains the method and its trap; this sheet is where the
     choice is made and defended. One metric that expresses delivered customer value,
     a small tree of inputs teams can actually move, and a review cadence that tests
     whether the tree's causal claims survived contact with reality.

     Two disciplines. First, the vanity test is answered in writing: if every
     customer silently stopped benefiting tomorrow, this number must fall within the
     quarter. Second, every input has exactly one owner; an input owned by "growth"
     is owned by nobody on a Tuesday. -->

**Owner:** [name] · **Last updated:** [YYYY-MM-DD] · **Vision:** [this product's vision doc](vision.md)

## 1. The metric

| Field | Answer |
|---|---|
| North star metric | [name, with unit and period, e.g. "weekly orders delivered on time"] |
| The customer value it expresses | [what the customer got when this ticks up] |
| Vanity test | [why this falls within a quarter if customers stop benefiting; if you cannot write this, the metric fails] |
| Source system | [where the number is computed; "not yet instrumented" fails, see the card's skip-it-when] |
| Current value | [number, with date] |

## 2. Input metric tree

<!-- Three to five inputs, each a dial one team can move, with the causal claim to
     the north star written down. The claim column is the point: an input without a
     stated mechanism is a metric that happened to be on a dashboard. -->

| Input metric | Causal claim (how it feeds the north star) | Owner (one name) | Current | Target |
|---|---|---|---|---|
| | | | | |
| | | | | |
| *search-to-order conversion* | *more completed searches become orders, and orders are the unit the north star counts* | *[name]* | *2.8%* | *4%* |

## 3. Guardrails

<!-- The metrics allowed to veto a north star win. A north star can be moved by
     methods that quietly spend trust: discounts, dark patterns, load-shedding
     quality. Each guardrail names its floor and who halts work when it is crossed. -->

| Guardrail metric | Floor or ceiling | Who calls the halt | Why it guards |
|---|---|---|---|
| | [number, with unit] | [name] | [what bad win it prevents] |

## 4. Review cadence

<!-- The tree is a set of hypotheses, and hypotheses expire. On each review, the
     question is not only "did the inputs move" but "did the north star follow", which
     is the causal claim on trial. Feed results into the
     [metrics review](../operate/metrics-review.md). -->

- **Cadence:** [e.g. monthly, plus each Gate 6]
- **Standing questions:** did each input move; did the north star follow; which causal claim looks weakest; what replaces it if it fails
- **Last review:** [date, link to the filled metrics review]
- **Next review:** [date, name of who runs it]

## Exit gate

This sheet is fit to steer by when:

- [ ] The north star passes the written vanity test and is computed by a named source system
- [ ] Every input carries a causal claim and exactly one named owner
- [ ] There are three to five inputs, not a dashboard's worth
- [ ] At least one guardrail exists, with a numeric floor and a named halt-caller
- [ ] The review cadence is scheduled with an owner, not left as an intention
- [ ] OKRs and PRD success metrics in flight trace to this tree, or the mismatch is logged

Signed: [name], [role], [YYYY-MM-DD]
