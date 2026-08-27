# Audit handoff delta - JourneyInformationService start

Status: JourneyInformationService historical start completed.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/06_journey_information_service_historical_start.md
docs/pdf_xsd_semantic_audit/generated/jis_historical_scope_matrix.csv
```

Current JIS result:

```text
Public JIS PDF observed: VDV 301-2-6 JourneyInformationService V1.0, 07/2016.
Official upstream current master contains IBIS-IP_JourneyInformationService_V1.0.xsd.
Integration branch contains IBIS-IP_JourneyInformationService_V1.0.xsd.
No version-exact JIS V2.x service XSD observed in the checked first-pass GitHub search.
```

Dependency pool:

```text
JIS V1.0 + Common V1.0 + Enumerations V1.0
```

First-pass operation model note:

```text
JIS V1.0 already has a local service group named JourneyInformationServiceGroup and top-level JourneyInformationService.* elements.
```

Finding decision:

```text
No JIS-specific finding opened yet.
Potential subscription/generic response observations stay as candidates until the detailed V1.0 PDF/XSD pass.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/06a_jis_v1_0_pdf_xsd_first_pass.md
```

Next sub-steps:

```text
1. Compare the V1.0 PDF operation table against JourneyInformationServiceGroup.
2. Compare central response/request structures and cardinalities.
3. Decide whether any JIS findings need to be opened after the detailed pass.
4. Keep subscription/generic response modelling aligned with CIS-002 cross-service review.
```
