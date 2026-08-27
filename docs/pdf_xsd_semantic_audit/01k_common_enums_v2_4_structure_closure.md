# Common structures / enumerations V2.4 - structure closure pass

Status: started, closure pass partial; SB-005 resolved; visual-only checks deferred.

Scope:

```text
VDV 301-2-1 V2.4 common data structures after the table-level passes in 01h, 01i and 01j.
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

## 1. Inputs reviewed

Detailed audit files used as input:

```text
01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
01g_common_enums_v2_4_datatypes_core_structures.md
01h_common_enums_v2_4_core_data_structures.md
01i_common_enums_v2_4_remaining_data_structures_part1.md
01j_common_enums_v2_4_remaining_data_structures_part2.md
01l_common_enums_v2_4_deferred_scope_resolution.md
```

Supporting registers:

```text
findings.md
validation_backlog.md
OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

## 2. Closure status summary

### Closed / OK in current audit evidence

```text
Wrapper datatypes 1.1-1.16
InternationalTextType structure
Announcement
BayArea
BeaconPoint
CardApplInformation
CardTicketData
DataAcceptedResponse
DataAcceptedResponseData
DataVersion
Destination
DoorCounting
DoorCountingList
DoorInformation
DoorOpenState
DoorOperationState
DoorState
DisplayContent
GNSSCoordinate
GNSSPoint
JourneyStopInformation checked core fields
LineInformation V2.4 additions
Point / PointType checked core shape
SpecificPoint
StopInformation V2.4 additions
StopInformationRequest checked core fields
StopSequence
TimingPoint
TripInformation V2.4 additions except CE-005
ViaPoint
```

### Closed with note / validation follows XSD

```text
CE-002 StopPointNumber wording vs PointNumber table/XSD
CE-004 ServiceNameEnumeration older service names still visible in PDF table
CE-006 DeviceState warning XSD-only value
CE-007 case-sensitive enum differences Other/Valid/Air vs other/valid/air
CE-008 submode case differences Unknown/Undefined/minicab vs unknown/undefined/miniCab
CE-009 RailSubmode specialRail vs specialTrain
CE-010 AirSubmode canalBarge XSD-only value
CE-011 Connection TransportMode/ConnectionMode PDF 0:* vs XSD 0:1
CE-012 DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*
CE-013 AdditionalAnnouncement InformationAtSpecificPoint vs SpecificPoint
CE-014 DataVersionList PDF 1:* vs XSD 0:*
CE-016 GlobalCardStatusID vs GlobalCardStausID
CE-017 TSPPoint Desciption spelling candidate
```

These items are not fixed during this audit. They become provider-facing notes and, where appropriate, possible later official PR candidates after full audit completion and revalidation.

### Deferred visual PDF confirmation

```text
CE-015 FareZoneInformation Farezone* vs FareZone* casing
CE-017 TSPPoint Desciption vs Description spelling
ZoneType first-field casing/spelling if the PDF differs from XSD FarezoneTypeID
```

These checks require manual/visual PDF confirmation. They are deferred by user request and no longer block non-visual audit work.

## 3. SB-005 deferred names resolved

SB-005 has been resolved in:

```text
docs/pdf_xsd_semantic_audit/01l_common_enums_v2_4_deferred_scope_resolution.md
```

Result:

| Deferred name | Closure classification | Follow-up |
|---|---|---|
| NetworkLocationPoint | not a Common V2.4 standalone type; service-specific / older V1.0 NetworkLocation scope | NetworkLocationService V1.0 audit |
| PassengerCounting | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PassengerCountingData | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PathDestination | field-level TripInformation usage as `PathDestinationNumber` | already covered in TripInformation audit |
| Route | JourneyInformationService V1.0 element using `TripInformationStructure` | JourneyInformationService V1.0 audit |
| OperationalInformation | not confirmed as Common V2.4 complexType; routing note only | revisit only with concrete PDF/XSD evidence |

Closure decision:

```text
SB-005 no longer blocks Common/Enums V2.4 first-pass closure.
No new CE finding opened.
No XSD change proposed.
```

## 4. Official PR candidate handling

The audit has a separate register:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Important rule:

```text
Do not open official correction PRs during the audit.
At the end of the full audit, recheck all candidate findings together, validate locally, compare against current upstream and open PRs, then decide whether a minimal official PR is justified.
```

Initial candidates tracked there:

```text
PR-CAND-001 GlobalCardStausID spelling, linked CE-016
PR-CAND-002 TSPPoint Desciption spelling, linked CE-017
PR-CAND-003 AdditionalAnnouncement InformationAtSpecificPoint vs SpecificPoint, linked CE-013
PR-CAND-004 cardinality discrepancy candidates, linked CE-011/CE-012/CE-014
```

## 5. Tool behaviour consequence

For the eventual VDV301 Tool / SDK logic:

```text
1. XSD validation result is authoritative.
2. PDF/XSD discrepancy is shown as contextual explanation.
3. Typo-like XSD names are not silently corrected by the tool.
4. Provider-facing text should explain why a PDF-oriented implementation may fail.
```

Example:

```text
FAIL: <GlobalCardStatusID> is not accepted by the XSD.
Allowed by current XSD: <GlobalCardStausID>.
PDF note: The PDF table lists GlobalCardStatusID; this looks like a typo-like schema/documentation discrepancy. Because the VDV 301-2 V2.4 conventions give XSD precedence in case of inconsistency, validation follows the XSD.
```

## 6. Current Common/Enums V2.4 closure state

Current state:

```text
Common/Enums V2.4 first-pass structure audit can continue with visual-only checks deferred.
SB-005 is resolved and no longer blocks closure.
```

Deferred items:

```text
1. Visually confirm CE-015 FareZoneInformation casing.
2. Visually confirm CE-017 TSPPoint Desciption/Description spelling.
3. Decide whether ZoneType needs its own finding or is covered by CE-015.
```

Decision:

```text
Do not wait for these visual checks before continuing the overall PDF/XSD audit.
Carry them in SB-006 until the user can perform the manual visual confirmation.
```

## 7. Next step

Next non-visual audit action:

```text
Continue with DeviceManagementService V2.4 audit integration.
```

Implemented in:

```text
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
```
