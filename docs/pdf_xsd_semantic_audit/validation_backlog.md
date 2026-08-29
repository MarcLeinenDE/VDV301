# PDF/XSD semantic audit - current validation backlog

Status: deterministic repository validation includes EV-113 for TicketValidationService V2.2. Remaining work includes continuing Deep Read Pass 2, mandatory post-Deep-Read legacy-finding revalidation, targeted finding regression, visual closure, live/integration evidence and later provider-specific work.

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
EV-110           run 33241603270  PASS  TrainSetDataService V2.2 TSD-002 unsubscribe request shape
EV-111           run 33242337308  PASS  official DoorState V2.1 DRS-002/DRS-003 behaviour
EV-112           run 33249561880  PASS  official TVS V2.1 RouteDeviation/CurrentTripRef/CurrentLineData type evidence
EV-113           run 33257767942  PASS  official TVS V2.2 RouteDeviation enum separation + CurrentTariffStop rename/type evidence
```

Last full-suite baseline: run `33228250613` confirmed:

```text
50/50 root XSDs compile
39 XSD service profiles
84 direct include edges
EV-103..EV-109 PASS
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

EV-110 through EV-113 are targeted additive tests and did not change any XSD. A later full-suite run can absorb them into the canonical all-checks baseline.

Authority guards:

```text
EV-108:
The public DMS V2.4 PDF is official VDV documentation.
The repository DMS V2.4 XSD checked by EV-108 is candidate/integration material.
EV-108 is not official-release XSD conformance evidence.

EV-109:
The three checked TrainSet V2.1 XSDs are byte-identical to the official VDV-301-2.1 tag.
EV-109 is V2.1 evidence only; V2.2 corrections/EV-104 are not back-applied.

EV-110:
TrainSetDataService V2.2 is exact official VDV-301-2.2 authority.
It proves the executable request-shape consequence of TSD-002; the PDF does not become executable authority.

EV-111:
DoorStateService V2.1 and its Common V1.0 + Enumerations V1.0 dependencies are exact official VDV-301-2.1 authority:
  DoorStateService abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
  Common V1.0     194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
  Enums V1.0      a9bea5bc73003ed91ded8519db06c32c4067831d
It proves RetrieveSpecific ErrorMessage vs OperationErrorMessage behavior and the default xs:anyType semantics of the exact untyped Get-request declaration form.
The DRS-003 probe does not claim a real global DoorState request root.

EV-112:
TicketValidationService V2.1 and its Common V1.0 + Enumerations V1.0 dependencies are exact official VDV-301-2.1 authority:
  TicketValidationService f6497e6469b82ee19b185c4de749d13a7ca60bed
  Common V1.0             194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
  Enums V1.0              a9bea5bc73003ed91ded8519db06c32c4067831d
It proves RouteDeviation uses RouteDeviationEnumeration with onroute/offroute/unknown, CurrentTripRef uses the case-sensitive IBIS-IP.NMTOKEN type, and GetCurrentLine uses TicketValidationService.CurrentLineDataStructure.
The CurrentLineData check proves XSD-side identifiers only; it does not classify every shortened PDF type-display convention.

EV-113:
TicketValidationService V2.2, Common V2.2 and Enumerations V2.2 are exact official VDV-301-2.2 authority:
  TicketValidationService 5a4be2b2ba66860f035777ec0458dba0790880e1
  Common V2.2             468fee6d177e7185dbcd5d3f90cfb114e29e01ae
  Enums V2.2              2a23b512379b18e8f122ac1272cef8229fb86283
It proves RouteDeviation uses RouteDeviationEnumeration even though RouteDirectionEnumeration also exists, and that the two enum value sets are incompatible.
It also proves CurrentTripRef uses case-sensitive IBIS-IP.NMTOKEN, confirms the exact CurrentLineData response type, and confirms the CurrentTariffStop rename boundary: new response root valid, stale CurrentStopPoint response root absent/invalid.
```

A provenance-only correction to the previously recorded DoorState dependency blob IDs is documented in `AUDIT_CORRECTION_DELTA_DOOR_V21_BLOB_PROVENANCE_2026-08-29.md`; executable results are unchanged.

