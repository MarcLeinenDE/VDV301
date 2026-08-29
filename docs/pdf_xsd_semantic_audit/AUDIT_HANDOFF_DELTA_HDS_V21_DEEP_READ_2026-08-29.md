# Audit handoff delta — HTMLDisplayService V2.1 Deep Read

Date: 2026-08-29

## Permanent result

- HDS V2.1 independent fresh read completed before historical findings were opened.
- Official PDF pin: `c8aa91626bf60c8e74200200d63d44d497aeb3ab240c47039333b2c922a0e495`, 734901 bytes, run `33265498869`.
- Visible fallback render: run `33265541783`, pages 7-10.
- Authority: intentionally non-XSD `discovery_http_profile`; no dedicated HDS service XSD in official VDV-301-2.1 tag or integration branch.
- Historical HDS-001 independently reproduced and revalidated for V2.1 as OK with note.
- RV-002 rerun `33266402138` PASS supports V2.1 `_http._tcp`, `content + path`, SRV/port/path endpoint construction, and non-retroactive version handling.
- No new HDS V2.1 finding IDs.
- No XSD changed.
- No live DNS/mDNS or reachability claim.

## Next

`HDS_V2.2` must receive its own byte pin, document-first fresh read and visible review before the historical V2.2 profile delta is reopened. Do not back-apply V2.2 `url` semantics to V2.1.
