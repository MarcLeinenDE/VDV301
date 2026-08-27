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
EV-104  TrainSet operation/root/context modelling
EV-105  AnalogRadio candidate Transmitter cardinality
```

Important:

```text
EV-003 through EV-100 were never defined.
The numbering intentionally separates baseline evidence (001/002) from finding-specific evidence (101+).
Do not describe the completed set as "EV-001 through EV-105".
Correct wording: "EV-001, EV-002 and EV-101 through EV-105".
```

Existing EV document names, historical workflow run IDs and historical tool names are not retroactively renamed because they are provenance evidence.

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

## Naming guard

Do not create future names such as:

```text
EV-25b
EV25c
runtime-EV-...
```

Use `RV-*` for runtime/protocol validation.