### Runtime/protocol deterministic evidence

```text
RV-001  run 33112730418 PASS  HTTP/XML + Content-Type
RV-002  run 33119080288 PASS  DNS-SD/service discovery
RV-003  run 33228250613 PASS  TimeService/SNTP
RV-004  run 33119694991 PASS  Video RTSP/RTP boundary
```

The canonical repository workflow is `workflow_dispatch` only. Temporary push-trigger evidence workflows are removed after use.

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

All surviving Common findings are also subject to final legacy-finding Evidence-Gate revalidation unless already explicitly revalidated under the current gate.

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

DMS V2.2 and V2.4 visual closure remains deferred where no pinned-byte page review has yet closed the specific item.

## 4. TimeService V1.0 evidence status

The official TimeService V1.0 PDF is byte-pinned and textually fresh-read. RV-003 confirms the non-XSD SNTP/discovery profile, including no cyclic current-time broadcast expectation.

Remaining TimeService work is live integration plus unresolved visual closure; no new deterministic check is currently required for the established facts.

## 5. TrainSet V2.1 / V2.2 evidence status

### V2.1

EV-109 run `33228250613` confirms:

```text
TSI-001  V2.1 flat composition structure cannot carry a second PDF-described coach record.
TSM-001  V2.1 executable root is GetTrainSetComposition; later ...Response root is absent.
TSD-001  V2.1 service XSD lacks service-prefixed Subscribe/Unsubscribe roots while Common generic subscription infrastructure exists.
```

Documentation findings: `DRTRAINSET21-001..003`. Rejected observation retained: suspected `coupledSide/CoupledSide` mismatch was disproved.

### V2.2

The byte-pinned V2.2 Fresh Read is textually complete with targeted pinned-byte visual review. Exact official VDV-301-2.2 service blobs are established.

Existing findings revalidated under the current Evidence Gate:

```text
TSM-002 -> executable-confirmed operation-group/global-root mismatch; EV-104 remains valid.
TSD-002 -> executable-confirmed PDF overview request-structure mismatch; EV-110 run 33241603270.
TSD-003 -> contextual-not-defect / response-context resolver requirement; General Conventions + EV-104 confirm immediate acknowledgement vs later data-event roles.
```

New V2.2 findings:

```text
TSM-003          stale V2.1-style flat composition diagram embedded on V2.2 page 31
TSD-004          SubscribeTripInformation text names RetrieveTripRefResponseStructure for later events instead of RetrieveTripInformationResponseStructure
DRTRAINSET22-001 examples cross-reference points to 9.1 instead of section 10
DRTRAINSET22-002 multiple stale 6.5.1 cross-references after new subscription structures were inserted
```

TrainSet V2.2 remains `needs_visual_review`, not `exhaustive_read`, because only targeted critical pages were visually closed.

## 6. DoorStateService V2.1 evidence status

The official DoorState V2.1 PDF is byte-pinned and fresh-read. Critical pages 9-12 were rendered from the exact pinned bytes and visibly inspected. Exact authority is intentionally mixed-version:

```text
DoorStateService V2.1 -> Common V1.0 -> Enumerations V1.0
```

Exact official blobs:

```text
DoorStateService  abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
Common V1.0      194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
Enums V1.0       a9bea5bc73003ed91ded8519db06c32c4067831d
```

Existing findings revalidated under the current Evidence Gate:

```text
DRS-001 -> context-verified PDF operation-overview copy/paste error.
DRS-002 -> executable-confirmed by EV-111: RetrieveSpecific accepts ErrorMessage, rejects OperationErrorMessage.
DRS-003 -> declaration semantics executable-confirmed by EV-111: exact untyped local request declarations default to xs:anyType and are more permissive than an explicitly empty request type.
DRS-004 -> context-verified XSD documentation-only typo note; no validation impact.
```

New findings:

```text
DRDOOR21-001  PDF request-table descriptions use shortened/typoed Retrieve operation names.
DRDOOR21-002  DoorOpenState success description is copied from operation-state semantics.
```

Rejected observation:

