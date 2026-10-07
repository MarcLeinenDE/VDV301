# Version-scope boundary review — ARCH-006 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-006` is a confirmed architecture-context non-defect and an important authority boundary: VDV 301-1 defines the architecture and establishes XML-based information exchange, while VDV 301-2 provides the technical interface/XML structures. Part 1 is not a replacement schema.

## Publication-lineage check
Current VDV publication surfaces expose only VDV 301-1 V1.0 in German plus its English convenience translation. No predecessor or successor architecture version is published.

## Independent English-language control
The English V1.0 introduction independently states that Part 1 defines the system architecture and Part 2 specifies implementation of the technical interface based on XML structures. Section 7.1 independently states that XML is used for transfer of information between two IBIS-IP services.

German V1.0 remains the normative, byte-pinned, visible-body-verified source; English is supporting language control.

## Boundary conclusion
- predecessor: none available;
- first/last applicable architecture version: V1.0;
- successor: none available;
- German: normative original;
- English: same authority split independently confirmed.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
XML validity must continue to follow the exactly selected applicable Part-2 XSD. Part 1 provides architecture context and must never override, normalize or repair that selected schema.
