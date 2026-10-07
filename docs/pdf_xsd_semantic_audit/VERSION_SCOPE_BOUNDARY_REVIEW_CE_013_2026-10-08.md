# Version-scope boundary review — CE-013 — 2026-10-08

Status: **verified / scope unchanged**.

## Finding
`CE-013` contains two independent AdditionalAnnouncement PDF/XSD boundaries:
1. the PDF names the third choice branch `InformationAtSpecificPoint`, while the exact selected XSD names it `SpecificPoint`;
2. the PDF presents a mandatory one-of choice, while the exact selected XSD makes the whole `xs:choice` optional with `minOccurs="0"`.

The exact selected XSD remains the executable XML authority for both boundaries.

## Lower boundary
Both mismatches are already present in Common V1.0, the earliest retained Common publication available to this audit:
- PDF: mandatory choice and `InformationAtSpecificPoint`;
- XSD: optional choice and `SpecificPoint`.

No earlier retained Common publication exists from which an unaffected predecessor could be established.

## Continuity
Both boundaries persist independently through Common V2.0, V2.1, V2.2 and V2.3.

The official V2.4 PDF still presents the mandatory choice and `InformationAtSpecificPoint`; the explicitly selected candidate/integration Common V2.4 XSD still uses optional `xs:choice` and `SpecificPoint`.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Common V1.0-V2.3 — official release/historical selected authority;
2. Common V2.4 — candidate/integration authority.

There is no earlier retained Common publication to use as a predecessor control.

## SDK consequence
The PDF name `InformationAtSpecificPoint` must not be accepted or normalized as an alias for XSD `SpecificPoint`. Conversely, absence of the whole choice must not be rejected beyond the exact selected XSD: where the XSD accepts an AdditionalAnnouncement without a choice branch, the normative XML result remains valid. CE-013 explains both boundaries without overriding XSD validation.
