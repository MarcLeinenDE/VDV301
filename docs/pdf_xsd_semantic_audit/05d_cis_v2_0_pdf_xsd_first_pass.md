# CustomerInformationService V2.0 PDF/XSD first pass

Status: PDF/XSD first pass completed for CIS V2.0; local schema compilation still pending.

Scope:

```text
PDF: VDV-Schrift 301-2-3 CustomerInformationService V2.0, 02/2018
XSD: IBIS-IP_CustomerInformationService_V2.0.xsd
Dependencies: IBIS-IP_common_V2.0.xsd + IBIS-IP_Enumerations_V2.0.xsd
```

Source class:

```text
The V2.0 service XSD was imported unchanged into dev/schema-integration from the official VDVde/VDV301 release tag VDV-301-2.0.
It is therefore historical official release material, not candidate material.
```

Authority rule:

```text
Executable validation follows CIS V2.0 XSD plus its V2.0 dependency pool.
PDF observations are documentation evidence and provider-facing notes where they differ from XSD.
No schema correction is made in this pass.
```

Mixed-version rule:

```text
Do not validate CIS V2.0 payloads against CIS V2.2, CIS V2.3 or CIS V2.4 by latest-wins substitution.
```

## 1. XSD dependency and operation-group observation

Observed XSD include family:

```text
IBIS-IP_CustomerInformationService_V2.0.xsd
  includes IBIS-IP_common_V2.0.xsd
  includes IBIS-IP_Enumerations_V2.0.xsd
```

Observed XSD operation group:

```text
CustomerInformationServiceOperations contains:
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
The XSD operation group represents the concrete XML elements defined by this service schema.
The PDF operation overview also lists Subscribe*/Unsubscribe* service operations, but those use common SubscribeRequest/SubscribeResponse and UnsubscribeRequest/UnsubscribeResponse structures.
No service-specific Subscribe*/Unsubscribe* top-level elements were observed in CIS V2.0 XSD.
```

Classification:

```text
CIS-002 candidate note: PDF documents service-specific Subscribe/Unsubscribe operations, while the CIS V2.0 XSD operation group contains only the concrete Get response and RetrievePartialStopSequence request/response elements.
This may be an intended generic-subscription modelling pattern, not a schema defect.
Keep as validation-routing/codegen note until General Conventions and other service schemas are compared.
```

## 2. PDF operation overview vs XSD operation group

Generated comparison file:

```text
docs/pdf_xsd_semantic_audit/generated/cis_v2_0_pdf_xsd_first_pass_matrix.csv
```

PDF operation overview lists these functional service operations:

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

XSD group contains the concrete Get response elements and RetrievePartialStopSequence request/response elements listed above.

First-pass result:

```text
No immediate XSD correction proposed.
The Subscribe/Unsubscribe gap must be carried as a later cross-service modelling check because the PDF explicitly says these subscription structures are the common VDV 301-2-1 Subscribe/Unsubscribe structures.
```

## 3. Data-structure alignment checks

### GetAllDataResponse / AllData

PDF-side observation:

```text
GetAllDataResponse is a choice between AllData and OperationErrorMessage.
AllData contains TimeStamp, VehicleRef, DefaultLanguage, TripInformation 1:2, CurrentStopIndex 1:1 and VehicleInformationGroup.
VehicleInformationGroup contains RouteDeviation 1:1 plus optional DoorState, InPanic, VehicleStopRequested, ExitSide, MovingDirectionForward, VehicleMode, SpeakerActive and StopInformationActive.
```

XSD-side observation:

```text
The checked CIS V2.0 XSD models the same AllData core fields and VehicleInformationGroup fields.
TripInformation has maxOccurs="2" and no minOccurs, therefore 1:2.
SpeakerActive and StopInformationActive are present with minOccurs="0".
```

Classification:

```text
Aligned in first pass.
```

### CurrentConnectionInformationData

PDF-side observation:

```text
CurrentConnection is documented as 0:*.
The V2.0 version history explicitly says CurrentConnection was updated to minOccurs="0" maxOccurs="unbounded".
```

XSD-side observation:

```text
CurrentConnection uses minOccurs="0" maxOccurs="unbounded".
```

Classification:

```text
Aligned in first pass.
```

### CurrentDisplayContentData

PDF-side observation:

```text
CurrentDisplayContent is documented as 1:*.
The V2.0 version history explicitly says CurrentDisplayContent was updated to maxOccurs="unbounded".
```

XSD-side observation:

