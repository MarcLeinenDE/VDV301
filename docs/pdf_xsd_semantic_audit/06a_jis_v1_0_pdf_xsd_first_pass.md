# JourneyInformationService V1.0 PDF/XSD first pass

Status: PDF/XSD first pass completed for JIS V1.0; local schema compilation still pending.

Scope:

```text
VDV 301-2-6 JourneyInformationService V1.0 PDF
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Source classification:

```text
JIS V1.0 PDF: public VDV writing, VDV-Schrift 301-2-6, 07/2016.
JIS V1.0 XSD: present in official VDVde/VDV301 master and in dev/schema-integration.
Dependency pool: Common V1.0 + Enumerations V1.0.
```

Authority rule:

```text
Executable validation follows the selected XSD family.
PDF/XSD differences are recorded as audit/provider-facing notes.
No XSD correction is made in this pass.
```

## 1. Operation overview

The PDF operation table contains these operation concepts:

```text
GetAllData
SubscribeAllData
UnsubscribeAllData
GetCurrentBlockRef
SubscribeCurrentBlockRef
UnsubscribeCurrentBlockRef
RetrievePartialTripSequence
RetrieveSpecificBlockInformation
RetrieveSpecificStopInformation
RetrieveSpecificTSPPointInformation
RetrieveSpecificTimingPointInformation
RetrieveSpecificGNSSPointInformation
RetrieveSpecificBeaconPointInformation
ListAllDisplayContents
ListAllLineInformation
ListAllDestinationInformation
ListAllViaPoint
ListAllAdditionalDisplayInformation
ListAllRoutes
RetrieveAllRoutesPerLine
SetBlockNumber
SetTripRef
SetDisplayContent
SetCurrentTripIndex
SetCurrentStopIndex
SetAdditionalAnnouncement
SetAdditionalTextMessage
```

The local XSD group `JourneyInformationServiceGroup` contains the concrete service-specific XSD elements for:

```text
Get* response elements,
Retrieve* request/response elements,
List* response elements,
RetrieveAllRoutesPerLine request/response elements,
Set* request elements.
```

First-pass interpretation:

```text
The XSD group is broadly aligned with the service-specific operation elements needed for strict XML validation.
Subscribe/Unsubscribe operations are listed in the PDF but not represented as local service-specific elements in JourneyInformationServiceGroup.
This mirrors the CIS observation and remains a cross-service subscription modelling note, not a JIS schema defect at this stage.
```

## 2. GetAllData / DataContent

Observed PDF table intent:

```text
JourneyInformationService.GetAllDataResponse choice:
  AllData 1:1 JourneyInformationService.DataContent
  OperationErrorMessage IBIS-IP.string

JourneyInformationService.DataContent:
  TimeStamp 1:1 IBIS-IP.dateTime
  BlockRef 0:1 IBIS-IP.NMTOKEN
  CurrentTripIndex 0:1 IBIS-IP.int
  TripSequence 1:* TripSequence
```

Observed XSD model:

```text
JourneyInformationService.GetAllDataResponse
  choice AllData / OperationErrorMessage

JourneyInformationService.DataContent
  TimeStamp required
  BlockRef minOccurs=0
  CurrentTripIndex minOccurs=0
  TripSequence maxOccurs=unbounded, default minOccurs=1
```

First-pass result:

```text
PDF and XSD align for the checked fields and cardinalities.
```

## 3. GetCurrentBlockRef

Observed PDF table intent:

```text
GetCurrentBlockRef has no request structure.
Response choice:
  CurrentBlockRefData 1:1
  OperationErrorMessage
CurrentBlockRefData:
  TimeStamp 1:1
  CurrentBlockRef 1:1
```

Observed XSD model:

```text
JourneyInformationService.GetCurrentBlockRefResponse
JourneyInformationService.CurrentBlockRefData
  TimeStamp required
  CurrentBlockRef required
```

First-pass result:

```text
PDF and XSD align for the checked response structure.
```

## 4. RetrievePartialTripSequence

Observed PDF table intent:

```text
Request:
  StartingTripIndex 1:1 IBIS-IP.int
  NumberOfTrips 1:1 IBIS-IP.int

Response choice:
  PartialTripSequenceData 1:1
  OperationErrorMessage

PartialTripSequenceData:
  TimeStamp 1:1
  TripSequence 1:*
```

Observed XSD model:

```text
JourneyInformationService.RetrievePartialTripSequenceRequest
  StartingTripIndex required
  NumberOfTrips required

JourneyInformationService.RetrievePartialTripSequenceResponse
  choice PartialTripSequenceData / OperationErrorMessage

JourneyInformationService.PartialTripSequenceData
  TimeStamp required
  TripSequence maxOccurs=unbounded, default minOccurs=1
