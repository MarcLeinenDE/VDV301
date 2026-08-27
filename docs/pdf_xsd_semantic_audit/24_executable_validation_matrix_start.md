# Executable validation matrix - technical baseline

Status: initial executable baseline completed successfully; targeted finding-specific validation is next.

Purpose:

```text
Convert semantic/provenance audit decisions into reproducible executable evidence.
No row is called compiled or validated until a real compiler/sample run exists.
```

## Current superbranch model

The former complete `schema_pools/official/VDV-301-1.0/` mirror has been removed from the operational branch after detailed dedup review.

The superbranch stores:

```text
one operational official XSD per required service/version packaging choice
shared Common/Enums once
legacy V1.0 operation-root metadata in schema_profiles/VDV-301-1.0-root-map.csv
```

Strict byte-for-byte VDV-301-1.0 release reconstruction remains available from the upstream official tag and recorded blob inventory, but is not the normal runtime layout.

## Executed baseline evidence

Successful controlled GitHub Actions run:

```text
workflow: schema-audit-validation
run number: 4
run id: 33109011670
head SHA tested: 8dac3ec3a9e6fbebec2b3c3d4f381d69cfc07066
runner OS: Ubuntu 24.04.4
Python: 3.12.14
lxml: 6.1.2
root_status: 0
legacy_status: 0
```

The branch was subsequently changed only to restore the workflow trigger to manual-only; no XSD or validator-content change occurred in that trigger-restoration commit.

## EV-001 - superbranch root-file compile sanity

Executed command:

```text
python tools/validate_xsd_pool.py --repo-root . --dms-v24-tests
```

Result:

```text
PASS
46 root-level XSD files compiled successfully with lxml.etree.XMLSchema.
No XSD compile error was reported.
```

Important authority note:

```text
The repository root is an integration inventory containing both official and candidate/integration XSDs.
A successful compile proves syntactic/schema dependency consistency of the selected files as stored.
It does NOT reclassify candidate XSDs as official material.
```

### DMS V2.4 targeted regression samples

All six current cases passed after correcting the test XML wrappers to match the Common scalar-wrapper model:

```text
device-error-messages-empty-is-valid                  PASS
subdevice-error-messages-empty-is-valid               PASS
device-status-impact-priority-omitted-is-valid        PASS
device-status-flag-still-required-is-invalid          PASS
install-update-request-empty-is-valid                 PASS
update-state-data-timestamp-still-required-is-invalid PASS
```

The initial failed runs were caused by invalid test samples that placed scalar text directly in wrapper elements such as `TimeStamp`, `SubdeviceName`, `DeviceStatusName` and `DeviceStatusFlag`. The XSD compiler itself already passed those runs. The samples were corrected by using their required `<Value>` children. No XSD was modified.

DMS V2.4 remains candidate/integration authority.

## EV-002 - legacy V1.0 operation-root adapter compile

Executed command:

```text
python tools/validate_legacy_v1_roots.py --repo-root .
```

Result:

```text
PASS
CustomerInformationService V1.0: 10 mapped root declarations
DeviceManagementService V1.0: 10 mapped root declarations
SystemDocumentationService V1.0: 5 mapped root declarations
```

The tool reads:

```text
schema_profiles/VDV-301-1.0-root-map.csv
```

and creates temporary harness XSDs. Each harness:

```text
includes the unchanged official service XSD
uses Common V1.0 + Enums V1.0 through that XSD
re-declares only the exact official root element/type pairs taken from IBIS_IP_V1.0.xsd provenance
```

The harness is an integration validation adapter, not an official VDV schema file.

## Workflow behaviour

`.github/workflows/schema-audit-validation.yml` is now deliberately:

```text
workflow_dispatch only
```

It no longer runs on every push to `dev/schema-integration`, preventing audit commits from generating repeated failed-run notifications.

## Block 24 next phase - targeted finding validation

The broad compile baseline is complete. The audit now returns to the planned finding-driven technical validation sequence.

Priority order:

### EV-101 - PCS-001 OperationNotSupported dependency/value-set mismatch

Goal:

```text
Compile the exact PassengerCountingService V2.1 dependency route.
Create a response sample using OperationNotSupported.
Prove that the exact selected Enums V1.0 pool rejects that value.
Run a control sample against the V2.1 enum family only as explanatory comparison, not as an alternative production route.
```

Expected classification outcome:

```text
confirm or revise PCS-001 from structural evidence to executable evidence
```

### EV-102 - CE-018 ServiceIdentificationWithStateList cardinality

Goal:

```text
Build positive zero-item and one-item samples against exact Common V1.0/V2.1/V2.2/V2.3/V2.4 families as applicable.
Prove XSD `minOccurs=0` behaviour against PDF `1:*` wording.
```

### EV-103 - video-service xs:choice modelling candidates

Services/findings:

```text
VideoLiveService V2.0 / VLS-002
VideoRecordingService V2.0 / VRS-003
VideoDisplayService V2.0 / VDS compositor findings
```

Goal:

```text
Create one-field samples that validate.
Create PDF-shaped multi-field samples expected to fail under the current XSD choice compositor.
Keep each service/finding separate in the evidence matrix.
```

### EV-104 - TrainSet operation/root modelling

Targets:

```text
TSM-002 operation-group name vs global GetTrainSetCompositionResponse
TSD-003 immediate Subscribe acknowledgement vs callback payload root/type model
```

Goal:

```text
Compile exact V2.2 pools and create root-specific samples to determine what the executable schema actually permits.
Do not infer HTTP/runtime behaviour beyond what schema/root tests prove.
```

### EV-105 - AnalogRadioService V2.4 candidate cardinality

Target:

```text
ARA-003 Transmitter PDF 1:1 vs candidate XSD minOccurs=0
```

Goal:

```text
Candidate-labelled positive sample without Transmitter and positive sample with Transmitter.
```

## Later runtime layers

After XML/XSD finding validation:

```text
subscription callback + heartbeat runtime trace
DNS-SD discovery profile checks
HTTP Content-Type and status semantics with authority attributed to General Conventions / HTTP standards
SNTP TimeService runtime checks
RTSP/RTP media checks for video services
```

These are intentionally separate from XSD validation.

## Guardrails

```text
No XSD is changed merely because a sample proves a PDF/XSD discrepancy.
Exact service/version dependency routes remain authoritative for validation.
Candidate XSD tests remain candidate-labelled.
No latest-wins dependency substitution.
No PR/comment/merge action without explicit approval.
```

## Immediate next task

```text
24a_executable_validation_pcs_001.md
EV-101: PassengerCountingService V2.1 OperationNotSupported
```
