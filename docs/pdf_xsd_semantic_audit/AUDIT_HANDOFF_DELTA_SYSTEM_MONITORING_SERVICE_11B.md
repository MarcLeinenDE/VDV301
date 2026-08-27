# AUDIT HANDOFF DELTA - SystemMonitoringService 11B

Status: supplemental delta after SystemMonitoringService V2.2 historical first-pass closure.

Branch:

```text
dev/schema-integration
```

Starting head:

```text
5993ede590d39db136dd71c06ee1f8e9821435c7
```

New audit files:

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
docs/pdf_xsd_semantic_audit/11a_system_monitoring_service_v2_2_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/11b_system_monitoring_service_findings_and_closure.md
docs/pdf_xsd_semantic_audit/SYSTEM_MONITORING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/generated/system_monitoring_service_historical_scope_matrix.csv
docs/pdf_xsd_semantic_audit/generated/common_service_identification_with_state_findings.csv
```

Routing result:

```text
SystemMonitoringService V2.2
-> IBIS-IP_SystemMonitoringService_V2.2.xsd
-> Common V2.2
-> Enumerations V2.2
```

Official provenance:

```text
VDVde/VDV301 tag VDV-301-2.2
service XSD source/branch blob d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
```

Findings:

```text
SMS-001: subscriptions use generic Common structures and are not local XSD-group elements; OK with note / service modelling.
SMS-002: SystemStatus section headings vs executable ServiceStatus names; high-confidence PDF label candidate.
SMS-003: stale HTMLDisplayService sentence in English foreword; documentation-only candidate.
SMS-004: `302-2` version-history reference vs VDV 301-2-0 reference context; unresolved documentation candidate.
CE-018: ServiceIdentificationWithStateList PDF 1:* vs XSD 0:* across V2.1-V2.4.
CE-019: extracted PDF list-item type/reference appears ServiceSpecificationWithState vs XSD ServiceIdentificationWithStateStructure; visual confirmation pending.
```

Validation status:

```text
No local XSD compilation performed.
No XML sample validation performed.
No XSD modified.
No PR/comment/merge performed.
```

Next planned audit block:

```text
docs/pdf_xsd_semantic_audit/12_analog_radio_service_historical_start.md
```
