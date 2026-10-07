# Version-scope boundary review — ARA-002 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding

`ARA-002` is a documentation-only identifier inconsistency inside the official AnalogRadioService V2.4 publication.

The existing visible-body evidence remains:

- printed page 11, section `2.2 DataStructure of SendTelegram Operation / 2.2.1 Request`: the request-structure table labels the last member `TransmitterType`;
- the embedded schema view on the same page uses `Transmitter`;
- the continuation diagram on printed page 12 uses `Transmitter`;
- the complete XML example on printed page 13 uses `<Transmitter>`;
- candidate/integration XSD blob `48fb303b80936d2d762f0889ce0c359e04c16e5b` also uses `Transmitter`, but only as corroboration.

This boundary review does not reclassify candidate XSD authority and does not turn candidate evidence into official executable authority.

## Publication-lineage check

The current VDV publication surfaces were rechecked on 2026-10-07.

Current public VDV entries expose:

- publication: `VDV-Schrift 301-2-19`
- service: `AnalogRadioService`
- version: `V2.4`
- issue: `01/2023`
- languages: German / English

The current VDV IP-KOM-ÖV publication index lists AnalogRadioService only once, as V2.4. The project PDF-source registry likewise contains only `ARA_V2.4`.

No earlier AnalogRadioService publication is available to test as a predecessor and no later AnalogRadioService publication exists to establish a correction boundary.

## Boundary conclusion

- predecessor publication: **none available**
- first affected publication: **V2.4**
- last affected publication: **V2.4**
- successor/correction publication: **none available**
- language boundary: the source is one bilingual German/English publication; this identifier inconsistency belongs to the shared technical structure representation and no separate later language correction exists.

Therefore the existing semantic scope remains exactly:

`V2.4 / documentation_only`

No scope expansion or reduction is required.

## Consequence

Unchanged:

- `TransmitterType` in the table is treated as a PDF/documentation defect;
- implementation guidance points to `Transmitter`;
- no XML alias, normalization or waiver is introduced;
- the separate ARA-001 official-XSD authority gap remains independent.
