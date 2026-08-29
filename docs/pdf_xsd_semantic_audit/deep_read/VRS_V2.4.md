# Deep Read - VideoRecordingService V2.4

Document id: `VRS_V2.4`

Status: `needs_visual_review`

Fresh-read date: 2026-08-28

## 1. Source and provenance

Official public writing:

```text
VDV-Schrift 301-2-12
VideoRecordingService - V2.4
01/2023
https://www.vdv.de/301-2-12-sdg-v2.4-videorecordingservice.pdfx
```

Byte pin:

```text
SHA-256: d1a3cf36b4a9719ff8d233a84ade34ed7ff9c3dccb58f8a8688727d82a568a7b
size:    1,036,423 bytes
pin run: 33206809886
```

No VDV PDF bytes or rendered page images are committed to the repository.

## 2. Authority boundary

The V2.4 PDF is an official public VDV writing.

The checked V2.4 XSD is not an official release-tag XSD. It comes from open upstream PR #27:

```text
VDVde/VDV301#27
state: open
merged: false
head: 0aa728aab47a7f13b6f36da415581d51592c4ca7
service XSD blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
```

The candidate service XSD includes exactly:

```text
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

Therefore:

```text
V2.4 PDF authority = official public writing
V2.4 XSD authority = candidate/integration only
```

The official PDF does not promote the candidate XSD to official release authority.

## 3. Independent-read order

The V2.4 writing was read first from its own official PDF. The candidate XSD and existing EV-103 candidate control were consulted only after the PDF corrections and remaining documentation defects were established independently.

## 4. Visual evidence

Pinned-byte fallback render:

```text
run: 33207026201
pages: 6, 19, 20, 21, 22, 23, 27, 28
resolution: 180 dpi
artifact digest: sha256:a81fa9b51ae3cc63fc00548e55308551754b6d17bb81c49d7272dcc24a277593
```

Targeted material pages are visually confirmed. An all-page/all-figure pass is not complete, so the document remains `needs_visual_review`.

## 5. Explicit V2.4 version history

Visible page 27 states:

```text
Functional Upgrade:
None

Technical Upgrade/Corrections:
- Copy/Paste-Fehler bei den Subscribe-Methoden behoben
  / Fixed Copy/Paste-Error at Subscribe-methods
- Unklarheiten bei der Antwort des GetVideoRecordingState bereinigt
  / clarified issues at GetVideoRecordingState
```

These statements are used as explicit correction history, but only for the items they actually describe. Other historical findings are checked separately rather than assumed corrected.

## 6. Operation inventory

Visible page 19 lists the same operation family:

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

The Pause request row still visibly names:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

The candidate XSD uses the same exact spelling.

## 7. VRS-003 - response model structurally corrected in V2.4 documentation/candidate

V1.0 and V2.0 public writings described one flat state response containing State, AlarmArchiveFillLevel, OperationErrorMessage and StartStopMode together. Official V2.0 XSD instead put those four fields in one `xs:choice`, which EV-103 proved rejects the PDF-shaped grouped response.

Visible V2.4 pages 20-21 change the documentation model.

Outer response table now contains alternatives:

```text
VideoRecordingState
OperationErrorMessage
```

The nested `VideoRecordingStateStructure` contains:

```text
State                   1:1
AlarmArchiveFillLevel   0:1
StartStopMode           0:1
```

The candidate V2.4 XSD models the same structure:

```text
VideoRecordingStateResponseStructure
  xs:choice
    VideoRecordingState -> VideoRecordingStateStructure
    OperationErrorMessage

VideoRecordingStateStructure
  xs:sequence
    State                  required
    AlarmArchiveFillLevel  optional
    StartStopMode          optional
```

Thus the V2.4 public documentation and candidate XSD are structurally aligned on the correction of the V2.0 flat-choice problem.

Authority guard:

```text
This does not make the candidate XSD official.
It is candidate/integration evidence that matches the official V2.4 writing's corrected model.
Official V2.0 behavior remains unchanged.
```

EV-103's candidate control already demonstrated that a grouped V2.4 state sample validates against the candidate schema.

## 8. VRS-004 - Subscribe headings corrected

Visible V2.4 page 23 headings are now:

```text
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

This matches the operation inventory and directly implements the version-history statement that Subscribe copy/paste errors were fixed.

History:

```text
V1.0: wrong SubscribeDisplayState/UnsubscribeDisplayState headings
V2.0: wrong headings persist
V2.4: corrected
```

## 9. VRS-005 - `PauseRecordingRRMRequestStruture` persists

Visible V2.4 page 19 still uses:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

The PR #27 candidate XSD uses the same type spelling.

Therefore the prior clarification remains:

```text
shared typo-like PDF/XSD identifier
not a PDF/XSD mismatch
exact spelling is required when the candidate profile is explicitly selected
```

## 10. VRS-006 - broken generated subscription references remain corrected

The V1.0 Word-generated broken references were already absent in V2.0.

Visible V2.4 page 23 continues with normal prose using SubscribeRequest/SubscribeResponse and UnsubscribeRequest/UnsubscribeResponse.

History:

```text
V1.0: present
V2.0: corrected
V2.4: remains corrected
```

