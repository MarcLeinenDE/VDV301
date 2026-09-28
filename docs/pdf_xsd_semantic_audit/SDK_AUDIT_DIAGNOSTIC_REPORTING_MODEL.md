# SDK audit diagnostic and reporting model

Status: canonical design baseline

## Goal
Every machine-detectable conformance failure must be reportable in German and English with equivalent meaning. CLI/live output and formal audit reports are generated from the same canonical diagnostic class and evidence data.

## FAIL report structure
Each reportable failure contains: Test result / Prüfergebnis; Test item / Prüfpunkt; Classification / Klassifizierung; Finding / Feststellung; Assessment / Bewertung; Expected behaviour or remediation / Erwartetes Verhalten oder Korrektur; Evidence / Nachweis.

A known curated finding may enrich a generic XSD failure. It must never change an XSD FAIL to PASS.

## Diagnostic layers
- Generic validator diagnostic: explains the concrete violated XSD rule.
- Curated known-finding advisory: added only when the failure matches a manually classified finding.
- Evidence: selected profile, XSD component/path, constraint and relevant PDF/XSD source locators.

No diagnostic may speculate that an XSD is defective unless the matched finding is explicitly classified accordingly.

## Required bilingual coverage
Every reportable diagnostic class requires German short text, German report text, English short text, English report text, remediation templates in both languages, and machine-readable evidence fields.

Missing DE or EN text is a release/gate failure for a reportable diagnostic class.

## XSD diagnostic taxonomy
The implementation inventory must be derived from the XSD constructs actually present in supported profiles. Baseline classes include:
- unexpected element / invalid structure
- missing required element
- element order / sequence violation
- choice/compositor violation
- minOccurs/maxOccurs violation
- unexpected or missing required attribute
- datatype violation
- enumeration or pattern violation
- minLength/maxLength/length violation
- numeric min/max bounds
- token-derived datatype violation, including NMTOKEN
- boolean, integer, decimal, date, time, dateTime and duration lexical/value violations
- namespace/QName violation
- nil/nillable violation
- invalid root element
- wrong selected service/schema/profile
- generic schema-validation fallback for validator errors not yet specialized

## Aggregation: one explanation, many occurrences
Formal reports MUST NOT repeat the full explanatory text for identical error classes.

Errors are stored losslessly as individual occurrences, then grouped for presentation by a stable diagnostic aggregation key. The key should normally contain:
- selected profile/schema version
- diagnostic class
- violated XSD component/constraint
- expected rule
- curated finding ID, if matched

Concrete XML location and actual value are occurrence data and normally do not split a group.

### Example: 20 NMTOKEN violations
The report contains one finding group:
- DE: 20 Vorkommen — ungültiger Wert für XSD-Datentyp NMTOKEN.
- EN: 20 occurrences — invalid value for XSD datatype NMTOKEN.

The datatype rule, assessment and remediation are explained once. A compact occurrence table lists affected XML paths and values.

Default presentation:
- show first 5 occurrences inline;
- show total occurrence count;
- if more than 5 exist, state how many additional occurrences were suppressed from the main report;
- preserve all occurrences in the machine-readable audit result and optional detailed appendix/export.

Example summary: 1 finding group / 20 occurrences / FAIL. If five rows are shown: +15 additional occurrences; see detailed findings export.

This is presentation deduplication only. It must never discard evidence, reduce the technical failure count, or merge semantically different constraints.

## Known PDF/XSD conflict example
A failure such as CE-017 is first detected as an XSD structure/name failure. If the curated matcher identifies CE-017, the report additionally explains that the PDF documents Description while the selected XSD requires Desciption, and that the implementation follows the PDF but still fails the authoritative selected XSD.

## Implementation gate
Before report generation is considered complete:
1. inventory all XSD constructs/datatypes used by supported profiles;
2. map validator-native errors to canonical diagnostic classes;
3. provide DE+EN templates for every reportable class;
4. test aggregation with repeated errors;
5. test known-finding enrichment separately from generic validation;
6. guarantee full lossless occurrence export.
