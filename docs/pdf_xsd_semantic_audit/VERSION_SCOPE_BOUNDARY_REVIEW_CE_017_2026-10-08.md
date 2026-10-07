# Version-scope boundary review — CE-017 — 2026-10-08

Status: **verified / scope unchanged**.

CE-017 is the TSPPoint identifier mismatch: the PDF uses `Description`, while the exact selected XSD requires the typo-like XML element `Desciption`.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists as a predecessor control.

Although `Desciption` is typo-like, the exact selected XSD remains normative. `Description` must not be silently accepted or normalized where the XSD requires `Desciption`; CE-017 may explain the resulting XSD failure.
