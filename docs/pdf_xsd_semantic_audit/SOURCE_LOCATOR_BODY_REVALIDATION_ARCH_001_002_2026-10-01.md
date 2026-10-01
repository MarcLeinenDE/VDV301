# Visible-body source-locator revalidation — ARCH-001 / ARCH-002

Date: 2026-10-01  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete architecture findings; no new finding progress credit.

## Source

Official German architecture publication:

- `VDV-Schrift 301-1`
- `IBIS-IP Teil 1: Systemarchitektur`
- publication 01/2014
- source ID: `VDV301-1_V1.0_DE`
- pinned SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`
- prior exact-byte render: run `33725750019`, job `100554215021`, artifact `9881897572`
- artifact digest: `sha256:b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510`

This is an architecture/documentation authority lane. No XSD validation lane applies to ARCH-001/002 themselves.

## ARCH-001 — service-oriented architecture is not a fixed physical Master/Slave role model

### Visible body

Printed page **7** visibly contains heading:

- **2. Anwendungsbereich**

The body explicitly states that the proven Master/Slave architecture of the former IBIS wagon bus was replaced by a modern service-oriented architecture.

Printed page **10** visibly contains:

- **3.2. Begriffe**
- **Dienstorientierte Architektur**
- **Dienst bzw. Service**
- **Operationen**

The body defines a service as software encapsulating related functionality and exposing it through a specified interface. It also says that services run on a device/application context, but that architecture derivation is performed independently of the devices used.

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- logical service and operation identity must not be replaced by a fixed physical Master/Slave device assumption
- concrete XML/service rules remain Part-2/XSD authority
- no runtime diagnostic is created
- DE/EN diagnostics remain technically correct

Canonical PDF locators remain:

1. printed page **7** — **2. Anwendungsbereich**
2. printed page **10** — **3.2. Begriffe — Dienstorientierte Architektur / Dienst bzw. Service / Operationen**

## ARCH-002 — provider/consumer hierarchy is a general architecture model

### Visible body

Printed page **12** visibly contains:

- **4. IBIS-IP-Systemarchitektur**
- **4.1. Ermittlung der Fachkomponenten**
- later on the same page: **4.2. Hierarchisierung anhand eines Beispiels**

Within 4.1 the text states that analysis of data flows and calls leads to a hierarchy of functional components forming the basis of a hierarchical service-oriented software architecture, while details of specified services are in Part 2.

Printed page **14** does **not** visibly repeat the 4.2 heading. Its visible body anchor is:

- **Abbildung 5: Hierarchisierung durch Ordnung der Fachkomponenten nach Aufrufrichtungen.**

Immediately below, the body states the general rules used for this and following figures:

- lower functional components provide data to higher ones;
- higher components are active information users in the client role;
- lower components are passive information providers in the server role;
- lower components generally do not know the querying service;
- higher components/devices know the services from which they retrieve data.

The page then begins **4.3. Die IBIS-IP-Systemarchitektur**.

### Result

No semantic change.

- classification remains `intentional_design_misread` / non-defect
- the client/provider wording is a general architecture hierarchy model
- it must not override service-specific request/subscription/callback semantics
- no runtime diagnostic is created
- DE/EN diagnostics remain technically correct

### Locator correction

The previous page-14 locator used inherited section context `4.2. Hierarchisierung anhand eines Beispiels`. That context is semantically correct but the heading is not visibly present on printed page 14.

The canonical page-14 locator is therefore corrected to the actual visible body anchor:

- printed page **14**
- **Abbildung 5: Hierarchisierung durch Ordnung der Fachkomponenten nach Aufrufrichtungen / unmittelbar folgende Client-/Server-Regeln**

Printed page 12 remains:

- **4.1. Ermittlung der Fachkomponenten**

## Body-verification accounting

After this block:

- ARCH-001: `verified_current_standard`
- ARCH-002: `verified_current_standard`
- structural locator count remains 40
- visible-body verified count becomes 11
- pending visible-body revalidation becomes 29
- next canonical body-revalidation finding: `ARCH-003`


## Gate

- GitHub Actions run: **36826837789**
- result: **SUCCESS**
- validated commit: `5e2046354d88c3a0a200e0119e0928af8d2947fd`
- structural locators: **40**
- visible-body verified: **11**
- visible-body pending: **29**
- next body-revalidation finding: **ARCH-003**
- upstream exact release-tag XSD checks: **19**

The gate verified CURRENT_STATE/body-registry synchronization and the ARCH-001/ARCH-002 visible-body locator assertions in addition to the existing audit regression suite.
