# PDF/XSD semantic audit - consolidated findings index

Status: central current-state index after completion of the semantic/provenance first pass, executable XSD evidence, deterministic runtime evidence and ongoing Deep Read Pass 2.

This file is deliberately concise. Detailed evidence remains in the service-specific finding registers, Common addendum, Deep Read reports, EV documents and RV documents.

## 1. Validation / authority rules

```text
Selected XSD family = executable XML validation authority where an XSD profile exists.
PDF/XSD differences = findings/provider notes, not silent schema rewrites.
No latest-XSD-wins dependency substitution.
No latest-external-protocol-version substitution.
Candidate/integration XSDs remain candidate/integration.
Operation-group membership alone is not a complete supported-operation authority.
Runtime results must retain authority source separately from severity.
```

## 2. Executable-confirmed high-impact findings

### PCS-001 - PassengerCountingService V2.1 `OperationNotSupported`

```text
state: executable-confirmed
exact route: PCS V2.1 -> Common V1.0 -> Enums V1.0
result: OperationNotSupported rejected by exact selected enum pool
control: Enums V2.1 accepts it
run: 33109367265
```

Handling: preserve exact dependency routing; do not substitute Enums V2.1 merely to make the documented value validate.

### CE-018 - ServiceIdentificationWithStateList cardinality

```text
state: executable-confirmed
PDF: 1:*
XSD history checked V1.0-V2.4: 0:*
run: 33109768872
```

Both zero-item and one-item structures validate across all checked Common versions.

### CE-020 - Common V2.3 InternationalTextType authority split

```text
state: visually + executable-confirmed mismatch
official XSD: Value xs:string / Language xs:language
official PDF + PR #30 candidate: IBIS-IP.string / IBIS-IP.language
run: 33169314332
evidence: EV-106
```

The two schema variants accept different XML instance shapes. Official VDV-301-2.3 bytes remain default authority; PR #30 is explicit candidate only.

### DMS-005 / DMS-006 / DMS-007 - DeviceManagementService Deep Read

V2.2 executable evidence:

```text
state: executable XSD declarations confirmed by EV-107
run: 33181833930
exact authority: official DMS V2.2 -> Common V2.2 -> Enumerations V2.2
```

Fresh byte-pinned DMS V2.2 evidence established:

```text
DMS-005:
  PDF response branch: DeviceManagementService.DeviceStatusInformationResponseData
  XSD response branch: DeviceManagementService.GetDeviceStatusInformationResponseData
  PDF-only spelling is not an XSD alias

DMS-006:
  PDF DeviceStatus table lists only DeviceStatusName + DeviceStatusFlag
  V2.2 XSD requires DeviceStatusName + DeviceStatusFlag + DeviceStatusImpact + DeviceStatusPriority
  all four have effective minOccurs=1

DMS-007:
  PDF InstallUpdate.UpdateTimestamp refers to GetUpdateStates
  exact XSD annotation refers to GetUpdateHistory + RetrieveUpdateState
  operation inventory contains GetUpdateHistory, not GetUpdateStates
```

V2.4 continuation:

```text
public PDF authority: official VDV DMS V2.4 writing
XSD comparison authority: candidate/integration only
EV-108 run: 33182963733 PASS

DMS-005 persists in the checked V2.4 PDF vs candidate/integration XSD.
DMS-006 is corrected/aligned for the checked V2.4 profile: name/flag required, impact/priority optional.
DMS-007 persists in the checked V2.4 PDF: GetUpdateStates wording vs GetUpdateHistory operation/XSD.
```

The V2.4 corrections are explanatory history only for older official profiles; they must not be back-applied to V2.1/V2.2.

### VLS-002 - VideoLiveService V2.0 LiveStreamData compositor

```text
state: executable-confirmed
PDF semantics: multi-field stream record
XSD: xs:choice among individual stream fields
run: 33111119723
```

One selected field validates; PDF-shaped multi-field records fail current official V2.0 XSD.

### VRS-003 - VideoRecordingService V2.0 state compositor

```text
state: executable-confirmed
PDF semantics: grouped state data
V2.0 XSD: xs:choice
V2.4 candidate control: grouped model accepted
run: 33111119723
```

The later candidate correction is explanatory evidence only and does not rewrite historical V2.0 validation.

