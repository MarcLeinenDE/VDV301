# Version-scope boundary review — CE-018 — 2026-10-08

Status: **verified / scope unchanged**.

CE-018 is the `ServiceIdentificationWithStateList` cardinality mismatch: the PDF requires `ServiceIdentificationWithState 1:*`, while the exact selected Common XSD permits `0:*`.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. Existing executable checks confirm that an empty list is accepted by the selected XSDs across this lineage. No earlier retained Common publication exists as a predecessor control.

The exact selected XSD remains normative. An empty list that is XSD-valid must remain valid; CE-018 may explain the stricter PDF cardinality but must not add an independent rejection.
