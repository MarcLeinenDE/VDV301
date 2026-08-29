# Evidence ID policy

Status: active naming policy for audit and SDK evidence.

## Purpose

The audit uses separate evidence-ID namespaces so XSD/schema evidence and runtime/protocol evidence cannot be confused.

## EV - executable XSD/schema evidence

`EV-*` is reserved for executable XML/XSD/schema-family evidence.

Existing historical IDs remain unchanged:

```text
EV-001  superbranch root-XSD compile sanity
EV-002  legacy V1.0 root-adapter compile
EV-101  PCS-001 OperationNotSupported dependency/value-set mismatch
EV-102  CE-018 ServiceIdentificationWithStateList cardinality
EV-103  video-service xs:choice findings
EV-104  TrainSet V2.2 operation/root/context modelling
EV-105  AnalogRadio candidate Transmitter cardinality
EV-106  Common V2.3 official vs PR #30 schema-variant behaviour
EV-107  DMS V2.2 Deep Read schema declarations
EV-108  DMS V2.4 candidate/integration Deep Read schema declarations
EV-109  TrainSet V2.1 Deep Read modelling/root/operation evidence
EV-110  TrainSetDataService V2.2 Unsubscribe request-shape mismatch (TSD-002)
EV-111  DoorStateService V2.1 RetrieveSpecific error-branch naming and untyped Get-request declaration semantics
EV-112  TicketValidationService V2.1 RouteDeviation/CurrentTripRef/CurrentLineData exact-type evidence
EV-113  TicketValidationService V2.2 RouteDeviation enum separation and CurrentTariffStop rename/type evidence
EV-114  TicketValidationService V2.3 official-route/candidate authority guard and inherited V2.2 executable boundary
```

Important:

```text
EV-003 through EV-100 were never defined.
The numbering intentionally separates baseline evidence (001/002) from finding-specific evidence (101+).
Do not describe the completed set as a continuous range beginning at EV-001.
Correct wording at the current state: "EV-001, EV-002 and EV-101 through EV-114".
```

Existing EV document names, historical workflow run IDs and historical tool names are not retroactively renamed because they are provenance evidence.

Authority guards:

