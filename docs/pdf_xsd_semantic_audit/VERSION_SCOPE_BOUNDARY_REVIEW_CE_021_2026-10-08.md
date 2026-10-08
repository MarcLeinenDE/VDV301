# Version-scope boundary review — CE-021 — 2026-10-08

Status: **verified / scope unchanged**.

CE-021 is the LogMessage member-name mismatch: the PDF uses `MessageBody`, while the exact selected XSD requires `Message` of `MessageStructure`.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists as a predecessor control.

`MessageBody` is not an XSD alias. XML following the PDF name fails the exact selected XSD and must remain a FAIL; CE-021 may explain the stale PDF identifier but must not normalize or silently rewrite it.
