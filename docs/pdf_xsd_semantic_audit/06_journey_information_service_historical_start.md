# JourneyInformationService historical audit start

Status: provenance/scope and first PDF/XSD orientation completed.

Scope:

```text
VDV 301-2-6 JourneyInformationService V1.0 PDF
IBIS-IP_JourneyInformationService_V1.0.xsd
```

Source classes:

```text
Public VDV PDF: VDV-Schrift 301-2-6, 07/2016, Dienst JourneyInformationService.
Official upstream current master: IBIS-IP_JourneyInformationService_V1.0.xsd observed.
Integration branch: IBIS-IP_JourneyInformationService_V1.0.xsd observed.
No version-exact JourneyInformationService V2.x service XSD was observed in the checked VDVde/MarcLeinenDE search pass.
```

Authority rule:

```text
Where the V1.0 service XSD exists, executable validation follows the selected V1.0 XSD family.
PDF observations remain documentation evidence and provider-facing notes.
No schema correction is made in this pass.
```

Mixed-version rule:

```text
JourneyInformationService V1.0 must remain independently routable and validatable.
Do not apply later Common/Enums pools to JIS V1.0 unless the selected JIS schema explicitly requires them.
```

## 1. Public PDF mapping

Observed public PDF:

```text
VDV-Schrift 301-2-6
07/2016
IBIS-IP Beschreibung der Dienste
Dienst JourneyInformationService
```

The PDF foreword states that VDV 301-2-6 was separated from VDV-301-2 to allow future independent changes to individual IBIS-IP services and that this writing describes the JourneyInformationService and its specific data structures.

Version-history note:

```text
The visible version history only records spelling corrections in the first pass.
No later JourneyInformationService V2.x public PDF was observed on the VDV publication index in this pass.
```

## 2. Repository XSD mapping

Observed XSD file:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
```

Observed dependency pool:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Classification:

```text
JourneyInformationService V1.0 is an official PDF-backed XSD baseline.
```

## 3. First XSD orientation

The V1.0 service schema defines a service group named:

```text
JourneyInformationServiceGroup
```

The group includes a broad operation set covering:

```text
GetAllDataResponse
GetCurrentBlockRefResponse
RetrievePartialTripSequenceRequest/Response
RetrieveSpecificBlockInformationRequest/Response
RetrieveSpecificStopInformationRequest/Response
RetrieveSpecificTSPPointInformationRequest/Response
RetrieveSpecificTimingPointInformationRequest/Response
RetrieveSpecificGNSSPointInformationRequest/Response
RetrieveSpecificBeaconPointInformationRequest/Response
ListAllDisplayContentsResponse
ListAllLineInformationResponse
ListAllDestinationInformationResponse
ListAllViaPointResponse
ListAllAdditionalDisplayInformationResponse
ListAllRoutesResponse
RetrieveAllRoutesPerLineRequest/Response
SetBlockNumberRequest
SetTripRefRequest
SetDisplayContentRequest
SetCurrentTripIndexRequest
SetCurrentStopIndexRequest
SetAdditionalAnnouncementRequest
SetAdditionalTextMessageRequest
```

First-pass interpretation:

```text
Unlike the historical CIS V1.0 file, the JIS V1.0 file already contains a local service operation group with top-level JourneyInformationService.* elements.
```

## 4. First PDF/XSD orientation notes

The PDF operation table includes normal Get/List/Retrieve/Set service operations. It also lists Subscribe/Unsubscribe concepts for AllData and CurrentBlockRef.

First-pass classification:

```text
Do not treat missing explicit service-specific Subscribe/Unsubscribe elements in the local operation group as a schema defect yet.
This resembles CIS-002 and likely needs a cross-service subscription-modelling review.
```

The PDF states that Set operation responses use the general response structure from VDV 301-2-1.

First-pass classification:

```text
Do not require service-specific Set*Response elements in the local JIS operation group unless the selected schema defines them.
The checked JIS V1.0 group lists the Set*Request elements.
```

## 5. Finding decision

Status after this start pass:

```text
No JIS-specific finding opened.
No schema correction proposed.
No official PR candidate opened.
```

Potential later notes:

```text
JIS-001 candidate: Subscribe/Unsubscribe modelling parallels CIS-002.
JIS-002 candidate: Set operation generic responses vs absence of service-specific Set*Response elements.
JIS-003 candidate: detailed table/element naming check for RetrieveSpecificGNSSPointInformation and other specific-information response data names.
```

These remain candidates only until the detailed JIS V1.0 PDF/XSD table pass.

## 6. Validation backlog impact

Later local validation should compile:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Suggested samples:

```text
Positive: JourneyInformationService.GetAllDataResponse with AllData/DataContent.
Positive: JourneyInformationService.GetCurrentBlockRefResponse with CurrentBlockRefData.
Positive: JourneyInformationService.RetrievePartialTripSequenceRequest with StartingTripIndex and NumberOfTrips.
Positive: JourneyInformationService.SetAdditionalTextMessageRequest with AdditionalTextMessage.
Negative: repeated fields where V1.0 XSD has no maxOccurs.
Cross-service check: Subscribe/Unsubscribe modelling via generic Common structures.
```

## 7. Next step

Next detailed file:

```text
docs/pdf_xsd_semantic_audit/06a_jis_v1_0_pdf_xsd_first_pass.md
```
