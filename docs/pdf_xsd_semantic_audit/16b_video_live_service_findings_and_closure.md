# VideoLiveService V1.0 / V2.0 findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD/sample/media validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/16_video_live_service_historical_start.md
docs/pdf_xsd_semantic_audit/16a_video_live_service_v1_0_v2_0_pdf_xsd_first_pass.md
```

## Routing closure

### Public V1.0-era profile

```text
Public writing: VDV 301-2-11, 05/2017
Strict official release-tag service XSD: unresolved / none found in checked tags
Historical backfill performed: no
Reason: no eligible official release-tag VideoLiveService V1.0 XSD found
```

### Official V2.0 profile

```text
Public writing: VDV 301-2-11 VideoLiveService V2.0, 08/2019
Service XSD: IBIS-IP_VideoLiveService_V2.0.xsd
Official blob: d8c52f5de9ef3f5915524fef12da11eabf0ca041
Branch blob: identical
Dependencies: Common V2.0 + Enumerations V2.0
```

## Findings

### VLS-001 - public V1.0 without official release-tag XSD

```text
classification: schema_family_or_provenance_gap
confidence: high for checked tag set
handling: no strict XSD route; do not substitute V2.0
```

### VLS-002 - LiveStreamData xs:choice vs multi-field record

```text
classification: xsd_structure_modelling_error_candidate
mismatch_kind: compositor_or_structure_modelling
confidence: high
handling: validation follows current XSD; local positive/negative samples required; post-audit official schema candidate review
```

The selected V2.0 XSD allows one alternative field per `LiveStreamData`; the V1.0/V2.0 PDFs describe a stream record containing the stream metadata fields together.

### VLS-003 - V1.0 German foreword 301-2-1 reference

```text
classification: pdf_label_or_heading_error_candidate
confidence: high
handling: documentation note only
```

The English V1.0 foreword and V2.0 foreword use 301-2-11.

### VLS-004 - VideoDisplayService name in VideoLiveService start/stop prose

```text
classification: pdf_table_or_documentation_error_candidate
confidence: high
version_scope: V1.0 and V2.0
handling: documentation note; no resolver alias
```

## SDK implications

```text
- Keep public V1.0 known but strict-XSD-unresolved.
- Route V2.0 only to VideoLive V2.0 + Common V2.0 + Enums V2.0.
- Do not use the V2.0 XSD as a silent replacement for V1.0 merely because the V2.0 PDF says the service is compatible with VDV301 1.0 and 2.x.
- Treat `ListAllLiveStreams` XML validation separately from RTSP/RTP media validation.
- Preserve VLS-002 as a known XSD-authoritative-but-semantically-suspicious profile until official correction decisions are made.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
XML sample validation: not performed.
RTSP/RTP runtime validation: not performed.
No XSD modification: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned block

```text
docs/pdf_xsd_semantic_audit/17_video_recording_service_historical_start.md
```

Initial focus:

```text
VideoRecordingService V1.0 / V2.0 / V2.4.
Resolve V1.0 provenance under official-release-only backfill policy.
Resolve official V2.0 pool.
Treat V2.4 branch schema provenance separately as candidate/integration if still unreleased.
Compare recording-control structures and media/file semantics without latest-wins mapping.
```
