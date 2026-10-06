# Source-locator review — CIS-004 — 2026-10-06

Status: **structurally complete / visible-body verified / executable mismatch preserved**.

## Finding

CIS-004 is a confirmed PDF defect in CustomerInformationService V2.0, V2.2 and V2.3.

PDF detail label:
`CustomerInformationService.RetrievePartialStopRequest`

Selected official XSD root:
`CustomerInformationService.RetrievePartialStopSequenceRequest`

The selected XSD remains normative.

## Visible PDF body

Exact byte-pinned CIS PDFs from evidence artifact `9885887536` were visually checked after the live PDF screenshots cache-missed.

- **V2.0**, printed page **20**, `1.28 Data Structure of RetrievePartialStopSequence Operation / 1.28.1 Request`, visible **Table 18** uses `CustomerInformationService.RetrievePartialStopRequest`.
- **V2.2**, printed page **21**, `1.29 ... / 1.29.1 Request`, visible **Table 18** uses the same shortened request name.
- **V2.3**, printed page **21**, same visible defect.

For all three versions, visible **Table 1** on printed page **12** names the operation `RetrievePartialStopSequence` and assigns `CustomerInformationService.RetrievePartialStopSequenceRequestStructure`. This is an internal negative control against treating the shortened detail label as intentional.

## Exact XSD authority

- V2.0: `VDVde/VDV301@VDV-301-2.0`, blob `fa8f0a51ad5f612660c9532c8557ad1ca473a908`; valid global request root at line 151, request structure at line 152.
- V2.2: `VDVde/VDV301@VDV-301-2.2`, blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`; valid root at line 163, structure at line 164.
- V2.3: `VDVde/VDV301@VDV-301-2.3`, blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`; valid root at line 163, structure at line 164.

No `CustomerInformationService.RetrievePartialStopRequest` global element exists in these selected schemas.

## Executable evidence

EV-125, run `33744039627`, already proves the root boundary on all three official routes:

- full XSD root → valid;
- shortened PDF root → invalid.

## Active disproof

Checked and rejected:

1. shortened detail label as intentional alias — no matching global XSD element exists;
2. alternate operation name — the same PDFs use `RetrievePartialStopSequence` and the full request-structure name in Table 1;
3. cross-version substitution — every lane is checked against its exact official release tag.

Classification remains **confirmed PDF defect**.

## SDK consequence

Existing runtime mapping remains correct: only decorate an already **INVALID** selected-XSD result when the submitted global request root exactly matches the PDF-short form. Never create a compatibility alias and never override the selected-XSD result.

No XSD bytes, semantic scope or runtime mapping were changed.
