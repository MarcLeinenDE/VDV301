# Audit handoff delta - JIS V1.0 PDF/XSD first pass

Status: completed after JourneyInformationService V1.0 PDF/XSD first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/06a_jis_v1_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/jis_v1_0_pdf_xsd_first_pass_matrix.csv
```

Scope:

```text
VDV 301-2-6 JourneyInformationService V1.0 PDF
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Main result:

```text
JIS V1.0 first pass is broadly aligned for DataContent, CurrentBlockRef, RetrievePartialTripSequence, RetrieveSpecific* patterns and most ListAll* repeatable structures.
No XSD correction was made.
No official PR candidate was opened.
```

Candidate notes carried forward:

```text
JIS-001: Subscribe/Unsubscribe operations are listed in the PDF but not local service-specific group elements in the JIS XSD.
JIS-002: Set* operations list generic DataAcceptedResponseStructure responses; the local JIS XSD contains Set*Request elements only.
JIS-003: ListAllLineInformation PDF 1:* vs XSD default 1:1 for LineInformation.
JIS-004: RetrieveAllRoutesPerLine detailed request table appears to be labelled SetBlockNumberRequest in the PDF.
JIS-005: RetrieveSpecificGNSSPointInformation response data element label may differ between PDF wording and XSD element name.
```

Strongest candidate:

```text
JIS-003 appears to be the strongest PDF/XSD cardinality candidate:
PDF table: LineInformation 1:*.
XSD: LineInformation without maxOccurs, therefore 1:1 by XML Schema default.
```

Next recommended detailed file:

```text
docs/pdf_xsd_semantic_audit/06b_jis_findings_and_closure.md
```

Next sub-steps:

```text
1. Confirm JIS candidate classifications.
2. Append confirmed JIS findings to findings.md.
3. Add validation backlog samples for JIS V1.0.
4. Keep JIS V1.0 dependency pool scoped to Common V1.0 + Enumerations V1.0.
```
