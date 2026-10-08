# Version-scope boundary review — CIS-002 — 2026-10-08

Status: **verified / non-defect / scope unchanged**.

## Finding
The missing CIS-local Subscribe/Unsubscribe entries are **intentional shared modelling**, not a schema defect. The byte-pinned official CIS V2.0, V2.2 and V2.3 PDFs explicitly direct SubscribeAllData/UnsubscribeAllData request and response structures to VDV 301-2-1/Common. Each corresponding official Common XSD supplies the generic SubscribeRequest, SubscribeResponse, UnsubscribeRequest and UnsubscribeResponse structures.

## Lower boundary
CIS V1.1 has an unresolved strict release-XSD authority (CIS-001); it cannot be promoted or used to infer a V2.x conformance rule. CIS V2.0 is the earliest *source-verified official service profile within this finding*. Its PDF explicitly delegates subscription structures to Common and its exact official Common V2.0 dependency provides them.

## Internal release continuity
- CIS V2.0: official `VDV-301-2.0` CIS XSD `fa8f0a51ad5f612660c9532c8557ad1ca473a908`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`.
- Global `VDV-301-2.1` release tree **retains the exact CIS V2.0 XSD** (same blob). This is not a distinct CIS V2.1 service schema.
- CIS V2.2: official CIS blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e`, Common `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`.
- CIS V2.3: official CIS blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e`, Common `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`.

PDF body locators are pinned in `SOURCE_LOCATOR_REVIEW_CIS_002_2026-10-06.md` (V2.0 printed p.13; V2.2/V2.3 printed p.14).

## Upper boundary
The VDV IP-KOM-ÖV publication index checked on 2026-10-08 lists CIS service publications V1.1, V2.0, V2.2, V2.3, not an official CIS V2.4 PDF (https://www.vdv.de/ip-kom-oev.aspx). A selected candidate/integration CIS V2.4 XSD exists, but cannot silently establish a new *official PDF-based* CIS-002 version claim.

## Conclusion and SDK
No version-scope correction and **no provider failure** for absence of CIS-specific duplicate Subscribe/Unsubscribe XSD entries. Keep `non_defect` and `no_runtime_diagnostic`. Use the Common structures prescribed by the exact selected release route. No XSD mutation or artificial aliases.
