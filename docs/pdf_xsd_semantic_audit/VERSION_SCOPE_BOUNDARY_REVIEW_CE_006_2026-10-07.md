# Version-scope boundary review — CE-006 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-006` is the confirmed DeviceStateEnumeration documentation/XSD mismatch for `warning`.

## Lower boundary
The V2.1 -> V2.2 historical audit proves that `warning` is added in Enumerations V2.2. V2.1 therefore cannot carry this specific mismatch because the XSD value does not yet exist there.

V2.2 is the first affected version:
- the exact Enumerations V2.2 XSD contains `warning`;
- the V2.2 DeviceStateEnumeration PDF table omits it.

## Continuity
- V2.3 reuses the exact Enumerations V2.2 dependency pool, so `warning` remains valid in the selected XSD while the V2.3 PDF table still omits it.
- V2.4 official documentation still omits `warning`.
- the explicitly selected V2.4 candidate/integration Enumerations XSD contains `warning`.

## Upper boundary
VDV-301-2.3 remains the latest official release. The V2.4 executable XSD lane remains candidate/integration authority only.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Enumerations V2.2-V2.3 — official release authority;
2. Enumerations V2.4 — candidate/integration authority.

V2.1 is an explicit unaffected predecessor for this specific finding.

## Consequence
When the exact selected XSD accepts `warning`, the value is schema-valid even though the corresponding PDF table omits it. The tool may explain the documentation gap but must not reject or rewrite the XSD-valid value.
