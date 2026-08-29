# Deep Read - TicketValidationService V2.1

Document ID: `TVS_V2.1`

Status: `needs_visual_review`

Date: 2026-08-29

## Source authority

Official VDV writing:

```text
https://www.vdv.de/301-2-16-sds-v2-1-ticketvalidation.pdfx
```

Pinned source:

```text
source_id: TVS_V2.1
sha256: 676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d
size: 752652 bytes
pin run: 33248946083
pinned_at_utc: 2026-08-29T10:56:16Z
```

The PDF is official documentation evidence. It does not replace the selected XSD family as executable XML-validation authority.

## Exact XSD authority

Official upstream tag:

```text
VDV-301-2.1
```

Exact service/dependency family:

```text
IBIS-IP_TicketValidationService_V2.1.xsd
  blob f6497e6469b82ee19b185c4de749d13a7ca60bed

IBIS-IP_common_V1.0.xsd
  blob 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c

IBIS-IP_Enumerations_V1.0.xsd
  blob a9bea5bc73003ed91ded8519db06c32c4067831d
```

The copies on `dev/schema-integration` match the official tag for these three files.

Important authority rule:

```text
TVS V2.1 -> Common V1.0 -> Enumerations V1.0
```

This mixed-version family is the official V2.1 route. Later Common/Enumerations files must not be substituted.

## Fresh-read method

The historical TicketValidationService findings were intentionally not reopened until after:

1. the official V2.1 PDF was byte-pinned,
2. exact V2.1 XSD/dependency authority was independently established,
3. the document was read afresh,
4. material pages were visibly checked from the exact pinned bytes,
5. counter-hypotheses were tested,
6. XML-material claims were executable-checked where practical.

Only then were historical TVS findings reopened for reconciliation.

## Visual evidence

The interactive PDF screenshot path returned cache-miss on material pages. The repository fallback rendered exact pinned bytes.

```text
render run: 33249247106
render job: 99091940668
requested/rendered pages: 10-17
dpi: 180
artifact: tvs-v21-rendered-pages
artifact id: 9713821340
result: PASS
```

Rendered-page hashes:

```text
10  129026321376391e08d4486ff099a7647af03210141a231647ad3cf8dace8649
11  3be24e44e9f62449804386324b505235bad31a46f9b011663c1605132a562322
12  ae25ab3b31a8a2ec83bbcde2a1488aebd301dde52b1ea95c4e22b359a8b1828e
13  a166df0b925ece93675d132703278437c1aec1bee63df59dbf999f701ad26cd2
14  f9f3d380bc128beb52762f553c2ceb9d88b6b3238c264e31588b94b2c9e63ee4
15  769e8ec6a52ae7fb5a276c5219e3d741d1e2172557944bfb5e40b6f6bc15755b
16  b893e78ec7c6f73af40cc46ff0a4bd807c47a21df6b8ffec5d1dd6f9d621ec2b
17  970e20a56b24584ce4a1626733bb4a43553a2cc9370c18f99fa9150c3e04bab5
```

The visual review is targeted, not exhaustive. Therefore the document remains `needs_visual_review`.

## Existing finding revalidated under the current Evidence Gate

### TVS-002 - `VehicleData.RouteDeviation` PDF type vs XSD type

Visible V2.1 PDF table on page 16:

```text
RouteDeviation
0:1
RouteDirectionEnumeration
```

The row describes route deviation and points to the Common enumeration chapter.

Exact V2.1 XSD:

```xml
<xs:element
    name="RouteDeviation"
    type="RouteDeviationEnumeration"
    minOccurs="0"/>
```

EV-112 verifies the exact selected schema family before exercising behavior:

```text
RouteDeviation exact type = RouteDeviationEnumeration
RouteDeviationEnumeration exists
RouteDirectionEnumeration does not exist in exact Enumerations V1.0
values = onroute / offroute / unknown

onroute                 -> valid
offroute                -> valid
unknown                 -> valid
NOT_A_ROUTE_DEVIATION   -> invalid
```

The active disproof attempt also checked whether the PDF wording could simply be an equivalent/alternate enumeration label. It is not: later Common documentation distinguishes `RouteDeviationEnumeration` from `RouteDirectionEnumeration`, and the exact V2.1 executable dependency does not provide `RouteDirectionEnumeration`.

State:

```text
executable_confirmed_EV-112
```

Classification:

```text
pdf_xsd_type_mismatch
```

Executable consequence:

```text
Validation follows RouteDeviationEnumeration in the exact selected V2.1 XSD family.
Do not silently accept or substitute RouteDirectionEnumeration because the PDF prints that name.
```

