# Runtime-mapping review — COMMON V2.0 DRCOM20-001 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

`DRCOM20-001` was reviewed against the exact official Common V2.0 XSD family, preserved EV-118 executable evidence and the frozen EV-136 revalidation.

Decision: `candidate -> reviewed`.

## Runtime boundary

The advisory is eligible only when all relevant preconditions hold:

- selected strict profile is official Common V2.0;
- the selected XSD result is already **INVALID**;
- the failure occurs in `InternationalTextType`;
- `Value` contains literal wrapper-shaped nested content derived from PDF type `IBIS-IP.string`, and/or
- `Language` contains literal wrapper-shaped nested content derived from PDF type `IBIS-IP.language`.

The exact V2.0 XSD authority declares:

```text
InternationalTextType.Value     xs:string
InternationalTextType.Language  xs:language
```

EV-118 confirms the executable consequence:

- direct primitive `<Value>Hello</Value><Language>de</Language>` is valid;
- wrapper-shaped nested `<Value><Value>...</Value></Value>` and/or `<Language><Value>...</Value></Language>` is invalid.

## Guards

- no `IBIS-IP.string` or `IBIS-IP.language` wrapper alias is introduced;
- invalid XML is not silently rewritten into the primitive shape;
- selected-XSD INVALID remains normative;
- matching is limited to the concrete InternationalTextType wrapper pattern and must not decorate unrelated structural failures.

## Mapping inventory after review

```text
reviewed        49
candidate       29
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and gate

- EV-118: run **33280224191**, job **99174026383**
- EV-136 historical closure: run **33856581531**
- primary runtime-mapping gate **35543011764**: **SUCCESS**

The primary gate verified:

- semantic registry and deterministic 49-entry runtime-mapping regeneration;
- exact official Common V2.0 / Enumerations V2.0 blobs;
- preserved EV-118;
- direct primitive positive instance;
- Value-only wrapper negative instance;
- Language-only wrapper negative instance;
- combined wrapper negative instance;
- all root XSDs unchanged.

No executable Known-Issues matcher was added and no XSD was changed.
