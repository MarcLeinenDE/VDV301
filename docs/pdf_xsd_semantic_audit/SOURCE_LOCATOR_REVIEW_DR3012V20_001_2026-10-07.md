# Source-locator review — DR3012V20-001 — 2026-10-07

Status: **complete / visible-body verified / bilingual contradiction verified / external authority preserved**.

## Finding

VDV 301-2 Base V2.0 gives different RFC references in the German and English tracks for the same ZeroConf / IPv4 link-local behavior.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`

### Page 21 — bilingual body text

Visible section:
- `2.1 Adressierung / Addressing`
- `2.1.1 IP-Adressen / IP Addresses`

German cites `RFC 3927` for ZeroConf automatic addressing and names the `169.254.xxx.xxx` range.

English describes the same behavior and same address range but cites `RFC 2927`.

Exact-byte page-21 PNG SHA-256:
`30d0cdb4e77b5f8aedec7a46fb2ac68d98ef8b21dc262e25f80bbe5e41e953cf`

### Page 110 — bibliography

Visible heading:
- `Regelwerke – Normen und Empfehlungen`

Visible entry (13):
- `RFC 3927 — Dynamic Configuration of IPv4 Link-Local Addresses`

Exact-byte page-110 PNG SHA-256:
`7544bb9c0d39d842e653f244c084d5b78cfa8e01efbbb3726b907d18f646ed4b`

## External authority

- RFC 3927 is the IPv4 Link-Local specification for the 169.254/16 prefix.
- RFC 2927 is an LDAP-schema MIME profile and does not define IPv4 link-local addressing.

## Disproof attempt

The mismatch cannot be explained as two different technical rules because both language tracks describe the same automatic addressing behavior and the same 169.254 range on the same page. The document's own bibliography independently aligns with the German RFC 3927 reference.

## Classification and SDK behavior

Confirmed bilingual documentation/reference defect.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable**
- runtime matcher: **not applicable**
- SDK behavior: **warning / protocol guidance**
- the English RFC 2927 citation must not be elevated into a separate technical profile.

The language variants remain preserved as evidence rather than silently reconciled.
