# Source-locator review — CE-015 — 2026-09-28

Status: **terminally validated / complete**.

## Finding

CE-015 records the case-sensitive XML identifier mismatch in `FareZoneInformation`.

The official PDFs use `FarezoneID`, `FarezoneType`, `FarezoneLongName` and `FarezoneShortName`. The exact selected XSDs use `FareZoneID`, `FareZoneType`, `FareZoneLongName` and `FareZoneShortName`.

Because XML element names are case-sensitive, the PDF spelling is not schema-equivalent.

## Version-specific source matrix

| Profile | Authority | PDF | Section / table | XSD |
|---|---|---:|---|---|
| Common V1.0 | official release | p. 14 | 1.26 / Table 26 | IBIS-IP_common_V1.0.xsd |
| Common V2.0 | official release | p. 21 | 2.26 / Table 26 | IBIS-IP_common_V2.0.xsd |
| Common V2.1 | official release | p. 23 | 2.26 / Table 26 | IBIS-IP_common_V2.1.xsd |
| Common V2.2 | official release | p. 24 | 2.26 / Table 26 | IBIS-IP_common_V2.2.xsd |
| Common V2.3 | official release | p. 24 | 2.26 / Table 26 | IBIS-IP_common_V2.3.xsd |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 26 | 2.26 / Table 26 | IBIS-IP_common_V2.4.xsd |

All four exact XSD members are individually located for every version.

## Conformance rule

The selected XSD remains the executable XML authority. A provider payload using the PDF spelling `Farezone*` fails schema validation where the selected XSD requires `FareZone*`. The diagnostic may explain the documentation mismatch but must not waive the FAIL.

The V2.4 XSD lane remains explicitly candidate/integration and is not promoted to official-release authority.

## Historical rule

Any later correction of this spelling must not remove or reinterpret CE-015 for an older affected profile. Later corrections are version-history evidence only.

## Validation

The persisted entry was re-read from the branch and checked against the locator JSON schema, semantic-registry scope, exact selected XSD blobs/components, manifest counters and both CURRENT_STATE counter surfaces. The six version lanes match the semantic scope and contain 24 exact XSD member locators. No stale counter or scope divergence was found.

## State

Canonical source-locator manifest after validation: **11 complete / 0 partial / 181 remaining**.

No XSD, semantic classification, runtime disposition or PASS/FAIL rule was modified in this block.
