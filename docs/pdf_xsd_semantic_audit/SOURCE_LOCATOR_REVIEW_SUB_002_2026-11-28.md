# SUB-002 source locator and version boundary review — 2026-11-28

Status: evidence complete; full schema/handoff gate pending at substantive commit. Terminal closure is recorded by CURRENT_STATE only after successful gates.

## Findings and scope

SUB-002 remains confirmed non_defect, intentional_design_misread, selected_xsd, no_runtime_diagnostic, runtime_match not_applicable. Earliest verified EN V1.0 and independent DE V1.0; sparse groups through Base V2.0/V2.1, explicit DMS contrast from V2.1, retained in V2.2 and candidate/integration V2.3/V2.4. Distinct SMS V2.2 functional successor confirms sparse group pattern. Official V2.4 PDF distinct from candidate XSD. No earlier or later comparable release in pinned catalog; no defect correction boundary because this is contextual design, not defect. No endpoint, HTTP acknowledgement, mandatory provider availability or production-root alias inference.

| Publication/authority | Visible body and scope | XSD inventory |
| --- | --- | --- |
| VDV 301-2 V1.0 English (01/2014) (official_release) | 87 9.9.1 Operations of SystemDocumentationService; Table 102; 89, 90 9.10.1 Operations of SystemManagementService; Table 110: Description of Operations at the SystemManagementService; 62, 63, 64 9.3.1 Operations of DeviceManagementService; Table 30: Description of Operationen des DeviceManagementService | Original service files lack local groups; aggregate contains sparse 5/2/10-member groups and generic global subscription roots. Published operations explicitly include subscriptions. Not an XSD defect. |
| VDV 301-2 V1.0 German (07/2016) (official_release) | 64 7.2.1 Operationen SystemDocumentationService; Tabelle 23; 67 7.3.1 Operationen SystemManagementService; Tabelle 31; 55, 56 Visible DeviceManagementService operations table continuation; caption on p56; Tabelle 6 Beschreibung von Operationen des DeviceManagementService | Original service files lack local groups; aggregate contains sparse 5/2/10-member groups and generic global subscription roots. Published operations explicitly include subscriptions. Not an XSD defect. |
| VDV 301-2 Basic Services V2.0 (official_release) | 99 7.2.1 Operationen SystemDocumentationService; Table 28: Description of Operations at the SystemDocumentationService; 103 7.3.1 Operationen SystemManagementService; Table 36: Description of Operations at the SystemManagementService; 89, 90, 91, 92 7.1.1 Operationen des DeviceManagementService / Operations of DeviceManagementService; Tabelle 11 Beschreibung von Operationen des DeviceManagementService / Description of Operationen des DeviceManagementService | SDS and SystemManagement remain sparse (5/2); DMS V2.0 has 10 members including 0 subscription members. Same-file SystemManagement revision 2d32630... is exact in this release, not original V1.0 85390f9.... |
| VDV 301-2 Basic Services V2.1 (official_release) | 112 7.2.1 Operationen SystemDocumentationService; Table 53: Description of Operations at the SystemDocumentationService; 116 7.3.1 Operationen SystemManagementService; Table 61: Description of Operations at the SystemManagementService; 90, 91, 92, 93, 94 7.1.1 Operationen des DeviceManagementService / Operations of DeviceManagementService; Tabelle 11 Beschreibung von Operationen des DeviceManagementService / Description of Operationen des DeviceManagementService | SDS and SystemManagement remain sparse (5/2); DMS V2.1 has 84 members including 40 subscription members. Same-file SystemManagement revision 2d32630... is exact in this release, not original V1.0 85390f9.... |
| DMS V2.2 official (official_release) | 14, 15, 16 2 Operations of DeviceManagementService; Tabelle/Table 1 Beschreibung von Operationen des DeviceManagementService / Description of Operationen des DeviceManagementService | V2.2 official DMS changes operation inventory but retains explicit generic subscription group members (68 total/36 subscription). No universal operation support inference. |
| SystemMonitoringService V2.2 functional successor (official_release) | 9 2 Operations of the SystemMonitoringService / 2.1 Operationen SystemMonitoringService; Tabelle 1 Beschreibung von Operationen des SystemMonitoringService / Description of Operations at the SystemMonitoringService; 12 3 Versionshistorie / Version History / 3.1 Version 2.2 / 3.1.1 Funktionale Erweiterungen / Functional Upgrade; history | Distinct identity; sparse two Get-response members coexist with four documented generic subscription operations. History explicitly states extraction and that predecessor SystemManagement/SystemDocumentation no longer required for configuration; not proof of universal prohibition. Earlier SMS-001–004 findings unchanged. |
| DMS V2.3 integration comparison (candidate_integration) | No separate verified PDF | No independently established official DMS V2.3 PDF or release-tag service XSD; work-branch comparison only (68/36). |
| DMS V2.4 official PDF (documentation_only) | 13, 14, 15 2 Operations of DeviceManagementService; Tabelle/Table 1 Beschreibung von Operationen des DeviceManagementService / Description of Operationen des DeviceManagementService | Official published V2.4 table retains nine generic subscription families and optional control notes; not official V2.4 schema authority. |
| DMS V2.4 candidate/integration comparison (candidate_integration) | No separate verified PDF | Exact selectable candidate/integration schema (68/36); not an official release; no later comparable publication in pinned catalog. |

