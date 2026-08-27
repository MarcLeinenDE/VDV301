# PDF/XSD semantic audit index

Status: started.

Branch:

```text
dev/schema-integration
```

Purpose:

This audit tracks a source-based comparison between the public VDV 301 PDF writings and the XSD files present in the integration branch.

Important limits:

- This is not an official VDV statement.
- Files from open PRs, forks, or local candidates stay labelled as candidate/integration material until accepted upstream or published by VDV.
- Semantic PDF/XSD checks are performed in small, traceable blocks.
- Local XSD compilation and sample XML validation remain a later technical validation step.

## Audit files

```text
00_index.md
01_common_enums_v2_1_to_v2_4.md
findings.md
validation_backlog.md
```

## Status overview

| Area | Status | Notes |
|---|---|---|
| Common structures / enumerations V2.1-V2.4 | started | Version-history deltas are being mapped to XSD evidence first. |
| Common structures / enumerations V1.0-V2.0 | pending | Needs older PDF/table extraction and XSD comparison. |
| DeviceManagementService | pending | DMS V2.4 candidate already has a separate derivation document; needs integration into this audit format. |
| TicketValidationService | pending | Must account for upstream V2.4 include state and open PR/candidate material. |
| CustomerInformationService | pending | Coverage and provenance unclear for older versions. |
| Remaining services | pending | To be split into small blocks after Common/Enums. |

## Evidence policy

Each finding should distinguish:

```text
PDF-derived fact
XSD-derived fact
inference / audit interpretation
open validation task
```

Finding states:

```text
OK
OK with note
Mismatch
Unclear
Not checked yet
```
