# Audit handoff delta - TrainSet V2.2 Deep Read - 2026-08-29

Base: current Deep Read Pass 2 state on `dev/schema-integration`.

## Source / visual evidence

```text
source_id: TRAINSET_V2.2
sha256: c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e
size: 1744296
pin run: 33239594518
pinned-byte render run: 33239787579
reviewed pages: 9,24,25,29,31,34,35,38,40,51
state: needs_visual_review
```

The textual Fresh Read was performed before reopening historical TrainSet V2.2 findings/EV-104.

## Exact official XSD authority

All three checked TrainSet V2.2 service schemas on the integration branch match the official `VDV-301-2.2` tag:

```text
TSI 7ab1f8f892bfcea2a8b8a055f07de92c143356f9
TSM da9465d6683e3f7d54a546ab4a13739fb3c3e902
TSD 7a132894c281d613e16514a6fa1bcbffe713d066
Common 468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enums 2a23b512379b18e8f122ac1272cef8229fb86283
```

## Existing V2.2 findings revalidated

```text
TSM-002 -> executable-confirmed XSD operation-group/global-root mismatch; EV-104 remains valid after current source/context/disproof gate.
TSD-002 -> executable-confirmed PDF overview mismatch; new EV-110 run 33241603270.
TSD-003 -> contextual-not-defect; immediate Subscribe acknowledgement vs later data-event typing confirmed by General Conventions + exact XSD + EV-104.
```

EV-110 decisive result:

```text
specialised TrainSetUnsubscribeRequestStructure shape -> valid
Retrieve-like CoachNumber-only shape                  -> invalid
schema expects Client-IP-Address first
```

Temporary EV-110 workflow was removed after execution; checker `tools/validate_trainset_tsd002_ev110.py` remains.

## New V2.2 findings

```text
TSM-003
  pinned-byte page 31 contains stale flat V2.1-style composition diagram despite corrected V2.2 root/text and exact SingleCoach wrapper in XSD.

TSD-004
  SubscribeTripInformation section says later event updates use RetrieveTripRefResponseStructure; exact event context uses RetrieveTripInformationResponseStructure.

DRTRAINSET22-001
  German and English introduction point examples to section 9.1; actual examples are section 10.

DRTRAINSET22-002
  multiple stale 6.5.1 cross-references remain after V2.2 insertion of the new 6.5.1/6.5.2 subscription structures.
```

## Authority / SDK guards

```text
- exact V2.2 XSD remains executable authority
- no alias for PDF overview unsubscribe shapes
- response-context resolver required for TSD-003
- do not route SubscribeTripInformation event data to TripRef type from the bad PDF sentence
- do not derive TSM global operation/root inventory solely from the stale V2.2 operation group
```

## Branch hygiene

Both temporary TrainSet V2.2 workflows used for pin/render/EV execution were removed after evidence extraction. Canonical workflow policy remains manual-only.

## Next natural Deep Read target

```text
DOOR_V2.1 (VDV 301-2-15 DoorStateService V2.1)
```

Before SDK/remediation baseline freeze, the separately planned full legacy-finding revalidation remains mandatory for every surviving finding not already explicitly revalidated under the current Evidence Gate.
