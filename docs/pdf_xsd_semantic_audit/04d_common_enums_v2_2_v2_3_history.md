# Common/Enums V2.2 -> V2.3 history audit

Status: XSD-side dependency/structure diff and PDF-side first pass completed.

Scope:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.3.xsd
No IBIS-IP_Enumerations_V2.3.xsd observed
VDV 301-2-1 Common Data Structures and Enumerations V2.3 PDF source
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.3 Common structures to a V2.2 service payload unless the selected service/dependency pool actually uses V2.3.
For V2.3, the selected dependency pool observed in this branch is Common V2.3 plus Enumerations V2.2.
```

## 1. XSD dependency family observation

### Common/Enums V2.2

Observed:

```text
IBIS-IP_common_V2.2.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
```

### Common/Enums V2.3

Observed:

```text
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
No IBIS-IP_Enumerations_V2.3.xsd was observed in dev/schema-integration.
```

First-pass result:

```text
This is a deliberate mixed dependency family for the selected branch state:
Common V2.3 reuses the V2.2 enumeration pool.
No V2.3 enumeration-value delta is opened.
```

## 2. XSD-side generated files

Created generated audit files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_2_vs_v2_3_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_2_vs_v2_3_structure_delta.csv
```

Enumeration result:

```text
No separate V2.3 enumeration file.
V2.3 common includes V2.2 enumerations.
No V2.2 -> V2.3 enumeration value change observed.
```

Structure result:

```text
V2.3 changes are structure-level additions in common V2.3, not enumeration-level additions.
```

## 3. V2.3 PDF-side first pass

The opened V2.3 PDF identifies itself as:

```text
VDV-Schrift 301-2-1
02/2021
Common Data Structures and Enumerations
V2.3
```

The V2.3 version history confirms these functional structure changes:

```text
AdditionalInformation(n) inserted in DisplayContent.
RunNumber inserted in DisplayContent.
ArrivalExpected inserted in StopInformation structure.
DepartureExpected inserted in StopInformation structure.
RunNumber inserted in TripInformation structure.
PatternNumber inserted in TripInformation structure.
PathDestinationNumber inserted in TripInformation structure.
AdditionalTextMessage(n) inserted in TripInformation structure.
```

The V2.3 version history also documents this technical/documentation-oriented change:

```text
Reference to the CIS tool in the foreword.
```

First-pass interpretation:

```text
The V2.3 PDF version history matches the observed XSD direction:
common structures change, but enumerations are reused from V2.2.
```

## 4. XSD structure observations

Observed V2.3 XSD additions include:

```text
DisplayContentStructure:
  AdditionalInformation1..AdditionalInformation9, each optional/repeatable.
  RunNumber optional.

StopInformationStructure:
  ArrivalExpected optional.
  DepartureExpected optional.

TripInformationStructure:
  RunNumber optional.
  PatternNumber optional.
  PathDestinationNumber optional.
  AdditionalTextMessage1..AdditionalTextMessage9 optional.
```

Important note on AdditionalTextMessage:

```text
The V2.3 XSD adds AdditionalTextMessage1..9.
The base AdditionalTextMessage element itself remains optional without maxOccurs="unbounded".
Therefore CE-005 is still supported for V2.3, because PDF/history expects 0:* behaviour but XSD modelling remains bounded by named fields.
```

## 5. CE-001 decision

CE-001 was originally opened as unclear because:

```text
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
No IBIS-IP_Enumerations_V2.3.xsd is present.
```

After this pass:

```text
The V2.3 PDF version history does not record enumeration additions/removals.
The V2.3 XSD dependency family intentionally reuses Enumerations V2.2 in the observed branch state.
This is a version-specific dependency fact, not a schema defect by itself.
```

Decision:

```text
CE-001 can be closed as OK with note after findings.md is updated.
Do not create an IBIS-IP_Enumerations_V2.3.xsd merely to make the version number symmetrical.
```

## 6. Already-known findings supported by this pass

| Topic | First-pass classification | Finding impact |
|---|---|---|
| V2.3 include family | Common V2.3 intentionally reuses Enumerations V2.2 in observed branch state. | CE-001 can be closed as OK with note. |
| V2.3 structural additions | PDF version history and XSD direction align for DisplayContent, StopInformation and TripInformation additions. | No new CE for existence. |
| AdditionalTextMessage(n) | XSD adds named fields AdditionalTextMessage1..9; base AdditionalTextMessage remains 0:1. | Supports CE-005 for V2.3. |
| ServiceNameEnumeration removed names | V2.3 inherits V2.2 enumeration pool; removed old service names remain absent from XSD, while V2.3 PDF table still carries inherited table inconsistency. | Supports CE-004 from V2.2 onward. |
| DeviceState warning | V2.3 inherits V2.2 enumeration pool containing warning; V2.3 PDF table does not list warning. | Supports CE-006 from V2.2 onward. |
| Common enum case issues | V2.3 inherits V2.2 enumeration pool and tables. | Supports CE-007/CE-008/CE-009 historical ranges. |

## 7. Finding state decision

Status after this pass:

```text
No new CE finding opened.
No XSD change proposed.
CE-001 is ready to be marked OK with note in findings.md.
```

Reason:

```text
The absence of IBIS-IP_Enumerations_V2.3.xsd is no longer unclear in this audit context.
The V2.3 document introduces structure additions, while the branch dependency family keeps V2.2 enumerations.
```

## 8. Validation backlog impact

Later technical validation should include this exact version-specific pool:

```text
Common/Enums V2.3 pool:
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd
```

Suggested targeted samples after schema compile:

```text
V2.2 negative / V2.3 positive: DisplayContent.AdditionalInformation1.
V2.2 negative / V2.3 positive: DisplayContent.RunNumber.
V2.2 negative / V2.3 positive: StopInformation.ArrivalExpected.
V2.2 negative / V2.3 positive: StopInformation.DepartureExpected.
V2.2 negative / V2.3 positive: TripInformation.PatternNumber.
V2.2 negative / V2.3 positive: TripInformation.PathDestinationNumber.
V2.3 positive with PDF note: AdditionalTextMessage1..9.
V2.3 still negative: repeated base AdditionalTextMessage elements if no maxOccurs is present.
```

## 9. Next work inside the historical block

Next detailed audit file:

```text
docs/pdf_xsd_semantic_audit/04e_common_enums_v2_3_v2_4_history_and_closure.md
```

Required next steps:

```text
1. Compare Common/Enums V2.3 and V2.4 XSD include families, structure deltas and enumeration deltas.
2. Check VDV 301-2-1 V2.4 PDF version history and affected tables.
3. Consolidate historical affected-version ranges for CE-004 through CE-017.
4. Keep visual-only CE-015/CE-017/ZoneType checks deferred where required by the user.
```

## 10. Result

```text
Common/Enums V2.2 -> V2.3 historical audit now has XSD dependency/structure diff plus PDF-side first pass.
V2.3 reuses Enumerations V2.2; this is documented as the selected V2.3 dependency pool.
CE-001 can be closed as OK with note.
No new finding opened in this pass.
Next: V2.3 -> V2.4 history and Common/Enums historical closure.
```
