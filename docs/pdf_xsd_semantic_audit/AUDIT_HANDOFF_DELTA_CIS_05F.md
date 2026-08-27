# Audit handoff delta - CIS 05f

Status: after CustomerInformationService V2.3 PDF/XSD first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05f_cis_v2_3_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/cis_v2_3_pdf_xsd_first_pass_matrix.csv
```

Current result:

```text
CIS V2.3 PDF/XSD first pass completed.
No XSD correction proposed.
No official PR candidate opened.
```

Dependency-pool result:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
  -> IBIS-IP_common_V2.3.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd
```

Interpretation:

```text
CIS V2.3 follows the established V2.3 dependency model: Common V2.3 + Enumerations V2.2.
Do not infer an Enumerations V2.3 file.
Do not substitute Enumerations V2.4.
```

PDF/XSD first-pass result:

```text
Local CIS V2.3 structures are stable against CIS V2.2 in first pass.
The V2.3 PDF version history mainly records the foreword reference to the CIS tool.
Important V2.2 features are carried forward:
  AllData.GlobalDisplayContent 0:*
  AllData.TripInformation 0:2
  CurrentConnection 0:*
  CurrentDisplayContent 1:*
  MyOwnVehicleMode / TripState in VehicleInformationGroup
```

Candidates carried forward:

```text
CIS-002: PDF operation overview includes Subscribe/Unsubscribe operations; XSD operation group contains concrete response/request elements. Cross-service generic subscription modelling check required.
CIS-003: PDF GetCurrentConnectionInformation vs detail-table GetCurrentConnectionResponse vs XSD GetCurrentConnectionInformationResponse.
CIS-004: PDF RetrievePartialStopSequence vs detail-table RetrievePartialStopRequest vs XSD RetrievePartialStopSequenceRequest.
CIS-005: MyOwnVehicleMode type inconsistency: PDF AllData table says NetexMode; PDF VehicleData table says PtModesEnumeration; XSD shared VehicleInformationGroup uses NetexMode.
```

Recommended next file:

```text
docs/pdf_xsd_semantic_audit/05g_cis_findings_and_v2_0_v2_2_v2_3_closure.md
```

Next sub-steps:

```text
1. Consolidate CIS-002 through CIS-005.
2. Open CIS-005 in findings.md or a service findings file if appropriate.
3. Decide whether CIS-002/CIS-003/CIS-004 remain candidate notes until cross-service/naming-pattern review.
4. Update validation_backlog.md with CIS V1.0/V2.0/V2.2/V2.3 compile/sample entries.
5. Then handle CIS V2.4 candidate/integration provenance separately.
```
