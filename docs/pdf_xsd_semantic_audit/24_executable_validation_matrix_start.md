# Executable validation matrix - start

Status: technical execution phase started.

Parent audit commit:

```text
ab495095a353dabb6239c3ebd3a37f5fd1853511
```

Purpose:

```text
Convert the historical semantic/provenance audit into reproducible executable evidence.
No row is called compiled or validated until a real compiler/sample run exists.
```

## Execution environment

The interactive audit container cannot resolve github.com, so it cannot clone the repository directly.

To make validation reproducible against the actual branch contents, this block adds a branch-scoped GitHub Actions workflow:

```text
.github/workflows/schema-audit-validation.yml
```

It runs only on `dev/schema-integration` pushes or explicit workflow dispatch and has read-only contents permission.

## Initial checks

### EV-001 - exact original VDV-301-1.0 aggregate pool compile

Target:

```text
schema_pools/official/VDV-301-1.0/
```

Command:

```text
python tools/validate_xsd_pool.py --repo-root schema_pools/official/VDV-301-1.0
```

Authority:

```text
official release pool only
pool_id official:VDV-301-1.0
```

Expected evidence:

```text
all twelve original XSDs compiled by lxml XMLSchema
aggregate IBIS_IP_V1.0.xsd resolves only relative includes from the isolated official pool
```

### EV-002 - current integration root sanity compile + DMS V2.4 candidate samples

Command:

```text
python tools/validate_xsd_pool.py --repo-root . --dms-v24-tests
```

Authority warning:

```text
The repository root is an integration inventory containing official historical/current and candidate files.
A successful broad compile is only a syntax/dependency sanity result per root file; it does not make candidate files official and does not replace exact resolver-pool classification.
```

The DMS V2.4 sample harness remains candidate/integration validation because DMS V2.4 itself is candidate material.

## Evidence handling

Workflow artifact:

```text
schema-audit-validation-results
```

Expected files:

```text
official_vdv_301_1_0.log
root_pool_and_dms_v24.log
validation_status.csv
```

## Next after first execution

```text
1. Record workflow run ID, runner/Python/lxml context and exact pass/fail results.
2. If EV-001 passes, mark the original V1.0 aggregate family compiled.
3. If any row fails, keep the error verbatim enough for diagnosis; do not silently alter schemas.
4. Expand into exact official V2.0/V2.1/V2.2 service-pool harnesses.
5. Add targeted positive/negative XML samples for high-impact findings.
```
