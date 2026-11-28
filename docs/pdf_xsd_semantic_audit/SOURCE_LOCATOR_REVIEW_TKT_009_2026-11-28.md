# TKT-009 source-locator and exact spelling review — 2026-11-28

Status: **gate_pending**, evidence gathering. Do not count as complete. Canonical classification and progress unchanged until full review.

## Visible original evidence

The previous TKT-009 entry described the typo as documentation-only with no runtime effect. The literal PDF child name is in the choice element-name column, not merely a caption. Both tracks independently show the following:

| Source | Body | Location | Literal |
| --- | --- | --- | --- |
| EN V1.0 01/2014 | p93 §9.11.3.2 Response | Table 117 choice a | TicketingSevice.GetTariffInformationResponseData; type TicketingSevice.GetTariffInformationResponseDataStructure |
| EN | p93 §9.11.3.2 | Table 118 | TicketingSevice.GetTariffInformationResponseDataStructure header and caption |
| EN | p94 §9.11.7.2 Response | Table 121 choice a | TicketingSevice.ValidateTicketResponseDataStructure type only; actual element TicketingService.ValidationResponseData correct |
| DE 301-2-9 V1.0 07/2016 | p9 §1.4.2 Response (starts p8) | Tabelle 3 choice a | same wrong child and type |
| DE | p9 §1.4.2 | Tabelle 4 | same wrong structure header and caption |
| DE | p11 §1.8.2 Response | Tabelle 7 choice a | same wrong validation type; actual element correct |
| DE | p14 Tabellenverzeichnis | Tabelle 4 entry | same wrong caption repeated; navigation not body authority |

EN p94 §9.11.6.2 and DE §1.7.2 explicitly refer to the shared tariff response model. EN p131 table index text search indicates same repeated caption, visual fallback requested (not yet verified). Correct service spelling appears in outer headings/captions and prose. Hyphenated line breaks do not supply a missing r; unbroken captions independently corroborate. No evidence that PDF prints a misspelled global root or requires explicit xsi:type. Distinguish exact literal child and optional explicit type errors from invented global root, unrelated errors, and correct naming with other content failures. Historical TKT-006 sequence discrepancy, TKT-004 request heading, TKT-008 CardApplicationInformation and TKT-002 filename alias are distinct.

## Exact source evidence

Live screenshots cache miss; reused EN artifact 15263067509 ZIP SHA256 5dd0b1a423fc0ad9af74af0b3b137faaf8fb9e6aa64fe25fa5b8fb941ce7719d, integrity PASS. Render manifest 284799a8da2839a6e5d2af531fb32f42b2abff97d0fd9656c45faa777023e1f0; source pin e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598, p93 f90858c4e3e79f57728dd0841db672eaa129fb6860c97a7e1999bcc97a9fa078 (244918), p94 aaf798843606b672d0039ec7b997eb9cd1302a760fe519fe751111e6396d47d6 (221771). Actual images visually inspected. EV-158 DE artifact 10336185560 ZIP SHA256 ba5ee246787f58d4cf690421fda683fb1dd072106d5c4e7eb6376c218b717870 integrity PASS; raw PDF SHA256 96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43 (627099); p9 41ec9fbd3e1d9ae0838fd55fe471f4962988feced6bbcb414ae213ab74ee7547 (277797), p11 d3340f41c706c295971bc47b93d824891fa2576cf74f4ca322ff543c2a4b6aa6 (289394), actual images inspected. DE p14 local PyMuPDF 160dpi render from recovered exact raw PDF SHA256 5fc878ae1b6b39cf109125c8a6c9bdcd0faa082c2b3752caffd25f6c3c3eb898 (102836), visually inspected. No new raw PDF acquisition asserted.

Original service 017ca64666e25d757fc0cde1f1be817f06a743fc and aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4 verified at official tag VDV-301-1.0. Later service 3fda66d872ab0d1c511247f13e715cf3ad56afe7 verified independently at tags 2.0, 2.1, 2.2, 2.3; Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enums a9bea5bc73003ed91ded8519db06c32c4067831d identical at all five tags; seven archived files rehashed as Git blobs matching those identities. Earlier isolated service does not provide complete global operation roots; complete original aggregate is independent executable lane. Publication boundary from TKT-001 catalog review (no earlier or corrected later service edition verified), no master-as-release. Fresh independent tag listing checked.

Local lxml compilation of later exact three-file family: both tariff roots complete canonical child and explicit canonical child type accepted; literal typo child rejected SCHEMAV_ELEMENT_CONTENT at exact child path with expected choice containing correct child and OperationErrorMessage; literal typo explicit type rejected SCHEMAV_CVC_ELT_4_2 at canonical child. ValidateTicketResponse canonical implicit and explicit inner type accepted, literal typo explicit type rejected SCHEMAV_CVC_ELT_4_2. This does not yet prove the complete original aggregate executable boundary. Permanent checker extension tests both complete profiles and isolated historical controls; actual GitHub result pending. No new runtime rule or alias implemented. No XSD or resolver changes.

