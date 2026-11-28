# TKT-002 source locator and service identity review — 2026-11-28

Status: original-source evidence complete; expanded permanent regression and full gate pending at substantive commit creation. Final gate evidence is recorded in CURRENT_STATE.

## Classification and boundary

TKT-002 confirmed non_defect, selected_xsd, contextual intentional_design_misread, no_runtime_diagnostic, runtime_match not_applicable. EN original 01/2014 pp91–92 and standalone DE 07/2016 pp7–8 use TicketingService identity. DE p10 Table6 misleading TicketInformationService.Validation.GetDataRequest heading is separate TKT-004, not executable alias. Both original official V1.0 service/aggregate and later identical official 2.0–2.3 service revisions use TicketingService dot names, no TicketInformationService declarations; no XML namespace prefix or synthetic roots. Existing routing override is filename metadata consumed by profile inventory. Master identical comparison, not release; no later standalone edition established. Historical packaging remains TKT-001, no resolver or runtime implementation change.

| Source | Visible body | Meaning |
| --- | --- | --- |
| EN combined V1.0 (01/2014) | p91 §9.11; pp91–92 §9.11.1 Table 115 | TicketingService public identity and service-qualified structure names |
| DE standalone 301-2-9 V1.0 (07/2016) | p7 §1/1.1; pp7–8 §1.2 Tabelle 1 | TicketingService public identity |
| DE counterexample | p10 §1.8.1 Tabelle 6 | Misleading TicketInformationService.Validation.GetDataRequest label; TKT-004 separate |

## Executable identity and metadata

The seven root/type pairs in TKT-001 remain exact. The original service file has no global roots, the historical aggregate supplies them. The later standalone schema defines them directly. The dot is part of the unqualified XML name, not a namespace separator. The filename mapping in routing_overrides is consumed by the schema profile inventory generator; no actual runtime implementation claim. The actual field TicketInformationRazziaStatus is not an alias. No normalization or invented name. TKT-004 and TKT-009 remain separate.

## Evidence

- Reused TKT-001 source archives 10322336797 (SHA256 df661f9444ab7e26b563b0c748fee583314b19d789b316c6405e45e1fe99589c), 10336185560 (ba5ee246787f58d4cf690421fda683fb1dd072106d5c4e7eb6376c218b717870), both ZIP hashes and integrity rechecked; both raw PDFs exact registered SHA256 96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43, 627099 bytes. Actual archived p7 1e3d45fcbf975045fb0d97948dfc3f7148fc43516b28f604e94d3cc844ec357c (185769), p8 191ea4b3948ea2953b0a345996b7651a3f56d689e37515553572a5f7ad4e3246 (190801), p10 7a1dbb41115b5c7fc910dea754bb20f9b6a525c13073db735b0d69e1494855b4 (235025) matched archive bytes and visually inspected. No new raw PDF acquisition.
- EN fallback run 46122547204 artifact 15254386230 ZIP SHA256 6ff41b34a5eb259ee674e6a321ef2620d3d9f422b673c625f56e3dddbff944e3 rehashed and integrity checked; source manifest pin e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size2403598; p91 5dad76930429c141c66a00d7d2b22d8019e16317f9b0b645f7c99fb815fa68dc (269589), p92 a78ef4241a53ac5818d655d9d694f6466fa4d612b384ceac7487f467e523c4fe (217236), both PNG manifest hashes/size rechecked and actual pages visually inspected.
- Exact upstream tag service blobs rechecked: 1.0 017ca64666e25d757fc0cde1f1be817f06a743fc, 2.0–2.3/master 3fda66d872ab0d1c511247f13e715cf3ad56afe7; original aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4, no TicketInformationService declaration, only filename include. No targetNamespace in either service. Exact dependency pins and release closure verified by TKT-001 predecessor, no additional official standalone edition established. TKT-001 full gate 46122865133 SUCCESS, EV-158 preserved.
- Existing sdk_manifest/routing_overrides_v0.1.json aliases entry public_service_name=TicketingService, schema_filename_token=TicketInformationService, version1.0, kind=legacy_alias; tools/generate_schema_profile_inventory_v0_1.py consumes filename token mapping, tools/validate_sdk_manifest_v0_1.py checks preservation. No claim of historical resolver runtime implementation. Root map has no Ticketing entry; strict historical profile requirement remains TKT-001, not silently remediated.
- Falsification: DE p10 Table6 literally TicketInformationService.Validation.GetDataRequest, surrounding heading ValidateTicket and overview p7 use TicketingService. Distinct TKT-004 remains unaltered. Legitimate TicketInformationRazziaStatus member is not an alias. Seven actual global root/type pairs in original aggregate/later service; no synthesis from filename, dot names are unqualified.
- Permanent regression expansion in tools/validate_tkt_001_release_context.py: retain existing TKT-001 tests; inventory all named declarations in exact original family and selected later dependencies, check routing metadata only, test seven exact roots and corresponding filename-derived aliases with identical payloads in both complete profiles, and explicit exact versus alias xsi:type for all seven. Local later-profile proof confirms all seven canonical roots and filename root aliases reject SCHEMAV_CVC_ELT_1; explicit type alias probe SCHEMAV_CVC_ELT_4_2. Full gate result pending on this substantive commit.

## Regression extension

The existing TKT-001 permanent checker now reuses the already pinned 12-file historical aggregate and later service/2 dependencies. It inspects named declarations, metadata and targetNamespace; uses seven valid payloads per complete profile, then changes only root or explicit xsi:type. Expected counts: 14 canonical root and 14 explicit type positive instances, 14 missing-root and 14 unresolved-type negatives. Original TKT-001 test remains intact; no success claim for the new regression until gate executes. No production XSD, resolver or runtime changes.
