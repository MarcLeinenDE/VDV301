# VDV 301 PDF source cache and byte-pinning policy

Status: active from 2026-08-28.

## Purpose

The PDF/XSD deep read must be reproducible against the exact VDV PDF bytes that were reviewed. The public repository therefore stores source metadata and cryptographic pins, but **does not store or redistribute the VDV PDF files themselves**.

The official public catalog remains:

```text
https://www.vdv.de/ip-kom-oev.aspx
```

Machine-readable source metadata is stored in:

```text
audit_registry/pdf_source_registry_v0.1.json
```

Local PDF bytes are stored only in:

```text
local_sources/vdv_pdfs/
```

That path is excluded from Git.

## Source states

Each physical PDF source has its own `source_id`. Two historical publications have separate German and English physical PDFs but map to one semantic audit unit; therefore the source registry contains 50 physical sources for 48 semantic document units.

A source is audit-ready only when all of the following are true:

```text
expected_sha256 != null
expected_size_bytes != null
pin_state == "pinned"
deep_read_source_ready == true
```

An unpinned URL is discovery metadata, not byte-level evidence.

## Initial pinning

Use the fetcher only from a local working copy:

```text
python tools/fetch_vdv_pdf_sources.py --source-id VDV301-2_GC_V2.3 --bootstrap-pins
python tools/fetch_vdv_pdf_sources.py --source-id COMMON_V2.3 --bootstrap-pins
```

To pin the complete public catalog:

```text
python tools/fetch_vdv_pdf_sources.py --all --bootstrap-pins
```

`--bootstrap-pins` is intentionally explicit. It establishes the first SHA-256 and byte-size pin for an unpinned source and updates the local registry file. The resulting registry change may then be reviewed and committed; the downloaded PDF remains local and ignored.

## Normal verification

After a source is pinned, normal use does not need the bootstrap flag:

```text
python tools/fetch_vdv_pdf_sources.py --source-id VDV301-2_GC_V2.3
python tools/fetch_vdv_pdf_sources.py --source-id VDV301-2_GC_V2.3 --check-only
```

Existing cache bytes are checked before use. Missing pinned files are downloaded from the registered official URL and verified before they are moved into the cache.

The fetcher additionally requires the `%PDF-` file signature so that an HTML error page cannot accidentally be accepted as evidence.

## Source changed since audit

If a pinned source downloads or exists locally with a different SHA-256 or byte size, the required state is:

```text
SOURCE_CHANGED_SINCE_AUDIT
```

The expected pin must **not** be replaced automatically.

Required response:

1. preserve the old registry pin in Git history;
2. verify that the VDV catalog still identifies the same publication/version;
3. determine whether only container/metadata bytes changed or visible/normative content changed;
4. create an explicit new audit decision before re-pinning;
5. repeat affected visual/text deep-read checks when content may have changed.

A hash must never be changed merely to make a fetch or validation step pass.

## Deep-read integration

`DEEP_READ_METHOD.md` remains the semantic method authority. For a visible PDF page to count as reproducible original-source evidence, the PDF must be tied to a pinned registry entry.

Until the currently completed textual deep-read documents are re-opened from pinned local PDF bytes and visually checked, they remain `needs_visual_review` rather than `exhaustive_read`.

## Repository boundary

The public repository may contain:

```text
official URLs
document/source identifiers
SHA-256 values
byte sizes
retrieval/pinning timestamps
audit and visual-review state
fetch/verification tooling
```

It must not contain the downloaded VDV PDF bytes under `local_sources/` or elsewhere.

This project policy is intentionally conservative: public availability at the VDV source site is treated as permission to fetch from the official source, not as permission for this repository to republish the documents.
