# CustomerInformationService V1.1 / V2.0 / V2.2 provenance and PDF-history audit

Status: provenance first pass completed; no schema correction proposed.

Scope:

```text
VDV 301-2-3 CustomerInformationService V1.1 PDF listing
VDV 301-2-3 CustomerInformationService V2.0 PDF source
VDV 301-2-3 CustomerInformationService V2.2 PDF source
VDVde/VDV301 master repository contents
MarcLeinenDE/VDV301 dev/schema-integration repository contents
first-pass GitHub PR/commit/file searches for historical CIS XSDs
```

Authority rule:

```text
Validation follows the selected version's XSD family where a version-exact XSD is available.
PDF evidence is documentation evidence and can be used for audit/routing, but it is not a replacement for a missing historical XSD.
No schema is reconstructed or corrected in this pass.
```

Mixed-version rule:

```text
Do not validate CIS V1.1, V2.0 or V2.2 traffic against CIS V2.3 only because CIS V2.3 is the earliest CIS service XSD currently observed in the current repository state.
Older CIS versions remain separate audit targets.
```

## 1. Public PDF publication map

The public VDV IP-KOM-ÖV page lists these CustomerInformationService publications:

```text
VDV 301-2-3 CustomerInformationService V1.1
VDV 301-2-3 CustomerInformationService V2.0
VDV 301-2-3 CustomerInformationService V2.2
VDV 301-2-3 CustomerInformationService V2.3
```

First-pass PDF-source observations from public search/opened snippets:

```text
V2.0 PDF: VDV-Schrift 301-2-3, 02/2018, Dienst CustomerInformationService V 2.0.
V2.2 PDF: VDV-Schrift 301-2-3, 08/2019, CustomerInformationService V 2.2.
V2.3 PDF: VDV-Schrift 301-2-3, 12/2020, CustomerInformationService V 2.3.
V1.1: public VDV page lists the publication, but this pass did not yet retrieve a direct standalone PDF text snippet beyond the listing.
```

Important source note:

```text
The VDV page also states that all VDV 301 documents from V2.0 onward are bilingual.
Therefore CIS V1.1 must not be assumed to have the same bilingual/table layout style as the V2.x documents.
```

## 2. Repository XSD availability map

### Official upstream master

Observed in `VDVde/VDV301` current master contents:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd is present.
No IBIS-IP_CustomerInformationService_V1.1.xsd observed.
No IBIS-IP_CustomerInformationService_V2.0.xsd observed.
No IBIS-IP_CustomerInformationService_V2.2.xsd observed.
```

### Integration branch

Observed in `MarcLeinenDE/VDV301` `dev/schema-integration` contents:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd is present.
IBIS-IP_CustomerInformationService_V2.4.xsd is present as integration/candidate material.
No IBIS-IP_CustomerInformationService_V1.1.xsd observed.
No IBIS-IP_CustomerInformationService_V2.0.xsd observed.
No IBIS-IP_CustomerInformationService_V2.2.xsd observed.
```

## 3. First-pass GitHub/search provenance result

First-pass searches performed:

```text
VDVde/VDV301 commit search for CustomerInformationService.
VDVde/VDV301 pull-request search for CustomerInformationService.
VDVde/VDV301 branch search for CIS.
Web search for exact historical filenames:
  IBIS-IP_CustomerInformationService_V1.1.xsd
  IBIS-IP_CustomerInformationService_V2.0.xsd
  IBIS-IP_CustomerInformationService_V2.2.xsd
  IBIS-IP_CustomerInformationService_V2.4.xsd
```

First-pass result:

```text
No historical CIS V1.1, V2.0 or V2.2 service XSD was found in these first-pass searches.
No pull request explicitly about CustomerInformationService history was found in the checked repository search.
```

Interpretation:

```text
This does not prove that no historical CIS XSD ever existed.
It only means the exact historical CIS service XSDs were not found in the currently checked public/current repository state and first-pass searches.
Possible remaining sources include old Git history not matched by search, archived downloads, ZIP bundles, CIS Excel tool material, local vendor/tool archives or VDV internal material.
```

