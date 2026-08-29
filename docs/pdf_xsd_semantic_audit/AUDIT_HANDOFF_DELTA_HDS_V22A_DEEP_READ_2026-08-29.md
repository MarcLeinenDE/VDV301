# Audit handoff delta — HTMLDisplayService V2.2a Deep Read

Date: 2026-08-29

## Permanent result

- HDS V2.2a source independently pinned/read before formal V2.2a reconciliation.
- PDF pin: `f3da1994e719572ba1689aea2448b9533faf9e8fbe42720b9e737b98edd8b0f8`, 431875 bytes, run `33266884196`.
- Render/read: run `33266920928`; fresh-read freeze `17f036c6257c5c71b94169c02905c2e80f36b847`.
- No `VDV-301-2.2a` release tag and no dedicated HDS service XSD; service remains non-XSD discovery/HTTP profile.
- V2.2a is an amended/corrected V2.2 profile publication, not the future next service version. Current publication recognises both `_http._tcp` and `_ibisip_http._tcp`; only the future next version after 2.2 is stated to delete `_http._tcp`.
- RV-002 wording `preferred` was refined to source-exact transition/future wording in commit `6f0875e80c55f6c1ac6e209c484187a41dbf3d54`; behavior unchanged.
- Corrected RV-002 run `33267198470` PASS.
- HDS-001 revalidated V2.2a as OK with note; no new finding IDs.
- HDS V2.1, V2.2 and V2.2a are now all revalidated under the current Evidence Gate.
- No XSD changed.

## Next

Start `SMS_V2.2`: own PDF pin, exact official XSD family, document-first fresh read, then historical reconciliation.
