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
