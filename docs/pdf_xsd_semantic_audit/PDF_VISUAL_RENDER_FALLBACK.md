# Reproducible visual PDF render fallback

Status: active from 2026-08-28.

## Problem addressed

The interactive PDF screenshot/render backend used during audit review can occasionally return a `cache miss` even though the official VDV PDF itself is reachable and its byte pin is valid. This state is a rendering-service/cache failure, not evidence that the VDV source PDF is missing, corrupt or semantically unreadable.

A `cache miss` must therefore never be recorded as a VDV document defect.

## Audit rule

Visual review must prefer the visible original PDF page. When the interactive screenshot backend cannot render a required page, the audit falls back to rendering the **same byte-pinned PDF source** independently.

The fallback implementation is:

```text
tools/render_vdv_pdf_pages.py
```

It resolves the source through:

```text
audit_registry/pdf_source_registry_v0.1.json
audit_registry/pdf_source_pins_v0.1.json
```

and refuses to render unless the downloaded/local PDF matches both the pinned SHA-256 and byte size.

A mismatch terminates with:

```text
SOURCE_CHANGED_SINCE_AUDIT
```

## Example

```text
python -m pip install pymupdf
python tools/render_vdv_pdf_pages.py \
  --source-id VLS_V1.0 \
  --pages 1,4,39-40 \
  --dpi 180 \
  --out-dir local_sources/vdv_pdf_renders/VLS_V1.0
```

The output consists of PNG page renders plus `render_manifest.json` containing:

```text
source_id
official_url
source SHA-256
source byte size
source pin evidence run id
PDF page count
render engine + version
DPI
rendered page numbers
per-PNG SHA-256 and byte size
```

## Repository/publication boundary

VDV PDF bytes and rendered page images are review artifacts and are not committed to the public repository. They belong under ignored local storage or short-lived CI artifacts.

The repository may retain only the tooling, hashes, page numbers, render metadata and resulting audit conclusions.

## What this solves

This does **not** prevent the external screenshot service from returning `cache miss`; that service is outside the repository's control.

It prevents that failure from blocking or weakening the audit by providing a deterministic second rendering path tied to the exact source bytes already used for the Deep Read.

A document may still remain `needs_visual_review` if neither the interactive renderer nor the pinned-byte fallback can produce a usable visible page. It may be promoted based on fallback rendering only after the rendered page was actually inspected.
