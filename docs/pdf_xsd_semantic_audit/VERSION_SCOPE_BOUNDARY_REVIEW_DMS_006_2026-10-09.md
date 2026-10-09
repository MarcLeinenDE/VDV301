# DMS-006 — verified version boundaries for DeviceStatusImpact/DeviceStatusPriority (2026-10-09)

**Confirmed official V2.2 PDF defect; material correction of affected scope.** The official V2.4 publication and corresponding candidate/integration XSD are a **non-affected correction boundary**, not an affected documentation-error lane. Only **V2.2 official** remains in the semantic/runtime *affected* scope. No XSD bytes were changed.

## Full independent predecessor / successor verification

| Version | Publication vs selected XSD (exact authority) | Finding scope |
| --- | --- | --- |
| V1.0 German and English | Official DMS V1.0 schema `IBIS-IP_DeviceManagementService_V1.0.xsd` blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4` has no `DeviceStatusStructure` | Not yet applicable; no invented prior defect |
| V2.0 | Official DMS V2.0 XSD blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a` has no `DeviceStatusStructure` | Not yet applicable |
| **V2.1 first status-structure publication, last nonaffected predecessor** | Official bilingual `VDV301-2_BASE_V2.1` PDF SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` **printed page 105, actual visible Table 34** explicitly lists only `DeviceStatusName 1:1` and `DeviceStatusFlag 1:1`. Official upstream `VDVde/VDV301@VDV-301-2.1` DMS XSD blob `191b43e01cdaba14b247725689a913c244a67eed` defines precisely the two fields. | **No mismatch.** Two-field XML valid. |
| **V2.2 first/last proven affected official release** | `DMS_V2.2` official PDF SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e` **printed p23, actual Table 20** shows only Name/Flag. Official selected `IBIS-IP_DeviceManagementService_V2.2.xsd` blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d` `DeviceStatusStructure` has **four mandatory** sequence members: `DeviceStatusName`, `DeviceStatusFlag`, `DeviceStatusImpact`, `DeviceStatusPriority` (implicit minOccurs=1 for latter two). | **Confirmed PDF/XSD mismatch.** PDF-shaped two-field XML fails selected XSD. |
| V2.3 integration comparison | `IBIS-IP_DeviceManagementService_V2.3.xsd` local blob `5fe444cf6d10462cc23fd159eb963abbec42248f` still requires all four fields; executable test confirms. **No independently pinned official DMS V2.3 PDF** from which to assert documentation mismatch. | XSD-only comparison; **no DMS-006 documentation defect asserted** for V2.3. Not official-release authority. |
| **V2.4 first checked corrected official publication** | Official published `DMS_V2.4` PDF SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd` **printed p23 actual Table 20** documents `DeviceStatusImpact 0:1` and an optional Priority row. Selected **candidate/integration** V2.4 DMS XSD blob `d222dfd98b2be3777576388da7ace8f333d24c3f` has `minOccurs=0` for both. | **Non-affected correction boundary.** The separate V2.4 PDF spelling `eDeviceStatusPriority` remains issue `DRDMS24-002`, not DMS-006 and not a valid alias. |

A separately available V2.3 integration XSD does **not** establish an official public V2.3 DMS PDF or a correction in an official released XSD. Thus the first **verified published** correction is V2.4; exact selectable V2.4 XSD is still candidate/integration.

## Visible-body reproducibility

- **V2.1 new predecessor:** official URL `https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx`; pinned SHA-256 above, PDF byte size **2,671,005**. GitHub Actions deterministic `.github/workflows/pdf-render-fallback.yml` run **37903052606 SUCCESS**, artifact **11603326400**, artifact digest `sha256:ac4949a5bad599df5e133ac3b54869f8037fa17d456aad2df0f7e18a78bb93cb`. Rendered **p105** PNG `VDV301-2_BASE_V2.1_page_0105_160dpi.png`, SHA-256 **`410fef8472cabb9ac343ada24dba932bc0a61dbb2c0378e10472fcab9ad43e23`**, actually inspected: table caption **Table 34**, both names and **1:1** cardinalities visibly present.
- **V2.2 affected:** earlier exact-byte pinned `audit_registry/dms_visual_revalidation_evidence_2026-09-03.json` run **33758274931**, artifact **9894357560**, printed p23 PNG sha256 `caa6a73b3117d766f48630114cc6c13ddcb30f65d42b861c1f6c677ef1c3c5b1`; visible Table 20 includes only Name/Flag.
- **V2.4 corrected:** same earlier pinned run **33758274931**, p23 PNG sha256 `e7e1d76a41e0ba5ed5120f60c437bed28682d9d3edf442be839252500a883a74`; visible Table 20 Impact/Priority optional, with separate misspelled priority label. Original source hashes are in canonical source pin registry.
- These locators follow **visible page bodies**, not TOC/history inference. The official V2.1 PDF is bilingual with English technical table; no fabricated parallel German Table 34 is claimed.

## Executable full version-boundary proof

`tools/validate_dms_instance_boundaries_ev127.py` expanded and run on GitHub Actions **37903327050 SUCCESS**, with exact XSD includes and actual `lxml.XMLSchema` positive/negative documents:

| Selected profile | Two fields (Name+Flag) | All four fields | Exactly one of Impact/Priority missing |
| --- | --- | --- | --- |
| V2.1 official | **PASS** | **FAIL** (unexpected future fields) | Not applicable |
| V2.2 official | **FAIL** | **PASS** | **FAIL** in each targeted omission case |
| V2.3 integration | **FAIL** | **PASS** | **FAIL** in each targeted omission case |
| V2.4 candidate | **PASS** | **PASS** | **PASS** (each optional member tested separately) |

Active disproof: the PDF omission was **not** inherited from an already-incompatible V2.1 schema; predecessor PDF and XSD match. Nor can the issue be extended into V2.4 merely because the two fields remain discussed: V2.4 actually marks them optional and candidate XSD accepts the documented two-field shape. The separate V2.4 `eDeviceStatusPriority` label is another finding, not an authorization to accept misspelled XML.

## Provider / SDK consequence, scope correction

`DMS-006` remains one finding with `defect_assessment=confirmed_pdf_defect`, `normative_authority=selected_xsd`, `sdk_behavior=error_with_advisory`, `runtime_match=reviewed` (not implemented). **Affected semantic + runtime profile scope: official V2.2 only.** V2.1 predecessor, V2.3 integration comparison, V2.4 corrected public PDF/candidate XSD are locator boundary evidence **only**, not provider diagnostic trigger lanes.

Under V2.2 an XML instance with only Name/Flag **must FAIL** exactly selected official XSD. Any optional SDK advisory can explain why following the published PDF produced that failure, but can never override it, patch bytes, create an alias or silently validate with the V2.4 rules.

Boundary count changes **54/70 → 55/70**, **15 pending**, next `DMS-007`. Because V2.4 was incorrectly included in the original affected version scope, this is a **material semantic/runtime scope correction**: stop current package here; close only after full schema-audit-validation SUCCESS and final terminal-clean HEAD handoff-integrity SUCCESS. No XSD remediation is authorized.
