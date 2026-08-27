# Audit handoff delta - CIS 05c V1.1 mapping

Status: after CustomerInformationService V1.1 PDF-to-XSD mapping first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05c_cis_v1_1_mapping.md
docs/pdf_xsd_semantic_audit/generated/cis_v1_1_mapping_matrix.csv
```

Current result:

```text
CIS V1.1 is a public VDV PDF version.
No version-exact IBIS-IP_CustomerInformationService_V1.1.xsd has been confirmed in the checked official source set.
CIS V1.0 XSD exists and is official historical release material, but it must not be silently used as CIS V1.1 validation authority.
CIS V2.0 XSD exists and has features that resemble visible V1.1 PDF features, but it must not be silently used as CIS V1.1 validation authority either.
```

Important observed reason:

```text
The CIS V1.1 PDF includes items such as SpeakerActive and StopInformationActive.
CIS V1.0 XSD does not contain these local VehicleInformationGroup items.
CIS V2.0 XSD does contain them, but V2.0 is a later version-exact schema family.
```

Conservative validator rule:

```text
CIS V1.0 selected -> use CIS V1.0 + Common V1.0 + Enumerations V1.0.
CIS V1.1 selected -> public PDF known, exact XSD mapping unresolved; strict XSD validation cannot be claimed.
CIS V2.0 selected -> use CIS V2.0 + Common V2.0 + Enumerations V2.0.
```

Finding/register note:

```text
CIS-001 should be tracked when the findings register is next consolidated:
CustomerInformationService V1.1 public PDF has no confirmed version-exact XSD mapping.
State: unresolved provenance / validation-routing gap.
```

Next recommended detailed file:

```text
docs/pdf_xsd_semantic_audit/05d_cis_v2_0_pdf_xsd_first_pass.md
```

Next sub-steps:

```text
1. Start CIS PDF/XSD detail work with V2.0 because V2.0 has both public PDF and official release-tag XSD.
2. Compare V2.0 operation table and key data structures against CIS V2.0 XSD.
3. Then continue CIS V2.2 and V2.3.
4. Keep CIS V1.1 unresolved unless a source-exact mapping is found.
```
