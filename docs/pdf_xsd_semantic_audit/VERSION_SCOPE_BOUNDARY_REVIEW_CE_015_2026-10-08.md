# Version-scope boundary review — CE-015 — 2026-10-08

Status: **verified / scope unchanged**.

CE-015 is the case-sensitive FareZoneInformation identifier mismatch: the PDF uses `FarezoneID`, `FarezoneType`, `FarezoneLongName` and `FarezoneShortName`, while the exact selected XSD requires the corresponding `FareZone*` names with capital Z.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists as a predecessor control.

Because XML element names are case-sensitive, the PDF spellings are not aliases. The exact selected XSD remains normative: payloads using `Farezone*` where `FareZone*` is required are invalid and CE-015 may explain the documentation mismatch without normalization.
