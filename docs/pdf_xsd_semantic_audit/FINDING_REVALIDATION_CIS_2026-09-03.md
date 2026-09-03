# CIS legacy finding revalidation — 2026-09-03

Status: **closed under the current Finding Evidence Gate** for `CIS-001..CIS-005`.

Evidence: `EV-125` (Actions run `33744039627`) plus official byte-pinned CIS PDFs from run `33736316368`, job `100587592810`, artifact `9885887536`. The four PDFs total **105 rendered pages**; source and page hashes were verified and the finding-bearing pages were visually inspected.

| Finding | Terminal state | Revalidated conclusion |
|---|---|---|
| CIS-001 | `unresolved` | The old claim “no CIS V1.1 XSD found” is corrected. Official Git history contains an untagged V1.1 working family at `0a5228a…`, but there is no `VDV-301-1.1` release tag and the working CIS V1.1 schema lacks published-PDF fields `SpeakerActive` and `StopInformationActive`. It therefore cannot be promoted to a strict published V1.1 release authority. |
| CIS-002 | `contextual_not_defect` | Subscribe/Unsubscribe are generic Common structures; their absence from the CIS-specific operation group is intentional shared modelling, not a CIS schema defect. |
| CIS-003 | `executable_confirmed` | PDF detail label `GetCurrentConnectionResponse` differs from executable XSD root `CustomerInformationService.GetCurrentConnectionInformationResponse`; EV-125 proves correct root valid / PDF short root invalid on V2.0, V2.2 and V2.3. |
| CIS-004 | `executable_confirmed` | PDF detail label `RetrievePartialStopRequest` differs from executable XSD root `CustomerInformationService.RetrievePartialStopSequenceRequest`; EV-125 proves the root boundary on all three official routes. |
| CIS-005 | `executable_confirmed` | PDF internally types `MyOwnVehicleMode` inconsistently (`NetexMode` vs `PtModesEnumeration`). V2.2/V2.3 XSD use `NetexMode`; EV-125 proves structured NetexMode valid and scalar text invalid. |

## Disproof / context checks

- V1.1 was searched in official Git history rather than inferred from release tags.
- The strongest alternative for CIS-001 — treating the untagged working files as publication authority — fails because no V1.1 release tag exists and the working XSD is materially behind the published PDF.
- CIS-002 was tested against Common generic subscribe/unsubscribe definitions and CIS operation-group scope.
- CIS-003/004 were checked as global-root naming questions, not merely table wording.
- CIS-005 was checked against the shared `VehicleInformationGroup`, not an isolated PDF row.

No XSD correction or mutation is authorized by this revalidation.