```text
Visible -1:1 rows with a/b labels are valid VDV choice notation, not negative cardinality.
No DoorState cardinality finding is opened from those rows.
```

DoorState V2.1 remains `needs_visual_review`, not `exhaustive_read`, because visual review was targeted.

## 7. TicketValidationService V2.1 evidence status

The official TVS V2.1 PDF is byte-pinned and independently fresh-read before reopening historical TicketValidation findings.

Exact authority is intentionally mixed-version:

```text
TicketValidationService V2.1 -> Common V1.0 -> Enumerations V1.0
```

Source/evidence:

```text
PDF sha256: 676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d
PDF size: 752652
pin run: 33248946083
visual render run: 33249247106
pages visibly reviewed: 10-17

TVS V2.1 service XSD: f6497e6469b82ee19b185c4de749d13a7ca60bed
Common V1.0:           194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
Enumerations V1.0:     a9bea5bc73003ed91ded8519db06c32c4067831d
```

Existing finding revalidated under the current Evidence Gate:

```text
TVS-002 -> executable-confirmed by EV-112:
           PDF RouteDirectionEnumeration vs exact XSD RouteDeviationEnumeration.
           onroute/offroute/unknown validate; out-of-set value fails.
```

Deep-Read findings:

```text
DRTVS21-001 CurrentTripRef PDF IBIS-IP.NMToken vs exact case-sensitive IBIS-IP.NMTOKEN; EV-112 executable-confirmed.
DRTVS21-002 GetCurrentLine response display misses service-name separator dot; Structure-suffix omission is explicitly not classified.
DRTVS21-003 flow text SubscribeCurrentStop vs formal SubscribeCurrentStopPoint.
DRTVS21-004 minor non-executable PDF spelling/caption residue.
```

Scope boundary:

```text
TVS-001 is V2.4 scope and was not revalidated by this block.
TVS-003 begins at V2.2 and was not revalidated by this block.
```

TVS V2.1 remains `needs_visual_review`, not `exhaustive_read`, because visual review was targeted.

## 8. TicketValidationService V2.2 evidence status

The official TVS V2.2 PDF was independently byte-pinned and fresh-read before historical V2.2 findings or V2.1 correction history were reopened.

Exact authority is version-aligned:

```text
TicketValidationService V2.2 -> Common V2.2 -> Enumerations V2.2
```

Source/evidence:

```text
PDF sha256: 1915a1b12c24386e9a8ab5638fd88af6a442b5e42586b7b2d48f03e9a4205083
PDF size: 785931
pin run: 33255245725
visual render run: 33255450850
pages visibly reviewed: 10-18

TVS V2.2 service XSD: 5a4be2b2ba66860f035777ec0458dba0790880e1
Common V2.2:           468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enumerations V2.2:     2a23b512379b18e8f122ac1272cef8229fb86283
```

Existing findings revalidated under the current Evidence Gate:

```text
TVS-002 -> executable-confirmed by EV-113.
           Exact RouteDeviationEnumeration and RouteDirectionEnumeration both exist but have incompatible value sets.
           VehicleData.RouteDeviation uses RouteDeviationEnumeration.

TVS-003 -> executable-confirmed/refined by EV-113.
           V2.2 explicitly documents CurrentStopPoint -> CurrentTariffStop, while stale CurrentStopPoint names remain in both operation overviews and page-14 response/data labels.
           Exact new response root validates; stale response root has no matching global declaration.
```

Existing Deep-Read finding scopes independently extended into V2.2:

```text
DRTVS21-001 -> V2.2 repeats IBIS-IP.NMToken; EV-113 confirms exact IBIS-IP.NMTOKEN and case-sensitive failure of the PDF spelling.
DRTVS21-002 -> V2.2 repeats missing-dot TicketValidationServiceCurrentLineData; context-verified with EV-113 exact-XSD support.
DRTVS21-003 -> V2.2 flow text repeats SubscribeCurrentStop; detailed formal section is SubscribeCurrentTariffStop after the documented rename.
```

Deduplication result:

