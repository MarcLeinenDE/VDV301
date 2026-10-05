# Visible-body source-locator revalidation — ARCH-005 / ARCH-006

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete architecture findings; no new finding progress credit.

## Source and visual method

Official source:

- `VDV-Schrift 301-1`
- `IBIS-IP Teil 1: Systemarchitektur`
- source ID: `VDV301-1_V1.0_DE`
- pinned SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`

Current visual verification:

- printed page 6 rendered successfully from the official PDF;
- printed pages 26 and 27 returned interactive-render cache misses;
- per `PDF_VISUAL_RENDER_FALLBACK.md`, those pages are covered by exact-byte render run `33725750019`, job `100554215021`, artifact `9881897572`, whose page hashes were verified and whose targeted visual pages include 26 and 27.

Canonical locators follow the actual visible page headings/body, not TOC wording, inherited context or inferred numbering.

## ARCH-005 — communication classes are not a universal transport hard rule

### Visible body

Printed page **26** visibly contains:

- **7. Kommunikation mit Diensten**

The body divides transferred information into two broad groups:

- rapidly changing information, where quick simultaneous distribution to consumers is more important than guaranteed delivery;
- less frequently changing information, where reliable notification of all consumers is required.

The same section states that:

- UDP is suitable for rapidly changing information;
- broadcast is to be avoided for IPv6 compatibility;
- UDP multicast is to be used instead;
- TCP is suitable for longer-lived/reliable information;
- HTTP over TCP is specified for reliable IBIS-IP communication.

### Locator correction

The previous locator:

`6 Kommunikation`

is wrong.

Canonical locator:

- printed page: **26**
- section: **7. Kommunikation mit Diensten**

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- the architecture establishes communication classes and design context
- this does not create a universal per-packet or per-service transport hard rule by itself
- concrete transport conformance remains profile/service-specific and must follow the applicable Part-2/external-protocol authority chain
- no runtime diagnostic is created from ARCH-005 alone
- DE/EN diagnostics remain technically correct

## ARCH-006 — Part 1 establishes XML generally; Part 2 supplies the technical XML structures

### Visible body — printed page 6

Printed page **6** visibly contains:

- **1. Einleitung**

Near the end of the page, the document states that Part 1 defines the IBIS-IP system architecture and that Part 2, VDV-Schrift 301-2, specifies the technical interface implementation based on XML structures.

### Visible body — printed page 27

Printed page **27** visibly contains:

- **7.1. Strukturierung der Informationsinhalte**

The body states that XML is to be used for transferring information between two services in IBIS-IP.

### Locator corrections

The previous page-6 locator:

`1 Vorbemerkung / document-part boundary`

is incorrect.

Canonical page-6 locator:

- printed page: **6**
- section: **1. Einleitung**

The previous page-27 locator:

`6 Kommunikation / XML information exchange`

is incorrect.

Canonical page-27 locator:

- printed page: **27**
- section: **7.1. Strukturierung der Informationsinhalte**

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- Part 1 establishes XML as architecture-level information exchange
- Part 2/XSD remains the authority for exact service elements, types, structures and cardinalities
- generic XML/protocol standards may form separate validation layers only through an applicable authority chain
- Part 1 never overrides or repairs the selected Part-2 XSD
- no runtime diagnostic is created from ARCH-006 itself
- DE/EN diagnostics remain technically correct

## Body-verification accounting

After this block:

- ARCH-005: `verified_current_standard`
- ARCH-006: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 15
- pending visible-body revalidation becomes 25
- next canonical body-revalidation finding: `ARCH-007`
