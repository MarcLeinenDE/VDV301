# Finding Revalidation — DRTRAINSET22 / TrainSet Services V2.2

Date: 2026-09-06  
Scope: `DRTRAINSET22-001`, `DRTRAINSET22-002`  
Evidence: `EV-149`, successful evidence run `34029942365`, job `101477508993`  
Evidence commit: `1f15247b85bad29808f086b69b03ea89df30bd85`  
Closure run: `34030216416`

## Authority route

Official byte-pinned VDV 301-2-14 TrainSet Services V2.2 PDF (`c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e`, 1,744,296 bytes), original pin run `33239594518`. The Deep Read is blob `61850045c26fb2a848c4670f1418fdb809ab475c`. Both findings are same-document navigation/cross-reference findings; XSD semantics are not required for their terminal state. The complete 50-XSD pool was rerun only as a repository regression/immutability guard.

## Visual evidence

EV-149 rendered the exact pinned source at 180 DPI. Physical pages 6, 9, 10, 35, 36, 38 and 40 were manually inspected after the successful run and match the permanent evidence-record hashes.

## DRTRAINSET22-001 — context_verified

Pages 9 and 10 visibly point the examples explaining interaction of the different services to section 9.1. Page 6 visibly identifies 9.1 as the driving-direction re-initialisation subsection and section 10 as `Examples`. The strongest counter-hypothesis was retained from the V2.1 review: 9.1 itself does contain an example-style re-initialisation scenario. However, overview item 4 already assigns re-initialisation to sections 7 and 9, while item 5 separately introduces service-interaction examples, and the same publication has a dedicated section 10 containing those examples. The 9.1 pointer is therefore a cross-reference error.

## DRTRAINSET22-002 — context_verified

Page 38 visibly says `UnsubscribeTripRef` uses `TrainSetUnsubscribeRequestStructure` described in section 6.5.1 and, in the next operation, says `RetrieveTripRef (cf. 6.5.1)`. Page 40 visibly repeats the 6.5.1 pointer for the `UnsubscribeTripInformation` request. Same-document positive controls reject a stable/historical-number interpretation: page 35 visibly defines `Specific TrainSetUnsubscribeRequestStructure` at 6.5.2 and page 36 visibly defines `Operation RetrieveTripRef` at 6.5.3. These are stale navigation references, not schema rules.

## Closure

EV-149 PASS; closure rerun PASS; all 50 root XSDs PASS as repository-regression evidence; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **122/192 terminal, 70 pending**. The first remaining pending finding is `DRTVS21-001`; next block is `DRTVS21` (`TVS_V2.1_DRTVS21`).
