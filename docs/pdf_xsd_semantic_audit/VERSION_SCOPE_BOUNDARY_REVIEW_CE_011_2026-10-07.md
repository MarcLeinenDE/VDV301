# Version-scope boundary review — CE-011 — 2026-10-07

Status: **verified / corrected scope confirmed unchanged**.

## Finding
`CE-011` is the Connection cardinality mismatch: from V2.2 onward the PDF documents `TransportMode` and `ConnectionMode` as `0:*`, while the exact selected Common XSDs declare each with `minOccurs="0"` and no `maxOccurs`, therefore effective `0:1`.

## Lower boundary
Common V2.1 is the explicit unaffected predecessor:
- its PDF documents `TransportMode` as `0:1`;
- exact Common V2.1 declares `TransportMode` with effective `0:1`;
- `ConnectionMode` is not yet present.

V2.2 is the first affected release. It introduces the later ConnectionMode/NetexMode path, while the PDF changes the two Connection mode fields to `0:*` and the XSD keeps each at effective `0:1`.

## Continuity
- V2.3 preserves the same PDF/XSD cardinality mismatch.
- V2.4 official PDF still documents `0:*`; the selected candidate/integration Common V2.4 XSD still constrains each field to effective `0:1`.

## Boundary conclusion
Existing corrected scope is confirmed unchanged:
1. Common V2.2-V2.3 — official release authority;
2. Common V2.4 — candidate/integration authority.

V2.1 and earlier are outside CE-011.

## SDK consequence
Repeated `Connection.TransportMode` or `Connection.ConnectionMode` entries remain XSD-invalid in the affected profiles. The SDK must reject them according to the exact selected XSD and may attach CE-011 as an explanation of the differing PDF cardinality.
