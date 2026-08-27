# CustomerInformationService V2.2 PDF/XSD first pass

Status: PDF/XSD first pass completed for CIS V2.2; local schema compilation still pending.

Scope:

```text
IBIS-IP_CustomerInformationService_V2.2.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
VDV 301-2-3 CustomerInformationService V2.2 PDF source
```

Source class:

```text
CIS V2.2 XSD is historical official release material imported unchanged from the official VDVde/VDV301 tag VDV-301-2.2.
```

Authority rule:

```text
Executable validation follows the V2.2 XSD dependency pool.
PDF differences are recorded as explanatory/provider-facing notes.
No schema correction is made in this pass.
```

Dependency pool:

```text
CIS V2.2 + Common V2.2 + Enumerations V2.2.
```

## 1. PDF source identification

The opened V2.2 PDF identifies itself as:

```text
VDV-Schrift 301-2-3
08/2019
CustomerInformationService - V 2.2
```

The document contents list the same service areas already known from V2.0, plus the V2.2 version-history section.

## 2. Version-history facts from PDF

The V2.2 PDF version history records these V2.2 functional additions:

```text
GlobalDisplayContent added (1.5.2).
TripState added (1.5.2; 1.26.2).
Myownvehicle added in GetAllData and GetVehicleData (1.5.2; 1.26.2).
```

The V2.2 PDF version history records these V2.2 technical corrections:

```text
Process of current stop index described in detail.
TripInformation changed from 1:2 to 0:2 (1.5.2).
Info at VehicleMode to use MyOwnVehicle instead.
```

XSD result:

```text
These V2.2 changes are visible in the imported CIS V2.2 XSD:
- AllData.TripInformation minOccurs="0" maxOccurs="2".
- AllData.GlobalDisplayContent minOccurs="0" maxOccurs="unbounded".
- VehicleInformationGroup.MyOwnVehicleMode minOccurs="0" type="NetexMode".
- VehicleInformationGroup.TripState minOccurs="0" type="TripStateEnumeration".
- VehicleMode remains optional and is annotated as deprecated / use MyOwnVehicleMode instead.
```

Classification:

```text
Aligned in first pass.
No schema correction proposed.
```

## 3. Operation set

V2.2 PDF operation overview includes the same operation family as V2.0:

```text
GetAllData
SubscribeAllData
UnsubscribeAllData
GetCurrentAnnouncement
SubscribeCurrentAnnouncement
UnsubscribeCurrentAnnouncement
GetCurrentConnectionInformation
SubscribeCurrentConnectionInformation
UnsubscribeCurrentConnectionInformation
GetCurrentDisplayContent
SubscribeCurrentDisplayContent
UnsubscribeCurrentDisplayContent
GetCurrentStopPoint
SubscribeCurrentStopPoint
UnsubscribeCurrentStopPoint
GetCurrentStopIndex
SubscribeCurrentStopIndex
UnsubscribeCurrentStopIndex
GetTripData
SubscribeTripData
UnsubscribeTripData
GetVehicleData
SubscribeVehicleData
UnsubscribeVehicleData
RetrievePartialStopSequence
```

The V2.2 XSD operation group contains the concrete service-specific Get response and RetrievePartialStopSequence request/response elements:

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

Classification:

```text
Same modelling note as CIS V2.0.
The PDF lists service operations, including generic subscribe/unsubscribe operations using VDV 301-2-1 structures.
The service XSD operation group lists the concrete service-specific XML elements.
Do not open a hard finding until subscription modelling is checked cross-service.
Carry forward CIS-002 as a candidate note.
```

## 4. Local structure table check

Generated summary file:

```text
docs/pdf_xsd_semantic_audit/generated/cis_v2_2_pdf_xsd_first_pass_matrix.csv
```

First-pass local structure results:

| Area | PDF V2.2 | XSD V2.2 | Classification |
|---|---|---|---|
| `AllData.GlobalDisplayContent` | 0:* | min 0 / max unbounded | aligned |
| `AllData.TripInformation` | 0:2 | min 0 / max 2 | aligned |
| `AllData.MyOwnVehicleMode` | 0:1 `NetexMode` | min 0 / `NetexMode` | aligned |
| `AllData.TripState` | 0:1 `TripStateEnumeration` | min 0 / `TripStateEnumeration` | aligned |
| `CurrentConnectionInformationData.CurrentConnection` | 0:* | min 0 / max unbounded | aligned |
| `CurrentDisplayContentData.CurrentDisplayContent` | 1:* | default min 1 / max unbounded | aligned |
| `TripData.TripInformation` | 1:1 | default 1:1 | aligned |
| `VehicleData.MyOwnVehicleMode` | 0:1 `PtModesEnumeration` in PDF table | min 0 / `NetexMode` in XSD | candidate PDF/XSD type-name mismatch |
| `VehicleData.TripState` | 0:1 `TripStateEnumeration` | min 0 / `TripStateEnumeration` | aligned |
| `PartialStopSequenceData.StopSequence` | 1:1 | default 1:1 | aligned |

