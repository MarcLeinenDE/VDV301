# Audit Handoff Delta - TimeService V1.0 Deep Read

Date: 2026-08-28
Branch: `dev/schema-integration`

This delta records the TimeService V1.0 Deep Read changes after the completed DMS V2.4 block.

## Source pin

```text
source_id: TIME_V1.0
VDV-Schrift: 301-2-10 TimeService V1.0, 02/2018
SHA-256: d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3
size: 515920 bytes
pin run: 33196758957
```

## Authority lane

```text
official VDV public writing
non-XSD service by design
validation_kind: protocol_discovery_profile
external protocol: RFC 4330 where explicitly referenced by VDV
```

Do not synthesize TimeService XML operations or an XSD.

## Fresh-read findings

```text
DRTIME10-001
  English foreword says VDV 301-2-1 describes TimeService;
  German text and document identity correctly use VDV 301-2-10.

DRTIME10-002
  German service text explicitly says cyclic transmission of current time is not intended;
  adjacent English section omits that sentence.
  Page-5 visual confirmation succeeded.

DRTIME10-003
  English V1.0 history prints 'cd. 1' after the _ibisip_udp._udp correction;
  treated as a minor editorial cross-reference artifact.
```

## DR3012-006 resolved

Old state:

```text
historical_cross_reference_candidate / needs_historical_context
```

Resolved evidence chain:

```text
VDV 301-2 V1.0, 07/2016:
  SNTP implementation points to VDV 301-2-11.

VDV-Mitteilung 3002, 10/2016:
  VDV-301-2-10 Dienst TimeService V1.0.

VDV 301-2-11, 05/2017:
  VideoLiveService.

VDV 301-2-10, 02/2018:
  TimeService V1.0.
```

New state:

```text
classification: pdf_cross_reference_error_candidate
state: historical_context_resolved
confidence: very_high
resolver guard: do not route TimeService to VDV 301-2-11
```

No speculation is made about the internal editorial reason for the stale number.

## RV-003 strengthened

Fresh-read reconciliation retained the existing deterministic rules for:

```text
_ibisip_udp._udp
mandatory sntp-server profile field
IP-address syntax for sntp-server
RFC 4330
conservative timezone handling
non-XSD architecture
```

New explicit architecture guard:

```text
cyclic_time_broadcast_expected() == False
```

Strengthened evidence:

```text
run: 33197358294
head tested: 215fd3cbb00619b0cf0232856c7163a52402318b
result: PASS
full deterministic suite: PASS
```

Workflow restored to manual-only in:

```text
b2153c3f01b436eb262f0884c1e212e5faa2d9fd
```

## Visual boundary

```text
service page 5: visual confirmation succeeded
foreword page 3: cache-miss
version-history page 6: cache-miss
```

Therefore TimeService ends as `needs_visual_review`, not `exhaustive_read`.

## Safety

```text
No XSD changed.
No master change.
No PR/comment/review/merge action.
No newer NTP standard silently substituted for RFC 4330.
No hard timezone cardinality invented.
```

## Recommended next Deep Read

`VLS_V1.0` / VDV 301-2-11 VideoLiveService V1.0.

Reason:

```text
- directly follows the now-resolved historical 301-2-10/301-2-11 numbering chain;
- the public V1.0 writing is already part of the source catalog;
- later V2.0 video compositor evidence exists, but V1.0 should be read independently first;
- this provides a clean bridge from non-XSD TimeService to the historical video family and its RTSP/RTP boundary.
```

Sequence:

```text
1. byte-pin official VLS_V1.0 PDF;
2. fresh-read V1.0 independently;
3. establish exact V1.0 schema/provenance status without mapping to V2.0 by convenience;
4. only after fresh read compare historical video findings and RV-004;
5. retain RTSP/RTP external-protocol authority separately from VDV XML/schema authority.
```
