# TrainSet services findings register addendum

Status: V2.1 and V2.2 Deep Reads completed textually under the mandatory Finding Evidence Gate. V2.1 executable evidence is EV-109; V2.2 revalidation uses EV-104 plus new EV-110. Both documents remain `needs_visual_review` rather than `exhaustive_read` where full-page visual closure is incomplete.

## V2.1 findings

### TSI-001

```text
state: executable-confirmed
classification: xsd_structure_modelling_error_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

Official V2.1 PDF describes multiple coach data sets, while the exact V2.1 XSD models only one flat coach record. EV-109 run `33228250613` accepts one record and rejects a second. V2.2 later corrects the model with repeated `SingleCoach` entries; that correction is explanatory history only and is not back-applied to V2.1.

### TSM-001

```text
state: executable-confirmed
classification: xsd_operation_or_element_name_error_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

V2.1 executable root/group name is `TrainSetManagementService.GetTrainSetComposition`; the later `...GetTrainSetCompositionResponse` form is absent. EV-109 confirms the historical root behaviour. No later-version alias is created for V2.1.

### TSD-001

```text
state: executable-confirmed
classification: service_modelling_or_generic_response_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

V2.1 PDF describes Retrieve/Subscribe/Unsubscribe triples, but exact V2.1 TrainSetDataService contains only the Retrieve roots/group members. EV-109 confirms the service-prefixed subscription modelling gap while also confirming that generic Common subscription infrastructure exists. Do not equate the missing service roots with absence of subscription infrastructure generally.

### DRTRAINSET21-001

```text
state: context-verified
classification: pdf_cross_reference_error_candidate
scope: official V2.1
validation impact: none
```

The V2.1 prose points to section `9.1` for examples located in section 10.

### DRTRAINSET21-002

```text
state: context-verified
classification: pdf_service_name_copy_paste_error_candidate
scope: official V2.1
validation impact: none; no synthetic operations
```

Visible page 44 attributes equally named composition operations to `TrainSetDataService`; the checked operation inventories show that the intended service context is `TrainSetManagementService`.

### DRTRAINSET21-003

```text
state: context-verified
classification: pdf_operation_name_typo_candidate
scope: official V2.1
validation impact: none; no alias
```

Visible page 44 prints `GetTrainSetCompositon`; exact operation name is `GetTrainSetComposition`.

### Rejected V2.1 observation

A suspected `coupledSide` / `CoupledSide` case mismatch was disproved: visible original and exact V2.1 XSD both use `CoupledSide`. No finding ID exists.

## V2.2 findings

Exact official authority:

```text
VDV-301-2.2 tag
TSI blob     7ab1f8f892bfcea2a8b8a055f07de92c143356f9
TSM blob     da9465d6683e3f7d54a546ab4a13739fb3c3e902
TSD blob     7a132894c281d613e16514a6fa1bcbffe713d066
Common blob  468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enums blob   2a23b512379b18e8f122ac1272cef8229fb86283
```

The integration-branch files checked for the three service schemas are byte-identical to the official tag.

### TSM-002

```text
state: executable-confirmed after current Evidence-Gate revalidation
classification: xsd_structure_modelling_error_candidate
subtype: operation_group_name_mismatch
scope: official V2.2
confidence: high
executable evidence: EV-104 run 33111644388
```

Fresh V2.2 PDF and version-history evidence use the corrected root `TrainSetManagementService.GetTrainSetCompositionResponse`. Exact XSD globally declares that corrected root, but `TrainSetManagementServiceOperations` still contains `TrainSetManagementService.GetTrainSetComposition`.

Counter-hypothesis rejected: the stale group member is not an intentional request name; it is typed as the reused response structure and conflicts with the explicit V2.2 correction history. SDK must not derive supported global-root inventory solely from this service group.

### TSD-002

```text
state: executable-confirmed
classification: pdf_table_or_documentation_error_candidate
scope: official V2.2
confidence: high
executable evidence: EV-110 run 33241603270
```

Visible V2.2 overview pages 34/35 still map the two Unsubscribe requests to the corresponding Retrieve request structures. Section 6.5.2, the detailed operation text and exact XSD instead use `TrainSetDataService.TrainSetUnsubscribeRequestStructure`.

EV-110 confirms:

```text
specialised request with Client-IP-Address + CoachNumber -> valid
Retrieve-like CoachNumber-only request                   -> invalid
schema expects Client-IP-Address before CoachNumber
```

Exact V2.2 XSD remains validation authority.

### TSD-003

```text
state: contextual_not_defect / executable-context-confirmed
classification: service_modelling_or_generic_response_context
scope: official V2.2
confidence: high
executable evidence: EV-104 run 33111644388
```

Fresh TrainSet V2.2 text and General Conventions V2.2 section 4.1.3 independently support two subscription phases:

```text
immediate acknowledgement -> SubscribeResponseStructure
later data event           -> service data response structure
```

Exact TSD V2.2 uses the Subscribe response names locally in `TrainSetDataServiceOperations` as `SubscribeResponseStructure`, while the same global names are typed as the matching Retrieve data response structures. EV-104 confirms both contexts.

This is a response-context resolver requirement, not an XSD defect. Lexical response name alone is insufficient.

### TSM-003

```text
state: context-verified
classification: pdf_embedded_xsd_diagram_stale_candidate
scope: official V2.2
original visual: pinned-byte page 31
validation impact: none; exact XSD remains authority
```

Page 31 uses the corrected `TrainSetManagementService.GetTrainSetCompositionResponse` name but its embedded expanded composition diagram still shows the old flat V2.1 coach fields directly. Exact V2.2 TSI structure has the repeated `SingleCoach -> SingleCoachInATrainSet` wrapper.

Counter-hypothesis rejected: the diagram is not merely hiding/collapsing the wrapper; it visibly expands the reused structure into the old immediate children.

### TSD-004

```text
state: context-verified
classification: pdf_response_structure_copy_paste_error_candidate
scope: official V2.2
original visual: pinned-byte page 40
validation impact: context routing note; exact XSD remains authority
```

Section 6.5.7.2 says later `SubscribeTripInformation` events are sent via `RetrieveTripRefResponseStructure`. The parallel TripRef subscription correctly uses that type, but the TripInformation operation, its Retrieve response semantics and exact XSD require `RetrieveTripInformationResponseStructure`.

No TripRef event-type alias is created for SubscribeTripInformation.

### DRTRAINSET22-001

```text
state: context-verified
classification: pdf_cross_reference_error_candidate
scope: official V2.2
validation impact: none
```

Both German and English introductions point the examples to section `9.1`; table of contents and actual heading place them in section `10`.

### DRTRAINSET22-002

```text
state: context-verified
classification: pdf_cross_reference_error_candidate
scope: official V2.2
validation impact: none
```

Multiple detail passages retain stale section `6.5.1` references after insertion of the new 6.5.1/6.5.2 subscription structures:

```text
UnsubscribeTripRef -> TrainSetUnsubscribeRequestStructure said to be in 6.5.1; actual 6.5.2
RetrieveTripInformation -> RetrieveTripRef said to be 6.5.1; actual 6.5.3
UnsubscribeTripInformation -> TrainSetUnsubscribeRequestStructure said to be in 6.5.1; actual 6.5.2
```

## Evidence

```text
docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md
docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.2.md
docs/pdf_xsd_semantic_audit/24h_executable_validation_trainset_v21.md
docs/pdf_xsd_semantic_audit/24i_executable_validation_trainset_v22_tsd002.md
docs/pdf_xsd_semantic_audit/24d_executable_validation_trainset.md
audit_registry/deep_read_findings_delta_trainset_v21_2026-08-29.json
audit_registry/deep_read_findings_delta_trainset_v22_2026-08-29.json
EV-104 run 33111644388
EV-109 run 33228250613
EV-110 run 33241603270
```

No PR/mail/schema-change disposition is implied by this register. All later remediation remains a separate explicit phase.
