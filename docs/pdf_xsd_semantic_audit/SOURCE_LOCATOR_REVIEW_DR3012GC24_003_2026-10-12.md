# DR3012GC24-003 — Duplicate digit 2 in English permitted IBIS-IP-version characters (GC V2.2–V2.4)

Date: 2026-10-12. Existing finding identity retained. The previously V2.4-only semantic scope is corrected after independently reviewing the original V1.0, Basic V2.0/V2.1 and GC V2.2/V2.3/V2.4 PDF bodies. No new finding identity.

## Visible original claim and version boundary

In visible English **§1.5 IBIS-IP-Version**, the allowed character sequence is `('0','1','2','2','3','4','5','6','7','8','9' or '.')`: the literal digit `2` is repeated. On the same original publications' visible German **§1.5 Versionierung in IBIS-IP**, each of `0`–`9` occurs once and `.` is separately listed. The nearby examples `2.1a`, `2.0.1` and `.2.1` remain invalid under the stated formatting rule. Duplicate listing does not create a different accepted character or a different executable grammar.

| Pinned official PDF | Printed page(s) checked | Observed result / boundary role |
|---|---|---|
| VDV-Schrift 301-2 V1.0 (Deutsch, 07/2016) | p19 | No enumerated allowed-character list in §1.6; historical_pre_character_list |
| VDV-Schrift 301-2 Basic Services V2.0 (02/2018) | p19 | No enumerated allowed-character list in §1.6; historical_pre_character_list |
| VDV-Schrift 301-2 Basic Services V2.1 (07/2018) | p20 | No enumerated allowed-character list in §1.6; last_pre_character_list_predecessor |
| VDV-Schrift 301-2 General Conventions V2.2 (08/2019) | DE p11; EN p15 | DE correct sequence 0–9; EN digit 2 twice; first_affected |
| VDV-Schrift 301-2 General Conventions V2.3 (02/2021) | DE p11; EN p15 | DE correct sequence 0–9; EN digit 2 twice; intermediate_affected |
| VDV-Schrift 301-2 General Conventions V2.4 (01/2023) | DE p14; EN p18 | DE correct sequence 0–9; EN digit 2 twice; last_checked_affected_no_corrected_successor |

**First affected:** GC V2.2 (08/2019), English §1.5 p15. **Also affected:** GC V2.3 English p15 and GC V2.4 English p18. **Last preceding publication:** Basic V2.1 §1.6 p20 has no such enumerated character list, not a corrected list. No later corrected GC publication is independently established. The V1.0 pinned original checked is German; no English V1.0 counterpart is asserted in this evidence.

## Byte-pinned original sources and visible-body render

Original PDF bytes: GitHub Actions **run 33752224704**, artifact **9892036202**, `disc-source-pin`, files `pdfs/*.pdf`. All six PDF SHA-256 and exact sizes match `audit_registry/pdf_source_pins_v0.1.json`, selected official URLs from `audit_registry/pdf_source_registry_v0.1.json`. PDF bytes stayed outside git. Local PyMuPDF 180dpi render used after live PDF screenshot cache misses; every rendered page inspected against its visible section heading, character list and footer. PDF page indices match printed page numbers on these pages.

- **VDV301-2_V1.0_DE** official original SHA256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` (1790447 bytes): DE/shared p19 PNG SHA256 `a8bceeefcbf6956105ddc6d7d6cdab830e9534acb73ab4f5837ea29a20d77770`; actual visible target `§1.6`.
- **VDV301-2_BASE_V2.0** official original SHA256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` (2374295 bytes): DE/shared p19 PNG SHA256 `039c69c232e4bfd9a09c0ca0794cfee461a3758af397e34978132a57f1736338`; actual visible target `§1.6`.
- **VDV301-2_BASE_V2.1** official original SHA256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` (2671005 bytes): DE/shared p20 PNG SHA256 `e26a34c9db55a58ac462da784b7ac0678a592a88f076a0af7a828d305b1a69a1`; actual visible target `§1.6`.
- **VDV301-2_GC_V2.2** official original SHA256 `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` (1562305 bytes): DE/shared p11 PNG SHA256 `d009d01315f5efacd9034cce96c2fc3bd33ea2894f95834d5ac5b0c75203edea`; English p15 PNG SHA256 `5fc5158191d3308010c7af3d634c40438b979a27c868319ca5263620003af947`; actual visible target `§1.5`.
- **VDV301-2_GC_V2.3** official original SHA256 `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` (1057483 bytes): DE/shared p11 PNG SHA256 `c6aebcd51c19dbedbde81f4eea77df569a50fadb88c9a68b49e7446edf165d22`; English p15 PNG SHA256 `4b675ffb5cd6d6f67ba3e17946018c30be0a39e8e59a50b4c1799e860eb0c2e0`; actual visible target `§1.5`.
- **VDV301-2_GC_V2.4** official original SHA256 `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` (1767094 bytes): DE/shared p14 PNG SHA256 `ccc94a427e3f975e81d1aa963ec5214a74cee04fd4c853f85819e6f73e99100b`; English p18 PNG SHA256 `7c4e2c8f6aafcf8f0f4eb2f09c767670a31a00ccf62d0cb9959d11c3e604e9c8`; actual visible target `§1.5`.

## Context, disproof and normative treatment

The strongest counter-hypothesis was that two occurrences of `2` encode an additional version-token requirement. It fails: the passage lists permitted **characters**, the German translation lists the same distinct characters without duplication, all three independent English editions repeat the same editorial artifact, and the surrounding one-major-digit/dot/one-minor-digit prose with invalid examples remains unchanged. No distinct syntax operator, compositor, regular expression or XSD enum is implicated. Earlier V1.0/Basic2.0/Basic2.1 do not supply an alternative explicit character list.

Classification: `confirmed_pdf_defect`, English-only editorial list redundancy, documentation-only. Authority: pinned official **PDF publications**; not an executable XSD conformance claim. `normative_authority=contextual_only`, `validation_effect=documentation_only/no_runtime_effect`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`. Do not infer an extra parser rule, don't reject a provider for duplicate documentation tokens, don't mutate XSDs, and don't create an SDK matcher. VDV editorial correction may enumerate V2.2/V2.3/V2.4; historic publications retain their exact findings.

Source-locator/body and version-boundary register progress 78 → **79 / 192**, remaining 113. Substantive change staged `gate_pending`, followed by full schema gate and a distinct `terminal_clean` closure once successful. Next canonical missing locator **DR3012GC24-004**.
