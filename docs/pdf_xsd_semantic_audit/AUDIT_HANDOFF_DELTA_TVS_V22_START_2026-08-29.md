# Audit handoff delta - TicketValidationService V2.2 start

Date: 2026-08-29
Canonical branch: `dev/schema-integration`

## Start state

`TVS_V2.1` was formally closed under the current Evidence Gate in commit:

```text
4d40323c82cd706e7716552f0156cdbc6a9385cc
Deep-read TicketValidationService V2.1 and confirm EV-112
```

The next independent document-first block is `TVS_V2.2`.

## Official PDF pin

Official source:

```text
https://www.vdv.de/301-2-16-sdes-v2-2-ticketvalidation.pdfx
```

Pin evidence:

```text
source_id: TVS_V2.2
sha256: 1915a1b12c24386e9a8ab5638fd88af6a442b5e42586b7b2d48f03e9a4205083
size: 785931 bytes
pinned_at_utc: 2026-08-29T13:31:54Z
run: 33255245725
job: 99107691622
result: PASS
```

The temporary source-pin workflow is removed from the permanent branch tip after the successful run.

## Exact XSD authority established independently

Official upstream tag:

```text
VDV-301-2.2
```

Exact family:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
  5a4be2b2ba66860f035777ec0458dba0790880e1

IBIS-IP_common_V2.2.xsd
  468fee6d177e7185dbcd5d3f90cfb114e29e01ae

IBIS-IP_Enumerations_V2.2.xsd
  2a23b512379b18e8f122ac1272cef8229fb86283
```

The service XSD explicitly includes Common V2.2 and Enumerations V2.2. The three copies on `dev/schema-integration` are blob-identical to the official `VDV-301-2.2` tag.

Authority rule:

```text
TVS V2.2 -> Common V2.2 -> Enumerations V2.2
```

This is a version-aligned official family. Do not replace it with V2.3/V2.4 dependencies.

## Fresh-read isolation rule

Historical TicketValidation findings and the V2.1 correction history must not be used to seed the V2.2 Fresh Read.

Required order:

```text
1. read the byte-pinned official V2.2 writing independently
2. inspect material visible table/layout context from the exact pinned bytes
3. compare fresh observations with the exact V2.2 authority
4. actively attempt to disprove each candidate
5. executable-confirm material XML behavior where practical
6. only then reopen historical V2.2 TicketValidation findings and reconcile them
```

No XSD modification, PR/comment/merge or remediation action is authorized by this start block.
