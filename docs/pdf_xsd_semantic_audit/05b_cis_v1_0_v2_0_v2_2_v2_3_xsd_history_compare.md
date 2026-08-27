# CustomerInformationService V1.0 / V2.0 / V2.2 / V2.3 XSD history compare

Status: XSD-side historical first pass completed; PDF-side detailed comparison still pending.

Scope:

```text
IBIS-IP_CustomerInformationService_V1.0.xsd
IBIS-IP_CustomerInformationService_V2.0.xsd
IBIS-IP_CustomerInformationService_V2.2.xsd
IBIS-IP_CustomerInformationService_V2.3.xsd
```

Source classes:

```text
CIS V1.0: imported unchanged from official VDVde/VDV301 tag VDV-301-1.0.
CIS V2.0: imported unchanged from official VDVde/VDV301 tag VDV-301-2.0.
CIS V2.2: imported unchanged from official VDVde/VDV301 tag VDV-301-2.2.
CIS V2.3: present in current official upstream master and in dev/schema-integration.
```

Authority rule:

```text
Where a version-exact XSD exists, executable validation follows that selected version's XSD family.
This file records XSD-side history only. PDF-side table comparison remains a later step.
No schema correction is made in this pass.
```

Mixed-version rule:

```text
Do not validate older CIS payloads against CIS V2.3 by latest-wins substitution.
Each CIS version must be mapped to its own service schema and dependency pool.
```

## 1. Dependency pools

Observed include families:

| CIS version | Service schema | Common dependency | Enumeration dependency | Classification |
|---|---|---|---|---|
| V1.0 | `IBIS-IP_CustomerInformationService_V1.0.xsd` | `IBIS-IP_common_V1.0.xsd` | `IBIS-IP_Enumerations_V1.0.xsd` | official historical release material |
| V2.0 | `IBIS-IP_CustomerInformationService_V2.0.xsd` | `IBIS-IP_common_V2.0.xsd` | `IBIS-IP_Enumerations_V2.0.xsd` | official historical release material |
| V2.2 | `IBIS-IP_CustomerInformationService_V2.2.xsd` | `IBIS-IP_common_V2.2.xsd` | `IBIS-IP_Enumerations_V2.2.xsd` | official historical release material |
| V2.3 | `IBIS-IP_CustomerInformationService_V2.3.xsd` | `IBIS-IP_common_V2.3.xsd` | `IBIS-IP_Enumerations_V2.2.xsd` | current upstream/current integration material |

Interpretation:

```text
CIS V2.3 follows the same V2.3 dependency-family pattern already established for Common/Enums: Common V2.3 + Enumerations V2.2.
```

## 2. Operation model history

### V1.0

Observed:

```text
CIS V1.0 defines response/request complex types but does not define the CustomerInformationServiceOperations group and does not define top-level CustomerInformationService.* operation elements in the same style as V2.x.
```

The V1.0 schema still defines these operation structures:

```text
CustomerInformationService.GetAllDataResponseStructure
CustomerInformationService.GetCurrentAnnouncementResponseStructure
CustomerInformationService.GetCurrentConnectionInformationResponseStructure
CustomerInformationService.GetCurrentDisplayContentResponseStructure
CustomerInformationService.GetCurrentStopPointResponseStructure
CustomerInformationService.GetCurrentStopIndexResponseStructure
CustomerInformationService.GetTripDataResponseStructure
CustomerInformationService.GetVehicleDataResponseStructure
CustomerInformationService.RetrievePartialStopSequenceRequestStructure
CustomerInformationService.RetrievePartialStopSequenceResponseStructure
```

First-pass interpretation:

```text
The V1.0 service-XSD style is structurally older than V2.x.
A later validator/code generator must not expect the V2.x operation group to exist in V1.0.
```

### V2.0 / V2.2 / V2.3

Observed:

```text
CIS V2.0, V2.2 and V2.3 define CustomerInformationServiceOperations.
The operation group contains the same ten operation elements in all checked V2.x files.
The same ten top-level CustomerInformationService.* elements are also defined in the service section.
```

Operation set:

```text
CustomerInformationService.GetAllDataResponse
CustomerInformationService.GetCurrentAnnouncementResponse
CustomerInformationService.GetCurrentConnectionInformationResponse
CustomerInformationService.GetCurrentDisplayContentResponse
CustomerInformationService.GetCurrentStopPointResponse
CustomerInformationService.GetCurrentStopIndexResponse
CustomerInformationService.GetTripDataResponse
CustomerInformationService.GetVehicleDataResponse
CustomerInformationService.RetrievePartialStopSequenceRequest
CustomerInformationService.RetrievePartialStopSequenceResponse
```

First-pass interpretation:

```text
No CIS operation-set delta is observed between V2.0, V2.2 and V2.3.
The visible V2.x operation model is stable across the checked schemas.
```

## 3. Data-structure/cardinality deltas

Generated summary file:

```text
docs/pdf_xsd_semantic_audit/generated/cis_v1_0_v2_0_v2_2_v2_3_xsd_history_delta.csv
```

Observed XSD-side deltas:

