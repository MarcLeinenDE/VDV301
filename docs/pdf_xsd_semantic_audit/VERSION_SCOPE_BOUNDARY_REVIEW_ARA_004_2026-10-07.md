# Version-scope boundary review — ARA-004 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`ARA-004` is the documentation-only wrong-operation-reference finding in AnalogRadioService V2.4.

Visible evidence remains:
- printed page 10: AnalogRadioService has one operation, `SendTelegram`;
- printed page 13 heading: `URI for the Operation SendTelegram`;
- the concrete URI alone uses `/AnalogRadioService/SendFFSKTelegram`;
- the immediately following XML example again uses `<AnalogRadioService.SendTelegram>`.

No alias is inferred.

## Publication boundary
The current VDV publication index was rechecked on 2026-10-07. AnalogRadioService is listed only as V2.4 / VDV 301-2-19. The project PDF source registry likewise contains only `ARA_V2.4`.

## Boundary conclusion
- predecessor publication: none available;
- first affected publication: V2.4;
- last affected publication: V2.4;
- successor/correction publication: none available;
- bilingual split: none; the shared bilingual technical example contains the same operation-name inconsistency.

The semantic scope remains exactly `V2.4 / documentation_only`.

## Consequence
`SendFFSKTelegram` remains a documentation typo/runtime-guidance finding only. It must not be accepted, rewritten or registered as an alias for `SendTelegram`.
