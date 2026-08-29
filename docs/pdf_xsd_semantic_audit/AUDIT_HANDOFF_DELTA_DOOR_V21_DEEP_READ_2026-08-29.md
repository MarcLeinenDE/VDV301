# Audit handoff delta - DoorStateService V2.1 Deep Read

Date: 2026-08-29
Canonical branch: `dev/schema-integration`

## Scope completed

`DOOR_V2.1` was processed under the current `FINDING_EVIDENCE_GATE.md` using the official public VDV writing, an exact byte pin, independent exact-XSD authority verification, fresh document reading before reopening legacy DoorState findings, targeted visible review of material pages, active counter-hypothesis checks and executable evidence where XML behavior was material.

Completion state:

```text
textual fresh read: complete
targeted visible review: pages 9-12 complete
exhaustive visual review: no
Deep Read state: needs_visual_review
```

## PDF source authority

```text
source_id: DOOR_V2.1
sha256: 7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8
size: 851513 bytes
pin run: 33241913638
pinned-byte visual render run: 33242075873
```

Interactive screenshots returned cache-miss on material pages, so exact pinned bytes were rendered through the repository fallback and pages 9-12 were visibly inspected.

## Exact XSD authority

Official tag: `VDV-301-2.1`.

```text
IBIS-IP_DoorStateService_V2.1.xsd  abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
IBIS-IP_common_V1.0.xsd            194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
IBIS-IP_Enumerations_V1.0.xsd      a9bea5bc73003ed91ded8519db06c32c4067831d
```

The integration-branch copies checked during this Deep Read match the official tag exactly.

Important routing rule:

```text
DoorState V2.1 intentionally depends on Common V1.0 + Enumerations V1.0.
Do not substitute later Common/Enums versions.
```

A provenance-only correction is recorded in:

```text
docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DOOR_V21_BLOB_PROVENANCE_2026-08-29.md
```

The earlier closure commit had incorrect Git blob IDs for Common/Enumerations metadata; validation itself used the actual branch files and remains unchanged.

## Existing findings revalidated

### DRS-001

PDF operation overview visibly duplicates `SubscribeDoorOpenStates` / `UnsubscribeDoorOpenStates` where the operation-state variants belong. Detailed sections and exact XSD use `SubscribeDoorOperationStates` / `UnsubscribeDoorOperationStates`.

State: `context_verified`.

### DRS-002

PDF RetrieveSpecific response tables use `OperationErrorMessage`; exact XSD uses `ErrorMessage` in both RetrieveSpecific response branches.

EV-111, run `33242337308`, job `99073684198`:

```text
ErrorMessage          -> valid
OperationErrorMessage -> invalid
```

for both RetrieveSpecific open-state and operation-state response types.

State: `executable_confirmed`.

### DRS-003

PDF says the two Get operations have no request structure. Exact XSD local operation-group declarations have no explicit/inline type and therefore use default `xs:anyType` semantics.

EV-111 verifies the exact declarations and demonstrates the declaration-form semantics with an ephemeral non-normative probe:

```text
empty -> valid
arbitrary nested content -> valid
```

Boundary: this does not claim a real global DoorState request root.

State: `executable_declaration_semantics_confirmed`.

### DRS-004

Typos such as `GetDoorOpeationStates` occur only in XSD documentation annotations and do not affect executable identifiers.

State: `context_verified_ok_note`.

## New findings

```text
DRDOOR21-001
PDF table descriptions use RetrieveDoorOpenState / RetrieveDoorOpereationState instead of the actual RetrieveSpecific... operation names.

DRDOOR21-002
RetrieveSpecificDoorOpenState success-row description incorrectly describes door operation state; context and exact type are open-state semantics.
```

Both are documentation-context findings with no direct XML validation effect.

## Rejected observation

Visible `-1:1` rows with `a` / `b` labels are established VDV XML-choice notation. They are not negative cardinalities and no DoorState cardinality finding is opened.

## EV-111 provenance

```text
checker: tools/validate_door_v21_ev111.py
run: 33242337308
job: 99073684198
head tested: 356d1b792730b66a4f5ec3b99b82e6d66185315c
result: PASS
```

The temporary push-trigger workflow was deleted immediately after the evidence run. The reusable checker remains. No XSD changed.

## Files added/updated by the permanent closure

```text
docs/pdf_xsd_semantic_audit/deep_read/DOOR_V2.1.md
audit_registry/deep_read_findings_delta_door_v21_2026-08-29.json
audit_registry/deep_read_registry_delta_door_v21_2026-08-29.json
docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/24j_executable_validation_door_v21.md
docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
audit_registry/finding_revalidation_registry_v0.1.json
00_START_HERE/CURRENT_STATE.json
tools/validate_door_v21_ev111.py
```

## Next natural Deep Read target

```text
TVS_V2.1
VDV 301-2-16 TicketValidationService V2.1
```

Required sequence remains:

```text
1. byte-pin official PDF
2. independently establish exact official XSD/dependency authority
3. Fresh Read before reopening historical TicketValidation findings
4. apply current Evidence Gate and visible pinned-byte review where layout/table context matters
5. executable-confirm material XML behavior where practical
6. close as needs_visual_review unless exhaustive visual closure is actually achieved
```

After all remaining Deep Reads, freeze the complete finding inventory and perform mandatory legacy-finding revalidation. SDK finding knowledge and remediation readiness remain false until that gate is complete.

No PR, comment, merge or official-facing remediation action was performed.
