# Version-scope boundary review — ARCH-001 — 2026-10-07

Status: **verified / scope unchanged / English translation independently checked**.

## Finding
`ARCH-001` is a confirmed non-defect/context finding: VDV 301-1 deliberately evolves the former Master/Slave architecture into a service-oriented architecture, and service/operation roles are logical rather than permanently tied to one physical device.

The canonical German V1.0 locator remains byte-pinned and visible-body verified at printed pages 7 and 10.

## Publication-lineage check
The current VDV IP-KOM-ÖV publication index was checked on 2026-10-07. It lists exactly:
- one German `VDV 301-1 IBIS-IP, Teil 1 - Systemarchitektur`;
- one English `VDV 301-1 IBIS-IP, Part 1: System architecture`;
- no later VDV 301-1 architecture version.

The official English PDF identifies itself as a translation of the German document `... Systemarchitektur, v1.0` released in January 2014. Its disclaimer states that the translation is for convenience only, has no legal effect and that the German original applies in case of inconsistency.

## Independent English-language control
The English V1.0 text independently repeats the material ARCH-001 semantics:
- Scope: the proven Master/Slave architecture is evolved to a service-oriented architecture;
- Terminology: IBIS-IP uses a service-oriented architecture;
- Service: services run on devices, while the architecture is determined independently of the devices used.

The interactive screenshot path returned cache-miss for the English PDF and direct external byte download was unavailable in this session. Therefore the English document is **not promoted to a new visible-body source-locator lane**. This does not weaken the canonical finding: the German original remains the normative, byte-pinned, visible-body-verified authority; the English text is only an independent language-control surface.

## Boundary conclusion
- predecessor VDV 301-1 publication: none available;
- first/last applicable architecture publication: V1.0;
- successor publication: none available;
- German: normative original, finding interpretation confirmed;
- English: V1.0 convenience translation, same semantics independently confirmed, German original prevails.

The semantic scope remains exactly `V1.0 / documentation_only`.

## Consequence
No runtime/XML rule is introduced. Device roles must not be hard-coded as permanent Master/Slave roles merely from architecture context.
