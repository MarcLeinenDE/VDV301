# Version-scope boundary review — CE-016 — 2026-10-08

Status: **verified / scope unchanged**.

CE-016 is the GlobalCardStatus identifier mismatch. The PDF uses `GlobalCardStatusID`; the exact selected XSD uses the typo-like element name `GlobalCardStausID`.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists as a predecessor control.

The spelling `Staus` is strongly typo-like, but this does not weaken executable conformance. For every affected selected profile, `GlobalCardStausID` is the exact XML name required by the XSD. `GlobalCardStatusID` from the PDF must not be silently accepted, repaired or normalized; CE-016 may explain the mismatch on the resulting XSD failure.
