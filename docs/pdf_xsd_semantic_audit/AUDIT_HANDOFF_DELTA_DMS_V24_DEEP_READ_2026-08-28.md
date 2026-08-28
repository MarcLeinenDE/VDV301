# Audit Handoff Delta - DMS V2.4 Deep Read

Date: 2026-08-28
Branch: `dev/schema-integration`

This delta supplements the current audit handoff and records only the changes from the DMS V2.4 Deep Read block.

## Source provenance

Official public PDF:

```text
source_id: DMS_V2.4
VDV-Schrift: 301-2-0 DeviceManagementService V2.4
SHA-256: 347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd
size: 1298127 bytes
pin run: 33182486754
```

The V2.4 XSD stored in `dev/schema-integration` remains candidate/integration authority. Do not relabel it as an official release XSD.

## Deep Read result

Textual fresh read is complete. Critical visible-page requests returned cache-miss, therefore state is `needs_visual_review`, not `exhaustive_read`.

Fresh comparison was performed before opening the pre-existing `02_dms_v2_4_pdf_xsd_audit.md` report.

## Finding history

```text
DMS-003  V2.4 correction confirmed: ErrorMessage 0:*; never back-apply to V2.2.
DMS-004  V2.4 correction confirmed: InstallUpdate ID/Timestamp/URL optional; never back-apply.
DMS-005  persists in V2.4 PDF vs candidate/integration XSD response-data spelling.
DMS-006  resolved/aligned for checked V2.4 profile; historical V2.2 mismatch remains valid.
DMS-007  persists: GetUpdateStates PDF wording vs GetUpdateHistory operation/XSD.

DRDMS22-001  resolved in V2.4.
DRDMS22-002  resolved in V2.4.
DRDMS22-003  persists; executable enum remains InstallationSuccessful.
DRDMS22-004  persists.
DR3012V20-007 persists.
DR3012V20-008 persists.

DRDMS24-001 new:
V2.4 DMS foreword incorrectly describes HtmlDisplayService in both language sections.
```

## Executable evidence

```text
EV-108
run: 33182963733
head tested: 1ea19f21c630b5f111fc8e41e6e39479e2b1c97f
result: PASS
authority: candidate/integration DMS V2.4 XSD
```

EV-108 confirms the candidate-XSD side of DMS-005/DMS-006/DMS-007 and the corrected V2.4 cardinalities/optionality.

The workflow was restored to manual-only in commit:

```text
4b738d837edf0cb4ee01acada1afe95621e99f1e
Restore manual-only audit workflow after EV-108
```

## Safety

```text
No XSD changed.
No master change.
No PR/comment/review/merge action.
No candidate XSD promoted to official authority.
No visual closure claimed where rendering failed.
```

## Next Deep Read target

Recommended next target: `TIME_V1.0` / VDV 301-2-10 TimeService V1.0.

Reason:

```text
- intentionally non-XSD service, so it exercises the protocol/discovery audit lane;
- current Deep Read finding DR3012-006 still needs historical resolution of the old 301-2-11 TimeService cross-reference context;
- deterministic TimeService/SNTP profile already exists as RV-003 and can be compared only after an independent PDF fresh read.
```

Sequence:

```text
1. byte-pin official TIME_V1.0 PDF;
2. fresh-read PDF without using old findings/RV-003 as a template;
3. resolve historical 301-2-10 vs 301-2-11 numbering evidence;
4. only then compare with DR3012-006 and RV-003;
5. retain non-XSD authority lane; do not synthesize XML schemas/operations.
```
