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
