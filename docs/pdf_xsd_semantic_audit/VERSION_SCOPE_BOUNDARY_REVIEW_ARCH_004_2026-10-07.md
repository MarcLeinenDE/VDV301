# Version-scope boundary review — ARCH-004 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-004` is a confirmed non-defect/context finding. VDV 301-1 establishes a non-safety-system boundary and a general requirement for adequate protection against unauthorized intrusion, but it does not define a concrete TLS version, certificate model or cipher suite.

The canonical German V1.0 source remains the normative, byte-pinned, visible-body-verified locator authority.

## Publication-lineage check
The current VDV IP-KOM-ÖV publication index lists only the German VDV 301-1 and its English translation. No later VDV 301-1 architecture version is listed.

The English document identifies itself as a translation of the German V1.0 document released January 2014 and states that the German original prevails.

## Independent English-language control
The English V1.0 text independently confirms both material ARCH-004 points:

- Scope: the presented architecture/applications are for non-safety-related systems; safety-related systems may be linked through defined interfaces while side effects/interference must be excluded.
- System security: IBIS-IP must be protected with contemporarily adequate safeguards against unauthorized intrusion; safety-relevant interfaces must prevent adverse failure.

The English text does not define a TLS version, certificate hierarchy/model or cipher suite.

The interactive screenshot path for the English PDF returned cache-miss and direct external byte download was unavailable. Therefore English remains a content-level supporting language control and is not promoted to a new visible-body locator lane.

## Boundary conclusion
- predecessor architecture publication: none available;
- first/last applicable version: V1.0;
- successor architecture publication: none available;
- German: normative original;
- English: same V1.0 security/non-safety semantics independently confirmed; German original prevails.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
Do not synthesize a concrete cryptographic hard-fail profile from ARCH-004. Specific TLS, certificate or cipher requirements require a separate explicit applicable authority.
