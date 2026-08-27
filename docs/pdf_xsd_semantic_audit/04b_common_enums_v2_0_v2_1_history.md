# Common/Enums V2.0 -> V2.1 history audit

Status: XSD-side enumeration diff and PDF-side first pass completed.

Scope:

```text
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
IBIS-IP_common_V2.1.xsd
IBIS-IP_Enumerations_V2.1.xsd
VDV 301-2-1 Common Data Structures and Enumerations V2.1 PDF source
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.1 Common/Enums definitions to a V2.0 service payload unless the selected service/dependency pool actually uses V2.1.
V2.0 and V2.1 must stay separately validatable.
```

## 1. XSD dependency family observation

### Common/Enums V2.0

Observed:

```text
IBIS-IP_common_V2.0.xsd includes IBIS-IP_Enumerations_V2.0.xsd.
```

### Common/Enums V2.1

Observed:

```text
IBIS-IP_common_V2.1.xsd includes IBIS-IP_Enumerations_V2.1.xsd.
```

Initial result:

```text
V2.0 and V2.1 each have their own common/enumeration dependency family in the branch.
No V2.0/V2.1 include-family mismatch is opened in this observation.
```

## 2. XSD enumeration diff

Created diff files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_0_vs_v2_1_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_0_vs_v2_1_xsd_diff.md
```

Observed XSD-side deltas:

| Change | V2.0 | V2.1 | Status | Notes |
|---|---|---|---|---|
| DeviceClass value added | - | `MultiFunctionalDisplay` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ErrorCode value added | - | `OperationNotSupported` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `DoorStateService` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `TrainSetDataService` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `TrainSetInformationService` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `TrainSetManagementService` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `TicketValidationService` | confirmed XSD delta | V2.1 PDF history/table confirms. |
| ServiceName value added | - | `HTMLDisplayService` | confirmed XSD delta | V2.1 PDF history/table confirms. |

No removed V2.0 enumeration value was classified in this first pass.

## 3. V2.1 PDF-side first pass

The opened V2.1 PDF identifies itself as:

```text
VDV-Schrift 301-2-1
07/2018
Common Data Structures and Enumerations
V2.1
```

The V2.1 version history confirms these functional enumeration changes:

```text
DeviceClassEnumeration updated, MultiFunctionalDisplay added.
ErrorCodeEnumeration updated, OperationNotSupported added.
ServiceNameEnumeration updated with DoorStateService, TrainSetDataService,
TrainSetInformationService, TrainSetManagementService, TicketValidationService,
HTMLDisplayService.
```

The V2.1 version history also documents these technical/documentation-oriented additions:

```text
InternationalTextType extended with inline formatting element definitions.
DestinationStructure multiline texts defined.
DisplayContent supply of separate contents to different displays defined.
```

First-pass interpretation:

```text
The functional enumeration changes are directly reflected in V2.1 XSD.
The InternationalTextType / DestinationStructure / DisplayContent notes are primarily semantic/documentation behaviour in this first pass.
No separate XSD structural mismatch is opened from them at this point.
```

## 4. PDF tables checked in this pass

The V2.1 PDF tables confirm:

```text
DeviceClassEnumeration includes MultiFunctionalDisplay.
ErrorCodeEnumeration includes OperationNotSupported.
ServiceNameEnumeration includes DoorStateService, TrainSetDataService,
TrainSetInformationService, TrainSetManagementService, TicketValidationService,
HTMLDisplayService.
InternationalTextType contains an extensive inline-formatting explanation.
```

The following already-known PDF/XSD value/case issues remain visible in V2.1:

```text
TicketValidationEnumeration is printed as Valid while the XSD uses valid.
VehicleModeEnumeration is printed as Air while the XSD uses air.
GNSSTypeEnumeration is printed as Other while the XSD uses other.
```

These support the historical range of CE-007, but the finding register is not updated in this pass. Final affected-version ranges should be consolidated after the full Common/Enums V1.0 -> V2.4 chain is checked.

## 5. Classification

| Topic | First-pass classification | Finding impact |
|---|---|---|
| V2.1 include family | V2.1 common includes V2.1 enumerations. | No CE. |
| `MultiFunctionalDisplay` | V2.1 PDF and V2.1 XSD align. | No CE. |
| `OperationNotSupported` | V2.1 PDF and V2.1 XSD align. | No CE. |
| V2.1 ServiceName additions | V2.1 PDF and V2.1 XSD align for DoorState, TrainSet, TVS and HTMLDisplay service names. | No CE. |
| InternationalTextType inline formatting | PDF defines behaviour; XSD wrapper remains structurally simple. | Documentation/semantic note only. No CE in this pass. |
| Destination multiline texts | PDF defines behaviour; XSD permits repeated destination text structures but does not encode rendering semantics. | Documentation/semantic note only. No CE in this pass. |
| DisplayContent separate display contents | PDF defines behaviour; existing structure supports separate content fields. | Documentation/semantic note only. No CE in this pass. |
| TicketValidation `Valid` vs `valid` | Still visible in V2.1 PDF/XSD pair. | Supports CE-007 historical range; final update deferred. |
| VehicleMode `Air` vs `air` | Still visible in V2.1 PDF/XSD pair. | Supports CE-007 historical range; final update deferred. |
| GNSSType `Other` vs `other` | Still visible in V2.1 PDF/XSD pair. | Supports CE-007 historical range; final update deferred. |

## 6. Finding state decision

Status after this pass:

```text
No new CE finding opened.
No XSD change proposed.
No existing finding state changed in findings.md during this pass.
```

Reason:

```text
The V2.1 PDF confirms the observed V2.0 -> V2.1 enumeration additions.
The semantic/documentation additions in V2.1 do not create a confirmed XSD mismatch in this first pass.
Existing CE-007 receives stronger historical support for V2.1 but final affected-version ranges remain deferred to the Common/Enums historical closure step.
```

## 7. Validation backlog impact

Later technical validation should include version-specific pools:

```text
Common/Enums V2.0 pool:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd

Common/Enums V2.1 pool:
  IBIS-IP_common_V2.1.xsd
  IBIS-IP_Enumerations_V2.1.xsd
```

Suggested targeted samples after schema compile:

```text
V2.0 negative / V2.1 positive: DeviceClassEnumeration MultiFunctionalDisplay.
V2.0 negative / V2.1 positive: ErrorCodeEnumeration OperationNotSupported.
V2.0 negative / V2.1 positive: ServiceNameEnumeration TicketValidationService.
V2.1 explanatory sample: InternationalTextType Value containing escaped inline formatting.
```

## 8. Next work inside the historical block

Next detailed audit file:

```text
docs/pdf_xsd_semantic_audit/04c_common_enums_v2_1_v2_2_history.md
```

Required next steps:

```text
1. Compare Common/Enums V2.1 and V2.2 XSD include families and enumeration deltas.
2. Check VDV 301-2-1 V2.2 PDF version history and affected tables.
3. Track especially ServiceNameEnumeration removal/addition history for CE-004.
4. Track NetexMode / ConnectionMode / VehicleMode/Submode changes and CE-007/CE-008/CE-009/CE-010 history.
```

## 9. Result

```text
Common/Enums V2.0 -> V2.1 historical audit now has XSD-side diff plus PDF-side first pass.
The V2.1 PDF confirms the main V2.1 XSD-side enumeration additions.
No new finding opened yet.
Next: V2.1 -> V2.2 historical audit.
```
