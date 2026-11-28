# TS-002 — historical TimeService V1.0 provenance mirror locator review

2026-11-28. **Gate pending until full audit and terminal handoff succeed.** Confirmed TS-002 legacy duplicate of DRTIME10-001, same exact bilingual source/p4; one additional archival locator slot, zero new logical defects. Preserve 192 historical IDs; no XSD/SDK runtime change.

## Identity and evidence

The checkpoint [CORRECTION_TS_002_DRTIME10_001_IDENTITY_2026-11-28.md](CORRECTION_TS_002_DRTIME10_001_IDENTITY_2026-11-28.md) established exact-source identity with DRTIME10-001. Both checkpoint gates succeeded (schema 46173828390, handoff 46173828374, HEAD 804140b75c547d8320d2a189472d40fa8dddd5a3); result artifact 15274926624 ZIP SHA256 1c4d820b622de53ba6559bbdda49d5982664aa9a46c50163e5de166d542209aa, ZIP integrity PASS, 24 individual exit-status files 0. No registry credit at checkpoint. Existing [TrainSet identity precedent](IDENTITY_RECONCILIATION_DRTRAINSET21_001_DRTRAINSET22_001_2026-11-24.md) expressly permits a frozen historical provenance slot to be completed without counting a second logical defect; apply exactly that non-destructive approach here. The earlier checkpoint's instruction to withhold locator credit is resolved by this precedent, not a retroactive rewrite of the checkpoint report. Both frozen IDs and original EV147/EV159 reports remain unchanged. Current semantic TS-002 notes mark LEGACY_DUPLICATE_OF_DRTIME10-001; canonical DRTIME10-001 notes link TS-002. Both are no_runtime_diagnostic/not_applicable, no matcher. Same source, same p4, same wrong document number, same English-only scope, same SDK result. Distinct from TS-001, DRTIME10-002, DR3012-006.

## Exact source and scope

- EV159 artifact 10336194085 ZIP SHA256 4d5c36f36c468b92e1a3ca962eb1e76b8670f6460f2ecf667bd1cdc2c2e2d010 rehashed integrity PASS; actual p4 131551B PNG SHA256 1614a270b77c37cd2abb51bbfb84f3626554ff7b60b385c45b3b02ee29d2ac06 rehashed and visually reviewed, identical EV147 render.
- Artifact 10336172299 ZIP SHA256 c24cfc7d8b80652a5caaeafa4d131f31c32fcbe85e45cfb4a6bb5edb2f789c94 rehashed integrity PASS; recovered exact TIME_V1.0 PDF SHA256 d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3 / 515920B / 10 pages; actual p8 local 180dpi Poppler PNG SHA256 e8389e14de78058e4cc73febabf0c984667eebe0c9b0739d2b7f41e9a1ea40ea independently visually inspected entry (5) 301-2-1 Common. No new raw URL acquisition or GitHub renderer p8 claim.
- VDV official catalog accessed 2026-11-28; only dedicated V1.0; DE correct, EN affected; no dedicated predecessor or corrected successor verified. DR3012-006 distinct. Confirmed TS-002 legacy duplicate of DRTIME10-001, same exact bilingual source/p4; one additional archival locator slot, zero new logical defects. Preserve 192 historical IDs; no XSD/SDK runtime change.

Current PDF raw bytes recovered from previously pinned archive; not a new official URL download. Live screenshots cache-missed; exact p4 archived renderer image verified and read, p8 local Poppler additional corroboration. No new XML/vehicle test. No XSD or resolver/SDK implementation changes. Historical source and original reports retained. New gate validates synchronized registries and unchanged runtime behavior.

## Accounting

156→157 of 192 frozen historical locator slots, 157 body/157 boundary verified in registry pending full gate, 35 remaining. Zero new logical issues; 192 is not proven unique root-cause count. Lexical candidate screening surfaced already-reconciled TrainSet mirror; CE-017/CE-026 concern distinct members TSPPoint/BeaconPoint, no new duplicate asserted. Not a comprehensive dedup audit. Following successful terminal handoff, next canonical slot TSD-001.
