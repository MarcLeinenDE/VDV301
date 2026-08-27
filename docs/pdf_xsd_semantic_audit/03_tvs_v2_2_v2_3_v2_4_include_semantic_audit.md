# TicketValidationService V2.2 / V2.3 / V2.4 - include and semantic audit

Status: completed first pass.

Scope:

```text
VDV 301-2-16 TicketValidationService V2.4
IBIS-IP_TicketValidationService_V2.2.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.4.xsd
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Important PDF-side rule observed in the TVS V2.4 document:

```text
For implementation, the corresponding XSD file shall be used.
In case of mismatches between the PDF description and the XSD, the XSD is the master.
```

## 1. Source and provenance notes

### PDF side

Source document:

```text
VDV-Schrift 301-2-16
TicketValidationService V2.4
01/2023
```

The V2.4 foreword and version history state that V2.4 introduces a new operation to return, for the current stop, all stops of the current line that are reachable via the short-haul tariff.

### XSD side

Files checked in `dev/schema-integration`:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.4.xsd
```

Upstream note:

```text
Current official upstream VDVde/VDV301 master has TicketValidationService V2.4 including common V2.4 but enumerations V2.2.
The dev/schema-integration branch intentionally aligns the TVS V2.4 candidate to both common V2.4 and Enumerations V2.4.
```

## 2. Dependency include history

### TVS V2.2

Observed include family:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

### TVS V2.3

Observed include family:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Interpretation:

```text
The V2.3 PDF version history says the correction in chapter 3.1.2 brought the description in line with XSD and no XSD update was necessary.
The branch XSD confirms no schema-family include change from TVS V2.2 to TVS V2.3.
```

### TVS V2.4 in dev/schema-integration

Observed include family:

```text
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Interpretation:

```text
This is the desired V2.4 dependency-family alignment for the integration branch.
It also resolves the upstream/candidate inconsistency where TVS V2.4 used common V2.4 but still used Enumerations V2.2.
```

## 3. V2.2 to V2.3 comparison

First-pass semantic result:

```text
No service-operation delta observed in the XSD files.
No include-family delta observed.
```

PDF version-history interpretation:

```text
V2.3 appears to be a documentation correction for chapter 3.1.2, not a schema update.
```

Status: OK with note.

No TVS-specific finding opened for V2.2 -> V2.3.

## 4. V2.3 to V2.4 comparison

V2.4 adds a new operation/data structure family:

```text
TicketValidationService.GetCurrentShortHaulStopsResponse
TicketValidationService.GetCurrentShortHaulStopsResponseStructure
TicketValidationService.CurrentShortHaulStopsDataStructure
```

The data structure in the integration-branch XSD is:

```text
TimeStamp 1:1 IBIS-IP.dateTime
CurrentTariffStop 0:* StopInformationStructure
CurrentTripRef 0:1 IBIS-IP.NMTOKEN
```

This matches the V2.4 PDF table-level intent for the new short-haul stop operation.

Status: OK for the data structure itself.

## 5. TVS-001 - GetCurrentShortHaulStops missing from operation group

State: confirmed XSD internal consistency candidate.

Observation:

```text
The V2.4 XSD defines the top-level element:
TicketValidationService.GetCurrentShortHaulStopsResponse

The V2.4 XSD also defines the corresponding response and data structures.

However, the xs:group `TicketValidationServiceOperations` still lists only the older V2.2/V2.3 operation elements and does not include:
TicketValidationService.GetCurrentShortHaulStopsResponse
```

Impact:

```text
Validation of the top-level element may still work when it is validated directly.
However, any schema consumer, code generator or audit extractor that relies on `TicketValidationServiceOperations` as the service operation inventory will miss the new V2.4 operation.
```

Tool implication:

```text
The VDV301 Tool / SDK should not rely only on the service group for operation discovery.
It should cross-check top-level service elements and operation groups and report group omissions as schema consistency findings.
```

PR-candidate note:

```text
This may become a narrow official correction PR candidate after the full audit, upstream recheck, open-PR check and local XSD/sample validation.
Do not open a PR during the audit.
```

## 6. TVS-002 - VehicleData RouteDeviation type PDF vs XSD

State: confirmed PDF/XSD type-name discrepancy candidate.

PDF-side observation:

```text
TicketValidationService.VehicleData / RouteDeviation is shown with type RouteDirectionEnumeration.
```

XSD-side observation:

```text
TicketValidationService.VehicleDataStructure / RouteDeviation uses RouteDeviationEnumeration.
```

Interpretation:

```text
The XSD name aligns with the field name RouteDeviation and with the existing common enumeration RouteDeviationEnumeration.
The PDF type name RouteDirectionEnumeration appears likely to be a documentation/table mismatch, but validation follows XSD.
```

Tool implication:

```text
Payload validation must use RouteDeviationEnumeration.
If a provider discussion cites the PDF table, the tool should explain that the PDF lists RouteDirectionEnumeration while the XSD uses RouteDeviationEnumeration, and that TVS V2.4 itself says the XSD is master in case of mismatch.
```

PR-candidate note:

```text
Likely documentation correction candidate, not necessarily an XSD correction candidate.
Recheck historical PDFs and examples before any official-facing action.
```

## 7. Dependency issue against official upstream master

Current official upstream master observation:

```text
IBIS-IP_TicketValidationService_V2.4.xsd includes:
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Integration-branch observation:

```text
IBIS-IP_TicketValidationService_V2.4.xsd includes:
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Interpretation:

```text
The integration branch deliberately aligns TVS V2.4 to the V2.4 dependency family.
This alignment is already part of the DMS V2.4 draft PR dependency-support path and must remain labelled as candidate/integration material until accepted upstream.
```

## 8. Relation to Common/Enums findings

TVS uses shared Common/Enums types. The following already known findings remain relevant when these shared types are used by TVS:

```text
CE-005 TripInformation AdditionalTextMessage cardinality mismatch.
CE-007 VehicleModeEnumeration PDF Air vs XSD air.
CE-011 Connection-related common structure findings if referenced indirectly.
CE-015 / CE-017 visual-only pending checks if relevant via shared StopInformation / point structures.
```

Do not duplicate Common/Enums findings as TVS findings unless TVS introduces a service-specific mismatch.

## 9. First-pass result

```text
TVS V2.2 -> V2.3: no XSD schema delta observed; V2.3 is treated as a documentation correction.
TVS V2.4: new short-haul operation/data structure is present and structurally aligned with the V2.4 PDF data table.
TVS-001 opened: new short-haul operation is missing from the operation group.
TVS-002 opened: VehicleData.RouteDeviation PDF type name differs from XSD type name.
No XSD changes made.
```

## 10. Remaining technical validation tasks

Carry to validation backlog:

```text
Compile TVS V2.4 with common V2.4 / Enumerations V2.4.
Positive sample: GetCurrentShortHaulStopsResponse with empty CurrentTariffStop list.
Positive sample: GetCurrentShortHaulStopsResponse with multiple CurrentTariffStop entries.
Operation inventory check: compare top-level TicketValidationService.* elements against TicketValidationServiceOperations group.
VehicleData sample: verify RouteDeviationEnumeration use.
```

## 11. Next step

Next non-visual audit direction:

```text
Either continue TVS cross-version detail with V2.1/V2.2 PDF history,
or move to the next high-value service block: CustomerInformationService V2.3/V2.4.
```
