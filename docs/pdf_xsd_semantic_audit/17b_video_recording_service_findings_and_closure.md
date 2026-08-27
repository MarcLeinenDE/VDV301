# VideoRecordingService findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD compilation/sample validation remains pending.

## Routing closure

### V1.0

```text
Public VDV 301-2-12 document exists.
No official release-tag VideoRecordingService V1.0 XSD was found.
Strict XSD routing remains unresolved.
Do not map to V2.0.
```

### V2.0

```text
Official file: IBIS-IP_VideoRecordingService_V2.0.xsd
Blob: 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7
Pool: Common V2.0 + Enumerations V2.0
```

### V2.4

```text
Public document exists.
Executable branch file is exact open PR #27 candidate blob 07ff2c41731e63fd85b203e4b8e0186136caaaaf.
Pool remains Common V2.0 + Enumerations V2.0.
Candidate/integration authority only.
```

## Findings

```text
VRS-001  schema_family_or_provenance_gap
         V1.0 public PDF without official-tag XSD mapping

VRS-002  schema_family_or_provenance_gap
         V2.4 public PDF with open PR #27 candidate, no official V2.4 release tag

VRS-003  xsd_structure_modelling_error_candidate
         official V2.0 VideoRecordingStateResponseStructure uses xs:choice for fields described as one state response;
         V2.4 candidate corrects to VideoRecordingStateStructure sequence + error alternative

VRS-004  pdf_label_or_heading_error_candidate
         V1.0/V2.0 SubscribeDisplayState headings vs VideoRecordingState operation identity; corrected in V2.4

VRS-005  xsd_typo_candidate
         PauseRecordingRRMRequestStruture persists in V2.0 official and V2.4 candidate
```

## SDK implications

```text
- Do not infer XSD availability from PDF availability.
- Preserve official V2.0 and candidate V2.4 as separate profiles.
- V2.4 candidate deliberately selects Common/Enums V2.0; do not latest-wins substitute V2.4 dependencies.
- Diagnostics for V2.0 multi-field state responses should explain that the selected XSD uses xs:choice even though the PDF describes combined state information.
- Candidate V2.4 may be used only when candidate/integration profile is explicitly selected.
- Type-name typo handling must never silently rewrite PauseRecordingRRMRequestStruture.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
Sample XML validation: not performed.
No XSD correction: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned block

```text
18_video_display_service_historical_start.md
VideoDisplayService V1.0 / V2.0
```
