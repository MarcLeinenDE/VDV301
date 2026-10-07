# Source-locator review — DR3012V20-004 — 2026-10-07

Status: **complete / visible-body verified / exact official XSD context verified / documentation spelling defect confirmed**.

## Finding

VDV 301-2 Base V2.0 contains the misspelled service name `SystemDocumenationService` in nearby prose although the section heading and exact official XSD use `SystemDocumentationService`.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`
- printed page: **98**

Visible heading:
- `7.2 Dienst SystemDocumentationService`

Immediately below, both language tracks use the typo:
- German prose: `SystemDocumenationService`
- English prose: `SystemDocumenationService`

Exact-byte page-98 PNG SHA-256:
`ef250716223afaa4c777db354f9e54d8ad96664b950cdc5b3312173bfd2eef47`

## Exact XSD context

Selected schema:
- file: `IBIS-IP_SystemDocumentationService_V2.0.xsd`
- local blob: `ab959dddbfa2b8ca420af1b079501f94cff38051`
- official upstream repository: `VDVde/VDV301`
- official tag: `VDV-301-2.0`
- upstream blob: `ab959dddbfa2b8ca420af1b079501f94cff38051`

The exact XSD uses:
- `SystemDocumentationServiceGroup`
- `SystemDocumentationService.GetSystemConfigurationResponse`
- the `SystemDocumentationService` prefix throughout.

No `SystemDocumenationService` alias exists.

## Disproof attempt

The typo is not a distinct translated service name:
- the section heading immediately above is correct;
- both German and English prose repeat the same transposition;
- the exact selected XSD uses only the correct identifier.

## Classification and SDK behavior

Confirmed documentation spelling defect against the selected official service namespace.

- selected XSD remains normative for actual XML/service identifiers;
- `SystemDocumenationService` must not be accepted as an alias;
- SDK behavior: **warning / documentation-derived identifier advisory**;
- no XSD mutation, normalization or waiver is introduced.
