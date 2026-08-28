# Audit handoff delta – PDF source cache / reproducible PDF bytes

Date: 2026-08-28  
Branch: `dev/schema-integration`  
Base HEAD before this block: `fe406000793993c9258267e5a022739100fd4aaa`

## Purpose

Introduce a reproducible local-PDF source layer for Deep Read Pass 2 without redistributing VDV PDF bytes through the public repository.

This block is infrastructure/provenance only. It does not change any XSD and does not close any semantic finding by itself.

## Added

```text
audit_registry/pdf_source_registry_v0.1.json
tools/fetch_vdv_pdf_sources.py
docs/pdf_xsd_semantic_audit/PDF_SOURCE_CACHE_POLICY.md
.gitignore
```

The registry contains all 50 physical VDV 301 PDF links currently exposed by the official VDV IP-KOM-ÖV catalog and maps them to the existing 48 semantic document units.

Two historical semantic units have separate German and English physical PDFs:

```text
VDV301-1_V1.0_DE
VDV301-2_V1.0_DE
```

Therefore:

```text
physical PDF sources = 50
semantic document units = 48
```

## Byte-pinning state

At commit time the public registry contains the official source URLs but no guessed hashes:

```text
pdf_sources_byte_pinned = 0
pin_state = unpinned
deep_read_source_ready = false
```

This is deliberate. A URL alone is not promoted to byte-level evidence.

The first exact SHA-256 and byte-size pin must be created from a local fetch with explicit bootstrap mode:

```text
python tools/fetch_vdv_pdf_sources.py --source-id VDV301-2_GC_V2.3 --bootstrap-pins
python tools/fetch_vdv_pdf_sources.py --source-id COMMON_V2.3 --bootstrap-pins
```

After review, only the resulting registry metadata is committed. Downloaded PDF bytes remain under:

```text
local_sources/vdv_pdfs/
```

and are ignored by Git.

## Source-change guard

For already pinned sources the fetcher compares both SHA-256 and byte size.

Mismatch state:

```text
SOURCE_CHANGED_SINCE_AUDIT
```

An existing pin is never automatically replaced, including when `--bootstrap-pins` is supplied. Re-pinning requires an explicit audit decision.

The fetcher also verifies the `%PDF-` file signature before accepting a downloaded file.

## Deep-read rule change

`DEEP_READ_METHOD.md` now requires pinned local PDF bytes for reproducible original-page evidence.

An unpinned public URL may locate a source, but it is not sufficient to promote a document to:

```text
exhaustive_read
```

The existing textual Deep Read results that still need visible-page confirmation therefore remain `needs_visual_review`.

## Current active source targets

Immediate local pinning order:

```text
1. VDV301-2_GC_V2.3
2. COMMON_V2.3
```

Reason:

```text
VDV301-2_GC_V2.3 = current Deep Read document
COMMON_V2.3 = required later for full visual verification of CE-020
```

## Superbranch / executable validation status

Unchanged by this infrastructure block:

```text
root_xsd_count_current = 50
root_xsd_count_last_executed = 49
```

The post-authority-split 50-root state is still not claimed as executed successfully.

Required next executable step remains:

```text
re-run full root/profile validation
then run an isolated common-v2.3-upstream-pr30 candidate-overlay check
```

No workflow trigger was changed.

## Authority boundaries

Unchanged:

```text
selected exact XSD family/variant = executable XML authority
PDF/XSD differences = audit knowledge, not silent schema rewrite
official Common V2.3 = default
PR #30 Common V2.3 = explicit candidate overlay only
no latest-wins
```

No PR, upstream branch, official branch or master branch was modified by this block.
