# Version-scope boundary review — CIS-005 — 2026-10-08

Status: **verified / PDF-internal type contradiction / scope unchanged**.

## Finding
On both CIS V2.2 and CIS V2.3 official PDFs, the field `MyOwnVehicleMode` appears with two different types: `NetexMode` in AllData Table 3 (printed page 14), and `PtModesEnumeration` in VehicleData Table 17 (printed page 20). The exact selected official CIS schemas declare `MyOwnVehicleMode` as optional `NetexMode`; Common defines that as structured main/submode content. This is one semantic finding despite two rows inside each document.

## Lower boundary
Official CIS V2.0 schema `fa8f0a51ad5f612660c9532c8557ad1ca473a908` has no `MyOwnVehicleMode` element, so the contradictory typing cannot apply to that earlier service version. CIS V2.2 is the first proven affected publication (CIS XSD blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`).

## Continuity and upper boundary
CIS V2.3 official PDF repeats the Table 3 vs Table 17 discrepancy (CIS XSD blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e` still declares NetexMode). Selected CIS V2.4 candidate/integration XSD `49475efc7ed708f9d11999fa72703a98f1d3ce04` also declares NetexMode, but the published CIS V2.4 PDF needed to prove persistence or correction of the *PDF contradiction* is not established; do not extend CIS-005's official affected-version scope.

## Executable negative control / SDK
EV-125 (run `33744039627`) confirms structured NetexMode is valid and scalar PtModesEnumeration-style text is invalid for V2.2/V2.3. A provider using the scalar form must **FAIL** selected-XSD validation with an explanatory PDF Known-Issue advisory. No alias, normalization or false PASS. Existing semantic/runtime scope **CIS V2.2 / CIS V2.3** unchanged.

Source pin and PDF body: `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_CIS_005_2026-10-06.md`.
