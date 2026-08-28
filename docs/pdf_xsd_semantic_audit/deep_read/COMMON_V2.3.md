# VDV 301-2-1 Common Data Structures and Enumerations V2.3 - Deep Read Pass 2

Status: textual fresh read complete; exact official XSD/dependency/variant cross-check complete; previous-audit comparison complete; visual closure pending because the PDF screenshot backend repeatedly returned cache-miss.

Document ID: `COMMON_V2.3`

Official publication:

```text
VDV-Schrift 301-2-1
Version 2.3
02/2021
Common Data Structures and Enumerations
```

Official PDF:

```text
https://www.vdv.de/301-2-1-sdes-v2-3-commonstructure-enums.pdfx
```

Byte-pinned audit source:

```text
SHA-256: d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b
size:    793521 bytes
pin registry: audit_registry/pdf_source_pins_v0.1.json
```

## 1. Method and source quality

The official V2.3 publication was read afresh before the earlier Common/Enumerations audit was used for comparison.

The fresh pass covered the full native text layer with emphasis on:

```text
wrapper datatypes and InternationalTextType
NetexMode
all common data-structure tables
cardinalities
element/type names
subscription structures
service identification structures
enumeration tables and case-sensitive values
V2.3 version history
exact Common -> Enumerations dependency
official/candidate Common V2.3 authority split
```

The native text layer is generally good, but table line wrapping can obscure column boundaries. Therefore layout-sensitive findings remain `needs_visual_review` unless already closed by independent visible-page evidence.

Direct PDF screenshot attempts for the critical V2.3 pages repeatedly returned cache-miss. The same happened in control attempts against V2.2 and V2.4. No OCR substitute is promoted over the native text.

Result:

```text
textual_fresh_read_complete: true
original_pdf_visual_review: attempted_failed_cache_miss
deep_read_state: needs_visual_review
```

CE-020 is an exception to the general visual limitation because its original V2.3 PDF table had already been visually confirmed in the preceding authority-split evidence block and is additionally covered by executable EV-106.

## 2. Exact executable authority for Common V2.3

Official release route:

```text
Common V2.3
  IBIS-IP_common_V2.3.xsd
  official blob: 0d8926c4063c12de9a5e68b6f0addaab35a55dc1
  includes: IBIS-IP_Enumerations_V2.2.xsd
  official Enums V2.2 blob: 2a23b512379b18e8f122ac1272cef8229fb86283
```

There is no separate `IBIS-IP_Enumerations_V2.3.xsd` in the official V2.3 route.

The open upstream PR #30 Common candidate remains separate:

```text
schema_variant_id: common-v2.3-upstream-pr30
candidate Common blob: 456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

Authority rule remains:

```text
official Common V2.3 = default executable authority
PR #30 = explicit candidate overlay only
never latest-wins
```

The post-split root pool and the candidate overlay were executed successfully in GitHub Actions run `33169314332`; EV-106 proves the candidate changes accepted XML instance shape.

## 3. V2.3 intentional structure additions

The V2.3 version history and official XSD direction align on the principal V2.3 structure additions:

```text
DisplayContent:
  AdditionalInformation1..9
  RunNumber

StopInformation:
  ArrivalExpected
  DepartureExpected

TripInformation:
  AdditionalTextMessage1..9
  RunNumber
  PatternNumber
  PathDestinationNumber
