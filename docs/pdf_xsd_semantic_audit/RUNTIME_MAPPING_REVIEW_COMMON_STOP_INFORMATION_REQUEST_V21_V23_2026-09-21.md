# Runtime-mapping review — Common StopInformationRequest V2.1 / V2.3 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

Two StopInformationRequest findings were reviewed together because they describe complementary XSD-first runtime behaviour in the same conceptual structure.

### DRCOM21-001 — repeated StopName is XSD-valid

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V2.1;
- XSD result is **VALID**;
- `StopInformationRequest` contains more than one `StopName`;
- selected XSD declares `StopName minOccurs=0 maxOccurs=unbounded`.

Effect: retain the XSD-valid result and optionally explain that the PDF states the stricter maximum `0:1`.

The runtime layer must not impose the PDF maximum as an extra validation rule.

### DRCOM23-001 — expected-time fields are documented in the wrong request model

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common V2.3;
- XSD result is **INVALID**;
- `StopInformationRequest` contains exact PDF-documented child `ArrivalExpected` and/or `DepartureExpected`;
- the selected XSD contains both fields in `StopInformationStructure`, not in `StopInformationRequestStructure`.

Effect: preserve XSD INVALID and explain the PDF placement error.

No request aliases are introduced and invalid XML is not automatically relocated or rewritten.

## Mapping inventory after review

```text
reviewed        51
candidate       27
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-119: exact official Common V2.1 executable evidence
- EV-137 historical closure: run **33857041308**
- EV-121: exact official Common V2.3 executable evidence
- EV-139 historical closure: run **33857906408**
- primary runtime-mapping gate **35543388239**: **SUCCESS**
- closure/consistency gate **35543443163**: **SUCCESS**

The gate verified:

- semantic registry and deterministic 51-entry runtime-mapping regeneration;
- preserved EV-119 and EV-121;
- Common V2.1 accepts repeated `StopName`;
- Common V2.3 rejects `ArrivalExpected` and `DepartureExpected` in the request;
- Common V2.3 accepts those fields in `StopInformationStructure`;
- the valid/invalid advisory preconditions remain distinct;
- all root XSDs remain unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

No executable Known-Issues matcher was added and no XSD was changed.
