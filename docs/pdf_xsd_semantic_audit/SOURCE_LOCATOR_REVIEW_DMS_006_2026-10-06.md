# Source-locator review — DMS-006 — 2026-10-06

Status: **complete / visible-body verified / V2.2 PDF-XSD cardinality mismatch confirmed**.

## Result

DMS-006 is a confirmed V2.2 documentation defect.

- V2.2 PDF Table 20 visibly shows only `DeviceStatusName 1:1` and `DeviceStatusFlag 1:1`.
- The selected official V2.2 XSD also requires `DeviceStatusImpact` and `DeviceStatusPriority`.
- V2.4 later documents Impact/Priority as optional and its candidate/integration XSD uses `minOccurs="0"` for both.

## Exact XSD evidence

V2.2 official blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, lines 403-410:
Name, Flag, Impact and Priority are all required.

V2.4 candidate/integration blob `d222dfd98b2be3777576388da7ace8f333d24c3f`, lines 403-410:
Impact and Priority are optional.

EV-127 confirms:
- V2.2 Name+Flag only -> invalid;
- V2.2 four-field shape -> valid;
- V2.4 candidate/integration two-field and four-field shapes -> valid.

## Consequence

For V2.2 the selected XSD remains normative: Impact and Priority must be present. V2.4 optionality must not be back-applied. The separate V2.4 PDF typo `eDeviceStatusPriority` remains a distinct documentation finding and creates no alias.
