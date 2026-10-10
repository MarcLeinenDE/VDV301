# DR3012-003 — SystemDocumentationService heartbeat PDF/XSD release-language boundary (2026-10-10)

**Independently verified source bodies; CI gate pending. MATERIAL finding-scope correction, STOP five-finding package after DR3012-003.** Retain single existing finding identity DR3012-003 and the original correction delta. XSD remains conformance authority.

## Original official publication bodies and exact source pins

| Dedicated service publication | Printed body | PDF element/type in both affected structures | Exact official XSD under published release tag |
| --- | --- | --- | --- |
| Part2 **V1.0 German original**, pinned source `VDV301-2_V1.0_DE` SHA256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | p**65**, actual **Table 25** SystemConfigurationData / **Table 26** StoreSystemConfigurationRequest | **HertbeatIntervall**, 0:1, `IBIS-IP.duration` in both PDF tables | `VDV-301-1.0` `IBIS-IP_SystemDocumentationService_v1.0.xsd`, blob `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`: **HeartbeatIntervall** and type **IBIS-IP.double** in SystemConfigurationData, **IBIS-IP.duration** in StoreSystemConfigurationRequestStructure |
| Part2 **V1.0 English translation**, `VDV301-2_V1.0_EN` SHA256 `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | p**88**, actual **Table 104** SystemConfigurationData / **Table 105** StoreSystemConfigurationRequest | **HertbeatIntervall**, 0:1, `xs:duration` in both; source visibly checked separately | Same V1.0 official released XSD above, not a language-specific XSD |
| Bilingual **Base Services V2.0**, `VDV301-2_BASE_V2.0` SHA256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | p**100**, actual **Table 30** and **Table 31**, visible body | **HertbeatIntervall**, 0:1, `xs:duration` in both | Official `VDV-301-2.0` `IBIS-IP_SystemDocumentationService_V2.0.xsd`, blob `ab959dddbfa2b8ca420af1b079501f94cff38051`: **HeartbeatInterval** and `IBIS-IP.duration` in both |
| Bilingual **Base Services V2.1**, `VDV301-2_BASE_V2.1` SHA256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | p**113**, actual **Table 55** and **Table 56**; p**118** §8.1.2 history is a contradictory correction claim | **HertbeatIntervall**, 0:1, `xs:duration` in both actual tables (unchanged from V2.0 PDF) | Official `VDV-301-2.1` carries the same byte-identical `IBIS-IP_SystemDocumentationService_V2.0.xsd` blob `ab959dddbfa2b8ca420af1b079501f94cff38051`: **HeartbeatInterval** duration/duration |

Original-visible-body evidence:
- V1.0 DE established EV-129 pin run `33765167655`, artifact `9897171006`, page65 PNG SHA256 `1bf5fc05dcc3313bc74ff8994187fedaea0249fb2c9bc1a723a6fd37abff0b36`; original source locator review `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3012_003_2026-10-06.md`.
- V1.0 EN official URL <https://www.vdv.de/301-2ses.pdfx>, **strict byte-pinned** independent render `38032750261`, artifact **11662262438**, digest `sha256:3fabdd9ecb1a0857b2ac935c42349eb6dfb695794aafc0fa7a76d52de5086e5b`, page88 PNG `c9bce23ac4f0eaf8cfe873982fd6735b22c71bc25723caffe3499eaba7523ae1`.
- V2.0 publisher original <https://www.vdv.de/301-2-sds-v-2-0.pdfx>, exact pinned PDF via run `33752224704` artifact `9892036202`, p100 PNG generated for this verification SHA256 `3b6551a60c8514c15753fcbeaec4e678f42bca7184b98e768658902a857ec355`.
- V2.1 publisher original <https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx>, same pin corpus, p113 PNG SHA256 `c900b67dc0e6dc806b65d0084dbf9c395ed4b475a8c6f4e663c8b54bb1f24c9c`; history p118 SHA256 `ce477bf0ccb6e29681438f359edbef7956ee2402a40461c5ff269daa159391fa`.
- Selected official release-tag XSDs directly fetched and matched SHA/blob IDs under `VDVde/VDV301`. V1.0 member lines **43**/**50**, V2.0 member lines **30**/**39**. The local canonical branch carries exactly the same v1.0 and v2.0 blobs as upstream release tags. Original upstream V2.0 blob is byte-identical at official release tags `VDV-301-2.0` and `VDV-301-2.1`.

## Important version-history conflict

**VDV 301-2 Base Services V2.1 p118 §8.1.2** claims the `SystemDocumentationService.SystemConfigurationData.HeartbeatIntervall` and `StoreSystemConfigurationRequestStructure.HeartbeatIntervall` spelling was corrected to **HeartbeatInterval** (references §7.2.2). This is supported by the **official released XSD**, but *not* the corresponding main document's own actual **p113 Tables55/56**: both still say **HertbeatIntervall**. The release history is not a substitute for visibly reading the actual target tables.

## Independent first and last affected boundaries

- First independently verified affected **V1.0** dedicated service publication, original **German** and separately issued **nonbinding English translation**, both have identifier typo **plus** a type mismatch in `SystemConfigurationData` only.
- Independently verified next dedicated Basic Services publications **V2.0** and **V2.1**, both bilingual: same PDF identifier typo still appears. The exact released XSD now uses **HeartbeatInterval** (not V1.0 **HeartbeatIntervall**) and both XSD types are **duration**. Thus the V1.0 double-vs-duration type mismatch does **not** persist into V2.0/2.1.
- Last independently verified affected dedicated service publication in the checked official VDV index: **V2.1**. Published **V2.2, V2.3, V2.4 Common Conventions** are separately scoped documents, and their existence is not proof that they corrected or reintroduced SystemDocumentationService heartbeat tables. No claim about non-verified later service publications.
- No extra finding IDs, XSD aliases, or inferred compatibility fallback between `HeartbeatIntervall` and `HeartbeatInterval`.

## SDK and provider conformance

- **Selected XSD stays normative even when it contains a typo or mismatch with PDF.**
- Selected official **V1.0** profile: correct XML identifier `HeartbeatIntervall`, type `IBIS-IP.double` in SystemConfigurationData and `IBIS-IP.duration` in StoreSystemConfigurationRequestStructure. PDF `HertbeatIntervall` is rejected; `PT5S` fails in the V1.0 double lane, as already executably confirmed by EV-129.
- Selected official **V2.0 XSD** (released under tags 2.0 and 2.1): correct XML identifier `HeartbeatInterval`, type `IBIS-IP.duration` for both structures. V1.0 identifier `HeartbeatIntervall` is **not** a valid alias here; neither is the PDF typo `HertbeatIntervall`. A provider following incorrect PDF XML fails selected XSD, but merely documenting a defect does not create a provider test unless the actual instance and profile are checked.
- Existing runtime matcher is **reviewed_not_implemented**; update profile-specific trigger descriptions and advisory only. Never add an extra hard failure independent of a selected-XSD INVALID outcome.

**Boundary 61/70 → 62/70 verified; 8 pending; next `DR3012-004` in a NEW package.** Stop this current package because the affected version-scope and selected XSD identifier/type changed materially. Exact-HEAD full `schema-audit-validation` and final `handoff-integrity` required for terminal closure.
