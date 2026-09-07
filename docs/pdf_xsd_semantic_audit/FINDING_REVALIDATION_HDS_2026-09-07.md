# Finding Revalidation — HDS / HTMLDisplayService V2.1, V2.2, V2.2a

Date: 2026-09-07  
Scope: `HDS-001`  
Evidence: `EV-151`, successful run `34091867070`, job `101646862752`  
Evidence commit: `9f84047937e66236c1741dfe8a35ac124f1ca758`  
Closure run: `34092485260`

## Authority route

`HDS-001` is a non-XSD service-modelling finding. The exact byte-pinned official publications for HTMLDisplayService V2.1, V2.2 and V2.2a were re-fetched and hash/size checked. The exact official upstream `VDV-301-2.1` and `VDV-301-2.2` release inventories were also checked and contain no dedicated HTMLDisplayService service XSD. V2.2a has no dedicated upstream release tag and the 50-root integration pool likewise contains no HDS service XSD.

The absence of such a schema is therefore intentional, not a missing-schema defect. HDS routes to a version-specific DNS-SD/HTTP profile validator.

## HDS-001 — context_verified

The three canonical Deep Reads independently establish the same authority boundary and retain the version differences instead of applying latest-wins:

- V2.1: `_http._tcp`, TXT `content + path`, endpoint from SRV target/port plus TXT path.
- V2.2: canonical `_http._tcp`, TXT `content + url`, endpoint from TXT `url`; SRV host/port are not reconstructed into the content URL.
- V2.2a: `_ibisip_http._tcp` is the documented transition/future label while `_http._tcp` remains accepted with a deprecated/future-not-recommended note; endpoint remains TXT `url`.

RV-002 was rerun successfully and confirms these deterministic discovery/endpoint rules. It performs no live DNS/mDNS or HTTP reachability and no such claim is made.

## Disproof and regression guards

The strongest contrary hypothesis — that a hidden or omitted HDS XML contract exists — was actively checked against the exact V2.1/V2.2 upstream release inventories, the current integration XSD pool and the authoritative HDS publications. It was rejected. The complete 50-root-XSD regression pool also passed unchanged.

The first EV-151 attempt (`34091700946`) failed only because the fork checkout did not locally contain the upstream release-tag refs. The repair fetched and pinned the exact official upstream tag commits before the inventory check; no HDS behavior, finding classification, XSD or frozen inventory was changed.

## Closure

EV-151 PASS; RV-002 rerun PASS; all 50 root XSDs PASS; all three official HDS PDF pins PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **127/192 terminal, 65 pending**. The first remaining pending finding is `JIS-001`; next block is `JIS`.