## 11. VRS-007 - malformed `-1:1` notation persists but moves

V1.0/V2.0 printed malformed `-1:1` values directly on `State` and `StartStopMode`.

V2.4 corrects the nested state structure cardinalities to:

```text
State                  1:1
AlarmArchiveFillLevel  0:1
StartStopMode          0:1
```

However visible page 20 still prints:

```text
VideoRecordingState  -1:1
```

in the outer response table.

Therefore `VRS-007` is not fully corrected; the malformed notation persists at a different structural level.

No intended replacement value is guessed. If the candidate XSD is explicitly selected, its actual XSD occurrence rules remain executable authority.

## 12. VRS-008 - StopRecordingERM persists despite V2.4 corrections

Visible page 23 still says:

```text
No additional data must be given by execution of operation StopRecordingERM.
```

The section and operation inventory use `StopRecording`; the candidate XSD also declares `StopRecordingResponse` and no `StopRecordingERM` operation.

Thus `VRS-008` persists through V2.4 and was not one of the two corrections claimed in the version history.

No alias is created.

## 13. VRS-009 - VideoLiveService v1.1 reference persists

Visible page 28 still shows for VDV 301-2-11:

```text
German:  VideoLiveService v1.0, 1.0, 05/2017
English: VideoLiveService v1.1  1.0, 05/2017
```

The dedicated VLS V1.0 audit establishes VDV 301-2-11 as VideoLiveService V1.0 from 05/2017.

Thus the VideoLive portion of `VRS-009` persists through V2.4.

The adjacent VideoDisplayService `v1.1` reference is still deferred to the dedicated VDS V1.0 Deep Read.

## 14. VRS-010 - Pause table caption describes wrong role/name across all checked VRS PDFs

A cross-version visual comparison found the same misleading caption in V1.0, V2.0 and V2.4.

Visible examples:

```text
V1.0 page 45, Table 9
V2.0 page 20, Table 5
V2.4 page 22, Table 6
```

The table is the request structure for operation `PauseRecordingRRM`, and the table header uses `VideoRecordingService.PauseRecordingRRMRequest` as the logical structure name.

The caption instead says:

```text
Description of response structure VideoRecordingService.PauseRecordingRequest
```

This has two independent problems:

```text
request table described as response structure
PauseRecordingRRMRequest shortened to PauseRecordingRequest
```

Classification:

```text
pdf_table_caption_structure_name_error_candidate
```

Resolver rule: do not derive an operation or structure alias `PauseRecordingRequest` from this caption.

For official V2.0 validation, the exact XSD type remains `PauseRecordingRRMRequestStruture`. The candidate V2.4 XSD retains that same exact type.

## 15. VRS-011 - V2.4 VideoRecordingStateStructure table describes itself as Pause request data

The corrected V2.4 response section introduces a dedicated `VideoRecordingStateStructure` table.

Visible page 20 describes that table in its right-hand header cell as:

```text
Request data structure for operation PauseRecordingRRM
```

But the table is the nested state structure used by `VideoRecordingStateResponse`; it is not the Pause request structure.

The candidate XSD independently confirms the role:

```text
VideoRecordingStateResponseStructure
  -> VideoRecordingState
     -> VideoRecordingStateStructure
```

Classification:

```text
pdf_table_role_copy_paste_error_candidate
```

This appears to be a copy/paste artifact inside the newly clarified V2.4 response documentation. It does not create a second request structure or change candidate-XSD semantics.

## 16. Minor editorial issues not split into findings

The writing contains further low-impact spelling/grammar artifacts (`VideoReordingService`, pluralized operation prose, etc.). They are not split into individual findings because the exact operation inventory, structure tables and authority rules above already prevent those prose spellings from becoming resolver aliases.

## 17. Candidate provenance recheck

Upstream PR #27 was freshly rechecked during this Deep Read:

```text
state: open
merged: false
draft: false
head SHA: 0aa728aab47a7f13b6f36da415581d51592c4ca7
candidate service XSD blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
```

The file at the current PR head is byte-identical to the candidate copy in the integration branch.

No PR action was taken.

## 18. Fresh-read outcome

Existing finding history:

```text
VRS-002  candidate/official authority gap remains
VRS-003  corrected structurally in V2.4 PDF; candidate XSD aligns, candidate authority only
VRS-004  corrected in V2.4 exactly as version history states
VRS-005  persists
VRS-006  remains corrected
VRS-007  persists, moved to outer VideoRecordingState row
VRS-008  persists
VRS-009  VideoLive reference portion persists
```

New findings:

```text
VRS-010  Pause request table caption says response structure + wrong shortened structure name; present V1.0/V2.0/V2.4
VRS-011  V2.4 VideoRecordingStateStructure table wrongly describes itself as PauseRecordingRRM request data
```

No XSD change is made and candidate authority is not promoted.

## 19. Completion status

```text
textual fresh read: complete
exact PDF source pin: complete
targeted visual checks: complete
V2.4 version-history verification: complete
candidate PR provenance recheck: complete
candidate PDF/XSD structural comparison: complete after independent PDF read
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned document: `VDS_V1.0`, where the deferred VideoDisplayService `v1.1` reference label from VLS/VRS documents will be resolved against the dedicated VideoDisplay source history.