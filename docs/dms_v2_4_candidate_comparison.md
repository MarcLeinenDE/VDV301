# DMS V2.4 candidate variant comparison

Status: development comparison note, not an official VDV release file.

This document compares two conservative candidate variants for a future
`IBIS-IP_DeviceManagementService_V2.4.xsd` upstream pull request.

The actual XSD candidates are generated locally with:

```bash
python tools/derive_dms_v2_4_candidates.py --repo-root .
```

The generator reads the official baseline file
`IBIS-IP_DeviceManagementService_V2.2.xsd` and creates both candidate variants
under `generated/dms-v2.4-candidates/`.

## Common derivation rules for both variants

Both variants apply only the documented DMS V2.4 changes:

1. `DeviceManagementService.GetDeviceErrorMessagesResponseData / ErrorMessage`
   becomes optional (`minOccurs="0"`, `maxOccurs="unbounded"`).
2. `SubdeviceErrorMessages / ErrorMessage` becomes optional
   (`minOccurs="0"`, `maxOccurs="unbounded"`).
3. `DeviceStatusImpact` becomes optional.
4. `DeviceStatusPriority` becomes optional.
5. In `DeviceManagementService.InstallUpdateRequestStructure` only:
   `UpdateID`, `UpdateTimestamp`, and `UpdateURL` become optional.
6. Existing optional `UpdateFileChecksum` and `UpdateFileSize` stay unchanged.
7. Similarly named fields outside `InstallUpdateRequestStructure` stay mandatory.

The generator intentionally fails if the exact source patterns are not found, so
accidental broad replacements are avoided.

## Variant A: existing-repository dependencies

Generated path:

```text
generated/dms-v2.4-candidates/variant_a_existing_repository_dependencies/IBIS-IP_DeviceManagementService_V2.4.xsd
```

Dependency decision:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.3.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>
```

Assessment:

- Smallest practical DMS-only PR shape.
- Uses only dependency files already present in the official repository.
- Avoids adding Common/Enumerations V2.4 to the same PR.
- Does not resolve the broader V2.4 schema-family consistency issue.
- Less elegant for a V2.4 service schema, because it does not use the V2.4
  Common/Enumerations candidate family.

Use case:

- Suitable if maintainers prefer a very small DMS-only PR and want to review
  Common/Enumerations V2.4 separately.

## Variant B: V2.4 schema-family dependencies

Generated path:

```text
generated/dms-v2.4-candidates/variant_b_v24_schema_family_dependencies/IBIS-IP_DeviceManagementService_V2.4.xsd
```

Dependency decision:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.4.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
```

Assessment:

- More consistent with a complete V2.4 schema family.
- Aligns with the existing official `TicketValidationService V2.4` direction,
  which already references `IBIS-IP_common_V2.4.xsd`.
- Requires `IBIS-IP_common_V2.4.xsd` and `IBIS-IP_Enumerations_V2.4.xsd` to be
  included or already accepted by maintainers.
- Requires the known `TicketValidationService V2.4` mixed-include issue to be
  handled consistently.
- Larger review scope than a DMS-only PR.

Use case:

- Suitable if maintainers accept a schema-pool completion PR rather than a tiny
  DMS-only addition.

## Current recommendation

Do not open an upstream PR yet.

Preferred next review step:

1. Generate both variants locally.
2. Compile the complete selected schema pool for Variant A and Variant B.
3. Run positive and negative XML sample validations for DMS V2.4.
4. Choose PR strategy:
   - either a tiny DMS-only PR based on Variant A;
   - or a broader V2.4 schema-family PR based on Variant B after separately
     reviewing Common/Enumerations V2.4.

At the moment, Variant B is technically cleaner as a V2.4 family model, but
Variant A is easier for a minimal upstream PR review.
