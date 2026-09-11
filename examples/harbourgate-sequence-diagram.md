# Sequence Diagram: Harbourgate web and app card authorisation

Fills [templates/architecture/sequence-diagram.md](../templates/architecture/sequence-diagram.md). Everything here is invented: Harbourgate, Quay and Kestrel are fictional, Bea Lindqvist is fictional, and every number, date, amount, rate and identifier is ILLUSTRATIVE, drawn from the [Harbourgate journey](harbourgate-journey.md) and [coverage sheet](harbourgate-coverage-sheet.md), never to be quoted as a benchmark or copied as a target.

**Owner:** Bea Lindqvist, Senior Engineer, payments · **Date:** 2026-04-09 · **Status:** Gate 3 architecture review · **Story:** [HARBOURGATE-S1](harbourgate-journey.md) · **Supplement:** [HC5](harbourgate-coverage-sheet.md)

## Conventions

1. Synchronous calls carry their timeout: `authorise (t/o 20 s)`.
2. Asynchronous messages name the queue or topic in the label.
3. In the failure and timeout diagrams (Section 2 onward), every `alt` block has at least one failure branch. An `alt`/`else` used only to split Web from App channels, with both arms on the happy path, carries no failure branch by itself (Section 1).
4. Participants use the system names from the solution architecture one-pager: Web checkout, App, Quay, Kestrel hosted fields, Kestrel, and Order service.
5. The web and app clients wait 20 s for Quay. Quay's Kestrel call policy is an 8 s timeout, followed by one retry after 2 s on a network error, for a worst case of 18 s, from N61 and HC5.
6. Card data is entered into Kestrel hosted fields. The card number does not reach a Harbourgate server, satisfying AC-1.

## 1. Happy path

The web and app clients submit a token from Kestrel hosted fields to Quay. Quay authorises through Kestrel, writes its ledger row in the same transaction as the call outcome, and preserves the legacy table shape for the order service.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant W as Web checkout
    participant A as App
    participant H as Kestrel hosted fields
    participant Q as Quay
    participant K as Kestrel
    participant O as Order service

    alt Web checkout
        U->>W: enter card details
        W->>H: render hosted fields
        H-->>W: payment token
        W->>Q: authorise token (t/o 20 s)
    else App
        U->>A: enter card details
        A->>H: render hosted fields
        H-->>A: payment token
        A->>Q: authorise token (t/o 20 s)
    end

    Q->>K: authorise token (t/o 8 s)
    K-->>Q: authorisation result
    Q->>Q: write ledger row in the same transaction as the authorisation call
    Q-->>W: authorised result
    Q-->>A: authorised result
    Q-)O: status webhook topic, payment.authorised
    W-->>U: confirmation
    A-->>U: confirmation
```

For a card-not-present order above £250, or any order flagged by a fraud rule, Quay returns `requires_action` and the client presents Kestrel's hosted step-up challenge. This is BR-005 and HARBOURGATE-S10.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant W as Web checkout
    participant A as App
    participant Q as Quay
    participant H as Kestrel hosted fields
    participant K as Kestrel
    participant O as Order service

    alt Web checkout requires step-up
        W->>Q: authorise token (t/o 20 s)
        Q->>K: authorise token (t/o 8 s)
        K-->>Q: requires_action
        Q-->>W: requires_action
        W->>H: start hosted step-up challenge
        H-->>W: challenge result
        W->>Q: complete authorisation (t/o 20 s)
        Q->>K: complete authorisation (t/o 8 s)
        K-->>Q: authorised result
        Q->>Q: write ledger row in the same transaction as the authorisation call
        Q-)O: status webhook topic, payment.authorised
        Q-->>W: authorised result
        W-->>U: confirmation
    else App requires step-up
        A->>Q: authorise token (t/o 20 s)
        Q->>K: authorise token (t/o 8 s)
        K-->>Q: requires_action
        Q-->>A: requires_action
        A->>H: start hosted step-up challenge
        H-->>A: challenge result
        A->>Q: complete authorisation (t/o 20 s)
        Q->>K: complete authorisation (t/o 8 s)
        K-->>Q: authorised result
        Q->>Q: write ledger row in the same transaction as the authorisation call
        Q-)O: status webhook topic, payment.authorised
        Q-->>A: authorised result
        A-->>U: confirmation
    end
```

## 2. Failure and timeout paths

