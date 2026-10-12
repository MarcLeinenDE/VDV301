# DR3012GC22-001 — unresolved Word cross-references, corrected in V2.3 and reintroduced in V2.4 (2026-10-12)

**Identity:** Existing unique finding DR3012GC22-001. The planned DR3012V20-009 does not exist in the 192-entry semantic inventory. Resume at the actual first structurally unlocated finding, rather than manufacturing a new identity.

## Exact official byte pins and visible body targets

| Edition, status | Official source SHA-256 | Actual independently visible original body |
| --- | --- | --- |
| **General Conventions V2.2 — affected** | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, 1,562,305 bytes | printed p13 **§1.3 Device Classes**; p52 **§5 Prinzipien in IBIS-IP**, system-start paragraph; p62 **§6/6.1** German XML/table notation introduction; p64 real **Tabelle 5** caption and §6.1.3.1; p66 English **§6.1 Notation of XML Elements and Structures**. All five show literally `Fehler! Verweisquelle konnte nicht gefunden werden.` |
| **General Conventions V2.3 — corrected intermediate** | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603`, 1,057,483 bytes | Historical independently pinned V2.3 full-text read found no literal broken Word-reference marker. Fresh **p52** §5 system-start paragraph visibly omits the bad chapter reference; **p64 Tabelle 5** caption visibly reads `Beispiel für die tabellarische Notation einer XML-Struktur`, without the bad reference; original p13/62/66 and version-history pages70/71 were also rendered as controls. V2.3 is **not** an affected lane. |
| **General Conventions V2.4 — same-root regression** | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d`, 1,767,094 bytes | printed p16 **§1.3 Device Classes**; p56 **§5 Prinzipien in IBIS-IP** startup; p66 **§6/6.1** German XML notation; p68 actual **Tabelle 5** caption; p70 English **§6.1 Notation of XML Elements and Structures**. Same literal Word failure text restored/reintroduced at five corresponding body locations. |

Authoritative body evidence:

- V2.2 [EV-132](https://github.com/MarcLeinenDE/VDV301/actions/runs/33782124756), artifact **9903986586**, `ev132_result.json`, pinned original PDF and pages 13,52,62,64,66 PNGs. Independently inspected originals, including **p64 Table5**, SHA256 `60abf559d433662104701414006a64a99607cbc2ebea462b4d825d0551f6249a` and system-start p52 `3581e3491bbef20213e871afd3cd3ebcd217aeafc1c6cf8a97d6f32b1a768065`.
- V2.3 [EV-133](https://github.com/MarcLeinenDE/VDV301/actions/runs/33842952649), artifact **9925516670** plus fresh strict original [run38218016512](https://github.com/MarcLeinenDE/VDV301/actions/runs/38218016512), artifact **11732671602**. Exact verified source PDF, fresh PNG p52 `0da4d228c4fc228ea62000b753e3b3913531305d86c1e8f4807ee8f79fa8427f`, corrected Table5 p64 `a2b077ecb95b3862e967dfd866b70ec0138345c72c64e106e88b6e4c2e6316eb`. Independent prior source-wide string absence from `deep_read/VDV301-2_GC_V2.3.md`, not an inference from just two clean pages.
- V2.4 [EV-134](https://github.com/MarcLeinenDE/VDV301/actions/runs/33843888080), artifact **9925822375**, exact source PDF and targeted original p16,56,66,68,70 PNGs; visually rechecked p16 §1.3 and p68 original **Table5**. p68 PNG SHA256 `12add75b73063225d4731f259d8c35e83f5f9cdf6e290ba1509f5206007684f7`.

All three original PDFs are official byte-pinned publications. The source hash, byte sizes, and deterministic rendered PNG evidence are independent of the historical chat. PDF page/section/table body is the locator authority; do not treat the table of contents or version-history references as target locators.

## Boundary disproof and executable authority

The strongest counterhypothesis would be that `Fehler! Verweisquelle konnte nicht gefunden werden.` is intentional standardized cross-reference text or somehow normative XML syntax. It is a Word field-resolution diagnostic, appears inside ordinary prose or actual Table5 captions where a chapter number is expected, vanishes in V2.3, and reappears in V2.4. It is **neither** an IBIS-IP technical element **nor** an allowed XML identifier or schema value.

V2.2 version history printed p70 states technical corrections **Keine**; that does not make these broken cross-references meaningful. No official XSD declares such PDF references as executable constraints. V2.2 official Common / Enumerations XSD blobs `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` / `2a23b512379b18e8f122ac1272cef8229fb86283`; V2.3 official Common `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` and historical Enumerations V2.2 reused. V2.4 separate candidate/integration XML schema authority is **not** promoted by official PDF publication.

**Classification:** confirmed PDF/documentation editorial residue. `normative_authority=contextual_only`, `sdk_behavior=info`, `runtime_match=not_applicable`, no executable XML validity effect. Historical same-root identity preserved across affected noncontiguous releases; no new finding/alias; no vendor FAIL for editorial Word text.

## Canonical progress and handoff

This review corrects the stale next-finding pointer `DR3012V20-009` (no such semantic finding) to the first truly missing identity `DR3012GC22-001`. After one exact-HEAD full schema audit and separate terminal handoff, locator/body verified **73/192 → 74/192**, boundaries **73/73 → 74/74**, semantic classified **192/192** unchanged, runtime matcher implementations unchanged at zero. Next missing real semantic ID **DR3012GC22-002**. No XSD edits/PR remediation.