```text
No new V2.2-only finding ID was needed.
The operation-overview stale-name observation refines TVS-003.
The recurring NMToken / CurrentLine / SubscribeCurrentStop observations extend DRTVS21-001..003 instead of duplicating them.
```

TVS V2.2 remains `needs_visual_review`, not `exhaustive_read`, because visual review was targeted.

## 9. Mandatory legacy finding revalidation before baseline freeze

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

## 10. Canonical remaining live backlog

The full current live/device/network backlog is:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

Do not recreate duplicate per-service live backlog lists in this central file.

## 11. Remaining live/integration categories

```text
Subscription runtime:
  real Subscribe acknowledgement, callback delivery, heartbeat timing, Unsubscribe behavior, TrainSet parameterized subscription context

Discovery / DNS-SD:
  real PTR browse, raw SRV/TXT capture, mDNS vs unicast DNS transport, reachability, parallel versions, TTL/cache

HTTP:
  real GET/POST, HTTP version/status/headers, Content-Type/charset/encoding, redirects/auth/timeouts, feed response XML to exact resolver

UDP/network:
  multicast reception where applicable, IGMP symptoms, routing/duplicate-IP diagnostics, train/vehicle integration

TimeService:
  real DNS-SD, SNTP request/reply, reachability, clock offset/round trip, actual local synchronization state

Video:
  real RTSP session/SDP/auth, RTP/RTCP, loss/jitter/continuity and media-property comparison

Mixed-version resolver:
  discovery -> profile -> exact schema route, parallel versions, candidate guard, TrainSet response context, legacy V1.0 root-map path
```

Open live items require real devices/provider systems/simulators/network access or packet capture. Their open state is not a failed conformance result.

## 12. Deferred visual/document review

Layout-sensitive items not yet closed by visible-page evidence remain `needs_visual_review` / candidate as applicable. The pinned-byte visual fallback is preferred when the interactive renderer returns cache-miss.

Do not promote a document to `exhaustive_read` merely because selected critical pages were rendered.

## 13. Official correction candidate review

No upstream action is automatic. Any later official-facing correction requires Evidence-Gate-revalidated findings and explicit user approval before PR/comment/review/merge action.

## 14. SDK implementation readiness

Finding-driven SDK implementation remains frozen during the current Deep Read and legacy revalidation phases.

Required guardrails include:

```text
exact service/version routing
candidate authority separation
schema_variant_id for same-path variants
operation/context manifest
legacy root-map support
non-XSD protocol profiles
runtime authority + severity separation
no unexecuted live check represented as conformance evidence
no unrevalidated finding represented as SDK accept/reject knowledge
TrainSet V2.2 response-context resolver for TSD-003
TrainSet TSM root inventory must not rely blindly on stale operation-group member
DoorState V2.1 must preserve exact mixed-version Common V1.0/Enums V1.0 dependency routing
DoorState RetrieveSpecific diagnostics must not silently normalize OperationErrorMessage/ErrorMessage
DoorState untyped Get-request declarations must not be silently tightened to an invented empty type
TVS V2.1 must preserve exact mixed-version Common V1.0/Enums V1.0 dependency routing
TVS V2.2 must preserve exact version-aligned Common V2.2/Enums V2.2 routing
TVS RouteDeviation diagnostics must not replace RouteDeviationEnumeration with the PDF-printed RouteDirectionEnumeration
TVS V2.2 must not treat RouteDirectionEnumeration as an acceptable RouteDeviation alias merely because both enum names exist
TVS CurrentTripRef diagnostics must not case-normalize IBIS-IP.NMTOKEN into the PDF-printed IBIS-IP.NMToken
TVS CurrentTariffStop diagnostics must not accept stale CurrentStopPoint response/type labels as executable aliases
```

Current sequencing:

```text
fresh-read TVS_V2.3
-> continue remaining Deep Reads
-> finish Deep Read Pass 2
-> freeze complete finding inventory
-> revalidate all untouched/non-current findings under FINDING_EVIDENCE_GATE
-> reconcile findings/provenance and require zero pending SDK-relevant findings
-> freeze audit/finding baseline
-> only then implement finding-driven SDK regression/diagnostic knowledge
```