```

These are version evolution, not findings by themselves.

The base `AdditionalTextMessage` remains non-repeatable in XSD while the PDF describes `0:*`; the numbered fields do not make the base field repeatable. This strengthens existing `CE-005`.

## 4. Existing Common findings independently reconfirmed

### CE-011 - Connection repeated mode cardinalities

The V2.3 PDF lists both:

```text
TransportMode  0:*
ConnectionMode 0:*
```

The official V2.3 XSD gives each `minOccurs="0"` without `maxOccurs`, therefore `0:1`.

Validation follows XSD.

### CE-013 - AdditionalAnnouncement choice naming

The V2.3 PDF uses:

```text
InformationAtSpecificPoint
```

The official XSD element is:

```text
SpecificPoint
```

Validation follows the exact XSD element name.

### CE-014 - DataVersionList cardinality

The PDF describes at least one `DataVersion`; the XSD uses:

```text
minOccurs="0" maxOccurs="unbounded"
```

and therefore permits an empty list.

### CE-015 - FareZone / ZoneType casing

The fresh native V2.3 PDF text consistently prints `Farezone...` in `FareZoneInformation`, including:

```text
FarezoneID
FarezoneType
FarezoneLongName
FarezoneShortName
```

The official XSD uses:

```text
FareZoneID
FareZoneType
FareZoneLongName
FareZoneShortName
```

The V2.3 `ZoneType` table prints `FarezoneTypeID` and `FarezoneTypeName`; XSD uses `FarezoneTypeID` and `FareZoneTypeName`.

This substantially strengthens CE-015 from extraction-only suspicion to a native-text cross-check. Final visual closure still remains pending because the screenshot backend failed.

### CE-016 - GlobalCardStatusID spelling

The V2.3 PDF prints:

```text
GlobalCardStatusID
```

The official XSD requires:

```text
GlobalCardStausID
```

The typo-like XSD name remains executable authority.

### CE-017 - TSPPoint Description spelling

The V2.3 PDF native text prints:

```text
Description
```

The official XSD requires:

```text
Desciption
```

The same PDF/XSD direction persists in V2.4 for TSPPoint. Native-text confidence is now high; visible-page closure remains pending.

### CE-018 - ServiceIdentificationWithStateList cardinality

Fresh V2.3 reading reconfirms PDF `1:*`.

Official XSD:

```text
ServiceIdentificationWithState
minOccurs="0"
maxOccurs="unbounded"
```

Executable evidence already confirms the XSD accepts the empty list.

### CE-019 - ServiceIdentificationWithStateList item type/reference

The V2.3 table names the item:

```text
ServiceIdentificationWithState
```

but associates it with `ServiceSpecificationWithState` / the corresponding structure reference.

Official XSD:

```text
ServiceIdentificationWithState
type="ServiceIdentificationWithStateStructure"
```

The native-text evidence is clear and is consistent with the already observed V2.1-V2.4 documentation chain. Visual closure remains pending.

### CE-020 - InternationalTextType official XSD vs PDF / PR #30

Official V2.3 PDF:

```text
Value     1:1 IBIS-IP.string
Language  1:1 IBIS-IP.language
ErrorCode 0:1 ErrorCodeEnumeration
```

Official release XSD:

```text
Value     xs:string
Language  xs:language
```

PR #30 candidate:

```text
Value     IBIS-IP.string
Language  IBIS-IP.language
```

EV-106 proves this changes the accepted XML shape. The authority split remains intact; no XSD is modified by this audit.

## 5. New finding CE-021 - LogMessage `MessageBody` vs XSD `Message`

Fresh V2.3 PDF table `LogMessage` describes:

```text
MessageProvider 1:1 +DeviceSpecification
MessageBody     1:1 +Message
```

Official V2.3 XSD:

```text
LogMessageStructure
  MessageProvider
  Message
```

The same `MessageBody` PDF wording is present in checked V2.2 and V2.4 documents, while checked V2.2/V2.3/V2.4 XSDs use `Message`.

Classification:

```text
mismatch_kind: element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
version_scope: checked PDF/XSD V2.2-V2.4
validation_behavior: <MessageBody> rejected; <Message> required
confidence: high native-text + exact-XSD cross-version evidence
```

Visual page confirmation remains pending.

## 6. New finding CE-022 - ServiceIdentification `ServiceName` vs XSD `Service`

Fresh V2.3 PDF table `ServiceIdentification` describes:

```text
ServiceName 1:1 +ServiceSpecification
Device      1:1 +DeviceSpecification
```

Official V2.3 XSD:

```text
ServiceIdentificationStructure
  Service  ServiceSpecificationStructure
  Device   DeviceSpecificationStructure
```

The same PDF `ServiceName` wording is present in checked V2.2/V2.4 material, while checked V2.2/V2.3/V2.4 XSDs consistently use `Service`.

This is especially easy to misread because `ServiceSpecificationStructure` itself legitimately contains an inner `ServiceName` enumeration field.

Classification:

```text
mismatch_kind: element_name
likely_source_issue: pdf_table_copy_or_naming_error_candidate
version_scope: checked PDF/XSD V2.2-V2.4
validation_behavior: <ServiceName> at ServiceIdentification level rejected; <Service> required
confidence: high native-text + exact-XSD cross-version evidence
```

## 7. New finding CE-023 - V2.3 duplicate/corrupt second NetexMode table

The V2.3 document correctly defines NetexMode earlier in datatype section 1.18 with the expected main-mode/submode choice structure.

Later, however, V2.3 contains another section:

```text
2.34 NetexMode
```

whose table body is the `Message` structure:

```text
Message-ID
TimeStamp
MessageType
MessageText
```

The official V2.3 XSD `NetexMode` is correctly modelled with:

```text
PtMainMode / PrivateMainMode
PtSubmodeChoiceGroup / PrivateSubmodeChoiceGroup
```

Cross-version context:

```text
V2.2: after Message comes 2.34 Point
V2.3: inserts erroneous second 2.34 NetexMode copy of Message
V2.4: after Message comes 2.34 Point
```

Classification:

```text
mismatch_kind: duplicate_or_copy_paste_table
likely_source_issue: V2.3_pdf_table_error_candidate
version_scope: V2.3-specific in checked chain
validation_impact: documentation only if resolver follows XSD; do not model NetexMode from the corrupt table
confidence: high native-text + cross-version structure evidence
```

## 8. New finding CE-024 - UnsubscribeResponse `Active` PDF 0:1 vs XSD 1:1

Checked V2.2, V2.3 and V2.4 PDF tables describe:

```text
Active                0:1
OperationErrorMessage 0:1
```

Checked XSDs use:

```text
UnsubscribeResponseStructure
  Active                required
  OperationErrorMessage optional
