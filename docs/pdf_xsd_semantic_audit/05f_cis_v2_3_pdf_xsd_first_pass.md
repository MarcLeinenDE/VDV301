# CustomerInformationService V2.3 PDF/XSD first pass

Status: PDF/XSD first pass completed for CIS V2.3; local schema compilation still pending.

Scope:

```text
VDV 301-2-3 CustomerInformationService V2.3 PDF source
IBIS-IP_CustomerInformationService_V2.3.xsd
IBIS-IP_common_V2.3.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Source class:

```text
CIS V2.3 service XSD is current upstream/current integration material.
The dependency pool is Common V2.3 + Enumerations V2.2.
```

Authority rule:

```text
Executable validation follows the selected XSD dependency pool.
PDF differences are documented as provider-facing notes and audit findings/candidates.
No schema correction is made in this pass.
```

Mixed-version rule:

```text
Do not validate CIS V2.2 traffic against CIS V2.3 by latest-wins substitution.
Do not replace the CIS V2.3 dependency pool with Enumerations V2.4.
CIS V2.3 uses Common V2.3 + Enumerations V2.2.
```

## 1. PDF identity and version-history result

Observed PDF identity:

```text
VDV-Schrift 301-2-3
CustomerInformationService
V2.3
12/2020
```

The V2.3 PDF contains the public-operation/data-structure tables and records the V2.3 history item as a technical/textual documentation update:

```text
V2.3 technical upgrade/correction:
Reference to the CIS tool in the foreword.
```

Interpretation:

```text
The PDF version history does not indicate a new local CIS operation or local CIS data-structure change in V2.3.
The V2.3 XSD-side first pass matches this: local CIS structures appear stable against V2.2; the main version shift is the dependency pool Common V2.3 + Enumerations V2.2.
```

## 2. Dependency-pool check

Observed XSD includes:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
  -> IBIS-IP_common_V2.3.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd
```

Classification:

```text
OK with dependency note.
This is the same V2.3 Common/Enums pattern already established in the Common/Enums history block.
Do not create or infer IBIS-IP_Enumerations_V2.3.xsd.
Do not substitute Enumerations V2.4.
```

## 3. Operation set

Observed XSD operation group:

```text
CustomerInformationServiceOperations
```

It contains the same ten concrete operation elements already observed in CIS V2.0 and V2.2:

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

PDF operation overview:

```text
The PDF lists the broader operation set including Get, Subscribe and Unsubscribe operations.
For subscription/unsubscription chapters, the PDF repeatedly points to the generic SubscribeRequest/SubscribeResponse and UnsubscribeRequest/UnsubscribeResponse structures from VDV 301-2-1.
```

First-pass classification:

```text
No new CIS V2.3 operation-group finding is opened in this file.
The previously noted CIS-002 candidate remains a cross-service modelling question:
CIS-specific XSD operation group contains concrete response/request elements, while PDF tables describe service operations including generic subscribe/unsubscribe behaviour.
```

## 4. Main structure checks

Generated summary file:

```text
docs/pdf_xsd_semantic_audit/generated/cis_v2_3_pdf_xsd_first_pass_matrix.csv
```

### AllData

Observed PDF/XSD alignment:

```text
TimeStamp: 1:1
VehicleRef: 1:1
DefaultLanguage: 1:1
GlobalDisplayContent: 0:*
TripInformation: 0:2
CurrentStopIndex: 1:1
VehicleInformationGroup included
```

Classification:

```text
OK in first pass.
The V2.2 additions GlobalDisplayContent and TripInformation 0:2 are carried forward into V2.3.
```

### CurrentConnectionInformationData

Observed PDF/XSD alignment:

```text
TimeStamp: 1:1
CurrentConnection: 0:*
```

Classification:

```text
OK in first pass.
The V2.0 technical correction is carried forward.
```

Naming note:

```text
The PDF detail table still prints CustomerInformationService.GetCurrentConnectionResponse.
The operation overview and XSD use CustomerInformationService.GetCurrentConnectionInformationResponse.
Carry forward CIS-003 as candidate note; no schema correction in this pass.
```