### VDS-002 / VDS-003 / VDS-004 - VideoDisplayService V2.0 compositors

```text
state: executable-confirmed
run: 33111119723
```

Confirmed current-XSD behavior includes:

```text
ListViewCapabilitiesResponse multi-field view record rejected by xs:choice
SetVideoViewRequest ViewID + Timeout rejected by xs:choice
state + CurrentViewID response combinations rejected by xs:choice
State + OperationErrorMessage combination rejected where PDF presents combined semantics
```

### TSM-002 - TrainSetManagementService V2.2 operation-group/root mismatch

```text
state: executable-confirmed internal XSD mismatch
global root: GetTrainSetCompositionResponse
operation group still expects: GetTrainSetComposition
run: 33111644388
```

Handling: operation manifest/root mapping must override blind group enumeration.

### ARA-003 - AnalogRadioService V2.4 Transmitter cardinality

```text
state: executable-confirmed for candidate/integration profile only
PDF: 1:1
candidate XSD: 0:1
without Transmitter: valid
with Transmitter: valid
run: 33111831627
```

Authority guard: AnalogRadio V2.4 XSD is candidate material from open upstream PR #27, not an official release XSD.

## 3. Contextually resolved findings

### TSD-003 - TrainSetData V2.2 dual Subscribe-response typing

```text
state: resolved - OK with contextual resolver note
```

Same lexical response names legitimately serve two contexts:

```text
immediate Subscribe acknowledgement -> SubscribeResponseStructure
later subscription data event -> RetrieveTripRef/TripInformation response structure
```

Executable evidence run `33111644388` confirms both roles. This is a resolver-context requirement, not an automatic XSD defect.

### CIS-002 / SMS-001 - generic Subscribe/Unsubscribe modelling

```text
state: resolved - OK with note
```

General Conventions + Common provide generic subscription structures; omission of explicit service-prefixed Subscribe/Unsubscribe entries from local CIS/SMS groups is not sufficient evidence of a schema defect.

### SUB-001 - `TerminateSubscribe*` names in General-Conventions table

```text
state: documentation/XSD naming discrepancy
```

Checked Common history uses `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure`; no executable `TerminateSubscribe*` alias is created.

### DR3012-006 - historical TimeService document number

```text
state: historical_context_resolved
classification: pdf_cross_reference_error_candidate
confidence: very_high
```

Evidence chain:

```text
VDV 301-2 V1.0, 07/2016: SNTP implementation points to VDV 301-2-11.
VDV-Mitteilung 3002, 10/2016: TimeService is already listed as VDV-301-2-10.
VDV 301-2-11, 05/2017: VideoLiveService.
VDV 301-2-10, 02/2018: TimeService V1.0.
```

Handling: the old 301-2-11 reference is a wrong/stale document-number reference, not a resolver alias. TimeService routes to 301-2-10; 301-2-11 remains VideoLiveService.

## 4. Historically corrected / version-evolution findings

Important examples:

```text
TSI-001: TrainSetInformation V2.1 cannot model multiple coaches; V2.2 explicitly corrects with repeated SingleCoach.
TSM-001: TrainSetManagement V2.1 old composition response name; V2.2 history records correction.
TSD-001: V2.1 parameterized Retrieve subscriptions lack specialized schema structures; V2.2 introduces them.
DMS-003: ErrorMessage 10:* remains PDF/XSD-aligned through official V2.2; V2.4 0:* must not be back-applied.
DMS-004: InstallUpdate UpdateID/UpdateTimestamp/UpdateURL remain required through official V2.2; V2.4 optionality must not be back-applied.
DMS-006: V2.2 requires DeviceStatusImpact/Priority in XSD although its PDF table omits them; checked V2.4 PDF/candidate-XSD profile aligns with both optional.
DRDMS22-001: wrong V2.2 table reference is corrected in checked V2.4.
DRDMS22-002: V2.2 TOC numbering is corrected in checked V2.4.
CE-025: Reply-Path PDF naming persists through V2.3 and is corrected to ReplyPath in checked V2.4 documentation.
CE-026: BeaconPoint Desciption is the V2.3 XSD spelling; V2.4 XSD corrects BeaconPoint to Description.
VideoRecording V2.4 candidate clarifies/corrects the earlier state-response modelling but remains candidate authority.
```

