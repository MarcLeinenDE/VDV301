# XSD enumeration inventory - IBIS-IP_Enumerations_V2.4

Status: generated audit inventory.

Source XSD:

```text
IBIS-IP_Enumerations_V2.4.xsd
```

Machine-readable inventory:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
```

Reproducible exporter:

```text
tools/export_xsd_enumerations.py
```

Suggested command:

```bash
python tools/export_xsd_enumerations.py IBIS-IP_Enumerations_V2.4.xsd \
  --out-csv docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv \
  --out-md docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
```

Important:

```text
This inventory records what the XSD permits.
It does not decide whether a PDF/XSD difference is an XSD defect or a PDF/documentation issue.
XML enumeration values are case-sensitive.
```

## Inventory summary

| Simple type | Count | Notes |
|---|---:|---|
| `ConnectionStateEnumeration` | 3 | Standard common enum. |
| `ConnectionTypeEnumeration` | 2 | Standard common enum. |
| `DataIntervalEnumeration` | 4 | Standard common enum. |
| `DeviceClassEnumeration` | 15 | Includes `MultiFunctionalDisplay` and `CombiDevice`. |
| `DeviceStateEnumeration` | 5 | Contains `warning`; tracked as CE-006 because V2.4 PDF table currently lacks that value. |
| `DeviceTaskEnumeration` | 3 | Standard common enum. |
| `DoorCountingObjectClassEnumeration` | 7 | Contains corrected `Wheelchair`. |
| `DoorCountingQualityEnumeration` | 4 | Standard common enum. |
| `DoorOpenStateEnumeration` | 4 | Standard common enum. |
| `DoorOperationStateEnumeration` | 3 | Standard common enum. |
| `ErrorCodeEnumeration` | 8 | Includes `OperationNotSupported`. |
| `ExitSideEnumeration` | 4 | Lowercase values in XSD. |
| `GNSSCoordinateSystemEnumeration` | 9 | Includes `ETSR89` as present in XSD. |
| `GNSSQualityEnumeration` | 5 | Mixed case values. |
| `GNSSTypeEnumeration` | 8 | Contains `other`; tracked under CE-007 vs PDF `Other`. |
| `JourneyModeEnumeration` | 3 | Standard common enum. |
| `LocationStateEnumeration` | 4 | Standard common enum. |
| `MessageTypeEnumeration` | 3 | Standard common enum. |
| `RouteDeviationEnumeration` | 3 | Lowercase values in XSD. |
| `RouteDirectionEnumeration` | 5 | Standard common enum. |
| `ServiceNameEnumeration` | 22 | Contains `SystemMonitoringService`; older SystemDocumentation/SystemManagement names absent, tracked as CE-004. |
| `ServiceStateEnumeration` | 5 | Standard common enum. |
| `SystemDocumentationInformationEnumeration` | 4 | Present although SystemDocumentationService was removed from ServiceNameEnumeration. |
| `TicketRazziaInformationEnumeration` | 2 | Also contains xs:pattern declarations in XSD; CSV records enumeration values only. |
| `TicketValidationEnumeration` | 3 | Contains `valid`; tracked under CE-007 vs PDF `Valid`. |
| `VehicleModeEnumeration` | 8 | Contains `air`; tracked under CE-007 vs PDF `Air`. |
| `TripStateEnumeration` | 6 | Includes `unknown`. |
| `PtSubModesEnumeration` | 11 | Netex main PT submode selector. |
| `PrivateSubModesEnumeration` | 4 | Netex private submode selector. |
| `RailSubmodeEnumeration` | 18 | Netex/TPEG submode enum. |
| `CoachSubmodeEnumeration` | 11 | Netex/TPEG submode enum. |
| `MetroSubmodeEnumeration` | 5 | Netex/TPEG submode enum. |
| `BusSubmodeEnumeration` | 19 | Netex/TPEG submode enum. |
| `TramSubmodeEnumeration` | 8 | Netex/TPEG submode enum. |
| `WaterSubmodeEnumeration` | 22 | Netex/TPEG submode enum. |
| `AirSubmodeEnumeration` | 17 | Contains `canalBarge` with XSD annotation `Not in TPEG`; keep as audit note. |
| `TelecabinSubmodeEnumeration` | 8 | Netex/TPEG submode enum. |
| `FunicularSubmodeEnumeration` | 5 | Case/spelling candidates tracked under CE-008. |
| `TaxiSubmodeEnumeration` | 10 | Contains `miniCab`; tracked under CE-008 vs PDF spelling/case. |
| `SelfDriveSubmodeEnumeration` | 7 | Netex/TPEG submode enum. |

## Next use in audit

Use the CSV as the XSD-side source of truth for the next PDF comparison step:

```text
1. Extract/record PDF values table-by-table for VDV 301-2-1 V2.4 tables 65-104.
2. Compare PDF values against this CSV exactly and case-sensitively.
3. Classify each delta as OK, OK-with-note, mismatch, or unclear.
4. Do not modify XSD until intent and history are checked.
```
