# TrainSet services findings register addendum

Status: V2.1 Deep Read completed under the mandatory Finding Evidence Gate; EV-109 executable evidence completed for TSI-001, TSM-001 and TSD-001. V2.2 first-pass/EV-104 findings remain separate and must still pass their own V2.2 Fresh Read before final revalidation status is inherited.

## TSI-001

```text
state: executable-confirmed
classification: xsd_structure_modelling_error_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

The official V2.1 writing states that `GetTrainSetComposition` returns a sequence of coach data sets, one per coach. Visible pinned-byte pages 24/25 show the coach fields and the printed V2.1 XSD structure.

Exact official V2.1 XSD:

```text
IBIS-IP_TrainSetInformationService_V2.1.xsd
blob 897f373e31b76aa23d8bc206854b042524e4c102
```

models a single flat coach field sequence without a repeated coach wrapper.

EV-109, run `33228250613`:

```text
one flat coach record: valid
second PDF-described coach record: invalid
error: Element 'CoachNumber': This element is not expected.
```

Counter-hypothesis checked: the V2.1 model cannot represent repeated coach records by repeating flat fields; no repeated declarations/wrapper exist.

Handling:

```text
strict V2.1 validation follows the V2.1 XSD
explain the historical modelling limitation
do not synthesize a repeated wrapper from the later V2.2 correction
```

## TSM-001

```text
state: executable-confirmed
classification: xsd_operation_or_element_name_error_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

Exact V2.1 XSD declares:

```text
TrainSetManagementService.GetTrainSetComposition
  -> TrainSetInformationService.GetTrainSetCompositionResponseStructure
```

The later form `TrainSetManagementService.GetTrainSetCompositionResponse` does not exist as a V2.1 global root or operation-group member.

EV-109, run `33228250613`:

```text
old V2.1 root: valid
later corrected ...Response root: invalid / no matching global declaration
```

Counter-hypothesis checked: the old name is not merely a PDF shorthand; it is the actual executable V2.1 root/group element.

Handling:

```text
use the exact historical V2.1 root
do not create a later-version alias
```

## TSM-002

```text
state: executable-confirmed from historical EV-104, pending V2.2 Deep-Read Evidence-Gate revalidation
classification: xsd_structure_modelling_error_candidate
subtype: operation_group_name_mismatch
scope: official V2.2
confidence: provisional-high pending fresh V2.2 revalidation
```

Official V2.2 globally declares the corrected root:

```text
TrainSetManagementService.GetTrainSetCompositionResponse
```

but `TrainSetManagementServiceOperations` still uses:

```text
TrainSetManagementService.GetTrainSetComposition
```

EV-104 run `33111644388` established the executable global-root/group mismatch. Under the 2026-08-29 Evidence Gate, this old classification is **not grandfathered**; it will be independently rechecked during `TRAINSET_V2.2`.

## TSD-001

```text
state: executable-confirmed
classification: service_modelling_or_generic_response_candidate
scope: official V2.1
confidence: high after source/context/disproof checks + EV-109
```

The V2.1 PDF describes Retrieve/Subscribe/Unsubscribe triples for TripRef and TripInformation. The exact V2.1 TrainSetDataService XSD operation group/global inventory contains only the four Retrieve request/response members.

EV-109, run `33228250613`, confirms:

```text
all four Retrieve request/response members and roots exist
PDF-described TrainSetDataService-specific Subscribe/Unsubscribe members/roots are absent
generic Common V2.0 Subscribe/Unsubscribe structures exist
```

Counter-hypothesis checked: this is **not** evidence that subscription infrastructure is wholly absent. It is specifically a service-prefixed TrainSetDataService operation/root modelling gap.

Handling:

```text
do not invent missing V2.1 service roots
retain operation/context knowledge separately from XSD root inventory
```

## TSD-002

```text
state: historical candidate pending V2.2 Deep-Read Evidence-Gate revalidation
classification: pdf_table_or_documentation_error_candidate
scope: official V2.2
```

Earlier audit: V2.2 operation overview lists Retrieve request structures for Unsubscribe, while detailed text and XSD use `TrainSetUnsubscribeRequestStructure`.

This finding is **not grandfathered** and will be freshly checked against the byte-pinned V2.2 original, full table/detail context and exact V2.2 XSD.

## TSD-003

```text
state: resolved - OK with contextual resolver note after historical EV-104; pending V2.2 Deep-Read Evidence-Gate revalidation
classification: service_modelling_or_generic_response_context
scope: official V2.2
```

Historical EV-104 showed context-dependent typing of the same Subscribe response names:

```text
TrainSetDataServiceOperations:
  SubscribeTripRefResponse          -> SubscribeResponseStructure
  SubscribeTripInformationResponse  -> SubscribeResponseStructure

global elements:
  SubscribeTripRefResponse          -> RetrieveTripRefResponseStructure
  SubscribeTripInformationResponse  -> RetrieveTripInformationResponseStructure
```

The old interpretation was that immediate acknowledgement and later subscription data event are distinct contexts. The upcoming V2.2 Fresh Read will re-run this through the current Evidence Gate rather than accepting the old resolution automatically.

## DRTRAINSET21-001

```text
state: context-verified
classification: pdf_cross_reference_error_candidate
scope: official V2.1
validation impact: none
```

The V2.1 prose points to section `9.1` for material/examples located in section 10. Surrounding document structure was checked before classification.

## DRTRAINSET21-002

```text
state: context-verified
classification: pdf_service_name_copy_paste_error_candidate
scope: official V2.1
original visual: confirmed from pinned-byte page 44
validation impact: none; no synthetic operations
```

Page 44 states that TrainSetInformationService `GetTrainSetComposition` / `SubscribeTrainSetComposition` provide the same information as equally named operations of the **TrainSetDataService**.

Counter-check of the full V2.1 operation inventories:

```text
TrainSetDataService       -> no composition operations with those names
TrainSetManagementService -> composition operation/context exists
```

Therefore the printed TrainSetDataService reference is classified as a documentation/service-name error candidate; likely intended reference is TrainSetManagementService.

## DRTRAINSET21-003

```text
state: context-verified
classification: pdf_operation_name_typo_candidate
scope: official V2.1
original visual: confirmed from pinned-byte page 44
validation impact: none; no alias
```

Page 44 prints `GetTrainSetCompositon`. The operation inventory and exact XSD use `GetTrainSetComposition`.

SDK rule: never create the typo spelling as an operation alias.

## Rejected candidate observation

A potential `coupledSide` / `CoupledSide` casing discrepancy was explicitly tested and rejected.

Visible original pages 24/25 and exact V2.1 XSD both use:

```text
CoupledSide
```

No finding ID is created. This rejected observation is retained as evidence of the mandatory disproof step.

## Evidence

```text
docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md
docs/pdf_xsd_semantic_audit/24h_executable_validation_trainset_v21.md
audit_registry/deep_read_findings_delta_trainset_v21_2026-08-29.json
EV-109 run 33228250613
```

EV-104 remains V2.2-specific and will be compared only after the independent `TRAINSET_V2.2` Fresh Read.
