# VDV 301-2 Basisdienste V2.1 - Deep Read Pass 2

Status: textual fresh read complete; exact release/XSD inventory and previous-audit comparison complete; visual closure pending.

Document ID: `VDV301-2_BASE_V2.1`

Official publication:

```text
VDV-Schrift 301-2
Version 2.1
07/2018
Basisdienste / Base Services
DeviceManagementService
SystemManagementService
SystemDocumentationService
```

Official PDF:

```text
https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx?forced=false
```

## 1. Method and source quality

This pass followed `DEEP_READ_METHOD.md`:

1. fresh read of the original VDV PDF before opening the old V2.1 audit,
2. complete native-text pass across IP/DNS-SD/HTTP conventions, notation/subscription model, system configuration/start-up, DMS, SystemDocumentation, SystemManagement and version history,
3. exact official release-tag/XSD comparison,
4. visual-page review attempt,
5. only then comparison against the previous first-pass audit.

The native text layer is usable, with normal bilingual/table line-wrap artefacts.

A PDF screenshot was requested during this pass, but the screenshot backend returned an internal/cache error. Layout-sensitive observations therefore remain `needs_visual_review`; this document is not labelled `exhaustive_read`.

No dedicated independent OCR copy of this publication was found in the available File Library. XSD aggregate documentation and prior tool reports are not counted as OCR substitutes.

## 2. Exact official V2.1 release family

The complete official upstream tag `VDV-301-2.1` was inventoried and compared with the operational superbranch.

No additional missing historical official XSD was found.

The Base Services publication remains deliberately mixed-version:

