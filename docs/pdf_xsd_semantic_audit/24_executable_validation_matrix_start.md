# Executable validation matrix - start

Status: technical execution phase prepared; no compile/sample result is claimed yet.

Purpose:

```text
Convert semantic/provenance audit decisions into reproducible executable evidence.
No row is called compiled or validated until a real compiler/sample run exists.
```

## Current superbranch model

The former complete `schema_pools/official/VDV-301-1.0/` mirror has been removed from the operational branch after detailed dedup review.

The superbranch now stores:

```text
one operational official XSD per required service/version packaging choice
shared Common/Enums once
legacy V1.0 operation-root metadata in schema_profiles/VDV-301-1.0-root-map.csv
```

Strict byte-for-byte VDV-301-1.0 release reconstruction remains available from the upstream official tag and recorded blob inventory, but is not the normal runtime layout.

## EV-001 - superbranch root-file compile sanity

Command:

```text
python tools/validate_xsd_pool.py --repo-root . --dms-v24-tests
```

Interpretation:

```text
Each root-level XSD is compiled with its declared dependencies.
DMS V2.4 sample tests remain candidate/integration tests.
A broad root compile does not change candidate authority labels.
```

## EV-002 - legacy V1.0 operation-root adapter compile

Command:

```text
python tools/validate_legacy_v1_roots.py --repo-root .
```

The tool reads:

```text
schema_profiles/VDV-301-1.0-root-map.csv
```

and creates temporary harness XSDs for:

```text
CustomerInformationService V1.0
DeviceManagementService V1.0
SystemDocumentationService V1.0
```

Each harness:

```text
includes the unchanged official service XSD
uses Common V1.0 + Enums V1.0 through that XSD
re-declares only the exact official root element/type pairs taken from IBIS_IP_V1.0.xsd
```

The harness is an integration validation adapter, not an official schema file.

## Evidence handling

The branch-scoped workflow `.github/workflows/schema-audit-validation.yml` records:

```text
root_pool_and_dms_v24.log
legacy_v1_root_adapters.log
validation_status.csv
```

GitHub Actions had not executed successfully at the previous checkpoint, so this document does not claim any passed technical test yet.

## Next after first real execution

```text
1. Record runner/Python/lxml versions and exact commands.
2. Mark EV-001/EV-002 passed only from actual logs.
3. Add representative positive/negative XML samples for legacy V1.0 roots.
4. Continue exact official V2.0/V2.1/V2.2 service-pool tests.
5. Keep candidate pool tests explicitly candidate-labelled.
```
