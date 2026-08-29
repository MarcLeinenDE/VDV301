# Deep Read - DOOR_V2.1

Status: `needs_visual_review`

Document:

```text
VDV-Schrift 301-2-15
DoorStateService V2.1
07/2018
source_id: DOOR_V2.1
```

Source pin:

```text
sha256: 7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8
size:   851513 bytes
pin run: 33241913638
```

The native PDF text was fresh-read independently before the historical DoorState first-pass findings were reopened. Interactive screenshots for the material pages returned `cache miss`; the exact byte-pinned source was therefore rendered with the repository fallback. Pinned-byte render run `33242075873` produced pages 9-12, which were actually inspected. Because the visual review was targeted rather than exhaustive, the document remains `needs_visual_review`.

## Exact XSD authority

The selected executable profile is intentionally mixed-version:

```text
DoorStateService V2.1
  -> IBIS-IP_DoorStateService_V2.1.xsd
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

Exact official `VDV-301-2.1` blobs:

```text
IBIS-IP_DoorStateService_V2.1.xsd  abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
IBIS-IP_common_V1.0.xsd            267be9bf692da6781a003cee7db92e2072b71182
IBIS-IP_Enumerations_V1.0.xsd      399205aac6b912032812661176ebab0a9897d3c3
```

The integration-branch copies checked during this Deep Read match the official tag. The V1.0 dependencies are not treated as an error and must not be silently substituted with V2.1 Common/Enumerations.

## VDV choice-notation guard applied

Visible page 12 uses `a` / `b` choice labels together with `-1:1` on the two RetrieveSpecific response alternatives. Under the authoritative VDV Min:Max/Choice convention, the leading minus is an XML-choice marker, not a negative minimum cardinality.

Result:

```text
No cardinality defect is opened for the -1:1 rows.
The visible a/b grouping agrees with the exact XSD xs:choice compositor.
```

This is an explicit rejected-observation record so the earlier choice-notation failure mode cannot recur here.

## Existing findings revalidated under FINDING_EVIDENCE_GATE

### DRS-001 - copied DoorOpenStates subscription names in operation overview

Visible page 9, Table 1 lists the DoorOpenStates family and then `GetDoorOperationStates`, but the two following subscription rows repeat:

```text
SubscribeDoorOpenStates
UnsubscribeDoorOpenStates
```

The detailed DoorOperationStates sections and the exact XSD group instead use:

```text
SubscribeDoorOperationStates
UnsubscribeDoorOperationStates
```

Counter-hypothesis checked: the duplicate names are not a generic/shared operation convention. The PDF itself separates the OpenStates and OperationStates service families, and the executable operation group contains distinct operation-state names.

Result:

```text
DRS-001
state: context_verified
classification: pdf_table_or_documentation_error_candidate
subtype: copy_paste_operation_name
validation impact: none beyond operation-name diagnostics; exact XSD names remain authority
```

### DRS-002 - RetrieveSpecific error branch `OperationErrorMessage` vs `ErrorMessage`

Visible page 12, Tables 9 and 11, presents the error alternative as:

```text
OperationErrorMessage  -1:1  IBIS-IP.string
```

for both RetrieveSpecific response families. The exact DoorState V2.1 XSD instead declares:

```text
DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure
  choice: DoorOpenState | ErrorMessage

DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure
  choice: DoorOperationState | ErrorMessage
```

The Get response structures in the same XSD do use `OperationErrorMessage`, so the Retrieve-specific spelling difference is real rather than an extraction artifact.

EV-111 run `33242337308`, job `99073684198`, executable-confirmed against the exact profile:

```text
RetrieveSpecific open-state response:
  <ErrorMessage>          -> valid
  <OperationErrorMessage> -> invalid

RetrieveSpecific operation-state response:
  <ErrorMessage>          -> valid
  <OperationErrorMessage> -> invalid
