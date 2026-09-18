# Runtime-mapping review — COMMON V1.0 DRCOM10-002..005 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

The four Common V1.0 structure/cardinality candidates were reviewed against the exact official historical Common V1.0 schema family, preserved EV-117 executable evidence, the frozen EV-135 revalidation result, and focused instance probes.

### DRCOM10-002 — DataAcceptedResponse exclusive choice

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V1.0;
- an advisory requires an actual **XSD INVALID** result;
- both `DataAcceptedResponseData` and `OperationErrorMessage` are present in `DataAcceptedResponseStructure`;
- selected XSD defines the branches as an exclusive `xs:choice`.

Effect: preserve the XSD INVALID result and explain the misleading PDF table. No compositor override is introduced.

### DRCOM10-003 — empty ServiceSpecificationWithStateList

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V1.0;
- XSD result is **VALID**;
- `ServiceSpecificationWithStateList` is present with zero `ServiceSpecificationWithState` children;
- selected XSD declares `minOccurs=0 maxOccurs=unbounded`.

Effect: keep the XSD-valid result and optionally emit an advisory that the PDF states 1:*.

### DRCOM10-004 — repeated Announcement / FareZone

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V1.0;
- XSD result is **INVALID**;
- `JourneyStopInformation` contains a second `Announcement` or a second `FareZone`;
- selected XSD models each as an optional singleton.

Effect: preserve XSD INVALID and explain the PDF's incorrect 0:* cardinality.

### DRCOM10-005 — ShortTripStop child identifier

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V1.0;
- XSD result is **INVALID**;
- `ShortTripStopListStructure` contains exact PDF-derived child name `ShortTripStopList` instead of `ShortTripStop`;
- selected XSD declares `ShortTripStop` of type `ShortTripStopStructure`.

The PDF-referenced `StopPointTariffInformationStructure` is instance-shape equivalent to `ShortTripStopStructure` in this exact XSD family. No separate type-shape runtime mismatch is invented.

## Mapping inventory after review

```text
reviewed        46
candidate       32
not_designed     1
not_applicable 113
implemented      0
```

## Gate

Primary Common V1.0 gate **35347544265**: **SUCCESS**.

Closure/consistency gate **35347689664**: **SUCCESS**.

The gate verified:

- semantic registry and deterministic 46-entry runtime-mapping regeneration;
- preserved EV-117 exact-authority evidence;
- DataAcceptedResponse exact `xs:choice` boundary;
- empty ServiceSpecificationWithStateList is XSD-valid;
- one Announcement/FareZone validates while two repetitions fail;
- ShortTripStop child validates while PDF-derived ShortTripStopList child fails;
- ShortTripStopStructure and StopPointTariffInformationStructure have equivalent instance signatures in V1.0;
- all root XSDs remain unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

EV-135 remains frozen provenance for the completed historical revalidation. The runtime gate intentionally uses the relevant executable boundaries directly rather than reopening the historical revalidation workflow state.

No executable Known-Issues matcher was added and no XSD was changed.
