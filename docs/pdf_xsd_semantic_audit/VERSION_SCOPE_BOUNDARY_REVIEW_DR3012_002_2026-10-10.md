# DR3012-002 — DNS-SRV Weight RFC 2782 full DE/EN version boundary (2026-10-10)

**Proof complete / full gate pending. Material version-scope expansion: STOP package after this finding.** Existing DR3012-002 identity retained; first affected V1.0 both languages, last checked V2.4 both languages.

## Independently reviewed actual original-body table rows

Official source PDFs SHA256-matched the registered immutable pins. Original source bytes for V1.0 German and V2.0–V2.4 are preserved in GitHub run **33752224704** artifact **9892036202**; selected actual body pages were re-rendered at PyMuPDF 1.6 scale and visually checked without OCR or TOC inference. V1.0 English official source was also independently hash-pinned and strictly rendered by GitHub run **38027748616**, artifact **11661241034**, digest `sha256:85694cadb43c25a60fe51e20ba9dfb6a55910fcc64623326206ea174a9a2e977`.

| Version | Language | Actual page | Visible table/caption | Exact source ID | Official PDF SHA256 | Full-page PNG SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0 | DE | p26 | Tabelle 2 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_V1.0_DE` | `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | `195f591ef750f772536a00a4962041ca8a9ae482973349ac3700c73bbcb63556` |
| 1.0 | EN | p28 | Table 3: Meanings of the SRV record in DNS-SD (caption p29) | `VDV301-2_V1.0_EN` | `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | `ed70b72dc2a367b76ed3846c7345d2f09249766f3ae426fe3a94f11b1fac7432` |
| 2.0 | DE | p33 | Tabelle 3 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_BASE_V2.0` | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | `9dcb6b8b0f295137d8646bfcf683735cf345a27af8351d8283312950a2a10e51` |
| 2.0 | EN | p34 | Table 4: Meanings of the SRV record in DNS-SD | `VDV301-2_BASE_V2.0` | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | `bbdcc253188db6442fbdd747762e46661b51085cd4429837129830f50bfa7d89` |
| 2.1 | DE | p34 | Tabelle 3 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | `c9106f49fb5afe450dde43cd588560b496db2a05729075771a044317084eb85d` |
| 2.1 | EN | p35 | Table 4: Meanings of the SRV record in DNS-SD (caption p36) | `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | `156bdeb5f86a288e468141e5fd6278f06020326b97c7441495b28e0baf2b713c` |
| 2.2 | DE | p26 | Tabelle 2 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_GC_V2.2` | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` | `ba892aff84631ef60326b02ed6e6972ecce578b873a52ac62c570126ae56f0c8` |
| 2.2 | EN | p32 | Table 2: Meanings of the SRV record in DNS-SD | `VDV301-2_GC_V2.2` | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` | `7fa22804a7084cd46a0a6880dbcc86873fdc034b6f23f16c534e1d857459b1ec` |
| 2.3 | DE | p26 | Tabelle 2 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_GC_V2.3` | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` | `f350e73e4273f2eae550bae036328e2504bc4b43778b4a272c586e0622a8181e` |
| 2.3 | EN | p32 | Table 2: Meanings of the SRV record in DNS-SD | `VDV301-2_GC_V2.3` | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` | `d308b4730abdf7b9663ca9d8cbf9907faf5a458a0c601d6e67a4f049c89733d9` |
| 2.4 | DE | p29 | Tabelle 2 Bedeutungen der SRV-Records in DNS-SD | `VDV301-2_GC_V2.4` | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` | `6c54279504998e27cc096beff1d6260abf01ed1e77bce71b43e893aabb0e6968` |
| 2.4 | EN | p36 | Table 2: Meanings of the SRV record in DNS-SD | `VDV301-2_GC_V2.4` | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` | `bda39111ffe5c0d5b018dacddf330607030c2e3d9971737e2b6ad10378d87afc` |

**DE 1.0 p26 Table2** says literally `bei gleichem Gewicht ... geringeren Gewicht`, internally contradictory; **EN 1.0 p28 Table3 (caption on p29)** instead says a service with lower Weight is preferred, contradicting RFC2782 but not sharing the German same/lower phrase. Bilingual **Base 2.0 and 2.1** each contain independent German and English SRV tables, and both retain this error. **Common Conventions 2.2,2.3,2.4** likewise each have actual DE and EN SRV tables; none of the checked language tracks corrects the low-Weight statement. Even the latest independently checked official Common Conventions 2.4 remains affected, with no verified later corrected successor in the pinned corpus.

Full exact official PDF URL + pin metadata: `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`. Historical original V1.0 DE visual record: `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3012_002_2026-10-06.md`, EV-129. Source body page numbers are actual printed numbers, not extrapolated German pagination to English. The EN V1.0 translation expressly defers to German original if inconsistent.

## External authority and active falsification

[RFC2782](https://www.rfc-editor.org/rfc/rfc2782.html) defines DNS SRV priorities and weights separately: a client MUST attempt reachable *lowest-numbered Priority* first; among equal Priority, larger *Weight* values SHOULD get proportionately more probability of selection. The German V1.0 literal same-weight/lower-weight phrase cannot describe a coherent rule. Reading its first `Gewicht` as a typo for `Priorität` would still incorrectly prefer lower Weight, as the separately published English translation and all later versions explicitly do. RFC2782 zero-weight and weighted random selection also do not reverse this direction.

## Scope and SDK consequences

The same existing documentation/reference finding now covers **12 actual language+release lanes**: 1.0 DE/EN, 2.0 DE/EN, 2.1 DE/EN, 2.2 DE/EN, 2.3 DE/EN, 2.4 DE/EN. Earlier Part2 and later corrected successor not independently established. `confirmed_pdf_defect`, `primary_surface=external_standard`, `normative_authority=contextual_only`, `sdk_behavior=warning`, `runtime_match=not_applicable`. External-network protocol guidance does not change selected XSD bytes, XML validation, required child elements or provider FAIL classification; no alias or new runtime matcher.

**Boundary progress 60/70 -> 61/70, 9 pending; next DR3012-003 only in fresh package.** Stop current package on the material DE/EN scope expansion. Final gate is required on exact pending HEAD and then a separate terminal-clean handoff with its own successful handoff-integrity gate.
