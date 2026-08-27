# Audit handoff delta - CIS official tag correction

Status: corrected after official VDV tag check and historical XSD import.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

Important correction:

```text
The earlier CIS 05a first pass checked current master/current integration state only and therefore classified CIS V1.1/V2.0/V2.2 as XSD-not-found.
A follow-up check of official VDVde/VDV301 tags found historical CIS XSDs for V1.0, V2.0 and V2.2.
```

Imported files:

```text
IBIS-IP_CustomerInformationService_V1.0.xsd  from VDVde/VDV301 tag VDV-301-1.0
IBIS-IP_CustomerInformationService_V2.0.xsd  from VDVde/VDV301 tag VDV-301-2.0
IBIS-IP_CustomerInformationService_V2.2.xsd  from VDVde/VDV301 tag VDV-301-2.2
```

Updated files:

```text
docs/pdf_xsd_semantic_audit/05a_cis_v1_1_v2_0_v2_2_provenance_and_pdf_history.md
docs/pdf_xsd_semantic_audit/generated/cis_v1_1_v2_0_v2_2_provenance_matrix.csv
docs/pdf_xsd_semantic_audit/CIS_HISTORICAL_XSD_INTEGRATION_DECISION.md
```

Corrected CIS dependency pools now available:

```text
CIS V1.0 + common V1.0 + Enumerations V1.0
CIS V2.0 + common V2.0 + Enumerations V2.0
CIS V2.2 + common V2.2 + Enumerations V2.2
CIS V2.3 + common V2.3 + Enumerations V2.2
CIS V2.4 candidate + common V2.4 + Enumerations V2.4
```

Remaining open question:

```text
The public VDV page lists CIS V1.1, but the official tag contains CIS V1.0 XSD.
Do not assume the V1.1 PDF maps to CIS V1.0 XSD until the V1.1 publication/release context is checked.
```

Next recommended detailed file:

```text
docs/pdf_xsd_semantic_audit/05b_cis_v1_0_v2_0_v2_2_v2_3_xsd_history_compare.md
```

Next sub-steps:

```text
1. Compare CIS V1.0 -> V2.0 -> V2.2 -> V2.3 XSD operation sets and structures.
2. Resolve CIS V1.1 PDF-to-XSD mapping.
3. Then perform detailed CIS V2.3 PDF/XSD first pass.
```
