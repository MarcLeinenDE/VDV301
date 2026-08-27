# JourneyInformationService findings and closure

Status: first-pass closure completed for JourneyInformationService V1.0; local schema compilation still pending.

Scope:

```text
docs/pdf_xsd_semantic_audit/06_journey_information_service_historical_start.md
docs/pdf_xsd_semantic_audit/06a_jis_v1_0_pdf_xsd_first_pass.md
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Authority rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
No schema correction is made in this closure pass.
```

## 1. First-pass closure result

JourneyInformationService has one checked public service version in this pass:

```text
JourneyInformationService V1.0
```

Selected validation pool:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

The XSD contains a local service group:

```text
JourneyInformationServiceGroup
```

The group contains the checked Get, Retrieve, List and Set request/response operation elements. The local schema model is therefore usable as an executable V1.0 validation source once local compilation has been run.

## 2. Closure classification

| ID | State | Classification | XSD change now? |
|---|---|---|---|
| JIS-001 | note | Subscribe/Unsubscribe concepts in PDF vs generic/local XSD modelling | no |
| JIS-002 | note | Set* request elements in local XSD vs generic DataAcceptedResponseStructure response concept in PDF | no |
| JIS-003 | candidate finding | `ListAllLineInformation` PDF `LineInformation 1:*` vs XSD `LineInformation` default `1:1` | no |
| JIS-004 | note | `RetrieveAllRoutesPerLine` detail-label/table wording appears inconsistent | no |
| JIS-005 | note/candidate | `SpecificGNSSPointInformationData` structure naming vs XSD choice element `SpecificGNSSPointInformation` | no |

## 3. Findings / notes

### JIS-001 - PDF Subscribe/Unsubscribe operations vs service-XSD operation group modelling

State: OK with note / cross-service modelling check pending.

Observation:

```text
The JourneyInformationService V1.0 PDF lists Subscribe/Unsubscribe operation concepts.
The local JourneyInformationServiceGroup contains concrete Get/Retrieve/List/Set operation elements but not service-specific Subscribe/Unsubscribe elements.
```

Impact:

```text
This is not treated as a JourneyInformationService schema defect at this stage.
Subscribe/Unsubscribe may be modelled generically outside the local service group, as already suspected for CIS.
```

Next action:

```text
Keep JIS-001 together with CIS-002 for a cross-service subscription modelling review.
```

### JIS-002 - Set* requests vs DataAcceptedResponseStructure response concept

State: OK with note / cross-service response modelling check pending.

Observation:

```text
The local JourneyInformationServiceGroup contains Set*Request elements.
The PDF describes the positive response for Set operations through DataAcceptedResponseStructure rather than local JourneyInformationService.Set*Response elements.
```

Impact:

```text
This is not treated as a local JIS schema defect at this stage.
It may be generic response modelling.
```

Next action:

```text
Check generic operation response modelling across other services before considering any stronger classification.
```

### JIS-003 - ListAllLineInformation LineInformation cardinality PDF 1:* vs XSD 1:1

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
The checked JIS V1.0 PDF table indicates ListAllLineInformation/LineInformation as repeatable 1:*.
IBIS-IP_JourneyInformationService_V1.0.xsd defines AllLineInformationData/LineInformation without maxOccurs.
XML Schema default is maxOccurs="1", therefore XSD cardinality is 1:1.
```

Impact:

```text
A provider sending multiple LineInformation entries under AllLineInformationData may be following the PDF table but fail strict XSD validation.
Validation follows XSD until an official schema correction exists.
```

Next action:

```text
Add local positive/negative samples:
- one LineInformation entry should validate if the surrounding structure is valid.
- two LineInformation entries should fail against the current JIS V1.0 XSD.
Review after local compilation before any official-facing correction proposal.
```

### JIS-004 - RetrieveAllRoutesPerLine / SetBlockNumberRequest table-label inconsistency candidate

State: PDF label inconsistency note.

Observation:

```text
The XSD defines JourneyInformationService.RetrieveAllRoutesPerLineRequest and JourneyInformationService.RetrieveAllRoutesPerLineResponse.
The checked PDF detail/table area appears to contain inconsistent wording around RetrieveAllRoutesPerLine and SetBlockNumberRequest.
```

Impact:

```text
Do not rename the XSD based on ambiguous detail-table wording.
The XSD-valid operation elements remain RetrieveAllRoutesPerLineRequest and RetrieveAllRoutesPerLineResponse.
```

Next action:

```text
Keep as provider-facing note; no schema correction proposed.
```

### JIS-005 - SpecificGNSSPointInformationData vs SpecificGNSSPointInformation naming

State: naming/structure note; possible PDF/XSD naming inconsistency candidate.

Observation:

```text
The XSD complex type is JourneyInformationService.SpecificGNSSPointInformationData.
The XSD response choice element is SpecificGNSSPointInformation, not SpecificGNSSPointInformationData.
The PDF table wording refers to the data structure naming.
```

Impact:

```text
The XSD-valid payload element inside RetrieveSpecificGNSSPointInformationResponse is SpecificGNSSPointInformation.
A payload using SpecificGNSSPointInformationData as the element name would not match the current XSD choice.
```

Next action:

```text
Keep as provider-facing naming note and add a local positive/negative sample after schema compilation.
```

## 4. Local validation backlog impact

Add to local technical validation backlog:

```text
JIS V1.0 pool compile:
  IBIS-IP_JourneyInformationService_V1.0.xsd
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_Enumerations_V1.0.xsd

Targeted samples:
  JIS-003 positive: AllLineInformationData with one LineInformation.
  JIS-003 negative: AllLineInformationData with two LineInformation entries.
  JIS-005 positive: RetrieveSpecificGNSSPointInformationResponse with SpecificGNSSPointInformation.
  JIS-005 negative: RetrieveSpecificGNSSPointInformationResponse with SpecificGNSSPointInformationData as payload element.
```

## 5. Closure decision

```text
JourneyInformationService V1.0 first pass is closed.
No XSD file was changed.
No official PR candidate is opened now.
JIS-003 is the only strong JIS-specific PDF/XSD discrepancy candidate from this pass.
JIS-001, JIS-002, JIS-004 and JIS-005 remain notes/candidates for later cross-service or local-validation review.
```

Next recommended service-level block:

```text
07_location_services_historical_start.md
```
