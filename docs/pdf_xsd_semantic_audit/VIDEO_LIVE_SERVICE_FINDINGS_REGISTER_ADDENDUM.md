# VideoLiveService findings register addendum

Status: supplemental register; V1.0/V2.0 semantic/provenance first-pass closure completed. VLS-002 is now executable-confirmed.

Authority rule:

```text
V2.0 strict XML validation follows IBIS-IP_VideoLiveService_V2.0.xsd + Common V2.0 + Enums V2.0.
Public V1.0 has no confirmed official-release-tag service XSD in the checked tag set and must not be silently mapped to V2.0.
Media transport/runtime is separate from XML/XSD validation.
```

## VLS-001 - public V1.0 without confirmed official release-tag XSD

```text
state: unresolved strict-XSD provenance
classification: schema_family_or_provenance_gap
confidence: high for checked official release tags
version_scope: public V1.0
validation_behavior: no strict XSD profile; no V2.0 substitution
final_handling_bucket: official_schema_family_clarification_candidate
```

## VLS-002 - LiveStreamData xs:choice vs PDF multi-field structure

```text
state: executable-confirmed PDF/XSD semantic mismatch candidate
classification: xsd_structure_modelling_error_candidate
mismatch_kind: compositor_or_structure_modelling
confidence: high
version_scope: V2.0 XSD; semantic evidence in V1.0 and V2.0 PDFs
validation_behavior: current XSD permits one choice member per LiveStreamData
final_handling_bucket: executable_evidence_complete + post_audit_official_schema_candidate_review
```

Observed PDF record fields include StreamID, camera metadata, rtspURI, dimensions, codec, frame rate, bitrate, transforms and quality together. The XSD places all fields inside one `xs:choice`.

Executable evidence:

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
single StreamID sample: valid
StreamID + CameraName + rtspURI: rejected; CameraName not expected
complete PDF-shaped multi-field sample: rejected; CameraName not expected
EV-103 status: PASS
```

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
```

## VLS-003 - V1.0 German foreword wrong part number

```text
state: confirmed documentation candidate
classification: pdf_label_or_heading_error_candidate
confidence: high
version_scope: V1.0 PDF
validation_behavior: none
```

German V1.0 foreword says 301-2-1; English V1.0 and V2.0 use 301-2-11.

## VLS-004 - VideoDisplayService in VideoLiveService start/stop prose

```text
state: confirmed documentation candidate
classification: pdf_table_or_documentation_error_candidate
confidence: high
version_scope: V1.0 and V2.0 PDFs
validation_behavior: none; no service-name alias
```
