# Audit Correction Delta — DR3012-003 VDV 301-2 V1.0

Date: 2026-09-03
Branch: `dev/schema-integration`
Finding: `DR3012-003`
Evidence: `EV-129`, run `33765167655`

## Purpose

This correction preserves the historical Deep Read record while correcting one imprecise subclaim found during mandatory legacy-finding revalidation under the current Evidence Gate.

The original Deep Read correctly identified a material PDF/XSD discrepancy around the SystemDocumentation system-configuration heartbeat interval, but it additionally stated that the spelling `HertbeatIntervall` appeared in both the PDF and the XSD. That spelling subclaim is not supported by the exact selected XSD authority.

## Original imprecise subclaim

The historical Deep Read states:

`The misspelling HertbeatIntervall appears in both PDF and XSD.`

This sentence is superseded by the correction below. It is not silently rewritten because the audit requires an explicit correction trail.

## Corrected evidence

Byte-pinned official VDV 301-2 V1.0 PDF:

- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- size: `1790447` bytes
- targeted visible page: 65

Visible PDF page 65 contains two rows named `HertbeatIntervall`, both documented as `IBIS-IP.duration`:

1. `SystemDocumentationService.SystemConfigurationData/HertbeatIntervall`
2. `SystemDocumentationService.StoreSystemConfigurationRequest/HertbeatIntervall`

Exact selected historical XSD authority:

- file: `IBIS-IP_SystemDocumentationService_v1.0.xsd`
- repository branch blob: `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`
- official upstream `VDVde/VDV301` tag `VDV-301-1.0` blob: `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`
- branch and official tag are byte-identical for this file

The exact XSD declares:

- `SystemDocumentationService.SystemConfigurationData/HeartbeatIntervall` → `IBIS-IP.double`, `minOccurs="0"`
- `SystemDocumentationService.StoreSystemConfigurationRequestStructure/HeartbeatIntervall` → `IBIS-IP.duration`, `minOccurs="0"`

No XSD element named `HertbeatIntervall` exists in the exact selected file.

## Corrected finding interpretation

`DR3012-003` remains valid and is strengthened/refined rather than withdrawn:

- for `SystemConfigurationData`, the PDF/XSD discrepancy covers both the exact identifier and the type:
  - PDF: `HertbeatIntervall`, `IBIS-IP.duration`
  - XSD: `HeartbeatIntervall`, `IBIS-IP.double`
- for `StoreSystemConfigurationRequest`, the documented/executable type is aligned as `IBIS-IP.duration`, but the identifier still differs:
  - PDF: `HertbeatIntervall`
  - XSD: `HeartbeatIntervall`

The executable authority remains the exact selected historical XSD. No typo alias is invented.

## Executable disproof/confirmation

EV-129 additionally confirms the boundary with positive/negative XML validation against the exact Common V1.0 wrapper semantics:

- declared `HeartbeatIntervall` with numeric `Value` is accepted as `IBIS-IP.double`
- a duration lexical value such as `PT5S` is rejected when tested as the declared `IBIS-IP.double`
- the misspelled root `HertbeatIntervall` is rejected as the declared element
- an `IBIS-IP.duration` control sample with `PT5S` is accepted

Therefore the corrected state for `DR3012-003` is suitable for `executable_confirmed`.

## Audit invariants

- frozen finding inventory: unchanged
- XSD files: unchanged
- no alias or schema override created
- no `latest wins` substitution used
- future comparisons must preserve exact element identifiers before considering semantic similarity or typo normalization