```

Classification:

```text
mismatch_kind: cardinality
subclassification: xsd_stricter_than_pdf
version_scope: checked V2.2-V2.4
validation_behavior: response without Active is invalid
confidence: high native-text + exact-XSD cross-version evidence
```

No XSD is changed.

## 9. New finding CE-025 - `Reply-Path` vs XSD `ReplyPath`

V2.2 and V2.3 PDF subscription request tables print:

```text
Reply-Path
```

for both SubscribeRequest and UnsubscribeRequest.

The XSD family uses:

```text
ReplyPath
```

V2.4 documentation uses `ReplyPath`, so the PDF naming issue is historically corrected by V2.4.

Classification:

```text
mismatch_kind: element_name
version_scope: checked V2.2-V2.3; documentation corrected V2.4
validation_behavior: <Reply-Path> rejected; <ReplyPath> accepted
confidence: high
```

## 10. New finding CE-026 - BeaconPoint `Description` vs V2.3 XSD `Desciption`

The V2.3 PDF `BeaconPoint` table prints:

```text
Description
```

Official Common V2.3 XSD uses the typo-like:

```text
Desciption
```

V2.4 XSD corrects `BeaconPointStructure` to `Description`, while the separate `TSPPointStructure` typo remains and is covered by CE-017.

Classification:

```text
mismatch_kind: element_name_spelling
version_scope: Common V2.3 historical mismatch; corrected in Common V2.4 XSD
validation_behavior_v2_3: <Description> rejected; <Desciption> required
confidence: high native-text + exact-XSD + later-correction evidence
```

This is historical correction evidence only; it does not retroactively rewrite Common V2.3.

## 11. DataAcceptedResponse - no new finding

The V2.3 PDF table visually/textually presents both response alternatives as rows with `1:1`, but the semantic response model and official XSD use:

```text
DataAcceptedResponseData
or
OperationErrorMessage
```

through `xs:choice`.

The earlier table-level audit already treated this as either/or response semantics. The fresh Deep Read therefore does not create a duplicate finding.

Validation follows `xs:choice`: both alternatives together are invalid.

## 12. Enumeration findings and CE-010 historical correction

Common V2.3 reuses the official Enumerations V2.2 blob.

The fresh authority check discovered a stale statement in the earlier generated V2.3->V2.4 delta: `canalBarge` was **not** introduced by Enumerations V2.4.

The exact official VDV-301-2.2 `IBIS-IP_Enumerations_V2.2.xsd` already contains:

```text
AirSubmodeEnumeration = canalBarge
```

and the current branch stores the same official blob.

Therefore:

```text
CE-010 remains a PDF-vs-XSD enumeration omission,
but its confirmed XSD history starts at least with official Enumerations V2.2
and therefore applies to the Common V2.3 dependency pool as well.
```

The generated V2.3->V2.4 delta and 04e closure text must be corrected accordingly.

Other inherited enumeration findings remain:

```text
CE-004 old ServiceNameEnumeration values still printed in PDF
CE-006 warning absent from PDF but present in XSD
CE-007 case differences such as Valid/valid, Air/air, Other/other
CE-008 Netex/submode case differences
CE-009 specialRail vs specialTrain
```

## 13. Old-audit comparison

The older 04d/04e and V2.4 table-level audits were opened only after the fresh Common V2.3 pass.

They already covered much of the version-family foundation:

```text
Common V2.3 -> Enumerations V2.2 dependency
CE-004 through CE-017 ranges
V2.3 structure additions
CE-018/CE-019 addendum
CE-020 authority collision
```

The fresh read adds or materially strengthens:

```text
CE-015 native-text casing evidence including ZoneType
CE-017 native-text TSPPoint Description evidence
CE-019 native-text item type/reference evidence
CE-021 LogMessage MessageBody vs Message
CE-022 ServiceIdentification ServiceName vs Service
CE-023 V2.3 duplicate/corrupt second NetexMode table
CE-024 UnsubscribeResponse.Active PDF 0:1 vs XSD 1:1
CE-025 Reply-Path vs ReplyPath, corrected in V2.4 PDF
CE-026 BeaconPoint Description vs Desciption, corrected in V2.4 XSD
CE-010 historical range correction: canalBarge already exists in official Enums V2.2
```

No XSD change is proposed.

## 14. Deep-read conclusion

```text
textual fresh read: complete
byte-pinned original PDF: yes
exact official Common V2.3 XSD: verified
exact official Enumerations V2.2 dependency: verified
PR #30 candidate separated: yes
post-split executable baseline: PASS run 33169314332
old-audit comparison: complete
new Common findings: CE-021..CE-026
existing findings strengthened: CE-005, CE-011, CE-013..CE-020 and enumeration family findings
stale prior statement corrected: CE-010/canalBarge historical scope
visual page closure: pending because screenshot backend returns cache-miss
deep_read_state: needs_visual_review
```

## 15. Next Deep Read target

Return to the main semantic-document sequence with:

```text
VDV301-2_GC_V2.4
General Conventions V2.4
```

Before using it as reproducible page evidence, byte-pin the official PDF according to `PDF_SOURCE_CACHE_POLICY.md`.
