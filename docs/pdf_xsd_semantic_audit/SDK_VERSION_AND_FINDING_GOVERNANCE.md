# SDK version and finding governance

Status: canonical project rule.

## Purpose

The SDK must validate every supported VDV 301 profile against the authority selected for that exact profile and preserve enough verified context to explain an audit result in short and long form.

## Immutable historical findings

Findings are version-bound facts. A correction in a later VDV version, candidate, pull request or integration profile **never retroactively removes, weakens or rewrites a finding in an older profile**.

If V2.0 contains a defect and V2.4 corrects it, V2.0 remains reproducibly testable with the V2.0 behavior. The later correction is version-history evidence only.

Consequences:

- never apply "latest wins" to findings, schemas, dependencies or remediation;
- never silently backport a later correction into an older conformance profile;
- retain historical findings and their exact source locators;
- diagnostics may state that a later profile corrected the issue, but PASS/FAIL for the selected historical profile remains unchanged.

## PASS/FAIL authority

Where an XSD exists for the selected profile, that selected XSD remains the executable source of truth for XML PASS/FAIL. A confirmed typo or defect in the XSD does not turn a schema-invalid provider message into PASS.

Known Issues add explanation; they do not override normative validation.

## Candidate / integration profiles

Candidate and integration profiles are included in the SDK so the available VDV 301 1.x/2.x version landscape can be tested through V2.4.

They must remain explicitly labelled non-official and must never be presented as an official VDV release. Candidate/integration findings and corrections are version-scoped exactly like official-release findings.

Where a defect is found in a PR candidate, a correction may be contributed to that PR with a technical explanation so the correction remains discoverable even while the upstream Git repository is not actively maintained.

## Unpublished/future profile boundary

VDV is working on a 3.0 redesign. The existing 1.x/2.x SDK remains a separate compatibility and audit baseline because these profiles remain in operational use. unpublished/future-profile rules must not be inferred into or retroactively applied to 1.x/2.x profiles.

Future unpublished/future-profile support must be modelled as a separate generation/profile family unless verified source evidence justifies a specific compatibility relationship.

## Diagnostic contract

For a triggered finding, the SDK/audit tooling should be able to provide:

1. PASS/FAIL from the exact selected authority;
2. short user-facing explanation;
3. detailed technical explanation;
4. exact service/profile/version and authority class;
5. finding classification;
6. exact PDF and XSD source locators where applicable;
7. rationale and provider expectation;
8. version history, including later corrections without retroactive reinterpretation;
9. correction/PR status where known;
10. explicit separation between conformance result and a known VDV artifact issue.

Unverified assumptions must not be promoted to hard audit criteria.

## VDV feedback/export

A dedicated VDV error dossier is no longer a mandatory project deliverable. The canonical finding data must nevertheless remain sufficiently structured and sourced that a VDV-facing working document can be generated later without re-auditing the findings.
