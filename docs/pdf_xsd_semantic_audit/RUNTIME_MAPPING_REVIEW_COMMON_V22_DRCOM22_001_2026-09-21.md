# Runtime-mapping review — Common V2.2 NetexMode — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

`DRCOM22-001` was reviewed against the exact historical-upstream Common V2.2 XSD family, preserved EV-120 executable evidence and frozen EV-138 revalidation.

Decision: `candidate -> reviewed`.

## Runtime boundary

The advisory is eligible only when:

- selected strict profile is the exact historical-upstream Common V2.2 XSD family;
- the selected XSD result is already **VALID**;
- the instance contains an empty `NetexMode` with neither main-mode nor submode choice populated;
- both selected-XSD top-level `xs:choice` compositors remain `minOccurs=0`.

Effect: preserve XSD VALID and optionally explain that the PDF presents both choice groups as mandatory one-of choices.

## Guards

- the PDF one-of requirement must not become an additional validator rule;
- no synthetic `VDV-301-2.2` release tag or alternate schema authority may be invented;
- selected-XSD validity must remain unchanged;
- matching is limited to the concrete empty-NetexMode case and must not be generalized to unrelated optional choices.

## Mapping inventory after review

```text
reviewed        52
candidate       26
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-120: run **33620003188**, job **100214595629**
- EV-138 historical closure: run **33857443446**
- primary runtime-mapping gate **35543624338**: **SUCCESS**

The gate verified:

- semantic registry and deterministic 52-entry runtime-mapping regeneration;
- exact historical-upstream Common V2.2 / Enumerations V2.2 blobs;
- preserved EV-120;
- exactly two top-level NetexMode choice compositors;
- both choices use `minOccurs=0`;
- empty `NetexMode` validates;
- a populated exact main/submode form validates;
- all root XSDs remain unchanged.

No executable Known-Issues matcher was added and no XSD was changed.