### CurrentDisplayContentData

Observed PDF/XSD alignment:

```text
TimeStamp: 1:1
CurrentDisplayContent: 1:*
```

Classification:

```text
OK in first pass.
The V2.0 technical correction is carried forward.
```

### CurrentAnnouncementData / CurrentStopPointData / CurrentStopIndexData

Observed:

```text
The local CIS V2.3 XSD structures match the stable V2.x pattern observed in V2.0/V2.2.
No V2.3-specific local delta observed.
```

Classification:

```text
No CIS V2.3-specific finding opened.
```

### TripData

Observed PDF/XSD alignment:

```text
TimeStamp: 1:1
VehicleRef: 1:1
DefaultLanguage: 1:1
TripInformation: 1:1
CurrentStopIndex: 1:1
```

Classification:

```text
OK in first pass.
```

### VehicleData

Observed XSD model:

```text
VehicleData uses VehicleInformationGroup.
VehicleInformationGroup contains MyOwnVehicleMode type NetexMode.
```

Observed PDF table:

```text
The AllData table lists MyOwnVehicleMode as NetexMode.
The VehicleData table lists MyOwnVehicleMode as PtModesEnumeration.
```

Classification:

```text
CIS-005 candidate strengthened/confirmed for V2.3:
The PDF is internally inconsistent between AllData and VehicleData, while the XSD uses one shared VehicleInformationGroup and therefore one type: NetexMode.
Validation follows XSD.
```

No XSD correction is proposed in this pass.

### RetrievePartialStopSequence

Observed PDF/XSD issue carried forward:

```text
PDF operation name: RetrievePartialStopSequence.
PDF detail table name: CustomerInformationService.RetrievePartialStopRequest.
XSD request element/type: CustomerInformationService.RetrievePartialStopSequenceRequest / CustomerInformationService.RetrievePartialStopSequenceRequestStructure.
```

Classification:

```text
Carry forward CIS-004 as candidate note.
Likely PDF/table-name shorthand or documentation inconsistency.
No schema correction in this pass.
```

## 5. Finding/candidate decision

Status after this pass:

```text
No XSD correction proposed.
No official PR candidate opened.
No immediate schema import/backfill action required.
```

Finding candidates after checking V2.3:

```text
CIS-002: PDF operation overview includes Subscribe/Unsubscribe operations while the XSD operation group contains concrete response/request elements; generic subscription modelling must be checked cross-service.
CIS-003: GetCurrentConnectionInformation naming vs GetCurrentConnectionResponse table name.
CIS-004: RetrievePartialStopSequence naming vs RetrievePartialStopRequest table name.
CIS-005: MyOwnVehicleMode type inconsistency: AllData PDF NetexMode, VehicleData PDF PtModesEnumeration, XSD NetexMode.
```

Recommended classification for next findings-register update:

```text
Open CIS-005 as confirmed PDF-internal/XSD type-name discrepancy candidate.
Keep CIS-002/CIS-003/CIS-004 as candidate notes until cross-service/naming-pattern review.
```

## 6. Validation backlog impact

Later local technical validation should compile this exact pool:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
IBIS-IP_common_V2.3.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Suggested targeted samples:

```text
Positive: AllData with no TripInformation and with GlobalDisplayContent.
Positive: CurrentConnectionInformationData with zero CurrentConnection.
Positive: CurrentDisplayContentData with repeated CurrentDisplayContent.
Positive: VehicleData with MyOwnVehicleMode encoded as NetexMode according to XSD.
Negative: payload/model that assumes a PtModesEnumeration element/type for MyOwnVehicleMode in VehicleData.
```

## 7. Next CIS audit step

Next detailed step:

```text
05g_cis_findings_and_v2_0_v2_2_v2_3_closure.md
```

Recommended sub-steps:

```text
1. Consolidate CIS-002 through CIS-005.
2. Decide which CIS candidates should enter findings.md now and which should remain service-note candidates.
3. Update validation_backlog.md with CIS compile/sample entries for V1.0, V2.0, V2.2 and V2.3.
4. Then move to CIS V2.4 candidate/integration provenance if still needed.
```
