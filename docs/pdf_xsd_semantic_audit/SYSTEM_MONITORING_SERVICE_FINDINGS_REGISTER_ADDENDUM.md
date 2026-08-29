# SystemMonitoringService findings register addendum

Status: supplemental register; SystemMonitoringService V2.2 has now been independently re-read and the historical SMS finding set revalidated under the current Evidence Gate.

Authority rule:

```text
Validation follows SystemMonitoringService V2.2 + Common V2.2 + Enumerations V2.2.
PDF labels and generic operation concepts do not become executable aliases.
```

## SMS-001 - subscriptions vs service-local XSD group

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: contextual_not_defect
classification_confidence: high
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
likely_source_issue: pdf_operation_heading_error
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
likely_source_issue: pdf_wrong_service_copy_paste
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
mismatch_kind: documentation_reference_number
likely_source_issue: pdf_reference_number_error
classification_confidence: high
version_scope: V2.2 PDF
validation_behavior: none
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
Version history says 302-2; references section identifies VDV 301-2-0 as the former base-services document containing SystemManagementService and SystemDocumentationService.
```

No executable XSD change follows from this documentation reference-number error.

## Current Evidence-Gate closure — SMS V2.2

Fresh-read freeze: `625bb9a4d19f1f1c47a529686defa9b1368c80ff`.

Executable evidence: `EV-116`, run `33269006407`, job `99144006184`, PASS on the exact official VDV-301-2.2 family.

```text
SMS-001 -> contextual_not_defect_executable_context_confirmed_EV-116
SMS-002 -> executable_confirmed_EV-116
SMS-003 -> context_verified
SMS-004 -> context_verified_pdf_reference_number_error
```

`SMS-001` remains an intentional modelling note: generic Subscribe/Unsubscribe structures live in Common V2.2 and no service-specific subscription roots are invented. `SMS-002` is executable-constrained because the real `GetServiceStatusResponse` validates while invented `GetSystemStatusResponse` has no global declaration. `SMS-004` is no longer unresolved: the same official PDF identifies the old Base Services source as VDV 301-2-0, consistent with the official publication catalog.

### DRSMS22-001 — printed broken cross-reference

State: `context_verified`. Page 5 visibly contains `Fehler! Textmarke nicht definiert.` in the list-of-figures area. Documentation-generation defect; no executable effect.

### DRSMS22-002 — ServiceStatus prose describes device state

State: `context_verified_with_exact_common_type_semantics`. ServiceStatus tables use device-state wording even though exact Common V2.2 models `ServiceIdentificationWithState` as `ServiceIdentification` + `ServiceState`. PDF semantic/copy-paste defect; no XSD change.

### DRSMS22-003 — SystemManagementService spelling

State: `context_verified`. Version history spells the service `SystemManagmentService`; the reference section uses the correct name. Editorial PDF defect only.

### DRSMS22-004 — missing Req./Resp. labels

State: `context_verified`. The UnsubscribeServiceStatus row contains the request and response structures but omits the visible `Req.`/`Resp.` labels present for neighboring operations. Documentation-table omission only.

### Common-lane guard

CE-012, CE-018 and CE-019 remain outside this SMS closure. EV-116 observes the exact Common V2.2 declarations only as routing/executable context and does not revalidate those Common PDF findings.
