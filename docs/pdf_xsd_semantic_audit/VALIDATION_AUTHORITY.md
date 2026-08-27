# Validation authority and tool interpretation policy

Status: audit policy, added during the PDF/XSD semantic audit.

## Source-of-truth rule

VDV 301-2 V2.4 General Conventions, chapter 6, states that IBIS-IP information contents are transferred using XML data structures and can be validated using XML Schema Definition files (XSD). It also states that the VDV provides the XSD files for the specified services. The same chapter says that the XSD files should match the documentation and that, in case of inconsistencies, the XSD definitions take precedence over the documentation.

The V2.4 version history explicitly records this as a technical correction:

```text
in case of inconsistency XSD goes before document
```

Audit consequence:

```text
The semantic audit records both sides:
- what the PDF states
- what the XSD permits

For executable validation behaviour, the XSD is authoritative.
```

## Tool-facing interpretation model

The tool should keep validation strict but explain PDF/XSD discrepancies clearly.

Recommended result fields:

```text
validation_authority: XSD
xsd_result: PASS | FAIL
pdf_note: none | pdf_consistent | pdf_deviates | pdf_suggests_different_value | pdf_only_value | xsd_only_value
finding_ref: CE-xxx where applicable
```

Recommended user-facing wording pattern:

```text
FAIL: The value `<value_from_payload>` is not allowed by the XSD.
Allowed according to XSD: `<xsd_value>`.
Note: The VDV PDF table lists `<pdf_value>`, but VDV 301-2 V2.4 General Conventions state that, in case of inconsistencies, the XSD definitions take precedence over the documentation.
```

Example for CE-007:

```text
FAIL: `Valid` is not allowed by the XSD for TicketValidationEnumeration.
Allowed according to XSD: `valid`.
PDF note: VDV 301-2-1 V2.4 lists `Valid` in the table. This is documented as a PDF/XSD discrepancy. Because XSD has precedence, validation fails.
```

## Audit classification model

Use these classifications for future findings and tool messages:

```text
XSD-valid / PDF-consistent
XSD-valid / PDF-deviates
XSD-invalid / PDF-suggests-valid
XSD-only value
PDF-only value
case-sensitive PDF/XSD mismatch
historical check needed
unclear due to PDF extraction
```

## Operational rule

Do not change an XSD file merely because the PDF differs.

Workflow:

```text
1. Record PDF value/table evidence.
2. Record XSD value/type/cardinality evidence.
3. Classify the discrepancy.
4. For validation, follow XSD.
5. For provider feedback, explain the PDF discrepancy and XSD precedence.
6. Only propose a schema correction later if the discrepancy is confirmed as an XSD defect through historical checks, examples, maintainer feedback, or upstream VDV clarification.
```
