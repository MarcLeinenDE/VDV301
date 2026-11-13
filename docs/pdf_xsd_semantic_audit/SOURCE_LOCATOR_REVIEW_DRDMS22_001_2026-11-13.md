# Source-locator review — DRDMS22-001 — 2026-11-13

**Result: complete evidence; CI gated in the canonical repository.** This is the **same existing** documentation-only finding, not a duplicate. The historical V2.2-only scope was corrected to **V2.1–V2.2 affected**, first corrected published DMS document **V2.4**. No XSD or productive SDK implementation changed.

## Independently verified original-body defect

| Official source | Original actually visible printed body locator | Finding |
| --- | --- | --- |
| **VDV 301-2 Basic Services V2.1**, bilingual | **p106, Table 37 — Description of DeviceManagementService.SubdeviceStatusInformationStructure**, continuation of §7.1.34.2 Response | `DeviceStatusInformation 1:1 +DeviceStatusInformation` describes `Detailed device status (cf. table 27)` — **wrong** |
| V2.1 true target | **p105, Table 33 — Description of DeviceManagementService.DeviceStatusInformationStructure**, continuation of §7.1.31.2 Response | **Actual intended Table 33**, documents `DeviceState` and `DeviceStatusList` |
| V2.1 mistaken target | **p103 §7.1.27.1 Request, Table 27 — Description of DeviceManagementService.RestartServiceRequestStructure** | Not the status-information structure |
| **VDV 301-2-0 DMS V2.2**, bilingual | **p24, Table 23 — Description of DeviceManagementService.SubdeviceStatusInformationStructure**, continuation of §2.25.2 Response | Same erroneous `DeviceStatusInformation` description **`(cf. table 27)`** |
| V2.2 true target | **p23, Table 19 — Description of DeviceManagementService.DeviceStatusInformationStructure**, §2.22.2 Response | **Actual intended Table 19** |
| V2.2 mistaken target | **p26 §2.31.1 Request, Table 27 — Description of DeviceManagementService.InstallUpdateRequestStructure** | Not status-information structure |
| **VDV 301-2-0 DMS V2.4**, bilingual, *first corrected published successor* | **p24, Table 23 — Description of DeviceManagementService.SubdeviceStatusInformationStructure**, continuation of §2.25.2 Response | **Corrected** to `Detailed device status (cf. Table 19)` |
| V2.4 true target | **p22, Table 19 — Description of DeviceManagementService.DeviceStatusInformationStructure**, §2.22.2 Response | Actual visible Table19 body/caption is on p22, **not** assumed from adjacent p23 |

### Strongest active disproof

A mere change in table numbering between editions could explain a copied reference; it cannot make the cited table technically correct. The original visible **Table 27** is an unrelated *RestartServiceRequestStructure* in V2.1 and an unrelated *InstallUpdateRequestStructure* in V2.2. The explicitly named status-information structure is printed in the respective original bodies at Table33 (V2.1) and Table19 (V2.2). The correction to Table19 in V2.4 confirms the editorial interpretation. This is **not** a choice-compositor notation issue, an alternate XML element, an XSD defect, or an inferred TOC location.

## SHA-256-verified original visible PDF evidence

All images below were produced by the deterministic GitHub Actions `tools/render_vdv_pdf_pages.py` fallback from the **exact byte/size pinned official original PDF** (the mandatory fallback after the live PDF screenshot backend cache-missed). Actual page headings, table captions, rows and adjacent tables were independently visually inspected.

