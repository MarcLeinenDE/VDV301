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

## Semantic audit backlog

### SB-001 - Common/Enums V2.4 affected table check

Tables/sections:

```text
LineInformation
StopInformation
TripInformation
DoorCountingObjectClassEnumeration
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
```

Names from the continuation plan not yet confirmed as standalone `IBIS-IP_common_V2.4.xsd` complexType definitions:

```text
NetworkLocationPoint
OperationalInformation
PassengerCounting
PassengerCountingData
PathDestination
Route
```

Observed related fields/concepts:

```text
TripInformation contains RouteDirection.
TripInformation contains PathDestinationNumber.
```

Goal:

```text
Resolve whether each name is:
1. a PDF-only common structure,
2. a service-specific structure in another XSD,
3. an older-version leftover,
4. a differently named XSD structure,
5. or an extraction/planning artefact.

Do not open a CE finding until the scope is confirmed.
```

### SB-006 - visual PDF confirmation for spelling/casing candidates

Findings requiring visual PDF confirmation, not only text extraction:

```text
CE-015 FareZoneInformation Farezone* vs FareZone* casing.
CE-017 TSPPoint Desciption vs expected Description spelling.
```

Goal:

```text
Confirm the printed PDF table spelling before final classification or provider-facing wording.
```
