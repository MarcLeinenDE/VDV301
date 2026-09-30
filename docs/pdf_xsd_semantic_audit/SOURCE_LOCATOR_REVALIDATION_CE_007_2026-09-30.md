# CE-007 source-locator revalidation — 2026-09-30

## Result

CE-007 remains a confirmed case-sensitive PDF/XSD mismatch for the lexeme families:

- GNSSTypeEnumeration: PDF `Other` vs selected XSD `other`
- TicketValidationEnumeration: PDF `Valid` vs selected XSD `valid`
- VehicleModeEnumeration: PDF `Air` vs selected XSD `air`

XML Schema enumeration values are case-sensitive. Where the selected XSD is authoritative for the validation profile, the PDF spelling does not create an alias: the PDF-cased value is XSD-invalid and the exact XSD lexeme is required.

## Authority correction for the oldest lane

The historical audit already records that the public document labelled V1.0 behaves as a V1.x / V1.1-consolidated publication and that the independent pure V1.0 release-schema identity was not resolved.

Therefore this revalidation does **not** discard the executable V1.x evidence, but it removes the stronger claim that the selected `IBIS-IP_Enumerations_V1.0.xsd` blob is proven pure official V1.0 release authority.

Canonical scope after this correction:

- **V1.x historical selected profile:** exact selected `IBIS-IP_Enumerations_V1.0.xsd` blob; executable lexeme boundary confirmed, but pure V1.0 official-release schema authority unresolved.
- **V2.0–V2.3:** official release/dependency authority, version exact.
- **V2.4:** explicit candidate/integration XSD lane only; not promoted to official release authority.

This is an authority/provenance correction only. It does not change the observed case mismatch or the SDK PASS/FAIL rule.

## Provider-facing diagnostic

### DE

**Titel:** Groß-/Kleinschreibung von Enum-Werten weicht ab

**Kurz:** PDF-Lexeme wie `Other`, `Valid` oder `Air` sind nicht automatisch XSD-gültig.

**Lang:** Die Dokumentation und die ausgewählte XSD verwenden bei mehreren Enum-Werten unterschiedliche Groß-/Kleinschreibung. XML-Schema-Enumerationen sind case-sensitiv; deshalb muss für die Konformitätsprüfung das exakte Lexem der ausgewählten XSD verwendet werden. Für die älteste V1.x-Lane ist die technische Abweichung bestätigt, ohne daraus eine reine offizielle V1.0-Release-XSD-Autorität abzuleiten.

**Empfehlung:** Bei einem Case-Mismatch gegen ein ausgewähltes XSD-Profil als XSD-FAIL bewerten und zusätzlich den in der ausgewählten XSD gültigen Wert sowie die PDF/XSD-Abweichung erklären.

### EN

**Title:** Enumeration value casing differs

**Short:** PDF lexemes such as `Other`, `Valid` or `Air` are not automatically XSD-valid.

**Long:** The documentation and selected XSD use different casing for several enumeration values. XML Schema enumerations are case-sensitive, so conformance validation must use the exact lexeme defined by the selected XSD. For the oldest V1.x lane, the technical mismatch is confirmed without claiming proven pure official V1.0 release-XSD authority.

**Recommendation:** Treat a casing mismatch against a selected XSD profile as an XSD FAIL and additionally explain the value accepted by the selected XSD and the PDF/XSD discrepancy.

## SDK consequence

- primary issue kind: `identifier_case_error`
- selected XSD remains normative for an explicitly selected validation profile
- PDF spelling never becomes an alias
- XSD-invalid PDF-cased form remains **FAIL**
- SDK behavior remains `error_with_advisory`
- activation remains `xsd_invalid_advisory`
- result effect remains `decorate_existing_invalid`
- no automatic normalization or correction is allowed
- V1.x historical lane must not be presented as proven pure official V1.0 release conformance

## Executable evidence

Existing evidence remains sufficient for the lexeme boundary:

- EV-117 / run `33279461529` — selected historical V1.x/V1.0-named XSD pool
- EV-118 / run `33280224191` — V2.0
- EV-119 / run `33609779315` — V2.1
- EV-120 — V2.2
- EV-121 / run `33657653888` — V2.3 dependency route
- aggregate CE evidence EV-124 / run `33735601969`
- V2.4 candidate/integration XSD identity is pinned in the source-locator manifest

## Progress accounting

CE-007 already had a complete locator before this revalidation. The finding remains complete after the authority correction and receives **no duplicate progress credit**.
