# HTMLDisplayService V2.2a — Deep Read Pass 2

Status: independent V2.2a source read and targeted visible review complete; historical V2.2a reconciliation pending.

## Source and authority

- Official publication: VDV-Schrift 301-2-17, HTMLDisplayService V2.2a, 02/2021.
- Official URL: https://www.vdv.de/301-2-17-sdes-v2-2a-htmldisplayservice.pdfx
- Pinned SHA-256: `f3da1994e719572ba1689aea2448b9533faf9e8fbe42720b9e737b98edd8b0f8`
- Size: `431875` bytes.
- Pin run: `33266884196`.
- No repository tag `VDV-301-2.2a` exists.
- No dedicated HtmlDisplayService XSD exists in the integration root pool.
- Authority class: official service publication for a **non-XSD DNS-SD/HTTP profile**; no HDS XML contract is invented.

## Visual/read evidence

The interactive PDF screenshot path again returned cache miss. Exact pinned-byte fallback was used.

- Render/read run: `33266920928`
- Job: `99138495593`
- Artifact: `9718919955`
- Artifact digest: `6c0a636017990fe40bc69d3e88f549c06c0d3d90510429f188754b60974db449`
- Extracted full-text SHA-256: `8f21a5a9445e7b27f7cb6e4ce7783fc52e0bf73e40b48c3119867c0cdfac9809`
- Rendered pages: 7-14; visibly reviewed focus pages: 8, 10, 11.

## Independence boundary

The historical HDS block was already known from prior-version reconciliation, but no historical V2.2a statement is used as source authority here. The facts below were re-derived from the pinned V2.2a publication before formal V2.2a reconciliation.

## Independent V2.2a observations

1. The foreword says V2.2a contains a note on future use of `_ibisip_http._tcp` instead of `_http._tcp`.
2. HDS remains a DNS-SD/HTTP/browser profile without its own service protocol or service XSD.
3. The current V2.2a discovery table lists **both** `_http._tcp` and `_ibisip_http._tcp`.
4. German labels `_http._tcp` as `zukünftig nicht mehr empfohlen`; English labels it `deprecated`.
5. TXT remains `content + url`; `url` is the content access URL.
6. The publication states that **the next service version after 2.2** will adapt the SRV record, use `_ibisip_http._tcp`, and delete `_http._tcp`.
7. By mutual agreement, project-specific use of `_ibisip_http._tcp` is already permitted in version 2.2.
8. The version-history section is headed `Version 2.2` and records the usage-of-`_ibisip_http._tcp` note/correction.

## Interpretation boundary

V2.2a is treated as an amended/corrected V2.2 publication/profile variant, **not** as the future next service version mentioned in its own text. Therefore the current V2.2a authority recognises both labels. `_http._tcp` is deprecated/future-not-recommended, while `_ibisip_http._tcp` is the documented transition/future label and may be used by project agreement.

It would overstate the source to describe `_ibisip_http._tcp` as an exclusive current V2.2a requirement. The source reserves deletion of `_http._tcp` for the future next service version after 2.2.

## Active falsification

- Rejected the interpretation that V2.2a itself is the future next service version: its current table still contains both labels and its prose points to a future next version.
- Rejected an exclusive-current `_ibisip_http._tcp` rule: mutual-agreement wording and the dual-label table contradict exclusivity.
- German `zukünftig nicht mehr empfohlen` versus English `deprecated` is retained as a bilingual wording nuance, not promoted to a defect because the surrounding transition rule aligns.
- No hidden XML/XSD contract is inferred from generic foreword wording.

## Fresh finding result

No new unique VDV finding is promoted from the independent V2.2a fresh read. The protocol-label transition is version/profile routing knowledge.

## Audit-tool wording refinement pending

RV-002 currently labels `_ibisip_http._tcp` as `preferred` for V2.2a. Its acceptance behavior is compatible with the publication, but `preferred` is stronger than the source wording. After this source freeze, only the diagnostic/test wording will be refined to `transition/future` language; behavior will remain unchanged and RV-002 will be rerun.

## Next gate

Correct the audit-tool wording, rerun RV-002, then reconcile the historical V2.2a profile and close HDS V2.2a.
## Historical V2.2a reconciliation after fresh-read freeze

The independent V2.2a source state was frozen in commit `17f036c6257c5c71b94169c02905c2e80f36b847` before formal V2.2a historical reconciliation.

The historical HDS profile record is directionally consistent with the independently derived transition. The current-source wording is retained more precisely here: V2.2a itself still recognises both protocol labels; `_http._tcp` is deprecated/future-not-recommended, `_ibisip_http._tcp` is the documented transition/future label, and only the future next service version after 2.2 is stated to delete `_http._tcp`.

### HDS-001 — V2.2a revalidation

State: `context_verified_ok_with_note_runtime_profile_supported_RV-002_run_33267198470`.

Evidence chain:

- official byte-pinned V2.2a publication;
- pinned-byte visible review of the discovery table and version history;
- absence of a dedicated `VDV-301-2.2a` release tag and absence of a dedicated HDS service XSD;
- active falsification of the mistaken interpretations `V2.2a = future next service version` and `_ibisip_http._tcp = exclusive current requirement`;
- RV-002 wording correction commit `6f0875e80c55f6c1ac6e209c484187a41dbf3d54`;
- corrected deterministic RV-002 rerun `33267198470` PASS.

The RV-002 correction changed only diagnostic/test wording, not acceptance or endpoint behavior. `_ibisip_http._tcp` is accepted as the transition/future label; `_http._tcp` remains accepted with a deprecation/future-not-recommended note; endpoint resolution continues to use TXT `url`.

No live DNS/mDNS, endpoint reachability, or browser/content interoperability is claimed. No new V2.2a finding ID is opened.

With this closure, HDS V2.1, V2.2 and V2.2a are all revalidated under the current Evidence Gate.
