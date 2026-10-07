# Version-scope boundary review — ARA-001 — 2026-10-07

Status: **verified / scope unchanged / current upstream authority rechecked**.

## Finding

`ARA-001` records the AnalogRadioService V2.4 release-authority gap: an official VDV publication exists, but a matching official release-tagged XSD authority is not established; the available project XSD is candidate/integration material.

## Publication boundary

Current official VDV publication surfaces were checked again on 2026-10-07.

- VDV publication number: **301-2-19**
- service: **AnalogRadioService**
- published service version: **V2.4**
- issue: **01/2023**
- language: **German / English**
- project pinned source: `ARA_V2.4`
- PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`

The current VDV IP-KOM-ÖV publication index and the project source registry expose no earlier or later AnalogRadioService publication. V2.4 is therefore both the first and the last available publication in this service lineage at the review date.

## Official GitHub release authority

Current official upstream was rechecked rather than carrying the old authority result forward.

- repository: `VDVde/VDV301`
- current master: `14880bb33beec5c5dffe96315b730bd6c094a585`
- latest official GitHub release: `VDV-301-2.3`
- official releases present: `VDV-301-1.0`, `VDV-301-2.0`, `VDV-301-2.1`, `VDV-301-2.2`, `VDV-301-2.3`
- `VDV-301-2.4`: **not present**
- `IBIS-IP_AnalogRadioService_V2.4.xsd` on current official master: **not present (404)**

The existing integration XSD blob `48fb303b80936d2d762f0889ce0c359e04c16e5b` therefore remains candidate/integration authority only.

## Boundary conclusion

- predecessor publication: **none available**
- first affected publication: **AnalogRadioService V2.4**
- last affected publication: **AnalogRadioService V2.4**
- successor publication/correction boundary: **none available**
- bilingual split: **none** for this authority-gap finding; German and English are tracks of the same V2.4 publication and have the same release-authority state.

The existing semantic scope is **confirmed unchanged**:

1. V2.4 official documentation / unresolved official strict-XSD authority.
2. V2.4 candidate/integration XSD authority.

No earlier or later service version is added.

## SDK consequence

Unchanged:

- official strict V2.4 XSD profile remains fail-closed/unsupported;
- candidate/integration V2.4 may be selected only explicitly and must remain labelled non-official;
- exact selected candidate XSD still governs PASS/FAIL when that candidate profile is explicitly selected.

No XSD mutation, alias, normalization or waiver is introduced.
