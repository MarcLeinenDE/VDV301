# CustomerInformationService findings and V2.0/V2.2/V2.3 closure

Status: first-pass closure completed for CIS V2.0, V2.2 and V2.3; local schema compilation still pending.

Scope:

```text
docs/pdf_xsd_semantic_audit/05c_cis_v1_1_mapping.md
docs/pdf_xsd_semantic_audit/05d_cis_v2_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/05e_cis_v2_2_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/05f_cis_v2_3_pdf_xsd_first_pass.md
```

Source classes:

```text
CIS V1.0/V2.0/V2.2: historical official release-tag material in dev/schema-integration.
CIS V2.3: current official upstream/current integration material.
CIS V2.4: candidate/integration material only; not part of this official PDF closure.
```

Authority rule:

```text
Where a version-exact XSD exists, executable validation follows that selected version's XSD family.
PDF differences are documented as provider-facing notes and potential post-audit review items.
No schema correction is made in this closure block.
```

## 1. Closed first-pass CIS dependency pools

The following pools are now established for later local compile/sample validation:

```text
CIS V1.0 + Common V1.0 + Enumerations V1.0
CIS V2.0 + Common V2.0 + Enumerations V2.0
CIS V2.2 + Common V2.2 + Enumerations V2.2
CIS V2.3 + Common V2.3 + Enumerations V2.2
```

CIS V1.1 remains a public-PDF-known version with no confirmed version-exact XSD mapping.

## 2. First-pass closure by version

### CIS V2.0

Result:

```text
The V2.0 XSD reflects the key V2.0 PDF history changes checked in this pass:
- CurrentDisplayContentData.CurrentDisplayContent allows 1:*.
- CurrentConnectionInformationData.CurrentConnection allows 0:*.
- SpeakerActive and StopInformationActive are present via VehicleInformationGroup.
```

Finding decision:

```text
No V2.0 schema correction proposed.
Potential PDF wording/operation-modelling notes are carried as CIS-002, CIS-003 and CIS-004.
```

### CIS V2.2

Result:

```text
The V2.2 XSD reflects the main V2.2 CIS table/history additions checked in this pass:
- AllData.TripInformation is 0:2.
- AllData.GlobalDisplayContent is 0:*.
- MyOwnVehicleMode is present through VehicleInformationGroup.
- TripState is present through VehicleInformationGroup.
- CurrentConnection remains 0:*.
- CurrentDisplayContent remains 1:*.
```

Finding decision:

```text
No V2.2 schema correction proposed.
CIS-005 is carried because the PDF appears to type MyOwnVehicleMode differently in AllData and VehicleData, while the XSD uses one shared VehicleInformationGroup.
```

### CIS V2.3

Result:

```text
The V2.3 PDF history does not introduce a local CIS operation or local CIS data-structure change in this first-pass scope.
The V2.3 XSD keeps the V2.2 local CIS model and moves the dependency pool to Common V2.3 + Enumerations V2.2.
```

Finding decision:

```text
No V2.3 schema correction proposed.
CIS-005 remains relevant in V2.3 because the same PDF/XSD typing difference around MyOwnVehicleMode is still visible.
```

## 3. Findings added to findings.md

The closure creates the following CIS finding entries:

| Finding | State | Closure classification |
|---|---|---|
| CIS-001 | unresolved provenance / validation-routing gap | V1.1 PDF exists, but no version-exact CIS V1.1 XSD confirmed. |
| CIS-002 | OK with note / cross-service modelling check pending | Subscribe/Unsubscribe are listed in PDF but not service-specific entries in CIS operation group; likely generic modelling, not a CIS schema defect at this stage. |
| CIS-003 | PDF label inconsistency candidate | `GetCurrentConnectionInformation` vs detail-table short form `GetCurrentConnectionResponse`; XSD uses `GetCurrentConnectionInformationResponse`. |
| CIS-004 | PDF label inconsistency candidate | `RetrievePartialStopSequence` vs detail-table short form `RetrievePartialStopRequest`; XSD uses `RetrievePartialStopSequenceRequest`. |
| CIS-005 | confirmed PDF/XSD documentation discrepancy candidate | PDF typing for `MyOwnVehicleMode` differs between AllData and VehicleData; XSD shared group uses `NetexMode`. |

## 4. Validation backlog impact

Later local validation should add service-level compile and targeted XML samples for:

```text
CIS V1.0 pool
CIS V2.0 pool
CIS V2.2 pool
CIS V2.3 pool
```

Suggested samples:

```text
V1.0: compile without expecting CustomerInformationServiceOperations group.
V2.0 positive: repeated CurrentDisplayContent.
V1.0 negative / V2.0 positive: repeated CurrentDisplayContent.
V2.0 positive: zero CurrentConnection.
V2.0 negative / V2.2 positive: AllData without TripInformation.
V2.0 negative / V2.2 positive: AllData.GlobalDisplayContent.
V2.0 negative / V2.2 positive: VehicleInformationGroup.MyOwnVehicleMode using NetexMode.
V2.0 negative / V2.2 positive: VehicleInformationGroup.TripState.
V2.2 and V2.3: same local CIS structures but distinct dependency pools.
CIS-005 sample: MyOwnVehicleMode must validate as NetexMode, not as a standalone PtModesEnumeration element type.
```

## 5. Post-closure decision

No official PR candidate is opened by this closure.

Reason:

```text
The CIS findings are mainly provenance, PDF wording, or documentation/table consistency issues.
The checked XSD families are internally usable as version-scoped validation authority.
Any future official-facing correction must wait for local compile/sample validation and final post-audit review.
```

## 6. Next recommended block

Continue with the next service-level audit after CIS closure:

```text
06_journey_information_service_historical_start.md
```

Before starting, first map public JIS PDF versions against observed official release-tag/current-master XSDs, applying OFFICIAL_RELEASE_BACKFILL_POLICY.md and MIXED_VERSION_VALIDATION_PREMISE.md.
## Post-audit correction — 2026-09-03

The earlier V1.1 provenance statement is superseded by `AUDIT_CORRECTION_DELTA_CIS_V11_PROVENANCE_2026-09-03.md`. A historical untagged V1.1 working XSD family exists, but it is not a V1.1 release-tag authority and does not match all published V1.1 PDF fields. See also `FINDING_REVALIDATION_CIS_2026-09-03.md` / `EV-125`.
