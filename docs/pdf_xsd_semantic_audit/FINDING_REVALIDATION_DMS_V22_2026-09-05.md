# Finding revalidation — DMS V2.2 deep-read findings

Status: **completed** on 2026-09-05 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `DRDMS22-001` … `DRDMS22-004`. The frozen inventory remains exactly **192 entries**. The previously closed legacy `DMS` block (`DMS-001` … `DMS-007`) remains unchanged.

## Authority and evidence

- Byte-pinned official DMS V2.2 PDF: SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`, 1173719 bytes, 36 pages.
- Exact historical DMS V2.2 blob: `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`.
- Exact Common V2.2 blob: `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`.
- Exact Enumerations V2.2 blob: `2a23b512379b18e8f122ac1272cef8229fb86283`.
- Later V2.4 candidate corrections are explanatory history only and are **not** back-applied.
- Preserved **EV-107** was rerun unchanged and passed.
- Current evidence: **EV-141**, closure run **33974702338**; pinned successful evidence run **33974267275**, artifact **9971840037**.
- Initial EV-141 run **33974145598** failed closed because a service-group member was incorrectly tested as a global root; no finding/evidence/registry state was mutated. The corrected gate tests the actual `DeviceManagementServiceGroup` declaration boundary.
- All automatically discovered original pages were rendered and visibly inspected: 7, 19, 23, 24, 26, 28, 29, 30, 32, 33.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DRDMS22-001 | `context_verified` | Table 23 visibly points `DeviceStatusInformation` to table 27, while table 19 and the table index identify `DeviceStatusInformationStructure`; table 27 and the index identify `InstallUpdateRequestStructure`. Documentation cross-reference error only. |
| DRDMS22-002 | `context_verified` | TOC visibly uses 1.33/1.34/1.35; the body visibly uses 2.33/2.34/2.35. Documentation navigation error only. |
| DRDMS22-003 | `executable_confirmed` | PDF enumeration table visibly uses `InstallationSuccessful`; update-history prose visibly uses `InstallationSuccessfull`. Exact V2.2 schema validates only `InstallationSuccessful`; typo form is rejected and is not an alias. |
| DRDMS22-004 | `context_verified` | Section title/schema operation family use plural `GetDeviceErrorMessages`, while request prose visibly says singular `GetDeviceErrorMessage`. Exact service group contains the plural request and no singular alias. |

## Closure

- Frozen legacy terminal count: **100 / 192**
- Frozen legacy pending count: **92 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Existing legacy DMS block mutation: **none**
- Next revalidation block: **DMS**
- Next subblock: **DMS V2.4** (`DRDMS24-001`)
