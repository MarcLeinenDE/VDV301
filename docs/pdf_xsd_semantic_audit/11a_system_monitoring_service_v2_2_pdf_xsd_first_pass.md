# SystemMonitoringService V2.2 PDF/XSD first pass

Status: detailed first pass completed; local compile/sample validation pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
```

## 1. Selected validation family

```text
IBIS-IP_SystemMonitoringService_V2.2.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

The service file is byte-identical to the official `VDV-301-2.2` release-tag blob.

## 2. GetDeviceStatus

PDF operation model:

```text
Request: none
Response: SystemMonitoringService.GetDeviceStatusResponseStructure
```

PDF response choice:

```text
SystemMonitoringService.GetDeviceStatusResponseData
or OperationErrorMessage
```

PDF response data:

```text
TimeStamp                         1:1
DeviceSpecificationWithStateList 1:1
```

XSD result:

```text
Aligned at the service-local response wrapper/data level.
```

The inherited list's item cardinality is a Common-level discrepancy (CE-012), not an SMS-local mismatch.

## 3. GetServiceStatus

The operation table uses `GetServiceStatus`.

PDF response choice:

```text
SystemMonitoringService.GetServiceStatusResponseData
or OperationErrorMessage
```

PDF response data:

```text
TimeStamp                          1:1
ServiceIdentificationWithStateList 1:1
```

XSD result:

```text
Aligned at the service-local response wrapper/data level.
```

The XSD top-level/structure name is:

```text
SystemMonitoringService.GetServiceStatusResponse
```

The detailed PDF body also uses this name, while the section heading says `GetSystemStatus`. This supports SMS-002 as a PDF heading/label issue rather than an XSD naming defect.

## 4. Subscribe/Unsubscribe modelling

The PDF operation table includes subscribe/unsubscribe concepts for both device and service status.

The PDF explicitly references the generic subscription structures from VDV 301-2-1:

```text
SubscribeRequestStructure
SubscribeResponseStructure
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

The local service XSD group contains no SystemMonitoringService-specific subscribe/unsubscribe elements.

Interpretation:

```text
This is consistent with the broader generic subscription modelling pattern already seen in other services.
Do not classify this as a service XSD defect in the first pass.
The future SDK must not infer the complete HTTP operation concept set solely from service-local XSD group elements.
```

SMS-001 is therefore retained as `service_modelling_or_generic_response_candidate / OK with note` rather than an XSD correction candidate.

## 5. SMS-002 - SystemStatus headings vs ServiceStatus operation

Evidence is internally consistent in favour of `ServiceStatus` as the executable/operation name:

```text
PDF operation table: GetServiceStatus / SubscribeServiceStatus / UnsubscribeServiceStatus
PDF section 2.5 body: GetServiceStatus
PDF response element: SystemMonitoringService.GetServiceStatusResponse
XSD: SystemMonitoringService.GetServiceStatusResponse
```

Conflicting PDF headings:

```text
2.5 GetSystemStatus
2.6 SubscribeSystemStatus
2.7 UnsubscribeSystemStatus
```

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Validation behaviour:

```text
Use the XSD names exactly.
Do not accept `SystemMonitoringService.GetSystemStatusResponse` as an alias unless an official schema says so.
```

## 6. SMS-003 - stale HTMLDisplayService sentence in foreword

The English foreword contains an HTMLDisplayService explanation in the SystemMonitoringService document.

Classification:

```text
mismatch_kind: ok_note
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
final_handling_bucket: no_action_note
```

No executable impact.

## 7. SMS-004 - `302-2` version-history reference

The version history twice refers to `302-2`, while the same document's references section identifies VDV 301-2-0 as the former base-services source containing SystemManagementService and SystemDocumentationService.

Classification:

```text
mismatch_kind: unresolved
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: medium
final_handling_bucket: unresolved_keep_open
```

This is documentation-only. Do not promote it to a definitive typo without additional source confirmation.

## 8. Shared Common cardinality checks triggered by SMS

### CE-012 inherited

`DeviceSpecificationWithStateList`:

```text
Common PDF V2.2: DeviceSpecificationWithState 1:*
Common XSD V2.2: minOccurs="0" maxOccurs="unbounded"
```

SystemMonitoring GetDeviceStatus requires the list wrapper 1:1, but the list may be empty under the XSD.

### CE-018 newly opened

`ServiceIdentificationWithStateList`:

```text
Common PDFs V2.1, V2.2, V2.3, V2.4: ServiceIdentificationWithState 1:*
Common XSDs V2.1, V2.2, V2.3, V2.4: minOccurs="0" maxOccurs="unbounded"
```

Classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: high
final_handling_bucket: local_validation_required
```

SystemMonitoring GetServiceStatus is a direct service-level consumer of this shared list.

### CE-019 candidate

Text extraction of the same Common tables repeatedly associates the list item with `ServiceSpecificationWithState`, while the XSD item type is `ServiceIdentificationWithStateStructure`.

The surrounding semantics strongly favour the XSD type because a system-wide service identification includes the device on which the service runs.

However, direct screenshots of the relevant VDV PDF table pages were not reliably retrievable during this pass.

Classification:

```text
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: medium-high pending visual confirmation
final_handling_bucket: unresolved_keep_open
```

Validation follows the XSD irrespective of the pending visual confirmation.

## 9. Technical validation backlog

```text
SMS-VB-001: compile SystemMonitoringService V2.2 + Common V2.2 + Enumerations V2.2.
SMS-VB-002: positive GetDeviceStatusResponse with one DeviceSpecificationWithState.
SMS-VB-003: empty DeviceSpecificationWithStateList sample to demonstrate XSD 0:* behaviour for CE-012.
SMS-VB-004: positive GetServiceStatusResponse with one ServiceIdentificationWithState.
SMS-VB-005: empty ServiceIdentificationWithStateList sample to demonstrate XSD 0:* behaviour for CE-018.
SMS-VB-006: negative naming sample using GetSystemStatusResponse vs positive GetServiceStatusResponse.
SMS-VB-007: generic subscription operation modelling/inventory check against Common subscription structures.
```

No item above has been locally executed yet.

## 10. Result

```text
Service-local GetDeviceStatus and GetServiceStatus response structures align with the selected XSD.
SMS-001 retained as generic subscription modelling / OK with note.
SMS-002 confirmed as PDF heading/label candidate.
SMS-003 confirmed as documentation-only foreword copy/paste candidate.
SMS-004 retained as unresolved documentation reference candidate.
CE-012 inherited.
CE-018 newly opened as shared Common cardinality mismatch.
CE-019 opened as visually-pending Common type/documentation candidate.
No XSD modified.
No local validation claimed.
```
