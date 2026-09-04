# Finding revalidation — VDV 301-2 General Conventions V2.4

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen V2.4-specific entries: `DR3012GC24-001` … `DR3012GC24-005`. The frozen inventory remains exactly **192 entries**. Older findings that recur in V2.4 are context evidence only and are not counted a second time.

## Evidence

- Evidence gate: **EV-134**, closure workflow run **33844432985**; pinned successful evidence run **33843888080**.
- Official GC V2.4 PDF SHA-256: `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d`, size `1767094` bytes.
- EV-134 artifact: **9925822375**, digest `sha256:f69b3f678b5f9153aac90c03a1995d1ece7941e5c3db45ec96a55537f16731a2`.
- All finding pages were rendered at 180 dpi and visually inspected before closure.
- Selected V2.4 schema authority remains explicitly **candidate/integration**, not an official release tag: Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, Enumerations blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, provenance `VDVde/VDV301#31`.
- Root XSD pool regression gate and tracked-mutation guard passed.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DR3012GC24-001 | `executable_confirmed` | German PDF uses `OnBordUnit`; English and selected `DeviceClassEnumeration` use `OnBoardUnit`. Positive/negative validation confirms only `OnBoardUnit`. |
| DR3012GC24-002 | `context_verified` | German numbering duplicates `2.1.1` for IP addresses and subnet masks/gateways; English uses `2.1.1` / `2.1.2`. |
| DR3012GC24-003 | `context_verified` | English allowed-version-character list visibly duplicates digit `2`; this is documentation residue, not an extension of executable version syntax. |
| DR3012GC24-004 | `executable_confirmed` | Multiple typo-like service identifiers are visible in examples/glossary, while selected `ServiceNameEnumeration` contains the correct identifiers and executable negative samples reject the typo forms. |
| DR3012GC24-005 | `context_verified` | The document states there is no common IBIS-IP version, yet later uses stale `Version 1.0 of IBIS-IP` wording. No umbrella schema version is inferred. |

## Context controls

- The V2.3 history numbering defect `DR3012GC23-001` is visibly repaired in V2.4 (`7.2.1` / `7.2.2`).
- Literal Word cross-reference errors visibly recur in V2.4. This strengthens historical `DR3012GC22-001` context but does not create or terminalize a duplicate frozen finding.
- The document explicitly states that XSD definitions take precedence over documentation when inconsistent; the audit preserves the selected XSD authority for executable spelling boundaries.

## Closure

- Frozen legacy terminal count: **84 / 192**
- Frozen legacy pending count: **108 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- VDV301-2 Base/General-Conventions revalidation sequence: **completed through V2.4**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V1.0 (`DRCOM10-001…007`)**
