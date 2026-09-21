# Runtime-mapping review — DoorStateService V2.1 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

Three DoorStateService V2.1 findings were reviewed against the exact official mixed-version schema family.

### DRDOOR21-001 — shortened / misspelled operation references

Decision: `candidate -> reviewed`.

Activation: `informational`.

Only the exact documentation-side names `RetrieveDoorOpenState` and `RetrieveDoorOpereationState` are eligible for an informational explanation. The selected XSD operation identities remain `RetrieveSpecificDoorOpenState` and `RetrieveSpecificDoorOperationState`.

No operation alias is created.

### DRS-002 — wrong RetrieveSpecific error branch

Decision: `candidate -> reviewed`.

Activation: `xsd_invalid_advisory`.

The advisory is eligible only when selected-XSD validation is already **INVALID** because `OperationErrorMessage` is used in a RetrieveSpecific response where the exact XSD declares `ErrorMessage`.

No rewrite or alias is permitted.

### DRS-003 — untyped Get requests / xs:anyType

Decision: `candidate -> reviewed`.

Activation: `xsd_valid_advisory`.

The advisory is eligible only when selected-XSD validation is **VALID** for non-empty `GetDoorOpenStatesRequest` or `GetDoorOperationStatesRequest`. The exact declarations have neither explicit nor inline type and therefore use `xs:anyType` semantics.

The SDK must not synthesize an empty-content request model or reject content accepted by the selected XSD. Existing evidence does not establish whether the permissiveness is intentional design or a modelling defect.

## Mapping inventory after review

```text
reviewed        56
candidate       22
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-111: run **33242337308**, job **99073684198**
- EV-143: successful evidence run **33976777554**, closure **34025259521**
- EV-145: run **34026409256**, closure **34026674927**
- primary runtime-mapping gate **35551467491**: **SUCCESS**

The gate verified:

- exact DoorState V2.1 / Common V1.0 / Enumerations V1.0 blobs;
- preserved EV-111 executable behaviour;
- no shortened/misspelled Retrieve operation aliases in the service group;
- `ErrorMessage` is the exact RetrieveSpecific error choice member;
- the two Get request declarations remain untyped;
- the informational / INVALID / VALID runtime lanes remain distinct;
- all root XSDs remain unchanged.

No executable Known-Issues matcher was added and no XSD was changed.
