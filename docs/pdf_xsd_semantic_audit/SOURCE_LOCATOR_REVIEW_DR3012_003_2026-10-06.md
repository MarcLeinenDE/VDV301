# Source-locator review — DR3012-003 — 2026-10-06

Status: **complete / visible-body verified / exact official XSD authority verified / executable finding preserved**.

## Finding

VDV 301-2 V1.0 documents the SystemDocumentation heartbeat interval with a misspelled XML identifier and, for one structure, the wrong type.

The explicit correction delta
`AUDIT_CORRECTION_DELTA_DR3012_003_V10_IDENTIFIER_TYPE_2026-09-03.md`
controls over the older imprecise claim that the same misspelling existed in the XSD.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **65**

### Table 25 — SystemDocumentationService.SystemConfigurationData

Visible row:
- identifier: `HertbeatIntervall`
- cardinality: `0:1`
- type: `IBIS-IP.duration`

### Table 26 — SystemDocumentationService.StoreSystemConfigurationRequest

Visible row:
- identifier: `HertbeatIntervall`
- cardinality: `0:1`
- type: `IBIS-IP.duration`

Exact-byte EV-129 page-65 PNG SHA-256:
`1bf5fc05dcc3313bc74ff8994187fedaea0249fb2c9bc1a723a6fd37abff0b36`

The page hash was freshly recomputed from artifact `9897171006` and matches the EV-129 manifest.

## Exact XSD authority

Selected historical schema:
- file: `IBIS-IP_SystemDocumentationService_v1.0.xsd`
- local Git blob: `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`
- official upstream repository: `VDVde/VDV301`
- official tag: `VDV-301-1.0`
- official upstream blob: `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`

The local and official-tag blobs are byte-identical.

The exact XSD declares:

1. `SystemDocumentationService.SystemConfigurationData/HeartbeatIntervall`
   - `type="IBIS-IP.double"`
   - `minOccurs="0"`
   - line hint 43

2. `SystemDocumentationService.StoreSystemConfigurationRequestStructure/HeartbeatIntervall`
   - `type="IBIS-IP.duration"`
   - `minOccurs="0"`
   - line hint 50

No `HertbeatIntervall` element exists in the selected XSD.

## Correct comparison

For `SystemConfigurationData`:
- PDF: `HertbeatIntervall` + `IBIS-IP.duration`
- XSD: `HeartbeatIntervall` + `IBIS-IP.double`
- mismatch: **identifier and type**

For `StoreSystemConfigurationRequestStructure`:
- PDF: `HertbeatIntervall` + `IBIS-IP.duration`
- XSD: `HeartbeatIntervall` + `IBIS-IP.duration`
- mismatch: **identifier only**

## Active disproof attempt

The exact historical official-tag file was freshly re-read. It does not support the old claim that `HertbeatIntervall` also exists in XSD. The explicit correction trail is therefore necessary and remains controlling.

The type mismatch cannot be generalized across both structures: `duration` is correct in the XSD for StoreSystemConfigurationRequestStructure but not for SystemConfigurationData.

## Executable behavior

EV-129 already confirms the selected-XSD boundary:

- correctly spelled `HeartbeatIntervall` with numeric `Value` is accepted for the XSD `IBIS-IP.double` lane;
- duration lexical value `PT5S` is rejected in that double lane;
- misspelled `HertbeatIntervall` is rejected;
- the `IBIS-IP.duration` control accepts `PT5S`.

No new executable rule is synthesized here; the existing EV-129 evidence is preserved.

## Classification and SDK behavior

Confirmed PDF/XSD identifier mismatch plus a structure-specific type mismatch.

- selected official XSD remains normative;
- an instance following the PDF typo/type where it conflicts with XSD is **FAIL**;
- SDK behavior: **XSD error with explanatory advisory**;
- no typo alias, normalization, waiver or PDF-driven schema override is allowed.
