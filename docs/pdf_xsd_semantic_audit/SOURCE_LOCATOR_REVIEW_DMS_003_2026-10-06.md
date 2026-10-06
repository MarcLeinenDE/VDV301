# Source-locator review — DMS-003 — 2026-10-06

Status: **structurally complete / visible-body verified / version-specific cardinality confirmed**.

## Finding

DMS-003 is not a defect in the historical profiles. The `ErrorMessage` lower bound changes by selected DMS version:

- V2.0: `10:*`
- V2.1: `10:*`
- V2.2: `10:*`
- V2.4: `0:*`

The V2.4 relaxation must not be back-applied to V2.0–V2.2.

## Visible PDF evidence

- V2.0, byte-pinned `VDV301-2_BASE_V2.0`, printed page 95: GetDeviceErrorMessages response data shows `ErrorMessage 10:*`.
- V2.1, byte-pinned `VDV301-2_BASE_V2.1`, printed page 100: Table 20 shows `ErrorMessage 10:*`.
- V2.2, byte-pinned `DMS_V2.2`, printed page 20: Table 9 shows `ErrorMessage 10:*`.
- V2.4, byte-pinned `DMS_V2.4`, printed page 19: Table 9 shows `ErrorMessage 0:*` and states that at least 10 messages are useful if available.

## Exact XSD authority

- V2.0 official blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`, line 84: `minOccurs="10" maxOccurs="unbounded"`.
- V2.1 official blob `191b43e01cdaba14b247725689a913c244a67eed`, lines 213 and 497: `minOccurs="10" maxOccurs="unbounded"`.
- V2.2 official blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, lines 189 and 450: `minOccurs="10" maxOccurs="unbounded"`.
- V2.4 candidate/integration blob `d222dfd98b2be3777576388da7ace8f333d24c3f`, lines 189 and 450: `minOccurs="0" maxOccurs="unbounded"`.

The V2.4 schema remains candidate/integration authority and is not relabelled as official.

## Executable evidence

EV-127, run `33762375705`, confirms the selected-profile boundaries:

- V2.0–V2.2: 9 entries reject; 10 and 11 accept.
- V2.4 candidate/integration: 0 and 1 entries accept.

## Active disproof

Rejected interpretation: V2.4 demonstrates that the older lower bound of 10 was erroneous.

The historical PDFs and selected official XSDs align at `10:*`, and executable validation confirms the same boundary. V2.4 is a later relaxation/correction context, not a retroactive rewrite of prior release authority.

## SDK consequence

No extra runtime diagnostic is needed. Ordinary validation against the exact selected XSD already enforces the correct version-specific cardinality.

No XSD mutation, alias, or latest-version substitution is authorized.
