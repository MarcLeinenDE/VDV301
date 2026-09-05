# Finding revalidation — COMMON V2.4

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy finding: `DRCOM24-001`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V2.4 PDF: SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1689647 bytes.
- Selected XSD authority is **candidate/integration**, not an official V2.4 release.
- No `VDV-301-2.4` release tag is claimed.
- Candidate branch: `candidate/dms-v2.4-xsd`; upstream draft provenance: `VDVde/VDV301#31`.
- Selected Common V2.4 blob: `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`.
- Selected Enumerations V2.4 blob: `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`.
- `latest_xsd_wins=false`; authority remains the explicitly selected frozen candidate route.
- Frozen observation mapping: `FR-COM24-008` -> `DRCOM24-001`.
- Preserved base evidence **EV-122** was rerun unchanged and passed.
- Current revalidation evidence: **EV-140**, closure run **33973935324**; pinned visual/evidence run **33858121693**, artifact **9931012948**.
- Page 28 was selected from the exact PDF by the complete `LineInformation`/`LineName`/`LineShortName` table anchors, rendered, and visibly inspected.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM24-001 | `executable_confirmed` | PDF page 28 visibly documents `LineName` and `LineShortName` as `IBIS-IP.string 0:1`. The selected candidate V2.4 XSD declares both `InternationalTextType 0:*`. Preserved EV-122 confirms candidate InternationalText shapes and repetition as valid and rejects the PDF-derived simple value-only LineName shape. |

This terminal state is explicitly scoped to `selected_candidate_integration_V2.4_only_until_official_release_exists`; it must not be relabelled as an official VDV-301-2.4 release conclusion.

## Closure

- Frozen legacy terminal count: **96 / 192**
- Frozen legacy pending count: **96 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- COMMON revalidation family: **complete through V2.4**
- Next revalidation block: **DMS**
- Next subblock: **DMS V2.2** (`DRDMS22-001..004`)