Later correction evidence explains history; it does not alter earlier selected XSD profiles.

## 5. Candidate / provenance boundaries

### AnalogRadioService V2.4

```text
public V2.4 writing exists
no official VDV-301-2.4 GitHub release observed during audit
XSD in superbranch sourced from open upstream PR #27
```

Candidate profile must be explicitly selected.

### Common V2.3 PR #30

```text
official Common V2.3 root blob: 0d8926c4063c12de9a5e68b6f0addaab35a55dc1
candidate PR #30 blob:          456a7db179ce14bc3f04e2bc05e42e16545fb0c5
variant id: common-v2.3-upstream-pr30
```

Candidate selection is explicit; never latest-wins.

### DMS V2.4

```text
public VDV 301-2-0 V2.4 PDF: official public writing
repository IBIS-IP_DeviceManagementService_V2.4.xsd: candidate/integration
EV-108: candidate/integration declaration evidence only
```

Do not infer official-release XSD authority from the existence of the official public PDF.

### Historical public writings without exact strict XSD profile

Retained provenance gaps include service/version combinations where public documentation exists but no exact official-tag service XSD was confirmed, including relevant historical VideoLive/VideoRecording/VideoDisplay and CIS V1.1 cases recorded in their dedicated registers.

Rule:

```text
do not silently map an unresolved public version to a nearby XSD version
```

## 6. Intentionally non-XSD services

### TimeService V1.0

```text
classification: OK with note / non-XSD service by design
validation lane: protocol_discovery_profile
byte-pinned Deep Read: complete textually, needs_visual_review
latest RV-003 run: 33197358294 PASS
```

Fresh TimeService findings:

```text
DRTIME10-001: English foreword says VDV 301-2-1 describes TimeService; document/German text use 301-2-10.
DRTIME10-002: German text explicitly excludes cyclic transmission of current time; English omits that sentence.
DRTIME10-003: English version-history 'cd. 1' editorial cross-reference artifact.
```

Runtime guards:

```text
TimeService uses DNS-SD type _ibisip_udp._udp but must not be treated as a generic cyclic UDP time broadcaster.
Synchronization uses SNTP under the VDV-selected RFC 4330 profile.
sntp-server is required by the historical VDV profile and is an IP address.
timezone remains conservatively handled because no formal hard cardinality was established in the checked source chain.
No TimeService XML operations or XSD are synthesized.
```

### HTMLDisplayService V2.1/V2.2/V2.2a

```text
classification: OK with note / non-XSD HTTP/discovery profile by design
validation lane: discovery_http_profile
```

Version-specific DNS-SD endpoint semantics are retained; no HTML XSD is invented.

## 7. Runtime/protocol findings and guards

Deterministic RV phase:

```text
RV-001 HTTP/XML + Content-Type       run 33112730418 PASS
RV-002 DNS-SD/service discovery      run 33119080288 PASS
RV-003 TimeService/SNTP              run 33197358294 PASS (strengthened after fresh read)
RV-004 Video RTSP/RTP boundary       run 33119694991 PASS
```

Key guards:

```text
Missing Content-Type with a known body/media type is an external HTTP warning, not a fabricated explicit VDV hard failure.
DNS-SD is not automatically synonymous with mandatory mDNS.
HTMLDisplay V2.2/V2.2a uses TXT url as service-specific content endpoint semantics.
RFC 5905 does not silently replace the RFC 4330 profile explicitly selected by historical TimeService V1.0.
TimeService _ibisip_udp._udp discovery does not imply cyclic current-time multicast/broadcast.
RTSP 2.0 is not treated as a VDV requirement or a latest-wins drop-in replacement for RTSP 1.0.
Valid VideoLive XML metadata does not prove RTSP/RTP media availability.
```

## 8. Documentation-only finding themes

The detailed registers contain numerous high-confidence PDF issues, including:

```text
wrong service/part/section labels
copy/paste service names and copied structure tables
operation-name inconsistencies
case-sensitive enumeration spelling differences
cardinality table/XSD discrepancies
element-name mismatches
URI example inconsistencies
German/English General-Conventions divergences
historic document-number cross-reference errors
bilingual omissions
```

