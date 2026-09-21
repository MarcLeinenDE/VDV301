# Runtime-mapping review — JourneyInformationService V1.0 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

Two executable JIS V1.0 PDF/XSD mismatches were reviewed together.

### JIS-003 — AllLineInformationData.LineInformation cardinality

Decision: `candidate -> reviewed`.

Activation: `xsd_invalid_advisory`.

The advisory is eligible only when selected-XSD validation is already **INVALID** because a second `LineInformation` element occurs in `JourneyInformationService.AllLineInformationData`.

The exact JIS V1.0 XSD omits `maxOccurs`; XML Schema therefore applies the default `maxOccurs=1`. The PDF's `1:*` statement is explanatory defect context only and must not relax validation.

### JIS-005 — SpecificGNSSPointInformation element/type confusion

Decision: `candidate -> reviewed`.

Activation: `xsd_invalid_advisory`.

The advisory is eligible only when selected-XSD validation is already **INVALID** because `SpecificGNSSPointInformationData` is used as the choice element in `RetrieveSpecificGNSSPointInformationResponse`.

The selected XSD requires XML element `SpecificGNSSPointInformation`, whose type is `JourneyInformationService.SpecificGNSSPointInformationData`.

No Data-suffixed element alias or automatic rewrite is permitted.

## Mapping inventory after review

```text
reviewed        58
candidate       20
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-152: run **34113437268**, job **101714662141**, closure **34224429423**
- primary runtime-mapping gate **35551649878**: **SUCCESS**
- closure/consistency gate **35551713393**: **SUCCESS**

The current gate independently reproduced the decisive executable boundaries against the unchanged exact JIS V1.0 XSD route:

- one `LineInformation` validates;
- two `LineInformation` elements are rejected;
- `SpecificGNSSPointInformation` validates;
- `SpecificGNSSPointInformationData` as an XML choice element is rejected;
- exact JIS/Common/Enumerations V1.0 blobs remain unchanged;
- all root XSDs remain unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

No executable Known-Issues matcher was added and no XSD was changed.
