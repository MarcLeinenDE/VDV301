# AUDIT HANDOFF DELTA - VideoRecordingService V2.4 Deep Read

Date: 2026-08-28
Branch: `dev/schema-integration`
Base clean head before this closure: `907f3dd90b675d57faabbd8a42a9313d2f7f5ecd`

## Completed document

`VRS_V2.4` - VDV-Schrift 301-2-12 VideoRecordingService V2.4, 01/2023.

Official PDF pin:

```text
SHA-256: d1a3cf36b4a9719ff8d233a84ade34ed7ff9c3dccb58f8a8688727d82a568a7b
size: 1,036,423 bytes
pin run: 33206809886
```

Pinned-byte visual evidence:

```text
render run: 33207026201
pages: 6,19,20,21,22,23,27,28
artifact digest: sha256:a81fa9b51ae3cc63fc00548e55308551754b6d17bb81c49d7272dcc24a277593
```

Status after closure: `needs_visual_review` because targeted material pages are visually confirmed but an all-page/all-figure visual pass is not complete.

## Authority split

The V2.4 PDF is official public VDV documentation.

The checked V2.4 XSD remains candidate/integration material from upstream PR #27:

```text
PR: VDVde/VDV301#27
state: open
merged: false
head: 0aa728aab47a7f13b6f36da415581d51592c4ca7
service XSD blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
dependencies: IBIS-IP_common_V2.0.xsd + IBIS-IP_Enumerations_V2.0.xsd
```

No candidate authority was promoted and no upstream action was taken.

## Version-history result

The official V2.4 history explicitly states:

```text
Functional Upgrade: None
Technical corrections:
- Fixed Copy/Paste-Error at Subscribe-methods
- clarified issues at GetVideoRecordingState
```

Fresh visual review confirms both corrections, but also confirms that several unrelated older defects remain.

## Finding history

```text
VRS-002 remains: official-PDF / candidate-XSD authority gap
VRS-003 V2.4 documentation corrected; candidate aligns; official V2.0 remains unchanged
VRS-004 corrected in V2.4
VRS-005 persists as exact typo-like PDF/XSD identifier
VRS-006 remains corrected
VRS-007 persists as outer VideoRecordingState -1:1
VRS-008 persists: StopRecording prose says StopRecordingERM
VRS-009 VideoLive v1.1 reference persists; VideoDisplay portion deferred
```

New findings:

```text
VRS-010 PauseRecordingRRM request table caption says response structure + shortened wrong name
VRS-011 VideoRecordingStateStructure table describes itself as PauseRecordingRRM request data
```

No resolver aliases are created from these documentation errors.

## Repository changes intended in closure

```text
docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.4.md
audit_registry/deep_read_findings_delta_vrs_v24_2026-08-28.json
audit_registry/deep_read_registry_delta_vrs_v24_2026-08-28.json
docs/pdf_xsd_semantic_audit/VIDEO_RECORDING_SERVICE_V24_FINDINGS_REGISTER_ADDENDUM.md
00_START_HERE/CURRENT_STATE.json
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VRS_V24_DEEP_READ_2026-08-28.md
```

No XSD file belongs in this closure commit.

## Next document

`VDS_V1.0`.

Required order:

1. Byte-pin the official VDS V1.0 PDF.
2. Fresh-read the V1.0 writing independently.
3. Resolve the deferred `VideoDisplayService v1.1` reference label from VLS/VRS.
4. Establish exact historical VDS V1.0 XSD availability/provenance before mapping any schema.
5. Only after that, compare later VDS V2.0 findings and EV-103 in their exact authority context.
6. Use the pinned-byte renderer if the interactive screenshot backend returns cache miss.

Standing rules remain unchanged: no `master` modification, no PR/comment/merge/upstream changes without explicit user approval, no XSD modification merely because PDF and XSD differ, and no latest-XSD-wins routing.
