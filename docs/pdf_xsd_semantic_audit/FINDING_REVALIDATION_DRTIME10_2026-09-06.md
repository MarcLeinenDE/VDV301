# Finding Revalidation — DRTIME10 / TimeService V1.0

Date: 2026-09-06  
Scope: `DRTIME10-001`, `DRTIME10-002`, `DRTIME10-003`  
Evidence: `EV-147`, successful evidence run `34028395412`, job `101473376840`  
Evidence commit: `686ce92ede0f1391e04a4260bc7adf98b6ae3103`  
Closure run: `34028583953`

## Authority route

Official byte-pinned VDV 301-2-10 TimeService V1.0 PDF (`d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`, 515920 bytes) on the **PDF/API/prose** authority lane. TimeService has **no XSD semantic authority** in this audit. The complete 50-XSD pool was rerun only as a repository regression and immutability guard.

The original pin derives from run `33196758957`. EV-147 verified that the current official VDV URL still returns exactly the pinned bytes. The current Deep Read is blob `82a88fbd6dae5d22f472bf144770d915fcc902ea`.

## Visual-review closure

The older Deep Read remained `needs_visual_review` because interactive screenshot requests for the foreword and version history returned cache-miss. EV-147 resolved that boundary by rendering the exact pinned PDF at 180 DPI and preserving the PNGs in artifact `9987794844`. Physical PDF pages 4, 6 and 7 were then manually inspected. The old page numbers 3/5/6 were screenshot indices, not one-based physical page numbers.

## DRTIME10-001 — context_verified

Physical page 4 visibly places the German and English forewords together. German correctly says VDV-Schrift 301-2-10 describes TimeService; English visibly says VDV 301-2-1 describes TimeService. The equivalent-document-identity counter-hypothesis is rejected by the same-page bilingual comparison and the publication identity itself. Documentation/resolver error only.

## DRTIME10-002 — context_verified

Physical page 6 visibly contains the German statement that cyclic transmission of the current time is not intended. The directly following English TimeService section omits that sentence. This is a bilingual omission, not an English contradiction. The runtime/profile consequence remains conservative: do not infer a generic cyclic UDP time-broadcast service; synchronization remains the SNTP path.

## DRTIME10-003 — context_verified

Physical page 7 visibly prints `define Type for Service-Discovery: _ibisip_udp._udp (cd. 1)`. The extraction-only counter-hypothesis is rejected by the fresh render. No intended replacement for `cd. 1` is invented.

## Historical RV-003 reference

The current Deep Read records an older RV-003 check, including `cyclic_time_broadcast_expected() == False`. No current RV-003 checker or implementation with that name exists on the audited branch, so EV-147 does not pretend otherwise. The relevant invariant was re-derived directly from the pinned TimeService source and remains `false`.

## Closure

EV-147 PASS; closure rerun PASS; all 50 root XSDs PASS as regression-only evidence; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **117/192 terminal, 75 pending**. The first remaining pending finding is `DRTRAINSET21-001`; next block is `DRTRAINSET21` (`TRAINSET_V2.1_DRTRAINSET21`).
