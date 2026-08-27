# Executable validation - CE-018 ServiceIdentificationWithStateList cardinality

Status: completed; CE-018 executable-confirmed.

## Finding premise

Checked Common PDF versions V2.1, V2.2, V2.3 and V2.4 describe the list item `ServiceIdentificationWithState` with cardinality `1:*`.

The Common XSD family models the same item as:

```xml
<xs:element name="ServiceIdentificationWithState"
            type="ServiceIdentificationWithStateStructure"
            minOccurs="0"
            maxOccurs="unbounded"/>
```

This predicts XSD behaviour `0:*`.

## Executed tool

```text
tools/validate_ce018_service_identification_with_state_list.py
```

The tool creates a temporary harness for every root Common version currently present in the superbranch and lets each Common file resolve its own declared dependency filenames.

Tested Common versions:

```text
V1.0
V2.0
V2.1
V2.2
V2.3
V2.4
```

Per version, two samples are tested:

```text
1. empty ServiceIdentificationWithStateListStructure
2. one-item ServiceIdentificationWithStateListStructure with a complete service/device/state identification
```

## Evidence run

```text
workflow: schema-audit-validation
run number: 6
run id: 33109768872
head SHA tested: 2298f1297e9d2b00aacbf244f39f6c73587f713e
Python: 3.12.14
lxml: 6.1.2
ce018_status: 0
```

## Results

```text
Common V1.0 harness compile PASS
  empty list PASS
  one item  PASS

Common V2.0 harness compile PASS
  empty list PASS
  one item  PASS

Common V2.1 harness compile PASS
  empty list PASS
  one item  PASS

Common V2.2 harness compile PASS
  empty list PASS
  one item  PASS

Common V2.3 harness compile PASS
  empty list PASS
  one item  PASS

Common V2.4 harness compile PASS
  empty list PASS
  one item  PASS
```

Tool conclusion:

```text
PASSED: CE-018 executable 0:* behaviour confirmed across Common V1.0-V2.4
```

## Interpretation

The XSD behaviour is not a one-version accident. The executable Common family represented in the superbranch consistently permits an empty `ServiceIdentificationWithStateListStructure`.

For V2.1-V2.4, where the checked PDF tables say `1:*`, the PDF is stricter than the executable XSD.

Classification:

```text
cardinality_mismatch_candidate
xsd_more_permissive_than_pdf
executable-confirmed
```

## Validation authority / SDK consequence

The future SDK must:

```text
accept an empty list when validating against the selected Common XSD;
not impose PDF 1:* as an additional hard XML validation rule;
optionally surface the known PDF/XSD discrepancy as a diagnostic;
retain exact version provenance in the diagnostic.
```

No XSD is changed.

## Next planned executable block

```text
EV-103 - Video service xs:choice modelling candidates

VLS-002  VideoLiveService V2.0
VRS-003  VideoRecordingService V2.0
VDS       VideoDisplayService V2.0 compositor findings
```
