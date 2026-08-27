# VideoDisplayService V1.0 / V2.0 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation and targeted XML validation remain pending.

## 1. Exact routing

| Document | Strict executable schema | Pool | Authority |
|---|---|---|---|
| V1.0 | none confirmed | unresolved | public document only for semantics |
| V2.0 | `IBIS-IP_VideoDisplayService_V2.0.xsd` blob `fcfdadd3...` | Common V2.0 + Enums V2.0 | official release |

No latest-wins substitution is allowed.

## 2. VDS-002 - ListViewCapabilitiesResponse compositor

Both public V1.0 and V2.0 tables describe one `ListViewCapabilitiesResponse` structure containing:

```text
ViewID       1:1
ViewName     1:1
ViewType     1:1 (table extraction renders the marker imperfectly, but it is presented as the third field of the same structure)
```

Official V2.0 XSD:

```text
<xs:complexType name="VideoDisplayService.ListViewCapabilitiesResponseStructure">
  <xs:choice>
    <xs:element name="ViewID" .../>
    <xs:element name="ViewName" .../>
    <xs:element name="ViewType" .../>
  </xs:choice>
</xs:complexType>
```

Executable consequence:

```text
A payload carrying ViewID + ViewName + ViewType as one capability record is rejected by the selected XSD.
```

Classification:

```text
xsd_structure_modelling_error_candidate
confidence: high
```

## 3. VDS-003 - SetVideoViewRequest compositor

V1.0 and V2.0 PDFs both state:

```text
ViewID   1:1
Timeout  1:1
```

Official V2.0 XSD instead uses:

```text
choice(ViewID, Timeout)
```

Therefore a request containing both required PDF fields is rejected by the XSD.

Classification:

```text
xsd_structure_modelling_error_candidate
confidence: high
```

## 4. VDS-004 - response compositor family

### SetVideoViewResponse

PDF V1.0/V2.0 structure:

```text
State
CurrentViewID 1:1
OperationErrorMessage 0:1
```

XSD:

```text
choice(State, CurrentViewID, OperationErrorMessage)
```

### GetDisplayStateResponse

PDF V1.0/V2.0 structure:

```text
State
CurrentViewID 1:1
OperationErrorMessage 0:1
```

XSD:

```text
choice(State, CurrentViewID, OperationErrorMessage)
```

### SetNextViewIndexResponse

PDF V1.0/V2.0 structure:

```text
State
OperationErrorMessage 0:1
```

XSD:

```text
choice(State, OperationErrorMessage)
```

The repeated pattern and unchanged PDF semantics across V1.0/V2.0 make this a service-level compositor family candidate rather than three unrelated table typos.

Classification:

```text
xsd_structure_modelling_error_candidate
confidence: high
```

Strict validation behavior remains exactly the XSD choice semantics until an official correction exists.

## 5. Upstream history

The V2.0 service file was introduced in the official V2.0 release and current upstream master still contains the identical blob `fcfdadd3b62a584370cae326004050b4dc832e23`.

No upstream PR matching `VideoDisplayService` was found during this first-pass check.

Therefore there is no observed official/candidate correction analogous to VideoRecordingService PR #27.

## 6. VDS-005 - V1.0 broken document cross-reference

V1.0 includes literal unresolved document-generation text:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

It occurs in service lifecycle/subscription references.

Classification:

```text
pdf_table_or_documentation_error_candidate
confidence: high
validation impact: none
```

## 7. Technical validation backlog

```text
VDS-VB-001 compile official V2.0 + Common V2.0 + Enums V2.0.
VDS-VB-002 positive XSD sample containing only ViewID in ListViewCapabilitiesResponse.
VDS-VB-003 negative PDF-shaped sample containing ViewID + ViewName + ViewType.
VDS-VB-004 negative SetVideoViewRequest with ViewID + Timeout.
VDS-VB-005 negative SetVideoViewResponse with State + CurrentViewID.
VDS-VB-006 negative GetDisplayStateResponse with State + CurrentViewID.
VDS-VB-007 negative SetNextViewIndexResponse with State + OperationErrorMessage.
VDS-VB-008 codegen/operation inventory check.
```

No compile/sample result is claimed here.
