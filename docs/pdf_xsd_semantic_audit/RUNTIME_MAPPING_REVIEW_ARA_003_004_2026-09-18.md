# Runtime-mapping review — ARA-003 / ARA-004 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

Both remaining AnalogRadioService runtime candidates were individually reviewed against the completed semantic classification, the pinned V2.4 Deep Read, EV-105 and the explicit candidate-profile routing guard.

### ARA-003

Decision: `candidate -> reviewed`.

Runtime mapping is permitted only for the explicitly selected **AnalogRadioService V2.4 candidate/integration profile**.

Required context:

- candidate/integration V2.4 profile is explicitly selected;
- candidate XSD result is **VALID** for `AnalogRadioService.SendTelegram`;
- `RadioTelegramStructure` omits `Transmitter`.

Effect:

- informational Known-Issues note only;
- preserve the XSD VALID result;
- explain that the PDF table says 1:1 while the same PDF schema view and candidate XSD use optional `Transmitter`;
- never describe this as official V2.4 release conformance.

### ARA-004

Decision: `candidate -> reviewed`.

Runtime mapping is permitted only for an **exact** AnalogRadioService V2.4 URI/operation-path match on the literal segment:

```text
SendFFSKTelegram
```

Effect:

- warning/advisory that the operation inventory and XML example use `SendTelegram`;
- no fuzzy matching;
- no automatic rewrite;
- no `SendFFSKTelegram` alias registration;
- no inference of an official V2.4 strict XSD profile.

## Mapping inventory after review

```text
reviewed       32
candidate      49
not_designed    1
not_applicable 110
implemented     0
```

## Gate

GitHub Actions run **35344324381**: **SUCCESS**.

The gate verified:

- semantic registry remains valid and complete at 192 findings;
- deterministic runtime-mapping regeneration is byte-identical;
- ARA-003 maps to the informational activation class;
- ARA-004 maps to the resolver/profile-warning activation class;
- both remain `reviewed_not_implemented`;
- all mappings preserve `selected_xsd_result_remains_normative`;
- SDK manifest baseline self-test passes;
- all 50 root XSDs compile without mutation.

No executable matcher was added and no XSD was changed.
