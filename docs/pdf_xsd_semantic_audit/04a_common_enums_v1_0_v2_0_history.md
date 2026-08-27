# Common/Enums V1.0 -> V2.0 history audit

Status: started, XSD-side first observation completed.

Scope:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
VDV 301-2-1 Common Data Structures and Enumerations V1.0 / V2.0 PDF side, still to be checked in detail
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.0 Common/Enums definitions to a V1.0 service payload unless the selected service/dependency pool actually uses V2.0.
V1.0 and V2.0 must stay separately validatable.
```

## 1. XSD dependency family observation

### Common/Enums V1.0

Observed:

```text
IBIS-IP_common_V1.0.xsd includes IBIS-IP_Enumerations_V1.0.xsd.
```

### Common/Enums V2.0

Observed:

```text
IBIS-IP_common_V2.0.xsd includes IBIS-IP_Enumerations_V2.0.xsd.
```

Initial result:

```text
V1.0 and V2.0 each have their own common/enumeration dependency family in the branch.
No V1.0/V2.0 include-family mismatch is opened in this first observation.
```

## 2. Initial enumeration-history observation

The V2.0 enumeration XSD contains an internal comment indicating relevant edits:

```text
Video services added in ServiceNameEnumeration.
Video enumerations removed.
DeviceStateEnumeration extended by readyForShutdown.
Date in comment: 2018-01-22.
```

This is XSD-side evidence only. It is not yet a PDF/XSD finding.

Pending PDF-side check:

```text
Confirm whether VDV 301-2-1 V2.0 PDF version history and enumeration tables reflect these changes.
```

## 3. First classification

Status so far:

```text
OK to continue.
No new CE finding opened from V1.0 -> V2.0 first observation.
```

Potential historical closure targets:

```text
ServiceNameEnumeration video-service additions.
DeviceStateEnumeration readyForShutdown introduction.
Removal/relocation of video-specific enumerations.
Any type/cardinality changes in shared structures that later services depend on.
```

## 4. Next work inside this block

Required next steps:

```text
1. Generate/record XSD enumeration inventories for V1.0 and V2.0 using the exporter.
2. Compare V1.0 vs V2.0 XSD enumeration values.
3. Extract/check V1.0 and V2.0 PDF enumeration tables.
4. Record whether the XSD comment deltas are also visible in the PDF tables/version history.
5. Only then decide whether historical CE finding ranges need updates.
```

## 5. Validation backlog impact

Later technical validation should include version-specific pools:

```text
Common/Enums V1.0 pool:
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_Enumerations_V1.0.xsd

Common/Enums V2.0 pool:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
```

The pools must be compiled separately.

## 6. Result

```text
Common/Enums V1.0 -> V2.0 historical audit has started.
XSD-side dependency-family observation is clean for V1.0 and V2.0.
V2.0 XSD comment suggests concrete enumeration changes to verify against the PDF.
No new finding opened yet.
```