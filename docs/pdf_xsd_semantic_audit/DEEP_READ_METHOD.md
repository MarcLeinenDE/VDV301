# VDV301 Deep Read Pass 2 – method

Status: active from 2026-08-28.

## Goal

Re-read every one of the 48 semantic public VDV301 document/version units independently from the original VDV PDF, then compare that fresh reading against existing extracted/OCR material and the existing first-pass audit.

The deep read is not a search for already-known findings. It is a fresh audit intended to confirm, refine, reject or add findings.

## Source reliability order

For each relevant statement/table/figure:

1. **Visible original PDF page** – highest authority for what the publication actually shows.
2. **Embedded PDF text layer / native extraction** – preferred for exact searchable text when it agrees with the visible page.
3. **Existing OCR material** – independent cross-check; useful when the text layer has bad ordering or missing glyphs.
4. **Existing first-pass audit notes** – comparison only, never the source for the fresh reading.

If sources disagree, return to the visible original. If the visible original itself is ambiguous, mark `visual_review_required` rather than guessing.

OCR is never automatically preferred over the original PDF. Native visual/text extraction is never automatically preferred when it contradicts the visible page.

## Reproducible PDF byte source rule

The visible original remains the highest semantic authority, but the exact bytes used for a reproducible deep read must come from the public source registry and local cache model defined in:

```text
audit_registry/pdf_source_registry_v0.1.json
docs/pdf_xsd_semantic_audit/PDF_SOURCE_CACHE_POLICY.md
```

Downloaded VDV PDF bytes are local-only under `local_sources/vdv_pdfs/` and must not be committed.

A physical PDF source is byte-level audit evidence only after its registry entry is pinned with SHA-256 and byte size and the local file verifies against both. An unpinned URL may be used to locate a publication, but it is not sufficient to promote a document to `exhaustive_read`.

If a previously pinned source no longer matches, record `SOURCE_CHANGED_SINCE_AUDIT`; do not silently replace the expected hash or carry the earlier visual review forward.

## Required checks per document

Where applicable, inspect:

- cover/version/date/language and normative-language note;
- foreword and version history;
- scope and architecture statements;
- every operation table;
- request/response assignment;
- service/structure/element/type names;
- cardinality (`0:1`, `1:1`, `0:*`, `1:*`);
- element ordering;
- XSD compositor semantics (`sequence`, `choice`, groups);
- enumeration values including exact case/spelling;
- constraints/patterns/min/max where documented;
- global roots and local operation groups;
- Get/Subscribe/Unsubscribe modelling;
- immediate response vs subscription callback/data-event context;
- examples and XML snippets;
- XSD screenshots printed in the PDF;
- diagrams/figures where they carry semantic or architectural meaning;
- HTTP method/version/status/header requirements;
- DNS-SD service type/TXT fields;
- SNTP/RTSP/RTP or other external protocol references;
- references to other VDV parts/RFCs/standards;
- differences to predecessor/successor versions;
- obvious copy/paste/heading/cross-reference defects;
- exact selected XSD dependency family and transitive Common/Enumerations dependencies.

## Comparison outcomes

For each existing or new issue use one of:

- `confirmed`
- `confirmed_executable`
- `new_finding`
- `finding_refined`
- `rejected_after_deep_read`
- `contextual_not_defect`
- `ocr_mismatch`
- `embedded_text_mismatch`
- `visual_review_required`
- `ok_with_note`

## Source-quality fields

Each document deep-read record must include:

- `original_pdf_visual_review`: yes/no/partial
- `embedded_text_quality`: good/mixed/poor/unavailable
- `existing_ocr_found`: yes/no
- `ocr_quality`: good/mixed/poor/not_applicable
- `preferred_reading_source`: original_visual / embedded_text_with_visual_confirmation / ocr_with_visual_confirmation
- `source_conflicts`: list

## Completion levels

- `not_started`
- `in_progress`
- `targeted_first_pass` – historical status only
- `table_level_deep_pass`
- `exhaustive_read`
- `needs_visual_review`

A document may be marked `exhaustive_read` only after all applicable chapters/tables/examples/figures have been considered and source conflicts are resolved or explicitly recorded.

## Finding-to-SDK rule

Findings must later be available to the SDK as explanatory audit knowledge, but they do not automatically override normative validation.

Example: if an official service XSD includes Enumerations V1.0 and a PDF uses a value only present in a later enumeration, validation remains against the exact official dependency family. The SDK may attach the relevant finding to explain the failure; it must not silently switch enumeration versions.
