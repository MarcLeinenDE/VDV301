# Finding revalidation — VDV 301-2 Base V2.0

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy entries: `DR3012V20-001` … `DR3012V20-008`. The frozen inventory remains exactly **192 entries**. This is the Base V2.0 subblock of the larger `VDV301-2` revalidation block.

## Evidence

- Evidence gate: **EV-130**, closure workflow run **33781049413**; independently pinned successful evidence run **33780668141**.
- Official VDV301-2 Base V2.0 PDF SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, size `2374295` bytes.
- EV-130 visual artifact: **9903434312**, digest `sha256:d5e003a68cce78cff35882a98cd418876482e80a87ff3f8975fc30d5e1970b1c`.
- Targeted visible pages: 21, 33, 34, 90, 92, 93, 98, 100, 101, 102, 105, 110.
- External primary authorities: RFC 2927, RFC 3927 and RFC 2782.
- Exact official `VDV-301-2.0` XSD blobs: SystemDocumentation `ab959dddbfa2b8ca420af1b079501f94cff38051`, DeviceManagement `74189e0da65563eeb084ec2f3c400e9668d1ee1a`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`, Enumerations `27e3c183b00381d959622d13c10543123af8eef6`.
- SystemManagement remains historical V1.0 in this release family: `2d32630a0f1981e980e6a466e3f6a69136410f24`.
- Root XSD pool regression gate rerun after EV-130.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DR3012V20-001 | `context_verified` | German ZeroConf text uses RFC 3927 while the English translation still cites RFC 2927 for the same 169.254 link-local behavior; the bibliography points to RFC 3927. |
| DR3012V20-002 | `context_verified` | Both languages state that lower SRV Weight is preferred; RFC 2782 defines proportional selection with larger Weight receiving higher probability. |
| DR3012V20-003 | `executable_confirmed` | Version history claims correction to `HeartbeatInterval`, but both visible tables still print `HertbeatIntervall`. Exact V2.0 XSD uses `HeartbeatInterval` as `IBIS-IP.duration` in both structures. `PT5S` validates; numeric `5.5` and both stale aliases reject. |
| DR3012V20-004 | `context_verified` | Correct SystemDocumentation heading is followed by narrative typo `SystemDocumenationService`; exact XSD uses `SystemDocumentationService`. |
| DR3012V20-005 | `context_verified` | SystemManagement introduction visibly contains unresolved chapter-range placeholders in German and English. |
| DR3012V20-006 | `context_verified` | Operation inventory includes `SubscribeDeviceInformation`, but the detailed subsection sequence omits a dedicated heading; full-text disproof search confirms no such heading exists while generic subscription context remains. |
| DR3012V20-007 | `context_verified` | `GetDeviceConfiguration` prose describes setting the parameter; the following `SetDeviceConfiguration` is the actual setter and the exact DMS XSD preserves getter/setter direction. |
| DR3012V20-008 | `context_verified` | `GetDeviceInformationResponseStructure` and its response data are visibly described as request structures; exact DMS XSD confirms they are response structures. |

## Executable HeartbeatInterval boundary

The authoritative V2.0 identifier is exactly `HeartbeatInterval`; both SystemDocumentation structures use `IBIS-IP.duration`. No alias is introduced for V1.0 `HeartbeatIntervall` or PDF-stale `HertbeatIntervall`.

## Closure

- Frozen legacy terminal count: **75 / 192**
- Frozen legacy pending count: **117 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next top-level revalidation block: **VDV301-2**
- Next VDV301-2 subblock: **VDV301-2 Base V2.1** (`DR3012V21-…`)
