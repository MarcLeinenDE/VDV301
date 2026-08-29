# 24l - Executable validation: TicketValidationService V2.2

Status: completed

Date: 2026-08-29

Evidence ID: `EV-113`

## Purpose

EV-113 provides executable evidence for XML/XSD claims arising from the independent `TVS_V2.2` Deep Read. It does not make the PDF executable authority and does not modify normative XSDs.

## Exact authority

Official tag:

```text
VDV-301-2.2
```

Exact checked family:

```text
IBIS-IP_TicketValidationService_V2.2.xsd  5a4be2b2ba66860f035777ec0458dba0790880e1
IBIS-IP_common_V2.2.xsd                    468fee6d177e7185dbcd5d3f90cfb114e29e01ae
IBIS-IP_Enumerations_V2.2.xsd              2a23b512379b18e8f122ac1272cef8229fb86283
```

The repository files tested by EV-113 are byte-identical to those official-tag blobs.

Exact include route:

```text
TicketValidationService V2.2 -> Common V2.2 -> Enumerations V2.2
```

## Checker

```text
tools/validate_tvs_v22_ev113.py
```

The checker first validates the exact Git blob identity and include route, then compiles the untouched selected service family before running probes.

## Claims tested

### TVS-002 - RouteDeviation enum mismatch

Exact service declaration:

```text
VehicleData.RouteDeviation -> RouteDeviationEnumeration
```

Exact V2.2 enum value sets:

```text
RouteDeviationEnumeration:
  onroute
  offroute
  unknown

RouteDirectionEnumeration:
  Forward
  Backward
  Clockwise
  Counterclockwise
  Other
```

Executable results:

```text
onroute/offroute/unknown as RouteDeviation -> valid
Forward as RouteDeviation                 -> invalid
Forward/.../Other as RouteDirection       -> valid
onroute as RouteDirection                 -> invalid
```

This proves that the two V2.2 enum types are not interchangeable aliases.

### DRTVS21-001 V2.2 instance - CurrentTripRef type case

Exact declaration:

```text
CurrentTripRef -> IBIS-IP.NMTOKEN
```

Checks:

```text
IBIS-IP.NMTOKEN exists in exact Common V2.2
IBIS-IP.NMToken does not exist
probe using IBIS-IP.NMToken -> schema compile failure
```

### DRTVS21-002 V2.2 instance - CurrentLineData exact type

Exact response type:

```text
TicketValidationService.CurrentLineDataStructure
```

The PDF missing-dot string `TicketValidationServiceCurrentLineData` is not an exact service complex type. This is XSD-side identifier evidence only; PDF display-convention classification remains contextual.

### TVS-003 - CurrentTariffStop rename boundary

Exact V2.2 schema exposes:

```text
TicketValidationService.GetCurrentTariffStopResponse
TicketValidationService.CurrentTariffStopDataStructure
```

and does not expose the stale V2.1-era forms:

```text
TicketValidationService.GetCurrentStopPointResponse
TicketValidationService.CurrentStopPointDataStructure
```

Executable root samples:

```text
GetCurrentTariffStopResponse with OperationErrorMessage -> valid
GetCurrentStopPointResponse with same branch            -> invalid; no matching global declaration
```

## Run provenance

```text
run: 33257767942
job: 99114368558
head tested: 28851cfdcf10e5569e512e235ce58ab02adb5167
workflow: temporary push-trigger EV-113 workflow
result: PASS
```

The temporary workflow was removed immediately afterward. The permanent checker remains.

## Result

```text
EV-113 PASS
```

Evidence effect:

```text
TVS-002 V2.2 -> executable_confirmed
TVS-003 V2.2 executable rename boundary -> executable_confirmed
DRTVS21-001 V2.2 instance -> executable_confirmed
DRTVS21-002 V2.2 exact-XSD side -> confirmed; PDF display classification remains context_verified
```

No XSD was modified. No provider-facing or official-facing remediation action was taken.
