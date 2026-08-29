# Audit handoff delta - TicketValidationService V2.3 start

Date: 2026-08-29
Canonical branch: `dev/schema-integration`

## Start state

`TVS_V2.2` is closed under the current Evidence Gate with EV-113. The next Deep Read target is `TVS_V2.3`.

## V2.3 PDF source pin

Official source:

```text
https://www.vdv.de/301-2-16-sdes-v2-3-ticketvalidation.pdfx
```

Exact pin:

```text
source_id: TVS_V2.3
sha256: 74d9fd279e13f2661be24319c414ef9128b61c8fc6f30ea62b63f92f94ddbff4
size: 404383 bytes
pin run: 33258484479
pin job: 99116224918
pinned_at_utc: 2026-08-29T14:46:39Z
```

## Independently established official XSD authority

The historical routing note was treated as an unconfirmed hypothesis and checked directly against the official `VDV-301-2.3` tag before reopening V2.3 historical findings.

Direct tag result:

```text
IBIS-IP_TicketValidationService_V2.3.xsd -> absent from official VDV-301-2.3 tag

IBIS-IP_TicketValidationService_V2.2.xsd
  blob 5a4be2b2ba66860f035777ec0458dba0790880e1
  includes IBIS-IP_common_V2.2.xsd
  includes IBIS-IP_Enumerations_V2.2.xsd

IBIS-IP_common_V2.2.xsd
  blob 468fee6d177e7185dbcd5d3f90cfb114e29e01ae

IBIS-IP_Enumerations_V2.2.xsd
  blob 2a23b512379b18e8f122ac1272cef8229fb86283
```

Therefore the exact official tag route is independently established as:

```text
TVS document V2.3
-> official service XSD file V2.2
-> Common V2.2
-> Enumerations V2.2
```

This is official historical routing, not a latest-version substitution.

## Candidate/integration separation

The integration branch also contains:

```text
IBIS-IP_TicketValidationService_V2.3.xsd
blob b17591c5b067254dd3e2260f3ef2acd2e18394a9
```

Independent provenance check confirms it was added by:

```text
commit c9c086ac07f7e9bdb271c54f7a274e3cf0d03749
message: Integrate public schema candidate files
```

It is candidate/integration material and must not be treated as the historical official V2.3 release XSD.

## Evidence-Gate ordering

Before reopening any historical V2.3 TicketValidation finding or using V2.2 correction history as current evidence:

```text
1. Fresh-read the byte-pinned V2.3 PDF independently.
2. Use the official V2.3-tag route to the V2.2 service family as exact executable authority.
3. Keep the branch V2.3 candidate explicitly separated.
4. Render exact pinned bytes for material layout/table evidence if interactive screenshots fail.
5. Freeze fresh observations before historical reconciliation.
6. Only then reopen TVS-002 / TVS-003 or other historical V2.3 statements.
7. Add executable evidence only where current V2.3 claims require it.
```

No XSD was modified. No PR, comment, merge or official-facing remediation action was performed.
