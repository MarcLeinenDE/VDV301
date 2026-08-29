# Deep Read - TRAINSET_V2.2

Status: `needs_visual_review`

Document:

```text
VDV-Schrift 301-2-14
TrainSet services V2.2
08/2019
source_id: TRAINSET_V2.2
```

Source pin:

```text
sha256: c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e
size:   1744296 bytes
pin run: 33239594518
```

The text layer was fresh-read independently before the historical TrainSet findings and EV-104 conclusions were reopened. Material pages were then rendered from the exact byte-pinned PDF with the repository fallback; render run `33239787579` succeeded. The interactive PDF screenshot backend also returned `cache miss` for some pages, so the document remains `needs_visual_review` rather than `exhaustive_read`.

## Exact XSD authority

The three service XSDs in `dev/schema-integration` are byte-identical to the official upstream tag `VDV-301-2.2`:

```text
IBIS-IP_TrainSetInformationService_V2.2.xsd
  blob 7ab1f8f892bfcea2a8b8a055f07de92c143356f9

IBIS-IP_TrainSetManagementService_V2.2.xsd
  blob da9465d6683e3f7d54a546ab4a13739fb3c3e902

IBIS-IP_TrainSetDataService_V2.2.xsd
  blob 7a132894c281d613e16514a6fa1bcbffe713d066
```

Shared dependencies:

```text
IBIS-IP_common_V2.2.xsd        blob 468fee6d177e7185dbcd5d3f90cfb114e29e01ae
IBIS-IP_Enumerations_V2.2.xsd  blob 2a23b512379b18e8f122ac1272cef8229fb86283
```

There is no authority/provenance ambiguity for the checked V2.2 TrainSet service family.

## Version-history corrections confirmed

The V2.2 history explicitly records three technical corrections relevant to the audit:

1. `TrainSetInformationService.GetTrainSetCompositionResponseStructure` gains repeated `SingleCoachInATrainSet` modelling because V2.1 could not transmit multiple coaches.
2. `TrainSetManagementService.GetTrainSetCompositionResponse` replaces the V2.1 name without `Response`.
3. `TrainSetSubscribeRequestStructure` and `TrainSetUnsubscribeRequestStructure` are introduced for parameterised subscriptions to Retrieve data.

Visible page 24 confirms the repeated TSI V2.2 `SingleCoach` model. This closes the historical direction of TSI-001/TSM-001/TSD-001 without back-applying V2.2 behaviour to V2.1.

## Existing findings revalidated under the current Evidence Gate

### TSM-002 - stale operation-group member

Fresh PDF evidence:

- section 5.5.3.2 and the visible page 31 declaration use `TrainSetManagementService.GetTrainSetCompositionResponse`;
- the V2.2 version history explicitly says the old name was corrected to that form.

Exact XSD evidence:

```text
global root:
  TrainSetManagementService.GetTrainSetCompositionResponse

TrainSetManagementServiceOperations group:
  TrainSetManagementService.GetTrainSetComposition
```

EV-104 run `33111644388` already executable-confirmed that the corrected global root validates while the operation group still accepts the stale name and rejects the corrected name.

Counter-hypothesis checked: the group entry is not an intentional request name. The group element is typed with the response structure and occurs in the response-oriented operation inventory while the public V2.2 writing and version history explicitly identify the corrected response name.

Result:

```text
TSM-002
state: executable_confirmed
classification: xsd_structure_modelling_error_candidate
subtype: operation_group_name_mismatch
confidence: high
```

### TSD-002 - Unsubscribe overview table not updated

Visible pages 34/35 show the operation overview still listing:

```text
UnsubscribeTripRef Request
  -> TrainSetDataService.RetrieveTripRefRequestStructure

UnsubscribeTripInformation Request
  -> TrainSetDataService.RetrieveTripInformationRequestStructure
```

The immediately following section 6.5.2 defines the dedicated `TrainSetUnsubscribeRequestStructure`, and sections 6.5.5/6.5.8 say the Unsubscribe requests use that structure. The exact V2.2 XSD binds both Unsubscribe roots to `TrainSetUnsubscribeRequestStructure`.

EV-110 run `33241603270` proves the validation difference:

```text
correct specialised request including Client-IP-Address + CoachNumber -> valid
PDF-overview Retrieve-like request containing only CoachNumber          -> invalid
schema error: expected Client-IP-Address before CoachNumber
```

Counter-hypothesis checked: the overview rows cannot be read as only a semantic parameter hint, because the table column is explicitly `Data type used, data structure` and other rows name the exact request structures.

Result:

```text
TSD-002
state: executable_confirmed
classification: pdf_table_or_documentation_error_candidate
confidence: high
validation behaviour: exact V2.2 XSD requires TrainSetUnsubscribeRequestStructure
```

### TSD-003 - dual Subscribe response typing

Fresh V2.2 PDF context confirms the intended two phases:

```text
immediate Subscribe response -> SubscribeResponseStructure
later event-based update     -> Retrieve-style data response structure
```

