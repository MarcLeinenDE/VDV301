# Version-scope boundary review — ARCH-003 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-003` is a confirmed non-defect/context finding. VDV 301-1 defines each vehicle as its own closed IBIS-IP system while explicitly allowing another coupled vehicle to be linked as a separate IBIS-IP system through corresponding interfaces. A closed system boundary is therefore not a communication prohibition.

The canonical German V1.0 source remains the normative, byte-pinned, visible-body-verified locator authority.

## Publication-lineage check
The current VDV IP-KOM-ÖV publication index lists only the German VDV 301-1 and its English translation, with no later VDV 301-1 architecture version.

The English document identifies itself as a translation of the German V1.0 document released January 2014 and states that the German original prevails.

## Independent English-language control
The English V1.0 page-16 text independently states that:
- each vehicle by itself represents a closed IBIS-IP system;
- the coupled vehicle is another IBIS-IP system;
- corresponding interfaces must be provided for that link.

This matches the German ARCH-003 interpretation exactly.

The interactive screenshot path for the English PDF returned cache-miss and direct external byte download was unavailable. Therefore English remains a content-level supporting language control and is not promoted to a new visible-body locator lane.

## Boundary conclusion
- predecessor architecture publication: none available;
- first/last applicable version: V1.0;
- successor architecture publication: none available;
- German: normative original;
- English: same V1.0 system-boundary semantics independently confirmed; German original prevails.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
Do not interpret the vehicle system boundary as a ban on inter-vehicle communication. The architecture explicitly permits links to another IBIS-IP system through defined interfaces.
