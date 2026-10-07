# Version-scope boundary review — ARA-003 — 2026-10-07

Status: **verified / scope unchanged / candidate authority lane rechecked**.

## Finding

`ARA-003` is the AnalogRadioService V2.4 cardinality contradiction for the transmitter member.

Existing visible-body and executable evidence remains:

- official PDF printed page 11: the request-structure table states `TransmitterType 1:1`;
- embedded schema view on the same page shows `Transmitter` with `minOccurs=0`;
- candidate/integration XSD blob `48fb303b80936d2d762f0889ce0c359e04c16e5b` defines `Transmitter` as 0:1;
- EV-105 run `33228250613`, job `99036090357`, executable-confirms that candidate/integration instances both with and without `Transmitter` validate.

The executable result remains candidate/integration-only.

## Publication-lineage boundary

Current VDV publication surfaces were rechecked on 2026-10-07.

The current VDV catalog exposes AnalogRadioService only as:

- publication: `VDV-Schrift 301-2-19`
- service: `AnalogRadioService`
- version: `V2.4`
- issue: `01/2023`
- languages: German / English

No earlier AnalogRadioService publication is present and no later AnalogRadioService publication is currently listed.

## Current official GitHub authority

The current official upstream was rechecked independently of the stored historical evidence:

- repository: `VDVde/VDV301`
- current `master`: `14880bb33beec5c5dffe96315b730bd6c094a585`
- latest official release remains `VDV-301-2.3`
- `VDV-301-2.4` official release: not present
- `IBIS-IP_AnalogRadioService_V2.4.xsd` on current official master: not present

Therefore the existing V2.4 candidate/integration XSD remains provenance-distinct from official release authority.

## Boundary conclusion

- predecessor publication: **none available**
- first affected publication: **V2.4**
- last affected publication: **V2.4**
- successor/correction publication: **none available**
- candidate executable lane: **V2.4 candidate/integration only**
- bilingual split: none for the technical cardinality contradiction; both language tracks share the same technical representation.

The existing semantic scope is confirmed unchanged:

1. `V2.4 / documentation_only`
2. `V2.4 candidate/integration / candidate_integration`

No earlier or later version is added.

## SDK consequence

Unchanged:

- the official PDF inconsistency remains informational/documentation defect knowledge;
- when the explicit candidate/integration profile is selected, exact candidate XSD behavior remains normative for that selected profile;
- candidate behavior must not be presented as official V2.4 release conformance;
- no alias, normalization, cardinality override or waiver is introduced.
