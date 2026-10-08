# Version-scope boundary review — CE-025 — 2026-10-08

Status: **verified / scope unchanged**.

CE-025 is the historical `Reply-Path` versus XSD `ReplyPath` identifier mismatch in the Common SubscribeRequest and UnsubscribeRequest tables.

The mismatch is already present in Common V1.0, the earliest retained Common publication, and persists through official V2.3. XML names are exact, so `Reply-Path` is not an alias for `ReplyPath`.

Common V2.4 is an explicit correction boundary: the V2.4 documentation uses `ReplyPath`, matching the selected V2.4 XSD. V2.4 must therefore remain outside the affected scope and the later correction must not be back-applied to historical validation.

Boundary:
- Common V1.0-V2.3: affected;
- Common V2.4: not affected / corrected documentation.

SDK consequence: historical payloads using `Reply-Path` must fail whenever the selected XSD requires `ReplyPath`; CE-025 may explain the historical PDF spelling only.