```text
DeviceManagementService V2.1
  -> IBIS-IP_common_V2.1.xsd
  -> IBIS-IP_Enumerations_V2.1.xsd

SystemDocumentationService V2.0
  -> IBIS-IP_common_V2.0.xsd
  -> IBIS-IP_Enumerations_V2.0.xsd

SystemManagementService V1.0
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

This is another direct release-level proof that document version and service-schema version must not be conflated.

Current stored root-XSD count remains 50 after the earlier SystemDocumentation V2.0 backfill. The last actually executed full-root compile baseline remains 49; this block makes no 50/50 compile claim.

## 3. V2.0 -> V2.1 corrections confirmed by fresh read

### 3.1 SubscribeDeviceInformation subsection restored

V2.0 listed `SubscribeDeviceInformation` in the DMS operation inventory but lacked a corresponding detailed subsection heading.

V2.1 contains a dedicated `Data Structure of Operation SubscribeDeviceInformation` subsection.

Result:

```text
DR3012V20-006 is a V2.0 documentation issue and is not carried forward as a V2.1 defect.
```

### 3.2 Literal broken Word references removed

The repeated V2.0 strings:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

were not found in the V2.1 fresh text pass.

Result:

```text
DMS-002 is historically confirmed for V2.0 and resolved in the checked V2.1 publication.
```

### 3.3 DMS operation-group modelling materially expanded

The exact DMS V2.1 XSD operation group now explicitly contains generic Subscribe/Unsubscribe and control request/response entries, including ActivateDevice, DeactivateDevice, RestartDevice, Start/Restart/StopService and the new subdevice/update operations.

Result:

```text
DMS-001 remains a V2.0 modelling finding.
The V2.0 group/global-element gap is not carried forward as a V2.1 DMS mismatch.
```

## 4. New V2.1-specific finding

### DR3012V21-001 - stale service-document cross references

The V2.1 system-configuration/system-start principles refer to:

```text
DeviceManagementService -> VDV 301-2-2
SystemDocumentationService -> VDV 301-2-4
```

A further DeviceManagementService system-start reference again points to VDV 301-2-2.

Within the published VDV 301-2 family these numbers identify other service documents, e.g. 301-2-2 is BeaconLocationService and 301-2-4 is DistanceLocationService; the three Basisdienste are defined in the present VDV 301-2 publication.

Classification:

```text
pdf_cross_reference_error_candidate
confidence: high
validation impact: none
```

Resolver rule:

```text
Do not route a service schema from these stale prose references.
Use the exact official release/tag and operation/service manifest.
```

A minor English `HTPP services` typo was also observed. It is retained in this report as low-impact editorial evidence but not assigned a separate finding ID to avoid unnecessary fragmentation.

## 5. Persistent earlier findings in V2.1

### 5.1 Bilingual RFC conflict persists

German ZeroConf/link-local text cites RFC 3927; the English translation of the corresponding passage still cites RFC 2927. The bibliography uses RFC 3927.

This strengthens `DR3012-001` / the V2.0 evidence rather than creating another cause ID.

### 5.2 SRV Weight explanation remains inverted

The lower-weight-preferred explanation remains in V2.1, contrary to RFC 2782 weighted proportional selection semantics.

This strengthens `DR3012-002`.

### 5.3 Heartbeat typo/history contradiction persists

V2.1 history continues to say the spelling was corrected to:

```text
HeartbeatInterval
```

but the actual SystemDocumentation tables still print:

```text
HertbeatIntervall
```

The exact release family still selects `SystemDocumentationService_V2.0.xsd`, whose executable element is `HeartbeatInterval` of type `IBIS-IP.duration`.

This strengthens `DR3012V20-003`.

### 5.4 `SystemDocumenationService` typo persists

The misspelled service name remains in narrative text while the official service name/XSD is `SystemDocumentationService`.

This strengthens `DR3012V20-004`.

### 5.5 ServiceStatus/SystemStatus heading mismatch persists

The operation table and exact SystemManagement V1.0 XSD use:

```text
GetServiceStatus
SubscribeServiceStatus
UnsubscribeServiceStatus
```

Detailed PDF headings continue to use `GetSystemStatus`, `SubscribeSystemStatus`, `UnsubscribeSystemStatus` terminology.

The body itself refers to a GetServiceStatus operation and the response root is `SystemManagementService.GetServiceStatusResponse`.

This strengthens `DR3012-005`. No SystemStatus aliases are created.

### 5.6 SUB-001 persists

The V2.1 notation table still maps `UnsubscribeData` to:

```text
TerminateSubscribeRequestStructure
TerminateSubscribeResponseStructure
```

while Common uses the `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure` family.

The affected documentation history of `SUB-001` therefore now explicitly includes V1.0, V2.0 and V2.1, in addition to the later checked General Conventions versions.

### 5.7 GetDeviceConfiguration setter wording persists

The V2.1 `GetDeviceConfiguration` description still says the operation enables setting the variable device parameter, while `SetDeviceConfiguration` is the actual setter.

This strengthens `DR3012V20-007`.

### 5.8 GetDeviceInformation response still labelled request

The response structure/data description still uses request wording.

This strengthens `DR3012V20-008`.

## 6. DMS V2.1 functional extension and exact XSD alignment

The V2.1 history identifies two functional DMS extensions:

```text
- detailed device status including support for independent subdevices
- operations implementing the update procedure
```

The fresh read confirms the associated operation families, including:

```text
GetAllSubdeviceInformation
GetDeviceStatusInformation
GetAllSubdeviceStatusInformation
GetAllSubdeviceErrorMessages
InstallUpdate
RetrieveUpdateState
GetUpdateHistory
FinalizeUpdate
FinalizeAllPendingUpdates
```

The exact official DMS V2.1 XSD models those operations and routes to Common/Enums V2.1.

### DMS-003 reconfirmed, not duplicated

The V2.1 PDF continues the historical `ErrorMessage 10:*` rule for device/subdevice error messages, matching the exact V2.1 schema. This remains `ok_with_note`; the later 0:* correction must not be retroactively applied.

### DMS-004 reconfirmed, not duplicated

For `InstallUpdateRequest`, V2.1 PDF and exact XSD require:

```text
UpdateID        1:1
UpdateTimestamp 1:1
UpdateURL       1:1
```

while checksum/file-size fields are optional. The later V2.4 optionality change is not applied backwards.

## 7. Old-audit comparison

The earlier DMS historical first-pass was opened only after the fresh V2.1 read.

It independently confirms:

```text
DMS-001: V2.0 group/global modelling gap; V2.1 reorganized/expanded.
DMS-002: V2.0 broken Word references; absent in checked V2.1.
DMS-003: V2.1 ErrorMessage 10:* is PDF/XSD-aligned.
DMS-004: V2.1 InstallUpdate requiredness is PDF/XSD-aligned.
```

The fresh pass adds the broader cross-document/protocol findings above, especially `DR3012V21-001` and the persistence history of earlier Base-Service defects.

## 8. Deep-read conclusion for V2.1

```text
textual fresh read: complete
exact VDV-301-2.1 tag/XSD inventory: complete
additional historical XSD backfill required: no
old-audit comparison: complete
visual page closure: pending after screenshot backend error
deep_read_state: needs_visual_review
```

The V2.1 release is especially important for the SDK resolver because a single Base-Services PDF combines three service-schema generations at once:

```text
DMS 2.1 / SystemDocumentation 2.0 / SystemManagement 1.0
```

## 9. Next document

```text
VDV301-2_GC_V2.2
General Conventions V2.2
```

Fresh-read priorities:

```text
- IP-address allocation wording and German/English divergence,
- DNS-SD SRV Priority/Weight semantics,
- UnsubscribeData / TerminateSubscribe notation,
- HTTP methods/status/media-type rules,
- service/version publication and discovery rules,
- separation of service documents introduced with the V2.2 family,
- complete official VDV-301-2.2 release-tag XSD inventory before old-audit comparison.
```
