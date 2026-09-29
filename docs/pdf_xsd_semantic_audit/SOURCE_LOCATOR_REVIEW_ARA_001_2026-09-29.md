# Source-locator review — ARA-001 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
ARA-001 is an authority/provenance gap for AnalogRadioService V2.4.

An official VDV publication exists:
- VDV-Schrift 301-2-19 AnalogRadioService V2.4, 01/2023
- pinned official PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`
- 16 pinned pages; document identity anchored at printed page 1.

The frozen authority review found no official `VDV-301-2.4` release tag and no official upstream `IBIS-IP_AnalogRadioService_V2.4.xsd`.

## Candidate/integration boundary
A service schema does exist in the integration corpus:

- `IBIS-IP_AnalogRadioService_V2.4.xsd`
- blob `48fb303b80936d2d762f0889ce0c359e04c16e5b`
- candidate/integration provenance only
- integration origin recorded as commit `c9c086ac07f7e9bdb271c54f7a274e3cf0d03749`.

Its existence must not be used to manufacture official V2.4 release-schema authority.

## SDK consequence
Official and candidate/integration schema provenance remain distinct, but both are valid selectable validation authorities.

When a candidate/integration XSD is selected, the SDK validates against that exact XSD and derives PASS/FAIL from it in the same way as for a selected official XSD. The result must explicitly state that the selected authority is candidate/integration and must reference the exact XSD source/provenance (including the pinned blob/source route).

A candidate result must not be relabelled as official release authority; this provenance label does not reduce the candidate XSD's role as the selected executable validation authority.

This is an authority warning/context finding, not an instruction to modify an XSD.

## Completeness note
The absence of an official service XSD cannot have an XSD line locator. Completeness here means that the positive official-document authority and the provenance-limited candidate schema are both exactly pinned, while the missing official authority is supported by the frozen repository/tag provenance review.

## State
Canonical source-locator manifest after validation: **23 complete / 0 partial / 169 remaining**.