## 5. Candidate notes

### CIS-002 carry-forward: Subscribe/Unsubscribe operation modelling

State:

```text
candidate modelling note; no finding opened yet.
```

Observation:

```text
PDF operation overview lists service-specific Subscribe*/Unsubscribe* operations.
The V2.2 service XSD operation group does not list those as service-specific top-level operation elements.
The PDF sections state that subscription and unsubscription use the structures from VDV 301-2-1.
```

Classification:

```text
Likely generic subscription modelling rather than a CIS-only schema defect.
Cross-service check required before promoting this into findings.md.
```

### CIS-003 carry-forward: GetCurrentConnectionInformation vs GetCurrentConnectionResponse

State:

```text
candidate documentation naming note; no schema correction proposed.
```

Observation:

```text
PDF operation overview names GetCurrentConnectionInformation and its response structure as CustomerInformationService.GetCurrentConnectionInformationResponseStructure.
The detail table heading says CustomerInformationService.GetCurrentConnectionResponse.
The XSD uses CustomerInformationService.GetCurrentConnectionInformationResponse.
```

Classification:

```text
The XSD aligns with the operation overview. Treat the shorter detail-table name as a documentation inconsistency candidate.
```

### CIS-004 carry-forward: RetrievePartialStopSequence vs RetrievePartialStopRequest

State:

```text
candidate documentation naming note; no schema correction proposed.
```

Observation:

```text
PDF operation overview names RetrievePartialStopSequence and the used request structure CustomerInformationService.RetrievePartialStopSequenceRequestStructure.
The detail request table says CustomerInformationService.RetrievePartialStopRequest.
The XSD uses CustomerInformationService.RetrievePartialStopSequenceRequest.
```

Classification:

```text
The XSD aligns with the operation overview. Treat the shorter detail-table name as a documentation inconsistency candidate.
```

### CIS-005 new candidate: VehicleData.MyOwnVehicleMode PDF type PtModesEnumeration vs XSD NetexMode

State:

```text
candidate PDF/XSD type-name mismatch; no schema correction proposed in this pass.
```

Observation:

```text
In the V2.2 PDF AllData table, MyOwnVehicleMode is typed as NetexMode.
In the V2.2 PDF VehicleData table, MyOwnVehicleMode is typed as PtModesEnumeration.
In the V2.2 XSD VehicleInformationGroup is reused for AllData and VehicleData, and MyOwnVehicleMode is typed as NetexMode.
```

Impact:

```text
Provider-facing reports should not tell providers to use PtModesEnumeration for VehicleData validation against the V2.2 XSD.
Validation follows NetexMode.
```

Next action:

```text
Check CIS V2.3 PDF and XSD to see whether the VehicleData table type was corrected or carried forward.
Only then decide whether to open a CIS finding in findings.md.
```

## 6. Finding decision

Status after this pass:

```text
No findings.md update in this pass.
No XSD correction proposed.
No official PR candidate opened.
```

Reason:

```text
Most V2.2 PDF/XSD facts align.
The observed differences are either carried-forward modelling/naming notes from V2.0 or one new candidate type-name mismatch that should be checked against CIS V2.3 before finding registration.
```

## 7. Validation backlog impact

Later local technical validation should include:

```text
Compile CIS V2.2 with Common V2.2 + Enumerations V2.2.
Positive: AllData without TripInformation.
Positive: AllData with repeated GlobalDisplayContent.
Positive: VehicleData with MyOwnVehicleMode as NetexMode.
Positive: VehicleData with TripState.
Negative: payload or schema expectation using PtModesEnumeration directly for VehicleData.MyOwnVehicleMode, if a sample model is built from the PDF wording rather than XSD.
```

## 8. Next CIS audit step

Next detailed step:

```text
docs/pdf_xsd_semantic_audit/05f_cis_v2_3_pdf_xsd_first_pass.md
```

Focus:

```text
Check whether CIS V2.3 preserves the same local structures as V2.2.
Check whether CIS V2.3 PDF corrects or repeats the MyOwnVehicleMode/PtModesEnumeration table issue.
Decide whether CIS-002 through CIS-005 should become findings.md entries after V2.3 comparison.
```
