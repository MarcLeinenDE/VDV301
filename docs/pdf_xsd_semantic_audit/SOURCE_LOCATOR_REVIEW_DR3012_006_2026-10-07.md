# Source-locator review — DR3012-006 — 2026-10-07

Status: **complete / visible-body verified / historical source identity verified / documentation routing defect confirmed**.

## Finding

VDV 301-2 V1.0 routes the SNTP/TimeService implementation reference to `VDV 301-2-11`. Historical official-source identity shows that TimeService is part `301-2-10`, while `301-2-11` is VideoLiveService.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **22**
- visible section: **2.5 Weitere Protokolle**

The SNTP paragraph visibly ends with:

`Weitere Informationen zur Umsetzung siehe VDV 301-2-11.`

EV-129 page-22 PNG SHA-256:
`1c5e8cfab04e35ecb0e8640b5740ab788f265a8997373465bb8c659b4c53322c`

## Historical document identity

Canonical audit source registries preserve the historical V1.0 part mapping:

### TimeService

- source/document ID: `TIME_V1.0`
- VDV part: `301-2-10`
- version: `1.0`
- title: `TimeService`
- official URL filename: `301-2-10sds-v-1-01.pdfx`
- pinned SHA-256: `d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`

### VideoLiveService

- source/document ID: `VLS_V1.0`
- VDV part: `301-2-11`
- version: `1.0`
- title: `VideoLiveService`
- official URL filename: `301-2-11-sds.pdfx`
- pinned SHA-256: `f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c`

The routing defect is therefore historical as well as modern: part 301-2-11 is not the TimeService document in the V1.0 source set.

## Disproof attempt

A possible explanation would be that the number changed only in later releases. The historical V1.0 registry/pin evidence disproves that explanation:

- TimeService V1.0 is already identified as 301-2-10;
- VideoLiveService V1.0 is already identified as 301-2-11.

Thus the page-22 reference is genuinely wrong/stale for the historical context being audited.

## Classification and SDK behavior

Confirmed documentation/source-routing defect.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable**
- runtime matcher: **not applicable**
- SDK behavior: **warning / provenance guidance**
- no protocol rule is synthesized from the wrong part number.

Service/document routing must come from exact version-specific source provenance, not from this stale cross-reference.
