# Version-scope boundary review — ARCH-008 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-008` is a confirmed architecture-context non-defect. The functional-component vocabulary in VDV 301-1 is intentionally broader than concrete executable service identity.

## Publication-lineage check
Current VDV publication surfaces expose only VDV 301-1 V1.0 in German plus its English convenience translation. No predecessor or successor architecture version is published.

## Independent English-language control
The English terminology section independently states that a functional component represents encapsulated functionality independent of implementation and can be, among other things, an abstract interface, application, service or device. It then explicitly states that only part of the functional components are specified and implemented as services or applications.

German V1.0 remains normative and byte-pinned; English is supporting language control.

## Boundary conclusion
- predecessor: none available;
- first/last applicable architecture version: V1.0;
- successor: none available;
- German: normative original;
- English: same broader-than-service component semantics independently confirmed.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
A functional-component label must never be synthesized into a service identifier, endpoint, mandatory operation or XML root without separate explicit Part-2/discovery/XSD authority.