General Conventions V2.2 section 4.1.3 independently defines the same model: `SubscribeResponseStructure` confirms the subscription and communicates Heartbeat; the service later sends the current data associated with the subscription.

Exact TSD V2.2 XSD:

```text
operation-group context:
  SubscribeTripRefResponse          -> SubscribeResponseStructure
  SubscribeTripInformationResponse  -> SubscribeResponseStructure

global data-event context:
  SubscribeTripRefResponse          -> RetrieveTripRefResponseStructure
  SubscribeTripInformationResponse  -> RetrieveTripInformationResponseStructure
```

EV-104 executable-confirmed both contexts.

Counter-hypothesis checked: the duplicate lexical names are not sufficient to establish an XSD collision because the VDV subscription model explicitly distinguishes immediate acknowledgement from later data delivery and the two schema contexts represent those roles.

Result:

```text
TSD-003
state: contextual_not_defect / executable_context_confirmed
classification: service_modelling_or_generic_response_context
SDK implication: response-context resolver required; lexical response name alone is insufficient
```

## New V2.2 findings

### TSM-003 - stale V2.1-style composition diagram on page 31

Visible pinned-byte page 31 uses the corrected global element name and says the TSI response structure is reused, but the embedded XSD diagram still expands the old flat coach fields directly:

```text
CoachType
CoachNumber
FrontCabin
RearCabin
CoachPositionInTrainSet
CoupledSide
CoachState
```

It does not show the V2.2 repeated `SingleCoach -> SingleCoachInATrainSet` wrapper that exists in the exact official XSD and is shown in the corrected TSI section.

Counter-hypothesis checked: this is not merely a collapsed wrapper view. The visible diagram expands the reused structure directly into the old fields; the exact V2.2 schema has `SingleCoach` as the immediate child of `GetTrainSetCompositionResponseStructure`.

```text
state: context_verified
classification: pdf_embedded_xsd_diagram_stale_candidate
validation impact: none; exact XSD remains authority
```

### TSD-004 - SubscribeTripInformation names the wrong event data structure

Visible page 40, section 6.5.7.2 says that after `SubscribeTripInformation` is initialised, event-based updates are sent via:

```text
RetrieveTripRefResponseStructure
```

That conflicts with:

- the operation being `SubscribeTripInformation`,
- section 6.5.6 where the corresponding Retrieve response carries `TripInformationStructure`, and
- the exact official V2.2 global `SubscribeTripInformationResponse`, which is typed as `TrainSetDataService.RetrieveTripInformationResponseStructure`.

The parallel `SubscribeTripRef` wording on page 38 correctly uses `RetrieveTripRefResponseStructure`, which strongly indicates copy/paste residue in section 6.5.7.2.

Counter-hypothesis checked: there is no documented reason for a TripInformation subscription to emit only TripRef events, and the executable schema explicitly selects the TripInformation response structure.

```text
state: context_verified
classification: pdf_response_structure_copy_paste_error_candidate
validation impact: exact XSD/event-context mapping uses RetrieveTripInformationResponseStructure
SDK rule: do not route SubscribeTripInformation events to the TripRef response type from this sentence
```

### DRTRAINSET22-001 - overview points examples to section 9.1 instead of section 10

Both German and English introductory lists say that examples of service interaction are in section `9.1`. The table of contents and actual heading place the examples in section `10`, while section 9.1 is the re-initialisation scenario.

```text
state: context_verified
classification: pdf_cross_reference_error_candidate
validation impact: none
```

### DRTRAINSET22-002 - stale 6.5.1 cross-references after insertion of the new structures

The V2.2 text contains multiple wrong `6.5.1` references in the TrainSetDataService detail section:

```text
6.5.5 UnsubscribeTripRef:
  TrainSetUnsubscribeRequestStructure described in 6.5.1
  actual definition: 6.5.2

6.5.6 RetrieveTripInformation:
  RetrieveTripRef (cf. 6.5.1)
  actual operation: 6.5.3

6.5.8 UnsubscribeTripInformation:
  TrainSetUnsubscribeRequestStructure described in 6.5.1
  actual definition: 6.5.2
```

The V2.2 version history says the new structures were inserted as 6.5.1 and 6.5.2 and that textual corrections followed in these sections, but these references remained stale.

```text
state: context_verified
classification: pdf_cross_reference_error_candidate
validation impact: none
```

## Rejected / resolved observations

- `TSD-003` is not promoted as an XSD defect; the stronger counter-explanation is confirmed by General Conventions + exact XSD + EV-104.
- No new V2.2 authority/provenance finding is opened because all three service schemas are exact official-tag files.
- TSI V2.2 multi-coach modelling is aligned between the visible corrected section and exact XSD.

## Completion state

```text
textual_fresh_read_complete: true
selected critical pages visually inspected from byte-pinned source: yes
all pages/figures visually exhausted: no
state: needs_visual_review
```

The remaining visual-closure status does not change the exact executable conclusions above, but prevents promotion to `exhaustive_read`.
