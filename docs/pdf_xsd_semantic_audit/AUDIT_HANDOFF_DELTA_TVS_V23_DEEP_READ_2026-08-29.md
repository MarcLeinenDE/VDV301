# Audit handoff delta - TVS V2.3 Deep Read - 2026-08-29

## Completed block

`TVS_V2.3` is complete at Deep Read state `needs_visual_review`.

## Source pin

```text
PDF: https://www.vdv.de/301-2-16-sdes-v2-3-ticketvalidation.pdfx
sha256: 74d9fd279e13f2661be24319c414ef9128b61c8fc6f30ea62b63f92f94ddbff4
size: 404383
pin run: 33258484479
```

## Exact authority

Official tag `VDV-301-2.3` contains no V2.3-named TVS service XSD. Official routing is:

```text
IBIS-IP_TicketValidationService_V2.2.xsd  5a4be2b2ba66860f035777ec0458dba0790880e1
IBIS-IP_common_V2.2.xsd                   468fee6d177e7185dbcd5d3f90cfb114e29e01ae
IBIS-IP_Enumerations_V2.2.xsd             2a23b512379b18e8f122ac1272cef8229fb86283
```

Branch candidate/integration only:

```text
IBIS-IP_TicketValidationService_V2.3.xsd  b17591c5b067254dd3e2260f3ef2acd2e18394a9
```

Never latest-wins select the branch candidate as official V2.3 authority.

## Visual evidence

```text
render run: 33258612417
job: 99116563806
artifact: 9716575205
pages rendered: 10-19
pages visibly reviewed: 10-16, 18-19
```

## Evidence

EV-114 run `33264437557`, job `99131891930`: PASS.

It confirms the official-route/candidate identity boundary, critical declaration equality despite provenance distinction, RouteDeviation behavior, and CurrentTariffStop executable boundary.

## Finding reconciliation

```text
TVS-002      V2.3 executable-confirmed EV-114
TVS-003      V2.3 executable-confirmed/refined EV-114; explicit correction claim remains contradicted by stale labels
DRTVS21-001 V2.3 scope extension; exact official route identity + EV-114/EV-113 support
DRTVS21-002 V2.3 scope extension; context verified
DRTVS21-003 V2.3 scope extension; context verified
DRTVS21-004 not scope-extended
new V2.3-only IDs: none
TVS-001      untouched; V2.4 scope
```

## Next block

Start `TVS_V2.4` document-first:

1. pin its own official PDF bytes;
2. independently establish exact V2.4 XSD/dependency authority;
3. fresh-read without consulting historical V2.4 findings;
4. use pinned-byte visible review for material pages;
5. only after fresh-read freeze, reopen TVS V2.4 history including TVS-001;
6. executable-strengthen surviving XML-material findings as needed;
7. close V2.4 with audit-only diff and no XSD/workflow residue.

Global rules remain unchanged: no master changes, no upstream/PR action without explicit approval, no schema modification solely to match PDF, and no unrevalidated finding may drive SDK behavior.
