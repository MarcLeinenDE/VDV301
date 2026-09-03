# Finding revalidation — Device Management Service (DMS)

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy inventory entries: `DMS-001` … `DMS-007`.  The frozen inventory remains exactly **192 entries** and is not rewritten by this closure.

## Evidence

- Final executable evidence: **EV-127**, workflow run **33762375705**.
- Pre-closure full EV-127 run: **33761193163**, PASS.
- Independent byte-pinned visual render: run **33758274931**, artifact **9894357560**.
- Official PDF identities are rechecked against `audit_registry/pdf_source_pins_v0.1.json`.
- Exact selected DMS service XSD blobs are pinned in `audit_registry/finding_revalidation_registry_v0.1.json`.
- Positive/negative XML instance boundaries are executed by `tools/validate_dms_instance_boundaries_ev127.py`.
- Root XSD pool validation is rerun after EV-127.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DMS-001 | `context_verified` | Historical V2.0 DMS wrapper/service-group asymmetry confirmed. Generic Common subscribe/unsubscribe structures are intentional context and are **not** treated as defects. |
| DMS-002 | `context_verified` | Repeated unresolved Word cross-reference markers are visibly and textually present in V2.0 and absent in checked V2.1 context. |
| DMS-003 | `executable_confirmed` | V2.0–V2.2 `ErrorMessage` lower bound `10` is confirmed with 9=reject, 10/11=accept; V2.4 correction `0:*` is confirmed with 0/1=accept. |
| DMS-004 | `executable_confirmed` | V2.1/V2.2 require UpdateID, UpdateTimestamp and UpdateURL; omission of each is rejected. V2.4 permits the empty optional request as documented. |
| DMS-005 | `context_verified` | The public PDF visibly uses `DeviceManagementService.DeviceStatusInformationResponseData`; the selected XSD uses `DeviceManagementService.GetDeviceStatusInformationResponseData`. This is a documentation identifier mismatch, so no artificial executable label is assigned. |
| DMS-006 | `executable_confirmed` | The V2.2 PDF-visible Name+Flag-only shape is rejected by the selected V2.2 XSD; adding required Impact+Priority is accepted. V2.4 accepts the two-field shape after the later optionality correction. |
| DMS-007 | `context_verified` | PDF prose says `GetUpdateStates`; operation inventory/XSD use `GetUpdateHistory`. No `GetUpdateStates` operation alias is introduced. |

## Post-freeze visual delta

The independent visual review additionally discovered **`DRDMS24-002`**: DMS V2.4 table 20 visibly prints `eDeviceStatusPriority`, whereas the selected candidate/integration XSD declares `DeviceStatusPriority`.  The delta is recorded additively as `context_verified`, has **no validation behavior**, creates no alias, and does not mutate the frozen 192-entry legacy inventory.

## Closure

- Frozen legacy terminal count: **57 / 192**
- Frozen legacy pending count: **135 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **VDV301-1** (`DR3011-001…003`)
