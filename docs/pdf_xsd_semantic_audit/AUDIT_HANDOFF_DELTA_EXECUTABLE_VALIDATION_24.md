# Audit handoff delta - executable validation phase / block 24

Status: block 24 closed; use together with the current `AUDIT_SCOPE_MATRIX.md` and prior semantic/provenance audit deltas.

## Phase boundary

The planned executable XSD evidence sequence is complete. The next active phase is block 25 runtime/protocol validation.

No official-facing branch, PR, issue, comment or merge was changed during this phase. Fork `master` remains untouched. No XSD content was changed to make a test pass.

## Current validation model

```text
XSD = strict executable XML authority for the exact selected schema family.
PDF/XSD discrepancies = findings/provider notes, not silent XSD rewrites.
Candidate schemas remain candidate/integration only.
Operation support/root selection cannot be derived solely from an XSD operation group.
Response lexical name may be insufficient where the specification defines context-dependent response semantics.
```

## Executed evidence

### Baseline / EV-001 + EV-002

```text
run: 33109011670
head: 8dac3ec3a9e6fbebec2b3c3d4f381d69cfc07066
46 root XSDs compile PASS
DMS V2.4 targeted samples 6/6 PASS
legacy V1.0 root adapters PASS:
- CustomerInformationService
- DeviceManagementService
- SystemDocumentationService
```

### EV-101 / PCS-001

```text
run: 33109367265
head: 3ea0215bca353697466e90f8be6af3e3087810bd
exact PCS V2.1 -> Common V1.0 -> Enums V1.0 compile PASS
DataNotValid valid
OperationNotSupported invalid in exact pool
OperationNotSupported valid in Enums V2.1 explanatory control
result: dependency/value-set discrepancy executable-confirmed
```

### EV-102 / CE-018

```text
run: 33109768872
head: 2298f1297e9d2b00aacbf244f39f6c73587f713e
Common V1.0/V2.0/V2.1/V2.2/V2.3/V2.4 all accept:
- zero ServiceIdentificationWithState items
- one ServiceIdentificationWithState item
result: XSD 0:* behavior executable-confirmed
```

### EV-103 / video compositor findings

```text
run: 33111119723
head: d4ffe09067cb38bf7f78ba295e029902078ed18d
VLS-002 executable-confirmed
VRS-003 executable-confirmed
VDS-002 executable-confirmed
VDS-003 executable-confirmed
VDS-004 executable-confirmed
VRS V2.4 candidate grouped-state control PASS; explanatory only
```

### EV-104 / TrainSet

```text
run: 33111644388
head: a9e9d7d92bf80f2f013338f0cb8ded4aff4dcf88
TSM-002 executable-confirmed:
  corrected global root vs stale operation-group member
TSD-003 resolved:
  global Subscribe response = subscription data-event type
  operation-group response = generic immediate acknowledgement type
  classification -> contextual resolver requirement / OK with note
```

### EV-105 / AnalogRadio

```text
run: 33111831627
head: 86e3592968f24cfa59e05ace625f64886ca3ae89
candidate AnalogRadio V2.4 compile PASS
Transmitter declaration 0:1
SendTelegram without Transmitter valid
SendTelegram with Transmitter valid
result: ARA-003 executable-confirmed for candidate/integration profile only
```

## Added executable tooling

```text
tools/validate_xsd_pool.py
tools/validate_legacy_v1_roots.py
tools/validate_pcs_v21_operation_not_supported.py
tools/validate_ce018_service_identification_with_state_list.py
tools/validate_video_v20_compositors.py
tools/validate_trainset_ev104.py
tools/validate_analog_radio_ev105.py
```

## Evidence documents

```text
24_executable_validation_matrix_start.md
24a_executable_validation_pcs_001.md
24b_executable_validation_ce_018.md
24c_executable_validation_video_compositors.md
24d_executable_validation_trainset.md
24e_executable_validation_analog_radio.md
```

## GitHub Actions behavior

The branch workflow `.github/workflows/schema-audit-validation.yml` is `workflow_dispatch` only at phase close. Normal audit commits do not trigger it.

During evidence collection a temporary push trigger was used for one-shot execution, with status capture designed not to produce failure notifications for test-harness mismatches. It was restored to manual-only after each run.

## Next active block

```text
Block 25 - runtime/protocol validation profiles
25a authority/source matrix
25b HTTP/XML and Content-Type
25c DNS-SD/service discovery
25d TimeService/SNTP
25e Video RTSP/RTP boundary
```

Runtime checks must classify authority as one of:

```text
VDV-specific normative requirement
external normative standard incorporated/referenced/relied upon
implementation diagnostic heuristic/best practice
```

Do not blur these categories in SDK/provider output.
