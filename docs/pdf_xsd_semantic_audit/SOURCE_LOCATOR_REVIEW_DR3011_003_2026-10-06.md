# Source-locator review — DR3011-003 — 2026-10-06

Status: **complete / visible-body verified / editorial documentation defect confirmed**.

## Finding

VDV 301-1 V1.0 contains two immediately consecutive entries for `IBIS-IP` in the abbreviation list, with slightly different expanded wording.

## Visible evidence

Official source:
- source ID: `VDV301-1_V1.0_DE`
- SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`
- printed page: **34**
- visible section: **9. Abkürzungen**
- visible table columns: **Abkürzung / Beschreibung**

The two consecutive visible rows are:

1. `IBIS-IP` — `Integriertes-Bord Informations-System auf Basis Internet Protokoll`
2. `IBIS-IP` — `Integriertes-Bord-Informations-System auf Internet-Protokoll Basis`

The difference is visible in the punctuation/wording of the expansion; both rows use the same abbreviation.

## Exact-byte visual verification

The current review reused the exact byte-pinned render from:
- run `33725750019`
- artifact `9881897572`
- page-34 PNG SHA-256 `c61689499c594d47cd99cc7b61de57b4f0183b20ca9c33ee508ab411bc7a709b`

The page hash was freshly recomputed from the artifact and matches the frozen visual-evidence registry exactly.

## Disproof attempt

No table legend, footnote, language split or distinct abbreviation namespace explains the duplicate rows. They are adjacent entries in the same abbreviation table and use the identical abbreviation `IBIS-IP`.

## Classification and SDK behavior

Confirmed editorial PDF/documentation residue.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable**
- runtime matcher: **not applicable**
- SDK behavior: **no runtime diagnostic**
- implementation aliases or semantic rules: **none**

The finding is retained only so the documentation defect remains traceable.