```text
CurrentDisplayContent uses maxOccurs="unbounded" and no minOccurs, therefore 1:*.
```

Classification:

```text
Aligned in first pass.
```

### CurrentStopPointData / CurrentStopIndexData / TripData / VehicleData / PartialStopSequenceData

PDF-side observation:

```text
CurrentStopPointData contains TimeStamp 1:1 and CurrentStopPoint 1:1.
CurrentStopIndexData contains TimeStamp 1:1 and CurrentStopIndex 1:1.
TripData contains TimeStamp 1:1, VehicleRef 1:1, DefaultLanguage 1:1, TripInformation 1:1 and CurrentStopIndex 1:1.
VehicleData contains TimeStamp 1:1, VehicleRef 1:1 and VehicleInformationGroup.
PartialStopSequenceData contains TimeStamp 1:1 and StopSequence 1:1.
```

XSD-side observation:

```text
No first-pass mismatch observed for these local CIS V2.0 structures.
```

Classification:

```text
Aligned in first pass.
```

## 4. PDF naming/text discrepancies observed

### CIS-003 candidate - GetCurrentConnectionInformation naming inconsistency

Observation:

```text
The PDF operation overview uses GetCurrentConnectionInformation.
The XSD uses CustomerInformationService.GetCurrentConnectionInformationResponse and CustomerInformationService.GetCurrentConnectionInformationResponseStructure.
However, the detailed PDF response table heading uses GetCurrentConnectionResponse / CurrentConnectionData wording.
```

Classification:

```text
Likely PDF/textual naming inconsistency, not XSD defect.
Validation follows the XSD names.
```

Provider-facing note:

```text
If a provider refers to GetCurrentConnectionResponse from the PDF table, the XSD-valid top-level element is CustomerInformationService.GetCurrentConnectionInformationResponse.
```

### CIS-004 candidate - RetrievePartialStopSequence request table name

Observation:

```text
The PDF operation overview uses RetrievePartialStopSequence.
The XSD uses CustomerInformationService.RetrievePartialStopSequenceRequest and CustomerInformationService.RetrievePartialStopSequenceResponse.
However, the detailed PDF request table heading uses RetrievePartialStopRequest.
```

Classification:

```text
Likely PDF/textual naming inconsistency, not XSD defect.
Validation follows the XSD names.
```

Provider-facing note:

```text
If a provider refers to RetrievePartialStopRequest from the PDF table, the XSD-valid request element is CustomerInformationService.RetrievePartialStopSequenceRequest.
```

## 5. Finding decision

Status after this pass:

```text
No direct CIS V2.0 schema correction proposed.
No official PR candidate opened.
```

Candidate notes to carry forward:

```text
CIS-002: Subscribe/Unsubscribe operation representation should be checked across General Conventions and other services before classifying as OK or mismatch.
CIS-003: GetCurrentConnectionInformation vs GetCurrentConnectionResponse PDF naming inconsistency; likely documentation note.
CIS-004: RetrievePartialStopSequenceRequest vs RetrievePartialStopRequest PDF naming inconsistency; likely documentation note.
```

CIS-001 from the previous block remains:

```text
CIS V1.1 public PDF has no confirmed version-exact XSD mapping.
```

## 6. Validation backlog impact

Later local validation should include:

```text
Compile CIS V2.0 + Common V2.0 + Enumerations V2.0.
Positive: CurrentConnectionInformationData with zero CurrentConnection entries.
Positive: CurrentConnectionInformationData with multiple CurrentConnection entries.
Positive: CurrentDisplayContentData with multiple CurrentDisplayContent entries.
Negative: CurrentDisplayContentData with zero CurrentDisplayContent entries.
Negative: GetAllDataResponse using GetCurrentConnectionResponse as top-level element name.
Negative: RetrievePartialStopRequest as top-level request element name.
Positive: CustomerInformationService.GetCurrentConnectionInformationResponse.
Positive: CustomerInformationService.RetrievePartialStopSequenceRequest.
```

## 7. Next CIS audit step

Next detailed step:

```text
docs/pdf_xsd_semantic_audit/05e_cis_v2_2_pdf_xsd_first_pass.md
```

Focus:

```text
Check CIS V2.2 PDF against the now available official historical CIS V2.2 XSD.
Track the V2.2 additions already observed XSD-side:
  AllData.TripInformation 0:2
  AllData.GlobalDisplayContent 0:*
  VehicleInformationGroup.MyOwnVehicleMode NetexMode
  VehicleInformationGroup.TripState
  VehicleMode deprecation note
```