# TKT-001 source locator and release-context boundary review — 2026-11-28

Status: evidence complete; substantive full schema/handoff gate pending at commit creation. Final state and subsequent gates are recorded in CURRENT_STATE.

## Classification and boundary

TKT-001 confirmed non_defect, selected_xsd, provenance/version_routing_issue, no_runtime_diagnostic, runtime_match not_applicable. Earliest verified official release VDV-301-1.0 uses exact original service blob 017ca646... without global Ticketing roots/group; exact aggregate 41289eae... supplies seven root/type pairs and group. First later official tag 2.0 and persistent official tags 2.1/2.2/2.3 use identical service blob 3fda66d8... and exact V1.0 Common/Enums. Master same but not a release. EN original 01/2014 pp91–92 and standalone DE 07/2016 pp4,7–8 independently substantiate the operation contracts, not specific tag-to-publication alignment. No separate later official Ticketing publication or V2.4 release asserted. Both complete correct packaging profiles compile and validate both instances, isolated original fails due solely to absent global declarations. No defect or correction boundary, no synthetic roots, no runtime mapping or resolver mutation.

| Source | Visible original body | Meaning |
| --- | --- | --- |
| EN combined V1.0 01/2014 | pp91–92 §9.11.1 Table 115; p92 §9.11.2.2 | Original operation contract and shared SetRazzia response |
| DE standalone 301-2-9 V1.0 07/2016 | p4 Vorwort; pp7–8 §1.2 Table 1; p8 §1.3.2 | Extraction from January 2014, same operation contract and shared response |

## Exact root/type inventory

| TicketingService global root | Type |
| --- | --- |
| TicketingService.SetRazziaRequest | TicketingService.SetRazziaRequestStructure |
| TicketingService.GetTariffInformationResponse | TicketingService.GetTariffInformationResponseStructure |
| TicketingService.RetrieveTariffInformationRequest | TicketingService.RetrieveTariffInformationRequestStructure |
| TicketingService.RetrieveTariffInformationResponse | TicketingService.GetTariffInformationResponseStructure |
| TicketingService.ValidateTicketRequest | TicketingService.ValidateTicketRequestStructure |
| TicketingService.ValidateTicketResponse | TicketingService.ValidateTicketResponseStructure |
| TicketingService.GetValidationResult | TicketingService.GetValidationResultResponseStructure |

Original aggregate lines 125–131 and group 132–142 vs later service declaration; original service has neither these globals nor the operation group. The shared Common/Enums V1.0 pins remain unchanged across all verified tags. Historical SetRazziaResponseStructure and SetRazziaResponseDataStructure are not mapped by any global TicketingService root, removed later. Both PDF tracks explicitly specify common DataAcceptedResponseStructure; do not generate a service-specific response root. This is operation contract context, not a general callback acknowledgement obligation.

## Evidence

- EV-158 acquisition run 34771722424 job 103762406542 artifact 10322336797 ZIP SHA256 df661f9444ab7e26b563b0c748fee583314b19d789b316c6405e45e1fe99589c and independent run 34813527845 job 103879396942 artifact 10336185560 ZIP SHA256 ba5ee246787f58d4cf690421fda683fb1dd072106d5c4e7eb6376c218b717870 both downloaded and rehashed, ZIP integrity PASS. Both raw PDFs SHA256 96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43, 627099 bytes, 16 pages. Central TICKETING_V1.0 pin was missing, registered in 9dc8da365110d26120baff3450363cda641a264c; handoff 46122547139 SUCCESS. Historical logs re-read; EV-158 compiled two service files, aggregate only static. No fresh raw DE official download claimed.
- DE original pages visually inspected: p4 rendered locally from recovered byte-pinned PDF, SHA256 c03ab1d0ed8d4d816a0cd128937a349623739622dc1bb21f910389b475294e80; archived p7 1e3d45fcbf975045fb0d97948dfc3f7148fc43516b28f604e94d3cc844ec357c, p8 191ea4b3948ea2953b0a345996b7651a3f56d689e37515553572a5f7ad4e3246. Original raw bytes and historic ZIP identities verified; not falsely labelled fresh acquisition.
- EN original pinned fallback run 46122547204 SUCCESS artifact 15254386230 ZIP SHA256 6ff41b34a5eb259ee674e6a321ef2620d3d9f422b673c625f56e3dddbff944e3; source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598. p91 5dad76930429c141c66a00d7d2b22d8019e16317f9b0b645f7c99fb815fa68dc (269589), p92 a78ef4241a53ac5818d655d9d694f6466fa4d612b384ceac7487f467e523c4fe (217236). Both actual PNGs checked and visually viewed. Live screenshot cache miss for DE; fallback evidence used.
- Exact original official upstream commit f5b53785f703e898632603eec3bfa3555a79fdba tree 729bbe3270e52fed3e0641466048a745d5a09b32 (12 XSDs). Later service and dependencies identical at tags VDV-301-2.0/2.1/2.2/2.3 and master independently checked; master not a release. Official VDV catalog checked, sole 301-2-9 TicketingService V1.0; separate TicketValidationService is distinct, no V2.4 official Ticketing release inferred.
- New permanent regression tools/validate_tkt_001_release_context.py at commit 00bc5b35e6130355d91148a32b868bdb0f9243c0, full schema 46122600264 SUCCESS, handoff 46122600254 SUCCESS. Artifact 15254218098 ZIP SHA256 e9c93b69992e853654dca17d7245450641f2e641962b7d8b2c34ba87364a95e0 downloaded/rehashed; log confirms three compilations, four positive and two targeted missing-global-root negative instances. Exact full historic aggregate including all 12 original files, not integration deduplicated copy. No original XSD mutation, no new runtime diagnostic.
- Falsification: both profiles supply same seven root/type pairs in correct packaging; two valid messages fail only when original service isolated. Two original unused SetRazzia response types removed in later revision, both PDF tracks specify common DataAcceptedResponseStructure, no service-specific response root synthesized. Generic structures/operation labels not conflated with roots. Existing routing override filename token preserved; strict release-context selection is a design requirement, not a claim of implemented historical resolver.

## Reproduction and limits

Permanent regression pins every file of original official 12-file XSD tree at immutable commit, verifies closed include family, compiles both isolated service files and the complete original aggregate. Four positives and two targeted missing-global-root negatives verified. EV-158 historical checker preserved and not rerun with changed prestate. Original isolated file is a valid schema in its original packaging but not the complete operation-validation authority. Same public service/version and filename are insufficient for strict historical selection. Existing resolver routing design preserved, no claim of newly implemented historical routing. No XSD mutation, no new finding IDs, TKT-002..009 remain separate. No live PDF acquisition claim for DE; both archived raw copies and their ZIP identities were rechecked. Only the exact original EN and standalone DE documents in the registered catalog are within this finding's publication scope; no invented later version.
