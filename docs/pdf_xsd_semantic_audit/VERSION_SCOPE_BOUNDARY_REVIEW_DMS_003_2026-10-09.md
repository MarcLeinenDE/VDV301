# DMS-003 — full independently verified version-scope correction (2026-10-09)

**Classification remains `non_defect`; XML validation follows exact selected XSD.** The original scope V2.0–V2.2 and V2.4 was incomplete. V1.0 official German/English and V2.3 integration-only are now explicitly accounted for.

## Complete release/provenance boundary

| Context | Normative or comparison authority | GetDeviceErrorMessagesResponseData.ErrorMessage |
| --- | --- | --- |
| V1.0 German official PDF | `VDV301-2_V1.0_DE`, SHA-256 2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75, printed p60 §7.1.11.2 **Tabelle 15** | **10:\*** visible; V1.0 official XSD also 10:* |
| V1.0 English official PDF | `VDV301-2_V1.0_EN`, SHA-256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7, printed p67 §9.3.12.2 **Table 39** | **10:\*** visible; independent English track |
| V2.0 official | `VDV301-2_BASE_V2.0`, SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, p95 | **10:\*** PDF and official XSD |
| V2.1 official | `VDV301-2_BASE_V2.1`, SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, p100 | **10:\*** PDF and official XSD |
| V2.2 official | `DMS_V2.2`, SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`, p20 Table 9 | **10:\*** PDF and official XSD |
| V2.3 integration comparison only | Local `IBIS-IP_DeviceManagementService_V2.3.xsd` blob `5fe444cf6d10462cc23fd159eb963abbec42248f` | **0:\*** in integration XSD; **no official V2.3 DMS publication or authoritative released XSD inferred** |
| V2.4 public documentation + candidate schema | Official PDF `DMS_V2.4` SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`, p19 Table 9; local candidate XSD blob `d222dfd98b2be3777576388da7ace8f333d24c3f` | **0:\*** PDF + candidate XSD. Candidate XSD never labelled official. |

There is no earlier official predecessor to V1.0. No public DMS V2.3 official PDF is in the pinned catalog; the first *officially documented* 0:* successor in this chain is V2.4, whereas the earlier non-official V2.3 XSD already implements 0:*.

## Visible-body and exact-byte evidence

- V1.0 **Deutsch** original source p60 Table 15 GitHub strict pinned render run **37895016411** SUCCESS, artifact **11600031528**, PNG sha256 `69963b20434a148844c08501a7ad2aa33c3e08411dc640e3656e412dea1bee8e`. The actual rendered table visually reads `ErrorMessage 10:*`.
- V1.0 **English** first official URL source proposal run **37895410420** SUCCESS, artifact **11599922558**; official URL `https://www.vdv.de/301-2ses.pdfx`, first checksum e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7, size **2,403,598**, PDF page count **135**. This source identity was independently promoted to the pin registry before the next strict render.
- V1.0 English **strict pinned renderer rerun 37895617836** SUCCESS, artifact **11599902971**, SHA-256 source match e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7, printed p67 Table 39 PNG sha256 `e045607d1823b04f8ba873e586fcece5aa2494db100174c100fc202df3e7de3b`. The actual original visible table says `ErrorMessage 10:*`.
- The V1.0 official XSD at upstream `VDVde/VDV301` tag `VDV-301-1.0` has Git blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4`, `DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure` line 58 `minOccurs="10" maxOccurs="unbounded"`.
- Historical V2.0–V2.2 and V2.4 PDF pages were already visible-body verified and pinned in `SOURCE_LOCATOR_REVIEW_DMS_003_2026-10-06.md` and `dms_visual_revalidation_evidence_2026-09-03.json`.

## Executable proof, disproof and SDK

Extended `tools/validate_dms_instance_boundaries_ev127.py`; GitHub Actions **37895839654** SUCCESS, independent executable `lxml.XMLSchema` validation:

- V1.0, V2.0, V2.1, V2.2 official profiles: **9 rejects; 10 and 11 accept**.
- V2.3 integration comparison and V2.4 candidate: **0 and 1 accept**.

Active disproof: V1.0 demonstrates the ten-error minimum did **not** first appear in V2.0. V2.3 integration demonstrates the relaxed shape predated the V2.4 comparison XSD **but does not establish an official V2.3 correction**. The older minimum aligns with the corresponding official XSD and published table, so it is not a historical XML defect. Do not infer that ten errors must actually exist on a device: the XML response payload shape is distinct from device operational behaviour.

**Conformance:** `non_defect`, `normative_authority=selected_xsd`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`. No aliases, XSD mutation, unofficial promotion, provider FAIL, or runtime matcher. Use version-exact validator.

## Material-scope correction and package stop

Semantic registry, source locator scope, bilingual diagnostics, runtime semantic blob pointer, body-verification provenance, boundary registry, SDK manifestation, state and evidence synchronized. `DMS-003` changes boundary progress from **51/70 to 52/70**, leaving **18** pending with `DMS-004` as the next canonical finding. The current package **stops after this finding** because the original scope was materially incomplete. Completion requires full validation SUCCESS and final handoff-integrity SUCCESS on the eventual terminal-clean HEAD.
