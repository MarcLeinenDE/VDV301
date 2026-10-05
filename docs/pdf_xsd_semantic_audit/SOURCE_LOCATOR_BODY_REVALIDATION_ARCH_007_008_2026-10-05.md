# Visible-body source-locator revalidation — ARCH-007 / ARCH-008

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete architecture findings; no new finding progress credit.

## Source and visual method

Official source:

- `VDV-Schrift 301-1`
- `IBIS-IP Teil 1: Systemarchitektur`
- source ID: `VDV301-1_V1.0_DE`
- pinned SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`

The interactive PDF renderer returned cache misses for the required pages. Per the canonical workflow, the review immediately switched to the exact-byte fallback artifact:

- run `33725750019`
- job `100554215021`
- artifact `9881897572` (`arch-v10-pinned-read`)
- artifact digest `sha256:b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510`
- same pinned PDF SHA-256 as above
- all rendered page hashes previously verified against the artifact manifest

Printed pages 10 and 26 were inspected directly from that fallback render.

## ARCH-007 — historical SNTP/RTP wording is edition-specific

### Visible body

Printed page **26** visibly contains:

- **7. Kommunikation mit Diensten**

After the UDP-multicast and TCP/HTTP discussion, the body states that other IP-based communication protocols are conceivable, explicitly naming:

- **SNTP** for time synchronization;
- **RTP** for streaming audio/video data.

The paragraph then states that these are **in this edition not yet specified**.

### Locator correction

The previous locator:

`6 Kommunikation`

is wrong.

Canonical locator:

- printed page: **26**
- section: **7. Kommunikation mit Diensten**
- body anchor: final paragraph naming SNTP/RTP and limiting the statement to this edition

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- the statement is explicitly historical and edition-bound
- it must not be promoted to a permanent prohibition against later VDV profiles using SNTP/RTP
- later TimeService/video profiles must be assessed under their own VDV and external-protocol authority chain
- no runtime diagnostic is created from ARCH-007
- DE/EN diagnostics remain technically correct

## ARCH-008 — functional components are broader than executable service identity

### Visible body

Printed page **10** does **not** visibly repeat the heading `3.2. Begriffe`.

The page starts with the continuation of the definition of **Fachkomponente**. The relevant visible paragraph states that in this publication only **part** of the functional components are specified and implemented in the form of services or applications on devices. Therefore the broader term `Fachkomponente` continues to be used for describing functionality.

Immediately after this paragraph the page visibly continues with:

- **Funktionsgruppe**
- **Dienstorientierte Architektur**
- **Dienst bzw. Service**
- **Operationen**

This visually confirms that functional-component vocabulary and concrete service vocabulary are deliberately distinct.

### Locator correction

The previous locator:

`3.2 Begriffe / functional components and services`

used inherited section context rather than the actual visible page-10 anchor.

Canonical locator:

- printed page: **10**
- section/body anchor: **Fortsetzung der Definition Fachkomponente — Absatz „nur ein Teil der Fachkomponenten … in Form von Diensten bzw. Applikationen …“ / unmittelbar vor Funktionsgruppe**
- no table identifier

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- a functional-component label does not by itself establish a valid service identifier, endpoint, discovery obligation, XML root or mandatory operation
- executable service identity must come from the applicable Part-2 service publication, XSD, discovery/profile authority or another explicit service definition
- no runtime diagnostic is created from ARCH-008
- DE/EN diagnostics remain technically correct

## Body-verification accounting

After this block:

- ARCH-007: `verified_current_standard`
- ARCH-008: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 17
- pending visible-body revalidation becomes 23
- next canonical body-revalidation finding: `BG-001`


## Gate

- GitHub Actions run: **37286137293**
- result: **SUCCESS**
- validated commit: `f2ce3a4a8f794caed300ee1574bc5f48a493d104`
- structural locators: **40**
- visible-body verified: **17**
- visible-body pending: **23**
- next body-revalidation finding: **BG-001**
- upstream exact release-tag XSD checks: **19**

The gate verified CURRENT_STATE/body-registry synchronization and the ARCH-007/ARCH-008 visible-body locator assertions in addition to the existing audit regression suite.
