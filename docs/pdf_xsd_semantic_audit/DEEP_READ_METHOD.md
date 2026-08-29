# VDV301 Deep Read Pass 2 – method

Status: active from 2026-08-28; choice-notation guard corrected 2026-08-29.

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

## Reproducible visual-render fallback

The interactive PDF screenshot backend is a convenience path, not a source authority. If it returns `cache miss` or another rendering-backend error while the byte-pinned PDF remains valid, do **not** classify that as a document/source failure.

Use the independent fallback defined in:

```text
docs/pdf_xsd_semantic_audit/PDF_VISUAL_RENDER_FALLBACK.md
tools/render_vdv_pdf_pages.py
```

The fallback must:

```text
1. resolve the same registered source_id;
2. verify %PDF- signature;
3. verify the pinned SHA-256 and byte size before rendering;
4. abort with SOURCE_CHANGED_SINCE_AUDIT on mismatch;
5. render only from those verified bytes;
6. record page number, DPI, render engine/version and per-image hashes;
7. keep PDF/page-image bytes outside the public repository;
8. count as visual evidence only after the rendered page was actually inspected.
```

A successful pinned-byte render is a visible rendering of the same original source bytes and may be used to close layout-sensitive findings even when the interactive screenshot backend fails. The renderer itself does not promote a finding: actual page inspection is still required.

Targeted rendered pages do not by themselves make a document `exhaustive_read`; all applicable chapters/tables/examples/figures must still be considered according to the completion rules below.

## VDV table-notation guard: multiplicity vs XML choice

Do not interpret a leading minus sign as a negative minimum cardinality.

VDV 301-2 V2.0 section 6.1.3.3 `Multiplizität & Choice (Min:Max)` defines:

```text
0:1  optional single element
1:1  mandatory single element
0:*  optional repeated element

prefixed '-'  XML-choice marker
-1:1         mandatory choice example
-0:1         optional choice example
```

For documented choices, a lower-case letter (`a`, `b`, ...) before the element name identifies the listed alternatives.

Audit rules:

```text
- `-1:1` is valid VDV notation by itself and must never be classified as an invalid/negative cardinality.
- Evaluate the minus marker together with lower-case choice labels, surrounding rows and the selected XSD compositor.
- If the minus marker is shown without the documented alternative labels, or appears on isolated enum-valued rows with no visible peer alternative, classify only the application/presentation as potentially anomalous; do not call the cardinality itself invalid.
- A PDF/XSD compositor finding must be based on the complete visible grouping, not merely on the presence or absence of a minus sign.
- Historical correction overlay: `AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md`.
```

## Required checks per document

Where applicable, inspect:

- cover/version/date/language and normative-language note;
- foreword and version history;
- scope and architecture statements;
- every operation table;
- request/response assignment;
- service/structure/element/type names;
- cardinality (`0:1`, `1:1`, `0:*`, `1:*`) **and VDV choice notation (`-1:1`, `-0:1`, other leading-minus Min:Max forms plus a/b/... labels)**;
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

A successful independently rendered page from the exact byte-pinned source counts as `original_visual` evidence for that page when its source pin and render manifest are retained in the audit trail.

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