## Evidence and disproof

- Historical EV-157 34487918692 job 102906852658 PASS; original archives 10156457016/10155848626 unavailable; checker preserved. Permanent regression full gate 46120977971 SUCCESS, handoff 46120978579 SUCCESS, artifact 15253417163 SHA256 56ee7866dfe478e193dd4de869501381ce5079a0ffd3c4e90d1ab320464abb8d; eight service compilations + static aggregate inventory; expanded regression to be verified by full gate.
- Exact V1.0 EN/DE, Base V2.0/V2.1 pinned render archives and page hashes recorded in interim and final reports; six ZIPs verified, nine SDS/SystemManagement pages visually inspected. New DMS comparison: V1.0 EN pp62–64 Table 30; DE pp55–56 Table 6; Base2.0 pp89–92 Table 11; Base2.1 pp90–94 Table 11. All actually viewed.
- DMS V2.2 run 46121065904 artifact 15253357429 ZIP SHA256 433e894d8b472b55af0f508c3c9704ffac8600afac6f5530e03d8c5e179f6f49; p14 6fdf988a18c58934a978e1939f86c6d70237501d37e99fdb63e7448962b25d06, p15 1f7ae1ef5f20ac89dc5b937ba0f36f91aa8cd3e11981bff4647981ca80b3fac4, p16 24c4f47483f7fe52fb8c01c39954e0815f6cb78ee71726f02ec064c2f8694e01; ZIP and all PNG hashes/bytes verified, visually inspected.
- DMS V2.4 run 46121074759 artifact 15254220265 ZIP SHA256 a4ba6ee1bf30e01a24d27cbe6af1cae4002be90a5855424295e2b00e017aabb9; p13 6147837e494d3f8adc70676a0352f43a44b8e7e0ff4b28b650028242b2e564da, p14 3a3415df763be21c689781819b5b5a459367bf0939efcb3965c3a244b3d8c0f4, p15 594621f21afa436407dfc9b84898057334fb1c566b8ae8dab007630185848a6e; ZIP and all PNG hashes/bytes verified, visually inspected.
- SMS functional successor: EV-146 artifact 9987318510 ZIP SHA256 181ff01b16dae43ec2826299e6f14717aef1668d66491b6051ae07661ee607f6; all six PNG hashes and byte counts checked; p9 6f813ae55fd3acc28e99f055978c504b9759e03b1cfb52a133adaf696a2f3b79 and p12 41515d4afc0455e0628128f47eecba3d88364858882c5551b2616af72528addf visually checked. Pinned prior PDF bytes, no new raw acquisition. Official tags 2.2/2.3 contain same SMS V2.2 blob, no SDS or SystemManagement historical file at tested paths; history confirms functional transition. SMS-001 and SMS-004 remain distinct.
- Exact original SystemManagement V1.0 85390f99... vs later 2d32630...; official aggregate 41289eae... has 5/2/10 sparse groups and generic roots. Worktree V1.0 service files cannot substitute for exact historical aggregate. No new production root/HTTP support assertion. No XSD or resolver remediation; separate historical route consideration for future capability matrix.
- Four intermediate handoff failures from too-short pending_block repaired 017b2793, handoff 46120764702 SUCCESS; subsequent handoff gates SUCCESS. No history rewrite.
- tools/validate_sub_002_service_group_inventory.py

