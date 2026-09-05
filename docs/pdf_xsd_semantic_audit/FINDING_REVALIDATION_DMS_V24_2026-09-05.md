# Finding revalidation — DMS V2.4 deep-read finding

Status: **completed** on 2026-09-05 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen finding: `DRDMS24-001`. The frozen inventory remains exactly **192 entries**. The previously closed legacy `DMS` and `DMS_V2.2` blocks remain unchanged.

## Authority and evidence

- Byte-pinned official DMS V2.4 PDF: SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`, 1298127 bytes, 35 pages.
- The PDF is official public VDV writing.
- The repository DMS V2.4 XSD family remains explicitly **candidate/integration** and is not promoted to official release authority.
- Candidate DMS V2.4 blob: `d222dfd98b2be3777576388da7ace8f333d24c3f`.
- Candidate Common V2.4 blob: `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`.
- Candidate Enumerations V2.4 blob: `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`.
- `latest_xsd_wins=false`.
- Preserved **EV-108** was rerun unchanged and passed as corroborating structure context only.
- Current evidence: **EV-142**, closure run **33976613628**; pinned successful evidence run **33976298388**, artifact **9972412891**.
- Original PDF pages 1, 3 and 4 were rendered and visibly inspected. Pages 1 and 3 establish `DeviceManagementService V2.4` document identity. Page 4 visibly states in German and English that the document describes `HtmlDisplayService`; the English paragraph additionally carries its URL/web-server/HTML-display purpose.
- Active disproof attempt: the hypothesis that `HtmlDisplayService` is merely a related-service reference is rejected by the visible document-identity language plus copied service-purpose prose.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Result |
|---|---|---|
| DRDMS24-001 | `context_verified` | The DMS V2.4 foreword visibly contains copied HtmlDisplayService identity/purpose text despite the publication being DeviceManagementService V2.4. This is documentation-only and creates no HTMLDisplay route, alias or XML validation rule for DMS. |

Executable XML accept/reject evidence is not applicable to the defect itself because the erroneous foreword does not define XML validity; the candidate XSD execution is supporting service-identity context only.

## Closure

- Frozen legacy terminal count: **101 / 192**
- Frozen legacy pending count: **91 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Existing legacy DMS block mutation: **none**
- Existing DMS V2.2 block mutation: **none**
- DMS deep-read revalidation family: **complete through V2.4**
- Next revalidation block: **DOOR**
- Next subblock: **DOOR V2.1** (`DRDOOR21-001..002`)