```text
EV-108:
The public DMS V2.4 PDF is an official VDV writing.
The DMS V2.4 XSD checked by EV-108 is candidate/integration material in dev/schema-integration.
EV-108 success must never be described as official-release XSD conformance.

EV-109:
The three checked TrainSet V2.1 service XSDs are byte-identical to the official upstream VDV-301-2.1 tag.
EV-109 is V2.1 evidence only and must not be used to back-apply V2.2 corrections or EV-104 behaviour.

EV-110:
The checked TrainSetDataService V2.2 schema is byte-identical to official VDV-301-2.2 blob 7a132894c281d613e16514a6fa1bcbffe713d066.
EV-110 proves exact V2.2 Unsubscribe request validation behaviour for TSD-002; it does not turn the PDF into executable authority.

EV-111:
The checked DoorStateService V2.1 schema family is byte-identical to official VDV-301-2.1 authority and intentionally routes to Common V1.0 + Enumerations V1.0:
  DoorStateService abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
  Common V1.0     194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
  Enums V1.0      a9bea5bc73003ed91ded8519db06c32c4067831d
For DRS-002, probe roots are typed directly to exact normative RetrieveSpecific response complex types and prove ErrorMessage valid / OperationErrorMessage invalid.
For DRS-003, the exact normative local group declarations are first verified as untyped; the executable probe reproduces that declaration form at global scope only to demonstrate default xs:anyType semantics. EV-111 does not claim that real global DoorState Get request roots exist.

EV-112:
The checked TicketValidationService V2.1 schema family is byte-identical to official VDV-301-2.1 authority and intentionally routes to Common V1.0 + Enumerations V1.0:
  TicketValidationService f6497e6469b82ee19b185c4de749d13a7ca60bed
  Common V1.0             194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
  Enums V1.0              a9bea5bc73003ed91ded8519db06c32c4067831d
EV-112 proves the exact RouteDeviation type/value-set behavior, the case-sensitive CurrentTripRef type identifier, and the exact CurrentLineData response type.
Its CurrentLineData check is XSD-side evidence only; it does not declare every shortened PDF display convention defective.

EV-113:
The checked TicketValidationService V2.2 schema family is byte-identical to official VDV-301-2.2 authority and uses the version-aligned route:
  TicketValidationService 5a4be2b2ba66860f035777ec0458dba0790880e1
  Common V2.2             468fee6d177e7185dbcd5d3f90cfb114e29e01ae
  Enums V2.2              2a23b512379b18e8f122ac1272cef8229fb86283
EV-113 proves that VehicleData.RouteDeviation uses RouteDeviationEnumeration even though RouteDirectionEnumeration also exists in V2.2, and proves the two enum value sets are incompatible.
EV-113 also proves the case-sensitive CurrentTripRef type, the exact CurrentLineData response type, and the executable CurrentTariffStop rename boundary: GetCurrentTariffStopResponse is valid while stale GetCurrentStopPointResponse has no matching global declaration.
Its CurrentLineData check remains XSD-side evidence only; PDF display-convention classification is contextual.

EV-114:
The official VDV-301-2.3 release does not contain an IBIS-IP_TicketValidationService_V2.3.xsd file. The official route is the unchanged V2.2-named family:
  TicketValidationService V2.2 file 5a4be2b2ba66860f035777ec0458dba0790880e1
  Common V2.2                        468fee6d177e7185dbcd5d3f90cfb114e29e01ae
  Enums V2.2                         2a23b512379b18e8f122ac1272cef8229fb86283
The integration branch separately contains IBIS-IP_TicketValidationService_V2.3.xsd blob b17591c5b067254dd3e2260f3ef2acd2e18394a9, introduced as candidate/integration material.
EV-114 proves both families compile and currently match for the critical TVS declarations, but keeps their provenance distinct. It also reconfirms the official-route RouteDeviation behavior and CurrentTariffStop rename boundary. Semantic equality must never promote the V2.3-named candidate file to historical official release authority.
```

The provenance metadata correction for the two DoorState dependency blob IDs is recorded in `AUDIT_CORRECTION_DELTA_DOOR_V21_BLOB_PROVENANCE_2026-08-29.md`; the executed validation result itself is unchanged.

## RV - runtime/protocol evidence

`RV-*` is reserved for deterministic or live runtime/protocol evidence outside the XSD-validation lane.

Current mapping:

```text
RV-001  HTTP/XML transport and Content-Type classifier
RV-002  DNS-SD/service-discovery classifier
RV-003  TimeService/SNTP runtime profile
RV-004  Video RTSP/RTP boundary/profile
RV-005+ future runtime/network/subscription evidence as assigned
```

Block numbers remain document/work-plan identifiers and are not evidence IDs:

```text
Block 25a = authority/source matrix (planning/source classification; no standalone RV evidence ID required)
Block 25b = RV-001
Block 25c = RV-002
Block 25d = RV-003
Block 25e = RV-004
```

## Rule IDs are separate

Norm/profile check IDs such as:

```text
HTTP-V01
HTTP-X02
DNS-X03
DISC-V02
TS-V01
SNTP-X01
```

are rule identifiers, not evidence IDs. A single RV run can exercise many rule IDs.

## Provenance rule

Every evidence record should state:

```text
evidence_id
block/document
exact git head tested
workflow/run or local execution context
authority class
target profile/schema pool
result
```

Candidate/integration evidence must remain explicitly candidate-labelled.

## Finding Evidence Gate interaction

An EV proves the executable claims it actually tests; it does not by itself prove every PDF interpretation or remediation conclusion attached to a finding.

For findings re-evaluated under `FINDING_EVIDENCE_GATE.md`, executable evidence must be combined with the applicable original-source, notation/term, exact-authority, full-context and disproof checks before the complete finding is treated as revalidated.

## Naming guard

Do not create future names such as:

```text
EV-25b
EV25c
runtime-EV-...
```

Use `RV-*` for runtime/protocol validation.
