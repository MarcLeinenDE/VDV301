# Audit handoff delta - CIS 05e

Status: after CustomerInformationService V2.2 PDF/XSD first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05e_cis_v2_2_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/cis_v2_2_pdf_xsd_first_pass_matrix.csv
```

Current result:

```text
CIS V2.2 PDF/XSD first pass completed.
Most local V2.2 structures align with the imported official-release XSD.
No findings.md update in this pass.
No XSD correction proposed.
```

Main aligned V2.2 points:

```text
AllData.TripInformation 0:2.
AllData.GlobalDisplayContent 0:*.
AllData.MyOwnVehicleMode 0:1 NetexMode.
AllData.TripState 0:1 TripStateEnumeration.
CurrentConnection 0:*.
CurrentDisplayContent 1:*.
VehicleData.TripState 0:1 TripStateEnumeration.
```

Carried candidate notes:

```text
CIS-002: service-specific Subscribe/Unsubscribe operations in PDF vs concrete service-specific XSD operation group elements only. Cross-service modelling check required.
CIS-003: GetCurrentConnectionInformation operation overview vs GetCurrentConnectionResponse detail-table heading; XSD follows operation overview.
CIS-004: RetrievePartialStopSequence operation overview vs RetrievePartialStopRequest detail-table heading; XSD follows operation overview.
```

New candidate note:

```text
CIS-005: V2.2 PDF VehicleData table types MyOwnVehicleMode as PtModesEnumeration, while XSD uses NetexMode. The V2.2 PDF AllData table also uses NetexMode, so this looks like a table inconsistency candidate. Check V2.3 before opening findings.md.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/05f_cis_v2_3_pdf_xsd_first_pass.md
```

Next sub-steps:

```text
1. Compare CIS V2.3 PDF and XSD against V2.2 local structures.
2. Check whether the V2.3 PDF repeats or corrects the VehicleData.MyOwnVehicleMode PtModesEnumeration/NetexMode issue.
3. Decide after V2.3 whether CIS-002 through CIS-005 should be promoted into findings.md.
4. Keep inherited Common/Enums findings separate from CIS-specific findings.
```
