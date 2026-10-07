# Version-scope boundary review — BG-002 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`BG-002` records a historical packaging rule, not a defect. The aggregate schema `IBIS_IP_V1.0.xsd` belongs to the original VDV-301-1.0 package. Later release pools must not be "repaired" by mixing in that aggregate or by inventing a synthetic replacement.

## Official release-boundary recheck
The exact upstream path was rechecked across the complete current official release line.

- `VDV-301-1.0`: present, blob `41289eaed2674a169fdf77a10a2eff293c76d5c4`, size 23857.
- `VDV-301-2.0`: absent.
- `VDV-301-2.1`: absent.
- `VDV-301-2.2`: absent.
- `VDV-301-2.3`: absent.
- current `master`: absent; master is integration state, not official release authority.

`VDV-301-2.3` remains the latest official release.

## Boundary conclusion
- first/only release context containing the historical aggregate: **VDV-301-1.0**;
- first release context without it: **VDV-301-2.0**;
- absence persists through the latest official release **VDV-301-2.3**;
- no later official release exists.

The existing semantic scope remains correct:
1. VDV-301-1.0 aggregate exists.
2. VDV-301-2.0 and later official release pools do not contain it.

## Consequence
The old aggregate must be used only with its VDV-301-1.0 schema pool. Later profiles must use only the schemas/dependencies actually published in their selected release context. No synthetic aggregate or cross-release dependency mixing is allowed.
