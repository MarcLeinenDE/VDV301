# Visible-body source-locator revalidation — ARA-003 / ARA-004

Date: 2026-09-30  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete findings; no new finding progress credit.

## ARA-003 — Transmitter cardinality contradiction

### Visible PDF body

Printed page **11** visibly shows:

- heading: **2.2 DataStructure of SendTelegram Operation**
- subheading: **2.2.1 Request**
- request structure: **AnalogRadioService.RadioTelegramStructure**
- final table row: **TransmitterType**, cardinality **1:1**, type **TransmitterStructure**
- embedded schema view on the same page: element **Transmitter**, type **TransmitterStructure**, `minOccurs=0`

This establishes a PDF-internal cardinality contradiction independent of any external XSD.

### Candidate/integration corroboration and executable evidence

Selected candidate/integration XSD:

- file: `IBIS-IP_AnalogRadioService_V2.4.xsd`
- blob: `48fb303b80936d2d762f0889ce0c359e04c16e5b`
- component: `AnalogRadioService.RadioTelegramStructure/Transmitter`
- declaration: `minOccurs="0"`, default `maxOccurs="1"`

EV-105:

- run: `33228250613`
- job: `99036090357`
- candidate schema compiles;
- Transmitter declaration is 0:1;
- SendTelegram without Transmitter is valid;
- SendTelegram with Transmitter is valid;
- result explicitly applies only to the selected candidate/integration profile.

### Result

No semantic change.

- classification: confirmed PDF documentation defect / cardinality mismatch
- official PDF contradiction: confirmed visually
- candidate/integration executable behavior: 0:1
- official V2.4 release-XSD authority: not inferred
- SDK behavior remains informational
- no alias, normalization or waiver
- DE/EN diagnostics remain technically correct

Canonical PDF locator:

- printed page: **11**
- section: **2.2 DataStructure of SendTelegram Operation / 2.2.1 Request**
- table/model: **AnalogRadioService.RadioTelegramStructure request-structure table/model**

## ARA-004 — wrong operation name in URI example

### Visible PDF body

Printed page **10** visibly shows:

- heading: **2.1 Operations of the AnalogRadioService**
- text: the service has only one operation
- operation table: **SendTelegram**
- request/response table: **SendTelegram** request using `RadioTelegramStructure`

Printed page **13** visibly shows:

- heading: **2.5 Examples**
- subheading: **2.5.1 URI for the Operation SendTelegram**
- generic URI form: `http://Host:Port/ServiceName/Operation`
- concrete example: `192.168.1.2:8080/AnalogRadioService/SendFFSKTelegram`
- subheading: **2.5.2 XML of a complete telegram**
- XML root: `<AnalogRadioService.SendTelegram>`

Thus only the concrete URI example uses `SendFFSKTelegram`; the surrounding operation definition, heading and XML root all use `SendTelegram`.

### Candidate corroboration

The candidate/integration XSD blob `48fb303b80936d2d762f0889ce0c359e04c16e5b` defines `AnalogRadioService.SendTelegram` and does not define `SendFFSKTelegram`.

This is corroboration only. The finding remains fully established within the official PDF and stays documentation-only in semantic authority.

### Result

No semantic change.

- classification: confirmed PDF documentation error / wrong operation reference
- documented operation: `SendTelegram`
- isolated incorrect URI segment: `SendFFSKTelegram`
- SDK behavior remains warning/guidance
- `SendFFSKTelegram` must not be accepted, rewritten or registered as an alias merely because it appears in the example
- DE/EN diagnostics remain technically correct

Canonical PDF locators:

1. printed page **10**
   - section: **2.1 Operations of the AnalogRadioService**
   - table/model: **Operation inventory and Request / Response table**
2. printed page **13**
   - section: **2.5 Examples / 2.5.1 URI for the Operation SendTelegram**
3. printed page **13**
   - section: **2.5 Examples / 2.5.2 XML of a complete telegram**

## Body-verification accounting

After this block:

- ARA-003: `verified_current_standard`
- ARA-004: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 9
- pending visible-body revalidation becomes 31
- next canonical body-revalidation finding: `ARCH-001`


## Gate

- GitHub Actions run: **36721547904**
- result: **SUCCESS**
- validated commit: `7bd46ff43b8a31d33634d2d6b8fc5d11b7176bba`
- structural locators: **40**
- visible-body verified: **9**
- visible-body pending: **31**
- next body-revalidation finding: **ARCH-001**
- upstream exact release-tag XSD checks: **19**

The gate verified CURRENT_STATE/body-registry synchronization and the ARA-003/ARA-004 visible-body locator assertions in addition to the existing audit regression suite.
