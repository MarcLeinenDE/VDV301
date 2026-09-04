# Finding revalidation — COMMON V1.0

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy findings: `DRCOM10-001` … `DRCOM10-007`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V1.0 PDF: SHA-256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`, 892769 bytes.
- Exact official historical Common V1.0 blob: `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`.
- Exact official historical Enumerations V1.0 blob: `a9bea5bc73003ed91ded8519db06c32c4067831d`.
- Historical upstream import commit: `604a5a5c7608977e483072f7e450d7381cc182e4`.
- No synthetic Common V1.1 XSD authority is inferred from the document's internal Version 1.1 history.
- Preserved EV-117 was rerun unchanged and passed.
- Current evidence: **EV-135**, successful closure rerun **33850713729**; pinned visual/evidence artifact run **33850418941**, artifact **9928121371**.
- Visual page fallbacks are explicit, not inferred text matches: DRCOM10-002 page 9 and DRCOM10-005 page 18.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM10-001 | `executable_confirmed` | Document Version 1.1 changes are visibly present, while the exact V1.0 XSD remains the historical authority. Required DisplayContent/legacy spelling boundaries and absence of V1.1 aliases/additions are executable-confirmed. |
| DRCOM10-002 | `executable_confirmed` | PDF page 9 prints the two DataAcceptedResponse branches as ordinary rows; exact XSD uses `xs:choice`. Either branch validates alone and both together are rejected. |
| DRCOM10-003 | `executable_confirmed` | PDF prints ServiceSpecificationWithStateList as `1:*`; exact XSD is `0:*`, and an empty list validates. |
| DRCOM10-004 | `executable_confirmed` | PDF prints JourneyStopInformation Announcement/FareZone as `0:*`; exact XSD is `0:1`. One validates and two repeated instances are rejected for both fields. |
| DRCOM10-005 | `executable_confirmed` | PDF page 18 uses inner `ShortTripStopList` / `StopPointTariffInformation`; exact XSD uses `ShortTripStop` / `ShortTripStopStructure`. The child-name boundary is executable-confirmed; the two type alternatives are instance-shape equivalent and therefore not overstated as a separate instance distinction. |
| DRCOM10-006 | `executable_confirmed` | PDF `Wheelchair` / `Others` differ from exact enum lexemes `WheelChair` / `Other`; positive/negative enum probes confirm the boundary. |
| DRCOM10-007 | `context_verified` | Grouped editorial spelling/naming residue is visibly confirmed and does not define XML validity behavior or aliases. |

## Closure

- Frozen legacy terminal count: **91 / 192**
- Frozen legacy pending count: **101 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V2.0** (`DRCOM20-001`)
