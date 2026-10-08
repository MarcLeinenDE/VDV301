# Version-scope boundary DISPROOF — DISC-003 — 2026-10-08

Status: **MATERIAL SCOPE CORRECTION REQUIRED / package halted / NOT verified**.

## Existing claim disproved
The frozen semantic classification and source-locator coverage say `DISC-003` is a **German General Conventions V2.3** DNS-SD TXT-record Table 3 omission corrected by **V2.4**. The first affected version is too late: the same German-only omission already exists in **General Conventions V2.2**.

## Newly discovered direct official-PDF evidence — V2.2
Publication: `VDV301-2_GC_V2.2`, official `https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx`. Exact existing repository PDF pin: **SHA-256 `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`**, size `1562305` bytes.

- **German printed p.27**, §3.3.1 `Nutzung des TXT-Records`, **Table 3 `Bedeutungen der TXT-Records in DNS-SD (inklusive Festlegungen für IBIS-IP)`**: the displayed table stops at `ver`, `path`, `multicast`, `sntp-server`. **`coachnumber`, `deviceclass` and `deviceID` are absent**. Confirmed by direct visual screenshot of the official source on 2026-10-08.
- **English printed p.33**, §3.3.2 `Use of TXT Records`, **Table 3**: the same V2.2 document **does include** `coachnumber` (mandatory in Trainset network), `deviceclass` (mandatory from IBIS-IP 2.2), and `deviceID` (mandatory from IBIS-IP 2.2). Confirmed by direct visual screenshot of the official source on 2026-10-08.

Thus V2.2 has the exact **language-specific missing-row** defect previously attributed only to V2.3. This is not a claim that the protocol starts in V2.3 or V2.4.

## Lower boundary controls
- Base **V2.0** official `https://www.vdv.de/301-2-sds-v-2-0.pdfx`, pin SHA `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`: the DNS-SD TXT table lists `ver`, `path`, `multicast`, `sntp-server` in the available German and English sections; none of the three newer attributes is specified in either track (printed pp.35–36). Both tracks agree, so the V2.2 German-only omission cannot be back-applied.
- Base **V2.1** official `https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx`, pin SHA `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`: same earlier table rows in both German and English tracks (printed pp.36–37), with neither language adding the three attributes. Therefore **V2.1 is the last available unaffected predecessor** in this language-mismatch framing. The PDF web screenshot renderer cache-missed on these predecessor pages; the directly opened official PDF text and already pinned source provenance were used as negative-control evidence.

## Continuity and corrected successor
Prior canonical visible-body evidence **still stands**:
- General Conventions **V2.3 German**, printed p.27 Table 3, omits all three, while English lists them: affected.
- General Conventions **V2.4 German**, printed pp.30–31 Table 3, includes all three. Its printed p.75, §7.3.2 version history explicitly says missing entries in the German Table 3 were added. This is the **first corrected successor** and a historical documentation repair, not a new V2.4 protocol feature.
- Existing source locators: `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DISC_003_2026-10-06.md` and EV-126 run `33754189273`.

## Correct boundary requiring canonical correction
**First affected General Conventions V2.2 (German only); affected V2.3 (German only); first corrected V2.4.** V2.0/V2.1 are unaffected by this particular DE/EN omission because their corresponding English TXT tables do not yet carry the three new rows.

## Mandatory next action (do NOT skip)
Stop the current boundary package under `VERSION_SCOPE_BOUNDARY_POLICY.md` due to material semantic-scope correction. Before reclassifying the finding as verified:
1. Amend `audit_registry/finding_semantic_classification_v0.1.json` (version scope, descriptions/diagnostics/source references) to include the **V2.2 German** affected lane without changing the frozen finding ID or XSD authority.
2. Add exact **V2.2 German p.27** and **English p.33** Table 3 PDF body locators to `audit_registry/finding_source_locators_v0.1.json` and align `scope_claims`, evidence and body verification records; preserve the V2.3/V2.4 existing locators.
3. Review any other canonical derived scope/mapping stores, ensuring DISC-003 remains documentation-only and no runtime matcher/XSD rule is introduced.
4. Update the boundary registry as `verified` **only in the same independent correction mini-cycle**, then run full schema-audit-validation and final handoff-integrity gates. Do not resume DISC-004 or the structural locator backlog beforehand.

At this hold point **DISC-003 remains `pending_revalidation` and the counts stay 48/70 verified, 22 pending**.
