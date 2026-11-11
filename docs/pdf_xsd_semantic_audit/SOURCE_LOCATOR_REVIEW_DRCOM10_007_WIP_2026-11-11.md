<!-- NON_CANONICAL_CONTINUATION_DOCUMENT -->

# DRCOM10-007 — original PDF editorial body evidence, intermediate 2026-11-11

**WIP only; NOT terminal or locator-complete; canonical continuation is solely `00_START_HERE/CURRENT_STATE.json`.** Existing unique `DRCOM10-007` had a legacy V1.0-only scope. Fresh checks show repeatable, purely editorial residue in Common V1.0, V2.0, V2.1, V2.3 and V2.4, with V2.2 still requiring a new original-page render. No XSD, parser, runtime or SDK aliases may be inferred from incorrect textual table captions.

## Independently reopened exact original body pages

The available historical GitHub Actions ZIPs were re-opened, exact PNG SHA256 recomputed and compared to the archive manifest, while its official PDF SHA/byte size matched the canonical source pin. The actual image shows the heading, body, nearby tables and *visible* caption; names and table numbers are not copied from TOC, inferred sequence or extracted text.

Every line below records **two distinct original pages**: DoorOperationState/GNSSCoordinateSystem(s) and the following GNSSQuality; Table numbers differ by publication. On each first page, visible table text says `dorr operation`; GNSS §heading uses `GNSSCoordinateSystemEnumeration`, while the table cell and caption use `GNSSCoordinateSystemsEnumeration`. The following page visibly spells `Infromation about the GNSS quality`. These strings have **no independent XML schema validity effect**.

| Official original | Main original body page (DoorOperation / GNSS) | Next visible page GNSSQuality | Original PDF SHA-256 / size | First PNG SHA256; next PNG SHA256 | Historical original GitHub run / artifact |
| --- | --- | --- | --- | --- | --- |
| V1.0 | p26 §2.8 Table69, §2.11 Table72 | p27 §2.12 Table73 | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` / 892769 | `932f4a3acc4fc58fbd58cb649fd766b3b87700e58a2b53d2665c0512c7fed99e`; `68c6dc2ccead654a25a805c9a4d3163bb7ab2a13c2a6d24b996ab59160d9d83f` | 33275626001 / 9721397514 |
| V2.0 | p34 §3.10 Table74, §3.13 Table77 | p35 §3.14 Table78 | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` / 946088 | `ba97aaea09a3ca7b60b1ae2493392f0336cf93269fd757ed256adfc3dbd1cee8`; `7821bb75c2ce343c9362c29a1b0f7658ca352a6ee913f37eda406a67421b0004` | 33279811315 / 9722644456 |
| V2.1 | p36 §3.10 Table74, §3.13 Table77 | p37 §3.14 Table78 | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` / 1274051 | `8649ce7fdf571a12929d43db76e433acdc1d4b127c77c393b253ff72aa4ccef8`; `ff49b35913404b6642aaf3181d0092cc552dfeddcc2f8ab14bf676bc3811f1de` | 33393002497 / 9758203545 |
| V2.3 | p39 §3.10 Table75, §3.13 Table78 | p40 §3.14 Table79 | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` / 793521 | `072e30327edc317fb78b5709258a41b78585438f7f973dc24e202761a522a6e0`; `fbb2a0356b179911943597058401264cdf86cc43918796a3844263afa459884a` | 33656579631 / 9856965744 |
| V2.4 | p42 §3.10 Table74, §3.13 Table77 | p43 §3.14 Table78 | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` / 1689647 | `006d387354fd9f2aa0d949d79daecd5b8025ca1c885a934f432a4ba50eb982f9`; `25a04aa83e6480434f8b1118440123e1179cc35ba736efe10e030f298d708185` | 33658306978 / 9857652638 |

V1.0 separately has `Common enummerations` in its enumeration section (original printed p24, §2 introduction), and visibly retained German words in the *English* Version 1.1 history subsection (printed p30 §3.1, PNG SHA `1e8cd399b77af5692e641d0bd2faae183c82b30858671d973a139496d57f4d7c`, original artifact 9721397514); the same incorrect `cf. 0` reference is visible at p18 §1.42 **Table42** (ServiceSpecification.ServiceName, PNG SHA `793144ddf643e6d4f666c9233e0f6f77dd46b34de039127ae49296de6163191e`). Later versions have separate bilingual history lanes; *their intentional German-language bullets are not automatically copied into the V1.0 English-language error claim*.

The selected exact Enumerations XSDs independently define the **singular** `GNSSCoordinateSystemEnumeration`: V1.0 blob `a9bea5bc73003ed91ded8519db06c32c4067831d`; V2.0 `27e3c183b00381d959622d13c10543123af8eef6`; V2.1 `311464690ad60749ed8d326217787e4b8ed0b718`; V2.2 and V2.3 Common dependency `2a23b512379b18e8f122ac1272cef8229fb86283`; V2.4 only **selected candidate/integration** Enumerations `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`. No plural XSD simpleType exists in these pinned blobs. This contextual corroboration does **not** turn the editorial finding into a validator issue, an alias or an XSD correction.

## Open: official V2.2 body image

Historical deep read `docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.2.md` independently lists the same grouped residue, but fresh visible body page/table anchors are still unconfirmed. Exact original source pin `COMMON_V2.2`, SHA256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, 1411558 bytes. Pinned visual GitHub workflow request was committed as `74214690dacc93aeade78efa221b6c6313422e00`, source `COMMON_V2.2`, pages `38-42`, workflow run `43111602309`. Retrieve the artifact, verify render_manifest source hash/size and **individual PNG digests**, then visibly check actual section/table/captions.

**No structural entry credit until V2.2 is verified.** Afterward reconcile actual six-version scope, preserve version-specific differences as distinct subexamples in a single finding; add one locator, one body verification and one version-boundary verification with the same finding ID; keep no runtime diagnostic, no XSD change; update every counter and SDK summary, pass full GitHub gates, separate `terminal_clean` and final-HEAD gates. Only then consider an ai-mem memory PR.

