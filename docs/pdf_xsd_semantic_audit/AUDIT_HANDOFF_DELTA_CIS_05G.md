# Audit handoff delta - CIS 05g closure

Status: CustomerInformationService first-pass closure after CIS V2.0/V2.2/V2.3 PDF/XSD checks.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05g_cis_findings_and_v2_0_v2_2_v2_3_closure.md
docs/pdf_xsd_semantic_audit/generated/cis_findings_closure_matrix.csv
```

Updated files:

```text
docs/pdf_xsd_semantic_audit/findings.md
```

CIS closure result:

```text
CIS V2.0 first pass: no schema correction proposed.
CIS V2.2 first pass: no schema correction proposed.
CIS V2.3 first pass: no schema correction proposed.
CIS V1.1 remains unresolved exact-XSD mapping.
```

CIS findings now recorded:

```text
CIS-001 unresolved provenance / validation-routing gap: V1.1 PDF without confirmed V1.1 XSD.
CIS-002 OK with note / cross-service modelling check pending: Subscribe/Unsubscribe PDF concepts vs local operation group.
CIS-003 PDF label inconsistency candidate: GetCurrentConnectionInformation vs GetCurrentConnectionResponse wording.
CIS-004 PDF label inconsistency candidate: RetrievePartialStopSequence vs RetrievePartialStopRequest wording.
CIS-005 confirmed PDF/XSD documentation discrepancy candidate: MyOwnVehicleMode NetexMode vs PtModesEnumeration table inconsistency; XSD uses NetexMode.
```

Closed first-pass CIS validation pools:

```text
CIS V1.0 + Common V1.0 + Enumerations V1.0
CIS V2.0 + Common V2.0 + Enumerations V2.0
CIS V2.2 + Common V2.2 + Enumerations V2.2
CIS V2.3 + Common V2.3 + Enumerations V2.2
```

No official PR candidate opened:

```text
The CIS closure produced provider-facing notes and candidate documentation discrepancies, not a direct XSD correction proposal.
Local compile/sample validation remains pending before any post-audit official-facing decision.
```

Next recommended block:

```text
docs/pdf_xsd_semantic_audit/06_journey_information_service_historical_start.md
```

Next recommended method:

```text
1. Map public JourneyInformationService PDF versions.
2. Check official VDVde/VDV301 release tags and current master for version-exact JIS XSDs.
3. Use official release backfill only for historical material.
4. Keep newer PR/candidate material clearly labelled as candidate/integration.
5. Do not use latest-wins validation.
```
