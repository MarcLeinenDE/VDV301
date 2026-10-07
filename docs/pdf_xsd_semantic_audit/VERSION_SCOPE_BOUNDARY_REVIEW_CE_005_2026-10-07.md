# Version-scope boundary review — CE-005 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-005` is the confirmed cross-artifact cardinality mismatch for `TripInformation.AdditionalTextMessage`: affected PDFs document repeatability (`0:*` / unbounded) while the exact selected XSDs allow at most one instance per named element.

## Lower boundary
The public Common V1.0 URL is a consolidated V1.x/V1.1-era source and is not used as a clean untouched V1.0 baseline.

That ambiguity does not leave the CE-005 start boundary open, because the official version history explicitly places the relevant documentation change in **Version 2.0**:

`TripInformation structure: AdditionalTextMessage: maxOccurs="unbounded" updated`.

Therefore V2.0 is the first evidence-backed affected documentation version for this mismatch.

## Continuity
Existing exact source-locator evidence proves:
- V2.0: PDF 0:* versus XSD max 1;
- V2.1: mismatch persists;
- V2.2: mismatch persists;
- V2.3: mismatch persists; numbered fields are added but every named field remains individually bounded;
- V2.4: official PDF still documents repeatability while the explicitly selected candidate/integration Common V2.4 XSD keeps each named field bounded to one.

## Upper boundary
VDV-301-2.3 remains the latest official GitHub release. Common V2.4 documentation is official, but the selected V2.4 XSD lane remains candidate/integration authority rather than an official VDV-301-2.4 release.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Common V2.0-V2.3 — official release authority;
2. Common V2.4 — candidate/integration XSD authority with official PDF documentation.

No V1.x scope is added.

## Consequence
Validation continues to follow the exact selected XSD. Repeated `AdditionalTextMessage` elements rejected by that XSD remain FAIL; the PDF mismatch is explanatory only.
