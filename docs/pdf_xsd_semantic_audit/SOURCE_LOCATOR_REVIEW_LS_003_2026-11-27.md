# Source locator review — LS-003

Date: 2026-11-27. Existing non_defect, selected_xsd, no_runtime_diagnostic unchanged.

## Original body and independent version context

LS-003 non_defect: Beacon HTTP GetDataResponse choice (Data / OperationErrorMessage) versus direct UDP Distance, GNSS and Network *.Data roots. Both language publications confirm the transport and structure distinction. The full official VDV-301-1.0 umbrella declares Beacon root at line 123, with identical types in combined LocationService; later standalone schema moves that root without changing payload constraints. Distance/GNSS root and types identical; Network schema byte-identical. Exact selected service/version routing, no generic root/alias, no runtime diagnostic. No XSD or runtime change.

| Service | EN January 2014 | DE July 2016 | Transport and root |
| --- | --- | --- | --- |
| Beacon | pp52–53 §9.1/9.1.1/9.1.2.2 Tables 7–9 | pp7–8 §1.1/1.2/1.3.2 Tables 1–3 | HTTP; BeaconLocationService.GetDataResponse, choice Data or OperationErrorMessage |
| Distance | pp69–70 §9.4 Table 47 | p7 §1.1/1.2 Table 1 | UDP; DistanceLocationService.Data |
| GNSS | p70 §9.5 Table 48 | p7 §1.1/1.2 Table 1 | UDP; GNSSLocationService.Data |
| Network | p84 §9.7 Table 94 | p7 §1.1/1.2 Table 1 | UDP; NetworkLocationService.Data |

Beacon's reliable event delivery is expressly the reason for HTTP in both publications; the remaining three distribute frequently changing values via UDP. Choice marker -1:1 is not negative multiplicity. Distinguish operation response root, response type, and nested DataContent. No general statement that every HTTP service has this exact root or that every UDP service uses an identical root.

## Exact XSD and active disproof

The historical combined file alone contains Beacon types but not the global root. The full original V1.0 release umbrella declares it at line 123, includes the combined schema, and therefore resolves the apparent missing-root hypothesis. The four targeted type bodies compare equal after whitespace normalization; Network bytes unchanged. The later split preserves service-specific payload semantics; do not treat the combined schema alone as a complete Beacon profile or conflate whole-release aggregate acceptance with standalone routing. No change to SUPERBRANCH_V1_0_DEDUP_POLICY.md.

## Executable evidence and SDK impact

Archived EV-153 result contains four own-schema positive results and four specified paired cross-schema rejections (BLS↔DLS and GNSS↔NLS), not an exhaustive cross-matrix. Do not infer a generic Location root, wrapper alias or latest-wins routing. No fresh instance run or historical complete schema compilation. No XSD/runtime change; existing LS-001/002 unaffected.

## Evidence

