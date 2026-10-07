# Source-locator review — DR3012-005 — 2026-10-07

Status: **complete / visible-body verified / exact official XSD context verified / documentation terminology defect confirmed**.

## Finding

VDV 301-2 V1.0 is inconsistent about the SystemManagement service-status subscription terminology.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`

### Page 67 — operation inventory

Visible section:
- `7.3.1 Operationen des SystemManagementService`
- `Tabelle 31 Beschreibung von Operationen des SystemManagementService`

The visible operation names include:
- `GetServiceStatus`
- `SubscribeServiceStatus`
- `UnsubscribeServiceStatus`

EV-129 page-67 PNG SHA-256:
`2241db5cef5651ee67e2fd80bd1db142df53b00ed13c5817f8c67139c4770bfe`

### Page 69 — detailed subscription headings

The visible detailed headings are:
- `7.3.6 Datenstrukturen der Operation SubscribeSystemStatus`
- `Datenstrukturen der Operation UnsubscribeSystemStatus`

EV-129 page-69 PNG SHA-256:
`11f732afa98020a4256af71aa1063ac06fc55312e5853538f4efe89dcb8b4656`

Thus the same document uses `ServiceStatus` in the operation inventory and `SystemStatus` in the later subscription headings.

## Exact historical XSD context

Selected schema:
- file: `IBIS-IP_SystemManagementService_V1.0.xsd`
- local blob: `2d32630a0f1981e980e6a466e3f6a69136410f24`
- official upstream: `VDVde/VDV301`
- official tag: `VDV-301-2.0`
- upstream blob: `2d32630a0f1981e980e6a466e3f6a69136410f24`

The local and official-tag blobs are byte-identical.

The schema contains:
- `SystemManagementService.GetServiceStatusResponse`
- `SystemManagementService.GetServiceStatusResponseStructure`
- `SystemManagementService.GetServiceStatusResponseDataStructure`

This corroborates the `ServiceStatus` terminology for the concrete response identifiers modeled by this historical XSD.

The service-specific subscription operation names are not independently modeled as roots in this small historical service XSD; therefore the XSD is not overclaimed as direct proof of `SubscribeServiceStatus`. The visible page-67 operation inventory is the direct documentation source for those operation names.

## Disproof attempt

The mismatch is not explained by a generic "system status" concept:

- page 67 explicitly names the operations `SubscribeServiceStatus` and `UnsubscribeServiceStatus`;
- page 69 changes only the corresponding detailed headings to `SystemStatus`;
- the neighboring `GetServiceStatus` detail and XSD response identifiers retain `ServiceStatus`.

No evidence supports treating the page-69 `SystemStatus` wording as an alternative XML operation namespace.

## Classification and SDK behavior

Confirmed documentation terminology/stale-identifier defect.

- XML/XSD validity behavior: **unchanged by the documentation defect**
- runtime matcher: **not applicable**
- SDK behavior: **informational**
- `SubscribeSystemStatus` / `UnsubscribeSystemStatus` aliases: **must not be generated**
- concrete XML identifiers must follow the selected operation/XSD context.

The finding remains historical, version-specific documentation evidence.
