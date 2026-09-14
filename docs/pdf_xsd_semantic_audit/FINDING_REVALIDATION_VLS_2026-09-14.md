# Finding revalidation — VideoLiveService (VLS)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `VLS-001` through `VLS-005`. Frozen inventory remains exactly **192 entries**.

## Evidence

- Aggregate evidence: **EV-165**; closure run **34840162307**.
- Successful EV-165 validation run: **34839986276**, job **103962447178**, artifact **10345886539**, digest `sha256:20d85319cc0d8014102abaf9ce6bf985c5510d59d631403030f172be5c5c90b7`, head `b22d3d2840b68b62f5135ba8a583dc5fe63e496f`.
- Underlying executable compositor evidence: **EV-103**, run `33111119723`, job `98653897734`, artifact `9662552176`.
- VLS V1.0 PDF: official byte pin `f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c`; visual runs `33202961159`, `33203162588`.
- VLS V2.0 PDF: official byte pin `d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b`; visual run `33203850390`.
- Official V2.0 XSD authority: `VDV-301-2.0` / commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08`; VLS blob `d8c52f5de9ef3f5915524fef12da11eabf0ca041`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`, Enums `27e3c183b00381d959622d13c10543123af8eef6`.
- Complete regression pool: **50 root XSDs — PASS**.

## Terminal decisions

| Finding | State | Decision |
|---|---|---|
| VLS-001 | `context_verified` | The provenance gap itself is verified: the official V1.0 publication exists, but no exact official V1.0 VideoLiveService service XSD is confirmed in the checked release route. V2.0 is not substituted. |
| VLS-002 | `executable_confirmed` | Official V2.0 PDF presents a multi-field `LiveStreamData`; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |
| VLS-003 | `context_verified` | V1.0 German foreword visibly uses the wrong part number `301-2-1`; V2.0 corrects it to `301-2-11`. Documentation-only. |
| VLS-004 | `context_verified` | VideoLive start/stop prose visibly substitutes `VideoDisplayService`; the error persists into V2.0. No alias/routing rule is inferred. |
| VLS-005 | `context_verified` | Corrected finding only: leading-minus notation is valid VDV XML-choice notation. The surviving issue is incomplete/ambiguous application in the checked VLS tables. |

## Authority boundaries

- VLS V1.0 remains documentation authority only because no exact strict V1.0 service-XSD route is confirmed.
- VLS V2.0 executable conclusions use the exact official release-tag XSD family only.
- `VLS-005` must always be read through the 2026-08-29 choice-notation correction overlay.
- Runtime RTSP/RTP behavior remains outside XML/XSD validation except where separately established by runtime evidence.

## Closure

Prestate: **176 terminal / 16 pending**.

Poststate: **181 terminal / 11 pending**.

Next finding: **`VRS-001`**. Next block: **VRS**.

No XSD mutation. No frozen-inventory mutation.
