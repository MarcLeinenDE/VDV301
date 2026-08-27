# SystemMonitoringService findings and first-pass closure

Status: historical first-pass closure completed for SystemMonitoringService V2.2. Local XSD compilation/sample validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
docs/pdf_xsd_semantic_audit/11a_system_monitoring_service_v2_2_pdf_xsd_first_pass.md
```

## Routing closure

```text
SystemMonitoringService document V2.2
  -> IBIS-IP_SystemMonitoringService_V2.2.xsd
  -> IBIS-IP_common_V2.2.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd
```

Service XSD provenance:

```text
Official VDVde/VDV301 tag VDV-301-2.2
source blob: d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
branch blob: d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
```

No historical backfill was needed.

## Findings

### SMS-001 - generic subscription operation modelling

```text
State: OK with note / service-modelling candidate.
PDF documents Subscribe/UnsubscribeDeviceStatus and Subscribe/UnsubscribeServiceStatus using generic Common subscription structures.
Service-local XSD group contains only GetDeviceStatusResponse and GetServiceStatusResponse.
No XSD change proposed.
```

### SMS-002 - SystemStatus headings vs ServiceStatus executable names

```text
State: confirmed PDF label/heading candidate.
Executable naming: ServiceStatus.
Conflicting headings: SystemStatus.
Validation follows XSD; no alias introduced.
```

### SMS-003 - HTMLDisplayService sentence in SystemMonitoring foreword

```text
State: confirmed documentation-only copy/paste candidate.
No executable validation impact.
```

### SMS-004 - version-history reference `302-2`

```text
State: unresolved documentation reference candidate.
Same document references former base services as VDV 301-2-0.
Do not state final typo conclusion without additional authority.
```

## Shared Common findings exposed by SMS

```text
CE-012: DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*.
CE-018: ServiceIdentificationWithStateList PDF 1:* vs XSD 0:*; confirmed V2.1-V2.4 history.
CE-019: ServiceIdentificationWithStateList PDF table appears to reference ServiceSpecificationWithState while XSD uses ServiceIdentificationWithStateStructure; visual PDF confirmation pending.
```

## SDK implications

```text
- Resolve SMS V2.2 only to Common V2.2 + Enumerations V2.2.
- Use GetServiceStatus naming, not stale GetSystemStatus headings.
- Do not derive complete subscription capability solely from service-local XSD operation groups.
- Surface CE-012/CE-018 provider diagnostics when an empty list validates against XSD but conflicts with PDF cardinality.
- Do not auto-normalize the CE-019 type-name discrepancy.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not yet performed.
Sample XML validation: not yet performed.
```

No XSD changed. No PR, comment or merge performed.

## Next planned audit block

```text
docs/pdf_xsd_semantic_audit/12_analog_radio_service_historical_start.md
```

Initial focus:

```text
AnalogRadioService V2.4 public PDF vs branch candidate/integration XSD provenance.
Determine whether official release authority exists or whether this remains candidate-only material.
Resolve exact dependency family without upgrading provenance by assumption.
```
