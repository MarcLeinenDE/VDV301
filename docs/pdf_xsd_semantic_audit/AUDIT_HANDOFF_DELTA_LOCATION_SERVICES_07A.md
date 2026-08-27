# Audit handoff delta - Location Services 07A

Status: supplemental handoff delta after Location Services V1.0 PDF/XSD first pass.

Branch:

```text
dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/07a_location_services_v1_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/location_services_v1_0_pdf_xsd_first_pass_matrix.csv
docs/pdf_xsd_semantic_audit/LOCATION_SERVICES_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_LOCATION_SERVICES_07A.md
```

Result:

```text
BeaconLocationService V1.0: first-pass aligned, no service-local finding.
DistanceLocationService V1.0: first-pass aligned; Odometer-Pulses closed OK with note.
GNSSLocationService V1.0: LS-001 opened as PDF/XSD spelling discrepancy candidate.
NetworkLocationService V1.0: first-pass aligned, no service-local finding.
```

New finding candidate:

```text
LS-001 - GNSSLocationService HorizontalDilutionOfPrecision PDF spelling vs XSD HoriziontalDilutionOfPrecision
```

Closed OK notes:

```text
LS-002 - Odometer-Pulses exists in both PDF and XSD; preserve exact hyphenated element name.
LS-003 - Beacon wrapper vs raw *.Data modelling differs by service; no normalization.
```

No schema change:

```text
No XSD modified.
No official PR candidate opened.
```

Next recommended step:

```text
07b_location_services_findings_and_closure.md
```
