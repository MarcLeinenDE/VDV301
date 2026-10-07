# Version-scope boundary review — CE-010 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-010` is the confirmed AirSubmode documentation/XSD mismatch:
- the affected PDF AirSubmode tables omit `canalBarge`;
- the exact selected XSD contains `canalBarge` and therefore accepts it.

The selected XSD remains the executable XML authority. The PDF omission may explain the discrepancy but cannot make an XSD-valid `canalBarge` value invalid.

## Lower boundary
Exact `IBIS-IP_Enumerations_V2.1.xsd` contains neither `AirSubmodeEnumeration` nor `canalBarge`. The affected Netex/TPEG submode enumeration family is introduced with V2.2.

V2.2 is therefore the first affected version:
- the official V2.2 PDF AirSubmode table omits `canalBarge`;
- exact Enumerations V2.2 contains `canalBarge` (annotated as not in TPEG).

## Continuity
- V2.3 PDF still omits `canalBarge`; its exact dependency route reuses Enumerations V2.2 containing the value.
- V2.4 official PDF still omits `canalBarge`; the explicitly selected candidate/integration Enumerations V2.4 XSD still contains the value.

## Upper boundary and authority
The VDVde/VDV301 releases were rechecked on 2026-10-07: VDV-301-2.3 remains the latest official GitHub release. Upstream master remains at `14880bb33beec5c5dffe96315b730bd6c094a585`. The V2.4 executable XSD lane therefore remains candidate/integration authority only and is not promoted to official-release authority.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Enumerations V2.2-V2.3 — official release authority;
2. Enumerations V2.4 — candidate/integration authority.

V2.1 is an explicit unaffected predecessor.

## SDK consequence
`canalBarge` must remain valid whenever the exact selected XSD accepts it. CE-010 may decorate that valid result with the existing Known-Issue advisory explaining the PDF omission. No aliasing, normalization or additional rejection is permitted.
