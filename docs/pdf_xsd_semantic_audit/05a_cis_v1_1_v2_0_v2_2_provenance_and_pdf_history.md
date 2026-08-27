# CustomerInformationService historical XSD provenance correction

Status: corrected after official VDV tag check; historical CIS XSDs imported into dev/schema-integration.

Scope:

```text
VDV 301-2-3 CustomerInformationService V1.1 PDF listing
VDV 301-2-3 CustomerInformationService V2.0 PDF source/listing
VDV 301-2-3 CustomerInformationService V2.2 PDF source/listing
VDV 301-2-3 CustomerInformationService V2.3 PDF source/listing
Official VDVde/VDV301 tags VDV-301-1.0, VDV-301-2.0, VDV-301-2.1, VDV-301-2.2, VDV-301-2.3
MarcLeinenDE/VDV301 dev/schema-integration
```

Correction note:

```text
The earlier 05a first pass looked only at current master/current integration branch state and therefore incorrectly classified CIS V1.1/V2.0/V2.2 as XSD-not-found.
A follow-up check of official VDVde/VDV301 tags found historical CIS XSDs.
This file supersedes the earlier first-pass classification.
```

Authority rule:

```text
Validation follows the selected version's XSD family where a version-exact XSD exists.
PDF evidence is documentation evidence and is used for version mapping and provider-facing notes.
No schema is reconstructed or corrected in this pass.
```

Mixed-version rule:

```text
Do not validate older CIS payloads against CIS V2.3 by latest-wins substitution.
Use the exact service schema and dependency pool for the selected CIS version.
```

## 1. Corrected historical XSD map

| CIS / publication version | Official tag evidence | XSD file | Current integration status | Classification |
|---|---|---|---|---|
| V1.0 / V1.1 mapping question | `VDV-301-1.0` | `IBIS-IP_CustomerInformationService_V1.0.xsd` | imported | Historical XSD exists; V1.1 PDF-to-V1.0-XSD mapping still needs evidence. |
| V2.0 | `VDV-301-2.0`; also still present in `VDV-301-2.1` | `IBIS-IP_CustomerInformationService_V2.0.xsd` | imported | Historical executable CIS V2.0 baseline exists. |
| V2.2 | `VDV-301-2.2` | `IBIS-IP_CustomerInformationService_V2.2.xsd` | imported | Historical executable CIS V2.2 baseline exists. |
| V2.3 | `VDV-301-2.3` / current master | `IBIS-IP_CustomerInformationService_V2.3.xsd` | already present | Current executable CIS baseline. |
| V2.4 | no public CIS V2.4 PDF observed in this pass | `IBIS-IP_CustomerInformationService_V2.4.xsd` only in integration branch | already present as candidate/integration | Do not label official without source authority. |

## 2. Imported files

Imported into `dev/schema-integration` from official VDV tags, preserving blob contents and filenames:

```text
IBIS-IP_CustomerInformationService_V1.0.xsd  <- VDVde/VDV301 tag VDV-301-1.0
IBIS-IP_CustomerInformationService_V2.0.xsd  <- VDVde/VDV301 tag VDV-301-2.0
IBIS-IP_CustomerInformationService_V2.2.xsd  <- VDVde/VDV301 tag VDV-301-2.2
```

## 3. Dependency pools now available for CIS

```text
CIS V1.0:
  IBIS-IP_CustomerInformationService_V1.0.xsd
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_Enumerations_V1.0.xsd

CIS V2.0:
  IBIS-IP_CustomerInformationService_V2.0.xsd
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd

CIS V2.2:
  IBIS-IP_CustomerInformationService_V2.2.xsd
  IBIS-IP_common_V2.2.xsd
  IBIS-IP_Enumerations_V2.2.xsd

CIS V2.3:
  IBIS-IP_CustomerInformationService_V2.3.xsd
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd

CIS V2.4 integration/candidate:
  IBIS-IP_CustomerInformationService_V2.4.xsd
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

## 4. Remaining V1.1 mapping question

The public VDV page lists `CustomerInformationService V1.1`, while the official tag check found a service schema named `IBIS-IP_CustomerInformationService_V1.0.xsd` in tag `VDV-301-1.0`.

Current classification:

```text
Do not assume automatically that the V1.1 PDF is validated by the V1.0 XSD.
Treat this as a mapping/provenance question for the next CIS block.
```

Possible outcomes after checking the V1.1 PDF/release context:

```text
1. V1.1 PDF is a documentation update and still uses CIS V1.0 XSD.
2. A separate CIS V1.1 XSD exists outside the checked tag path.
3. V1.1 has no separate XSD and must be labelled as PDF-publication with V1.0-schema dependency if source evidence supports that.
```

## 5. Finding decision

Status after correction:

```text
No CIS-specific PDF/XSD finding opened.
No XSD correction proposed.
The previous "XSD not found" classification for V2.0 and V2.2 is superseded.
The previous "older CIS XSD recovery required" classification is narrowed to the V1.1 mapping question only.
```

## 6. Tool/SDK implication

For later SDK/tool validation:

```text
CIS V2.0 and V2.2 can be executable validation targets after local schema compile.
CIS V2.3 uses the known mixed Common V2.3 + Enumerations V2.2 dependency pool.
CIS V1.1 must remain a selectable documentation version only after its exact schema mapping is resolved.
```

## 7. Next CIS audit step

Next detailed file:

```text
docs/pdf_xsd_semantic_audit/05b_cis_v1_0_v2_0_v2_2_v2_3_xsd_history_compare.md
```

Required next steps:

```text
1. Compare CIS V1.0 -> V2.0 -> V2.2 -> V2.3 XSD operation sets and structure changes.
2. Check V1.1 PDF mapping against CIS V1.0 XSD.
3. Then compare CIS V2.3 PDF/XSD in detail as the current official service baseline.
4. Keep inherited Common/Enums findings separate from CIS-specific findings.
```

## 8. Result

```text
Historical CIS XSD provenance is corrected.
CIS V1.0, V2.0 and V2.2 XSDs are now present in dev/schema-integration from official VDV tags.
The remaining early-version uncertainty is the V1.1 PDF-to-XSD mapping, not the existence of all older CIS schemas.
```
