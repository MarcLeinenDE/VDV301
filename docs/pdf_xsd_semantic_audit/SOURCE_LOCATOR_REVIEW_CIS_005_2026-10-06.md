# Source-locator review — CIS-005 — 2026-10-06

Status: **structurally complete / visible-body verified / executable mismatch preserved**.

## Finding

CIS-005 is a confirmed PDF-internal type contradiction in CustomerInformationService V2.2 and V2.3.

The same field, `MyOwnVehicleMode`, is documented with two incompatible types:

- Table 3 / AllData: `NetexMode`
- Table 17 / VehicleData: `PtModesEnumeration`

The selected official XSD defines `MyOwnVehicleMode` as `NetexMode`. The selected XSD therefore resolves the documentation contradiction and remains normative.

## Visible PDF body

Exact byte-pinned CIS PDFs from evidence artifact `9885887536` were visually checked.

### CIS V2.2

- PDF SHA-256: `789abcd3ea9b42ef7393b09484bfd5257e20a069dbd7d1ca99409fc80a5e76f0`
- printed page **14**, visible **Table 3: Description ofCustomerInformationService.AllData**:
  - `MyOwnVehicleMode`
  - cardinality `0:1`
  - type `NetexMode`
- printed page **20**, visible **Table 17: Description of CustomerInformationService.VehicleData**:
  - the same field `MyOwnVehicleMode`
  - cardinality `0:1`
  - type `PtModesEnumeration`

### CIS V2.3

- PDF SHA-256: `b9e057a96dfbd824e18b4ace0958a6f80f62cd853ad6360bc2c76ea5db837f87`
- printed page **14**, Table 3: `MyOwnVehicleMode 0:1 NetexMode`
- printed page **20**, Table 17: `MyOwnVehicleMode 0:1 PtModesEnumeration`

The contradiction is therefore visible inside each affected official document, not inferred from another version.

## Exact XSD authority

### V2.2

- `VDVde/VDV301@VDV-301-2.2`
- CIS file `IBIS-IP_CustomerInformationService_V2.2.xsd`
- blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`
- line 221: `<xs:element name="MyOwnVehicleMode" type="NetexMode" minOccurs="0">`

Selected Common dependency:

- `IBIS-IP_common_V2.2.xsd`
- blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`
- `NetexMode` at lines 956–970 is a structured complex type with main-mode/submode choices.

### V2.3

- `VDVde/VDV301@VDV-301-2.3`
- CIS blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`
- line 221 again defines `MyOwnVehicleMode` as optional `NetexMode`.

Selected Common dependency:

- `IBIS-IP_common_V2.3.xsd`
- blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`
- `NetexMode` at lines 1036–1050 is structured.

## Scope disproof

CIS V2.0 was checked independently. `MyOwnVehicleMode` is not present in the selected V2.0 CIS XSD, so V2.0 is correctly excluded from the affected semantic/runtime scope.

## Executable evidence

EV-125, run `33744039627`, already proves for V2.2/V2.3:

- structured `NetexMode` content → valid;
- scalar text form corresponding to the PDF `PtModesEnumeration` interpretation → invalid.

## Classification

Confirmed **PDF defect / internal semantic contradiction**.

The authoritative executable rule is:

```text
MyOwnVehicleMode -> NetexMode
```

for CIS V2.2 and V2.3.

## SDK consequence

Existing runtime mapping remains correct:

- selected strict profile must be CIS V2.2 or V2.3;
- selected XSD must already have rejected the submitted scalar form;
- advisory explains the PDF contradiction;
- validation result remains **INVALID**;
- no scalar compatibility alias or normalization is allowed.

No XSD bytes, semantic scope or runtime mapping were changed.
