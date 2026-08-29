# Deep Read – TrainSet services V2.1

Status: `needs_visual_review`  
Date: 2026-08-29  
Document ID: `TRAINSET_V2.1`

## 1. Source identity

Official publication:

```text
VDV-Schrift 301-2-14
TrainSetInformationService / TrainSetManagementService / TrainSetDataService
Version 2.1
05/2018
```

Official source:

```text
https://www.vdv.de/vdv-301-2-14-v2-1-sds-trainsetservices.pdfx
```

Byte pin:

```text
SHA-256  8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e
size      1,708,401 bytes
pin run   33226637254
```

The interactive PDF screenshot backend returned cache-miss for requested material pages. Relevant pages were therefore rendered from the byte-pinned original with the approved pinned-byte visual fallback and inspected directly.

The document is not promoted to `exhaustive_read`: the textual fresh read is complete and the semantically critical pages were visually checked, but not every page/figure was individually rendered and inspected.

## 2. Evidence-gate discipline

This Deep Read is subject to:

```text
docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md
```

Work order used:

```text
1. fresh-read the official V2.1 writing independently;
2. inspect semantically critical original pages from pinned bytes;
3. establish exact official V2.1 XSD identities and dependencies;
4. only then compare with TSI-001 / TSM-001 / TSD-001 and later-version findings;
5. actively test plausible counter-explanations;
6. executable-test V2.1 XML/root/operation behaviour with EV-109.
```

A suspected `coupledSide` / `CoupledSide` casing mismatch was deliberately tested as a counter-hypothesis and rejected: the visible original page and the exact XSD both use `CoupledSide`. No finding is opened for that suspicion.

## 3. Exact V2.1 XSD authority

All three stored V2.1 service schemas are byte-identical to the official upstream tag `VDV-301-2.1`.

### TrainSetInformationService

```text
IBIS-IP_TrainSetInformationService_V2.1.xsd
Git blob: 897f373e31b76aa23d8bc206854b042524e4c102
includes: IBIS-IP_common_V2.0.xsd
```

### TrainSetManagementService

```text
IBIS-IP_TrainSetManagementService_V2.1.xsd
Git blob: add9d1cb37e5759ff7a77855b239108d38373206
includes:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
  IBIS-IP_TrainSetInformationService_V2.1.xsd
```

### TrainSetDataService

```text
IBIS-IP_TrainSetDataService_V2.1.xsd
Git blob: c2cdb73fcae265a2e4e0349ac6072e3548e36d8b
includes:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
  IBIS-IP_CustomerInformationService_V2.0.xsd
```

No neighbouring-version schema is substituted.

## 4. Fresh-read service inventory

### TrainSetInformationService

The writing describes:

```text
GetTrainSetComposition
SubscribeTrainSetComposition
UnsubscribeTrainSetComposition
```

The visible operation table leaves request data empty for `GetTrainSetComposition` and points its response to `TrainSetInformationService.GetTrainSetCompositionResponse`. The subscription sections use the generic Common `SubscribeRequest` / `SubscribeResponse` and `UnsubscribeRequest` / `UnsubscribeResponse` structures.

### TrainSetManagementService

The writing covers train-set mode management plus composition access. The V2.1 XSD uses the response data structure from TrainSetInformationService for its composition operation.

### TrainSetDataService

The writing describes Retrieve/Subscribe/Unsubscribe triples for TripRef and TripInformation. The V2.1 service XSD itself exposes only the Retrieve roots/members; generic subscription infrastructure exists in Common V2.0.

## 5. TSI-001 – multiple coaches cannot be represented by the V2.1 XSD

### Original publication

Visible page 24 introduces one coach data set with the fields:

```text
CoachType
CoachNumber
FrontCabin
RearCabin
CoachPositionInTrainSet
CoupledSide
CoachState
```

Visible page 25 then states that the response returns a **sequence of coach data sets, one per coach**.

On that same visible page, the printed XSD view shows a single flat sequence of coach fields under `TrainSetInformationService.GetTrainSetCompositionResponseStructure`; no repeated coach wrapper is present.

### Exact XSD

The official V2.1 schema contains one flat sequence and no repeating coach record/wrapper.

### Counter-hypothesis checked

Could repetition be represented by repeating one or more of the individual coach fields rather than a wrapper? No. The declarations do not provide such repetition and the resulting record boundaries would in any case not be represented.

### Executable evidence

EV-109, canonical workflow-dispatch run `33228250613`:

```text
one flat coach record                                 VALID
second PDF-described coach record                    INVALID
error: Element 'CoachNumber': This element is not expected.
```

### Result

```text
finding: TSI-001
state: executable_confirmed
classification: xsd_structure_modelling_error_candidate
validation behaviour: strict V2.1 validation follows the exact V2.1 XSD and therefore cannot carry the documented multi-coach sequence
SDK: explain the mismatch; do not invent a repeated wrapper for V2.1
```

The V2.2 correction is historical evidence only and is not back-applied here.

## 6. TSM-001 – V2.1 composition response root/name

### Exact V2.1 XSD

V2.1 declares:

```text
TrainSetManagementService.GetTrainSetComposition
  -> TrainSetInformationService.GetTrainSetCompositionResponseStructure
```

