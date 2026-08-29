# DoorStateService findings register addendum

Status: DoorStateService V2.1 Deep Read completed under the current Finding Evidence Gate. The document remains `needs_visual_review` because the visual review was targeted rather than exhaustive.

Authority rule:

```text
Validation follows the exact selected XSD family.
PDF differences are explanatory findings; they never silently rewrite or normalize XSD behavior.
```

Selected executable route:

```text
DoorStateService V2.1
-> IBIS-IP_DoorStateService_V2.1.xsd
-> IBIS-IP_common_V1.0.xsd
-> IBIS-IP_Enumerations_V1.0.xsd
```

Exact official `VDV-301-2.1` blobs:

```text
DoorStateService  abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
Common V1.0      194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
Enums V1.0       a9bea5bc73003ed91ded8519db06c32c4067831d
```

The checked integration-branch files are byte-identical to this official authority. The V1.0 dependency pool is intentional and must not be replaced by later Common/Enumerations versions.

Visual evidence:

```text
source pin sha256: 7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8
pin run: 33241913638
pinned-byte render run: 33242075873
visible pages reviewed: 9-12
```

Executable evidence:

```text
EV-111
run: 33242337308
job: 99073684198
head tested: 356d1b792730b66a4f5ec3b99b82e6d66185315c
result: PASS
```

## Revalidated existing findings

### DRS-001 - DoorOperationStates subscription names copied incorrectly in PDF operation overview

State: `context_verified`.

Visible page 9 repeats `SubscribeDoorOpenStates` and `UnsubscribeDoorOpenStates` after `GetDoorOperationStates`. The detailed operation-state sections and exact XSD instead use `SubscribeDoorOperationStates` and `UnsubscribeDoorOperationStates`.

Classification:

```text
pdf_table_or_documentation_error_candidate
subtype: copy_paste_operation_name
```

Counter-hypothesis rejected: these are not intentionally shared generic operation names; the PDF and XSD both distinguish the two operation families elsewhere.

Impact:

```text
No XSD change.
Diagnostics must preserve exact XSD operation names and may explain the PDF table error.
Do not synthesize aliases.
```

### DRS-002 - RetrieveSpecific error branch `OperationErrorMessage` PDF vs `ErrorMessage` XSD

State: `executable_confirmed` by EV-111.

Visible page 12, Tables 9 and 11, names the RetrieveSpecific error alternative `OperationErrorMessage`. Exact XSD uses `ErrorMessage` in both RetrieveSpecific response types; its Get response types separately use `OperationErrorMessage`.

EV-111:

```text
RetrieveSpecificDoorOpenStateResponse:
  ErrorMessage          -> valid
  OperationErrorMessage -> invalid

RetrieveSpecificDoorOperationStateResponse:
  ErrorMessage          -> valid
  OperationErrorMessage -> invalid
```

Classification:

```text
pdf_xsd_element_name_mismatch
```

Impact:

```text
Selected XSD remains authority.
Do not normalize OperationErrorMessage to ErrorMessage silently.
A later SDK may explain the discrepancy after final finding-baseline freeze.
No remediation disposition is made during Deep Read.
```

### DRS-003 - Get requests are untyped and therefore permissive

State: `executable_declaration_semantics_confirmed` by EV-111.

The PDF says the two Get operations have no request structure. Exact XSD declares the corresponding local operation-group elements without explicit or inline type:

```xml
<xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>
<xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>
```

This declaration form defaults to `xs:anyType` semantics. EV-111 first verifies the exact local declarations, then uses a non-normative probe that reproduces the exact declaration form solely to exercise XML Schema default-type behavior:

```text
empty request                        -> valid
arbitrary unexpected nested content -> valid
```

Evidence boundary:

```text
The real declarations remain local group members.
EV-111 does not claim or invent real global DoorState request roots.
```

Classification:

```text
xsd_more_permissive_request_modelling_candidate
```

Impact:

```text
Do not silently tighten the XSD to an invented empty type.
Retain exact XSD authority and explain the modelling consequence where relevant.
```

### DRS-004 - XSD documentation-only spelling residue

State: `context_verified_ok_note`.

Examples such as `GetDoorOpeationStates`, `RetrieveSpecificDoorOperationnState` and `operationn state` occur only inside `xs:documentation`; executable identifiers are unaffected.

Classification:

```text
xsd_documentation_typo_non_executable
```

Impact: none on XML validation.

## New DoorState V2.1 Deep Read findings

### DRDOOR21-001 - RetrieveSpecific operation names shortened/typoed in PDF table descriptions

State: `context_verified`.

Visible page 12 contains:

```text
RetrieveDoorOpenState
RetrieveDoorOpereationState
```

where the surrounding headings, operation overview and exact XSD use:

```text
RetrieveSpecificDoorOpenState
RetrieveSpecificDoorOperationState
```

The second PDF form additionally misspells `Operation`.

Classification:

```text
pdf_operation_name_editorial_error_candidate
validation impact: none
```

Do not synthesize the erroneous forms as aliases.

### DRDOOR21-002 - DoorOpenState description copied from operation-state semantics

State: `context_verified`.

In the RetrieveSpecificDoorOpenState response table, the `DoorOpenState` success row describes a current door operation state. Exact type/section context is open-state semantics; a separate operation-state response exists directly beside it.

Classification:

```text
pdf_description_copy_paste_error_candidate
validation impact: none
```

## Explicitly rejected observation

Visible `-1:1` rows on page 12 are accompanied by `a` / `b` choice labels. Under the established VDV notation this denotes XML choice membership, not a negative cardinality.

```text
No DoorState cardinality finding is opened from -1:1.
Exact XSD xs:choice agrees with the visible a/b grouping.
```

## Completion

```text
textual fresh read: complete
targeted visible review: complete for recorded critical pages
exhaustive visual review: no
Deep Read state: needs_visual_review
existing findings revalidated now: DRS-001..DRS-004
new findings: DRDOOR21-001, DRDOOR21-002
```

No XSD was changed. No PR, comment, merge, or official remediation action was initiated.
