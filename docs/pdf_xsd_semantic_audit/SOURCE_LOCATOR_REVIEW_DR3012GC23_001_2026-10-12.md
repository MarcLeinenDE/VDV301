# DR3012GC23-001 — German history subheadings V2.3, corrected in V2.4 (2026-10-12)

Existing finding identity `DR3012GC23-001`. Only official General Conventions **V2.3** is affected; V2.2 is the nonaffected predecessor and V2.4 the corrected nonaffected successor.

## Original document-body evidence

| Edition | Official pinned SHA-256 / source bytes | Visibly checked PDF body | Scope |
| --- | --- | --- | --- |
| GC V2.2 | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` / 1562305 | printed p70 **§7 Versionshistorie / 7.1 Version 2.2**, correctly DE/EN `7.1.1` and `7.1.2`; printed p71 starts **§8 Begriffe** | nonaffected predecessor |
| GC V2.3 | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` / 1057483 | printed p70 §7.1 still correct; printed p71 **§7.2 Version 2.3** has German `7.1.3 Funktionale Erweiterungen` and `7.1.4 Technische Ergänzungen/Korrekturen`; English same p71 `7.2.1 Functional Upgrade` and `7.2.2 Technical Upgrade/Corrections` | **affected** |
| GC V2.4 | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` / 1767094 | printed p75 **§7.2 Version 2.3**, bilingual `7.2.1`, `7.2.2`; §7.3 uses `7.3.1`, `7.3.2` | corrected nonaffected successor |

PDF links and immutable byte pins: `audit_registry/pdf_source_registry_v0.1.json`, `audit_registry/pdf_source_pins_v0.1.json`. Actual rendered visible body was used instead of TOC or cross-reference inference.

## Evidence provenance

- V2.2 exact-pinned original run38229436636 artifact11738251695 source 96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051, printed p70 PNG 7e620ddd9d380fa99f68e57ddb4bd084840dde20a7f90b653bc942ce155591a5, p71 PNG d0b1a67e0a70929f285b3ec16109b8d0a093f3d903644f0fd0ec2eb8cce4d7ce
- V2.3 EV-133 run33842952649 artifact9925516670 source 4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603, original printed p70 PNG da503ff771c2664991de5d3938c50556e5ed1344e64806c5a41a2b3cf9716d94, p71 PNG 97005280fa97521f2d8830dd60e11cc56512020a71a845fa33684cb0337827d7
- V2.4 EV-134 run33843888080 artifact9925822375 source 048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d, corrected printed p75 PNG 7d771d06392c0d7af610ad3eee211e60013f3946d6dfabd48f15ece28dbd0d68

V2.2 [fresh exact-byte PDF fallback](https://github.com/MarcLeinenDE/VDV301/actions/runs/38229436636) verified size/hash before 160 dpi render p69-71; artifact `11738251695` includes `render_manifest.json` with original PNG hashes. V2.3 [EV-133](https://github.com/MarcLeinenDE/VDV301/actions/runs/33842952649) and V2.4 [EV-134](https://github.com/MarcLeinenDE/VDV301/actions/runs/33843888080) preserve original-page artifacts; PNG SHA-256 values independently calculated from those artifacts.

## Disproof, classification, SDK result

The alternative hypothesis of intentional numbering continuation or a TOC-only error fails: the *actual original V2.3 body* prints 7.1.3/7.1.4 below 7.2 even though its English counterpart prints correct 7.2.1/7.2.2. The predecessor §7.1 labels 7.1.1/7.1.2 correctly and official V2.4 visibly corrects the old V2.3 heading.

Classification: **confirmed PDF editorial/history-navigation defect**; `normative_authority=contextual_only`; `validation_effect=documentation_only/no_runtime_effect`; `sdk_behavior=no_runtime_diagnostic`; `runtime_match=not_applicable`. No XML instance shape/value/cardinality affected. The exact chosen historical XSD remains the executable XML validation authority, but XSD locator/sample is not applicable to a history heading. V2.4 PDF publication does not promote candidate/integration XSDs to official.

The frozen 192-item semantic identity inventory is preserved. Corrected `version_scope` contains V2.3 only; V2.4 explicitly resides solely in nonaffected source-locator and boundary evidence. Source/body locator **76/192** and boundary **76/76**, **116** missing source locators. No upstream remediation or schema content edit in this audit phase. All gates and terminal handoff required before closure. Next `DR3012GC24-001`.
