# Version-scope boundary review — ARCH-005 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-005` is a confirmed architecture-context non-defect. VDV 301-1 distinguishes rapidly changing information suited to UDP/UDP multicast from longer-valid information that requires reliable transfer via TCP/HTTP. This is architecture-level communication guidance, not a universal hard rule for every service or packet.

## Publication-lineage check
The current VDV publication index exposes only VDV 301-1 V1.0 in German plus its English convenience translation. No predecessor or successor architecture version is currently published.

## Independent English-language control
The English V1.0 text independently states that rapidly changing information is best suited to UDP and UDP multicast, while longer-valid reliable information is transmitted using TCP/HTTP. The same passage explicitly points to VDV 301-2 for further detail.

German V1.0 remains the normative, byte-pinned, visible-body-verified authority; the English text is supporting language control.

## Boundary conclusion
- predecessor: none available;
- first/last applicable version: V1.0;
- successor: none available;
- German: normative original;
- English: same architecture semantics independently confirmed.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
Concrete transport requirements must still be derived from the applicable Part-2/service authority. ARCH-005 does not authorize a global per-service/per-packet transport hard-fail.
