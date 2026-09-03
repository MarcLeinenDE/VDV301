# CIS historical XSD integration decision

Status: decision recorded; historical XSD import pending.

Context:

```text
Question: Should the historical CustomerInformationService XSDs from official VDV tags be integrated into dev/schema-integration?
```

Decision:

```text
Yes. The integration branch should contain the historical CIS service XSDs that are required for version-exact validation.
```

Reason:

```text
The current master branch only shows the newest/current service schema state for several services. Historical VDV301 field systems still use older service versions. Therefore the audit/tool branch must preserve the historical executable schema files from official VDV tags as separate files, not replace them with latest versions.
```

Source facts already verified:

```text
VDVde/VDV301 tags exist for VDV-301-1.0, VDV-301-2.0, VDV-301-2.1, VDV-301-2.2 and VDV-301-2.3.
VDV-301-1.0 contains IBIS-IP_CustomerInformationService_V1.0.xsd.
VDV-301-2.0 contains IBIS-IP_CustomerInformationService_V2.0.xsd.
VDV-301-2.1 still contains IBIS-IP_CustomerInformationService_V2.0.xsd.
VDV-301-2.2 contains IBIS-IP_CustomerInformationService_V2.2.xsd.
Current master contains IBIS-IP_CustomerInformationService_V2.3.xsd.
```

Integration rules:

```text
1. Import historical CIS XSDs only from official VDVde tags, preserving exact contents.
2. Preserve original filenames.
3. Do not rewrite include versions during import.
4. Label provenance in audit docs, not inside the upstream-copied XSDs unless a separate provenance wrapper is used.
5. Do not treat imported historical XSDs as new upstream corrections; they are historical official tag material used for audit and tool validation.
```

Target files for integration:

```text
IBIS-IP_CustomerInformationService_V1.0.xsd  <- VDVde/VDV301 tag VDV-301-1.0
IBIS-IP_CustomerInformationService_V2.0.xsd  <- VDVde/VDV301 tag VDV-301-2.0
IBIS-IP_CustomerInformationService_V2.2.xsd  <- VDVde/VDV301 tag VDV-301-2.2
```

CIS V1.1 note:

```text
The public VDV page lists CustomerInformationService V1.1 as a PDF publication. The official tag check found CIS V1.0 XSD in tag VDV-301-1.0, but no CIS V1.1 XSD has been confirmed yet. Therefore CIS V1.1 must be treated as a separate PDF-vs-XSD mapping question: possibly V1.1 PDF with V1.0 schema, but this must not be assumed without source evidence.
```

Immediate next action:

```text
Import the three historical XSDs into dev/schema-integration and then update 05a provenance docs/matrices to replace the earlier first-pass "not found" classification.
```
## Post-audit correction — 2026-09-03

The earlier V1.1 provenance statement is superseded by `AUDIT_CORRECTION_DELTA_CIS_V11_PROVENANCE_2026-09-03.md`. A historical untagged V1.1 working XSD family exists, but it is not a V1.1 release-tag authority and does not match all published V1.1 PDF fields. See also `FINDING_REVALIDATION_CIS_2026-09-03.md` / `EV-125`.
