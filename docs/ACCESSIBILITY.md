# Operator Documentation Accessibility

## Scope

This repository's operator documentation is Markdown. The local contract
checks heading order, non-empty image alternative text, descriptive link text,
and local link resolution for the primary operator documents. It is a local
evidence check, not external evidence of assistive-technology usability.

## Reading and operating the system

Use the [operating loop](../os/OPERATING-LOOP.md) for lifecycle decisions, the
[security guide](../SECURITY.md) for credential and provider boundaries, and
the [threat model](THREAT-MODEL.md) for what local tests do not prove. The
documented API paths are `pmos/domain.py`, `pmos/store.py`, `pmos/hooks.py`,
and `pmos/openrouter.py`; the documented command-line entry point is
`pmos/cli.py`.

## Evidence limits

Local evidence is not external evidence. A passing documentation check does
not prove a live sandbox is accessible, a provider is accessible, users can
complete a task, or a regulatory requirement is satisfied. Those require
separate observed and recorded evidence.

## Authoring rules

- Use a single H1 and do not skip heading levels.
- Give every meaningful image concise alternative text; use no image for purely
  decorative information that must be understood to operate the system.
- Use destination-specific link labels rather than "click here" or "more".
- State the actor, action, evidence, and boundary in operational instructions.
