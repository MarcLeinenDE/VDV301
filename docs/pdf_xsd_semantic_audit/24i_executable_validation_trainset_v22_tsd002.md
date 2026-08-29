# EV-110 - TrainSetDataService V2.2 Unsubscribe request shape

Status: completed / PASS.

Purpose: executable confirmation of `TSD-002` after the V2.2 Fresh Read under the mandatory Finding Evidence Gate.

## Authority

```text
PDF: official VDV-Schrift 301-2-14 V2.2, source_id TRAINSET_V2.2
XSD: IBIS-IP_TrainSetDataService_V2.2.xsd
     official VDV-301-2.2 blob 7a132894c281d613e16514a6fa1bcbffe713d066
Dependencies:
     IBIS-IP_common_V2.2.xsd       468fee6d177e7185dbcd5d3f90cfb114e29e01ae
     IBIS-IP_Enumerations_V2.2.xsd 2a23b512379b18e8f122ac1272cef8229fb86283
```

## PDF observation

The operation overview on visible pinned-byte pages 34/35 still lists the Unsubscribe requests with the Retrieve request structures:

```text
UnsubscribeTripRef
  Request -> TrainSetDataService.RetrieveTripRefRequestStructure

UnsubscribeTripInformation
  Request -> TrainSetDataService.RetrieveTripInformationRequestStructure
```

The immediately following detailed text defines and uses `TrainSetDataService.TrainSetUnsubscribeRequestStructure` instead. The version history explicitly says this new structure was introduced in V2.2 to enable correct subscription handling for Retrieve data.

## Executable harness

```text
tools/validate_trainset_tsd002_ev110.py
```

Workflow evidence:

```text
run: 33241603270
job: 99071787598
head tested: 19245d4d81688a8ce597c7772348ad3a8bb73fe9
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
result: PASS
```

The temporary push-trigger workflow used only for execution was removed immediately after the run. The checker remains in the repository; no XSD was changed.

## Results

For both roots:

```text
TrainSetDataService.UnsubscribeTripRefRequest
TrainSetDataService.UnsubscribeTripInformationRequest
```

the correct specialised shape containing at least:

```xml
<Client-IP-Address><Value>192.0.2.10</Value></Client-IP-Address>
<CoachNumber><Value>4711</Value></CoachNumber>
```

validates.

A Retrieve-like shape matching the misleading overview idea:

```xml
<CoachNumber><Value>4711</Value></CoachNumber>
```

is rejected for each root with the decisive schema error:

```text
Element 'CoachNumber': This element is not expected. Expected is ( Client-IP-Address ).
```

## Evidence-Gate conclusion

Counter-hypothesis considered: the overview might only be an informal indication of the coach parameter rather than an exact structure reference. This does not hold because the table column is explicitly `Data type used, data structure`, and neighbouring entries identify exact request/response structure types.

Conclusion:

```text
TSD-002 = executable-confirmed PDF overview / exact-XSD request-shape mismatch.
Exact V2.2 validation requires TrainSetUnsubscribeRequestStructure.
The SDK must not accept or synthesize the Retrieve-like CoachNumber-only form from the PDF overview.
```
