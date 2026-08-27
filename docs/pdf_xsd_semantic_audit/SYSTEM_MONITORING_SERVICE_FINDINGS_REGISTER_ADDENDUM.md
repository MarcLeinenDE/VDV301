# SystemMonitoringService findings register addendum

Status: supplemental register; first-pass closure completed for SystemMonitoringService V2.2.

Authority rule:

```text
Validation follows SystemMonitoringService V2.2 + Common V2.2 + Enumerations V2.2.
PDF labels and generic operation concepts do not become executable aliases.
```

## SMS-001 - subscriptions vs service-local XSD group

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: service_modelling_or_generic_response_candidate
classification_confidence: high for observation; medium-high for intentional-modelling interpretation
version_scope: V2.2
validation_behavior: preserve generic Common subscription modelling
final_handling_bucket: no_action_note
```

Observation:

```text
PDF operation table includes Subscribe/UnsubscribeDeviceStatus and Subscribe/UnsubscribeServiceStatus.
The relevant PDF sections explicitly use generic VDV 301-2-1 subscription structures.
The service XSD group contains only GetDeviceStatusResponse and GetServiceStatusResponse.
```

Impact:

```text
Do not infer full service capability only from local operation-group members.
Do not invent missing service-specific subscription elements.
```

## SMS-002 - SystemStatus section headings vs ServiceStatus

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
version_scope: V2.2
validation_behavior: exact XSD ServiceStatus names
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
Operation overview, PDF body and XSD use GetServiceStatus.
Section headings use GetSystemStatus / SubscribeSystemStatus / UnsubscribeSystemStatus.
```

## SMS-003 - HTMLDisplayService sentence in foreword

Classification:

```text
mismatch_kind: ok_note
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.2 PDF
validation_behavior: none
final_handling_bucket: no_action_note
```

Observation:

```text
SystemMonitoringService English foreword contains an unrelated HTMLDisplayService URL/HTML sentence.
```

## SMS-004 - `302-2` version-history source reference

Classification:

```text
mismatch_kind: unresolved
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: medium
version_scope: V2.2 PDF
validation_behavior: none
final_handling_bucket: unresolved_keep_open
```

Observation:

```text
Version history says 302-2; references section identifies VDV 301-2-0 as the former base-services document containing SystemManagementService and SystemDocumentationService.
```

No executable change follows from this candidate.
