# HTMLDisplayService V2.2 — Deep Read Pass 2

Status: independent V2.2 source read and targeted visible review complete; V2.2 historical reconciliation pending.

## Source and authority

- Official publication: VDV-Schrift 301-2-17, HTMLDisplayService V2.2, 08/2019.
- Official URL: https://www.vdv.de/301-2-17-sdes-v2-2-htmldisplayservice.pdfx
- Pinned SHA-256: `bf62b7a8b6cfdf654181b48da2d85a805118687c7463a46fadfd32679c9b7577`
- Size: `802399` bytes.
- Pin run: `33266549282`.
- Official release tag checked: `VDV-301-2.2` / commit `f283697124750d12189b960b302b399769bad530`.
- No dedicated HtmlDisplayService XSD exists in that exact official tag or in the integration root pool.
- Service authority: **non-XSD DNS-SD/HTTP profile**.

## Visual evidence

The interactive PDF screenshot path returned cache miss. Exact pinned-byte fallback was therefore used.

- Render/read run: `33266588436`
- Job: `99137608617`
- Artifact: `9718826204`
- Artifact digest: `54ae8617da6f26f31a855925f54af0059d7dec1001c0932ed75f4bee4d6e1267`
- Extracted full-text SHA-256: `c0db2e41ddaf56ac90b8f2e51957ed2190923e859ad5754ea4db989d79ea745d`
- Visibly reviewed pages: 7, 8, 9, 10, 11.

## Independence boundary

The broader historical HDS audit had already been viewed during the preceding V2.1 reconciliation. For this V2.2 pass, those historical V2.2 statements were not used as factual authority. The V2.2 facts below were independently re-derived from the pinned V2.2 source before performing V2.2 reconciliation.

## Independent V2.2 observations

1. HDS remains a DNS-SD/HTTP/browser profile and the text again states that it defines no own protocol.
2. DNS-SD service name: `HtmlDisplayService`; protocol label: `_http._tcp`.
3. TXT entries are `content` and `url`.
4. `url` contains the access URL and may include query and fragment components.
5. `content` is project-specific and not standardized.
6. Multiple content URLs are published as separate DNS-SD entries.
7. SRV `Port` remains published but is explicitly said to have no meaning for the content address. `Host` identifies the publishing device.
8. The HTTP content itself is intentionally not standardized by this service publication.
9. The V2.2 version history explicitly records `url` as a new TXT entry replacing `host`, `port` and `path` for access-address construction.

## Active falsification

A superficial reading of the version history could suggest that SRV host/port are removed in V2.2. This is disproved by the main V2.2 discovery table, which still publishes both; the prose limits their role and makes TXT `url` the content address.

The foreword says the publication describes HDS and its specific data structures. This wording is not promoted into an XML/XSD claim: the exact release inventory has no dedicated HDS schema and the concrete service definition is DNS-SD/HTTP.

## Fresh finding result

No new unique V2.2 finding is promoted from the independent fresh read. The V2.2 profile change is normative version-specific behavior, not by itself a defect.

## Next gate

Reconcile the already-existing HDS historical register against this frozen V2.2 source. Do not back-apply V2.1 `content + path` endpoint reconstruction to V2.2.