## 4. Version-specific classification

| CIS version | Public PDF listed | Service XSD observed in current official master | Service XSD observed in dev/schema-integration | First-pass classification |
|---|---:|---:|---:|---|
| V1.1 | yes | no | no | PDF-publication known; XSD recovery required before true XSD validation. |
| V2.0 | yes | no | no | PDF-publication known; XSD recovery required before true XSD validation. |
| V2.2 | yes | no | no | PDF-publication known; XSD recovery required before true XSD validation. |
| V2.3 | yes | yes | yes | First currently observed official service-XSD baseline. |
| V2.4 | no public CIS V2.4 PDF observed in this pass | no | yes | Integration/candidate only; do not label official. |

## 5. CIS V2.3 baseline dependency pool

Observed CIS V2.3 include family:

```text
IBIS-IP_CustomerInformationService_V2.3.xsd
  includes IBIS-IP_common_V2.3.xsd
  includes IBIS-IP_Enumerations_V2.2.xsd
```

This aligns with the Common/Enums historical closure:

```text
Common V2.3 + Enumerations V2.2 is a legitimate V2.3 dependency pool in the observed branch state.
```

## 6. CIS V2.4 integration/candidate dependency pool

Observed CIS V2.4 include family:

```text
IBIS-IP_CustomerInformationService_V2.4.xsd
  includes IBIS-IP_common_V2.4.xsd
  includes IBIS-IP_Enumerations_V2.4.xsd
```

Classification:

```text
CIS V2.4 stays integration/candidate material until a public CIS V2.4 PDF/source authority or accepted upstream state is confirmed.
It is useful for tool/internal experiments but not an official-facing correction baseline in this pass.
```

## 7. Finding decision

Status after this pass:

```text
No CIS-specific finding opened.
No XSD change proposed.
No historical CIS XSD is reconstructed.
```

Reason:

```text
The absence of CIS V1.1/V2.0/V2.2 service XSDs in the currently checked sources is a provenance gap, not yet a confirmed PDF/XSD contradiction.
The correct next action is source recovery and then version-specific comparison.
```

## 8. Tool/SDK implication

For the later validator/SDK:

```text
CIS V2.3 can be mapped to an executable XSD pool:
  CIS V2.3 + Common V2.3 + Enumerations V2.2.

CIS V1.1/V2.0/V2.2 must not be silently validated with CIS V2.3.
Until version-exact XSDs are recovered or a deliberate PDF-derived compatibility profile is approved, they should be marked as:
  known public version, XSD not yet available in audited source set.
```

Potential user-facing validator wording later:

```text
CIS V2.0 selected: a public VDV PDF exists, but no version-exact CIS V2.0 XSD is available in the audited source set yet. XSD validation cannot be claimed for this version until the historical schema is recovered or an explicitly labelled compatibility profile is selected.
```

## 9. Next CIS audit step

Next detailed file:

```text
docs/pdf_xsd_semantic_audit/05b_cis_v2_3_pdf_xsd_first_pass.md
```

Required next steps:

```text
1. Use CIS V2.3 as the first executable CIS baseline because it has both public PDF and service XSD evidence.
2. Compare top-level operations/group entries against the CIS V2.3 PDF operation set.
3. Check key data structures: AllData, CurrentAnnouncementData, CurrentConnectionInformationData, CurrentDisplayContentData, CurrentStopPointData, CurrentStopIndexData, TripData, VehicleData, PartialStopSequenceData.
4. Track inherited Common/Enums findings separately from CIS-specific findings.
5. Keep older CIS V1.1/V2.0/V2.2 in the source-recovery backlog.
```

## 10. Result

```text
CIS V1.1/V2.0/V2.2 provenance first pass is complete.
The older public CIS versions are confirmed as audit targets, but no version-exact historical service XSD was found in the checked sources.
CIS V2.3 is the first executable baseline for detailed CIS PDF/XSD comparison.
Next: CIS V2.3 PDF/XSD first pass.
```
