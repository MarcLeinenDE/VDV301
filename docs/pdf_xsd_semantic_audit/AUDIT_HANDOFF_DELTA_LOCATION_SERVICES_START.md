# Audit handoff delta - Location services historical start

Status: supplemental delta after starting the location-services audit block.

New files:

```text
docs/pdf_xsd_semantic_audit/07_location_services_historical_start.md
docs/pdf_xsd_semantic_audit/generated/location_services_historical_scope_matrix.csv
```

Current result:

```text
BeaconLocationService V1.0, DistanceLocationService V1.0, GNSSLocationService V1.0 and NetworkLocationService V1.0 are public-PDF-known and have matching V1.0 service XSDs in dev/schema-integration.
All four use Common V1.0 + Enumerations V1.0.
No LS finding is opened in the start pass.
```

Important candidate notes for next pass:

```text
LS-001 candidate: GNSS XSD spelling HoriziontalDilutionOfPrecision vs likely PDF/semantic HorizontalDilutionOfPrecision; verify PDF table first.
LS-002 candidate: DistanceLocationService Odometer-Pulses exact hyphenated XSD spelling; verify PDF table first.
LS-003 candidate: BeaconLocationService GetDataResponse style vs raw *.Data style of Distance/GNSS/Network; likely service-specific modelling, document rather than correct unless PDF/XSD conflict is shown.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/07a_location_services_v1_0_pdf_xsd_first_pass.md
```

No XSD changes made.
No official PR action.
