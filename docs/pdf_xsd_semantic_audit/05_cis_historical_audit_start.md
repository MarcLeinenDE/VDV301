# CustomerInformationService historical audit start

Status: started; provenance/scope and first XSD/PDF mapping completed.

Scope:

```text
VDV 301-2-3 CustomerInformationService V1.1 PDF
VDV 301-2-3 CustomerInformationService V2.0 PDF
VDV 301-2-3 CustomerInformationService V2.2 PDF
VDV 301-2-3 CustomerInformationService V2.3 PDF
IBIS-IP_CustomerInformationService_V2.3.xsd
IBIS-IP_CustomerInformationService_V2.4.xsd candidate/integration file in dev/schema-integration
```

Authority rule:

```text
Validation follows the selected service version's XSD family where an XSD is present.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not validate an older CustomerInformationService payload against a newer CIS XSD merely because the newer XSD is available.
Every CIS version must be routed explicitly to its own observed/confirmed XSD dependency pool.
If a public PDF exists but no matching XSD is observed in the selected repository state, record that as a provenance gap / routing task, not as an automatic service defect.
```

## 1. Public PDF version mapping

The official VDV publication index currently exposes these CustomerInformationService publications:

```text
VDV 301-2-3 CustomerInformationService V1.1
VDV 301-2-3 CustomerInformationService V2.0
VDV 301-2-3 CustomerInformationService V2.2
VDV 301-2-3 CustomerInformationService V2.3
```

First-pass source notes:

```text
V1.1 PDF: identified as VDV-Schrift 301-2-3, 12/2016, Dienst CustomerInformationService.
V2.0 PDF: identified as VDV-Schrift 301-2-3, 02/2018, Dienst CustomerInformationService V2.0.
V2.2 PDF: public VDV 301-2-3 CustomerInformationService V2.2 PDF source opened for the next detailed pass.
V2.3 PDF: identified as VDV-Schrift 301-2-3, 12/2020, CustomerInformationService V2.3.
```

No public CIS V2.4 PDF was observed on the VDV publication index in this first pass.

## 2. Repository XSD version mapping

Observed in official upstream master:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
```

Observed in dev/schema-integration:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
IBIS-IP_CustomerInformationService_V2.4.xsd
```

Not observed in dev/schema-integration during this pass:

```text
IBIS-IP_CustomerInformationService_V1.1.xsd
IBIS-IP_CustomerInformationService_V2.0.xsd
IBIS-IP_CustomerInformationService_V2.2.xsd
```

Classification:

```text
CIS V1.1/V2.0/V2.2: public PDFs exist, but no matching CIS service XSD is currently observed in the selected branch. These versions need repository-history/fork-history search before claiming they are not validatable.
CIS V2.3: official upstream and integration branch contain a matching service XSD.
CIS V2.4: integration branch contains a candidate/integration XSD, but no public CIS V2.4 PDF was observed in this first pass. Treat as candidate/integration material only.
```

## 3. CIS V2.3 dependency pool

Observed XSD includes:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
  includes IBIS-IP_common_V2.3.xsd
  includes IBIS-IP_Enumerations_V2.2.xsd
```

This matches the Common/Enums historical closure result:

```text
Common/Enums V2.3 pool = Common V2.3 + Enumerations V2.2.
```

Result:

```text
No CIS-specific include mismatch opened for V2.3 in this starter pass.
```

## 4. CIS V2.4 candidate/integration dependency pool

Observed XSD includes:

```text
IBIS-IP_CustomerInformationService_V2.4.xsd
  includes IBIS-IP_common_V2.4.xsd
  includes IBIS-IP_Enumerations_V2.4.xsd
```

Classification:

```text
The file is useful for the integration branch and later tool work.
It must not be described as official CIS V2.4 unless a public VDV CIS V2.4 writing or upstream acceptance is confirmed.
```

## 5. First CIS V2.3/V2.4 XSD comparison

Observed at service-operation level:

```text
CIS V2.3 and CIS V2.4 expose the same service operation group names in the first pass:
  GetAllDataResponse
  GetCurrentAnnouncementResponse
  GetCurrentConnectionInformationResponse
  GetCurrentDisplayContentResponse
  GetCurrentStopPointResponse
  GetCurrentStopIndexResponse
  GetTripDataResponse
  GetVehicleDataResponse
  RetrievePartialStopSequenceRequest
  RetrievePartialStopSequenceResponse
