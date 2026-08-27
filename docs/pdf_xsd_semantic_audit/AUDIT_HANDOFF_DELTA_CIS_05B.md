# Audit handoff delta - CIS 05b XSD history compare

Status: delta handoff after CustomerInformationService XSD-side historical first pass.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New files:

```text
docs/pdf_xsd_semantic_audit/05b_cis_v1_0_v2_0_v2_2_v2_3_xsd_history_compare.md
docs/pdf_xsd_semantic_audit/generated/cis_v1_0_v2_0_v2_2_v2_3_xsd_history_delta.csv
```

Source context:

```text
CIS V1.0, V2.0 and V2.2 were backfilled unchanged from official VDVde/VDV301 release tags.
CIS V2.3 is present in the current official master and in dev/schema-integration.
```

Observed dependency pools:

```text
CIS V1.0 + Common V1.0 + Enumerations V1.0
CIS V2.0 + Common V2.0 + Enumerations V2.0
CIS V2.2 + Common V2.2 + Enumerations V2.2
CIS V2.3 + Common V2.3 + Enumerations V2.2
```

First-pass XSD-side results:

```text
V1.0 uses an older service-XSD style: structures exist, but no CustomerInformationServiceOperations group and no top-level CustomerInformationService.* operation elements are present in the same style as V2.x.
V2.0 introduces/uses the V2.x operation group/top-level element model with ten operation entries.
V2.2 keeps the operation set stable and adds/changes data model behaviour: AllData.TripInformation optional, GlobalDisplayContent added, NetexMode/TripState supported.
V2.3 keeps local CIS operation structures stable versus V2.2 and mainly changes the dependency pool to Common V2.3 + Enumerations V2.2.
```

No finding opened:

```text
Observed differences are XSD version-history deltas.
CIS-specific PDF/XSD mismatch findings require matching PDF table checks.
```

Remaining open question:

```text
CIS V1.1 public PDF mapping is still open.
Do not silently map CIS V1.1 to CIS V1.0 XSD until publication/release context is checked.
```

Next recommended detailed files:

```text
docs/pdf_xsd_semantic_audit/05c_cis_v1_1_mapping.md
docs/pdf_xsd_semantic_audit/05d_cis_v2_0_v2_2_v2_3_pdf_xsd_first_pass.md
```
