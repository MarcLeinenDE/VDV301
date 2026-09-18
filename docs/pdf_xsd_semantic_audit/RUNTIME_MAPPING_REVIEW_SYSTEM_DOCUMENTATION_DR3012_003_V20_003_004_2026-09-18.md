# Runtime-mapping review — DR3012-003 / DR3012V20-003 / DR3012V20-004 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

The SystemDocumentationService V1.0/V2.0 runtime candidates in this block were reviewed against the exact selected XSDs, the frozen VDV301-2 V1.0 and Base V2.0 revalidation records, the pinned official PDFs, and the previously successful EV-129/EV-130 evidence.

### DR3012-003 — V1.0 HeartbeatIntervall

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official SystemDocumentationService V1.0;
- an advisory requires an actual **XSD INVALID** result;
- the invalid input either uses exact PDF spelling `HertbeatIntervall`, or supplies duration-shaped content at `SystemConfigurationData/HeartbeatIntervall` where the selected XSD requires `IBIS-IP.double`;
- V1.0 `StoreSystemConfigurationRequestStructure/HeartbeatIntervall` remains `IBIS-IP.duration`.

No typo alias is introduced and V1.0 is never normalized forward to V2.0 `HeartbeatInterval`.

### DR3012V20-003 — V2.0 HeartbeatInterval

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official SystemDocumentationService V2.0;
- an advisory requires an actual **XSD INVALID** result;
- exact stale identifiers `HertbeatIntervall` and historical V1.0 `HeartbeatIntervall` are recognized only as explanatory causes of that invalid result;
- authoritative V2.0 identifier is only `HeartbeatInterval`;
- both V2.0 structures use `IBIS-IP.duration`.

No stale spelling is registered as an alias and no V2.0 input is normalized back to V1.0.

### DR3012V20-004 — SystemDocumenationService

Decision: `candidate -> reviewed`.

Runtime boundary:

- official SystemDocumentationService V2.0 context;
- exact resolver/code-generation/documentation-derived identifier `SystemDocumenationService`;
- selected XSD authority is `SystemDocumentationService`.

Effect: warning only. No fuzzy matching, alias registration or schema-result change.

## Mapping inventory after review

```text
reviewed        42
candidate       36
not_designed     1
not_applicable 113
implemented      0
```

## Gate

Primary evidence/runtime gate **35346736511**: **SUCCESS**.

Closure/consistency gate **35346884670**: **SUCCESS**.

The successful gate verified:

- complete semantic registry and deterministic 42-entry runtime-mapping regeneration;
- exact V1.0 `HeartbeatIntervall` identifier with structure-specific double/duration types;
- exact V2.0 `HeartbeatInterval` identifier with duration type in both structures;
- absence of stale identifier aliases in the selected XSDs;
- exact `SystemDocumentationServiceGroup` authority;
- official PDF bytes freshly retrieved and verified against pinned SHA-256 and size;
- stable visible identifier anchors for `HertbeatIntervall` and `SystemDocumenationService`;
- frozen EV-129 / EV-130 revalidation provenance;
- all root XSDs unchanged;
- synchronized SDK/runtime-mapping counters validated by the hardened manifest consistency checks.

Earlier temporary gate attempts exposed only harness/environment issues: missing local PDF cache, missing `pdftotext`, an unrelated live RFC-2782 string anchor inside the broad EV-129 checker, and unstable extraction of a PDF type token. None changed the reviewed decisions. The final gate deliberately checks only evidence relevant to these three findings.

No executable Known-Issues matcher was added and no XSD was changed.
