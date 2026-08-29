# PDF/XSD semantic audit - current validation backlog

Status: deterministic repository validation includes EV-109 TrainSet V2.1 evidence and the current full-suite baseline. Remaining work includes the continuing Deep Read, mandatory post-Deep-Read legacy-finding revalidation, targeted finding regression, visual closure, live/integration evidence and later provider-specific work.

## 1. Completed deterministic evidence

### XML/XSD evidence

```text
EV-001 + EV-002  run 33109011670  PASS
EV-101           run 33109367265  PASS  PCS-001
EV-102           run 33109768872  PASS  CE-018
EV-103           run 33111119723  PASS  video compositors
EV-104           run 33111644388  PASS  TrainSet V2.2 context/root evidence
EV-105           run 33111831627  PASS  AnalogRadio candidate cardinality
EV-106           run 33169314332  PASS  Common V2.3 official/candidate authority split
EV-107           run 33181833930  PASS  official DMS V2.2 Deep Read declarations
EV-108           run 33182963733  PASS  candidate/integration DMS V2.4 Deep Read declarations
EV-109           run 33228250613  PASS  official TrainSet V2.1 Deep Read evidence
```

Current full-suite run `33228250613` confirmed:

```text
50/50 root XSDs compile
39 XSD service profiles
84 direct include edges
EV-103..EV-109 PASS in the current suite
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

Authority guards:

```text
EV-108:
The public DMS V2.4 PDF is official VDV documentation.
The repository DMS V2.4 XSD checked by EV-108 is candidate/integration material.
EV-108 is not official-release XSD conformance evidence.

