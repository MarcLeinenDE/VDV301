# CE-007 source-locator revalidation — 2026-09-30

## Result

CE-007 remains a confirmed case-sensitive PDF/XSD mismatch for the lexeme families:

- GNSSTypeEnumeration: PDF `Other` vs selected XSD `other`
- TicketValidationEnumeration: PDF `Valid` vs selected XSD `valid`
- VehicleModeEnumeration: PDF `Air` vs selected XSD `air`

XML Schema enumeration values are case-sensitive. The selected XSD is normative for conformance validation; the PDF spelling does not create an alias.

## V1.0 release authority

The selected V1.0 schema files are directly present in the official `VDVde/VDV301` release tag `VDV-301-1.0`:

- `IBIS-IP_common_V1.0.xsd` — blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`
- `IBIS-IP_Enumerations_V1.0.xsd` — blob `a9bea5bc73003ed91ded8519db06c32c4067831d`

The repository workflow states that an official release is marked by the corresponding release tag. Therefore these blobs are official V1.0 release XSD authority for the tagged release.

A separate historical note that the publicly available V1.0-labelled PDF behaves like consolidated V1.x/V1.1 material does not downgrade the authority of the tagged XSD files. PDF provenance and XSD release authority are separate concerns.

## Version scope

- **V1.0:** official release tag `VDV-301-1.0`
- **V2.0:** official release
- **V2.1:** official release
- **V2.2:** official release
- **V2.3:** official release dependency route reusing the exact V2.2 enumerations pool
- **V2.4:** selected candidate/integration XSD lane only; not official-release authority

## Provider-facing diagnostic

### DE

**Titel:** Groß-/Kleinschreibung von Enum-Werten weicht ab

**Kurz:** PDF-Lexeme wie `Other`, `Valid` oder `Air` sind nicht automatisch XSD-gültig.

**Lang:** Die Dokumentation und XSD verwenden bei mehreren Enum-Werten unterschiedliche Groß-/Kleinschreibung. Da XML-Schema-Enumerationen case-sensitiv sind, muss das SDK die exakten XSD-Lexeme verwenden.

**Empfehlung:** Bei einem Case-Mismatch ablehnen und den in der ausgewählten XSD gültigen Wert anzeigen.

### EN

**Title:** Enumeration value casing differs

**Short:** PDF lexemes such as `Other`, `Valid` or `Air` are not automatically XSD-valid.

**Long:** The documentation and XSD use different casing for several enumeration values. XML Schema enumerations are case-sensitive, so the SDK must use the exact selected-XSD lexeme.

**Recommendation:** Reject a casing mismatch and show the value accepted by the selected XSD.

## SDK consequence

- primary issue kind: `identifier_case_error`
- SDK behavior: `error_with_advisory`
- activation class: `xsd_invalid_advisory`
- required precondition: `xsd_result_invalid`
- result effect: `decorate_existing_invalid`
- selected XSD remains normative
- no alias or automatic case normalization is allowed
- PDF-cased values that do not match the selected XSD remain **FAIL**

## Executable evidence

Existing executable evidence remains valid, including EV-117 for the official V1.0-tagged selected XSD pool and the later per-version/aggregate CE evidence.

## Correction note

An earlier draft of this revalidation temporarily downgraded the V1.0 XSD lane because of the PDF provenance caveat. That was incorrect. Direct verification against the official `VDVde/VDV301` tag `VDV-301-1.0` proves that the selected V1.0 XSD blobs are release-tag authority. This report supersedes that temporary interpretation.

## Progress accounting

CE-007 already had a complete locator before this revalidation. No duplicate progress credit is awarded.
