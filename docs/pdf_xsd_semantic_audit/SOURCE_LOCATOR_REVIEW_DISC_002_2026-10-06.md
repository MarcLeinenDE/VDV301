# Source-locator review — DISC-002 — 2026-10-06

Status: **structurally complete / visible-body verified / external-reference defect preserved**.

## Finding

DISC-002 is a confirmed documentation reference error: affected VDV 301-2 passages associate **RFC 2927** with automatic IPv4 Link-Local / 169.254 addressing, although RFC 2927 is not an IPv4 Link-Local specification.

No XML/XSD conformance rule applies.

## Visible VDV evidence

### V1.0 German

Source: `VDV301-2_V1.0_DE`

- printed page **20**, section `2.1.1 IP-Adressen`: visible text cites **RFC 2927** in the context of automatic `169.254.xxx.xxx` addressing.
- printed page **80**, `Regelwerke – Normen und Empfehlungen`: the same document visibly identifies:
  - `RFC 2927`
  - `MIME Directory Profile for LDAP Schema`

The contradiction is therefore already internally demonstrable within the V1.0 publication.

### V2.0 / V2.1

- `VDV301-2_BASE_V2.0`, printed page **21**
- `VDV301-2_BASE_V2.1`, printed page **22**

The visible English text continues to cite RFC 2927 for ZeroConf / `169.254.xxx.xxx` link-local addressing, while the German track uses RFC 3927.

### General Conventions V2.2 / V2.3 / V2.4

Affected English tracks visibly retain the same RFC 2927 reference in their IP-addressing text:

- V2.2 printed page **20**
- V2.3 printed page **20**
- V2.4 printed page **23**

## External standard provenance

Official RFC Editor provenance confirms:

- **RFC 2927** — `MIME Directory Profile for LDAP Schema`
- **RFC 3927** — `Dynamic Configuration of IPv4 Link-Local Addresses`

RFC 3927 explicitly covers automatic IPv4 Link-Local addressing in the `169.254/16` prefix.

## Active disproof

Rejected counter-hypothesis: RFC 2927 might be an older or alternative IPv4 Link-Local specification.

It is not. Its title and content concern an LDAP schema MIME directory profile. The VDV V1.0 bibliography itself already confirms that identity.

## Classification boundary

This finding corrects an **external reference number**, not the policy question of whether VDV universally requires ZeroConf / 169.254.

Therefore:

- DISC-002 confirms RFC 2927 is the wrong technical reference.
- DISC-001 remains controlling for the German/English semantic conflict and whether any universal allocation requirement can be inferred.

## SDK consequence

Documentation-only warning:

- do not use RFC 2927 as technical basis for IPv4 Link-Local;
- cite RFC 3927 as the technically relevant standard when explaining the reference defect;
- do not turn that correction into a universal VDV allocation mandate;
- no XSD validation behavior is changed.

Existing semantic classification and runtime state remain unchanged.
