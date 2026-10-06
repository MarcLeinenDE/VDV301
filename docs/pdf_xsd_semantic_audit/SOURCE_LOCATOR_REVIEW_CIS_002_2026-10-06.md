# Source-locator review — CIS-002 — 2026-10-06

Status: **structurally complete / visible-body verified / confirmed non-defect** under the current audit workflow contract.

## Finding

CIS-002 records an earlier interpretation that Subscribe/Unsubscribe might be missing from the CIS-specific XSD operation group. Revalidation shows that this interpretation is incorrect: the CIS documents explicitly delegate the subscription request/response structures to VDV 301-2-1/Common.

Affected review lanes: **CIS V2.0, V2.2 and V2.3**, all with official release XSD authority.

## Visible PDF body

Exact official byte-pinned PDFs from CIS evidence artifact `9885887536` were used. The web PDF renderer was also attempted as required; where it cache-missed, the exact pinned rendered artifact was used as the deterministic fallback.

- **CIS V2.0, printed page 13**
  - `1.5 Data Structures of SubscribeAllData Operation`
  - `1.6 Data Structures of UnsubscribeAllData Operation`
  - The visible body says the subscription data structures described in **VDV 301-2-1** are used, explicitly naming `SubscribeRequest` / `SubscribeResponse`, and likewise `UnsubscribeRequest` / `UnsubscribeResponse`.

- **CIS V2.2, printed page 14**
  - `1.6 Data Structures of SubscribeAllData Operation`
  - `1.7 Data Structures of UnsubscribeAllData Operation`
  - Same explicit delegation to VDV 301-2-1/Common.

- **CIS V2.3, printed page 14**
  - `1.6 Data Structures of SubscribeAllData Operation`
  - `1.7 Data Structures of UnsubscribeAllData Operation`
  - Same explicit delegation to VDV 301-2-1/Common.

These are direct visible-body statements, not TOC-derived inferences.

## Exact XSD authority

### CIS V2.0

- `VDVde/VDV301@VDV-301-2.0`
- CIS: `IBIS-IP_CustomerInformationService_V2.0.xsd`
- blob: `fa8f0a51ad5f612660c9532c8557ad1ca473a908`
- `CustomerInformationServiceOperations`: lines 7–20.
- Common: `IBIS-IP_common_V2.0.xsd`
- blob: `8608e3dcd665c197c34da7f6ec6af5a3758da164`
- generic Subscribe/Unsubscribe structures: lines 867–892.

### CIS V2.2

- `VDVde/VDV301@VDV-301-2.2`
- CIS blob: `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`
- Common blob: `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`
- Common generic structures: lines 875–912.

### CIS V2.3

- `VDVde/VDV301@VDV-301-2.3`
- CIS blob: `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`
- Common blob: `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`
- Common generic structures: lines 955–992.

For every lane, the CIS-specific `CustomerInformationServiceOperations` group does not duplicate Subscribe/Unsubscribe structures, while the exact selected Common dependency contains the generic structures the PDF explicitly references.

## Active disproof

The strongest alternative interpretation was: “If Subscribe/Unsubscribe are listed as CIS operations in the PDF, their absence from `CustomerInformationServiceOperations` means the CIS XSD is incomplete.”

That interpretation fails because the body text explicitly says those operations use the data structures from VDV 301-2-1/Common. The Common dependency provides exactly those structures. Therefore no missing CIS-specific alias or structure can be inferred.

## Classification and SDK consequence

Classification remains **non-defect / intentional shared modelling**.

- no XSD correction;
- no runtime diagnostic;
- no provider failure merely because no CIS-specific duplicate exists;
- use the generic Common Subscribe/Unsubscribe structures prescribed by the selected release context.

The selected XSD remains normative for executable conformance. This review changes no semantic scope, runtime mapping or XSD bytes.
