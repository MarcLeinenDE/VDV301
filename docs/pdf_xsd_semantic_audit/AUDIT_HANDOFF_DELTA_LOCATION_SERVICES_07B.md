# Audit handoff delta - Location Services 07B closure

Status: supplemental delta after Location Services V1.0 closure.

Branch:

```text
dev/schema-integration
```

New/updated files:

```text
docs/pdf_xsd_semantic_audit/07b_location_services_findings_and_closure.md
docs/pdf_xsd_semantic_audit/generated/location_services_findings_closure_matrix.csv
docs/pdf_xsd_semantic_audit/LOCATION_SERVICES_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_LOCATION_SERVICES_07B.md
```

## Closure result

Location Services V1.0 first pass is closed for:

```text
BeaconLocationService V1.0
DistanceLocationService V1.0
GNSSLocationService V1.0
NetworkLocationService V1.0
```

Selected pool:

```text
Each service V1.0 + IBIS-IP_common_V1.0.xsd + IBIS-IP_Enumerations_V1.0.xsd
```

## Findings state

```text
LS-001 open candidate: GNSS PDF HorizontalDilutionOfPrecision vs XSD HoriziontalDilutionOfPrecision.
LS-002 OK with note: Distance Odometer-Pulses is identical in PDF/XSD and must not be normalized.
LS-003 OK with note: Location-service wrapper/top-level modelling differs by service and must be preserved.
```

No XSD files changed.
No official PR candidate opened.

## Validation backlog impact

Later local samples should cover:

```text
Beacon GetDataResponse positive sample.
Distance Data positive sample with Odometer-Pulses.
GNSS positive sample using HoriziontalDilutionOfPrecision.
GNSS negative/provider-note sample using HorizontalDilutionOfPrecision.
Network Data positive sample.
```

## Next recommended block

```text
08_door_state_service_historical_start.md
```
