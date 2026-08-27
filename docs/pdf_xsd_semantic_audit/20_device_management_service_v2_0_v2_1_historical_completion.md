# DeviceManagementService V2.0 / V2.1 historical completion

Status: historical semantic/provenance first pass completed for V2.0 and V2.1. Together with existing blocks 02/02a, the DMS V2.0-V2.4 first-pass chain is now complete. Local XSD compilation/sample validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
e6b0431f93cb90118c8082bc7a4157f6f1cff611
```

Existing later-history sources retained:

```text
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
docs/pdf_xsd_semantic_audit/02a_dms_v2_2_v2_3_v2_4_history_compare.md
```

## 1. Official historical backfill

The integration branch lacked the two older official DMS service schemas.

They are restored unchanged from official VDVde/VDV301 release tags:

```text
VDV-301-2.0
  IBIS-IP_DeviceManagementService_V2.0.xsd
  blob 74189e0da65563eeb084ec2f3c400e9668d1ee1a

VDV-301-2.1
  IBIS-IP_DeviceManagementService_V2.1.xsd
  blob 191b43e01cdaba14b247725689a913c244a67eed
```

Classification:

```text
historical official release material
not candidate material
not a schema correction
```

No content is changed during import.

## 2. Exact dependency routing

```text
DMS V2.0
  -> Common V2.0
  -> Enumerations V2.0

DMS V2.1
  -> Common V2.1
  -> Enumerations V2.1

DMS V2.2
  -> Common V2.2
  -> Enumerations V2.2

DMS V2.3 integration comparison material
  -> Common V2.3
  -> Enumerations V2.2

DMS V2.4 candidate/integration
  -> Common V2.4
  -> Enumerations V2.4
```

Do not substitute another pool merely because it is newer.

## 3. V2.0 -> V2.1 functional delta

The official V2.1 document history explicitly lists two functional extensions of DeviceManagementService:

```text
- detailed device status including support for independent subdevices
- operations implementing the update procedure
```

The V2.1 XSD reflects those extensions with subdevice information/status/error structures and the InstallUpdate/RetrieveUpdateState/GetUpdateHistory/Finalize update operation family.

The V2.1 history says there were no additional technical corrections for V2.1.

## 4. DMS-001 - V2.0 PDF operation inventory vs service-XSD modelling

The public V2.0 operation table already lists, among others:

```text
Subscribe/Unsubscribe DeviceInformation
Subscribe/Unsubscribe DeviceConfiguration
Subscribe/Unsubscribe DeviceStatus
Subscribe/Unsubscribe DeviceErrorMessages
RestartDevice
DeactivateDevice
ActivateDevice
Subscribe/Unsubscribe ServiceInformation
Subscribe/Unsubscribe ServiceStatus
StartService / StopService / RestartService with generic DataAccepted responses
```

The official V2.0 `DeviceManagementServiceGroup` contains only ten service-specific request/response declarations and omits the generic subscription/control response operation entries.

More importantly, the V2.0 service XSD contains no `ActivateDevice` or `DeactivateDevice` element declarations at all, although the PDF documents both operations and generic DataAccepted responses. `RestartDeviceResponse` exists globally, but RestartDevice is not represented in the V2.0 service group.

V2.1 reorganizes the operation group and includes the generic subscribe/unsubscribe, activate/deactivate/restart and response operation names.

Classification:

```text
finding: DMS-001
classification: service_modelling_or_generic_response_candidate
confidence: high for the inventory difference; medium for whether every omission constitutes an XSD defect
validation_behavior: V2.0 validation follows V2.0 XSD exactly; do not borrow V2.1 roots/groups
```

Reason for conservative classification:

```text
Many omitted V2.0 operations use generic Common response/subscription structures.
The V2.0 group may have been intended as a service-specific payload inventory rather than a complete operation registry.
However, ActivateDevice/DeactivateDevice are documented operations with no service XSD elements in the V2.0 file, so the mismatch is operationally relevant and must remain visible.
```

Technical root/group validation is required before stronger classification.

## 5. DMS-002 - V2.0 unresolved document cross-references

The V2.0 PDF contains repeated literal Word-generation errors:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

They appear in DMS tables/descriptions, including references for DeviceInformation, DeviceState, ServiceInformationList, ServiceSpecificationWithStateList and service control request descriptions.

The checked V2.1 PDF no longer contains this literal broken-reference string.

Classification:

```text
finding: DMS-002
classification: pdf_table_or_documentation_error_candidate
confidence: high
validation impact: none
```

## 6. DMS-003 - historical ErrorMessage cardinality is version-specific

V2.0 PDF and XSD both specify:

```text
GetDeviceErrorMessagesResponseData.ErrorMessage 10:*
```

V2.1 PDF and XSD continue that `10:*` rule. V2.1 additionally documents SubdeviceErrorMessages.ErrorMessage as `10:*`, matching the corresponding historical schema modelling.

V2.2 also retains the historical XSD `minOccurs="10"` state already documented in block 02a.

The later V2.4 correction changes this family to `0:*`.

Classification:

```text
finding: DMS-003
classification: ok_with_note
meaning: this is a historical semantic correction, not evidence that V2.0/V2.1 should be validated with V2.4 cardinality
```

SDK rule:

```text
DMS V2.0/V2.1/V2.2 -> enforce selected historical 10:* XSD.
DMS V2.4 candidate profile -> enforce selected 0:* XSD.
Diagnostics may explain the later correction but must not relax the historical schema.
```

## 7. DMS-004 - InstallUpdate requiredness is also version-specific

V2.1 PDF and XSD require:

```text
UpdateID        1:1
UpdateTimestamp 1:1
UpdateURL       1:1
```

while checksum and file size are optional.

The V2.4 correction makes UpdateID/UpdateTimestamp/UpdateURL optional for InstallUpdateRequest, as already audited in block 02/02a.

Classification:

```text
finding: DMS-004
classification: ok_with_note
meaning: later correction must not be retroactively applied to V2.1
```

## 8. DMS full first-pass routing result

```text
V2.0 official historical profile: restored
V2.1 official historical profile: restored
V2.2 official profile: existing
V2.3 integration comparison profile: existing, non-official
V2.4 candidate/integration profile: existing
```

No XSD change has been made.

## 9. Technical validation backlog

```text
DMS-VB-001 compile official V2.0 exact pool.
DMS-VB-002 compile official V2.1 exact pool.
DMS-VB-003 inventory V2.0 PDF operations vs service group vs global elements.
DMS-VB-004 test V2.0 generic DataAccepted/Subscribe handling to resolve DMS-001.
DMS-VB-005 verify V2.0/2.1 10:* ErrorMessage positive/negative boundaries.
DMS-VB-006 verify V2.1 SubdeviceErrorMessages 10:* boundary.
DMS-VB-007 verify V2.1 InstallUpdate required UpdateID/UpdateTimestamp/UpdateURL.
DMS-VB-008 retain existing VB-005 for V2.4 candidate correction samples.
```

No compile/sample result is claimed by this audit block.
