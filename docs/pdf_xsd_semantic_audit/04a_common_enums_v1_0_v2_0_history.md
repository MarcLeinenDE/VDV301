# Common/Enums V1.0 -> V2.0 history audit

Status: XSD-side enumeration inventory, first diff and PDF-side first pass completed.

Scope:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
VDV 301-2-1 Common Data Structures and Enumerations V1.x public PDF source
VDV 301-2-1 Common Data Structures and Enumerations V2.0 PDF source
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.0 Common/Enums definitions to a V1.0 service payload unless the selected service/dependency pool actually uses V2.0.
V1.0 and V2.0 must stay separately validatable.
```

## 1. XSD dependency family observation

### Common/Enums V1.0

Observed:

```text
IBIS-IP_common_V1.0.xsd includes IBIS-IP_Enumerations_V1.0.xsd.
```

### Common/Enums V2.0

Observed:

```text
IBIS-IP_common_V2.0.xsd includes IBIS-IP_Enumerations_V2.0.xsd.
```

Initial result:

```text
V1.0 and V2.0 each have their own common/enumeration dependency family in the branch.
No V1.0/V2.0 include-family mismatch is opened in this observation.
```

## 2. XSD enumeration inventories

Created grouped XSD-side inventory:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_v2_0_xsd_inventory.csv
```

Scope of this inventory:

```text
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

Important reproducibility note:

```text
This file is a grouped audit inventory recorded from the XSD files during the audit pass.
It is not yet the row-by-row exporter output format used for the V2.4 inventory.
The exporter/header mismatch noted earlier should still be cleaned up before claiming full automated reproducibility across all versions.
```

## 3. V1.0 -> V2.0 XSD enumeration diff

Created diff files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.md
```

Observed XSD-side deltas:

| Change | V1.0 | V2.0 | Status | Notes |
|---|---|---|---|---|
| Type spelling change | `DataIntervallEnumeration` | `DataIntervalEnumeration` | confirmed XSD delta | Same value set. V2.0 PDF uses `DataIntervalEnumeration`. |
| Type no longer observed | `IBIS-IP-VersionEnumeration` | not observed | confirmed XSD delta | V1.0 XSD had value `1.0`; V2.0 PDF version history says this enumeration was removed. |
| DeviceState value added | - | `readyForShutdown` | confirmed XSD delta | V2.0 PDF/version history confirms the addition. |
| Type added | - | `RouteDirectionEnumeration` | confirmed XSD delta | V2.0 PDF contains the enumeration; public V1.x PDF also contains it as a Version 1.1 change. |
| ServiceName value added | - | `PassengerCountingService` | confirmed XSD delta | V2.0 PDF table/history confirms. |
| ServiceName value added | - | `VideoLiveService` | confirmed XSD delta | V2.0 PDF table/history confirms. |
| ServiceName value added | - | `VideoRecordingService` | confirmed XSD delta | V2.0 PDF table/history confirms. |
| ServiceName value added | - | `VideoDisplayService` | confirmed XSD delta | V2.0 PDF table/history confirms. |
| ServiceState value added | - | `starting` | confirmed XSD delta | V2.0 PDF table contains `starting`; source/history check complete for first pass. |

## 4. Public V1.0 source-labelling note

The official VDV publication index exposes a Common/Enums `V1.0` PDF link. The opened public PDF itself is dated `05/2017` and contains a Version History section with explicit `Version 1.1` changes.

Important consequence:

```text
Treat the available public V1.0 link as a V1.x / V1.1-consolidated source for this first pass.
Do not treat it as a clean untouched V1.0 baseline without further evidence.
Do not open a CE finding merely because the public V1.x PDF already contains items that are absent from IBIS-IP_Enumerations_V1.0.xsd.
```

Examples of this source-labelling ambiguity:

```text
The public V1.x PDF contains RouteDirectionEnumeration, while the V1.0 XSD inventory used here does not.
The public V1.x PDF contains PassengerCountingService / ServiceState starting in its tables, while the V1.0 XSD inventory used here does not.
The public V1.x version history itself explains several Version 1.1 changes.
```

Follow-up:

```text
Locate or confirm whether an original pure V1.0 baseline PDF exists separately.
Until then, keep V1.0 vs V1.x table mismatches as source-provenance notes, not new findings.
```

## 5. V2.0 PDF-side first pass

The V2.0 PDF is explicitly identified as `VDV-Schrift 301-2-1 V2.0`, dated `02/2018`.

The V2.0 PDF version history confirms the following relevant deltas:

```text
ServiceNameEnumeration updated with PassengerCountingService.
ServiceNameEnumeration updated with VideoLiveService, VideoRecordingService and VideoDisplayService.
IBIS-IP-VersionEnumeration removed.
DeviceStateEnumeration extended with readyForShutdown.
DisplayContent in Connection changed to minOccurs=0.
TripInformation.AdditionalTextMessage changed to maxOccurs=unbounded.
Typo ExpectedDepatureTime in Common V1.0/V1.1 fixed to ExpectedDepartureTime in Common V2.0.
```

The V2.0 PDF tables confirm or expose these first-pass observations:

