# Version-scope boundary review — CIS-001 — 2026-10-08

Status: **verified / scope unchanged / strict CIS V1.1 remains unsupported**.

## Finding and authority
CIS-001 concerns the **release-authority gap** for CustomerInformationService V1.1, not a claim that a matching official schema exists.

The byte-pinned official V1.1 PDF (SHA-256 `f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739`) explicitly includes `SpeakerActive` and `StopInformationActive` in VehicleInformationGroup (printed pp. 13 and 20). The upstream **untagged** historical working V1.1 CIS XSD, commit `0a5228a768c7d710c40f5f99fbdce2e544d19883`, blob `5957e27f128a191c794b0c8081b531a07126784a`, lacks both fields. That working file is evidence only.

## Lower boundary (predecessor)
The official `VDV-301-1.0` release tree contains `IBIS-IP_CustomerInformationService_V1.0.xsd` (blob `7a95fc03c06c8c84d078bf06d18ef5873a15c215`); it has its own tagged release authority and does **not** share this V1.1 authority gap.

## Affected boundary
The official V1.1 PDF was published, but no matching **VDV-301-1.1 release tag** with normative CIS V1.1 XSD authority is established. The untagged V1.1 working snapshot is also materially behind the published document. Do not promote it or treat the PDF as an executable XSD.

## Upper boundary (successor)
The official `VDV-301-2.0` release tree includes `IBIS-IP_CustomerInformationService_V2.0.xsd` (blob `fa8f0a51ad5f612660c9532c8557ad1ca473a908`). The V1.1-specific authority gap must not be propagated to the V2.0 profile.

## Boundary conclusion and SDK consequence
**CIS V1.1 only: unresolved official release-XSD authority.** Maintain `unsupported_profile` / fail-closed for strict CIS V1.1. Do not substitute V1.0, V2.0, or the untagged V1.1 snapshot, and do not apply latest-wins routing. Existing semantic/routing decision unchanged.
