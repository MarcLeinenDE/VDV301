# Source-locator review — DR3012V20-003 — 2026-10-07

Status: **complete / visible-body verified / version-history mismatch verified / exact official XSD authority verified**.

## Finding

VDV 301-2 Base V2.0 says the heartbeat identifier typo was corrected to `HeartbeatInterval`, but the visible SystemDocumentation tables still print `HertbeatIntervall`.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`

### Page 100 — stale table identifiers

Visible SystemDocumentation tables:
- Table 30: `SystemDocumentationService.SystemConfigurationData`
- Table 31: `SystemDocumentationService.StoreSystemConfigurationRequest`

Both visible rows use:
- identifier: `HertbeatIntervall`
- cardinality: `0:1`
- type: `xs:duration`

Exact-byte page-100 PNG SHA-256:
`fce057d9d8ebf6d8cc69407393c7341ff1fae672cc7df684ed482c02148db9c3`

### Page 105 — version history

Visible section:
- `8 Versionshistorie / Version History`
- `8.1.2 Technische Ergänzungen/Korrekturen / Technical Upgrade/Corrections`

The history explicitly says the SystemDocumentation heartbeat typo was corrected to `HeartbeatInterval`.

Exact-byte page-105 PNG SHA-256:
`0e1bea0141021712bc812bb9987a9e8f1c444ef12729628529060735dda1242a`

## Exact XSD authority

Selected schema:
- file: `IBIS-IP_SystemDocumentationService_V2.0.xsd`
- local blob: `ab959dddbfa2b8ca420af1b079501f94cff38051`
- official upstream: `VDVde/VDV301`
- official tag: `VDV-301-2.0`
- upstream blob: `ab959dddbfa2b8ca420af1b079501f94cff38051`

The local and official-tag blobs are byte-identical.

The XSD declares:
- `SystemDocumentationService.SystemConfigurationData/HeartbeatInterval` as `IBIS-IP.duration`
- `SystemDocumentationService.StoreSystemConfigurationRequestStructure/HeartbeatInterval` as `IBIS-IP.duration`

No `HertbeatIntervall` or historical V1.0 `HeartbeatIntervall` element is declared in the V2.0 schema.

## Disproof attempt

The stale PDF spelling cannot be treated as an allowed V2.0 synonym:
- the V2.0 history says it was corrected;
- the exact official V2.0 XSD uses only `HeartbeatInterval`;
- existing EV-130 executable evidence confirms the selected-XSD boundary.

## Classification and SDK behavior

Confirmed PDF/XSD identifier mismatch with stale body text.

- selected V2.0 XSD remains normative;
- a V2.0 instance using `HertbeatIntervall` or historical `HeartbeatIntervall` is not normalized into `HeartbeatInterval`;
- SDK behavior: **XSD error with explanatory advisory**;
- no alias, waiver or PDF-driven schema override is permitted.