- EN pinned render run 46001420624 SUCCESS at 6d7d228fc1077785c982dbcc188f7ff6e91af511, artifact 15197719169 ZIP SHA256 412306ca04310ca0278fa9d855c84a5f2bea17542f9058be50be86f096498833 size 1261946; registered EN source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598. All five PNG hashes/sizes verified against manifest and pages visually inspected: p52 a97fb7fb5adf570420a714452d0604c563b1aef8a02ad07e85c417b99430c667 (237441); p53 455980c0eb2779eae91cd8d102350958462ee3cae456df988588ea7b62dff1e7 (240675); p69 0a883b0bec59fb3d3cf1ef13bb49a85b0dc27802d11f3b1c9afa4cb19f3c1c21 (280137); p70 a53bb9ed4e53bd4dcfd5cfeee8859a57841c2efc30dd1aadde57ff66ea2ba161 (313736); p84 b197046c8c22242217f7c5c0b434246e7158fc2363dff399c6eb7404053078b0 (298626). Live screenshot cache miss, deterministic fallback succeeded.
- Historical DE source pin archive 10056787340, run 34228583786, ZIP SHA256 ddbcc1774639c3d57a5cdf8efbc5f213a107f804d303cf11af520f5b1d66fe8e; all 21 manifest entries verified after removing archive path prefix. EV-153 archive 10057222866 ZIP SHA256 914a1b126e8c06145fe0ccc896f4e2a85db5204a7562ad7dada21ad660fecff7, all 25 manifest entries verified. DE original pages visually inspected: BLS p7 40df64802d52da1e3984ba25a3664fc2caef6b8a4eb839029905c8e7c7b7fc07 (208600), p8 698b315983a5c8ee7fa5205c885c9b37b983007650a6f65077063cae8518f709 (207741), DLS p7 5ba0c63b9343c55e108b8741e5ee7eadeb1ae036b97045e335992ca4f195af7d (130087), GNSS p7 400ca6d9488609131a9fcab6ff024b7e8d310d972f48174d96cd7b429e5bce8e (341322), NLS p7 0d2ef56f421381ca4f18b9ff7978bcef9b8c8bc4fafa342d0d702d4061fc53de (268778). BLS/NLS historical pins registered centrally, no new DE raw PDF retrieval.
- EV-153 run 34229647400 SUCCESS on 45eeed958b3f7f1081f19d6858e54a27824c682f, result and four archived positives verified. BLS ac2ce833f26ce88a1662455d2c70b1e2af4058f5d0b957fad3201b0b7c702bf9 own valid, rejected by DLS; DLS eff4890c820958bf6dd7fc6c7c9e81a56153bb20f36b0ce6d327f1a45efcd2f5 own valid, rejected by BLS; GNSS fecf00bc529c4a0cdc60486cd14740525ce9010a95d3c3f3c15d2156889d9f67 own valid, rejected by NLS; NLS a7e2610697fde18aa00c743f589f981809b5277d6ed9ab42f3ab042e070fed6b own valid, rejected by GNSS. Four tested cross-pairs, not exhaustive 12-pair matrix. No fresh instance execution or historical aggregate compilation.
- Exact VDVde/VDV301 VDV-301-1.0 IBIS_IP_V1.0.xsd umbrella blob 41289eaed2674a169fdf77a10a2eff293c76d5c4 line 123 defines Beacon root, line 9 includes combined LocationService blob 2a653ba7d35a6e91b5fd691eb5c606160192ab9e. Combined lines 7/8 define DLS/GNSS roots; Beacon types at lines 42 and 48. All four historical complex types (Beacon response/content, Distance, GNSS) equal standalone definitions after whitespace normalization. Network original standalone identical. Selected BLS 791e2889f2baa4779ab66ae9e77038ff1b4be915; DLS e6fdc418b6ddaba75d3fbe8f048d1c6d70e023b6; GNSS a74a22079af25cdd028a3e519019d9b3326d9971; NLS bd1f83df2dfa83f36666a3ab3df4457242b387e9; Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c; Enum a9bea5bc73003ed91ded8519db06c32c4067831d. Same six blobs on official 2.0, 2.1, 2.2, 2.3 and master; selected branch matches. Complete historical release is not equivalent to a single standalone schema; preserve existing deduplication policy.
- VDV official catalog https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-27 lists four standalone V1.0 German publications and EN aggregate January 2014; no earlier publication, newer standalone version or separate DE 2014 full aggregate / EN 2016 standalone independently established. EN and DE independently show HTTP Beacon and UDP other services. Active disproof of missing historical root resolved by umbrella declaration; no generic root pattern, no new diagnostic. LS-001 spelling conflict remains separate; LS-002 exact hyphen remains separate.

## Closure

135/192 locator/body/boundary entries pending both CI gates. Initial render-request handoff gate 46001420532 failed only on too-short pending_block; corrected by a228f541b1fa812ab97110661f72b58400f548a5, handoff 46001508745 SUCCESS. Next NET-001 only after terminal closure and memory review.
