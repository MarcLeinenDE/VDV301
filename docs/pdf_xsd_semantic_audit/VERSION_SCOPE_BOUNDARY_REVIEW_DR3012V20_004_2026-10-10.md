# DR3012V20-004 — SystemDocumenationService editorial typo: German V1.0 vs English V1.0 and bilingual Base V2.0/V2.1 (2026-10-10)

Status: **Original page bodies visually verified, exact official schema authority checked. Full schema gate required for terminal closure.** Historical finding ID retained, no new finding identity and no XSD mutation.

## Pinned visible-body comparison

| Published document/language | Actual visible body | Original PDF source SHA256 | New exact-byte PNG source evidence |
| --- | --- | --- | --- |
| **V1.0 German original** | Printed p**63**, **§7.2 Dienst SystemDocumentationService** heading correct, directly following italic prose spells **SystemDocumenationService** (missing t after `Documen`) | `VDV301-2_V1.0_DE` `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | GitHub strict-pinned fallback run **38041326281**, artifact **11666156248**; page63 PNG `c24bead10e953a31c84d719f878092ebb32521182514cb9fc61e3df9e5c02248`. Independently viewed original visible page |
| **V1.0 separately issued English translation** | Printed p**86**, **§9.9 SystemDocumentationService** heading and immediately following paragraph both correct; **no** `SystemDocumenationService` in the corresponding section. **This English track is NOT affected.** | `VDV301-2_V1.0_EN` `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | GitHub strict-pinned fallback run **38041399999**, artifact **11666116355**; page86 PNG `aed7ed1880d8a7f1f82fc839c051f39dcd027288c7c761b1e9c8de7d31f956c2`. Independently viewed original visible page |
| **Base V2.0 bilingual German + English** | Printed p**98**, **§7.2 Dienst SystemDocumentationService / SystemDocumentationService** headings correct; both immediately following DE and EN paragraphs use **SystemDocumenationService** | `VDV301-2_BASE_V2.0` `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | Prior EV130 original byte-pinned visible-body locator report `SOURCE_LOCATOR_REVIEW_DR3012V20_004_2026-10-07.md`; original p98 PNG `ef250716223afaa4c777db354f9e54d8ad96664b950cdc5b3312173bfd2eef47` |
| **Base V2.1 bilingual German + English** | Printed p**112**, **§7.2** correct headings, both DE and EN prose still use **SystemDocumenationService**. The first checked V2.1 dedicated service publication did **not** correct this prose typo. | `VDV301-2_BASE_V2.1` `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | GitHub strict-pinned fallback run **38041466615**, artifact **11666121559**; p112 PNG `81aafe63728781c934231f4f6d30dccfac2336ec38f9e508079b09bb443c5fc2`. Independently viewed original visible page |

All new PNG SHA256 checks were repeated against the obtained original GitHub render artifacts; hashes match manifests. The official PDF source hashes were verified by the GitHub pinned renderer before page generation. The interactive web screenshot renderer had returned errors, so the mandated deterministic exact-source fallback was used and the resulting images were inspected, not merely OCR or table-of-contents.

## Exact released XSD authority

- Official upstream `VDVde/VDV301` tag `VDV-301-1.0`: `IBIS-IP_SystemDocumentationService_v1.0.xsd`, blob **8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5**. Correct `SystemDocumentationService` prefix in complex type names, e.g. `SystemDocumentationService.GetSystemConfigurationResponseStructure` line32. No `SystemDocumenationService` executable token.
- Official upstream tags `VDV-301-2.0` and `VDV-301-2.1`: both ship byte-identical `IBIS-IP_SystemDocumentationService_V2.0.xsd`, blob **ab959dddbfa2b8ca420af1b079501f94cff38051**. Correct `SystemDocumentationServiceGroup` line7, correct global `SystemDocumentationService.GetSystemConfigurationResponse` line18; no misspelled alias.
- The V1.0 German-vs-English difference is **PDF publication specific**, not two different official schema definitions.

## Boundary and active falsification

No independently verified earlier dedicated SystemDocumentationService publication precedes German V1.0. **First affected: original V1.0 German.** Independent English V1.0 translation shows no typo in the equivalent body section and is therefore a **non-affected control**, not an assumed translation affected by the German source. **First affected English track is bilingual Base V2.0.** The next bilingual Base V2.1 remains wrong in DE and EN prose; latest independently checked affected dedicated service publication is V2.1. No corrected later dedicated service successor is established. Common Conventions V2.2–V2.4 are separate publication scopes, not evidence of a correction.

Disproof checks: correct section headings, correct operation table names and exact release XSD across all versions negate the hypothesis of an intentional alternative service identifier. Separate V1.0 English wording disproves uniform bilingual V1.0 scope. This is NOT the separate heartbeat-identifier finding DR3012-003 / DR3012V20-003 and must not be merged with that cause.

## Classification, SDK and provider behavior

`confirmed_pdf_defect`, `sdk_behavior=warning`, `runtime_match=reviewed_not_implemented`, `normative_authority=selected_xsd`. This typo appears only in **editorial PDF prose**, not in an executable official XSD declaration. An implementation is assessed using its exact selected official schema and actual protocol/operation semantics; this editorial inconsistency cannot itself create an XML-validation error, new mandatory service behavior, an alias, a normalization or an additional provider FAIL. An advisory may explain documentation-derived wrong service names in resolver/code-generation contexts without changing normative XSD PASS/FAIL.

## Boundary closure and next phase

Retroactive version-boundary registry **69/70 → 70/70 verified**, **0 pending**. Set registry `complete`, unfreeze structural source-locator expansion, retain 70/192 structurally complete locators and 192/192 classified semantics. **Next canonical structurally missing locator: DR3012V20-006.** Full exact-HEAD schema-audit-validation and final terminal_clean handoff-integrity must both succeed before starting the next finding.