DMS-specific Deep Read history includes DRDMS22-001..004 and DRDMS24-001; TimeService Deep Read adds DRTIME10-001..003 and resolves DR3012-006.

These remain documentation notes except where a separate executable/runtime effect has been demonstrated.

## 9. Common/Enumerations detailed register status

The historic CE register contains more individual findings than this central index repeats.

Fresh byte-pinned Common V2.3 Deep Read opened:

```text
CE-021 LogMessage MessageBody PDF vs XSD Message
CE-022 ServiceIdentification ServiceName PDF vs XSD Service
CE-023 V2.3 duplicate/corrupt second NetexMode table
CE-024 UnsubscribeResponse Active PDF 0:1 vs XSD 1:1
CE-025 Reply-Path PDF vs XSD ReplyPath; documentation corrected by V2.4
CE-026 BeaconPoint Description PDF vs V2.3 XSD Desciption; XSD corrected by V2.4
```

It also strengthens CE-015, CE-017 and CE-019 from native PDF text, while visual page closure remains pending because the PDF screenshot backend returns cache-miss.

Historical correction:

```text
CE-010 / canalBarge:
The exact official VDV-301-2.2 Enumerations V2.2 XSD already contains canalBarge.
Therefore canalBarge is already part of the Common V2.3 dependency pool and was not introduced by V2.4.
CE-010 remains a PDF-vs-XSD omission, but its confirmed XSD history begins at least with V2.2.
```

Important rule:

```text
Do not interpret omission from this concise central file as closure or deletion of a detailed CE/service finding.
```

## 10. Detailed evidence sources

Primary current detailed sources include:

```text
AUDIT_SCOPE_MATRIX.md
AUDIT_HANDOFF_DELTA_EXECUTABLE_VALIDATION_24.md
AUDIT_HANDOFF_DELTA_RUNTIME_25.md
AUDIT_HANDOFF_DELTA_POST_SPLIT_EXECUTION_2026-08-28.md
AUDIT_HANDOFF_DELTA_DMS_V22_DEEP_READ_2026-08-28.md
AUDIT_HANDOFF_DELTA_DMS_V24_DEEP_READ_2026-08-28.md
AUDIT_HANDOFF_DELTA_TIME_V10_DEEP_READ_2026-08-28.md
deep_read/COMMON_V2.3.md
deep_read/DMS_V2.2.md
deep_read/DMS_V2.4.md
deep_read/TIME_V1.0.md
COMMON_FINDINGS_REGISTER_ADDENDUM.md
DEVICE_MANAGEMENT_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
24a_executable_validation_pcs_001.md
24b_executable_validation_ce_018.md
24c_executable_validation_video_compositors.md
24d_executable_validation_trainset.md
24e_executable_validation_analog_radio.md
24f_executable_validation_dms_v22.md
24g_executable_validation_dms_v24.md
25b_http_xml_content_type_profile.md
25c_dns_sd_service_discovery_profile.md
25d_time_service_sntp_profile.md
25e_video_rtsp_rtp_boundary.md
service-specific *_FINDINGS_REGISTER_ADDENDUM.md files
```

## 11. Official-facing action guard

No finding in this repository automatically authorizes an upstream change.

Before any official PR/comment/review:

```text
1. classify finding and authority
2. verify exact affected version(s)
3. run targeted executable/runtime regression where applicable
4. decide documentation-vs-schema/protocol correction
5. obtain explicit user approval for official-facing action
```

## COMMON V1.0 / public V1.x Deep Read closure

```text
source: byte-pinned official 05/2017 VDV 301-2-1 publication
exact XSD authority: Common V1.0 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
                     Enumerations V1.0 a9bea5bc73003ed91ded8519db06c32c4067831d
EV-117: run 33279461529 PASS
```

The source has internal document/data-definition revision `Version 1.1` while the
official executable XSD family remains the unchanged V1.0 import. Existing Common
finding IDs are reused where the Fresh Read rediscovered the same discrepancy.
Unique additions are `DRCOM10-001..DRCOM10-007`, covering revision-vs-XSD drift,
DataAcceptedResponse choice modelling, additional list/cardinality/model differences,
DoorCountingObjectClass lexemes and grouped editorial residue.

No V1.1 XSD authority is invented and no XSD is changed.
