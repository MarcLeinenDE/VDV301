# Source-locator review — DR3012-002 — 2026-10-06

Status: **complete / visible-body verified / external primary authority verified / documentation semantics defect confirmed**.

## Finding

VDV 301-2 V1.0 describes DNS-SRV `Weight` selection incorrectly.

## Visible VDV evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **26**
- visible table: **Tabelle 2 Bedeutungen der SRV-Records in DNS-SD**
- relevant row: **Weight**

The visible Weight description reads:

`Gewicht für den Inhalt (hier also der Dienst), bei gleichem Gewicht wird der Dienst mit dem geringeren Gewicht bevorzugt`

This wording is internally inconsistent when read literally: two records cannot simultaneously have the same Weight and one have the lower Weight. In the surrounding SRV context, the intended comparison is evidently between records at the same Priority; under that interpretation, the sentence says the lower Weight is preferred.

## Exact-byte visual verification

EV-129:
- closure run: `33765633886`
- pinned evidence run: `33765167655`
- artifact: `9897171006`
- artifact digest: `sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7`
- page-26 PNG SHA-256: `704181401df2300d23caac7683713b363d0ae06e688fe77908c431294b4b5ca5`

The page hash was freshly recomputed from the exact EV-129 artifact during this review and matches its manifest.

## External primary-authority cross-check

RFC Editor RFC 2782, **A DNS RR for specifying the location of services (DNS SRV)**:

- Priority: lower-numbered Priority is preferred.
- Weight applies to entries with the **same Priority**.
- Larger Weight values should receive **proportionately higher probability** of being selected.

Primary source:
- https://www.rfc-editor.org/rfc/rfc2782.html

RFC 2782 has historical errata discussions concerning details of the selection algorithm, but those do not reverse the specification's explicit larger-Weight/proportionately-higher-probability rule.

## Disproof attempt

Possible explanations were checked:

- The visible text itself says `bei gleichem Gewicht ... geringeren Gewicht`, so a literal reading is self-contradictory rather than a valid alternative rule.
- Interpreting the first `Gewicht` as an editorial substitution for `Priorität` produces a meaningful sentence, but then its "lower Weight preferred" rule contradicts RFC 2782.
- RFC 2782's Priority rule cannot rescue the Weight wording: low numeric values are preferred for **Priority**, not **Weight**.
- Existing RFC 2782 errata do not establish a reversed lower-Weight preference.

The finding therefore remains confirmed.

## Classification and SDK behavior

Confirmed PDF/documentation semantics defect against an external protocol authority.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable**
- runtime matcher: **not applicable**
- SDK behavior: **warning / informational protocol guidance**
- no XML alias, normalization or schema rule is introduced.

Provider-facing guidance must preserve the distinction: lower numeric **Priority** is preferred; for equal Priority, larger **Weight** receives proportionately higher selection probability under RFC 2782.
