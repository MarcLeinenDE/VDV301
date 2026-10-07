# Version-scope boundary review — CE-019 — 2026-10-08

Status: **verified / scope unchanged**.

CE-019 is the ServiceIdentificationWithState type-reference mismatch. The PDF names the list item `ServiceIdentificationWithState` but references/types it as `ServiceSpecificationWithState`; the exact selected XSD instead types the item as `ServiceIdentificationWithStateStructure`.

This is distinct from CE-018's cardinality mismatch.

The type-reference mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists as a predecessor control.

The exact selected XSD structure remains normative. The PDF's `ServiceSpecificationWithState` reference is not an alternate accepted type for this list item; CE-019 may explain the documentation defect without changing XSD validation.
