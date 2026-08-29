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
```

Important:

```text
EV-003 through EV-100 were never defined.
The numbering intentionally separates baseline evidence (001/002) from finding-specific evidence (101+).
Do not describe the completed set as a continuous range beginning at EV-001.
Correct wording at the current state: "EV-001, EV-002 and EV-101 through EV-111".
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
The checked DoorStateService V2.1 schema family is byte-identical to official VDV-301-2.1 authority and intentionally routes to Common V1.0 + Enumerations V1.0.
For DRS-002, probe roots are typed directly to exact normative RetrieveSpecific response complex types and prove ErrorMessage valid / OperationErrorMessage invalid.
For DRS-003, the exact normative local group declarations are first verified as untyped; the executable probe reproduces that declaration form at global scope only to demonstrate default xs:anyType semantics. EV-111 does not claim that real global DoorState Get request roots exist.
```

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
