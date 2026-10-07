# Version-scope boundary review — CE-009 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-009` is the confirmed RailSubmode lexeme mismatch:
- PDF: `specialRail`
- exact selected XSD: `specialTrain`

XML enumeration values are case- and lexeme-sensitive.

## Lower boundary
The V2.1 -> V2.2 historical audit proves that the affected Netex mode/submode enumeration family is introduced in V2.2. V2.1 is therefore an unaffected predecessor for this specific finding.

V2.2 is the first affected version:
- the V2.2 RailSubmode PDF table uses `specialRail`;
- exact Enumerations V2.2 uses `specialTrain`.

## Continuity
- V2.3 PDF still uses `specialRail`; its dependency route reuses exact Enumerations V2.2 containing `specialTrain`.
- V2.4 official PDF still uses `specialRail`; the explicitly selected candidate/integration Enumerations V2.4 XSD uses `specialTrain`.

## Upper boundary
VDV-301-2.3 remains the latest official release. The V2.4 executable XSD lane remains candidate/integration authority only.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Enumerations V2.2-V2.3 — official release authority;
2. Enumerations V2.4 — candidate/integration authority.

## Consequence
For XML, `specialTrain` from the exact selected XSD remains authoritative. `specialRail` from the PDF must not be accepted or normalized as an alias.
