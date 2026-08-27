# EV-104 - executable validation of TrainSet root and context modelling

Status: completed.

Results:

```text
TSM-002: executable-confirmed XSD operation-group/global-root mismatch
TSD-003: dual response typing by context confirmed; resolve as contextual modelling / resolver requirement, not an automatic XSD defect
```

## Evidence run

```text
GitHub Actions run: 33111644388
head tested: a9e9d7d92bf80f2f013338f0cb8ded4aff4dcf88
job: 98655689274
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
EV-104 status: 0 / PASS
```

Harness:

```text
tools/validate_trainset_ev104.py
```

No XSD was changed.

## TSM-002 - V2.2 operation group vs corrected global root

Exact official service family:

```text
IBIS-IP_TrainSetManagementService_V2.2.xsd
-> IBIS-IP_common_V2.2.xsd
-> IBIS-IP_Enumerations_V2.2.xsd
-> IBIS-IP_TrainSetInformationService_V2.2.xsd
```

Static declarations confirmed by the executable harness:

```text
global root exists:
  TrainSetManagementService.GetTrainSetCompositionResponse

global root does not exist:
  TrainSetManagementService.GetTrainSetComposition

TrainSetManagementServiceOperations contains:
  TrainSetManagementService.GetTrainSetComposition

TrainSetManagementServiceOperations does not contain:
  TrainSetManagementService.GetTrainSetCompositionResponse
```

Executable results:

```text
PASS: corrected global GetTrainSetCompositionResponse payload validates
PASS: stale GetTrainSetComposition is rejected as a global root
PASS: actual TrainSetManagementServiceOperations harness compiles
PASS: actual operation group accepts the stale GetTrainSetComposition name
PASS: actual operation group rejects the corrected GetTrainSetCompositionResponse name
```

The operation-group rejection explicitly reports that the corrected element is not expected and that the stale `TrainSetManagementService.GetTrainSetComposition` is expected.

Conclusion:

```text
TSM-002 = executable-confirmed internal XSD operation-inventory mismatch.
Direct global-root validation and operation-group-derived inventory disagree inside the same V2.2 service schema.
```

SDK implication:

```text
Do not derive supported-operation/root inventories solely from service XSD groups.
Use the operation semantic manifest plus global payload-root mapping and retain this finding as a provider/schema note.
```

## TSD-003 - Subscribe response dual typing by context

Exact official service family:

```text
IBIS-IP_TrainSetDataService_V2.2.xsd
-> IBIS-IP_common_V2.2.xsd
-> IBIS-IP_Enumerations_V2.2.xsd
```

The harness confirms two bindings for the same response names.

### SubscribeTripRefResponse

```text
global element type:
  TrainSetDataService.RetrieveTripRefResponseStructure

TrainSetDataServiceOperations local element type:
  SubscribeResponseStructure
```

### SubscribeTripInformationResponse

```text
global element type:
  TrainSetDataService.RetrieveTripInformationResponseStructure

TrainSetDataServiceOperations local element type:
  SubscribeResponseStructure
```

Executable context evidence:

```text
PASS: global SubscribeTripRefResponse accepts Retrieve-style TripRef event data
PASS: global SubscribeTripRefResponse rejects generic Active acknowledgement
PASS: global SubscribeTripInformationResponse rejects generic Active acknowledgement and expects TripInformation
PASS: generic SubscribeResponseStructure acknowledgement accepts Active for both subscription acknowledgement projections
```

This matches the PDF semantic distinction already recorded in the first pass:

```text
immediate subscription acknowledgement -> SubscribeResponseStructure
subsequent event-based data update -> corresponding Retrieve response structure
```

Conclusion:

```text
TSD-003 = resolved as contextual dual typing / resolver requirement.
state: OK with contextual note
classification: service_modelling_or_generic_response_context
not classified as an XSD defect from current evidence
```

SDK implication:

```text
A validator cannot select the payload schema from the lexical response name alone.
It must also know whether it is validating the immediate subscription acknowledgement context or the later subscription data-event context.
This belongs in the operation manifest / response-context resolver.
```

## Block result

```text
TSM-002 -> executable-confirmed XSD mismatch
TSD-003 -> resolved contextual model, not automatic schema defect
```

## Next

```text
EV-105 - AnalogRadioService V2.4 candidate
ARA-003 Transmitter cardinality PDF 1:1 vs candidate XSD 0:1
```
