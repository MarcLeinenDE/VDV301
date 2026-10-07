# Version-scope boundary review — ARCH-002 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-002` is a confirmed non-defect/context finding. The architecture hierarchy describes higher functional components as active information users (client role) and lower components as passive information providers (server role). This general architecture model must not be promoted into a rigid protocol rule for every concrete service interaction.

The canonical German V1.0 source-locator remains the normative, byte-pinned, visible-body-verified authority.

## Publication-lineage check
The current VDV IP-KOM-ÖV publication index lists one German VDV 301-1 publication and one English VDV 301-1 translation. No later VDV 301-1 architecture version is listed.

The English document explicitly identifies itself as a translation of the German V1.0 document released January 2014, has no legal effect, and states that the German original prevails.

## Independent English-language control
The English page-14 text independently states:
- lower functional components provide data to higher functional components;
- higher functional components are active information users in the client role;
- those clients retrieve data from passive information providers in the server role;
- the following bullets describe the associated service-knowledge asymmetry.

This matches the German ARCH-002 source meaning.

The interactive screenshot path for the English PDF returned cache-miss and direct external byte download was unavailable. Therefore English remains a content-level supporting language control and is not promoted to a new visible-body locator lane.

## Boundary conclusion
- predecessor architecture publication: none available;
- first/last applicable version: V1.0;
- successor architecture publication: none available;
- German: normative original;
- English: same V1.0 semantics independently confirmed; German original prevails.

Semantic scope remains `V1.0 / documentation_only`.

## Consequence
Do not hard-code the architecture hierarchy as a universal request/callback/subscription direction rule. Concrete service communication remains governed by the applicable Part-2/Common-Conventions authority.