## Next steps

Verify permanent regression, exact EN p131 render, and archive hashes; review existing semantic classification and candidate reviewed mapping policy before deciding exact triggers, test same reasoning pattern in existing findings, synchronize all affected canonical registers, full gate, terminal handoff, reviewed ai-mem PR. Counts remain 154/192; do not begin next finding.

## Final evidence and classification decision (registry gate pending)

- docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_TKT_009_2026-11-28.md
- Original EN pp93–94 and DE pp9,11 inspected from hash-verified pinned archives; exact body rows distinguish actual element/type/caption. EN source e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7; DE source 96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43. Detailed page hashes in report.
- EN p131 fallback run 46169309442 artifact 15273186599 ZIP SHA256 329f1c134d63e770bcb8c71d4e3f1a36a365c3923931e9b8f8e7a5e094ec325f, manifest SHA256 508b54e600112c9f4733912f529576737e1de7c324a7c81de661b4ae4aad52bf, PNG SHA256 14147d102037cf01105a84f4ad59f7592da6215898878d2e11082e306ca03229 (263990 bytes); actual image inspected. DE p14 table list also inspected. Navigation repetitions only.
- Exact upstream tag files verified; original complete aggregate and later identical 2.0–2.3 profile, Common/Enums pinned. No earlier or corrected later publication established.
- Permanent checker c2f16733c641bae84842356b274b06b210eb5511 schema 46169309426 and handoff 46169309429 SUCCESS; artifact 15273051245 ZIP SHA256 eef28865d392d7ab661c2a2f5d229443d45f322f5f773214b3ddb494790cb662 rehashed, 24/24 status exit 0. 18 positive, 4 exact child negative, 6 exact type negative, 22 context and 6 isolated historical controls PASS.
- Same-pattern backcheck of 13 documentation/no-runtime identifier/spelling records; DRTRAINSET21-003 operation label without request payload, DRTVS21-002 shortened display type, DRSMS22-003 historical text distinct. No analogous proven correction among reviewed records; not new full PDF review. Guard: distinguish actual element column, type reference, caption and invented root.

TKT-009 confirmed_pdf_defect, identifier_typo, selected_xsd retained; supersede prior documentation_only/no_runtime_effect with error_with_advisory. Both EN original and DE standalone show the literal wrong tariff response data element and tariff/validation data type references, not just captions. Complete original V1.0 aggregate and exact later official family 2.0–2.3 enforce correct spelling. 56 targeted cases PASS; only exact child/expected choice or explicit unresolved xsi:type at correct child under exact response root on selected-XSD INVALID can trigger. No invented root, string-only match, alias, waiver, normalization or XSD/resolver/runtime implementation change. 78 reviewed / 0 implemented; 114 not applicable. Publication boundaries unchanged.

Exact declarative trigger branches (all require selected-profile INVALID):

- selected profile is the complete official original VDV-301-1.0 aggregate with exact pinned dependency family or exact later official self-contained TicketingService V1.0 at VDV-301-2.0 through VDV-301-2.3; isolated original service excluded; selected-XSD result must be INVALID
- branch A: actual unqualified direct child TicketingSevice.GetTariffInformationResponseData under exact TicketingService.GetTariffInformationResponse or TicketingService.RetrieveTariffInformationResponse root at the data/error choice position; schema rejection SCHEMAV_ELEMENT_CONTENT expects TicketingService.GetTariffInformationResponseData or OperationErrorMessage; require actual node/path and expected choice together
- OR branch B: actual explicit xsi:type resolves to the exact misspelled unqualified TicketingSevice.GetTariffInformationResponseDataStructure on the correctly spelled TicketingService.GetTariffInformationResponseData child under either exact tariff response root; OR TicketingSevice.ValidateTicketResponseDataStructure on correctly spelled TicketingService.ValidationResponseData under exact TicketingService.ValidateTicketResponse root; verified unresolved-type SCHEMAV_CVC_ELT_4_2; require exact type, node/path and selected declaration context
- do not trigger for typo in invented root, missing child, unrelated child/type, wrong child position after completed choice, mere table captions or string-only matches; xsi:type optional, not required; no alias, normalization or result change

Historical EV-158 and frozen classification report remain unchanged. The earlier label-only/no-runtime assessment is explicitly superseded by direct body and executable evidence. The advisory inventory increases from 77 to 78, not the finding inventory (192). No executable matcher implemented. Next finding TS-001 not started.