```

Observed service-local structural result:

```text
No service-local CIS V2.3 -> V2.4 operation addition/removal was observed in this first pass.
The main difference is dependency-family movement from Common V2.3/Enums V2.2 to Common V2.4/Enums V2.4.
```

Important inherited effects from Common/Enums V2.4:

```text
CIS V2.4 will inherit V2.4 Common/Enums changes such as LineInformation, StopInformation, TripInformation and enumeration value changes.
These must not be back-propagated to CIS V2.3 validation.
```

## 6. V2.3 PDF first-pass observations

The V2.3 PDF foreword explicitly says that the writing describes CustomerInformationService and its specific data structures. It also references VDV Mitteilung 3003 and the CIS Tool for further element usage guidance.

The V2.3 PDF operation table and XSD first pass align on the core set of Get/Subscribe/Unsubscribe concepts and the service-specific Get/Retrieve response structures.

Specific first-pass alignment point:

```text
V2.3 PDF: CurrentDisplayContentData / CurrentDisplayContent is documented as 1:*.
V2.3 XSD: CurrentDisplayContent has maxOccurs="unbounded" and no minOccurs, therefore 1:*.
```

Specific first-pass history point:

```text
V2.3 PDF version history says V2.0 changed CurrentDisplayContentData.CurrentDisplayContent to maxOccurs="unbounded".
The V2.3 XSD reflects the 1:* model.
```

## 7. Initial finding decision

Status after this starter pass:

```text
No CIS-specific finding opened yet.
No XSD change proposed.
```

Reason:

```text
This block primarily establishes provenance and routing.
V1.1/V2.0/V2.2 missing service XSDs are a coverage/provenance task, not yet a defect.
CIS V2.3 dependency usage matches the audited Common/Enums V2.3 pool.
CIS V2.4 is candidate/integration material without a public CIS V2.4 PDF observed in this pass.
```

## 8. Validation backlog impact

Later technical validation should include:

```text
CIS V2.3 pool:
  IBIS-IP_CustomerInformationService_V2.3.xsd
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd

CIS V2.4 candidate/integration pool:
  IBIS-IP_CustomerInformationService_V2.4.xsd
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

Suggested targeted samples after schema compile:

```text
V2.3 positive: GetCurrentDisplayContentResponse with one CurrentDisplayContent.
V2.3 positive: GetCurrentDisplayContentResponse with multiple CurrentDisplayContent.
V2.3 negative: GetCurrentDisplayContentResponse without CurrentDisplayContent.
V2.3 positive: VehicleData.RouteDeviation using RouteDeviationEnumeration.
V2.4 candidate positive: TripInformation.BlockNumber via inherited Common V2.4 where applicable.
V2.3 negative / V2.4 candidate positive: Common V2.4-only fields used inside inherited common structures.
```

## 9. Next CIS work

Next detailed CIS file should continue with:

```text
docs/pdf_xsd_semantic_audit/05a_cis_v1_1_v2_0_v2_2_provenance_and_pdf_history.md
```

Required next steps:

```text
1. Search repository history, forks and open PRs for CIS V1.1, V2.0 and V2.2 XSD material.
2. Compare the V1.1, V2.0 and V2.2 PDFs against any located historical XSDs.
3. If no historical XSDs are located, record exact validation-routing status for those PDF-only versions.
4. Then perform detailed CIS V2.3 PDF/XSD table pass.
5. Keep CIS V2.4 candidate separated from official PDF-backed versions.
```

## 10. Result

```text
CustomerInformationService historical audit is started.
Public PDF versions are mapped.
Observed XSD coverage is mapped.
CIS V2.3 is official and has a matching XSD/dependency pool.
CIS V2.4 exists only as integration/candidate material in this branch in this first pass.
No CIS finding opened yet.
```
