# Version-scope boundary review — CE-007 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-007` is the confirmed case-sensitive PDF/XSD mismatch for selected enumeration lexemes including:
- GNSSTypeEnumeration: PDF `Other` vs XSD `other`;
- TicketValidationEnumeration: PDF `Valid` vs XSD `valid`;
- VehicleModeEnumeration: PDF `Air` vs XSD `air`.

XML enumeration values are case-sensitive.

## Lower boundary
The earliest available Common/Enumerations publication and official release-tag XSD lane is V1.0.

Exact V1.0 source-locator evidence already proves the mismatch:
- PDF tables use `Other`, `Valid`, `Air`;
- official Enumerations V1.0 uses `other`, `valid`, `air`.

No earlier Common/Enumerations publication is present in the current VDV publication lineage.

## Continuity
The same case mismatch is directly located in:
- V2.0 official PDF/XSD;
- V2.1 official PDF/XSD;
- V2.2 official PDF/XSD;
- V2.3 official PDF plus its exact V2.2 enumeration dependency pool;
- V2.4 official PDF plus the explicitly selected candidate/integration Enumerations V2.4 XSD.

## Upper boundary
VDV-301-2.3 remains the latest official release. V2.4 is an official documentation publication with candidate/integration executable XSD authority.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Enumerations V1.0-V2.3 — official release authority;
2. Enumerations V2.4 — candidate/integration authority.

## Consequence
Validation must use the exact case-sensitive XSD lexeme. PDF capitalization is explanatory documentation evidence only and must not be accepted as an alias.
