# Source-locator review — DR3012V20-002 — 2026-10-07

Status: **complete / visible-body verified / RFC 2782 contradiction confirmed**.

## Finding

VDV 301-2 Base V2.0 describes DNS-SRV Weight selection incorrectly in both language tracks.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`

### Page 33 — German

Visible table:
- `Tabelle 3 Bedeutungen der SRV-Records in DNS-SD`

The visible `Weight` row states that the service with the lower Weight is preferred.

Page-33 PNG SHA-256:
`ab523621ba1f0c9bc3eb338b4e084e067feae0abd2af7ac57e7394bf07133b53`

### Page 34 — English

Visible table:
- `Table 4: Meanings of the SRV record in DNS-SD`

The visible `Weight` row likewise says the service with the lower Weight is preferred.

Page-34 PNG SHA-256:
`5a11906f6aa7ad965389ae406d0ce0fa6c3dbd16c3be83083d6724e8d59b924f`

## External authority

RFC 2782 defines Weight for records at the same Priority. Larger Weight values receive proportionately higher probability of selection.

## Disproof attempt

The wording is not limited to one translation; both German and English carry the same reversed Weight semantics. The Priority row immediately above correctly uses the lower-value preference for Priority, which further supports a copy/semantic carryover into the Weight row.

## Classification and SDK behavior

Confirmed documentation/external-protocol contradiction.

- XML/XSD validity behavior: **unchanged**
- runtime matcher: **not applicable**
- SDK behavior: **warning / protocol guidance**
- lower numeric Priority remains preferred;
- Weight selection follows RFC 2782 rather than the PDF wording.
