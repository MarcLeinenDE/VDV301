# Version-scope boundary review — CE-008 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-008` is the confirmed case-sensitive PDF/XSD mismatch in Netex submode enumerations:
- FunicularSubmode: PDF `Unknown` vs XSD `unknown`;
- TaxiSubmode: PDF `Unknown`, `Undefined`, `minicab` vs XSD `unknown`, `undefined`, `miniCab`.

## Lower boundary
The V2.1 -> V2.2 historical audit proves that the affected Netex mode/submode enumerations are introduced in V2.2. V2.1 is therefore an unaffected predecessor for this specific finding.

## Continuity
- V2.2 official PDF/XSD shows the mismatch.
- V2.3 official PDF retains the same spellings and its dependency route reuses exact Enumerations V2.2.
- V2.4 official PDF retains the same spellings; the explicitly selected V2.4 candidate/integration Enumerations XSD retains the XSD lexemes.

## Upper boundary
VDV-301-2.3 remains the latest official release. The V2.4 XSD lane remains candidate/integration authority only.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Enumerations V2.2-V2.3 — official release authority;
2. Enumerations V2.4 — candidate/integration authority.

## Consequence
The exact selected XSD lexemes remain authoritative and case-sensitive. PDF spellings must not be accepted as aliases.
