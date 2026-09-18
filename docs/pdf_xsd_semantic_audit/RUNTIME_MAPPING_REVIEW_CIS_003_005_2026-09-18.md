# Runtime-mapping review — CIS-003 / CIS-004 / CIS-005 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

The three remaining CustomerInformationService runtime candidates were reviewed against the official V2.0/V2.2/V2.3 XSD routes and EV-125.

### CIS-003

Decision: `candidate -> reviewed`.

Trigger boundary:

- selected strict profile is CIS V2.0, V2.2 or V2.3;
- strict XSD result is **INVALID**;
- the global response root is exactly `CustomerInformationService.GetCurrentConnectionResponse`;
- the selected XSD instead defines `CustomerInformationService.GetCurrentConnectionInformationResponse`.

Effect: retain the XSD error and add the bilingual Known-Issues advisory. No alias is created.

### CIS-004

Decision: `candidate -> reviewed`.

Trigger boundary:

- selected strict profile is CIS V2.0, V2.2 or V2.3;
- strict XSD result is **INVALID**;
- the global request root is exactly `CustomerInformationService.RetrievePartialStopRequest`;
- the selected XSD instead defines `CustomerInformationService.RetrievePartialStopSequenceRequest`.

Effect: retain the XSD error and add the advisory. No compatibility alias is created.

### CIS-005

Decision: `candidate -> reviewed`.

Trigger boundary:

- selected strict profile is CIS V2.2 or V2.3 only;
- strict XSD result is **INVALID** for `MyOwnVehicleMode`;
- the submitted value is scalar text while the selected XSD requires structured `NetexMode` content.

CIS V2.0 is explicitly excluded because `MyOwnVehicleMode` is absent from that route.

Effect: retain the XSD error and explain the PDF's internal NetexMode/PtModesEnumeration contradiction. No automatic conversion is performed.

## Mapping inventory after review

```text
reviewed       35
candidate      46
not_designed    1
not_applicable 110
implemented     0
```

## Gate

GitHub Actions run **35344691614**: **SUCCESS**.

The gate verified:

- complete 192-entry semantic registry;
- deterministic 35-entry runtime mapping inventory;
- exact CIS V2.0/V2.2/V2.3 global-root boundaries;
- `MyOwnVehicleMode` absent in V2.0 and typed `NetexMode` in V2.2/V2.3;
- all three mappings remain `reviewed_not_implemented`;
- SDK manifest self-test passes;
- all 50 root XSDs compile without mutation.

No runtime matcher was implemented and no XSD was changed.
