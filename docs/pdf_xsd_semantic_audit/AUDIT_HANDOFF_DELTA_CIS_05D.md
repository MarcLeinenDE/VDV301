# Audit handoff delta - CIS 05d

Status: CustomerInformationService V2.0 PDF/XSD first pass completed.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05d_cis_v2_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/cis_v2_0_pdf_xsd_first_pass_matrix.csv
```

Scope:

```text
PDF: VDV-Schrift 301-2-3 CustomerInformationService V2.0, 02/2018
XSD: IBIS-IP_CustomerInformationService_V2.0.xsd
Dependency pool: Common V2.0 + Enumerations V2.0
```

Main result:

```text
Core CIS V2.0 local data structures are aligned in first pass:
  GetAllDataResponse / AllData
  CurrentConnectionInformationData CurrentConnection 0:*
  CurrentDisplayContentData CurrentDisplayContent 1:*
  CurrentStopPointData
  CurrentStopIndexData
  TripData
  VehicleData
  PartialStopSequenceData
```

Candidate notes carried forward:

```text
CIS-002: PDF lists service-specific Subscribe/Unsubscribe operations, while CIS V2.0 XSD operation group contains only Get response and RetrievePartialStopSequence request/response elements. This may be intended generic subscription modelling and needs cross-service/general-conventions check before classifying.

CIS-003: PDF operation overview uses GetCurrentConnectionInformation, but one detailed PDF table heading says GetCurrentConnectionResponse. XSD uses CustomerInformationService.GetCurrentConnectionInformationResponse. Likely documentation note, not XSD defect.

CIS-004: PDF operation overview uses RetrievePartialStopSequence, but one detailed PDF request table says RetrievePartialStopRequest. XSD uses CustomerInformationService.RetrievePartialStopSequenceRequest. Likely documentation note, not XSD defect.
```

No direct schema correction proposed:

```text
No CIS V2.0 XSD change.
No official PR candidate opened.
findings.md not updated in this micro-pass; CIS-002..CIS-004 remain detailed-file candidate notes pending cross-service confirmation.
```

Validation backlog notes:

```text
Compile CIS V2.0 pool later.
Add positive/negative samples for CurrentConnection 0:*, CurrentDisplayContent 1:*, and the two PDF naming discrepancies.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/05e_cis_v2_2_pdf_xsd_first_pass.md
```
