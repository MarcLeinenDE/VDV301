# Finding revalidation — VDV 301-2 V1.0

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy entries: `DR3012-001` … `DR3012-007`. The frozen inventory remains exactly **192 entries**. This is the V1.0 subblock of the larger `VDV301-2` revalidation block.

## Evidence

- Evidence gate: **EV-129**, closure workflow run **33765633886**; independently pinned successful evidence run **33765167655**.
- Official VDV301-2 V1.0 PDF SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`, size `1790447` bytes.
- EV-129 visual artifact: **9897171006**, digest `sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7`.
- Targeted visible pages: 20, 22, 26, 59, 63, 65, 67, 69, 75, 80.
- External primary authorities: RFC 2927, RFC 3927 and RFC 2782.
- Exact historical SystemDocumentation V1.0 XSD blob: `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`; byte-identical to the official upstream `VDV-301-1.0` tag.
- Exact historical SystemManagement V1.0 XSD blob: `2d32630a0f1981e980e6a466e3f6a69136410f24`.
- Root XSD pool regression gate rerun after EV-129.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DR3012-001 | `context_verified` | VDV page 20 cites RFC 2927 for ZeroConf/169.254 addressing. RFC 2927 is the LDAP-schema MIME profile; RFC 3927 is the IPv4 link-local authority. |
| DR3012-002 | `context_verified` | VDV page 26 says lower SRV Weight is preferred at equal Priority; RFC 2782 defines proportional selection with larger Weight receiving higher probability. |
| DR3012-003 | `executable_confirmed` | Refined correction: PDF page 65 uses `HertbeatIntervall` + `IBIS-IP.duration`; exact XSD uses `HeartbeatIntervall`, with `IBIS-IP.double` in SystemConfigurationData and `IBIS-IP.duration` in StoreSystemConfigurationRequestStructure. Positive/negative XML tests confirm identifier and lexical-type boundaries. |
| DR3012-004 | `context_verified` | DeviceState points to 9.3 although visible section 9.4 is DeviceStateEnumeration. |
| DR3012-005 | `context_verified` | Operation inventory uses ServiceStatus names while detailed headings use SystemStatus; exact historical SystemManagement XSD supports the ServiceStatus terminology. |
| DR3012-006 | `context_verified` | Historical context resolves the TimeService reference to VDV 301-2-11 as wrong/stale, not merely a modern numbering difference. |
| DR3012-007 | `context_verified` | StopService request description visibly refers to the service to be started; retained as a copy/paste documentation defect. |

## DR3012-003 correction trail

The historical statement that `HertbeatIntervall` appears in both PDF and XSD is explicitly superseded by `docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DR3012_003_V10_IDENTIFIER_TYPE_2026-09-03.md`. The finding itself remains valid and is strengthened; no schema alias or typo normalization is introduced.

## Closure

- Frozen legacy terminal count: **67 / 192**
- Frozen legacy pending count: **125 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next top-level revalidation block: **VDV301-2**
- Next VDV301-2 subblock: **VDV301-2 Base V2.0** (`DR3012V20-001…008`)
