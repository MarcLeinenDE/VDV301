# Version-scope boundary review — CE-022 — 2026-10-08

Status: **verified / scope unchanged**.

CE-022 is the ServiceIdentification structure-reference mismatch. The PDF places `ServiceName` at the outer `ServiceIdentification` level, while the exact selected XSD requires outer element `Service` of `ServiceSpecificationStructure`. `ServiceName` legitimately exists one level deeper inside that nested structure, which explains the likely table-copy/naming defect but does not create an XML alias.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3 plus the selected V2.4 candidate/integration lane. No earlier retained Common publication exists.

The exact selected XSD remains normative: outer `ServiceName` must fail where outer `Service` is required. CE-022 may explain the PDF structure error but must not normalize it.
