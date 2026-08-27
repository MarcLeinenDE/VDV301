# Location Services findings register addendum

Status: supplemental register; keep separate until the main findings register is consolidated.

Authority rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

Source audit files:

```text
docs/pdf_xsd_semantic_audit/07_location_services_historical_start.md
docs/pdf_xsd_semantic_audit/07a_location_services_v1_0_pdf_xsd_first_pass.md
```

## Location Services findings

### LS-001 - GNSSLocationService HorizontalDilutionOfPrecision PDF spelling vs XSD HoriziontalDilutionOfPrecision

State: confirmed PDF/XSD spelling discrepancy candidate.

Observation:

```text
The checked GNSSLocationService V1.0 PDF table lists HorizontalDilutionOfPrecision.
IBIS-IP_GNSSLocationService_V1.0.xsd defines HoriziontalDilutionOfPrecision.
The XSD spelling is typo-like but is the current executable schema spelling in the checked V1.0 pool.
```

Impact:

```text
Payloads using <HorizontalDilutionOfPrecision> as printed in the PDF will fail against the checked V1.0 XSD.
Payloads using <HoriziontalDilutionOfPrecision> validate against the checked XSD but look typo-like in provider discussions.
Validation follows XSD unless an official schema correction exists.
```

Next action:

```text
Add local positive/negative XML samples.
Include LS-001 in the post-audit official-facing review before deciding whether to propose a minimal correction or only document the compatibility risk.
```

### LS-002 - DistanceLocationService Odometer-Pulses spelling

State: OK with note.

Observation:

```text
The checked DistanceLocationService V1.0 PDF table and IBIS-IP_DistanceLocationService_V1.0.xsd both use Odometer-Pulses.
```

Impact:

```text
No discrepancy opened.
Element name contains a hyphen, so tooling must preserve the exact XML element name.
Do not normalize to OdometerPulses or Odometer_Pulses.
```

Next action: local positive sample with Odometer-Pulses.

### LS-003 - Location-service wrapper style differs by service

State: OK with note.

Observation:

```text
BeaconLocationService uses BeaconLocationService.GetDataResponse with a Data / OperationErrorMessage choice.
DistanceLocationService, GNSSLocationService and NetworkLocationService expose raw *.Data top-level elements.
```

Impact:

```text
No discrepancy opened.
A future validator must preserve service-specific top-level element modelling and must not normalize the location services to one wrapper pattern.
```

Next action: include this in the executable service/version routing matrix.
