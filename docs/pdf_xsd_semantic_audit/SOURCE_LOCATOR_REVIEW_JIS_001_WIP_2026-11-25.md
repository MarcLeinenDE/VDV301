# JIS-001 source locator review — work in progress

Date: 2026-11-25. This is a recoverable evidence checkpoint, not a terminal review. Historical EV-152 classified intentional shared modelling, no runtime diagnostic. Current completed locator counts remain 127/192.

## Verified current evidence

- EV-152 successful run 34113437268, artifact 10015273758. ZIP SHA256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently checked; all seven render hashes match persisted evidence. Actually visually inspected printed pages 9, 12, 13.
- JIS_V1.0 standalone 07/2016 PDF SHA256 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73, 772125 bytes. Original pin artifact 10011459459 run 34103529949, ZIP SHA256 ee5383e391c2c2e79b229a56094f0a77edc96836516dffa464fc710450647a6a; independently checked all 24 manifest entries after removing original archive path prefix. The historical pin-result.json records exact source URL, SHA, size, retrieval time, valid PDF signature; registry_mutated=false. Central pin registered now from original evidence, not a newly downloaded PDF.
- Original printed p9 §1.2 Operationen des JourneyInformationService, overview table begins here (caption not visible on p9; inspect continuation p11 before final table locator): SubscribeAllData, UnsubscribeAllData, SubscribeCurrentBlockRef, UnsubscribeCurrentBlockRef use four generic structures. p12 §§1.4/1.5 and p13 §§1.7/1.8 explicitly delegate to VDV 301-2-1. All three pages visually inspected from EV-152 renders.
- Later selected JIS V1.0 XSD 8c303db5a9c0548d66b90174d9c329d33092ad24 includes Common V1.0 and Enumerations V1.0 (lines 4–5), group lines 7–40 lacks dedicated subscription members. Common V1.0 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c defines four generic types at lines 856, 863, 869, 876; Enum V1.0 a9bea5bc73003ed91ded8519db06c32c4067831d.

## Newly discovered historical distinction, unresolved routing

Exact official upstream tree VDV-301-1.0 has same-named JIS V1.0 blob 1ee4d7aeb15f3269c5335313be9e214bdb519d2e (283 lines; no local service group); VDV-301-2.1, VDV-301-2.2 and master have 8c303db5a9c0548d66b90174d9c329d33092ad24 (350 lines, local service group). Both files read and compared; not byte-identical. The existing legacy root map README lists CIS/DMS/SDS only, not JIS. Do not assume this is an uncovered routing bug until aggregate and inventory checked. Need inspect exact historical aggregate, root/type equivalence and adapter route; do not modify XSD or runtime without authorization.

Official 2016 PDF foreword says standalone edition separated from January 2014 VDV301-2. Public English January 2014 source https://www.vdv.de/301-2ses.pdfx text shows generic types §9.6.1 and delegation §§9.6.3/4, 9.6.6/7. Live screenshot cache miss; original English pinned artifact 11599922558 contains p66–68 only. Requested pinned renderer pages 71–74 to establish visible original body. Exact EN pin e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7, 2403598 bytes. Current catalog https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-25 (cached): only standalone JIS V1.0 listed. Need distinguish historical aggregate publication from standalone scope; independently assess German 2014 predecessor availability (2016 German base is split, not equivalent to 2014 aggregate). No corrected/later standalone edition evidenced.

## Next action

Check pinned-render workflow on this commit, verify ZIP and page hashes, visually inspect printed page/table/section in 2014 EN, inspect p11 caption in already verified JIS artifact, check historical official aggregate and SDK schema route, and check relevant Common source where required. Then finish JIS-001 scope/evidence, update all locator/body/boundary and mirrored counts together, run full gate and terminal handoff. No semantic promotion or new progress yet. Preserve earlier HDS closure.
