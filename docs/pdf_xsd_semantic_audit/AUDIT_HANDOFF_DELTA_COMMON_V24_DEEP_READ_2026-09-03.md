# Audit handoff delta — COMMON V2.4 Deep Read — 2026-09-03

## Completed block

`COMMON_V2.4` is closed as the final planned Deep Read Pass 2 unit.

- source-only freeze commit: `789f02f697809b1eef4d3b1a366a3599649a6d7d`
- official PDF SHA-256: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1,689,647 bytes, 63 pages
- render/read run `33658306978`, job `100342316111`, artifact `9857652638`; all 63 render hashes rechecked
- selected XSD authority is candidate/integration, not official: Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` + Enumerations blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, matching open draft `VDVde/VDV301#31`
- EV-122 PASS: run `33716645876`, job `100527119224`
- new unique finding `DRCOM24-001`: LineName/LineShortName PDF `IBIS-IP.string 0:1` vs candidate XSD `InternationalTextType 0:*`

## Scope corrections

Do not extend `DRCOM23-001`, `CE-025`, `CE-026` or DoorCounting portion of `DRCOM10-006` into V2.4; the fresh source and EV-122 show those boundaries corrected. `CE-020` remains V2.3 authority-collision specific; `CE-023` remains V2.2-only.

The stale V2.4 first-pass InternationalText statement in `01g...` is explicitly superseded by a correction delta; no history is silently deleted.

## Guardrails

- No XSD changed.
- Candidate/integration is not relabelled official.
- `latest wins` remains forbidden.
- `-1:1` remains XML choice notation.

## Next phase

Deep Read Pass 2 is frozen complete. Proceed with `LEGACY_FINDING_REVALIDATION_PLAN.md`: freeze the full finding inventory and revalidate every finding not already explicitly revalidated under the current Evidence Gate, requiring zero pending SDK-relevant findings before baseline freeze.
