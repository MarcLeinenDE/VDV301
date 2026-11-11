# SOURCE LOCATOR REVIEW — DRCOM10-007 — 2026-11-11

**Evidence status:** Six distinct official original Common V1.0–V2.4 PDF source/page hashes, actual visible table/body headings, editorial wording, exact selected corroborating XSD blobs and boundary all checked; **the canonical final gate/terminal state is only `00_START_HERE/CURRENT_STATE.json`**. One pre-existing unique documentation-only finding; no duplicate finding ID.

## Identity and cross-version falsification

The V1.0-only semantic scope originally assigned to `DRCOM10-007` was too narrow: all six audited official Common PDFs have the **same core editorial inconsistency** in the GNSS coordinate-system enumeration page, alongside `dorr operation` and `Infromation` prose misspellings. This is not a new XML element, value, XSD type alias, parser defect or independent PASS/FAIL rule.

The visibly printed **section heading** spells `GNSSCoordinateSystemEnumeration`, whereas the visible **Enumeration Name table cell** and **caption** both print plural `GNSSCoordinateSystemsEnumeration`. The exact selected Enumerations XSD simpleType is singular across the V1.0/V2.0/V2.1/V2.2 historical schemas, V2.3 reusing the exact V2.2 dependency, and the separately selected V2.4 **candidate/integration** XSD. This corroborates the editorial table-naming inconsistency only, not an independent XSD-conformance mismatch affecting XML instance values. The actual enum value lists were not reclassified as differences here.

## Pinned official original PDF body table evidence

Every quoted original page image was actually opened and visually reviewed (not from a TOC or OCR). Historical GitHub Actions archive PNG hashes were recomputed against their manifest (V2.2 freshly SHA-pinned/rendered in run `43111602309`, artifact `13896921851`). Official PDF SHA-256 and exact byte size matched the canonical source pin. The first page shows **both** wrong `dorr` description and singular/plural GNSS table; the following page shows `Infromation` in the GNSSQuality table.

