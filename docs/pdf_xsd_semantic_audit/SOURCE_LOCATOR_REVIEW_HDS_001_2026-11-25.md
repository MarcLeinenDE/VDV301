# Source locator review — HDS-001

Date: 2026-11-25. Existing finding; intentional_design, no_strict_xsd_profile, no_runtime_diagnostic unchanged. No XSD, semantic classification or runtime matcher modifications.

## Visible body and scope

Intentional non-XSD service in all three independently inspected DE/EN standalone publications. V2.1 first listed; V2.2 changes path to url; V2.2a introduces transition and explicit V2.2 project agreement exception; no later standalone edition established. No missing-schema defect, no SDK runtime finding diagnostic.

- V2.1: DE p7 §1.1 Abbildung 1, p7–8 §1.2, p8 §1.3; EN p9 §1.1 Figure 1, p9–10 §1.2, p10 §1.3. Both tracks list _http._tcp, TXT content+path, endpoint from SRV host/port and path; query/fragment allowed.
- V2.2: DE p7 §1.1 Abbildung 1, p8 §1.2, p8 §1.3; EN p9 §1.1 Figure 1, p10 §1.2, p10 §1.3. Both tracks list _http._tcp and TXT content+url; SRV port has no endpoint meaning; host identifies publisher.
- V2.2a: DE p7 §1.1 Abbildung 1, p8 §1.2, p8 §1.3; EN p9 §1.1 Figure 1, p10 §1.2, p10 §1.3. Both tracks list _http._tcp (future-not-recommended/deprecated) and _ibisip_http._tcp; project agreement allows latter already for V2.2; removal of former reserved for future next service version. TXT content+url unchanged.

The apparent missing XSD is disproved by the web-server/browser architecture, the explicit lack of a dedicated protocol, and separate display DMS requirement. The content identifiers are project-specific, not a standardized enum. Both language tracks independently agree. V2.2a is not the future service version. Existing RV-002 lines 150–235 and checker lines 196–253 cover deterministic routing, including V2.2 transition with note; a bilateral project agreement cannot be verified from advertisement alone. Historical EV-151 rechecked, not a newly executed test. No live network or browser compatibility claim.

## Evidence

- audit_registry/hds_revalidation_evidence_2026-09-07.json; EV-151 run 34091867070 SUCCESS rechecked, historical RV-002 PASS; no fresh runtime rerun yet.
- Exact official upstream commit trees rechecked, nontruncated: VDV-301-2.1 585e0bea34b64887db4276f1c94d5f3e78f06c66 (25 XSD paths), VDV-301-2.2 f283697124750d12189b960b302b399769bad530 (26 XSD paths), neither has HDS-named path. V2.2a no separate tag per EV-151.
- VDV publication index https://www.vdv.de/ip-kom-oev.aspx retrieved 2026-11-25 (cached crawl), lists exactly standalone 301-2-17 V2.1/V2.2/V2.2a; no other dedicated edition established.
- HDS_V2.1 exact source pin c8aa91626bf60c8e74200200d63d44d497aeb3ab240c47039333b2c922a0e495; original archived render run 33265541783, artifact 9718526667, independently verified ZIP SHA256 7c614eb57da7c2f43ae62ee930c4bbbc326dd99effcfe13cded0a85363ec907a, all manifest PNG hashes verified; visibly inspected p7–10, SHA256 respectively 2a27330b04c1c75c9d2a8959d3c5a1973251752bcab758480cddb851cc757263, 6e362a61d66d6a7018327e4aaadc71ed5174ab2d8268adf66764f6423da6adae, fd03a121c9efb2e884a736bd1bc624f9482ece46d004b4b3185a2b683b2af8f2, 250c5aa85bf3a0cd37bfc3e50d470fda6b8a7bd7a274cf417493aa15164a0a08. No raw PDF re-fetch.
- HDS_V2.2 exact source pin bf62b7a8b6cfdf654181b48da2d85a805118687c7463a46fadfd32679c9b7577; original archived render run 33266588436, artifact 9718826204, independently verified ZIP SHA256 54ae8617da6f26f31a855925f54af0059d7dec1001c0932ed75f4bee4d6e1267, all manifest PNG hashes verified; visibly inspected p7–10, SHA256 respectively 1d7064db8f4ebf5d7e37d9dd177bd9af8a37e49f6deaf688debefbef2851e39f, 5f3899e84db643ec680e1048ae9dc630f5d474cf189cf93c4dcd3f276e145956, 42d98d492e9cae5784f05c4d53630d8c45766589e5e6962eaa7c0b17e52e7d06, fd4ddefa0ac65aaa24ad1af763feac6dd44d12a73d20dada8f3968ed9826a251. No raw PDF re-fetch.
- HDS_V2.2a exact source pin f3da1994e719572ba1689aea2448b9533faf9e8fbe42720b9e737b98edd8b0f8; original archived render run 33266920928, artifact 9718919955, independently verified ZIP SHA256 6c0a636017990fe40bc69d3e88f549c06c0d3d90510429f188754b60974db449, all manifest PNG hashes verified; visibly inspected p7–10, SHA256 respectively 9ba058cebc50e613e2947343aa6e15203e4720f3cf1749058cce7aa5ac2b9a78, db5ed1dfd2c1e1d82361d9bd471a8908095031ddf4291cad4e84e73009f85b24, 41e38a9c640d93d8b3b7dc04b3215eb773711e0e28158bb8873975c138608024, 8e8c1ccfc18a96e71ef9383adae80ed8f7dc0f50915b24dbb899eef99bb849f1. No raw PDF re-fetch.

## Closure

127/192 locators, body and scope verified pending full CI. Next JIS-001 only after terminal gate and memory review.

## CI mirror repair (2026-11-25)

Initial schema run 45618895283 failed only the source-locator SDK state mirror and handoff assertions; all other component statuses including discovery RV-002 and scope-boundary validation were zero. Handoff run 45618895176 failed the minimum length of the pending block description. Commit eefdb837 corrected all duplicated SDK state counters and the pending description; handoff run 45619627970 succeeded. No evidence classification or validator changes. State-only push does not trigger schema CI; this SDK summary status update triggers the full gate. Independent local ZIP SHA-256 recheck and all 20 PNG manifest hash/size checks confirmed (4/4, 8/8, 8/8).