DMS early PDF lists six subscription families even without explicit service-qualified entries. DMS V2.1 explicitly models ten families (40 group entries); later V2.2/V2.4 nine families (36 entries), retaining GetDeviceConfiguration without subscription. Later explicit style is not proof of mandatory implementation: optional operation footnote on V2.2 p16 / V2.4 p15 provides counterexample. Original aggregate supplies groups separately from types; no invented roots. The official V1.0 SystemManagement service file is not the later same-filename blob. Historical root routing is documented by upstream tag/aggregate, not modified here. SDS/SystemManagement files absent at tested official 2.2/2.3 paths; historical lineage ends in Base2.1 for those identities; V2.2 SystemMonitoring is distinct functional successor. No unsupported-operation inference based on group membership. No runtime matcher or normative XML outcome changes.

The expanded regression compiles 11 exact service schemas (8 previously verified plus SMS V2.2 and DMS V2.3 integration/V2.4 candidate), checks the official historical aggregate inventory statically, and preserves EV-157. Final gate evidence to be recorded in terminal state.

## Page hash detail for DMS early controls

- EN1.0 p62 5b6562662aca46a49d1445949e53dcff1c16b0caa3af1855360aa22399388fb0; p63 5307fc23ded7f6a748dfa1e45a0266ce073ac8950ff4a3c2935b2cd20b8afa10; p64 15340364b3cd739d266d24fc3ab7f70b91021cd8bae1a0d6d689fb3726a2e578.
- DE1.0 p55 506b04b236373bdc25d0545af6b722514fbd6656c9378d9e8204e8da4d7bc4f9; p56 be3dacf306d0d359197be755d71171032dd719786912fc833db06bc389a96906.
- Base2.0 p89 bf76b9291fd0dd2ccd6ac6d5fb51f7098557ded9634e90ad2b3168c00e0b5521; p90 042fb374f27bd754f6e55e12bd884e138fc7675c4811c218b3f36993798a3999; p91 40cd45e4270121d489f4d26cbbe6e56a8572f8bd089d7541dee90aea229a0d50; p92 05ed33fbde5e167ea5e480b3ac9d8a89594ecb50ba51bc4205452566cdd8e2ba.
- Base2.1 p90 21fb46298ea5d1448456039ddcf70f567b94b42b64713757ca329472d5455f10; p91 eeeabf30bf02357a092cf554eda221cb95410590f1ee21e47a2f250332e282a9; p92 a3f04e213de4f7f55c6392bb4acf62e324f1f4f9b6be01c95f32fc3a3a7affaf; p93 ede823a0c9bf330539e09efa94b0c9b9caf9c9e09b32179202f63a8a29de8150; p94 9d7b5571430397bc933daa9e9aa8f60571f303277f4f0061410102727d7d07b7.

## Earlier interim report (preserved)

# SUB-002 interim original-source and group inventory review — 2026-11-28

Status: **gate_pending**, not a completed source locator or version boundary. Canonical progress remains 145/192.

## Historical EV-157 recovery and visible originals

Original EV-157 acquisition/evidence artifacts 10155848626 and 10156457016 still return 404. Job 102906852658 of run 34487918692 is readable and records PASS; original checker is retained unchanged.

Six render archives were downloaded; their ZIP digests and each contained PNG size/SHA256 were locally matched to manifests, with pinned source SHA256/size checked against the registry. New render runs:
- EN V1.0 46120688791 / artifact 15253203672, pages 62–64,87,89–90, ZIP SHA256 4eb9dd79ad84afc552ea62a5ffcacacd6a4f63881fb8794ef0ea5c86d53ef02a.
- DE V1.0 46120695397 / artifact 15253308120, pages 55–56,64,67, ZIP SHA256 2ebab12fc8afa36d1137b93d979bc8d3d314f966040f650c68b28d1fbe6ed108.
- Base V2.0 46120702726 / artifact 15252969983, pages 89–92,103, ZIP SHA256 561131706228df7b391851567c4e84a40007f0071844c78c087b6a2180ba26ef.
- Base V2.1 46120709891 / artifact 15253576492, pages 90–94,116, ZIP SHA256 581691b705cb844c33479c3d01f2555e320844804083fe02244dfb70ddb9c4f7.
- Reused SUB-001 Base V2.0 46088141460 / artifact 15239797181, p99, ZIP SHA256 53f5ef11b1b5e60a08d568d3764f8b934aac2ea20cb9f0198e3568016f5e130e.
- Reused SUB-001 Base V2.1 46088148878 / artifact 15239259853, p112, ZIP SHA256 bf4f18dad27cbc74ea5efa417d74330a2f14acb973856759b28d59e7cf69bac1.

