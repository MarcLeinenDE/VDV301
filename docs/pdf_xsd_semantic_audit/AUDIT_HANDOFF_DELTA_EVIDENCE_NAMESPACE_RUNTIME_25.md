# Audit handoff delta - evidence namespace and runtime phase

Status: current naming policy established; runtime phase active.

## Evidence namespaces

```text
EV-* = executable XML/XSD/schema-family evidence only
RV-* = runtime/protocol evidence only
```

Historical XSD evidence remains:

```text
EV-001
EV-002
EV-101
EV-102
EV-103
EV-104
EV-105
```

Do not describe this as a continuous `EV-001 through EV-105` sequence. EV-003..EV-100 were never defined.

Runtime mapping:

```text
Block 25a -> source/authority matrix, no standalone evidence ID
Block 25b -> RV-001 HTTP/XML/Content-Type
Block 25c -> RV-002 DNS-SD/service discovery
Block 25d -> RV-003 TimeService/SNTP
Block 25e -> RV-004 RTSP/RTP boundary
```

See `EVIDENCE_ID_POLICY.md`.

## RV-001 status

Historical controlled run:

```text
run 33112730418
head 9584a07e5abd70dd34d122fbbb230dd03bb6e83b
result PASS
```

The historical tool filename `tools/validate_http_runtime_ev25b.py` is retained only so the prior run remains traceable. Its evidence ID is now formally `RV-001`.

The workflow output name for future executions has been changed to `rv_001_http_runtime`.

## Current active task

```text
RV-002 / block 25c DNS-SD/service discovery classifier
```

Existing implementation starter:

```text
tools/runtime_discovery_profile.py
```

Next executable harness should use an RV-prefixed identity, for example:

```text
tools/validate_discovery_runtime_rv002.py
```

## Guard

```text
Do not rename historical run IDs or XSD EV documents.
Do not use EV-* for runtime/protocol evidence going forward.
Rule IDs such as HTTP-X01 or DNS-X02 remain separate from evidence IDs.
```
