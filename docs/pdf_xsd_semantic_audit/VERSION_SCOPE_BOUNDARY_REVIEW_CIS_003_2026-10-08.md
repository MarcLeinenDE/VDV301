# Version-scope boundary review — CIS-003 — 2026-10-08

Status: **verified / confirmed PDF defect / scope unchanged**.

## Finding
In the official CIS V2.0, V2.2 and V2.3 PDFs, the GetCurrentConnectionInformation response-detail tables shorten the response label to `CustomerInformationService.GetCurrentConnectionResponse`. The exact selected official XSD in every affected version instead defines the global XML response root `CustomerInformationService.GetCurrentConnectionInformationResponse`.

The same PDF's operation overview retains the full `GetCurrentConnectionInformationResponseStructure` name. The shorter detail label is thus not established as an intentional alternate root.

## Lower boundary
- V1.0 official XSD uses an earlier response-structure model without the corresponding V2.x global response-root declaration; it does not establish this exact V2.x global-root PDF defect.
- V1.1 has no proven strict release-XSD authority (CIS-001); no V1.1 profile may be substituted to widen this finding.
- CIS V2.0 is the first independently byte-pinned published-PDF and release-tagged-XSD affected comparison. Printed PDF p. 15 Table 6 uses the short name, while its own overview on p.10 uses the full structure name.

## Continuity / release version
- CIS V2.0: official XSD blob `fa8f0a51ad5f612660c9532c8557ad1ca473a908`.
- Global `VDV-301-2.1` release retains the exact V2.0 CIS blob; no separate CIS V2.1 service XSD.
- CIS V2.2: official XSD blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`, PDF p.16 Table 6 still shortens the detail label.
- CIS V2.3: official XSD blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`, PDF p.16 Table 6 still shortens the detail label.

`EV-125` (run `33744039627`) executes the valid full root and invalid PDF-short root on all three official service versions. The exact PDF locators and internal overview controls are pinned in `SOURCE_LOCATOR_REVIEW_CIS_003_2026-10-06.md`.

## Upper boundary
The VDV publication index (https://www.vdv.de/ip-kom-oev.aspx) checked 2026-10-08 lists CIS V1.1, V2.0, V2.2 and V2.3, not a published CIS V2.4 PDF. A candidate/integration CIS V2.4 XSD with the full root exists but cannot by itself prove continuation of this *published-PDF defect*.

## Boundary conclusion / SDK
Existing finding remains **CIS V2.0, V2.2 and V2.3 only**. The XML `CustomerInformationService.GetCurrentConnectionResponse` root must FAIL exact selected-XSD validation in those profiles. CIS-003's bilingual advisory may explain the PDF contradiction, but must never add an alias, silently normalize the XML, or convert INVALID to VALID.
