# VideoDisplayService V1.0 / V2.0 historical audit start

Status: provenance and PDF/XSD semantic first pass completed. Local XSD compilation/sample validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
3fb6b083e3b0a012dd99ecc3738ee18ed7b5bbd2
```

Scope:

```text
VDV 301-2-13 VideoDisplayService V1.0 (05/2017)
VDV 301-2-13 VideoDisplayService V2.0 (08/2019)
VDVde/VDV301 official release tags
IBIS-IP_VideoDisplayService_V2.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

## 1. V1.0 public document / XSD provenance

The public V1.0 document is an explicit VDV301 V1.0 video-service proposal and defines the VideoDisplayService operation family.

No `IBIS-IP_VideoDisplayService_V1.0.xsd` was found in the checked official VDVde/VDV301 release tags or repository source history.

Therefore:

```text
V1.0 public document known
strict V1.0 XSD routing unresolved
no historical backfill available under current source policy
no substitution with V2.0
```

This becomes VDS-001.

## 2. V2.0 official schema family

Official source:

```text
Repository: VDVde/VDV301
Tag: VDV-301-2.0
File: IBIS-IP_VideoDisplayService_V2.0.xsd
Blob: fcfdadd3b62a584370cae326004050b4dc832e23
```

The branch file has the same blob SHA. Current official upstream master also still has the same blob.

Exact dependency pool selected by the service XSD:

```text
VideoDisplayService V2.0
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

The V2.0 PDF states that the service is compatible with VDV301 V1.0 and 2.x. This does not create an executable V1.0-XSD mapping; the SDK must keep document compatibility and strict XSD provenance separate.

## 3. Operation continuity

V1.0 and V2.0 describe the same core operation family:

```text
ListViewCapabilities
SetVideoView
SetNextViewIndex
GetDisplayState
SubscribeDisplayState
UnsubscribeDisplayState
```

Subscribe/Unsubscribe explicitly use generic VDV301-2 subscription structures and are not treated as missing service-local XSD operations.

## 4. Compositor findings preview

The official V2.0 XSD uses `xs:choice` in several structures for fields the V1.0 and V2.0 PDFs describe together in one structure.

Candidate groups:

```text
VDS-002 ListViewCapabilitiesResponseStructure
  PDF: ViewID + ViewName + ViewType
  XSD: choice(ViewID, ViewName, ViewType)

VDS-003 SetVideoViewRequestStructure
  PDF: ViewID 1:1 + Timeout 1:1
  XSD: choice(ViewID, Timeout)

VDS-004 response compositor family
  SetVideoViewResponse PDF: State + CurrentViewID + optional OperationErrorMessage
  GetDisplayStateResponse PDF: State + CurrentViewID + optional OperationErrorMessage
  SetNextViewIndexResponse PDF: State + optional OperationErrorMessage
  XSD: choice among those sibling fields
```

These are strong `xsd_structure_modelling_error_candidate` findings. Validation still follows the selected XSD until an official correction exists.

## 5. V1.0 broken cross-reference

The V1.0 PDF contains literal unresolved Word cross-reference text such as:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

This is VDS-005 (`pdf_table_or_documentation_error_candidate`) and has no executable XML effect.

## 6. Next file

```text
docs/pdf_xsd_semantic_audit/18a_video_display_service_v1_0_v2_0_pdf_xsd_first_pass.md
```
