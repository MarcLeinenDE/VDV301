# DMS-005 — corrected version boundary for GetDeviceStatusInformation PDF-only identifier (2026-10-09)

**Classification: confirmed PDF documentation identifier defect.** Material version-scope correction: the typo starts in the **official V2.1** publication rather than first appearing in V2.2. Keep this **one finding ID**.

## Proven original-body locations and exact schema evidence

The wrong *PDF response choice branch* is `DeviceManagementService.DeviceStatusInformationResponseData` (without `Get`). The selected schema's actual branch element is `DeviceManagementService.GetDeviceStatusInformationResponseData`. They are not aliases.

| Version | PDF evidence and authority | XSD authority and conclusion |
| --- | --- | --- |
| V1.0 | Distinct German/English official V1.0 originals; this specific response operation does not exist in the V1.0 service XSD | Official `IBIS-IP_DeviceManagementService_V1.0.xsd` blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4`; **predicate not applicable** |
| V2.0 | Official bilingual `VDV301-2_BASE_V2.0` PDF; the selected DMS V2.0 XSD does not declare this response operation | Official V2.0 DMS blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`; **last non-applicable predecessor** |
| **V2.1 — first affected** | Official bilingual `VDV301-2_BASE_V2.1` **SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`**, printed **p104**, actual §7.1.31.2 Response **Table 31**: choice branch *a* explicitly omits `Get`, while its adjacent type column and **Table 32** immediately below print the correct Get-prefixed identifier | Official VDVde/VDV301 tag `VDV-301-2.1`, `IBIS-IP_DeviceManagementService_V2.1.xsd` blob `191b43e01cdaba14b247725689a913c244a67eed`, `DeviceManagementService.GetDeviceStatusInformationResponseStructure` line 172: **Get-prefixed branch only**, no non-Get alias |
| **V2.2 — persists** | Official `DMS_V2.2` **SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`**, printed **p23 Table 17**: non-Get choice branch, adjacent type Get | Official `VDV-301-2.2` DMS XSD blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, line 148 Get-prefixed branch only |
| V2.3 integration-only comparison | **No pinned official V2.3 DMS PDF**. A documentation defect cannot be asserted absent an actual publication; do not invent a V2.3 PDF or promote comparison schema to official | `IBIS-IP_DeviceManagementService_V2.3.xsd` integration blob `5fe444cf6d10462cc23fd159eb963abbec42248f`, line 148 Get-prefixed branch only |
| **V2.4 — still persists in official PDF** | Official `DMS_V2.4` **SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`**, printed **p22 Table 17** non-Get choice branch; adjacent type Get | V2.4 selected **candidate/integration** DMS XSD blob `d222dfd98b2be3777576388da7ace8f333d24c3f`, line 148 Get-prefixed branch only; **candidate XSD not official** |

**No first corrected-successor publication is established through V2.4.** The technical table in the bilingual V2.1 PDF is English-language; no separate German-language copy of Table 31 is asserted. Earlier V2.2/V2.4 exact-byte visual source evidence is preserved and reused under original pinned hashes; the present first-affected correction is newly visually checked.

## Original source render provenance — V2.1

Official URL `https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx`, byte size **2,671,005**, SHA-256 as above. GitHub `.github/workflows/pdf-render-fallback.yml`, **run 37897714010 SUCCESS**, artifact **11600767562** `vdv-pdf-render-fallback`, artifact SHA-256 digest `9a16fafb7a19f4169e1d52ef681ce6584c2c9a0644759f76f13c2204f96aba62`. Original p104 image **actually inspected**, filename `VDV301-2_BASE_V2.1_page_0104_160dpi.png`, PNG SHA-256 **`f38528dd5e1f818280cb38d4a141664146c2ea4280cba40c04e0abd4e78e88df`**; page had **Table 31 and Table 32** with contradictory labels.

The separate previously recorded `audit_registry/dms_visual_revalidation_evidence_2026-09-03.json` pins **run 33758274931 / artifact 9894357560**: V2.2 printed p23 PNG `caa6a73b3117d766f48630114cc6c13ddcb30f65d42b861c1f6c677ef1c3c5b1`; V2.4 printed p22 PNG `97a4a83efd7dda8dc81b4d966ff0cbe217878f9622adb2cf67f4a0b26db4696a`. These were independently visually reviewed under the same exact source pins.

## Positive/negative executable proof and active disproof

Extended `tools/validate_dms_instance_boundaries_ev127.py` with full-valid XML message payloads using each exact schema's local `GetDeviceStatusInformationResponseStructure` choice and its real dependency route. **GitHub run 37897942988 SUCCESS** shows on official V2.1/V2.2, integration V2.3 and candidate V2.4:

- Actual Get-prefixed branch accepted with valid nested TimeStamp/DeviceState.
- Same otherwise-identical XML using PDF-only non-Get spelling rejected.

Active disproof: the non-Get branch is not a legitimate optional alias, not a `choice` syntax issue, not a German-to-English translation artifact, and not a renamed replacement introduced after V2.1. Correct type/reference printed beside erroneous branch in V2.1 PDF; exact official XSD only has Get. No need to alter XSD bytes. V1.0/V2.0 operation absence limits how far back the *specific branch typo* can be asserted.

## SDK/provider implications and handoff

`normative_authority=selected_xsd`, `defect_assessment=confirmed_pdf_defect`, `sdk_behavior=warning`, `runtime_match=reviewed` (not implemented). Runtime affected documentation lane now includes V2.1, V2.2, V2.4 with correct authority classes; V2.3 remains **schema-only integration context, not a proven affected PDF lane**. An XML response with the PDF-only branch is **FAIL** under the chosen XSD, even if a provider copied the publication's label. The optional SDK warning explains why the XML fails; it never overrides the selected-XSD PASS/FAIL. No DMS alias and no PR/remediation changes.

This correction moves boundary count **53/70 → 54/70** with **16 pending**, next `DMS-006`. Material scope correction requires **stop of the current package after this finding**, full schema-audit-validation **SUCCESS**, terminal_clean commit and final handoff-integrity **SUCCESS**.