```text
DataIntervalEnumeration exists under the corrected spelling.
DeviceStateEnumeration lists readyForShutdown.
RouteDirectionEnumeration exists.
ServiceNameEnumeration lists PassengerCountingService and video services.
ServiceStateEnumeration lists starting.
TripInformation.AdditionalTextMessage is documented as 0:* InternationalTextType.
TicketValidationEnumeration is printed as Valid, while XSD uses valid.
VehicleModeEnumeration is printed as Air, while XSD uses air.
GNSSTypeEnumeration is printed as Other, while XSD uses other.
```

## 6. PDF/XSD first-pass classification

| Topic | First-pass classification | Finding impact |
|---|---|---|
| `DataIntervallEnumeration` -> `DataIntervalEnumeration` | V2.0 PDF and V2.0 XSD align on corrected spelling. | No new CE. Keep as historical delta. |
| `IBIS-IP-VersionEnumeration` removed | V1.0 XSD contains it; V2.0 XSD omits it; V2.0 PDF history says removed. | No new CE. |
| `readyForShutdown` | V2.0 PDF and V2.0 XSD align. | Supports that CE-006 is about later `warning`, not `readyForShutdown`. |
| `RouteDirectionEnumeration` | V2.0 PDF and XSD align. Public V1.x PDF already contains it as V1.1-era material. | No new CE; relevant context for TVS-002. |
| `ServiceNameEnumeration` additions | V2.0 PDF and XSD align for PassengerCountingService and video services. | No new CE; CE-004 later concerns V2.2/V2.4 removal of old services. |
| `ServiceStateEnumeration starting` | V2.0 PDF and XSD align. | No new CE. |
| `TripInformation.AdditionalTextMessage` | V2.0 PDF/history says 0:* / maxOccurs unbounded; V2.0 XSD has no maxOccurs and therefore max 1. | Supports CE-005 for V2.0. Final range update deferred to historical closure. |
| `TicketValidationEnumeration Valid/valid` | V1.x and V2.0 PDFs print `Valid`; V1.0/V2.0 XSDs use `valid`. | Supports historical range for CE-007. Final range update deferred. |
| `VehicleModeEnumeration Air/air` | V1.x and V2.0 PDFs print `Air`; V1.0/V2.0 XSDs use `air`. | Supports historical range for CE-007. Final range update deferred. |
| `GNSSTypeEnumeration Other/other` | V1.x and V2.0 PDFs print `Other`; V1.0/V2.0 XSDs use `other`. | Supports historical range for CE-007. Final range update deferred. |
| `DoorCountingObjectClassEnumeration` wording | V1.x/V2.0 PDF extraction shows `Wheelchair` / `Others`; XSD uses `WheelChair` / `Other`. | Historical candidate only; needs broader check before opening a new finding. |
| `TSPPoint Description` | V2.0 PDF table uses `Description`. | Relevant historical support for CE-017; visual/manual V2.4 check remains deferred. |
| `ZoneType FarezoneType*` | V2.0 PDF table uses `FarezoneTypeID` / `FarezoneTypeName`. | Relevant to CE-015/ZoneType history; final visual/manual check remains deferred. |

## 7. XSD comment / history signal

The V2.0 enumeration XSD contains an internal comment indicating relevant edits:

```text
Video services added in ServiceNameEnumeration.
Video enumerations removed.
DeviceStateEnumeration extended by readyForShutdown.
Date in comment: 2018-01-22.
```

The first diff and V2.0 PDF check confirm these parts:

```text
VideoLiveService / VideoRecordingService / VideoDisplayService added to ServiceNameEnumeration.
DeviceStateEnumeration adds readyForShutdown.
```

The comment part `Video enumerations removed` remains only an editor-history note in this pass:

```text
No separate video-specific enumeration type was observed in the fetched V1.0 enumeration XSD inventory used here.
Do not open a finding from that note without repository/PDF history evidence.
```

## 8. Finding state decision

Status after this pass:

```text
No new CE finding opened.
No XSD change proposed.
No existing finding state changed in findings.md during this pass.
```

Reason:

```text
The V2.0 PDF confirms several XSD-side deltas.
The public V1.0 source behaves like a V1.x / V1.1-consolidated source and must not be over-interpreted as pure V1.0.
CE-005 and CE-007 receive stronger historical support, but final affected-version ranges should be updated in the dedicated historical closure file after the full Common/Enums V1.0 -> V2.4 chain is checked.
```

## 9. Validation backlog impact

Later technical validation should include version-specific pools:

```text
Common/Enums V1.0 pool:
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_Enumerations_V1.0.xsd

Common/Enums V2.0 pool:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
```

The pools must be compiled separately.

## 10. Next work inside the historical block

Next detailed audit file:

```text
docs/pdf_xsd_semantic_audit/04b_common_enums_v2_0_v2_1_history.md
```

Required next steps:

```text
1. Compare Common/Enums V2.0 and V2.1 XSD include families and enumeration deltas.
2. Check VDV 301-2-1 V2.1 PDF version history and affected tables.
3. Track whether CE-004, CE-005, CE-007 and other existing findings are inherited, introduced or corrected in V2.1.
```

## 11. Result

```text
Common/Enums V1.0 -> V2.0 historical audit now has XSD-side diff plus PDF-side first pass.
V2.0 PDF confirms the main V2.0 XSD-side changes.
The public V1.0 PDF source is treated as V1.x / V1.1-consolidated until a pure V1.0 baseline is confirmed.
No new finding opened yet.
Next: V2.0 -> V2.1 historical audit.
```