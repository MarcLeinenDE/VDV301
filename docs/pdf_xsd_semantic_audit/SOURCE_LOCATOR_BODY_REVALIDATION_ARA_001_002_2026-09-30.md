# Visible-body source-locator revalidation — ARA-001 / ARA-002

Date: 2026-09-30  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete findings; no new finding progress credit.

## Sources and authority

Official PDF:

- VDV-Schrift 301-2-19 AnalogRadioService
- publication: 01/2023
- document version: V2.4
- pinned SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`

Current upstream authority recheck:

- official repository workflow states that official releases are marked with corresponding release tags;
- ref `VDV-301-2.4` does not resolve in the official `VDVde/VDV301` repository;
- `IBIS-IP_AnalogRadioService_V2.4.xsd` is not present on official upstream `master`;
- local candidate/integration service XSD remains blob `48fb303b80936d2d762f0889ce0c359e04c16e5b`;
- candidate XSD includes `IBIS-IP_common_V2.3.xsd`;
- candidate/integration material remains selectable only when explicitly selected and is not official-release authority.

## ARA-001 — official V2.4 document / release-XSD authority gap

### Visible PDF identity

The official PDF visibly identifies itself as:

- `VDV-Schrift 301-2-19`
- `Dienst – AnalogRadioService / Service – AnalogRadioService`
- `V 2.4`

This is a document-identity locator rather than a layout-sensitive semantic table claim.

Canonical PDF locator:

- printed page: **1**
- section/locator: **Cover — VDV-Schrift 301-2-19 / Dienst – AnalogRadioService / V 2.4**

### Revalidation result

No finding change.

- classification: `release_authority_gap`
- official PDF authority: confirmed
- official V2.4 service-XSD release authority: unresolved / absent at current upstream authority point
- candidate/integration XSD: remains provenance-distinct
- SDK behavior: `unsupported_profile` for an official strict V2.4 profile; explicit candidate/integration selection remains separate
- no XSD bytes changed
- DE/EN diagnostics remain technically correct

## ARA-002 — TransmitterType vs Transmitter PDF-internal contradiction

### Visible body verification

Printed page **11** visibly shows:

- heading: **2.2 DataStructure of SendTelegram Operation**
- subheading: **2.2.1 Request**
- table/model label: **AnalogRadioService.RadioTelegramStructure**
- final table row: **TransmitterType**, cardinality **1:1**, type **TransmitterStructure**
- embedded schema view on the same page: element **Transmitter**, type **TransmitterStructure**, `minOccurs=0`

Printed page **12** visibly shows the continuation diagram for the request model. The diagram itself is labelled **AnalogRadioService.RadioTelegramStructure** and contains **Transmitter**. Below it, the next visible body heading begins with **2.3 DataStructure TransmitterStructure**.

Printed page **13** visibly shows:

- heading: **2.5 Examples**
- subheading: **2.5.2 XML of a complete telegram**
- XML member: **<Transmitter>**

The official PDF therefore proves the identifier contradiction internally before candidate-XSD comparison.

### Candidate corroboration

Candidate/integration XSD blob `48fb303b80936d2d762f0889ce0c359e04c16e5b` defines:

- complex type `AnalogRadioService.RadioTelegramStructure`
- element `Transmitter`
- type `TransmitterStructure`
- `minOccurs="0"`

This corroborates the document-internal majority representation but does not create official V2.4 release authority.

### Revalidation result

No finding change.

- classification: confirmed PDF/documentation defect
- canonical intended identifier for explanatory guidance: `Transmitter`
- runtime behavior: informational only; no runtime matcher required
- separate ARA-003 cardinality finding remains independent
- official strict V2.4 XSD authority gap remains ARA-001
- no alias/normalization is introduced
- DE/EN diagnostics remain technically correct

## Locator corrections

ARA-001:

- replace generic `Cover / document identity` with the actual visible cover identity string.

ARA-002:

- page 11 section becomes `2.2 DataStructure of SendTelegram Operation / 2.2.1 Request`;
- page 11 table becomes the visible `AnalogRadioService.RadioTelegramStructure` request-structure table/model;
- page 12 locator explicitly records the continuation diagram labelled `AnalogRadioService.RadioTelegramStructure`;
- page 13 section becomes `2.5 Examples / 2.5.2 XML of a complete telegram`.

## Body-verification accounting

After this block:

- ARA-001: `verified_current_standard`
- ARA-002: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 7
- pending visible-body revalidation becomes 33
- next canonical body-revalidation finding: `ARA-003`


## Gate

- GitHub Actions run: **36720086602**
- result: **SUCCESS**
- validated commit: `10725bbad4aa4ccb7566411e0203f83297cac6de`
- structural locators: **40**
- visible-body verified: **7**
- visible-body pending: **33**
- next body-revalidation finding: **ARA-003**
- upstream exact release-tag XSD checks: **19**

The gate also verified that `CURRENT_STATE.json` matches the body-verification registry and that the ARA-001/ARA-002 canonical locator strings match the revalidated body positions.