```

Counter-hypothesis checked: the PDF row is not merely a generic prose label; it appears in the element/name column of the response-data table and uses the same choice notation as the success element. Conversely, the XSD distinction from the Get responses is explicit.

Result:

```text
DRS-002
state: executable_confirmed
classification: pdf_xsd_element_name_mismatch
likely source issue remains unresolved until later remediation review
validation behavior: exact XSD accepts ErrorMessage and rejects OperationErrorMessage in RetrieveSpecific response branches
sdk eligibility: explanatory diagnostic only; do not normalize either spelling
```

### DRS-003 - Get requests are untyped, not explicitly empty

The PDF states that `GetDoorOpenStates` and `GetDoorOperationStates` have no request structure. The exact XSD operation group declares the request elements without an explicit or inline type:

```xml
<xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>
<xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>
```

Under XML Schema default typing semantics these declarations are `xs:anyType`, which is more permissive than an explicitly empty content model.

EV-111 first parses the exact normative XSD and proves that each local declaration has neither a `type` attribute nor an inline simple/complex type. It then uses a non-normative probe schema that reproduces the exact declaration form at global scope solely to exercise the default type semantics. Both an empty request and a request containing arbitrary unexpected nested child content validate.

Important boundary:

```text
EV-111 does NOT invent or claim a real global DoorState Get request root.
The normative declarations remain local members of DoorStateServiceGroup.
The probe demonstrates the XML Schema semantics of the exact untyped declaration form.
```

Counter-hypothesis checked: an element with no explicit request structure does not automatically mean 'must be empty'. The exact declaration semantics disprove that assumption.

Result:

```text
DRS-003
state: executable_declaration_semantics_confirmed
classification: xsd_more_permissive_request_modelling_candidate
validation behavior: untyped declaration defaults to xs:anyType; arbitrary child content is permitted by the declaration semantics
sdk eligibility: explanatory/model guard; do not silently replace with an invented empty type
```

### DRS-004 - XSD annotation-only spelling residue

The exact official XSD contains annotation text such as:

```text
GetDoorOpeationStates
RetrieveSpecificDoorOperationnState
operationn state
```

The executable element/type names around those annotations are correctly spelled. These strings occur in `xs:documentation` only.

Counter-hypothesis checked: no executable identifier or type reference depends on these spellings.

Result:

```text
DRS-004
state: context_verified_ok_note
classification: xsd_documentation_typo_non_executable
validation impact: none
```

## New Deep Read findings

### DRDOOR21-001 - RetrieveSpecific operation names are shortened/typoed in table descriptions

Visible page 12 contains two operation-description naming defects:

```text
Table 8 request description: RetrieveDoorOpenState
expected surrounding/executable operation: RetrieveSpecificDoorOpenState

Table 10 request description: RetrieveDoorOpereationState
expected surrounding/executable operation: RetrieveSpecificDoorOperationState
```

The second form additionally misspells `Operation` as `Opereation`.

Counter-hypothesis checked: these are not alternate service operation names. The operation headings, operation overview and exact XSD use the `RetrieveSpecific...` forms.

```text
state: context_verified
classification: pdf_operation_name_editorial_error_candidate
validation impact: none; do not synthesize aliases
```

### DRDOOR21-002 - DoorOpenState description copied from operation-state semantics

Visible page 12, Table 9, is the RetrieveSpecificDoorOpenState response table. Its `DoorOpenState` success row describes a current door **operation** state rather than the door open state represented by the element and surrounding section.

Counter-hypothesis checked: the exact response type is `SpecificDoorOpenStateStructure`, containing `OpenState`; the adjacent RetrieveSpecificDoorOperationState section separately models `DoorOperationState`. The wording is therefore not a deliberate shared semantic description.

```text
state: context_verified
classification: pdf_description_copy_paste_error_candidate
validation impact: none
```

## Positive alignments retained

Fresh reading also reconfirmed that:

```text
- GetDoorOpenStates response data uses TimeStamp + 1:* DoorOpenStates and aligns with XSD.
- GetDoorOperationStates response data uses TimeStamp + 1:* DoorOperationStates and aligns with XSD.
- RetrieveSpecific request data uses DoorID and aligns with the exact request structures.
- RetrieveSpecific success branches use the corresponding SpecificDoor* structures.
- Subscribe/Unsubscribe executable structures are the generic Common V1.0 subscription structures selected by the exact service XSD.
```

## Completion state

```text
textual_fresh_read_complete: true
selected critical pages visually inspected from byte-pinned source: yes (9-12)
all pages/figures visually exhausted: no
state: needs_visual_review
```

No XSD was changed. No remediation/PR disposition is implied by these findings.
