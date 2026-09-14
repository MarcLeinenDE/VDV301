# Finding revalidation — VideoRecordingService (VRS)

Status: **final finding block completed** on 2026-09-14 under the current Evidence Gate.

## Scope and evidence

Frozen findings: `VRS-001` through `VRS-011`. EV-166 successful validation run **34840970136**, job **103965628772**, artifact **10346331279**, digest `sha256:da205bc769db11a5406a11de1c2febeb6c38745924d51835fe7a22b6fd978309`, head `8bcfbbc3e93fcc1bfc41e422cd5a83790ed99e9f`. Closure run: **34841174977**. EV-103 is the executable V2.0 compositor evidence for `VRS-003`. All **50 root XSDs PASS**.

V1.0/V2.0/V2.4 official PDFs were reacquired byte-identically. V2.0 uses the exact official `VDV-301-2.0` XSD family. V2.4 XSD remains open, unmerged PR #27 candidate/integration evidence only.

## Terminal decisions

| Finding | State | Decision |
|---|---|---|
| VRS-001 | `context_verified` | Official V1.0 PDF exists; no exact official V1.0 VRS service-XSD release route is confirmed. No nearby version is substituted. |
| VRS-002 | `context_verified` | Official V2.4 PDF vs open/unmerged PR #27 candidate-XSD authority gap is confirmed. |
| VRS-003 | `executable_confirmed` | Official V2.0 PDF/XSD compositor mismatch remains; EV-103 confirms accepted/rejected shapes. |
| VRS-004 | `context_verified` | Wrong SubscribeDisplayState headings persist through V2.0 and are corrected in V2.4. |
| VRS-005 | `context_verified` | `PauseRecordingRRMRequestStruture` is a shared exact PDF/XSD typo-like identifier, not a mismatch; executable spelling must not be normalized. |
| VRS-006 | `context_verified` | Broken generated subscription references are present in V1.0 and corrected from V2.0 onward. |
| VRS-007 | `withdrawn` | The premise was false: leading `-` is valid VDV XML-choice notation. The correction overlay supersedes older Deep-Read wording. |
| VRS-008 | `context_verified` | StopRecording prose says StopRecordingERM through V2.4; no such alias is created. |
| VRS-009 | `context_verified` | Neighboring VLS/VDS `v1.1` reference labels are cross-document documentation errors. |
| VRS-010 | `context_verified` | Pause request table caption has wrong role/name across all checked VRS PDFs. |
| VRS-011 | `context_verified` | V2.4 VideoRecordingStateStructure table has a copy/paste role description error. |

## Final frozen-inventory state

Prestate: **181 terminal / 11 pending**.

Poststate: **192 terminal / 0 pending**. There is no next revalidation block.

The frozen inventory is fully terminalized, but SDK finding-knowledge readiness is **not promoted yet**: `CIS-001` remains the sole terminal `unresolved` finding and receives a separate readiness reconciliation because the plan requires zero unresolved finding that could alter SDK accept/reject/routing behavior.

No XSD mutation. No frozen-inventory mutation.
