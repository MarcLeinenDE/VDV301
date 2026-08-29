# EV-112 - TicketValidationService V2.1 executable evidence

Date: 2026-08-29

Status: PASS

## Purpose

EV-112 supplies deterministic executable evidence for XML-material observations found during the independent TicketValidationService V2.1 Deep Read.

It does not turn PDF wording into executable authority and does not authorize schema remediation.

## Exact authority guard

The checker first verifies the exact Git blobs before compiling or probing the schema family:

```text
IBIS-IP_TicketValidationService_V2.1.xsd
f6497e6469b82ee19b185c4de749d13a7ca60bed

IBIS-IP_common_V1.0.xsd
194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c

IBIS-IP_Enumerations_V1.0.xsd
a9bea5bc73003ed91ded8519db06c32c4067831d
```

Authority:

```text
official tag VDV-301-2.1
TVS V2.1 -> Common V1.0 -> Enumerations V1.0
```

The checker also verifies the service's exact include dependency names before running probes.

## Execution provenance

```text
evidence_id: EV-112
checker: tools/validate_tvs_v21_ev112.py
workflow run: 33249561880
job: 99092772643
temporary tested head: 5edc3f1d167e93dffcc3978f6e903ee0fba3f960
result: success / PASS
```

The temporary push-trigger workflow was removed in commit:

```text
83b3cb49c641a789e9e310dc203d590cbf3806a9
Remove temporary TVS V2.1 EV-112 workflow
```

The reusable checker remains on `dev/schema-integration`.

## Evidence A - RouteDeviation

Exact declaration:

```text
VehicleData.RouteDeviation type = RouteDeviationEnumeration
```

Exact Enumerations V1.0:

```text
RouteDeviationEnumeration exists
RouteDirectionEnumeration does not exist

RouteDeviationEnumeration values:
  onroute
  offroute
  unknown
```

Executable samples:

```text
onroute               -> valid
offroute              -> valid
unknown               -> valid
NOT_A_ROUTE_DEVIATION -> invalid
```

Consequence for TVS-002:

```text
The selected V2.1 XSD family enforces RouteDeviationEnumeration.
The PDF's RouteDirectionEnumeration wording is not an executable alias.
```

## Evidence B - CurrentTripRef

Exact declaration:

```text
CurrentTripRef type = IBIS-IP.NMTOKEN
```

Exact Common V1.0:

```text
IBIS-IP.NMTOKEN exists
IBIS-IP.NMToken does not exist
```

Negative schema probe:

```text
type="IBIS-IP.NMToken" -> schema compilation fails
```

Consequence for DRTVS21-001:

```text
The PDF's NMToken spelling cannot be treated as a case-insensitive executable type alias.
```

## Evidence C - CurrentLineData

Exact GetCurrentLine response type:

```text
TicketValidationService.CurrentLineDataStructure
```

The concatenated display string:

```text
TicketValidationServiceCurrentLineData
```

is not an exact service complex type.

Evidence boundary:

```text
EV-112 proves only the exact XSD-side identifier facts.
The PDF uses shortened display conventions elsewhere, including omission of Structure.
Classification of the visible PDF display therefore remains a contextual documentation judgment limited to the missing separator dot.
```

## Scope boundary

EV-112 does not:

- modify any XSD;
- back-apply later TVS/Common/Enumeration versions;
- validate every PDF spelling or display convention;
- revalidate TVS-001 or TVS-003, whose scopes are outside V2.1;
- create compatibility aliases or normalizations.

The exact selected XSD remains normative validation authority.
