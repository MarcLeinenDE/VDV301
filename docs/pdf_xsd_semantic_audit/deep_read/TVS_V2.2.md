# Deep Read - TicketValidationService V2.2

Document ID: `TVS_V2.2`

Status: `needs_visual_review`

Date: 2026-08-29

## Source authority

Official VDV writing:

```text
https://www.vdv.de/301-2-16-sdes-v2-2-ticketvalidation.pdfx
```

Pinned source:

```text
source_id: TVS_V2.2
sha256: 1915a1b12c24386e9a8ab5638fd88af6a442b5e42586b7b2d48f03e9a4205083
size: 785931 bytes
pin run: 33255245725
pinned_at_utc: 2026-08-29T13:31:54Z
```

The PDF is official documentation evidence. It does not replace the selected XSD family as executable XML-validation authority.

## Exact XSD authority

Official upstream tag:

```text
VDV-301-2.2
```

Exact service/dependency family:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
  blob 5a4be2b2ba66860f035777ec0458dba0790880e1

IBIS-IP_common_V2.2.xsd
  blob 468fee6d177e7185dbcd5d3f90cfb114e29e01ae

IBIS-IP_Enumerations_V2.2.xsd
  blob 2a23b512379b18e8f122ac1272cef8229fb86283
```

The copies on `dev/schema-integration` match the official `VDV-301-2.2` tag exactly for these three files.

Authority route:

```text
TVS V2.2 -> Common V2.2 -> Enumerations V2.2
```

This is a version-aligned official family. Later dependencies must not be substituted.

## Fresh-read method

The historical TicketValidationService V2.2 findings and the prior V2.1 correction history were intentionally not reopened until after:

1. the official V2.2 PDF was byte-pinned independently,
2. exact V2.2 XSD/dependency authority was independently established,
3. the V2.2 document was read afresh,
4. material pages were visibly checked from the exact pinned bytes,
5. the Fresh Read observations were frozen in `deep_read_registry_delta_tvs_v22_2026-08-29.json`,
6. only then were historical TicketValidation findings reopened,
7. XML-material claims were executable-checked with EV-113.

This preserves the Evidence-Gate separation between fresh observation and historical expectation.

## Visual evidence

The interactive PDF screenshot path returned cache-miss on material pages. The repository fallback rendered exact pinned bytes.

```text
render run: 33255450850
render job: 99108219131
requested/rendered pages: 10-18
dpi: 180
artifact: tvs-v22-rendered-pages
artifact id: 9715657871
artifact digest: sha256:f6c313f94fe89ad14f6ed6114a0402efc543c31d4d2353a60dde05ea7f7d6e93
result: PASS
```

Rendered-page hashes:

```text
10  3bd17dd87b8f5a9551a75c6354ccedd5e9d4fb6ea3b1775772c73c065ad3ee06
11  13d455d6428cd7bbdf3c09456287694617770338a33690e6ed518313e3aa32fd
12  c2d2d2da3a3182da5f798853c925f7be35fbc81f28dc2ffdca9d4e292aaf7c48
13  2d92ac98c0c7136bcaab0a21d33f5f62d71be06e12737a6d2ccf38294a3d0740
14  666e5bc5e52c4f9252f6c0419d769c14cf5e982a914fec7efb75f9c75916a688
15  349285137e542cc00d6cbcc2981647f87d33c62c7271342e2f6e05a328d9b2a6
16  beab96e776b29311d3d68e0f6ff1eaf233a126c2427e51dc385c2fd10a40202b
17  4aaa739da2b94e023831a7d3787e5b91488ed9403913b29e765c7d335e208705
18  5c162bdcbcf2d1a01fac1d661044f4f091c156c9fbfbcf98e94183e4a729f37e
```

The visual review is targeted, not exhaustive. Therefore the document remains `needs_visual_review`.

## Existing findings revalidated under the current Evidence Gate

### TVS-002 - `VehicleData.RouteDeviation` PDF type vs XSD type

Visible V2.2 PDF page 16 prints:

```text
RouteDeviation
0:1
RouteDirectionEnumeration
```

Exact V2.2 XSD declares:

```xml
<xs:element name="RouteDeviation" type="RouteDeviationEnumeration" minOccurs="0"/>
```

Unlike the V2.1 dependency family, exact Enumerations V2.2 contains both names. This makes a V2.2-specific executable disproof essential rather than inheriting EV-112.

EV-113 confirms:

```text
RouteDeviationEnumeration values:
  onroute / offroute / unknown

RouteDirectionEnumeration values:
  Forward / Backward / Clockwise / Counterclockwise / Other

RouteDeviation type = RouteDeviationEnumeration
onroute  as RouteDeviation -> valid
Forward  as RouteDeviation -> invalid
Forward  as RouteDirection -> valid
onroute  as RouteDirection -> invalid
```

The active counter-hypothesis that the PDF could merely be naming an equivalent enum is therefore rejected: the two exact V2.2 types have different value sets and different semantics.

State:

```text
executable_confirmed_EV-113
```

Executable consequence:

```text
Validation of VehicleData.RouteDeviation follows RouteDeviationEnumeration.
Do not silently substitute RouteDirectionEnumeration because the PDF prints that name.
```

### TVS-003 - stale `CurrentStopPoint` names after `CurrentTariffStop` rename

V2.2 version history page 18 explicitly records the technical correction:

```text
CurrentStopPoint ... is renamed to CurrentTariffStop
```

The same V2.2 document nevertheless retains stale names in several places:

```text
page 10 German operation overview:
  GetCurrentStopPoint
  SubscribeCurrentStopPoint
  UnsubscribeCurrentStopPoint

page 12 English operation overview:
  GetCurrentStopPoint
  SubscribeCurrentStopPoint
  UnsubscribeCurrentStopPoint

