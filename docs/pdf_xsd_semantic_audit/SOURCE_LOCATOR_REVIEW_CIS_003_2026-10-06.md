# Source-locator review — CIS-003 — 2026-10-06

Status: **structurally complete / visible-body verified / executable mismatch preserved**.

## Finding

CIS-003 is a confirmed PDF defect in CustomerInformationService V2.0, V2.2 and V2.3.

PDF detail label:
`CustomerInformationService.GetCurrentConnectionResponse`

Selected official XSD root:
`CustomerInformationService.GetCurrentConnectionInformationResponse`

The selected XSD remains normative.

## Visible PDF body

Exact byte-pinned CIS PDFs from evidence artifact `9885887536` were visually checked.

- **V2.0**, printed page **15**, `1.10.2 Response`, Table 6 visibly uses `CustomerInformationService.GetCurrentConnectionResponse`. The operation overview on page **10** uses `GetCurrentConnectionInformation` and `CustomerInformationService.GetCurrentConnectionInformationResponseStructure`.
- **V2.2**, printed page **16**, `1.11.2 Response`, Table 6 visibly uses the same shortened response name. The operation overview across pages **10–11** uses the full `GetCurrentConnectionInformationResponseStructure` name.
- **V2.3**, printed page **16**, same visible defect; the overview across pages **10–11** again uses the full response-structure name.

This internal contrast disproves an intentional alternate naming convention.

## Exact XSD authority

- V2.0: `VDVde/VDV301@VDV-301-2.0`, blob `fa8f0a51ad5f612660c9532c8557ad1ca473a908`; valid global root at line 59, response structure at line 60.
- V2.2: `VDVde/VDV301@VDV-301-2.2`, blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`; valid root at line 71, structure at line 72.
- V2.3: `VDVde/VDV301@VDV-301-2.3`, blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`; valid root at line 71, structure at line 72.

No `CustomerInformationService.GetCurrentConnectionResponse` global element exists in these selected schemas.

## Executable evidence

EV-125, run `33744039627`, already proves on all three official routes:

- full XSD root → valid;
- shortened PDF root → invalid.

## Active disproof

Checked and rejected:

1. shortened label as intentional alias — no matching global XSD element exists;
2. renamed operation — same PDF uses `GetCurrentConnectionInformation` and full response structure elsewhere;
3. cross-version substitution — each lane is checked independently against its exact official release tag.

Classification remains **confirmed PDF defect**.

## SDK consequence

Existing runtime mapping remains correct: only decorate an already **INVALID** selected-XSD result when the submitted global root exactly matches the PDF-short form. Never normalize it to valid and never override the selected XSD result.

No XSD bytes, semantic scope or runtime mapping were changed.
