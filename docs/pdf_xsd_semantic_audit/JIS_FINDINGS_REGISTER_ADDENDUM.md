# JourneyInformationService findings register addendum

Status: active addendum after `06b_jis_findings_and_closure.md`.

Purpose:

```text
Record JIS findings in a dedicated addendum so the main findings register can be consolidated later in one clean register-maintenance step.
```

Source:

```text
docs/pdf_xsd_semantic_audit/06b_jis_findings_and_closure.md
```

## JourneyInformationService findings

### JIS-001 - PDF Subscribe/Unsubscribe operations vs service-XSD operation group modelling

State: OK with note / cross-service modelling check pending.

Observation:

```text
The JourneyInformationService V1.0 PDF lists Subscribe/Unsubscribe operation concepts.
The local JourneyInformationServiceGroup contains concrete Get/Retrieve/List/Set operation elements but not service-specific Subscribe/Unsubscribe elements.
```

Impact:

```text
Not treated as a JIS schema defect at this stage.
Subscribe/Unsubscribe may be modelled generically outside the local service group.
```

Next action: cross-service subscription modelling review together with CIS-002.

### JIS-002 - Set* requests vs DataAcceptedResponseStructure response concept

State: OK with note / cross-service response modelling check pending.

Observation:

```text
The local JourneyInformationServiceGroup contains Set*Request elements.
The PDF describes the positive response for Set operations through DataAcceptedResponseStructure rather than local JourneyInformationService.Set*Response elements.
```

Impact:

```text
Not treated as a local JIS schema defect at this stage.
It may be generic response modelling.
```

Next action: cross-service generic response modelling review.

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

Next action: local positive/negative sample validation before PR review.

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

Next action: provider-facing note only.

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

Next action: local positive/negative sample validation.
