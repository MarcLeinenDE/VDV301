# DMS-001 — version-scope boundary probe (2026-10-09)

**State: EVIDENCE IN PROGRESS — not boundary-verified; NO progress credit.**

This note is an additive probe, not a terminal boundary review or semantic/SDK reclassification. It records independently observed predecessor/successor evidence and the remaining mandatory visible-body check. Existing canonical scope remains **V2.0 only**, and existing `contextual_only`, `defect_assessment=undetermined`, `sdk_behavior=info`, `runtime_match=not_applicable` remain unchanged.

## Identity and issue definition

`DMS-001` concerns the historical discrepancy between a **public DMS operation inventory** and the **local service-specific XML modelling in `DeviceManagementServiceGroup`**. This must not be interpreted as proof that generic Subscribe/Unsubscribe or DataAccepted Common types are missing; Common modelling is intentional. The special feature of the V2.0 XSD is omission of DMS-prefixed operation request/response declarations from that local group (including Subscribe/Unsubscribe and ActivateDevice/DeactivateDevice) even though the publication names the operations.

## Independently examined versions

| Lane | PDF/publication | Selected service XSD Git blob | Observation and scope relevance |
| --- | --- | --- | --- |
| V1.0 predecessor | German `VDV301-2_V1.0_DE`; SHA-256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`; visible printed pp55–56, Table 6 | `IBIS-IP_DeviceManagementService_V1.0.xsd` blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4` | The PDF already uses generic Common Subscribe/Unsubscribe and DataAccepted types. However V1.0 service XSD **has no DeviceManagementServiceGroup at all**, so the precise V2.0 *group inventory* defect predicate cannot simply be backdated to V1.0. Different modelling era; related context, not automatically affected scope. |
| V2.0 | `VDV301-2_BASE_V2.0`, SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`; previously byte-pinned visible-body verified printed pp90–92, Table 11 (run `33758274931`, artifact `9894357560` for pp90 and 95) | `IBIS-IP_DeviceManagementService_V2.0.xsd` blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`; Common V2.0 blob `8608e3dcd665c197c34da7f6ec6af5a3758da164` | Public operations use generic Common types; DMS V2.0 group consists of **10 local elements** and omits DMS-prefixed Subscribe/Unsubscribe and Activate/Deactivate wrappers. This is the historically recorded contextual asymmetry, **not an executable XSD validation defect**. |
| V2.1 possible first nonaffected successor | `VDV301-2_BASE_V2.1`, SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`; native PDF text, printed pp91–94, Table 11 | `IBIS-IP_DeviceManagementService_V2.1.xsd` blob `191b43e01cdaba14b247725689a913c244a67eed` | The XML `DeviceManagementServiceGroup` now contains **84 local request/response elements**, including `DeviceManagementService.SubscribeDeviceInformationRequest/Response`, `UnsubscribeDeviceInformationRequest/Response`, `ActivateDeviceRequest/Response` and `DeactivateDeviceRequest/Response`. PDF text continues to reference generic Common operation payload structures. **The new wrappers do not abolish shared Common structure semantics.** Exact-byte visible PDF body pp91–94 must still be rechecked before claiming verified first-corrected boundary. |
| V2.2 official | `DMS_V2.2`, SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`; native PDF text printed pp14 onward | `IBIS-IP_DeviceManagementService_V2.2.xsd` blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d` | Selected XSD has explicit DMS-prefixed Subscribe/Unsubscribe request/response elements in group. Service operations changed compared with V2.1; do not blindly compare a removed operation across release families. |
| V2.3 integration comparison | No separately pinned DMS V2.3 official PDF in source registry | `IBIS-IP_DeviceManagementService_V2.3.xsd` blob `5fe444cf6d10462cc23fd159eb963abbec42248f` | Candidate/integration comparison only; it has explicit DMS-prefixed subscription wrappers, **not** a later official corrective authority. |
| V2.4 candidate/integration | `DMS_V2.4`, SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`; published PDF printed p13 visibly checked | `IBIS-IP_DeviceManagementService_V2.4.xsd` blob `d222dfd98b2be3777576388da7ace8f333d24c3f` | Group continues to model subscription request/response wrappers. Candidate/integration XSD is **not** promoted to official authority. Visible operation table in official PDF uses Common structures. |

## Active disproof and guardrails

- **Disproof checked:** “Every public operation must carry its own DMS-prefixed data *type*.” False: the published tables explicitly reference generic Common subscription/acknowledgement types; V2.1+ local operation *elements* may legitimately reuse those same generic structures.
- **Disproof checked:** “The same V2.0 group mismatch starts in V1.0.” Unsupported: V1.0 has no `DeviceManagementServiceGroup`; the grouping predicate has no equivalent there, even though the generic Common modelling already exists.
- **Disproof still open:** Is V2.1 the exact first nonaffected release in *visible-body* terms, and are all material DMS operations in the V2.1 inventory represented by the appropriate operation wrappers? Text extraction indicates yes for the representative named operations; do not overstate as a complete body-verified inventory comparison.
- No schema modification, aliases, provider FAIL, SDK runtime matcher, remediation recommendation or finding identity change follows from this probe.

## Blocker, required resume operation

Interactive screenshot of V2.1 PDF at physical pages 90 and 91 failed with a **cache miss** on 2026-10-09; retry also failed. Mandatory deterministic fallback was attempted but official source download in this execution environment failed (external DNS/network unreachable), so the pinned V2.1 PDF could not be passed to `tools/render_vdv_pdf_pages.py`. This is a **source-access / visual-verification blocker**, not a contradiction established by the PDF.

To close: obtain the exact `VDV301-2_BASE_V2.1` byte-pinned PDF (verify `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` and size 2671005), render/check the **actual body** of Table 11 on printed pp91–94, compare all operations to the V2.1 group, and re-evaluate V1.0 absence of group. Verify official tag/ref/blob provenance again. Only then finalize `DMS-001` with boundary registry, semantically justified scope, source locators and any necessary SDK changes; run the full gate and terminal handoff. Do not start `DMS-002` before independent terminal closure.

**No boundary registry counts or canonical semantic/locator/runtime scope were changed by this probe.**
