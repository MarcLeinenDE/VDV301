# VideoRecordingService V2.4 findings register addendum

Status: Deep Read Pass 2 completed for `VRS_V2.4`.

Authority boundary:

```text
Official V2.4 PDF authority: public VDV writing 301-2-12 V2.4
Candidate/integration XSD authority only: upstream PR #27
PR #27 state during recheck: open, not merged
PR head: 0aa728aab47a7f13b6f36da415581d51592c4ca7
candidate VRS V2.4 blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
candidate dependencies: Common V2.0 + Enumerations V2.0
```

The public V2.4 writing does not promote the candidate XSD to official release authority.

## VRS-002

Authority/provenance gap remains. The V2.4 PDF is official; the checked V2.4 service XSD remains candidate/integration material from open PR #27.

## VRS-003

V2.4 documentation corrects the former flat response model. The visible response now contains alternatives `VideoRecordingState` / `OperationErrorMessage`, while nested `VideoRecordingStateStructure` contains `State`, optional `AlarmArchiveFillLevel`, and optional `StartStopMode` together. The PR27 candidate XSD models the same correction.

This is V2.4 alignment evidence only. Official V2.0 behavior and EV-103 remain unchanged.

## VRS-004

Corrected in V2.4. Visible headings are now `SubscribeVideoRecordingState` and `UnsubscribeVideoRecordingState`, matching the explicit version-history statement that Subscribe copy/paste errors were fixed.

## VRS-005

Persists. Visible V2.4 operation table and candidate XSD both use the typo-like exact identifier `PauseRecordingRRMRequestStruture`. It remains PDF/XSD-consistent, not a PDF/XSD mismatch. Do not silently normalize it in candidate-profile code generation or routing.

## VRS-006

Remains corrected. The generated Word cross-reference failures seen in V1.0 do not return in the checked V2.4 subscription prose.

## VRS-007

Not fully corrected. Nested state cardinalities are now plausible (`State 1:1`, `AlarmArchiveFillLevel 0:1`, `StartStopMode 0:1`), but the outer `VideoRecordingState` row still visibly prints malformed `-1:1` notation.

## VRS-008

Persists. The `StopRecording` request prose still says `StopRecordingERM`; neither operation inventory nor candidate XSD defines such an operation. No alias is created.

## VRS-009

The VideoLive reference inconsistency persists through V2.4: German says `VideoLiveService v1.0`, English says `VideoLiveService v1.1` for VDV 301-2-11 / 05-2017. The dedicated VLS V1.0 Deep Read establishes the service as V1.0.

The adjacent VideoDisplayService `v1.1` label remains deferred to the dedicated `VDS_V1.0` Deep Read.

## VRS-010 - Pause request table caption role/name error

```text
classification: pdf_table_caption_structure_name_error_candidate
state: visually_confirmed_cross_version
confidence: very_high
scope: VRS V1.0, V2.0, V2.4
```

The PauseRecordingRRM request table caption says:

```text
Description of response structure VideoRecordingService.PauseRecordingRequest
```

although the table describes the request for operation `PauseRecordingRRM` and its logical structure is `PauseRecordingRRMRequest`.

The defect is visible in V1.0 page 45, V2.0 page 20 and V2.4 page 22.

Do not create a `PauseRecordingRequest` alias from this caption.

## VRS-011 - VideoRecordingStateStructure table role copy/paste error

```text
classification: pdf_table_role_copy_paste_error_candidate
state: visually_confirmed
confidence: very_high
scope: VRS V2.4
```

Visible V2.4 page 20 describes `VideoRecordingStateStructure` as:

```text
Request data structure for operation PauseRecordingRRM
```

but the table is the nested state structure used by the corrected VideoRecording state response. PR27 candidate XSD independently confirms this response role.

No second PauseRecording request structure is inferred from the prose.

## V2.4 version-history evidence

Visible page 27 records:

```text
Functional Upgrade: None
Technical corrections:
- Fixed Copy/Paste-Error at Subscribe-methods
- clarified issues at GetVideoRecordingState
```

The audit applies these claims only where the visible V2.4 document actually confirms them; other historical findings are checked independently.

## Visual evidence

```text
source SHA-256: d1a3cf36b4a9719ff8d233a84ade34ed7ff9c3dccb58f8a8688727d82a568a7b
source size: 1,036,423 bytes
pin run: 33206809886
render run: 33207026201
pages: 6, 19, 20, 21, 22, 23, 27, 28
artifact digest: sha256:a81fa9b51ae3cc63fc00548e55308551754b6d17bb81c49d7272dcc24a277593
```

Targeted material findings are visually confirmed. An all-page/all-figure pass is not complete, so the document remains `needs_visual_review`.