EV-109:
The three checked TrainSet V2.1 XSDs are byte-identical to the official VDV-301-2.1 tag.
EV-109 is V2.1 evidence only; V2.2 corrections/EV-104 are not back-applied.
```

### Runtime/protocol deterministic evidence

```text
RV-001  run 33112730418  PASS  HTTP/XML + Content-Type
RV-002  run 33119080288  PASS  DNS-SD/service discovery
RV-003  run 33197358294  PASS  TimeService/SNTP, strengthened after byte-pinned Fresh Read
RV-004  run 33119694991  PASS  Video RTSP/RTP boundary
```

The canonical repository workflow is `workflow_dispatch` only.

## 2. Targeted Common regression backlog from Deep Read

Fresh byte-pinned Common V2.3 Deep Read opened CE-021..CE-026.

Later executable strengthening may cover:

```text
CE-021 LogMessage: negative <MessageBody>, positive <Message>
CE-022 ServiceIdentification: negative outer <ServiceName>, positive outer <Service>
CE-024 UnsubscribeResponse: negative without Active, positive with Active
CE-025 Subscribe/Unsubscribe request: negative <Reply-Path>, positive <ReplyPath>
CE-026 BeaconPoint V2.3: negative <Description>, positive <Desciption>; V2.4 control <Description>
```

CE-023 is a PDF copy/paste-table finding and does not require an executable XSD defect test. CE-019 visual closure remains pending. CE-020 is already executable-confirmed by EV-106.

All surviving Common findings are also subject to the final legacy-finding Evidence-Gate revalidation; earlier confidence labels are not grandfathered.

## 3. DMS V2.2 / V2.4 evidence status

EV-107 closes the deterministic official-V2.2 declaration side for DMS-005..DMS-007 and the executable enum spelling behind DRDMS22-003.

EV-108 closes the deterministic candidate/integration-V2.4 declaration side and confirms:

```text
DMS-005 persists against candidate/integration V2.4 XSD.
DMS-006 is aligned in checked V2.4 PDF/candidate profile.
DMS-007 persists against candidate/integration V2.4 XSD.
ErrorMessage is 0:* in V2.4 candidate.
InstallUpdate ID/Timestamp/URL/checksum/size are optional in V2.4 candidate.
```

DMS V2.2 and V2.4 visual closure remains deferred where original-PDF screenshot attempts returned cache-miss and no later pinned-byte page review has yet closed the specific item.

## 4. TimeService V1.0 evidence status

The official TimeService V1.0 PDF is byte-pinned and textually fresh-read.

Fresh findings:

```text
DRTIME10-001 English foreword wrongly points TimeService to VDV 301-2-1.
DRTIME10-002 German text excludes cyclic transmission of current time; English omits that sentence.
DRTIME10-003 minor English version-history cross-reference artifact 'cd. 1'.
```

Historical finding resolved:

```text
DR3012-006:
07/2016 base writing points TimeService to VDV 301-2-11.
VDV-Mitteilung 3002 10/2016 already maps TimeService to VDV-301-2-10.
VDV 301-2-11 05/2017 is VideoLiveService.
Result: wrong/stale historical document-number reference; no TimeService 301-2-11 resolver alias.
```

Strengthened RV-003 run `33197358294` confirms:

```text
_ibisip_udp._udp discovery profile
mandatory sntp-server profile field
IP-address-only sntp-server syntax
RFC 4330 request/reply checks
no XML/XSD operations
no cyclic transmission of current time expected
conservative timezone handling retained
```

No further deterministic TimeService regression is currently required for these established facts. Remaining TimeService work is live integration plus any unresolved visual closure.

## 5. TrainSet V2.1 evidence status

The byte-pinned V2.1 Fresh Read is completed textually with targeted original visual review and exact official V2.1 XSD authority established.

EV-109 run `33228250613` confirms:

```text
TSI-001  V2.1 flat composition structure accepts one coach record and rejects a second PDF-described record.
TSM-001  V2.1 executable root is GetTrainSetComposition; later ...Response root is absent.
TSD-001  V2.1 service XSD lacks service-prefixed Subscribe/Unsubscribe members/roots while Common generic subscription infrastructure exists.
```

New documentation findings:

```text
DRTRAINSET21-001  stale/wrong section cross-reference
DRTRAINSET21-002  page 44 wrongly names TrainSetDataService as having equally named composition operations
DRTRAINSET21-003  page 44 GetTrainSetCompositon typo
```

Disproof success retained:

```text
suspected coupledSide/CoupledSide mismatch -> rejected; visible original + exact XSD both use CoupledSide
```

V2.2-specific `TSM-002`, `TSD-002`, `TSD-003` remain deferred until an independent `TRAINSET_V2.2` Fresh Read under the current Evidence Gate. Historical EV-104 evidence is not sufficient to skip that revalidation.

## 6. Mandatory legacy finding revalidation before baseline freeze

After Deep Read Pass 2, every surviving finding not already explicitly revalidated under the current Evidence Gate must be checked again.

Canonical plan/registry:

```text
docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md
audit_registry/finding_revalidation_registry_v0.1.json
```

Rules:

```text
no grandfathering of old confidence/state labels
freeze the complete finding inventory only after Deep Read completion
run original-source + definition + exact-authority + context + disproof checks
executable-confirm XML-validity claims when technically practical
reconcile duplicate/superseded/withdrawn findings
require zero pending SDK-relevant findings before finding-baseline freeze
```

Until this phase is complete:

```text
SDK finding knowledge ready = false
remediation ready = false
```

## 7. Canonical remaining live backlog

The full current live/device/network backlog is:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

Do not recreate duplicate per-service live backlog lists in this central file.

## 8. Remaining live/integration categories

### Subscription runtime

```text
real Subscribe acknowledgement
callback delivery
heartbeat timing
Unsubscribe behavior
TrainSet parameterized subscription context
```

### Discovery / DNS-SD

```text
real PTR browse
raw SRV/TXT capture
actual mDNS vs unicast DNS transport
host resolution/reachability
multiple simultaneous versions using separate endpoint identity
TTL/cache behavior
```

### HTTP

```text
real GET/POST operations
HTTP version/status/headers
actual Content-Type/charset/encoding
redirect/auth/timeout behavior
feed real response XML to exact XSD resolver
HTMLDisplay real fetch path
```

### UDP / network

```text
multicast join/reception
cycle observation where the selected service profile actually defines cyclic UDP data
IGMP-related failure symptoms
routing/duplicate-IP diagnostics
train/vehicle network integration
physical/network architecture evidence
```

TimeService guard: do not put TimeService into a generic cyclic current-time-broadcast test merely because its DNS-SD type is `_ibisip_udp._udp`.

### TimeService

```text
real DNS-SD discovery
real SNTP request/reply
advertised endpoint reachability
clock offset/round-trip observation
actual local clock synchronization state
certificate/TLS clock-skew diagnostic integration
```

### Video

```text
real ListAllLiveStreams
rtspURI reachability
RTSP session/control sequence
SDP/auth
RTP/RTCP reception
loss/jitter/continuity
codec/resolution/frame-rate/bitrate comparison
```

### Mixed-version resolver

```text
end-to-end discovery -> profile -> exact schema route
parallel versions of one service
candidate-selection guard
TrainSet response-context routing
legacy V1.0 root-map end-to-end path
```

## 9. Environment dependency

Open live items require one or more of:

```text
real VDV301 device
provider test system
controlled simulator
network access
packet capture
physical/inventory documentation
```

Their open state is **not** a failed conformance result.

## 10. Deferred visual/document review

Layout-sensitive items that are not yet closed by visible-page evidence remain `needs_visual_review` / candidate as applicable. The pinned-byte visual fallback is preferred when the interactive renderer returns cache-miss.

Do not promote a document to `exhaustive_read` merely because selected critical pages were rendered; all applicable chapters/tables/examples/figures must have been considered.

## 11. Official correction candidate review

No upstream action is automatic.

If an official-facing correction is later considered:

```text
- use only Evidence-Gate-revalidated findings
- identify exact affected versions
- distinguish PDF correction from XSD/protocol correction
- add targeted regression evidence where materially useful
- obtain explicit user approval before PR/comment/review/merge action
```

## 12. SDK implementation readiness

SDK architecture may continue to be derived from the deterministic authority baseline, but finding-driven implementation remains frozen during the current Deep Read and legacy revalidation phases.

Required guardrails:

```text
exact service/version routing
candidate authority separation
schema_variant_id for same-path variants
operation/context manifest
legacy root-map support
non-XSD protocol profiles
runtime authority + severity separation
TimeService no-cyclic-time-broadcast specialization
no unexecuted live check represented as conformance evidence
no unrevalidated finding represented as SDK accept/reject knowledge
```

Current sequencing:

```text
finish Deep Read Pass 2
-> freeze complete finding inventory
-> revalidate all untouched/non-current findings under FINDING_EVIDENCE_GATE
-> reconcile findings/provenance and require zero pending SDK-relevant findings
-> freeze audit/finding baseline
-> only then implement finding-driven SDK regression/diagnostic knowledge
```