| Document | Original PDF SHA-256 and byte size | Successful GitHub render / artifact | Original page-image SHA-256 |
| --- | --- | --- | --- |
| `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`; **2671005 bytes** | [run 37897714010](https://github.com/MarcLeinenDE/VDV301/actions/runs/37897714010), artifact **11600767562** | p103 `af75f882cc630d8cbeeb60d68aed2e3fbb47675fc50e38624ddc3b86c99f801a`; p105 `410fef8472cabb9ac343ada24dba932bc0a61dbb2c0378e10472fcab9ad43e23`; p106 `c68f3267cc1253928e1e615b73878883b812ec936b5854f2ce921ca06da7bea2` |
| `DMS_V2.2` | `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`; **1173719 bytes** | [run 43424551144](https://github.com/MarcLeinenDE/VDV301/actions/runs/43424551144), artifact **14035527166** | p23 `ef50b73d735c34d386d2c257c5f6c6ead7b63729ecf43518b24cdb2ea53d385f`; p24 `99fb907c3eb9f27f1770d13ff916daac055ffef90f75d4831935b7202130b492`; p26 `b74ec0ed88e51ba1f32d363d2facc0366a9c51389079516e1dd377fec3030576` |
| `DMS_V2.4` | `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`; **1298127 bytes** | [run 43425060754](https://github.com/MarcLeinenDE/VDV301/actions/runs/43425060754), artifact **14036545472** | p22 `77219201fdc9eb877abd97181516eb38bf2580693f4a4df0af5f3e8222b555bd`; p24 `a5a561d6a8987049ea9636af6b158f03a7ccf087f30889d4731dc97f834f16fe` |

The older V2.1 GitHub artifact was reused only after verifying the exact original PDF SHA/size and matching individual page-image hashes. V2.2 and V2.4 were freshly rerendered under separate crash-safe `gate_pending` state commits. Original byte identities and manifest hashes are preserved, no OCR-derived table locator was promoted.

## Version / language / XSD authority boundary

| Version | Actual selected exact DMS XSD / provenance | Finding scope |
| --- | --- | --- |
| V1.0 separate official German/English publications | `IBIS-IP_DeviceManagementService_V1.0.xsd`, blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4` | No comparable later `SubdeviceStatusInformationStructure`; non-applicable predecessor, keep DE and EN publications independent |
| V2.0 official bilingual Base | `IBIS-IP_DeviceManagementService_V2.0.xsd`, blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a` | No comparable later structure; **last non-applicable predecessor** |
| **V2.1 official Base** | `IBIS-IP_DeviceManagementService_V2.1.xsd`, blob `191b43e01cdaba14b247725689a913c244a67eed`, `SubdeviceStatusInformationStructure` lines470–480 | **First verified affected publication**: p106 Table37 wrong cf.27 vs actual Table33 |
| **V2.2 official standalone DMS** | `IBIS-IP_DeviceManagementService_V2.2.xsd`, blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, lines423–433 | **Last verified affected publication**: p24 Table23 wrong cf.27 vs actual Table19 |
| V2.3 local integration-only XSD | `IBIS-IP_DeviceManagementService_V2.3.xsd`, blob `5fe444cf6d10462cc23fd159eb963abbec42248f` | **No published standalone DMS V2.3 PDF** in the canonical source registry. No inferred PDF persistence/correction. |
| **V2.4 official PDF / separately selected candidate XSD** | `IBIS-IP_DeviceManagementService_V2.4.xsd`, candidate/integration blob `d222dfd98b2be3777576388da7ace8f333d24c3f` | **First corrected published original PDF**. Candidate executable XSD must never be labelled official. Excluded from affected semantic/runtime scope. |

The bilingual V2.1 Base and dedicated V2.2/V2.4 originals contain the relevant **English technical member table**. No separate German translation of these tables is inferred, and the separately published V1.0 German and English language sources are treated as distinct historical controls.

## SDK and evidence consequences

- **Identity and classification:** reuse `DRDMS22-001`, `confirmed_pdf_defect`, `documentation_only`, `documentation_navigation_error`. Existing V2.2 finding is **corrected for a newly verified earlier V2.1 boundary**, not counted twice.
- **Exact XSD rule:** the official V2.1 DMS XSD line480 and V2.2 line433 both declare `SubdeviceStatusInformationStructure.DeviceStatusInformation` of type `DeviceStatusInformationStructure`. The PDF's wrong cross-reference **cannot change XML validity**, add an alias, alter any XSD field, or create a different DMS operation.
- **Runtime / provider:** `no_runtime_diagnostic` and `runtime_match.not_applicable`. No SDK matcher, resolver, XSD or application-code modification. Preserved [EV-141 closure run 33974702338](https://github.com/MarcLeinenDE/VDV301/actions/runs/33974702338) is previous contextual evidence; no newly executed XML-instance validation suite is claimed for this pure documentation-navigation typo.
- **Diagnostics:** source-authoritative DE/EN `title`, `short`, `long` and `recommendation` now separately describe V2.1 37→33 and V2.2 23→19 and the official PDF V2.4 correction.
- **Progress:** one additional unique source locator yields **97/192**, **97/97** original PDF body verifications and **97/97** version boundaries, **95 remaining**. All counter mirrors and canonical registers are updated in the same substantive `gate_pending` commit. Historical reports/tests unchanged.
- **CI closure:** complete only after full schema-audit-validation SUCCESS on the substantive commit, followed by distinct `terminal_clean` finalization and final HEAD handoff-integrity SUCCESS; actual run IDs reside in the canonical state and GitHub Actions.
- **Next unique missing locator:** `DRDMS22-002` (not started).
