# DR3012V20-002 — DNS-SRV Weight, original V2.0 legacy finding and DR3012-002 root-cause correlation (2026-10-10)

**Version/language boundary independently rechecked against existing exact-original visual evidence; complete full-gate and handoff confirmation mandatory.** The historical ID `DR3012V20-002` stays intact. It is not a second independent manufacturer or SDK defect: primary same-root finding `DR3012-002` already covers V1.0–V2.4 in both languages.

## Visible original-body release evidence

Original official VDV PDF bytes and selected page renders were SHA256 pinned and independently reviewed in `docs/pdf_xsd_semantic_audit/VERSION_SCOPE_BOUNDARY_REVIEW_DR3012_002_2026-10-10.md`, including initial V2.0 evidence (EV130, pinned run33780668141 artifact9903434312). This review reuses the exact previously inspected original page hashes, **not TOC, inferred translation pagination, or unverified successor claims**.

| Publication | Original SRV Weight table body | Official source ID | Official PDF SHA256 | Existing independently checked DE/EN page PNG SHA256 |
| --- | --- | --- | --- | --- |
| Base V2.0 | DE p33 / EN p34 | `VDV301-2_BASE_V2.0` | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | DE `9dcb6b8b0f295137d8646bfcf683735cf345a27af8351d8283312950a2a10e51`, EN `bbdcc253188db6442fbdd747762e46661b51085cd4429837129830f50bfa7d89` |
| Base V2.1 | DE p34 / EN p35 | `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | DE `c9106f49fb5afe450dde43cd588560b496db2a05729075771a044317084eb85d`, EN `156bdeb5f86a288e468141e5fd6278f06020326b97c7441495b28e0baf2b713c` |
| Common Conventions V2.2 | DE p26 / EN p32 | `VDV301-2_GC_V2.2` | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` | DE `ba892aff84631ef60326b02ed6e6972ecce578b873a52ac62c570126ae56f0c8`, EN `7fa22804a7084cd46a0a6880dbcc86873fdc034b6f23f16c534e1d857459b1ec` |
| Common Conventions V2.3 | DE p26 / EN p32 | `VDV301-2_GC_V2.3` | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` | DE `f350e73e4273f2eae550bae036328e2504bc4b43778b4a272c586e0622a8181e`, EN `d308b4730abdf7b9663ca9d8cbf9907faf5a458a0c601d6e67a4f049c89733d9` |
| Common Conventions V2.4 | DE p29 / EN p36 | `VDV301-2_GC_V2.4` | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` | DE `6c54279504998e27cc096beff1d6260abf01ed1e77bce71b43e893aabb0e6968`, EN `bda39111ffe5c0d5b018dacddf330607030c2e3d9971737e2b6ad10378d87afc` |

The V2.0 source-locator review `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3012V20_002_2026-10-07.md` independently confirms the original German Table3 p33 and English Table4 p34 (EV130 PNG hashes: p33 `ab523621ba1f0c9bc3eb338b4e084e067feae0abd2af7ac57e7394bf07133b53`; p34 `5a11906f6aa7ad965389ae406d0ce0fa6c3dbd16c3be83083d6724e8d59b924f`). Different pin-verified render runs can produce different page PNG hashes depending on renderer/dpi; the official PDF source SHA256 remains the exact-byte authority.

## Active falsification, RFC authority and version boundaries

All five original publications V2.0, V2.1, V2.2, V2.3 and V2.4 in both language tracks visibly describe smaller SRV `Weight` as preferred. RFC2782 `Priority` uses the *lowest numeric* value for reachable target attempts, whereas at the *same Priority* RFC2782 `Weight` controls **weighted random selection**, with larger Weight receiving proportionally more selection probability; the recorded VDV text conflates the two ideas. RFC2782's zero-weight nuance does not make general lower-Weight preference valid. Primary external source: https://www.rfc-editor.org/rfc/rfc2782.html.

**First already affected predecessor:** V1.0 DE p26 and separately issued EN p28, proven under `DR3012-002`. Thus this is not a newly emerging technical defect in 2.0. **First source of frozen historical ID:** bilingual Base V2.0 p33/p34. **Affected successors:** bilingual Base V2.1 p34/p35; Common Conventions V2.2 p26/p32, V2.3 p26/p32, V2.4 p29/p36. **Last checked affected:** Common Conventions V2.4 both languages; no independently proven later corrected successor.

This is one same-root documentation/external-protocol error already described by `DR3012-002`; retain both historical provenance IDs but **correlate them in provider reports and SDK knowledge** rather than producing duplicate diagnostics. The selected official XSD bytes and PASS/FAIL validity rules are not affected. `confirmed_pdf_defect`, `normative_authority=contextual_only`, `sdk_behavior=warning` as historical warning knowledge, `runtime_match=not_applicable`; no new runtime matcher, XML alias, mandatory method or extra manufacturer failure is authorized.

## Package and gate boundary

Retroactive boundary registry **67/70 → 68/70 verified; 2 pending**, next `DR3012V20-003`. `DR3012V20-002` is the **fifth and last** independently terminalized finding of the authorized package [`DR3012-005`, `DR3012-006`, `DR3012-007`, `DR3012V20-001`, `DR3012V20-002`]. Wait for exact pending-HEAD `schema-audit-validation` SUCCESS; create separate `terminal_clean` handoff commit, and verify green exact-final-HEAD `handoff-integrity` before treating package complete.
