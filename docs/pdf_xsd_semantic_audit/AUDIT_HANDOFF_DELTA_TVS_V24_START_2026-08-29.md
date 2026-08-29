# Audit handoff delta - TVS V2.4 start - 2026-08-29

TVS V2.4 has been started document-first. Historical V2.4 findings remain closed.

## Official PDF source

```text
URL: https://www.vdv.de/301-2-16-sde-v2.4-ticketvalidationservice.pdfx
sha256: e7caca3de444b3eca15d539572cd4b896e56e5bb608b4827211b51be0ad56c51
size: 864860
pin run: 33264912909
pinned: 2026-08-29T17:10:21Z
```

## V2.4 XSD authority boundary

No upstream `VDV-301-2.4` tag exists. Tags currently stop at `VDV-301-2.3`.

Upstream master head is `14880bb33beec5c5dffe96315b730bd6c094a585`, merge of PR #26 on 2023-01-04. It contains `IBIS-IP_TicketValidationService_V2.4.xsd` blob `291f41518fd48cd9dcc9f285cf9b5fec7dd72159`, which includes Common V2.4 and Enumerations V2.2. Current upstream master does not contain the referenced Common V2.4 file, so that master family is dependency-incomplete and cannot be treated like a release-tagged exact family.

For Deep Read technical comparison, `dev/schema-integration` contains a complete candidate/integration family:

```text
TVS V2.4     34b18b8c874e325dd923b366a72bb0ebee32e59e
Common V2.4  1946fd37e29ced605654f49ea3d98cd2fbbdc8e4
Enums V2.4   2afed8cf23afa91db92b0f043cc5b4ad428b0f25
```

The service include was changed from Enums V2.2 to Enums V2.4 in integration commit `c9c086ac07f7e9bdb271c54f7a274e3cf0d03749` (`Integrate public schema candidate files`). This family is candidate/integration authority only.

## Next

1. Fresh-read the exact pinned V2.4 PDF without opening historical TVS findings.
2. Render material pages from pinned bytes and inspect visibly.
3. Freeze independent observations.
4. Only then open/reconcile V2.4 history, especially TVS-001.
5. Add executable candidate/integration evidence if needed, with explicit authority guard.

No XSD change or upstream action is authorized.
