# SystemMonitoringService historical audit start

Status: historical first pass started from `dev/schema-integration` head `5993ede590d39db136dd71c06ee1f8e9821435c7`. Public PDF, official release-tag XSD provenance and exact dependency pool resolved. Local XSD compilation/sample validation remains pending.

Scope:

```text
VDV 301-2-18 SystemMonitoringService V2.2, 08/2019
IBIS-IP_SystemMonitoringService_V2.2.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

## 1. Authority and source policy

```text
Validation follows the selected XSD family.
PDF differences are retained as documentation/provider-facing findings.
No XSD is changed merely because PDF and XSD differ.
Historical authority is resolved from official VDVde/VDV301 release material.
No latest-version dependency substitution is allowed.
```

## 2. Public PDF mapping

Observed public document:

```text
VDV-Schrift 301-2-18
SystemMonitoringService V2.2
08/2019
```

The document describes a system-wide monitoring service which provides information about devices and services and queries DeviceManagementServices in the IBIS-IP system.

The document states that there should generally be only one SystemMonitoringService in an IBIS-IP system and describes the service as an HTTP service.

## 3. Official XSD provenance

Official release source checked:

```text
VDVde/VDV301 tag VDV-301-2.2
IBIS-IP_SystemMonitoringService_V2.2.xsd
blob d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
```

The file in `MarcLeinenDE/VDV301 dev/schema-integration` has the same blob SHA:

```text
d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
```

Therefore this is official release material already present in the integration branch. No historical backfill is required.

## 4. Exact dependency pool

The service XSD explicitly includes:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Selected executable pool:

```text
SystemMonitoringService V2.2
+ Common V2.2
+ Enumerations V2.2
```

This exact pool is the later SDK routing target for SystemMonitoringService V2.2.

## 5. Service-local XSD inventory

The service group is:

```text
SystemMonitoringServiceGroup
```

It contains:

```text
SystemMonitoringService.GetDeviceStatusResponse
SystemMonitoringService.GetServiceStatusResponse
```

The XSD defines the corresponding top-level response elements and structures.

GetDeviceStatus response data:

```text
TimeStamp                         1:1
DeviceSpecificationWithStateList 1:1
```

GetServiceStatus response data:

```text
TimeStamp                          1:1
ServiceIdentificationWithStateList 1:1
```

The two list structures themselves are inherited from Common V2.2.

## 6. Candidate notes for detailed pass

### SMS-001 candidate - subscriptions are documented but not service-local XSD operation elements

PDF operation table contains:

```text
GetDeviceStatus
SubscribeDeviceStatus
UnsubscribeDeviceStatus
GetServiceStatus
SubscribeServiceStatus
UnsubscribeServiceStatus
```

The subscription sections explicitly say that the generic structures from VDV 301-2-1 are used.

The service XSD group contains only the two concrete Get response elements.

Initial classification:

```text
mismatch_kind: service_modelling
likely_source_issue: service_modelling_or_generic_response_candidate
```

This resembles the already observed generic subscription modelling pattern in CIS/JIS and is not treated as a schema defect without cross-service/runtime evidence.

### SMS-002 candidate - SystemStatus headings vs ServiceStatus executable naming

The PDF operation overview and executable XSD use:

```text
GetServiceStatus
SubscribeServiceStatus
UnsubscribeServiceStatus
```

But section headings 2.5 through 2.7 use:

```text
GetSystemStatus
SubscribeSystemStatus
UnsubscribeSystemStatus
```

The body text in section 2.5 itself says `GetServiceStatus`, and the response structure is `SystemMonitoringService.GetServiceStatusResponse`.

Initial classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
```

### SMS-003 candidate - HTMLDisplayService sentence in English foreword

The English foreword correctly says the document describes SystemMonitoringService, but immediately contains a sentence explaining that HTMLDisplayService provides a URL to a web server for multifunction screens.

Initial classification:

```text
mismatch_kind: ok_note
likely_source_issue: pdf_table_or_documentation_error_candidate
```

This is documentation-only and has no executable validation impact.

### SMS-004 candidate - version history reference `302-2`

The V2.2 version-history text says the service was extracted from `VDV-Schrift 302-2` / `VDV-requirements 302-2`.

The references section of the same document identifies the relevant former base-services document as:

```text
VDV 301-2-0
DeviceManagementService, SystemManagementService, SystemDocumentationService V2.0
```

No separate authoritative evidence for a VDV 302-2 IBIS-IP source was established in this pass.

Initial classification:

```text
mismatch_kind: unresolved
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: medium
```

Keep as documentation candidate only; do not assert final typo status without additional source confirmation.

## 7. Shared Common findings inherited by SystemMonitoringService

The two SystemMonitoring response paths expose shared list structures and therefore make Common cardinality findings operationally relevant.

Existing:

```text
CE-012: DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*
```

Newly identified during this service pass:

```text
CE-018: ServiceIdentificationWithStateList PDF 1:* vs XSD 0:*
CE-019 candidate: PDF table type/reference for ServiceIdentificationWithState list item appears to say ServiceSpecificationWithState while XSD uses ServiceIdentificationWithStateStructure; visual confirmation pending.
```

These are Common findings and must not be duplicated as SMS-specific executable defects.

## 8. Next file

```text
docs/pdf_xsd_semantic_audit/11a_system_monitoring_service_v2_2_pdf_xsd_first_pass.md
```
