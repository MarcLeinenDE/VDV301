# Finding Revalidation — DRTRAINSET21 / TrainSet Services V2.1

Date: 2026-09-06  
Scope: `DRTRAINSET21-001`, `DRTRAINSET21-002`, `DRTRAINSET21-003`  
Evidence: `EV-148`, successful evidence run `34029363792`, job `101475946965`  
Evidence commit: `1f5fcc0245bc5f53c29118f90252f644feef276d`  
Closure run: `34029618883`

## Authority route

Official byte-pinned VDV 301-2-14 TrainSet Services V2.1 PDF (`8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e`, 1,708,401 bytes), original pin run `33226637254`. The current Deep Read is blob `6d5680f438e7e592aaf1d056e39224e7c2a3f2d9`. Exact V2.1 service XSD blobs are TSI `897f373e31b76aa23d8bc206854b042524e4c102`, TSM `add9d1cb37e5759ff7a77855b239108d38373206`, and TSD `c2cdb73fcae265a2e4e0349ac6072e3548e36d8b`.

The XSDs and EV-109 are used as exact-version counter-context only. All three DRTRAINSET21 terminal states are documentation/navigation/name-context findings and do not alter XML validation behaviour. EV-109 and the complete 50-XSD pool were rerun and passed without XSD mutation.

## Visual evidence

EV-148 rendered the exact pinned PDF at 180 DPI. Physical pages 6, 9, 10 and 44 were manually inspected after the successful run and match the stored render hashes in the permanent evidence record.

## DRTRAINSET21-001 — context_verified

German page 9 and English page 10 both point the service-interaction examples to section 9.1. Page 6 identifies 9.1 as the driving-direction re-initialisation subsection and separately identifies section 10 as `Examples`. The counter-hypothesis that 9.1 was intentionally referenced because it itself contains an example-style re-initialisation use case was tested. It does contain such a use case; however, overview item 4 already assigns re-initialisation to sections 7 and 9, while item 5 separately introduces examples of service interaction, and section 10 contains multiple dedicated cross-service example use cases. The 9.1 pointer is therefore retained as a stale/wrong cross-reference.

## DRTRAINSET21-002 — context_verified

Page 44 says the TrainSetInformationService composition operations provide the same information as equally named operations of the `TrainSetDataService`. Exact TrainSetDataService V2.1 exposes TripRef/TripInformation operations and no `TrainSetComposition` operation. The alternate-alias hypothesis is therefore rejected. TrainSetManagementService carries composition context in this V2.1 family; it is recorded only as the likely intended reference, not used to rewrite or synthesize schema operations.

## DRTRAINSET21-003 — context_verified

Page 44 visibly prints `GetTrainSetCompositon`. Exact TrainSetInformationService V2.1 and the publication operation inventory use `Composition`; no `Compositon` declaration or alias exists. The typo is documentation-only and no compatibility alias is created.

## Closure

EV-148 PASS; closure rerun PASS; EV-109 PASS; all 50 root XSDs PASS as repository-regression evidence; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **120/192 terminal, 72 pending**. The first remaining pending finding is `DRTRAINSET22-001`; next block is `DRTRAINSET22` (`TRAINSET_V2.2_DRTRAINSET22`).
