# Version-scope boundary review — CE-002 — 2026-10-07

Status: **verified / scope unchanged / V2.4-only**.

## Finding
`CE-002` is the V2.4 documentation defect where the version history says `StopPointNumber` was inserted into StopInformation, while the actual StopInformation table and selected V2.4 candidate/integration XSD use `PointNumber`.

## Predecessor boundary
Official V2.2 and V2.3 publications were rechecked.

### Common V2.2
The StopInformation table contains StopIndex, StopRef, StopName, StopAlternativeName, Platform, DisplayContent, StopAnnouncement, ArrivalScheduled, DepartureScheduled, RecordedArrivalTime, DistanceToNextStop, Connection and FareZone. There is no PointNumber or StopPointNumber. The V2.2 history does not introduce either name.

### Common V2.3
The StopInformation table adds ArrivalExpected and DepartureExpected but still contains no PointNumber/StopPointNumber. The V2.3 history explicitly records ArrivalExpected and DepartureExpected additions and does not mention PointNumber/StopPointNumber.

Therefore V2.2 and V2.3 are proven non-affected predecessors.

## V2.4 boundary
Existing byte-pinned visible-body evidence remains authoritative:
- actual StopInformation table: `PointNumber`;
- V2.4 history: `StopPointNumber`;
- selected candidate/integration XSD: `PointNumber`.

The current VDV publication index still lists Common Data Structures and Enumerations V2.4 as the latest publication.

## Renderer note
The interactive PDF screenshot path for V2.2/V2.3 returned cache-miss. The required deterministic local fallback was attempted, but the runtime environment could not resolve the VDV host for a fresh byte download. The predecessor conclusion therefore uses the official PDF text extraction together with the already frozen deep-read evidence; no new unpinned visual source was substituted.

## Boundary conclusion
- V2.2: unaffected predecessor;
- V2.3: unaffected last predecessor;
- V2.4: first and current last affected publication;
- successor: none published.

Existing semantic scope remains `Common V2.4 / candidate_integration` for selected XSD authority, with official PDF documentation defect.

## Consequence
Use `PointNumber`. Never infer `StopPointNumber` as an alias or accepted XML spelling from the version-history typo.
