# VideoRecordingService V1.0 / V2.0 / V2.4 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation and targeted XML validation remain pending.

## 1. Version routing matrix

| Document | Executable service schema | Dependency pool | Authority |
|---|---|---|---|
| V1.0 | none confirmed | unresolved | public PDF only for semantics; no strict XSD profile |
| V2.0 | `IBIS-IP_VideoRecordingService_V2.0.xsd` blob `6ef0dae6...` | Common V2.0 + Enums V2.0 | official release |
| V2.4 | `IBIS-IP_VideoRecordingService_V2.4.xsd` blob `07ff2c41...` | Common V2.0 + Enums V2.0 | open PR #27 candidate/integration |

## 2. Operation-family continuity

Across V1.0, V2.0 and V2.4 the functional operation family remains materially stable:

```text
StartRecordingRRM
StartRecordingERM
PauseRecordingRRM
StopRecording
ForceStopRecording
GetVideoRecordingState
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

Service-specific XSD groups list the concrete start/stop/state responses and Pause request. Subscribe/Unsubscribe remain generic subscription modelling and are not treated as missing service-specific XSD operations.

## 3. VRS-003 - V2.0 response compositor mismatch

PDF evidence V1.0/V2.0:

```text
VideoRecordingStateResponse is described as a response data structure providing state information,
fill-level details and error information.
The tables list State, AlarmArchiveFillLevel, OperationErrorMessage and StartStopMode in the same response description.
```

Official V2.0 XSD:

```text
<xs:complexType name="VideoRecordingService.VideoRecordingStateResponseStructure">
  <xs:choice>
    <xs:element name="State" .../>
    <xs:element name="AlarmArchiveFillLevel" .../>
    <xs:element name="OperationErrorMessage" .../>
    <xs:element name="StartStopMode" .../>
  </xs:choice>
</xs:complexType>
```

Executable consequence:

```text
A V2.0 response containing State + AlarmArchiveFillLevel cannot validate against the selected XSD.
A V2.0 response containing State + StartStopMode cannot validate against the selected XSD.
```

V2.4 candidate correction:

```text
Response choice becomes:
  VideoRecordingState OR OperationErrorMessage

VideoRecordingStateStructure becomes:
  State
  AlarmArchiveFillLevel optional
  StartStopMode optional
```

V2.4 document history records:

```text
clarified issues at GetVideoRecordingState
```

Classification:

```text
mismatch_kind: compositor/structure modelling
likely_source_issue: xsd_structure_modelling_error_candidate
confidence: high
validation_behavior: V2.0 still validates exactly against its xs:choice; candidate V2.4 uses corrected candidate structure
```

No V2.0 XSD patch is made in the audit branch.

## 4. VRS-004 - SubscribeDisplayState copy/paste headings

V1.0/V2.0 operation tables use the semantically correct VideoRecordingState operation names.

Detailed section headings/TOC use DisplayState instead.

V2.4 uses VideoRecordingState consistently and its version history explicitly notes fixing copy/paste errors in the subscribe methods.

Classification:

```text
pdf_label_or_heading_error_candidate
confidence: high
```

## 5. VRS-005 - RequestStruture spelling

Official V2.0 XSD and PR-#27 V2.4 candidate both use:

```text
PauseRecordingRRMRequestStruture
```

The element itself is correctly named:

```text
VideoRecordingService.PauseRecordingRRMRequest
```

Impact is mainly type-name/code-generation/API exposure rather than an XML element-name alias.

Classification:

```text
xsd_typo_candidate
confidence: high that spelling is typo-like
breaking-risk: non-zero for codegen/type-name consumers
```

Validation/code generation must use the exact selected XSD until an official correction exists.

## 6. VRS-001 / VRS-002 provenance behavior

```text
V1.0: do not claim strict XSD validation; no official-tag V1.0 service schema found.
V2.4: candidate profile only; open PR #27 is not an official release.
```

## 7. Validation backlog

```text
VRS-VB-001 compile official V2.0 service + Common V2.0 + Enums V2.0.
VRS-VB-002 V2.0 positive single-field response samples allowed by xs:choice.
VRS-VB-003 V2.0 negative multi-field response sample State + AlarmArchiveFillLevel.
VRS-VB-004 compile candidate V2.4 exact pool Common V2.0 + Enums V2.0.
VRS-VB-005 candidate V2.4 positive VideoRecordingState sample with State + optional FillLevel + StartStopMode.
VRS-VB-006 candidate V2.4 alternative OperationErrorMessage response.
VRS-VB-007 codegen/type-inventory check for PauseRecordingRRMRequestStruture.
```

No compile/sample result is claimed by this first pass.