## New findings from the independent V2.1 Fresh Read

### DRTVS21-001 - `CurrentTripRef` type identifier case

Visible page 14 prints:

```text
IBIS-IP.NMToken
```

Exact XSD uses:

```text
IBIS-IP.NMTOKEN
```

EV-112 confirms:

```text
IBIS-IP.NMTOKEN exists.
IBIS-IP.NMToken does not exist.
A probe schema using type="IBIS-IP.NMToken" fails to compile.
```

The counter-hypothesis that this is an executable alias/case-insensitive identifier is rejected.

State: `executable_confirmed`.

Classification: `pdf_xsd_type_identifier_case_mismatch`.

Validation impact: none beyond normal exact-XSD behavior; no normalization alias is permitted.

### DRTVS21-002 - `CurrentLineData` response display missing service-name separator

Visible page 15 prints the GetCurrentLine response type as:

```text
TicketValidationServiceCurrentLineData
```

The exact XSD response type is:

```text
TicketValidationService.CurrentLineDataStructure
```

The surrounding PDF conventions intentionally omit the `Structure` suffix in several displayed type labels. Therefore omission of `Structure` is not itself classified as an error here.

The material anomaly is the missing separator dot after `TicketValidationService`. This is reinforced by the immediately following table, which prints the displayed name with a dot:

```text
TicketValidationService. CurrentLineData
```

EV-112 confirms the exact XSD type and confirms that the missing-dot concatenated string is not an exact service complex type.

State: `context_verified`.

Classification: `pdf_type_display_identifier_typo_candidate`.

Subtype: `missing_service_name_separator_dot`.

Evidence boundary: this is a PDF display/documentation finding, not proof that every shortened PDF type display is an invalid XML QName.

### DRTVS21-003 - `SubscribeCurrentStop` vs `SubscribeCurrentStopPoint`

Visible German flow text on page 11 and English flow text on page 13 use:

```text
SubscribeCurrentStop
```

Formal operation overviews on pages 10 and 12 and the detailed operation section on page 14 use:

```text
SubscribeCurrentStopPoint
```

The exact XSD operation group also uses `SubscribeCurrentStopPoint`.

The counter-hypothesis that `SubscribeCurrentStop` is a second/legacy formal operation name is rejected by the same V2.1 document's operation overview and detailed section plus the exact XSD.

State: `context_verified`.

Classification: `pdf_operation_name_editorial_error_candidate`.

Executable impact: none; no operation alias is created.

### DRTVS21-004 - minor PDF editorial spelling residue

Targeted visible review also found non-executable editorial residue:

```text
page 10: Unscubscribe (two operation-description texts)
page 15: Description of GetrazziaResponsetData
page 15: Description of Error Respone
```

These strings occur in prose/table captions, not executable identifiers.

State: `context_verified`.

Classification: `pdf_documentation_typo_non_executable`.

Executable impact: none.

## Historical-finding reconciliation boundary

After the independent V2.1 Fresh Read, the historical TicketValidationService register was reopened.

Result for V2.1:

```text
TVS-002 survives and is revalidated under the current Evidence Gate with EV-112.
TVS-001 is a V2.4 XSD internal-operation-inventory candidate and is not revalidated by this V2.1 block.
TVS-003 concerns V2.2+ CurrentTariffStop-era PDF labels and is not revalidated by this V2.1 block.
```

The new DRTVS21 findings are not aliases for TVS-001/003 and are recorded separately.

## Positive alignment checks

The targeted V2.1 review also confirmed useful non-findings:

- formal operation names consistently use `SubscribeCurrentStopPoint` / `UnsubscribeCurrentStopPoint`;
- the exact GetCurrentLine response is typed to `TicketValidationService.CurrentLineDataStructure`;
- `VehicleData.RouteDeviation` and `VehicleData.CurrentTripRef` are optional as reflected by the exact XSD;
- the V2.1 service file explicitly includes Common V1.0 and Enumerations V1.0;
- the mixed-version dependency route is therefore expected authority, not a defect.

## EV-112 provenance

```text
evidence: EV-112
checker: tools/validate_tvs_v21_ev112.py
run: 33249561880
job: 99092772643
tested temporary head: 5edc3f1d167e93dffcc3978f6e903ee0fba3f960
result: PASS
```

The temporary push-trigger workflow was removed after the run. The reusable checker remains. No XSD changed.

## Completion state

```text
textual fresh read: complete
targeted visible review: pages 10-17 complete
exhaustive visual review: no
Deep Read state: needs_visual_review
```

This block does not authorize remediation, schema changes or official-facing action.

Next natural Deep Read target:

```text
TVS_V2.2
```
