# Source-locator review — CE-005 through CE-010 — 2026-09-25

Status: **pilot persisted / closure gate pending**.

## Purpose

This is the Phase-B pilot for canonical finding source locators.

It does not change finding assessment, SDK behaviour, runtime disposition or XSD PASS/FAIL authority. It adds exact locations that the future Prüfsdk and a VDV-facing remediation dossier can cite directly.

## Canonical locator model

Each reviewed finding now carries:

- the exact semantic `version_scope` copied as `scope_claims`;
- one version-specific coverage lane per affected document/profile;
- PDF identity by official publication ID, URL and byte SHA-256;
- printed page, section and table;
- XSD identity by filename and exact Git blob;
- stable XSD component/XPath-style locator;
- a concise statement of what is visible at that location.

Line numbers are retained only as non-canonical convenience hints because the Git blob plus component path is the stable identity.

## Pilot findings

`CE-005` — TripInformation AdditionalTextMessage repeatability

Coverage: V2.0, V2.1, V2.2, V2.3 and explicit V2.4 candidate/integration lane.

`CE-006` — DeviceStateEnumeration.warning omitted by PDF

Coverage: V2.2, V2.3 dependency route and explicit V2.4 candidate/integration lane.

`CE-007` — Other/other, Valid/valid, Air/air

Coverage: V1.0, V2.0, V2.1, V2.2, V2.3 dependency route and explicit V2.4 candidate/integration lane.

`CE-008` — Funicular/Taxi casing

Coverage: V2.2, V2.3 dependency route, V2.4 candidate/integration.

`CE-009` — RailSubmode specialRail/specialTrain

Coverage: V2.2, V2.3 dependency route, V2.4 candidate/integration.

`CE-010` — AirSubmode canalBarge omitted by PDF

Coverage: V2.2, V2.3 dependency route, V2.4 candidate/integration.

## Authority safeguards

- The exact selected XSD remains executable XML authority.
- A locator never converts an INVALID result into PASS or a VALID result into failure.
- No V2.4 Common/Enumerations XSD is labelled official release authority.
- No synthetic Enumerations V2.3 file is invented; V2.3 locators identify the actual Enumerations V2.2 dependency blob.
- PDF locations identify the official publication bytes independently of XSD authority.
- No XSD file is changed.

## Pilot counts

```text
semantic findings        192
locator entries            6
complete                    6
partial                     0
remaining                 186
```

The primary gate must validate schema, exact semantic scope projection, exact XSD blobs/components, pilot PDF identities/locations, SDK-manifest integration and the complete root-XSD regression pool.

## Primary gate

Run **36128950500**: **SUCCESS** on HEAD `f7a21412a04d95335691c78a9f8a3d921e97082c`.

The gate validated the locator JSON Schema, exact semantic-scope projection, all six PDF source registrations and byte pins, all 23 version lanes, the expected printed page/table matrix, every stored XSD XPath against the exact pinned Git blob, semantic/runtime manifests, SDK-manifest integration, the full root-XSD regression pool and a clean XSD working tree.