Visually inspected (printed page and physical index agree):
| Edition | SystemDocumentation operations | SystemManagement operations |
| --- | --- | --- |
| EN V1.0 | p87 §9.9.1 Table 102 | p89–90 §9.10.1 Table 110 (split table) |
| DE V1.0 | p64 §7.2.1 Table 23 | p67 §7.3.1 Table 31 |
| Base V2.0 | p99 §7.2.1 Table 28 | p103 §7.3.1 Table 36 |
| Base V2.1 | p112 §7.2.1 Table 53 | p116 §7.3.1 Table 61 |

All eight operation tables explicitly list generic subscription/unsubscription for SystemConfiguration, DeviceStatus and ServiceStatus using the corresponding Common structures. The nine relevant pages were visually inspected. Other DMS pages in the archives have been hash-verified but are not yet all visually reviewed. No callback HTTP acknowledgement, mandatory provider availability or production root inference follows from a group inventory.

## Exact historical schema distinction

The original official tag VDV-301-1.0 SystemManagementService V1.0 file has blob 85390f99d6c19c88923ed9a5fc8a5706137708af and **no local group**. Later tags VDV-301-2.0 and VDV-301-2.1 contain the same filename but blob 2d32630a0f1981e980e6a466e3f6a69136410f24 (the worktree copy), with two Get response members. The original V1.0 aggregate IBIS_IP_V1.0.xsd at blob 41289eaed2674a169fdf77a10a2eff293c76d5c4 supplies the five-member SystemDocumentationServiceGroup and two-member SystemManagementServiceGroup, as well as generic global Subscribe/Unsubscribe roots. Both service groups are sparse. Do not equate aggregate members, service-local declarations and operational capability. The original V1.0 SystemDocumentation and DMS service files also contain no local group. Exact upstream tags confirm those bytes and V2.0 SDS/DMS, V2.1 DMS and V2.2 DMS.

A permanent regression is added to the existing full schema gate, using current exact service profiles and independently fetching the original official SMS and aggregate, verifying exact Git blob identity. It checks eight service schema compilations, exact dependency pins, count and type mapping of local subscription members, plus static historical aggregate evidence. No results claimed until CI succeeds.

## Remaining work

Review DMS comparative table pages visually (V1.0–V2.1) and relevant later DMS editions/authority lanes, establish exact successor boundaries without generalizing a non-defect into a defect. The same-path V1.0 SMS revisions must be explicitly distinguished in source locators, scope and provenance; assess existing legacy-root routing implications without changing historical schema bytes or runtime. Update canonical semantic/locator/body/boundary/provenance stores only when scope is resolved. Keep no_runtime_diagnostic unless new evidence establishes a different SDK consequence. Run required gates and terminal close before memory update.

Four render request commits updated CURRENT_STATE atomically but failed the handoff guard because pending_block was only seven characters (required >=12). Repaired at 017b279333ae838c438c46669b2b861e24226503; handoff 46120764702 SUCCESS. No history rewrite. Future pending_block must be descriptive, >=12 characters.

## Executed regression result

Commit f7c9c6dcc05ccd48a6119b95496d6aed6e5f1460: full schema gate 46120977971 SUCCESS and handoff 46120978579 SUCCESS. Artifact 15253417163 ZIP SHA256 56ee7866dfe478e193dd4de869501381ce5079a0ffd3c4e90d1ab320464abb8d verified locally. Log sub_002_service_group_inventory.log: eight schema compilations PASS including original V1.0 SystemManagementService, historical aggregate inventory PASS (static only). No XML/SDK mutation. DMS V2.3 integration-only and V2.4 candidate/integration are not official XSD release authorities; existing DMS-003 locator confirms those lanes. V2.2 official DMS schema independently verified against upstream tag. Final scope and locator closure still pending.
