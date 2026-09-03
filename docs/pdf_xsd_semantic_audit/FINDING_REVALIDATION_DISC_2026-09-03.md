# Finding revalidation - DISC-001..DISC-003

Date: 2026-09-03
State: completed under current `FINDING_EVIDENCE_GATE.md`
Evidence: `EV-126` (run `33754189273`)
Source pin/render run: `33752224704`, job `100638164877`, artifact `9892036202`
Artifact digest: `sha256:263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030`

## Authority lane

These findings are non-XSD discovery/documentation findings. The authoritative evidence is the exact official VDV publication by version/language plus RFC Editor definition provenance where an external RFC number is being classified. No XML schema contract is inferred from this block.

Four previously unpinned General-Conventions/Base-Service sources were freshly retrieved and pinned during this revalidation. V2.3 and V2.4 were also re-fetched and matched their existing pins byte-for-byte.

## DISC-001 - German/English IP-address allocation conflict

Terminal state: `context_verified`.

Visible exact-source evidence establishes the version chain:

- V1.0 German page 20 uses ZeroConf, RFC 2927 and 169.254.xxx.xxx.
- V2.0 page 21 and V2.1 page 22 use RFC 3927 in German but RFC 2927 in English for the same link-local rule.
- V2.2 pages 17/20, V2.3 pages 17/20 and V2.4 pages 20/23 are materially divergent: German says there are no prescribed IP-address allocation rules and gives fixed IP/DHCP as best practice; English retains ZeroConf, RFC 2927 and 169.254.xxx.xxx requirements.

Strongest counter-hypothesis rejected: this is not merely a wrong RFC number in an otherwise equivalent translation. The V2.2+ language tracks state different allocation semantics.

SDK consequence retained: do not hard-enforce ZeroConf or 169.254/16 as a universal VDV requirement from the stale English track alone. Preserve version/language provenance when reporting the conflict.

## DISC-002 - RFC 2927 reference mismatch

Terminal state: `context_verified`.

V1.0 page 20 cites RFC 2927 for automatic 169.254 addressing; the same publication's page 80 bibliography labels RFC 2927 `MIME Directory Profile for LDAP Schema`. Official RFC Editor definition provenance independently confirms:

- RFC 2927: MIME Directory Profile for LDAP Schema.
- RFC 3927: Dynamic Configuration of IPv4 Link-Local Addresses, including 169.254/16.

Strongest counter-hypothesis rejected: RFC 2927 is not an alternate IPv4 Link-Local specification.

This remains a reference-number/documentation finding only. It does not independently turn RFC 3927 into a universal VDV allocation requirement and does not override DISC-001.

## DISC-003 - V2.4 German DNS-SD table repair

Terminal state: `context_verified`.

V2.4 page 75 explicitly records that missing entries in the German version of Table 3 were added. The visible table comparison confirms the repair is real:

- V2.3 German Table 3 page 27 ends after the earlier attributes and lacks `coachnumber`, `deviceclass` and `deviceID`.
- V2.4 German Table 3 pages 30-31 contains `coachnumber`, `deviceclass` and `deviceID`.

Strongest counter-hypothesis rejected: the V2.4 history note is not merely editorial wording without a corresponding document change.

## Executable-evidence decision

No XML-validity, schema-shape, compositor, cardinality, enum or root behavior is claimed by DISC-001..003. Therefore XSD executable validation is not applicable. EV-126 is a deterministic exact-source/RFC-provenance evidence check, not an XSD conformance test.

No XSD changed. The frozen 192-finding inventory remains immutable.

Next revalidation block: `DMS`.
