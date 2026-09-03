# CustomerInformationService V1.1 PDF-to-XSD mapping

Status: first-pass mapping analysis completed; no version-exact CIS V1.1 XSD confirmed.

Scope:

```text
VDV 301-2-3 CustomerInformationService V1.1 public PDF
IBIS-IP_CustomerInformationService_V1.0.xsd
IBIS-IP_CustomerInformationService_V2.0.xsd
Official VDVde/VDV301 release-tag evidence observed in the audit
```

Authority rule:

```text
Where a version-exact XSD exists, validation follows that XSD family.
Where no version-exact XSD is confirmed, do not claim XSD validation for that public PDF version.
Do not infer, rename or reconstruct a missing XSD only from a PDF.
```

Mixed-version rule:

```text
CIS V1.1 must not be silently validated as CIS V1.0 or CIS V2.0.
Any compatibility selection must be explicit and labelled as such.
```

## 1. Public PDF fact

Observed public source:

```text
VDV 301-2-3 IBIS-IP Beschreibung der Dienste - Dienst CustomerInformationService V1.1
PDF URL observed from official VDV IP-KOM-OEV publication page:
https://www.vdv.de/301-2-3-sds-v1-1.pdfx?forced=false
```

First-pass PDF observations:

```text
Document: VDV-Schrift 301-2-3
Date on PDF: 12/2016
Subject: IBIS-IP Beschreibung der Dienste - Dienst CustomerInformationService
```

The V1.1 PDF states that the service document was separated from VDV-301-2 so that individual IBIS-IP services can be adapted independently; it describes CustomerInformationService and its specific data structures.

Important implication:

```text
CIS V1.1 is a real public PDF version and remains a separate audit target.
```

## 2. Official GitHub tag/XSD fact

Observed official VDVde/VDV301 release-tag state in this audit:

```text
VDV-301-1.0 tag contains:
  IBIS-IP_CustomerInformationService_V1.0.xsd

VDV-301-2.0 tag contains:
  IBIS-IP_CustomerInformationService_V2.0.xsd

VDV-301-2.2 tag contains:
  IBIS-IP_CustomerInformationService_V2.2.xsd
```

No version-exact file named `IBIS-IP_CustomerInformationService_V1.1.xsd` has been confirmed in the checked source set.

Important implication:

```text
The V1.1 PDF cannot currently be paired with a version-exact CIS V1.1 XSD.
```

## 3. Why CIS V1.1 must not be mapped to CIS V1.0 automatically

The official VDV-301-1.0 tag provides `IBIS-IP_CustomerInformationService_V1.0.xsd`, and this XSD is useful for strict CIS V1.0 validation.

However, the CIS V1.1 PDF is not simply proven to be the same as CIS V1.0 XSD.

Key PDF-side observations from the V1.1 PDF:

```text
The V1.1 PDF operation overview lists the Get/Subscribe/Unsubscribe operation family and their request/response structures.
The V1.1 PDF AllData table contains SpeakerActive and StopInformationActive in VehicleInformationGroup.
```

Key XSD-side observations:

```text
CIS V1.0 XSD does not define the V2.x-style CustomerInformationServiceOperations group.
CIS V1.0 XSD does not define top-level CustomerInformationService.* operation elements in the V2.x style.
CIS V1.0 XSD VehicleInformationGroup does not contain SpeakerActive or StopInformationActive.
```

Therefore:

```text
Strict CIS V1.1 -> CIS V1.0 mapping is not supported by the first-pass evidence.
A validator must not say that CIS V1.1 is fully XSD-validated by CIS V1.0.
```

## 4. Why CIS V1.1 must not be mapped to CIS V2.0 automatically

CIS V2.0 XSD contains some structures that match visible V1.1 PDF features better than CIS V1.0 does, especially:

```text
CustomerInformationServiceOperations group.
Top-level CustomerInformationService.* operation elements.
SpeakerActive.
StopInformationActive.
CurrentConnection 0:*.
CurrentDisplayContent 1:*.
```

But CIS V2.0 is a later official schema family with its own public V2.0 PDF and V2.0 dependency pool.

Therefore:

```text
CIS V2.0 may be useful as a comparison target for V1.1, but it is not a proven official CIS V1.1 XSD mapping.
A validator must not silently validate CIS V1.1 payloads against CIS V2.0 and call that strict V1.1 validation.
```

## 5. First-pass classification

| Item | Classification | Reason |
|---|---|---|
| CIS V1.1 PDF | public VDV PDF version | Listed on official VDV page and opened as VDV 301-2-3, 12/2016. |
| CIS V1.1 XSD | not confirmed | No `IBIS-IP_CustomerInformationService_V1.1.xsd` found in checked official tag/current source set. |
| CIS V1.0 XSD | official historical release schema | Valid source for strict CIS V1.0, not automatically V1.1. |
| CIS V2.0 XSD | official historical release schema | Valid source for strict CIS V2.0, not automatically V1.1. |
| CIS V1.1 mapping | unresolved | PDF contents appear newer than CIS V1.0 in at least some visible features, but no version-exact V1.1 XSD is confirmed. |

## 6. Tool/SDK behaviour recommendation

Strict validation mode:

```text
CIS V1.0 selected -> validate with CIS V1.0 + Common V1.0 + Enumerations V1.0.
CIS V1.1 selected -> report: public PDF known, but no version-exact CIS V1.1 XSD confirmed in audited source set.
CIS V2.0 selected -> validate with CIS V2.0 + Common V2.0 + Enumerations V2.0.
```

Provider-facing wording later:

```text
CustomerInformationService V1.1 is a public VDV PDF version, but this audit has not confirmed a version-exact CIS V1.1 XSD. Strict XSD validation for CIS V1.1 cannot be claimed. Select CIS V1.0 or CIS V2.0 only if the system/provider explicitly states that one of those schema families is used.
```

Optional later compatibility profile, only if explicitly approved:

```text
A labelled CIS V1.1 compatibility profile could be designed later after detailed PDF table comparison.
It must not be presented as official VDV XSD validation unless a matching official V1.1 schema or source decision is found.
```

## 7. Finding decision

No schema correction is proposed.

A service-level provenance finding should be tracked in the audit register when the register is next consolidated:

```text
CIS-001 - CustomerInformationService V1.1 public PDF has no confirmed version-exact XSD mapping
State: unresolved provenance / validation-routing gap
```

This is not a request to invent or import a schema.

## 8. Next CIS audit step

Next detailed step:

```text
docs/pdf_xsd_semantic_audit/05d_cis_v2_0_pdf_xsd_first_pass.md
```

Recommended next work:

```text
1. Start with CIS V2.0 because it has both public PDF and official release-tag XSD.
2. Compare V2.0 PDF operation table and key data structures against CIS V2.0 XSD.
3. Then continue CIS V2.2 and V2.3.
4. Keep CIS V1.1 unresolved unless a source-exact mapping is found.
```
## Post-audit correction — 2026-09-03

The earlier V1.1 provenance statement is superseded by `AUDIT_CORRECTION_DELTA_CIS_V11_PROVENANCE_2026-09-03.md`. A historical untagged V1.1 working XSD family exists, but it is not a V1.1 release-tag authority and does not match all published V1.1 PDF fields. See also `FINDING_REVALIDATION_CIS_2026-09-03.md` / `EV-125`.