A decline is a business response, not a transport failure. Quay returns `402`, the client does not resubmit the same card automatically, and the user sees an actionable decline with an offer to use a different method. This implements BR-001 and AC-5.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant W as Web checkout
    participant A as App
    participant Q as Quay
    participant K as Kestrel

    alt Web checkout
        W->>Q: authorise token (t/o 20 s)
        Q->>K: authorise token (t/o 8 s)
        K-->>Q: declined
        Q-->>W: 402 decline with reason class
        W-->>U: card declined, choose a different method
        Note over W,Q: Never resubmit the same card automatically
    else App
        A->>Q: authorise token (t/o 20 s)
        Q->>K: authorise token (t/o 8 s)
        K-->>Q: declined
        Q-->>A: 402 decline with reason class
        A-->>U: card declined, choose a different method
        Note over A,Q: Never resubmit the same card automatically
    end
```

A Kestrel timeout is retried once after 2 s, with the same idempotency key, only for the network-error case. The Kestrel call policy is 8 s, so the worst case is `8 s + 2 s + 8 s = 18 s`. The client timeout is 20 s, leaving time for Quay to return `503` if the same-key retry also times out.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant W as Web checkout
    participant A as App
    participant Q as Quay
    participant K as Kestrel

    alt Web checkout
        W->>Q: authorise token, idempotency key (t/o 20 s)
        Q->>K: authorise token, same key (t/o 8 s)
        alt Kestrel responds
            K-->>Q: authorisation result
            Q-->>W: result
            W-->>U: confirmation or decline
        else Kestrel network timeout
            Q->>K: retry once, same idempotency key, after 2 s (t/o 8 s)
            alt Retry succeeds
                K-->>Q: authorisation result
                Q-->>W: result
                W-->>U: confirmation or decline
            else Retry also times out
                Q-->>W: 503 service unavailable
                W-->>U: payment still processing, reference shown
            end
        end
    else App
        A->>Q: authorise token, idempotency key (t/o 20 s)
        Q->>K: authorise token, same key (t/o 8 s)
        alt Kestrel responds
            K-->>Q: authorisation result
            Q-->>A: result
            A-->>U: confirmation or decline
        else Kestrel network timeout
            Q->>K: retry once, same idempotency key, after 2 s (t/o 8 s)
            alt Retry succeeds
                K-->>Q: authorisation result
                Q-->>A: result
                A-->>U: confirmation or decline
            else Retry also times out
                Q-->>A: 503 service unavailable
                A-->>U: payment still processing, reference shown
            end
        end
    end
```

Kestrel sends the status webhook asynchronously. If the webhook is missed, the client resolves the pending state with a status poll after 30 s. The poll's client timeout is governed by the client status-call setting, which is not specified in the supplied data.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant W as Web checkout
    participant Q as Quay
    participant K as Kestrel
    participant O as Order service

    W->>Q: authorise token (t/o 20 s)
    Q->>K: authorise token (t/o 8 s)
    K-->>Q: authorised, webhook pending
    Q->>Q: write ledger row in the same transaction as the authorisation call
    Q-->>W: pending result
    W-->>U: payment processing, reference shown
    alt Status webhook arrives
        K-)Q: status webhook topic, payment.status
        Q-)O: status webhook topic, payment.status
        Q-->>W: status update
        W-->>U: final payment outcome
    else Status webhook missed
        W->>Q: poll status after 30 s (t/o per client status setting)
        Q-->>W: final payment outcome
        W-->>U: final payment outcome
    end
```

## 3. Open questions from drawing the flow

| Question surfaced | Owner | Moved to (decision log / risk register row) |
|---|---|---|
| What happens if a web or app client retries the authorisation with a new idempotency key after receiving `503` or remaining in a pending state? | Bea Lindqvist | Risk register R1, the duplicate-authorisation risk; dispositioned for the R1 control and review |

## Exit gate

- [x] Every synchronous call shows a timeout, or explicitly identifies the supplied client setting where the value is not specified
- [x] Every flow has at least one failure or timeout diagram, not just the happy path
- [x] Each failure branch shows what the user or caller sees
- [x] Retries state their idempotency mechanism
- [x] Participant names match the solution architecture one-pager
- [x] Section 3 questions are all dispositioned to a log or register

Signed at Gate 3, 2026-04-09: Bea Lindqvist, Senior Engineer, payments.
