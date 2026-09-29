# Source-locator review — ARCH-001 — 2026-09-29

Status: **complete; gate pending**.

## Finding
ARCH-001 is an architecture/context finding, not an XML/XSD defect.

Pinned official PDF: VDV-Schrift 301-1 V1.0 (01/2014), SHA-256 `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`.

Exact evidence:
- printed page 7, §2 `Anwendungsbereich`: the former IBIS Wagenbus Master/Slave architecture is explicitly replaced by a modern service-oriented architecture;
- printed page 10, §3.2 `Begriffe`, `Dienstorientierte Architektur / Dienst bzw. Service / Operationen`: a service exposes related functionality through a specified interface; services may run on devices, but architecture derivation is explicitly independent of the devices used.

## Classification
Existing semantic classification remains correct: `non_defect`, `contextual_only`, runtime `not_applicable`. No executable XML rule and no XSD correction follows.

## Evidence provenance
Official source ID `VDV301-1_V1.0_DE`; pin/render run `33725750019`, job `100554215021`, artifact `9881897572`. Supporting terminal revalidation: `FINDING_REVALIDATION_ARCH_V10_2026-09-03.md`.

## State
Canonical source-locator manifest after persistence: **27 complete / 0 partial / 165 remaining**.
