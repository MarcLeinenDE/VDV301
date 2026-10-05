# Current-standard source-locator revalidation — BG-001 / BG-002

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete Base/General findings; no new finding progress credit.

## Source-surface applicability

Both findings are **XSD/release-provenance findings**. Their canonical locator entries contain no PDF locators.

Therefore the visible-body rule is **not applicable** to this block. No PDF page is invented merely to satisfy the body-verification backlog. The current-standard revalidation instead follows the actual authoritative source surface: exact official upstream release tags, file paths and Git blob identities.

## Fresh official upstream reconstruction

Repository: `VDVde/VDV301`

### VDV-301-1.0

- `IBIS-IP_JourneyInformationService_V1.0.xsd` — `1ee4d7aeb15f3269c5335313be9e214bdb519d2e`
- `IBIS-IP_PassengerCountingService_V1.0.xsd` — `600a3ee6290c630a4435fb06ca9803dabaceb788`
- `IBIS-IP_SystemManagementService_V1.0.xsd` — `85390f99d6c19c88923ed9a5fc8a5706137708af`
- `IBIS-IP_TicketInformationService_V1.0.xsd` — `017ca64666e25d757fc0cde1f1be817f06a743fc`
- `IBIS_IP_V1.0.xsd` — `41289eaed2674a169fdf77a10a2eff293c76d5c4`

### VDV-301-2.0

- `IBIS-IP_JourneyInformationService_V1.0.xsd` — `8c303db5a9c0548d66b90174d9c329d33092ad24`
- `IBIS-IP_PassengerCountingService_V1.0.xsd` — `4161872be76740abfdd1cddf96f8a736333fc8be`
- `IBIS-IP_SystemManagementService_V1.0.xsd` — `2d32630a0f1981e980e6a466e3f6a69136410f24`
- `IBIS-IP_TicketInformationService_V1.0.xsd` — `3fda66d872ab0d1c511247f13e715cf3ad56afe7`
- `IBIS_IP_V1.0.xsd` — **absent (GitHub contents lookup returns 404)**

The stored source locators therefore still match the exact official upstream release contexts.

## BG-001 — same service/version label does not uniquely identify historical schema bytes

The four same-path V1.0 service files again resolve to different official blobs between the two release tags.

The active disproof attempt was retained: a changed blob does not by itself prove a changed payload-validity model. That counter-explanation remains valid. The observed changes include packaging/self-containment changes such as service operation groups and global element declarations. The TicketInformationService comparison also shows declaration-content differences. This strengthens the need for exact release routing, but does not justify treating every blob difference as an independent validation-rule change.

Result: no semantic change. Classification remains `version_routing_issue` / non-defect; selected exact XSD/release pool remains authority; latest-same-name substitution remains forbidden; SDK behavior remains a routing/provenance warning; no PDF locator applies.

## BG-002 — historical aggregate belongs only to VDV-301-1.0 packaging

The exact aggregate `IBIS_IP_V1.0.xsd` is present at tag `VDV-301-1.0` with blob `41289eaed2674a169fdf77a10a2eff293c76d5c4`. The same path is absent at tag `VDV-301-2.0`. The later release instead contains the self-contained V1.0 service schemas.

The strongest disproof attempt also fails: the missing aggregate is not evidence of a broken later dependency chain. It is release packaging history. Reconstructing or mixing the old aggregate into the later release would create authority that upstream did not publish.

Result: no semantic change. Classification remains `intentional_design_misread` / non-defect; the aggregate is authoritative only in VDV-301-1.0; later profiles use their actually published schema pool; no synthetic official aggregate is permitted; SDK behavior remains `no_runtime_diagnostic`; no PDF locator applies.

## Current-standard accounting

After this block:

- BG-001: `verified_current_standard`
- BG-002: `verified_current_standard`
- structural locator count remains **40**
- current-standard/body-registry verified count becomes **19**
- pending current-standard revalidation becomes **21**
- next pending finding: **CE-001**

The term `body-registry` is retained because that is the existing registry name. For these two XSD-only findings, verification means that the current body-locator rule was applied and correctly determined that there is no PDF body surface to inspect; the exact authoritative XSD/release provenance was revalidated instead.

## Gate

- GitHub Actions run: **37288058025**
- result: **SUCCESS**
- validated commit: `c85b87ad8442660ce3138d08e82747d3757e331b`
- structural locators: **40**
- current-standard/body-registry verified: **19**
- pending current-standard revalidation: **21**
- next pending finding: **CE-001**

The gate verified CURRENT_STATE/body-registry synchronization, the new BG-001/BG-002 exact XSD-locator assertions, and the existing audit regression suite.
