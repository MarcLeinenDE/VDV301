# Schema profiles

This directory contains resolver metadata for the VDV301 integration/superbranch.

Files here are **not official VDV XSDs**. They describe how the tool/SDK should assemble validation roles from official XSD material without duplicating complete historical release snapshots.

Rules:

```text
- XSD field/type validation always follows the selected official/candidate XSD file and its exact dependencies.
- Resolver metadata may provide operation-root -> type mappings that were historically carried by an aggregate XSD.
- Resolver metadata must record its official source tag/blob.
- No resolver metadata may silently invent or rename an operation root.
- A generated harness built from this metadata is an integration validation adapter, not an official VDV schema file.
```

Current legacy profile:

```text
VDV-301-1.0-root-map.csv
```

It carries only the operation-root declarations needed for V1.0 service XSDs that remain type-only in the deduplicated superbranch:

```text
CustomerInformationService V1.0
DeviceManagementService V1.0
SystemDocumentationService V1.0
```

Source of those root declarations:

```text
VDVde/VDV301 tag VDV-301-1.0
IBIS_IP_V1.0.xsd
blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```
