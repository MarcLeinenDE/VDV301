# Source-locator review — DR3011-001 — 2026-10-06

Status: **complete / visible-body verified / documentation cross-reference defect confirmed**.

## Finding

VDV 301-1 V1.0 contains an internal section-reference mismatch for SystemManagement.

## Visible evidence

Official source:
- source ID: `VDV301-1_V1.0_DE`
- SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`

Printed page **2** visibly assigns:
- `5.1.2 System-Dokumentation`
- `5.1.3 System-Management`

Printed page **10** contains the SystemManagementService example and points that System-Management example to section `5.1.2`.

The two visible statements conflict.

## Evidence route

The live PDF screenshot endpoint cache-missed during this review. The existing deterministic visual evidence from run `33725750019`, artifact `9881897572`, was therefore used under the current fallback rule. The official PDF text layer independently confirms the same section numbering.

## Classification

Confirmed PDF/documentation cross-reference defect only.

- no XSD authority applies;
- no XML validity effect;
- no SDK runtime matcher;
- do not derive any conformance rule from the wrong section number.