```

First-pass result:

```text
PDF and XSD align for the checked request and response structures.
```

## 5. RetrieveSpecific* structures

Checked local structures:

```text
RetrieveSpecificBlockInformation
RetrieveSpecificStopInformation
RetrieveSpecificTSPPointInformation
RetrieveSpecificTimingPointInformation
RetrieveSpecificGNSSPointInformation
RetrieveSpecificBeaconPointInformation
```

Observed general pattern:

```text
Each request has the expected required reference field.
Each response is a choice between a specific data element and OperationErrorMessage.
The specific data structures contain TimeStamp plus the referenced common data structure.
```

First-pass result:

```text
The checked RetrieveSpecific* structures are broadly aligned.
```

Candidate note:

```text
The XSD response choice for RetrieveSpecificGNSSPointInformation uses element name SpecificGNSSPointInformation, while the type is JourneyInformationService.SpecificGNSSPointInformationData.
The PDF table wording around the response data uses SpecificGNSSPointInformationData.
This is a possible element-name/table-label difference but needs a final table/element-level closure pass before opening a finding.
```

## 6. ListAll* structures

Checked list responses:

```text
ListAllDisplayContents
ListAllLineInformation
ListAllDestinationInformation
ListAllViaPoint
ListAllAdditionalDisplayInformation
ListAllRoutes
RetrieveAllRoutesPerLine
```

First-pass result by structure:

| Structure | PDF cardinality / table intent | XSD observation | Result |
|---|---|---|---|
| `AllDisplayContentsData.DisplayContent` | 1:* | `maxOccurs="unbounded"`, default min 1 | aligned |
| `AllLineInformationData.LineInformation` | 1:* | no `maxOccurs`, default max 1 | candidate discrepancy |
| `AllDestinationInformationData.Destination` | 1:* | `maxOccurs="unbounded"`, default min 1 | aligned |
| `AllViaPointData.ViaPoint` | 1:* | `maxOccurs="unbounded"`, default min 1 | aligned |
| `AllAdditionalDisplayInformationData.AdditionalDisplayInformation` | 1:* | `maxOccurs="unbounded"`, default min 1 | aligned |
| `AllRoutesData.Route` | 1:* | `maxOccurs="unbounded"`, default min 1 | aligned |
| `RetrieveAllRoutesPerLineResponse` | same as ListAllRoutesResponse | XSD reuses `JourneyInformationService.ListAllRoutesResponseStructure` | aligned |

Candidate finding:

```text
JIS-003 candidate:
ListAllLineInformation PDF table indicates LineInformation 1:*.
The JIS V1.0 XSD defines LineInformation without maxOccurs, therefore 1:1 by XML Schema default.
A response containing multiple LineInformation entries would follow the PDF table but fail strict XSD validation.
Validation follows XSD.
```

## 7. RetrieveAllRoutesPerLine request table label

Observed:

```text
The PDF section heading is RetrieveAllRoutesPerLine.
The operation overview lists RetrieveAllRoutesPerLineRequestStructure.
In the detailed request table, the printed request/table label appears as SetBlockNumberRequest.
The XSD defines JourneyInformationService.RetrieveAllRoutesPerLineRequest with LineRef.
```

Candidate finding:

```text
JIS-004 candidate:
RetrieveAllRoutesPerLine detailed PDF request table appears to carry the wrong SetBlockNumberRequest label.
This is treated as PDF/table wording inconsistency candidate, not as an XSD defect.
```

## 8. Set* request structures

Checked set operations:

```text
SetBlockNumber
SetTripRef
SetDisplayContent
SetCurrentTripIndex
SetCurrentStopIndex
SetAdditionalAnnouncement
SetAdditionalTextMessage
```

Observed:

```text
The PDF operation overview lists each Set* request as a JourneyInformationService.*RequestStructure and the response as DataAcceptedResponseStructure.
The local JIS XSD group contains the Set*Request elements and their request structures.
It does not define local JourneyInformationService.*Response elements for these Set operations.
```

First-pass interpretation:

```text
No direct XSD defect is opened.
The response appears to use a generic Common/VDV-301-2-1 DataAcceptedResponseStructure rather than a local service-specific response element.
This is carried as JIS-002 / cross-service generic-response modelling note.
```

## 9. Candidate notes carried forward

```text
JIS-001: Subscribe/Unsubscribe operations are listed in the PDF but not local service-specific group elements in the JIS XSD.
JIS-002: Set* operations list generic DataAcceptedResponseStructure responses; the local JIS XSD contains Set*Request elements only.
JIS-003: ListAllLineInformation PDF 1:* vs XSD default 1:1 for LineInformation.
JIS-004: RetrieveAllRoutesPerLine detailed request table appears to be labelled SetBlockNumberRequest in the PDF.
JIS-005 candidate: RetrieveSpecificGNSSPointInformation response data element label may differ between PDF wording and XSD element name.
```

## 10. Finding decision

Status after this pass:

```text
Do not edit XSD in this pass.
Do not open an official PR candidate in this pass.
Open/append JIS findings in findings.md only after one closure pass confirms the candidate classification.
```

Reason:

```text
JIS-003 is the strongest observed PDF/XSD candidate and should be preserved for validation backlog and post-audit review.
The remaining JIS notes may be PDF/table wording or generic modelling issues and should be classified carefully.
```

## 11. Validation backlog impact

Add later local validation samples for:

```text
JIS V1.0 + Common V1.0 + Enumerations V1.0 schema compile.
Positive: ListAllLineInformationResponse with one LineInformation.
Negative according to XSD / PDF-positive candidate: ListAllLineInformationResponse with multiple LineInformation entries.
Positive: ListAllDisplayContentsResponse with multiple DisplayContent entries.
Positive: ListAllRoutesResponse with multiple Route entries.
Positive: RetrieveAllRoutesPerLineResponse using ListAllRoutesResponseStructure.
Positive: SetDisplayContentRequest without a local service-specific SetDisplayContentResponse element.
```

## 12. Next JIS audit step

Next detailed step:

```text
docs/pdf_xsd_semantic_audit/06b_jis_findings_and_closure.md
```
