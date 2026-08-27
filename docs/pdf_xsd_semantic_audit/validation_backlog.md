# PDF/XSD semantic audit validation backlog

Status: started.

## Local technical validation backlog

These checks require a local checkout or downloaded XSD pool.

### VB-001 - compile common/enums pool

Scope:

```text
IBIS-IP_common_V2.1.xsd + IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_common_V2.2.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.3.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.4.xsd + IBIS-IP_Enumerations_V2.4.xsd
```

Goal:

```text
All includes resolve.
No duplicate type definition conflicts within a selected version pool.
XSD parser accepts every selected schema.
```

### VB-002 - targeted XML samples for Common/Enums V2.4

Initial sample structures:

```text
LineInformation with LinePublicCode / LineSymbolText / ExternalLineRef
StopInformation with StopShortName / StopLongNo / PointNumber / StopGlobalID / StopPointGlobalID
TripInformation with BlockNumber
DoorCountingObjectClassEnumeration with Wheelchair
```

Goal:

```text
Positive samples validate.
Negative samples fail where expected.
```

### VB-003 - version-family include verification

Goal:

```text
Confirm whether common V2.3 intentionally uses Enumerations V2.2.
Confirm V2.4 service candidates consistently use common V2.4 / Enumerations V2.4 when semantically required.
```

### VB-004 - end-of-audit local validation for official PR candidates

Source:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Goal:

```text
Before any official correction PR is prepared, run local XSD compilation and targeted positive/negative XML validation for the exact proposed change.
```

This applies especially to typo-like candidates such as:

```text
CE-016 / PR-CAND-001 GlobalCardStausID
CE-017 / PR-CAND-002 TSPPoint Desciption
```

## Semantic audit backlog

### SB-001 - Common/Enums V2.4 affected table check

Tables/sections:

```text
LineInformation
StopInformation
TripInformation
DoorCountingObjectClassEnumeration
```

Status:

```text
Covered in first-pass Common/Enums V2.4 audit files; keep open for later history/validation closure.
```

### SB-002 - Common/Enums V2.3 affected table check

Tables/sections:

```text
DisplayContent
StopInformation
StopInformationRequest
TripInformation
```

### SB-003 - Common/Enums V2.2 affected table check

Tables/sections:

```text
DisplayContent / LineCode area
TripStateEnumeration
Connection / ConnectionMode / NetexMode
Mode/SubMode enumerations
DeviceClassEnumeration
ServiceNameEnumeration
```

### SB-004 - Common/Enums V2.1 affected table check

Tables/sections:

```text
DeviceClassEnumeration
ErrorCodeEnumeration
ServiceNameEnumeration
InternationalTextType
DestinationStructure
DisplayContent
```

### SB-005 - Common/Enums V2.4 deferred structure-name scope resolution

Source:

```text
docs/pdf_xsd_semantic_audit/01j_common_enums_v2_4_remaining_data_structures_part2.md
docs/pdf_xsd_semantic_audit/01k_common_enums_v2_4_structure_closure.md
docs/pdf_xsd_semantic_audit/01l_common_enums_v2_4_deferred_scope_resolution.md
```

Status:

```text
Resolved for Common/Enums V2.4 first-pass closure.
No new CE finding opened.
```

Resolution:

| Name | Classification | Follow-up |
|---|---|---|
| NetworkLocationPoint | service-specific / older V1.0 NetworkLocation scope | NetworkLocationService V1.0 audit |
| PassengerCounting | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PassengerCountingData | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PathDestination | field-level TripInformation usage | already covered as PathDestinationNumber |
| Route | service-specific JourneyInformation element using TripInformationStructure | JourneyInformationService V1.0 audit |
| OperationalInformation | not confirmed / routing note only | revisit only with concrete PDF/XSD evidence |

### SB-006 - visual PDF confirmation for spelling/casing candidates

Findings requiring visual PDF confirmation, not only text extraction:

```text
CE-015 FareZoneInformation Farezone* vs FareZone* casing.
CE-017 TSPPoint Desciption vs expected Description spelling.
ZoneType first-field casing/spelling if PDF differs from XSD FarezoneTypeID.
```

Goal:

```text
Confirm the printed PDF table spelling before final classification or provider-facing wording.
```

Status:

```text
Next Common/Enums V2.4 closure task.
```

### SB-007 - post-audit official PR candidate review

Source:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Goal:

```text
At the end of the full PDF/XSD audit, review all CE findings and decide whether any minimal official-facing PRs should be prepared.
No official PR is opened from this register during the audit.
```

Required review steps:

```text
1. Re-fetch current VDVde/VDV301 upstream state.
2. Check open/merged PRs for duplicate fixes.
3. Re-check PDF table spelling visually where relevant.
4. Check historical XSD/PDF versions.
5. Run local schema compilation and targeted sample validation.
6. Split candidates into documentation-only notes, tool notes, validation backlog items and possible official PRs.
7. Ask the user for explicit approval before preparing or opening any PR.
```
