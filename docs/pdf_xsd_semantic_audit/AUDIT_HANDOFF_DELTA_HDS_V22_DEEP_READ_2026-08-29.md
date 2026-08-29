# Audit handoff delta — HTMLDisplayService V2.2 Deep Read

Date: 2026-08-29

## Permanent result

- HDS V2.2 source independently pinned/read before formal V2.2 reconciliation.
- PDF pin: `bf62b7a8b6cfdf654181b48da2d85a805118687c7463a46fadfd32679c9b7577`, 802399 bytes, run `33266549282`.
- Render/read: run `33266588436`, pages 7-11 visibly reviewed.
- Authority: non-XSD discovery/HTTP profile; no dedicated HDS XSD in official `VDV-301-2.2` tag.
- Canonical V2.2: `_http._tcp`, TXT `content + url`, endpoint from TXT `url`; SRV port not used for content address, host identifies publisher.
- HDS-001 revalidated V2.2 as OK with note.
- RV-002 post-freeze run `33266770833` PASS.
- No new V2.2 finding IDs and no XSD changes.
- `_ibisip_http._tcp` is not back-written into native V2.2 authority; only later V2.2a compatibility context may permit it with note.

## Next

`HDS_V2.2a`: own byte pin, document-first read and visible review, then reconcile the protocol-label transition.