| Official Common original | Visible main body heading/table | Next page | PDF SHA-256 | Size | Exact main PNG SHA-256 | Next PNG SHA-256 | GitHub run/artifact |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| V1.0 | p26 §2.8 **T69**; §2.11 **T72** | p27 §2.12 **T73** | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | 892769 | `932f4a3acc4fc58fbd58cb649fd766b3b87700e58a2b53d2665c0512c7fed99e` | `68c6dc2ccead654a25a805c9a4d3163bb7ab2a13c2a6d24b996ab59160d9d83f` | [33275626001](https://github.com/MarcLeinenDE/VDV301/actions/runs/33275626001) / `9721397514` |
| V2.0 | p34 §3.10 **T74**; §3.13 **T77** | p35 §3.14 **T78** | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | `ba97aaea09a3ca7b60b1ae2493392f0336cf93269fd757ed256adfc3dbd1cee8` | `7821bb75c2ce343c9362c29a1b0f7658ca352a6ee913f37eda406a67421b0004` | [33279811315](https://github.com/MarcLeinenDE/VDV301/actions/runs/33279811315) / `9722644456` |
| V2.1 | p36 §3.10 **T74**; §3.13 **T77** | p37 §3.14 **T78** | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | `8649ce7fdf571a12929d43db76e433acdc1d4b127c77c393b253ff72aa4ccef8` | `ff49b35913404b6642aaf3181d0092cc552dfeddcc2f8ab14bf676bc3811f1de` | [33393002497](https://github.com/MarcLeinenDE/VDV301/actions/runs/33393002497) / `9758203545` |
| V2.2 | p38 §3.10 **T75**; §3.13 **T78** | p39 §3.14 **T79** | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | `8aed2050426ae63489634164129054ba7a04a001654b9fb0d5c6aff422f56921` | `3c6269519e87295efb5d2cb9ca8d3cef45aa932822750970f05cd39766d90658` | [43111602309](https://github.com/MarcLeinenDE/VDV301/actions/runs/43111602309) / `13896921851` |
| V2.3 | p39 §3.10 **T75**; §3.13 **T78** | p40 §3.14 **T79** | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | `072e30327edc317fb78b5709258a41b78585438f7f973dc24e202761a522a6e0` | `fbb2a0356b179911943597058401264cdf86cc43918796a3844263afa459884a` | [33656579631](https://github.com/MarcLeinenDE/VDV301/actions/runs/33656579631) / `9856965744` |
| V2.4 | p42 §3.10 **T74**; §3.13 **T77** | p43 §3.14 **T78** | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | `006d387354fd9f2aa0d949d79daecd5b8025ca1c885a934f432a4ba50eb982f9` | `25a04aa83e6480434f8b1118440123e1179cc35ba736efe10e030f298d708185` | [33658306978](https://github.com/MarcLeinenDE/VDV301/actions/runs/33658306978) / `9857652638` |

The actual body captions are `Description of DoorOperationStateEnumeration`, `Description of GNSSCoordinateSystemsEnumeration`, and `Description of GNSSQualityEnumeration` with version-specific table numbers exactly as printed above. The official source URLs and source SHA pins are retained in the canonical locator registry.

### Additional V1.0-only grouped subexamples (not silently propagated to later versions)

- Official V1.0 original printed **p24 §2 introduction** spells English title `Common enummerations` (PNG SHA256 `25db03ee88b6aba8f30dfcd30a09128db0852ac6579fd5c8df6e4dbb83499f0f`).
- Printed **p18 §1.42 Table42 — ServiceSpecification**, `ServiceName` prose refers to a nonexistent `cf. 0` (PNG SHA256 `793144ddf643e6d4f666c9233e0f6f77dd46b34de039127ae49296de6163191e`). `cf. 0` also appears in later extracted text, but no additional individual page/table body claim is promoted here without its own specifically verified locator.
- Printed **p30 §3.1**, explicitly English `Version 1.1` history subsection has `ergänzt` and `Typ` (PNG SHA256 `1e8cd399b77af5692e641d0bd2faae183c82b30858671d973a139496d57f4d7c`). Later Common publications have intentional German and English history subsections: the mere presence of German words in a German part is **not** treated as a continuing English translation error.

Other grouped cross-reference/caption examples in each historical Deep Read stay historically preserved without assuming every V1.0-only example reproduces literally in every later version.

## Exact selected XSDs: contextual evidence, NOT a new executable finding

| Version | Exact selected Enumerations XSD | Pinned Git blob | Singular simpleType definition |
| --- | --- | --- | --- |
| V1.0 | `IBIS-IP_Enumerations_V1.0.xsd` | `a9bea5bc73003ed91ded8519db06c32c4067831d` | line 122 `GNSSCoordinateSystemEnumeration` |
| V2.0 | `IBIS-IP_Enumerations_V2.0.xsd` | `27e3c183b00381d959622d13c10543123af8eef6` | line 125 `GNSSCoordinateSystemEnumeration` |
| V2.1 | `IBIS-IP_Enumerations_V2.1.xsd` | `311464690ad60749ed8d326217787e4b8ed0b718` | line 127 `GNSSCoordinateSystemEnumeration` |
| V2.2 | `IBIS-IP_Enumerations_V2.2.xsd` | `2a23b512379b18e8f122ac1272cef8229fb86283` | line 129 `GNSSCoordinateSystemEnumeration` |
| V2.3 | `IBIS-IP_Enumerations_V2.2.xsd` | `2a23b512379b18e8f122ac1272cef8229fb86283` | line 129 `GNSSCoordinateSystemEnumeration` |
| V2.4 | `IBIS-IP_Enumerations_V2.4.xsd` | `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` | line 129 `GNSSCoordinateSystemEnumeration` |

The V2.3 released Common XSD uses the official **Enumerations V2.2** dependency; no synthetic Enumerations V2.3 or latest-wins substitution. The V2.4 **official PDF** may be used as publication evidence while its exact separately selected V2.4 XSD is still **candidate/integration**—never mislabeled as official. None of these names authorize a plural enum type.

## Version-boundary and falsification rationale

- **First available / first affected**: Common V1.0 original body pages 26–27, plus specific additional V1.0 material pages 18, 24, 30.
- **Intermediate official affected releases checked independently**: V2.0, V2.1, V2.2, V2.3. Each has the same core GNSS naming inconsistency and adjacent wording typos in the actual visible source.
- **Last verified affected publication**: Common V2.4 original body pages 42–43. In this audited VDV Common corpus there is **no independently verified corrected later Common publication**, and no earlier separate predecessor. A later artifact must be rechecked rather than presumed corrected or erroneous.
- **Language guard**: XML identifiers/enum captions use English words across the original published Common tables. The V1.0 English history has mixed-language residue, but deliberately bilingual later versions cannot be characterized by the same fault merely because German text occurs.
- **Active disproof**: candidate claims that the singular/plural pair represents two legitimate schema types fail against exact XSD blobs, which define only the singular type. That does **not** turn the printed plural table label into a runtime validation mismatch: there is no demonstrated XML instance field/value difference. Claims that the named editorial residue was corrected by V2.0 or V2.4 fail against the independent original-page images. Some isolated V1.0 copy errors were in fact absent from later publications, as preserved above.

**Classification**: `confirmed_pdf_defect`, `documentation_spelling`, `normative_authority=contextual_only`, `no_runtime_diagnostic` and `runtime_match.state=not_applicable`. No XSD changes, aliases, validator PASS/FAIL changes, code generation rules or runtime matcher implementation.

## Scope of terminal update

This block extends **one existing finding's** semantic documentation scope V1.0→V1.0–V2.4, adds exactly **one** new canonical source locator entry with six individually verified official-documentation lanes, one PDF visible-body verification and one version-boundary record. After complete GitHub gate and terminal status-only close, progress becomes **91/192** complete (91/91 body, 91/91 boundary, **101 open**), next **DRCOM20-001**. Prior historical V1.0-only notes and WIP evidence remain accessible and explicitly superseded for affected-version coverage.

Current GitHub gate run IDs and final-HEAD status are recorded exclusively in `00_START_HERE/CURRENT_STATE.json`.

