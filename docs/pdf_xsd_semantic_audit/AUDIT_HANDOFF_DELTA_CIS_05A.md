# Audit handoff delta - CIS provenance 05a

Status: delta handoff after CustomerInformationService V1.1/V2.0/V2.2 provenance first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05a_cis_v1_1_v2_0_v2_2_provenance_and_pdf_history.md
docs/pdf_xsd_semantic_audit/generated/cis_v1_1_v2_0_v2_2_provenance_matrix.csv
```

Current result:

```text
Public CIS PDF versions confirmed as audit targets:
  V1.1, V2.0, V2.2, V2.3.

Current official VDVde/VDV301 master service-XSD observation:
  CIS V2.3 present.
  CIS V1.1/V2.0/V2.2 not observed.

Current dev/schema-integration observation:
  CIS V2.3 present.
  CIS V2.4 present as integration/candidate material.
  CIS V1.1/V2.0/V2.2 not observed.
```

Important classification:

```text
The absence of CIS V1.1/V2.0/V2.2 service XSDs in first-pass checked sources is a provenance gap, not a confirmed schema defect.
Do not validate older CIS traffic against CIS V2.3 by latest-wins substitution.
Do not label CIS V2.4 as official; no public CIS V2.4 PDF was observed in this pass.
```

First executable CIS baseline:

```text
CIS V2.3 + Common V2.3 + Enumerations V2.2.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/05b_cis_v2_3_pdf_xsd_first_pass.md
```

Next sub-steps:

```text
1. Compare CIS V2.3 operation group/top-level elements to the V2.3 PDF operation set.
2. Check key CIS V2.3 structures:
   AllData
   CurrentAnnouncementData
   CurrentConnectionInformationData
   CurrentDisplayContentData
   CurrentStopPointData
   CurrentStopIndexData
   TripData
   VehicleData
   PartialStopSequenceData
3. Keep inherited Common/Enums findings separate from CIS-specific findings.
4. Keep CIS V1.1/V2.0/V2.2 in source-recovery backlog.
```
