# DMS-001 — independently verified version scope (2026-10-09)

**Result: VERIFIED.** The affected scope remains **DeviceManagementService V2.0 only** for the **specific local `DeviceManagementServiceGroup` / public operation-inventory asymmetry**. Not an extra XML/provider conformance failure.

## Exact issue predicate and disproof

The public V2.0 DMS operation inventory cannot be interpreted as a one-to-one listing of `DeviceManagementServiceGroup` entries: V2.0 contains only ten local service-specific elements. Among absent local operation wrappers are `SubscribeDeviceInformation`, `UnsubscribeDeviceInformation`, `ActivateDevice`, `DeactivateDevice`. The PDF's generic Common `SubscribeRequestStructure`, `SubscribeResponseStructure`, `UnsubscribeRequestStructure`, `UnsubscribeResponseStructure` and `DataAcceptedResponseStructure` are **intentional reusable datatype structures**, not missing DMS-specific types. The mismatch is contextual and defect attribution remains **undetermined**; never generate an alias or fail providers merely because a wrapper is absent from V2.0.

## Full version-boundary check

| Version / role | Document evidence | Exact selected XSD/provenance | Conclusion |
| --- | --- | --- | --- |
| V1.0 earlier predecessor, non-affected for this exact predicate | Official German VDV 301-2 V1.0 (`VDV301-2_V1.0_DE`, SHA-256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`), historical Table 6, pp55-56; English publication separately exists | `IBIS-IP_DeviceManagementService_V1.0.xsd` blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4`, includes Common/Enumerations V1.0; **no DeviceManagementServiceGroup** | Generic shared Common modelling predates V2.0, but the precise *local service group inventory* comparison is inapplicable in V1.0. Do not backdate DMS-001 as a claim about that group. |
| V2.0 first/last affected | Official `VDV301-2_BASE_V2.0`, SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, printed p90 actual body §7.1.1 and Table 11; p95 generic response context, prior pinned visual run `33758274931` artifact `9894357560` | Official upstream `VDVde/VDV301` tag `VDV-301-2.0`: DMS XSD blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`; Common V2.0 blob `8608e3dcd665c197c34da7f6ec6af5a3758da164` | Local DMS group has 10 elements and is not equivalent to the PDF operation inventory. The reusable Common datatypes are intentional. |
| V2.1 first non-affected successor | Official bilingual `VDV301-2_BASE_V2.1`, SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, **actual visible body** printed pp91–94, section 7.1.1, **Tabelle 11**; all four pages inspected from pinned-byte visual render | Exact official upstream tag `VDV-301-2.1`: DMS blob `191b43e01cdaba14b247725689a913c244a67eed`, Common V2.1 blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, Enums V2.1 blob `311464690ad60749ed8d326217787e4b8ed0b718` | The group has **84 elements: Request + Response for each of the 42 PDF Table 11 operations** (all 42 names matched; zero unpaired or missing wrappers). PDF still deliberately references generic Common subscription/acknowledgement structures *as data types*. |
| V2.2 subsequent | Official `DMS_V2.2`, SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`; separately published DMS operation tables | Official V2.2 DMS blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d` | Service-prefixed subscription request/response group declarations persist. DMS operation family differs from V2.1: do not assume every historical operation is still in scope. |
| V2.3 comparison, **not official** | No separately pinned V2.3 DMS PDF in canonical official source registry | `IBIS-IP_DeviceManagementService_V2.3.xsd` integration blob `5fe444cf6d10462cc23fd159eb963abbec42248f` | Integration comparison has prefixed subscription wrappers. Cannot promote this to released authority. |
| V2.4 subsequent | Official `DMS_V2.4` PDF SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd` | Candidate/integration `IBIS-IP_DeviceManagementService_V2.4.xsd` blob `d222dfd98b2be3777576388da7ace8f333d24c3f` | Service-prefixed operation group entries persist; candidate XSD must not be relabelled official. |

## Reproducible GitHub byte-pinned visual fallback: V2.1 Table 11

Source: `VDV301-2_BASE_V2.1`, official URL `https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx`. GitHub workflow: `.github/workflows/pdf-render-fallback.yml`, run **37894085576** (SUCCESS), artifact **11598819821** (`vdv-pdf-render-fallback`, artifact digest `sha256:27773475d236cdd36e47407bfb1f902daadc95a383d0896804a1e82f513b78ae`). `tools/render_vdv_pdf_pages.py` verified original bytes **SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, size 2,671,005 bytes, 130 PDF pages** before rendering. Exact PDF page index = printed page for target pages; render 160 dpi; original images actually inspected, not text-only.

| Printed/PDF page | Actual visible content in table 11 | PNG SHA-256 |
| --- | --- | --- |
| 91 | Get/Subscribe/Unsubscribe device information/configuration/status; generic Common structures | `eeeabf30bf02357a092cf554eda221cb95410590f1ee21e47a2f250332e282a9` |
| 92 | Device error messages, Restart/Deactivate/ActivateDevice, service information/status, StartService | `a3f04e213de4f7f55c6392bb4acf62e324f1f4f9b6be01c95f32fc3a3a7affaf` |
| 93 | Stop/RestartService, subdevices and status/error subscriptions | `ede823a0c9bf330539e09efa94b0c9b9caf9c9e09b32179202f63a8a29de8150` |
| 94 | Subdevice error unsubscribe and five update operations; actual body caption **Tabelle 11** and §7.1.2 | `9d7b5571430397bc933daa9e9aa8f60571f303277f4f0061410102727d7d07b7` |

The comparison used all 42 operation names in the visible table; selected V2.1 XSD group contains exactly the corresponding `DeviceManagementService.{Operation}Request` and `...Response` entries, with generic Common *types* for Subscribe/Unsubscribe/DataAccepted where appropriate. Do not confuse the PDF's named *structure type* with the XSD operation *element name*.

## SDK / provider consequences

- Keep `DMS-001` one identity, affected `V2.0` only; `normative_authority=contextual_only`, `defect_assessment=undetermined`, `sdk_behavior=info`, `runtime_match=not_applicable`.
- Exact historical XSD including typos remains XML validation authority; no modification, alias, normalization or additional provider FAIL.
- The operation-context resolver must understand generic shared Common structures and version-exact service wrappers. Do not derive service support only from the local DMS group.
- No remediation/PR action. No extra completion credit for the earlier probe; this terminal boundary verification adds exactly one count to the 70-entry boundary backlog.
- The previous `VERSION_SCOPE_BOUNDARY_PROBE_DMS_001_2026-10-09.md` remains historical incomplete evidence; its cache-miss blocker is **resolved by this report**, not an active remaining limitation.

## Closure protocol

This report is the final evidence record, conditional on successful full schema/audit validation and terminal handoff check of the final canonical HEAD. Next boundary candidate: `DMS-002`.