page 14 chapter heading:
  GetCurrentTariffStop

page 14 stale response/data labels:
  TicketValidationService.GetCurrentStopPointResponse
  TicketValidationService.CurrentStopPointData
```

Page 14 simultaneously uses `CurrentTariffStopData` and `CurrentTariffStop` inside the table, and detailed sections 3.2/3.3 use `SubscribeCurrentTariffStop` / `UnsubscribeCurrentTariffStop`.

Exact V2.2 XSD uses only the renamed executable service identifiers:

```text
TicketValidationService.GetCurrentTariffStopResponse
TicketValidationService.GetCurrentTariffStopResponseStructure
TicketValidationService.CurrentTariffStopDataStructure
CurrentTariffStopData
CurrentTariffStop
```

EV-113 confirms the rename boundary:

```text
GetCurrentTariffStopResponse global root exists
GetCurrentStopPointResponse global root does not exist
CurrentTariffStopDataStructure exists
CurrentStopPointDataStructure does not exist

new GetCurrentTariffStopResponse sample -> valid
stale GetCurrentStopPointResponse sample -> invalid
```

The active alias hypothesis is rejected. The stale PDF names are documentation residue and must not be accepted as schema aliases.

State:

```text
executable_confirmed_EV-113
```

Classification remains a PDF documentation/label error candidate, with the V2.2 scope refined to include both operation overviews and response/data table labels.

## Existing Deep-Read findings whose scope extends into V2.2

No duplicate finding IDs are created for repeated observations. Instead, the independently observed V2.2 instances extend the scope of the existing Deep-Read findings.

### DRTVS21-001 - `CurrentTripRef` type identifier case

Visible V2.2 page 14 prints:

```text
IBIS-IP.NMToken
```

Exact V2.2 XSD/Common use:

```text
IBIS-IP.NMTOKEN
```

EV-113 confirms that `IBIS-IP.NMTOKEN` exists, `IBIS-IP.NMToken` does not, and a probe using the PDF spelling fails schema compilation.

State for V2.2: `executable_confirmed_EV-113`.

Version scope is extended from V2.1 to V2.1-V2.2.

### DRTVS21-002 - `CurrentLineData` response display missing service-name separator

Visible V2.2 page 15 again prints:

```text
TicketValidationServiceCurrentLineData
```

The immediately following data table prints a dotted display form, while exact XSD uses:

```text
TicketValidationService.CurrentLineDataStructure
```

EV-113 confirms the exact XSD type and that the concatenated missing-dot string is not an exact service complex type.

The same boundary as V2.1 remains: shortened PDF display conventions may omit `Structure`; that omission is not classified here. The finding remains limited to the missing separator dot.

State for V2.2: `context_verified` with EV-113 XSD-side support.

Version scope is extended from V2.1 to V2.1-V2.2.

### DRTVS21-003 - truncated `SubscribeCurrentStop` flow name

Visible V2.2 German page 11 and English page 13 still use:

```text
SubscribeCurrentStop
```

In V2.2 the detailed operation section is now:

```text
SubscribeCurrentTariffStop
```

The V2.2 version history explicitly establishes the CurrentStopPoint -> CurrentTariffStop rename. The counter-hypothesis that `SubscribeCurrentStop` is a second formal V2.2 operation name is rejected by the detailed section and the documented rename.

State for V2.2: `context_verified`.

Version scope is extended from V2.1 to V2.1-V2.2. The expected formal name differs by version: `SubscribeCurrentStopPoint` in V2.1, `SubscribeCurrentTariffStop` in V2.2.

### DRTVS21-004

The V2.1 minor editorial-residue finding is not automatically extended. V2.2 has minor prose/caption residue, but no separate V2.2 scope extension is required for SDK or validation behavior in this block.

## Historical reconciliation result

After the independent V2.2 Fresh Read, the historical TicketValidation register was reopened.

Result:

```text
TVS-002 survives for V2.2 and is executable-confirmed by EV-113.
TVS-003 survives for V2.2, is scope-refined, and its executable rename boundary is confirmed by EV-113.
DRTVS21-001 independently recurs in V2.2; scope extended without duplicate ID.
DRTVS21-002 independently recurs in V2.2; scope extended without duplicate ID.
DRTVS21-003 independently recurs in V2.2; scope extended without duplicate ID.
TVS-001 remains V2.4-only and is not revalidated here.
```

No new V2.2-only finding ID is needed after deduplication.

## Positive alignment checks

The V2.2 review also confirms:

- chapter 3.1 itself uses `GetCurrentTariffStop`;
- sections 3.2 and 3.3 use `SubscribeCurrentTariffStop` and `UnsubscribeCurrentTariffStop`;
- the exact V2.2 service family is version-aligned to Common V2.2 and Enumerations V2.2;
- `CurrentTripRef` is optional in the exact XSD;
- `RouteDeviation` is optional in the exact XSD;
- the PDF itself states that, on mismatch, the corresponding XSD is the master for implementation.

## EV-113 provenance

```text
evidence: EV-113
checker: tools/validate_tvs_v22_ev113.py
run: 33257767942
job: 99114368558
tested temporary head: 28851cfdcf10e5569e512e235ce58ab02adb5167
result: PASS
```

The temporary push-trigger workflow was removed immediately after the run in commit:

```text
02512d99a3cfc4f29950e68788ce9233b45ff1f4
```

The reusable checker remains. No XSD changed.

## Completion state

```text
textual fresh read: complete
targeted visible review: pages 10-18 complete
historical reconciliation: complete
executable evidence: EV-113 PASS
exhaustive visual review: no
Deep Read state: needs_visual_review
```

This block does not authorize remediation, schema changes or official-facing action.

Next natural Deep Read target:

```text
TVS_V2.3
```
