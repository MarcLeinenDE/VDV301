# Source-locator review — DR3012-001 — 2026-10-06

Status: **complete / visible-body verified / external primary authority verified / documentation reference defect confirmed**.

## Finding

VDV 301-2 V1.0 cites RFC 2927 in the IP-addressing paragraph for ZeroConf-style automatic `169.254.xxx.xxx` addressing. RFC 2927 is unrelated to IPv4 Link-Local addressing; RFC 3927 is the applicable IPv4 Link-Local specification.

## Visible VDV evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **20**
- visible body anchors:
  - **2 Verwendete Kommunikationsprotokolle**
  - **2.1 Adressierung**
  - **2.1.1 IP-Adressen**

The visible paragraph states that IP addresses in IBIS-IP are assigned decentrally using part of "Zero Conf", cites `RFC 2927`, and then names `169.254.xxx.xxx` as the address range whose RFC requirements must be observed.

## Exact-byte visual verification

EV-129:
- closure run: `33765633886`
- pinned evidence run: `33765167655`
- artifact: `9897171006`
- artifact digest: `sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7`
- page-20 PNG SHA-256: `f47019ea03dcccdb4277894ee82af43aa290b781fbd4e963385e21ceadedb949`

The page hash was freshly recomputed from the exact EV-129 artifact during this review.

## External primary-authority cross-check

RFC Editor primary sources:

- RFC 2927: **MIME Directory Profile for LDAP Schema** — an LDAP schema MIME profile, not an IPv4 Link-Local addressing specification.
- RFC 3927: **Dynamic Configuration of IPv4 Link-Local Addresses** — explicitly describes automatic interface configuration in the `169.254/16` prefix.

Primary URLs:
- https://www.rfc-editor.org/rfc/rfc2927.html
- https://www.rfc-editor.org/rfc/rfc3927.html

## Disproof attempt

The VDV text does not merely cite RFC 2927 in an unrelated bibliography entry: the citation is embedded directly in the ZeroConf/IP-addressing sentence and is immediately connected to the `169.254.xxx.xxx` address range. RFC 2927's subject matter cannot explain that usage. RFC 3927 directly matches both the automatic IPv4 Link-Local behavior and the 169.254/16 prefix.

## Classification and SDK behavior

Confirmed PDF/documentation reference defect.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable**
- runtime matcher: **not applicable**
- SDK behavior: **informational/context only**
- no alias, normalization or executable XML rule is introduced.

The finding remains version-specific historical documentation evidence.
