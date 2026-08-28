# Deep Read superbranch backfill — SystemDocumentationService V2.0

Date: 2026-08-28
Trigger: fresh Deep Read of VDV 301-2 Base Services V2.0

## Discovery

The audited superbranch contained `IBIS-IP_SystemDocumentationService_v1.0.xsd` but not the official V2.0 service schema, even though the official `VDVde/VDV301` release tag `VDV-301-2.0` contains:

`IBIS-IP_SystemDocumentationService_V2.0.xsd`

Official Git blob:

`ab959dddbfa2b8ca420af1b079501f94cff38051`

## Backfill

The file was copied byte-for-byte from the exact official release tag. Creating the Git blob from the fetched content produced the same blob SHA:

`ab959dddbfa2b8ca420af1b079501f94cff38051`

No XSD content was edited.

Authority: `official`
Source: `VDVde/VDV301`, tag `VDV-301-2.0`

Direct dependencies in the official file:

- `IBIS-IP_common_V2.0.xsd`
- `IBIS-IP_Enumerations_V2.0.xsd`

## Important service-version distinction

The same official `VDV-301-2.0` release tag contains `IBIS-IP_SystemManagementService_V1.0.xsd`; no `IBIS-IP_SystemManagementService_V2.0.xsd` is present there.

Therefore the Base Services V2.0 publication/release context must not be interpreted as a blanket rule that every base service uses service-XSD version 2.0. Exact service-specific routing remains required.

## Validation status

Byte/provenance identity is confirmed. Compilation/profile-generator evidence for the expanded 50-root inventory must be executed separately before claiming the new root count as validated.