It does not declare the later corrected root:

```text
TrainSetManagementService.GetTrainSetCompositionResponse
```

### Counter-hypothesis checked

Could `GetTrainSetComposition` merely be a shorthand operation label while a `...Response` global root exists elsewhere? No. The exact V2.1 global-root inventory and operation group both use the old form; the later form is absent.

### Executable evidence

EV-109 run `33228250613`:

```text
V2.1 old-name root GetTrainSetComposition            VALID
later GetTrainSetCompositionResponse root            INVALID / no matching global declaration
```

### Result

```text
finding: TSM-001
state: executable_confirmed
classification: xsd_operation_or_element_name_error_candidate
SDK: use the exact V2.1 root; do not create a compatibility alias from the later spelling
```

## 7. TSD-001 – V2.1 service-specific subscription operation gap

### Publication context

The V2.1 writing describes:

```text
RetrieveTripRef / SubscribeTripRef / UnsubscribeTripRef
RetrieveTripInformation / SubscribeTripInformation / UnsubscribeTripInformation
```

### Exact service XSD

`TrainSetDataServiceOperations` contains only:

```text
RetrieveTripRefRequest
RetrieveTripRefResponse
RetrieveTripInformationRequest
RetrieveTripInformationResponse
```

No TrainSetDataService-prefixed Subscribe/Unsubscribe roots or operation-group members exist in the V2.1 service schema.

### Counter-hypothesis checked

Could the apparent gap mean that subscription is entirely unsupported by the schema family? No. Generic Common V2.0 `Subscribe*` / `Unsubscribe*` infrastructure exists. Therefore the precise finding is a **service-specific operation/root modelling gap**, not absence of all subscription support.

### Executable evidence

EV-109 run `33228250613` confirms:

```text
all four Retrieve group members/roots present
all PDF-described TrainSetDataService-specific Subscribe/Unsubscribe members/roots absent
generic Common V2.0 subscription structures present
```

### Result

```text
finding: TSD-001
state: executable_confirmed
classification: service_modelling_or_generic_response_candidate
SDK: do not infer service-prefixed V2.1 roots that the selected XSD does not declare; retain operation/context knowledge separately from XSD root inventory
```

## 8. DRTRAINSET21-001 – stale/wrong section cross-reference

The V2.1 prose points the reader to section `9.1` for material/examples that are located in section 10.

Counter-check: the surrounding section structure was checked rather than treating the number in isolation.

```text
state: context_verified
classification: pdf_cross_reference_error_candidate
validation impact: none
SDK eligibility: explanatory documentation knowledge only
```

## 9. DRTRAINSET21-002 – wrong service named in composition comparison

Visible page 44 states that `GetTrainSetComposition` / `SubscribeTrainSetComposition` provided by `TrainSetInformationService` provide the same information as the equally named operations of the **TrainSetDataService**.

Full operation inventories were checked before classification:

```text
TrainSetDataService       -> no equally named composition operations
TrainSetManagementService -> contains GetTrainSetComposition and composition-related service context
```

Counter-hypothesis: this is not merely an alternate alias for TrainSetDataService; the actual V2.1 TSD operation inventory is TripRef/TripInformation-oriented and contains no composition operation.

```text
state: context_verified
classification: pdf_service_name_copy_paste_error_candidate
likely intended reference: TrainSetManagementService
validation impact: none; do not synthesize TrainSetDataService composition operations
```

## 10. DRTRAINSET21-003 – `GetTrainSetCompositon` typo

Visible page 44 prints:

```text
GetTrainSetCompositon
```

in a paragraph that otherwise refers to the actual operation `GetTrainSetComposition`.

The document operation inventory and exact XSD spelling were checked as counter-evidence; both use `Composition`.

```text
state: context_verified
classification: pdf_operation_name_typo_candidate
validation impact: none
SDK: never create `GetTrainSetCompositon` as an alias
```

## 11. Rejected candidate observation – `coupledSide`

A casing discrepancy was suspected from extracted material.

Visible original pages 24/25 and the exact XSD show:

```text
CoupledSide
```

Result:

```text
rejected_after_deep_read
no finding ID opened
reason: original visible source disproves the extracted-text suspicion
```

This rejection is retained as evidence that the Deep Read actively attempts to disprove candidate findings.

## 12. EV-109 full-suite baseline

Canonical manual workflow run:

```text
run: 33228250613
result: PASS
```

In addition to EV-109:

```text
50/50 root XSD compile
39 XSD service profiles
84 direct include edges
EV-103..EV-109 checked in the current suite
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

EV-104 remains specifically the later V2.2 TrainSet evidence lane; it is not used to replace V2.1 authority.

## 13. Deferred V2.2 findings

The following existing topics are deliberately **not** resolved from V2.1 evidence:

```text
TSM-002
TSD-002
TSD-003
```

They belong to `TRAINSET_V2.2` and must pass a separate independent V2.2 Fresh Read and the current Finding Evidence Gate before their older classifications are accepted.

## 14. Completion state

```text
textual fresh read: complete
targeted original visual review: complete for semantically critical pages
exact V2.1 XSD authority: established
active-disproof examples: completed
executable validation: EV-109 PASS
document state: needs_visual_review
```

No XSD was changed by this Deep Read.
