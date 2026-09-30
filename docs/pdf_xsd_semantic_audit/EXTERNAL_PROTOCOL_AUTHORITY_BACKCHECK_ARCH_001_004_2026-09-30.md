# External-protocol authority backcheck — ARCH-001..ARCH-004 — 2026-09-30

Status: completed under `EXTERNAL_PROTOCOL_STANDARD_AUTHORITY.md`.

## Result

No existing terminal classification, runtime-match state or PASS/FAIL authority for ARCH-001 through ARCH-004 changes.

| Finding | Protocol relevance | Authority-chain result | Decision |
|---|---|---|---|
| ARCH-001 | Service-oriented architecture provides the architectural premise for later service/protocol resolution. | Part 1 does not select an executable external protocol clause for this finding. Concrete service/protocol authority remains Part 2/profile specific. | Keep `no_runtime_effect` / `not_applicable`. |
| ARCH-002 | Consumer/client and provider/server roles are relevant context for discovery, endpoint resolution and later DNS-SD behavior. | The architecture hierarchy does not itself select a DNS-SD RFC clause or override service-specific request/subscription/callback rules. External DNS/DNS-SD requirements become executable only through the applicable VDV discovery/profile authority chain. | Keep `no_runtime_effect` / `not_applicable`; do not synthesize a provider/consumer protocol hard rule. |
| ARCH-003 | Vehicle/system boundaries can affect network topology, discovery scope and cross-vehicle routing. | The vehicle-boundary statement does not select an external routing/discovery protocol requirement and does not prohibit cross-vehicle communication. Any executable network/protocol check needs a separate applicable VDV profile plus external authority where relevant. | Keep `no_runtime_effect` / `not_applicable`. |
| ARCH-004 | General protection/security language can intersect TLS, certificates and other security standards. | Part 1 supplies no concrete TLS version, certificate profile, cipher suite or external security-standard clause for this finding. A concrete security hard-fail therefore requires another explicit VDV/profile authority and the complete external-standard authority chain. | Keep `no_runtime_effect` / `not_applicable`; no invented cryptographic profile. |

## Governance consequence

Architecture context may establish why a later protocol check exists, but it is not by itself sufficient to complete the external-protocol hard-fail chain.

For ARCH-001..004 the chain stops before an exact externally normative clause is selected. Their existing contextual classifications therefore remain correct.

Future service/profile checks must still preserve the chain:

`selected VDV profile -> VDV protocol selection/specialization -> exact external standard/version -> exact normative clause -> applicability -> VDV override check -> result`.