| Area | V1.0 | V2.0 | V2.2 | V2.3 | First-pass interpretation |
|---|---|---|---|---|---|
| Operation group/top-level elements | absent | present | present | present | V2.0 introduces/uses the newer operation element/group style. |
| `AllData/TripInformation` | default min 1, max 2 | default min 1, max 2 | min 0, max 2 | min 0, max 2 | V2.2 makes trip information optional in `AllData`. |
| `AllData/GlobalDisplayContent` | absent | absent | 0:* | 0:* | V2.2 adds global display content to `AllData`. |
| `CurrentConnectionInformationData/CurrentConnection` | default 1:1 | 0:* | 0:* | 0:* | V2.0 makes current connections repeatable/optional. |
| `CurrentDisplayContentData/CurrentDisplayContent` | default 1:1 | 1:* | 1:* | 1:* | V2.0 makes current display content repeatable. |
| `VehicleInformationGroup/SpeakerActive` | absent | optional | optional | optional | V2.0 adds speaker state. |
| `VehicleInformationGroup/StopInformationActive` | absent | optional | optional | optional | V2.0 adds stop information active state. |
| `VehicleInformationGroup/MyOwnVehicleMode` | absent | absent | optional `NetexMode` | optional `NetexMode` | V2.2 adds Netex mode/submode support. |
| `VehicleInformationGroup/TripState` | absent | absent | optional `TripStateEnumeration` | optional `TripStateEnumeration` | V2.2 adds trip-state support. |
| `VehicleInformationGroup/VehicleMode` | optional `VehicleModeEnumeration` | optional `VehicleModeEnumeration` | optional deprecated `VehicleModeEnumeration` | optional deprecated `VehicleModeEnumeration` | V2.2 deprecates old vehicle mode in favour of `MyOwnVehicleMode`. |

## 4. Version-pair interpretation

### V1.0 -> V2.0

Key XSD-side changes:

```text
- newer CustomerInformationServiceOperations group appears.
- top-level CustomerInformationService.* operation elements appear.
- CurrentConnection becomes 0:*.
- CurrentDisplayContent becomes 1:*.
- SpeakerActive and StopInformationActive are added to VehicleInformationGroup.
```

No finding opened:

```text
These are version-history deltas, not PDF/XSD contradictions by themselves.
```

### V2.0 -> V2.2

Key XSD-side changes:

```text
- dependency pool moves from Common/Enums V2.0 to Common/Enums V2.2.
- AllData.TripInformation becomes optional with max 2.
- AllData.GlobalDisplayContent is added as 0:*.
- VehicleMode becomes explicitly deprecated in the annotation.
- MyOwnVehicleMode is added as NetexMode.
- TripState is added.
```

No finding opened:

```text
These changes match the broader Common/Enums V2.2 model transition toward NetexMode/TripState.
PDF-side confirmation remains a later CIS PDF table check.
```

### V2.2 -> V2.3

Key XSD-side changes:

```text
- service operation set appears unchanged.
- local CIS service structures appear unchanged in the first pass.
- dependency pool moves from Common V2.2 + Enumerations V2.2 to Common V2.3 + Enumerations V2.2.
```

Interpretation:

```text
CIS V2.3 is mainly a dependency-family/common-structure version shift in the checked XSD.
The impact is inherited from Common V2.3 structures rather than from local CIS operation changes.
```

## 5. CIS V1.1 mapping remains open

Current known state:

```text
Public VDV page lists CIS V1.1.
Official VDVde/VDV301 tag VDV-301-1.0 contains CIS V1.0 service XSD.
No version-exact CIS V1.1 service XSD has been confirmed in the checked source set.
```

Conservative classification:

```text
Do not silently map CIS V1.1 PDF to CIS V1.0 XSD yet.
Treat CIS V1.1 as public-PDF-known / exact-XSD-mapping-open until the V1.1 publication or release context is checked.
```

## 6. Finding decision

Status after this pass:

```text
No CIS-specific finding opened.
No schema correction proposed.
No official PR candidate opened.
```

Reason:

```text
The observed differences are legitimate version-to-version XSD deltas or source-provenance facts.
A PDF/XSD contradiction can only be opened after checking the matching CIS PDF tables for the affected version.
```

## 7. Validation backlog impact

Later local technical validation should compile these pools separately:

```text
CIS V1.0 + Common V1.0 + Enumerations V1.0
CIS V2.0 + Common V2.0 + Enumerations V2.0
CIS V2.2 + Common V2.2 + Enumerations V2.2
CIS V2.3 + Common V2.3 + Enumerations V2.2
```

Suggested targeted version-delta samples:

```text
V1.0 operation group absent: do not require CustomerInformationServiceOperations when compiling V1.0.
V1.0 negative / V2.0 positive: repeated CurrentDisplayContent in CurrentDisplayContentData.
V1.0 negative / V2.0 positive: zero CurrentConnection in CurrentConnectionInformationData.
V2.0 negative / V2.2 positive: AllData without TripInformation.
V2.0 negative / V2.2 positive: AllData.GlobalDisplayContent.
V2.0 negative / V2.2 positive: VehicleInformationGroup.MyOwnVehicleMode.
V2.0 negative / V2.2 positive: VehicleInformationGroup.TripState.
V2.2 and V2.3: same local CIS operation set; dependency-pool difference must be preserved.
```

## 8. Next CIS audit step

Next detailed step:

```text
Resolve CIS V1.1 PDF-to-XSD mapping and then run CIS PDF-side table checks for V2.0, V2.2 and V2.3.
```

Recommended file sequence:

```text
05c_cis_v1_1_mapping.md
05d_cis_v2_0_v2_2_v2_3_pdf_xsd_first_pass.md
```
