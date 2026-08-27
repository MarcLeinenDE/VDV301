# Common/Enums V1.0 -> V2.0 history audit

Status: XSD-side enumeration inventory and first diff completed; PDF-side check pending.

Scope:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
VDV 301-2-1 Common Data Structures and Enumerations V1.0 / V2.0 PDF side, still to be checked in detail
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
No V1.0/V2.0 include-family mismatch is opened in this first observation.
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
| Type spelling change | `DataIntervallEnumeration` | `DataIntervalEnumeration` | confirmed XSD delta | Same value set; PDF/history check pending. |
| Type no longer observed | `IBIS-IP-VersionEnumeration` | not observed | confirmed XSD delta | V1.0 had value `1.0`; PDF/history check pending. |
| DeviceState value added | - | `readyForShutdown` | confirmed XSD delta | V2.0 XSD comment explicitly mentions this. |
| Type added | - | `RouteDirectionEnumeration` | confirmed XSD delta | PDF/history check pending. |
| ServiceName value added | - | `PassengerCountingService` | confirmed XSD delta | PDF/history check pending. |
| ServiceName value added | - | `VideoLiveService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceName value added | - | `VideoRecordingService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceName value added | - | `VideoDisplayService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceState value added | - | `starting` | confirmed XSD delta | PDF/history check pending. |

## 4. XSD comment / history signal

The V2.0 enumeration XSD contains an internal comment indicating relevant edits:

```text
Video services added in ServiceNameEnumeration.
Video enumerations removed.
DeviceStateEnumeration extended by readyForShutdown.
Date in comment: 2018-01-22.
```

The first diff confirms these parts directly from the current branch XSDs:

```text
VideoLiveService / VideoRecordingService / VideoDisplayService added to ServiceNameEnumeration.
DeviceStateEnumeration adds readyForShutdown.
```

The comment part `Video enumerations removed` remains only an editor-history note in this pass:

```text
No separate video-specific enumeration type was observed in the fetched V1.0 enumeration XSD inventory used here.
Do not open a finding from that note without repository/PDF history evidence.
```

## 5. First classification

Status so far:

```text
OK to continue.
No new CE finding opened from the V1.0 -> V2.0 XSD-side diff alone.
```

Reason:

```text
The observed changes are XSD-side historical deltas.
They become findings only if the matching V1.0/V2.0 PDF version history or tables contradict, omit or misstate them after PDF-side checking.
```

Potential historical closure targets:

```text
CE-006 DeviceStateEnumeration: readyForShutdown exists already in V2.0, while warning is a later V2.4 XSD-only issue.
CE-004 ServiceNameEnumeration: old SystemDocumentationService/SystemManagementService are still present in V1.0 and V2.0; later removal history must be checked in V2.2+.
TVS-002 context: RouteDirectionEnumeration exists as a Common/Enums V2.0 type, but TVS V2.4 XSD uses RouteDeviationEnumeration for VehicleData.RouteDeviation.
```

No finding state is changed yet.

## 6. Validation backlog impact

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

## 7. Next work inside this block

Required next steps:

```text
1. Extract/check VDV 301-2-1 V1.0 PDF version history and enumeration tables.
2. Extract/check VDV 301-2-1 V2.0 PDF version history and enumeration tables.
3. Compare those PDF-side facts to the XSD deltas listed here.
4. Decide whether any existing CE finding version ranges need updates.
5. Then continue with V2.0 -> V2.1.
```

## 8. Result

```text
Common/Enums V1.0 -> V2.0 historical audit has moved from first observation to XSD-side diff completed.
V1.0 and V2.0 include-family observation is clean.
V1.0 vs V2.0 enumeration deltas are recorded.
No new finding opened yet.
PDF-side confirmation is the next required step.
```