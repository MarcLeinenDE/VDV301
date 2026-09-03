# Finding revalidation — VDV 301-2 Base V2.1

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy entry: `DR3012V21-001`. The frozen inventory remains exactly **192 entries**. Persistent older Base-Service findings are not duplicated here; this closure changes only the V2.1-specific frozen finding.

## Evidence

- Evidence gate: **EV-131**, closure workflow run **33781657200**; independently pinned successful evidence run **33781385699**.
- Official VDV301-2 Base V2.1 PDF SHA-256: `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, size `2671005` bytes.
- EV-131 visual artifact: **9903719333**, digest `sha256:b0fdcb3705e5e95158545d099845184a1effe9b57647011881bb35fdf94df2d8`.
- Targeted visible pages: 59, 60, 69, 70, 75, 76.
- Exact official VDV-301-2.1 mixed route: DMS 2.1 `191b43e01cdaba14b247725689a913c244a67eed`, SystemDocumentation 2.0 `ab959dddbfa2b8ca420af1b079501f94cff38051`, SystemManagement 1.0 `2d32630a0f1981e980e6a466e3f6a69136410f24`.
- DMS 2.1 dependencies are Common 2.1 `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` and Enumerations 2.1 `311464690ad60749ed8d326217787e4b8ed0b718`.
- Root XSD pool regression gate rerun after EV-131.

## Terminal state

| Finding | Terminal state | Result |
|---|---|---|
| DR3012V21-001 | `context_verified` | Base V2.1 prose repeatedly routes DeviceManagementService to `VDV 301-2-2` and SystemDocumentationService to `VDV 301-2-4`. The official source catalog assigns 301-2-2 to BeaconLocationService and 301-2-4 to DistanceLocationService, while the exact VDV-301-2.1 release tag directly supplies the mixed DMS/SystemDocumentation/SystemManagement schema family. The prose numbers are stale and must not drive schema routing. |

## Evidence interpretation

This is a documentation/routing defect, not an XML-validity defect. No artificial negative XML instance is created. The service XSDs are compiled to establish the exact authority route; the active disproof is the conflicting official document identity of 301-2-2 and 301-2-4.

V2.1 also visibly fixes some V2.0-only issues (for example the missing SubscribeDeviceInformation subsection), while other earlier defects persist. Those histories remain attached to their existing finding IDs and are not counted again in this subblock.

## Closure

- Frozen legacy terminal count: **76 / 192**
- Frozen legacy pending count: **116 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next top-level revalidation block: **VDV301-2**
- Next VDV301-2 subblock: **General Conventions V2.2**
