# Runtime-mapping review — TrainSet V2.2 TSD-002 / TSD-004 / TSM-002 / TSM-003 — 2026-09-21

Status: **reviewed / persisted / closure gate pending**.

## Exact authority

This block uses only the official VDV-301-2.2 TrainSet family:

```text
TrainSetDataService V2.2        7a132894c281d613e16514a6fa1bcbffe713d066
TrainSetManagementService V2.2  da9465d6683e3f7d54a546ab4a13739fb3c3e902
TrainSetInformationService V2.2 7ab1f8f892bfcea2a8b8a055f07de92c143356f9
Common V2.2                     468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enumerations V2.2               2a23b512379b18e8f122ac1272cef8229fb86283
```

No neighbouring version is substituted.

## TSD-002 — stale Unsubscribe request structures in the PDF overview

Assessment remains **confirmed PDF defect**.

The V2.2 overview points UnsubscribeTripRef and UnsubscribeTripInformation at Retrieve request structures, while the detailed text and exact XSD require `TrainSetDataService.TrainSetUnsubscribeRequestStructure`. EV-110/EV-160 prove that the specialised request including Client-IP-Address validates and the Retrieve-like CoachNumber-only form is rejected.

Decision: `candidate -> reviewed`.

The advisory is restricted to the two exact Unsubscribe request roots and the documented Retrieve-like request-shape boundary.

## TSD-004 — TripRef response structure named for TripInformation subscription events

Assessment remains **confirmed PDF defect**.

Physical page 40 says event-based `SubscribeTripInformation` updates use `RetrieveTripRefResponseStructure`. The exact XSD global subscription-event root instead uses `RetrieveTripInformationResponseStructure`; the parallel TripRef wording on page 38 is internally consistent.

Decision: `candidate -> reviewed`.

Critical context guard: this finding applies only to the **later data-event/callback** phase. The immediate Subscribe acknowledgement legitimately uses `SubscribeResponseStructure` under the operation-group context and must never be treated as TSD-004.

## TSM-002 — stale V2.2 operation-group member

Assessment remains **likely XSD defect**, confidence **high**.

The V2.2 correction history and global declaration use `TrainSetManagementService.GetTrainSetCompositionResponse`, but `TrainSetManagementServiceOperations` still contains the old `...GetTrainSetComposition` member. EV-104 executable-confirms both sides of that internal inconsistency.

Decision: `candidate -> reviewed`.

This is a resolver/operation-inventory **warning**, not an override of global-root validation. Tools must not silently rewrite the XSD group.

## TSM-003 — stale flat coach diagram

Assessment remains **confirmed PDF defect**.

The page-31 embedded diagram still depicts the old flat coach layout. The exact V2.2 response structure instead has one immediate `SingleCoach` child, typed as `SingleCoachInATrainSet`, with `maxOccurs=unbounded`. EV-162 and the independent visual review reject the hypothesis that the diagram is merely a collapsed view.

Decision: `candidate -> reviewed`.

The advisory is restricted to an actual XSD rejection where the submitted V2.2 composition response follows the old flat layout at the point where `SingleCoach` is required.

## Expected inventory after persistence

```text
reviewed        70
candidate        8
not_designed     0
not_applicable 114
implemented      0
```

No executable matcher, compatibility alias, payload rewrite or XSD mutation is introduced.

## Primary gate

Primary runtime-mapping gate **35646408602**: **SUCCESS**.

The gate verified all exact official V2.2 TrainSet blob identities, re-ran EV-104 and EV-110, executable-checked the TSD-004 data-event/acknowledgement separation and TSM-003 flat-vs-SingleCoach boundary, then passed semantic-registry, deterministic runtime-mapping, SDK-manifest and complete root-XSD regression checks.
