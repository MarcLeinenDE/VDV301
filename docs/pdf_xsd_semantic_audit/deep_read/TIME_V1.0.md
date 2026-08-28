# TimeService V1.0 Deep Read Pass 2

Status: textual fresh read complete; partial original-PDF visual confirmation available; remaining critical pages returned cache-miss, therefore final state is `needs_visual_review` rather than `exhaustive_read`.

## Scope and source provenance

Official public document:

```text
VDV-Schrift 301-2-10
TimeService V1.0
02/2018
```

Byte-pinned source:

```text
source_id: TIME_V1.0
SHA-256: d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3
size: 515920 bytes
pin run: 33196758957
```

Authority lane:

```text
official VDV documentation + referenced external protocol standards
validation_kind: protocol_discovery_profile
XSD authority: not applicable by design
```

TimeService must not be converted into an XML/XSD service merely because other VDV 301 services use XML payloads.

## Fresh-read method

The byte-pinned TimeService document was read independently before consulting existing `DR3012-006` or RV-003 as a template.

After the fresh read, the result was compared with:

```text
VDV 301-2 V1.0, 07/2016
VDV-Mitteilung 3002, 10/2016
VDV 301-2-11 VideoLiveService, 05/2017
existing RV-003 deterministic profile
```

## Normative/profile facts established by the fresh read

The TimeService V1.0 writing states:

```text
- TimeService implements the time-determination component.
- SNTP is used under RFC 4330.
- DNS-SD is used to announce the SNTP server.
- TXT entry: sntp-server=$IP-address.
- service-discovery type: _ibisip_udp._udp.
- actual time synchronization is performed by SNTP.
- German text explicitly states that cyclic transmission of the current time is not intended.
- timezone information is described as a TXT value, example timezone=UTC+1.
```

The earlier VDV 301-2 V1.0 generic TXT table explicitly marks `sntp-server` as mandatory for the time-synchronization service. It does not provide a comparable mandatory/optional cardinality for `timezone`.

Therefore the audit keeps the existing conservative runtime rule:

```text
missing sntp-server -> VDV profile error
hostname instead of IP address -> VDV profile error
missing timezone -> profile note, not invented hard failure
present timezone -> preserve raw value; no silent syntax conversion
```

## DRTIME10-001 - English foreword points TimeService to VDV 301-2-1

German foreword:

```text
VDV-Schrift 301-2-10 describes TimeService.
```

English foreword:

```text
VDV 301-2-1 describes TimeService.
```

The document identity itself is VDV 301-2-10. VDV 301-2-1 is the Common Data Structures/Enumerations part, not TimeService.

Classification:

```text
id: DRTIME10-001
classification: pdf_cross_reference_or_document_identity_error_candidate
state: confirmed_text_needs_visual_review
confidence: very_high
validation impact: documentation/resolver only
handling: never route TimeService to VDV 301-2-1 from this English foreword sentence
```

The original page-3 render attempt returned cache-miss; native PDF text is clear.

## DRTIME10-002 - bilingual omission of the no-cyclic-time statement

The German TimeService section explicitly states:

```text
No cyclic transmission of the current time is intended in addition to SNTP synchronization.
```

The adjacent English service section describes the same SNTP/DNS-SD profile but omits this sentence.

Classification:

```text
id: DRTIME10-002
classification: bilingual_normative_text_omission_candidate
state: visually_confirmed
confidence: very_high
validation impact: runtime/profile interpretation
```

This is an omission, not an English contradiction.

SDK/runtime consequence:

```text
Do not infer from _ibisip_udp._udp that TimeService is a generic cyclic UDP time-broadcast service.
Time acquisition/synchronization remains the SNTP path.
```

A visible page-5 screenshot confirmed the German sentence and its absence from the adjacent English section.

## DRTIME10-003 - English version-history `cd. 1`

The English V1.0 technical-correction line prints:

```text
Definition of the service type: _ibisip_udp._udp, cd. 1
```

The context strongly indicates an editorial cross-reference artifact; the German line uses a chapter-reference formulation.

Classification:

```text
id: DRTIME10-003
classification: minor_pdf_editorial_cross_reference_typo_candidate
state: confirmed_text_needs_visual_review
confidence: high
validation impact: none
```

No technical meaning is inferred from `cd.`. The page-6 render attempt returned cache-miss.

## DR3012-006 - historical context resolved

Earlier finding state:

```text
historical_cross_reference_candidate
needs_historical_context
```

The VDV 301-2 V1.0 base writing dated 07/2016 says in its SNTP section:

```text
Further information on implementation: see VDV 301-2-11.
```

Historical cross-check:

```text
VDV-Mitteilung 3002 | 10/2016:
  VDV-301-2-10 Dienst TimeService, Version 1.0, extracted from VDV-301-2.

VDV-Schrift 301-2-11 | 05/2017:
  VideoLiveService.

VDV-Schrift 301-2-10 | 02/2018:
  TimeService V1.0.
```

Resolution:

```text
id: DR3012-006
classification: pdf_cross_reference_error_candidate
state: historical_context_resolved
confidence: very_high
summary: the 07/2016 reference to VDV 301-2-11 for TimeService is a wrong/stale document-number reference, not merely a modern renumbering ambiguity
normative validation impact: none
resolver guard: do not route TimeService to VDV 301-2-11
```

The audit does not speculate on the internal editorial reason for the stale number.

## RV-003 reconciliation

Existing RV-003 was compared only after the independent PDF read.

Result:

```text
existing sntp-server rule: retained
existing IP-address-only rule: retained
existing _ibisip_udp._udp rule: retained
existing RFC 4330 profile: retained
existing no-XML/XSD architecture guard: retained
existing conservative timezone handling: retained
```

One additional deterministic architecture guard was added:

```text
cyclic_time_broadcast_expected() == False
```

Strengthened full-suite evidence:

```text
RV-003 strengthened run: 33197358294
head tested: 215fd3cbb00619b0cf0232856c7163a52402318b
result: PASS
new check: TimeService does not expect cyclic transmission of current time
```

The same run re-confirmed the full deterministic repository baseline, including 50 root XSDs, existing EV-101 through EV-108, RV-001/RV-002/RV-004 and SDK manifest/profile checks.

The workflow was immediately restored to `workflow_dispatch` only.

## External-standard version guard

The selected VDV TimeService V1.0 writing explicitly references RFC 4330.

Therefore:

```text
RFC 5905 or later NTP material may be used as modern compatibility/control context only.
Do not latest-wins substitute it for the VDV-selected historical RFC 4330 profile.
```

## Visual-review boundary

```text
page 5 service-content screenshot: succeeded
page 3 foreword screenshot: cache-miss
page 6 version-history screenshot: cache-miss
```

Consequently:

```text
textual_fresh_read_complete: true
original_pdf_visual_review: partial
state: needs_visual_review
```

## Result

```text
TimeService V1.0 fresh textual read complete.
Non-XSD protocol/discovery architecture confirmed.
DRTIME10-001 opened.
DRTIME10-002 opened and visually confirmed.
DRTIME10-003 opened as minor editorial finding.
DR3012-006 historical context resolved as wrong/stale VDV 301-2-11 reference.
RV-003 strengthened with explicit no-cyclic-time-broadcast guard and full-suite PASS.
No XSD changed.
No official-facing action authorized.
```
