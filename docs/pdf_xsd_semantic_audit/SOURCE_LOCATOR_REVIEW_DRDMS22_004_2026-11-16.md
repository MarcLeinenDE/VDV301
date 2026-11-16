# Source-locator review — DRDMS22-004 — 2026-11-16

**Outcome:** Historical V2.2-only observation is a true but incomplete subset. The singular `GetDeviceErrorMessage` in GetDeviceErrorMessages request prose is confirmed on five independently SHA-pinned official publication bodies: German V1.0, bilingual V2.0 and V2.1, standalone DMS V2.2, and the officially published DMS **V2.4 PDF**. The separately published English V1.0 uses generic Get-operation wording and is **not affected**. No independent official published standalone DMS V2.3 PDF is established. The selected V2.4 XSD is candidate/integration only. Documentation error only; no aliases, schema edits, XML validation overrides or productive SDK matcher.

## Exact visible original publication body

| Edition/language | Exact source/visible body and request prose | Corresponding real operation heading | SHA-verified render proof |
| --- | --- | --- | --- |
| V1.0 DE | VDV301-2_V1.0_DE, visible printed p59, §7.1.11/§7.1.11.1: GetDeviceErrorMessage | GetDeviceErrorMessages | [run 43868258506](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868258506), artifact 14225993110, PNG SHA256 `ef708c1d8853bb9330b3145744aba3e23aace4edbc95b44bb4f03668778a658d` |
| V1.0 EN | VDV301-2_V1.0_EN, visible printed p66, §9.3.12/§9.3.12.1: generic Get-operation prose (unaffected) | GetDeviceErrorMessages | [run 43868660266](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868660266), artifact 14225968623, PNG SHA256 `48d490502d9bab10a7e75e5d48ae536176e594cd4c462e0a5c76590c2549215b` |
| V2.0 | VDV301-2_BASE_V2.0, visible printed p94, §7.1.11/§7.1.11.1: GetDeviceErrorMessage | GetDeviceErrorMessages | [run 43868683696](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868683696), artifact 14226753033, PNG SHA256 `bfeaf84c5ef07d0b57ff64790c3e689adf4192613d6300e602f53f0865a9654f` |
| V2.1 | VDV301-2_BASE_V2.1, visible printed p99, §7.1.13/§7.1.13.1: GetDeviceErrorMessage | GetDeviceErrorMessages | [run 43868712810](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868712810), artifact 14226268352, PNG SHA256 `7a719650d552ea42a7fc0ef29f8b0d66cd7639ca10c98245ac676f2b36ecf6dd` |
| V2.2 | DMS_V2.2, visible printed p19, §2.9/§2.9.1: GetDeviceErrorMessage | GetDeviceErrorMessages | [run 43868851957](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868851957), artifact 14226014590, PNG SHA256 `e8b80be432f161601d1349bf36d18fa1240b2fe406eae8d7cd766af2177b327f` |
| V2.4 | DMS_V2.4, visible printed p18, §2.9/§2.9.1: GetDeviceErrorMessage | GetDeviceErrorMessages | [run 43868875443](https://github.com/MarcLeinenDE/VDV301/actions/runs/43868875443), artifact 14226468630, PNG SHA256 `df7a2f470db3e4b20a9c582ebade9f9c87ae755be850ce36488cb7fa5128ab5a` |

Each cited source is registered in `audit_registry/pdf_source_registry_v0.1.json` and exact-byte-pinned in `audit_registry/pdf_source_pins_v0.1.json`. The respective official SHA-256 PDF hashes and sizes are:

- V1.0 DE `VDV301-2_V1.0_DE`: SHA256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`, **1790447 bytes**
- V1.0 EN `VDV301-2_V1.0_EN`: SHA256 `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7`, **2403598 bytes**
- V2.0 `VDV301-2_BASE_V2.0`: SHA256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, **2374295 bytes**
- V2.1 `VDV301-2_BASE_V2.1`: SHA256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, **2671005 bytes**
- V2.2 `DMS_V2.2`: SHA256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`, **1173719 bytes**
- V2.4 `DMS_V2.4`: SHA256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`, **1298127 bytes**

Every render was produced by the canonical `tools/render_vdv_pdf_pages.py` fallback and checked against its own `render_manifest.json`; the original visible PNGs were inspected, and their hashes reverified. Actual visible body headings (§ and printed page) control locators; table-of-contents, OCR/text-layer extraction, version-history references and numerical inference were not substituted. Corresponding plural response structures are in original V1.0 German Table14 p60, V1.0 English Table38 p66, V2.0 Table19 p95, V2.1 Table19 p100, V2.2 Table8 p20 and V2.4 Table8 p19.

## Selected exact schema authority

| Schema | Exact Git blob | Authority and declaration |
| --- | --- | --- |
| `IBIS-IP_DeviceManagementService_V1.0.xsd` | `602a963f91000d0d39e3c271bacb3c7aba73e6d4` | official; plural response structure only; do not invent request root |
| `IBIS-IP_DeviceManagementService_V2.0.xsd` | `74189e0da65563eeb084ec2f3c400e9668d1ee1a` | official; plural group and response |
| `IBIS-IP_DeviceManagementService_V2.1.xsd` | `191b43e01cdaba14b247725689a913c244a67eed` | official; plural group and response |
| `IBIS-IP_DeviceManagementService_V2.2.xsd` | `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d` | official; plural group and response |
| `IBIS-IP_DeviceManagementService_V2.3.xsd` | `5fe444cf6d10462cc23fd159eb963abbec42248f` | integration only; plural; no published DMS V2.3 PDF established |
| `IBIS-IP_DeviceManagementService_V2.4.xsd` | `d222dfd98b2be3777576388da7ace8f333d24c3f` | candidate/integration only; plural; official PDF V2.4 separately remains typo-affected |

Official V1.0–V2.2 XSDs retain their historical exact dependency routes. There is **no singular schema alias**. V1.0 has plural response-declaration evidence without inventing an undeclared global request element. The V2.3 XSD is integration-only and does not prove any V2.3 published PDF wording. The V2.4 PDF is published official text; its selected V2.4 XSD is separately a nonofficial candidate.

## Active disproof, version boundary and diagnostic meaning

1. **Alternative valid singular operation?** Contradicted by the actual same-edition plural heading, plural response table and exact selected schema identifiers; no singular alias is permitted.
2. **Only V2.2?** Disproved by original German V1.0 and V2.0/V2.1/V2.4 original bodies. Keep the older V2.2 record as a historically correct partial observation, not a superseded fabrication.
3. **All V1.0 languages?** Disproved by independently inspected English V1.0 §9.3.12.1 p66, which uses a generic Get description rather than singular. Explicitly separate German and English publication tracks.
4. **Corrected in published V2.4?** Disproved by original official V2.4 PDF §2.9.1 p18 still saying `GetDeviceErrorMessage`. The selected V2.4 XSD remains candidate/integration and cannot imply official release of an XSD.
5. **V2.3 publication scope?** Unverified: there is no independently pinned official DMS V2.3 standalone PDF in the canonical public source registry, only integration-only schema material.

**Classification:** confirmed PDF-prose operation reference error; documentation-only. All executable PASS/FAIL remains strictly governed by the exact selected XSD, with no alias or automatic correction. Existing informational runtime mapping stays `reviewed_not_implemented` (no productive matcher). DE/EN descriptions expanded to the independently verified document/version boundary. This documentation-only audit executed **no new XML-instance test**; historical EV-141 remains background rather than a newly performed test.

## Checkpoint / durability

The existing single finding ID `DRDMS22-004` is updated across the semantic registry, exact source locators, visible-body registry, independent scope boundary registry, reviewed-only runtime mapping and `CURRENT_STATE.json`, for **100/192** uniquely completed locators, **100/100** visibly verified bodies and version/language boundaries, **92 open**. Apply required full schema-audit-validation, separate `terminal_clean` status commit and successful final-HEAD handoff-integrity before claiming completion. After terminal green, publish only durable findings to private ai-mem via reviewed PR. Next unique `DRDMS22-005` must not be started before clean closure.
