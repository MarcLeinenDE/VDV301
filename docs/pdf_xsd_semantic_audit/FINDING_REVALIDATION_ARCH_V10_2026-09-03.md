# Legacy finding revalidation — ARCH V1.0 — 2026-09-03

Status: completed under the current Finding Evidence Gate.

## Original-source evidence

- Authority: official German `VDV-Schrift 301-1`, 01/2014, Part 1 Systemarchitektur. This is an architecture authority lane, not an XSD lane.
- Official source ID: `VDV301-1_V1.0_DE`.
- Fresh PDF SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`; size `1052021` bytes.
- Pin/render run `33725750019`, job `100554215021`, artifact `9881897572`, artifact digest `sha256:b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510`.
- 36 pages rendered at 120 dpi; all 36 page hashes verified locally against the artifact hash list.
- Fulltext SHA-256: `bcf21432e5cec543317d029b882eef1a62706d2a5fb35a9e0b0bf3ec07afd964`.
- Relevant visual pages: 6, 7, 10, 14, 16, 26, 27.

## Terminal states

| Finding | State | Gate result / active disproof |
|---|---|---|
| ARCH-001 | `contextual_not_defect` | Pages 7/10 visibly establish replacement of Master/Slave by a service-oriented architecture and define service/operation independently of the device. This is architecture context, not a defect. |
| ARCH-002 | `contextual_not_defect` | Page 14 visibly describes higher components as active consumers and lower ones as providers. The wording is a general hierarchy model; it does not override service-specific callback/subscription rules. |
| ARCH-003 | `contextual_not_defect` | Page 16 visibly says every vehicle is a self-contained IBIS-IP system and a coupled vehicle is another IBIS-IP system connected through interfaces. It does not prohibit cross-vehicle communication. |
| ARCH-004 | `contextual_not_defect` | Pages 7 and 26 establish the non-safety architecture boundary and general contemporary protection requirement. No concrete TLS/certificate/cipher profile is specified here. |
| ARCH-005 | `contextual_not_defect` | Page 26 visibly distinguishes fast-changing data using UDP multicast from reliable longer-lived information using TCP/HTTP. These are architecture communication classes refined by Part 2, not a global per-packet SDK rule. |
| ARCH-006 | `contextual_not_defect` | Pages 6 and 27 visibly place XML information exchange in Part 1 while Part 2 supplies technical XML structures. Exact elements/cardinalities therefore remain Part-2/XSD authority. |
| ARCH-007 | `contextual_not_defect` | Page 26 explicitly calls SNTP/RTP conceivable but not yet specified **in this edition**. The strongest counter-hypothesis—treating that phrase as a permanent prohibition—is rejected by its publication-context wording. |
| ARCH-008 | `contextual_not_defect` | Page 10 visibly states that only part of the functional components are specified/implemented as services or applications. A component name therefore cannot be promoted to an executable service identity. |

## Executable-evidence boundary

Executable XSD evidence is not applicable to these eight records because they are architecture/authority constraints, not XML validity claims. Any downstream service-specific XML rule must still be proven against its exact selected Part-2 XSD family.

Frozen inventory remains unchanged at 192 IDs. Live revalidation total after this block: **14 terminal / 178 pending**. Next block: `BG`. No XSD was changed.
