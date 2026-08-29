# AUDIT HANDOFF DELTA - VideoDisplayService V2.0 Deep Read

Date: 2026-08-29
Branch: `dev/schema-integration`
Clean head before closure: `93c0fe6e927724e335a49973f37be330201c8f13`

## Completed document

`VDS_V2.0` - VDV-Schrift 301-2-13 VideoDisplayService V2.0, 08/2019.

Official PDF pin:

```text
SHA-256: c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2
size: 903,444 bytes
pin run: 33226181059
```

Pinned visual evidence:

```text
render run: 33226294383
engine: PyMuPDF 1.28.2
pages: 4,6,11,12,13,14,15,16
artifact digest: sha256:a8f9a098f7bbf534d41c1586230a45518ada62c67482494d8ba9b0debb617fb1
```

Status: `needs_visual_review` because material findings are visually confirmed but an all-page/all-figure pass is not complete.

## Exact XSD authority

After the independent PDF fresh read, the official `VDV-301-2.0` service XSD was selected.

```text
IBIS-IP_VideoDisplayService_V2.0.xsd
Git blob: fcfdadd3b62a584370cae326004050b4dc832e23
includes: Common V2.0 + Enumerations V2.0
```

The integration-branch copy has the same Git blob. No newer/candidate schema was substituted.

## Executable evidence

EV-103 / run `33111119723` applies directly to the same selected V2.0 service schema.

```text
VDS-002 ViewCapabilities multi-field PDF record -> rejected by xs:choice
VDS-003 ViewID + Timeout PDF request -> rejected by xs:choice
VDS-004 grouped response fields -> rejected by xs:choice after first member
```

All remain executable-confirmed. No XSD change is made.

## Finding history

```text
VDS-001 V1.0 provenance gap only; unaffected
VDS-002 fresh PDF/XSD + EV-103 confirmed
VDS-003 fresh PDF/XSD + EV-103 confirmed
VDS-004 fresh PDF/XSD + EV-103 confirmed
VDS-005 corrected/absent in V2.0
VDS-006 malformed -1:1 notation persists
VDS-007 cross-document VDS v1.1 reference issue remains resolved; no V1.1 profile
VDS-008 new: RTP/SOA abbreviation expansions are technically wrong in V1.0/V2.0
```

VDS-008 reference terminology:

```text
PDF: RTP = Real Time Protocol
RFC 3550: RTP = real-time transport protocol / A Transport Protocol for Real-Time Applications

PDF: SOA = Server Oriented Architecture
OASIS SOA Reference Model: SOA = Service Oriented Architecture
```

No XML validation behavior is derived from these wrong expansions.

## Compatibility authority note

The V2.0 writing says the service is compatible/compliant with VDV301 versions 1.0 and 2.x. This does not authorize validation of the unresolved VDS V1.0 schema lane with the V2.0 XSD.

## Repository files in closure

```text
docs/pdf_xsd_semantic_audit/deep_read/VDS_V2.0.md
audit_registry/deep_read_findings_delta_vds_v20_2026-08-29.json
audit_registry/deep_read_registry_delta_vds_v20_2026-08-29.json
docs/pdf_xsd_semantic_audit/VIDEO_DISPLAY_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
00_START_HERE/CURRENT_STATE.json
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VDS_V20_DEEP_READ_2026-08-29.md
```

No XSD file belongs in the closure commit.

## Next document

Registry/catalog order after VDS is `TRAINSET_V2.1`.

Required order:

1. Byte-pin the official TrainSet V2.1 PDF.
2. Fresh-read it independently.
3. Establish exact TrainSetMasterData/TrainSetData operation inventories and XSD dependency families.
4. Only after the independent read, compare TSM-002/TSD-003 and EV-104.
5. Then continue to TrainSet V2.2.

Standing rules remain unchanged: no fork `master` modification, no PR/comment/merge/upstream action without explicit approval, no XSD modification merely because PDF and XSD differ, and no latest-version substitution.
