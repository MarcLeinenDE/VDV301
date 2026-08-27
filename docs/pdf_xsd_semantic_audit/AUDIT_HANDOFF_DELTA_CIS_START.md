# Audit handoff delta - CIS start

Status: supplemental delta to `AUDIT_HANDOFF.md` after starting CustomerInformationService audit.

Current branch after this delta:

```text
dev/schema-integration
```

New CIS audit files:

```text
docs/pdf_xsd_semantic_audit/05_cis_historical_audit_start.md
docs/pdf_xsd_semantic_audit/generated/cis_version_xsd_matrix.csv
```

Current CIS result:

```text
CustomerInformationService historical audit is started.
Public PDF versions observed on the VDV index: V1.1, V2.0, V2.2, V2.3.
Observed official upstream CIS service XSD: IBIS-IP_CustomerInformationService_V2.3.xsd.
Observed dev/schema-integration CIS service XSDs: V2.3 and V2.4.
No CIS V1.1/V2.0/V2.2 service XSD was observed in dev/schema-integration during this first pass.
No public CIS V2.4 PDF was observed on the VDV index during this first pass.
```

Classification:

```text
CIS V1.1/V2.0/V2.2: public PDFs exist, but matching service XSDs must still be searched in repository history/forks/PRs before final validation-routing status is assigned.
CIS V2.3: official PDF-backed XSD present; dependency pool is CIS V2.3 + Common V2.3 + Enumerations V2.2.
CIS V2.4: candidate/integration material only in this branch; dependency pool is CIS V2.4 + Common V2.4 + Enumerations V2.4. Do not label official until PDF/upstream acceptance is confirmed.
```

No new CIS-specific finding was opened in this starter pass.

Next recommended CIS file:

```text
docs/pdf_xsd_semantic_audit/05a_cis_v1_1_v2_0_v2_2_provenance_and_pdf_history.md
```

Next steps:

```text
1. Search official repo history, forks and open PRs for CIS V1.1/V2.0/V2.2 XSD material.
2. Compare V1.1/V2.0/V2.2 PDF facts against any located XSD material.
3. If no historical XSDs are found, record PDF-only validation-routing status explicitly.
4. Then do detailed CIS V2.3 PDF/XSD table pass.
5. Keep CIS V2.4 candidate separate from official PDF-backed versions.
```
