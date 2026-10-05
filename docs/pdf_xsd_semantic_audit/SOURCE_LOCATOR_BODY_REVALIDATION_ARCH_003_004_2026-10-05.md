# Visible-body source-locator revalidation — ARCH-003 / ARCH-004

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete architecture findings; no new finding progress credit.

## Source and visual method

Official source:

- `VDV-Schrift 301-1`
- `IBIS-IP Teil 1: Systemarchitektur`
- source ID: `VDV301-1_V1.0_DE`
- pinned SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`

Current interactive PDF rendering succeeded for printed page 7 and returned cache-miss for printed pages 16 and 26. Per the repository fallback rule `PDF_VISUAL_RENDER_FALLBACK.md`, those pages are covered by the existing exact-byte render:

- run `33725750019`
- job `100554215021`
- artifact `9881897572` (`arch-v10-pinned-read`)
- artifact digest `sha256:b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510`
- all 36 page PNG hashes verified against the artifact manifest
- targeted visual pages include printed pages 16 and 26

The visible-body anchor is taken from the actual page content, not from the table of contents or inherited section context.

## ARCH-003 — one IBIS-IP system per vehicle does not prohibit coupling

### Visible body

Printed page **16** does not show a chapter heading for the relevant paragraph. It visibly continues the explanation of the system architecture figure and then states that an additional coupled vehicle appears in the figure.

The relevant visible body says, in substance:

- every vehicle represents a self-contained IBIS-IP system;
- a coupled vehicle is another IBIS-IP system;
- corresponding interfaces must be provided for its connection.

The same page then visibly begins **5. Funktionsgruppen**.

### Locator correction

The previous locator:

`4 Systemarchitektur / vehicle-system architecture figure and accompanying coupling description`

used inherited architecture context rather than the actual visible body anchor on printed page 16.

Canonical locator:

- printed page: **16**
- section/body anchor: **Fortsetzung der Beschreibung zu Abbildung 6 — Absatz zum gekuppelten Fahrzeug / unmittelbar vor 5. Funktionsgruppen**
- no table/figure identifier is claimed as visible on this page

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- each vehicle remains its own IBIS-IP system boundary
- the architecture explicitly supports connection of another coupled-vehicle IBIS-IP system through interfaces
- no blanket cross-vehicle communication prohibition may be inferred
- concrete coupling/service behavior remains the responsibility of the applicable interface/service specifications
- no runtime diagnostic is created
- DE/EN diagnostics remain technically correct

## ARCH-004 — general protection requirement is not a concrete cryptographic profile

### Visible body

Printed page **7** visibly contains:

- **2. Anwendungsbereich**

The body limits the architecture/applications presented in the document to non-safety-related systems and allows safety-relevant systems to be connected through defined interfaces, for example gateways, provided non-interference is maintained.

Printed page **26** visibly contains:

- **6. Systemsicherheit**

The body requires contemporary adequate security mechanisms against unauthorized intrusion and requires interfaces to safety-relevant components to be designed so that interference with those components is excluded.

The same printed page later begins **7. Kommunikation mit Diensten**. The security claim therefore belongs to section 6, not section 7.

### Locator correction

The previous page-26 locator:

`6 Kommunikation / security and protection context`

is incorrect.

Canonical page-26 locator:

- printed page: **26**
- section: **6. Systemsicherheit**

Printed page 7 remains:

- **2. Anwendungsbereich**

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- the document provides a general security/protection requirement
- this architecture edition does not establish a concrete TLS version, certificate model or cipher-suite validation profile
- concrete cryptographic hard-fails must come from an applicable explicit standard/profile authority, not be synthesized from ARCH-004 alone
- no runtime diagnostic is created
- DE/EN diagnostics remain technically correct

## Body-verification accounting

After this block:

- ARCH-003: `verified_current_standard`
- ARCH-004: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 13
- pending visible-body revalidation becomes 27
- next canonical body-revalidation finding: `ARCH-005`


## Gate

- GitHub Actions run: **37274313692**
- result: **SUCCESS**
- validated commit: `89dc9ace147ca32f40c8caeab2b4eac2296a612b`
- structural locators: **40**
- visible-body verified: **13**
- visible-body pending: **27**
- next body-revalidation finding: **ARCH-005**
- upstream exact release-tag XSD checks: **19**

The gate verified CURRENT_STATE/body-registry synchronization and the ARCH-003/ARCH-004 visible-body locator assertions in addition to the existing audit regression suite.
