# Version-scope boundary review — CE-020 — 2026-10-08

Status: **verified / scope unchanged**.

## Finding
CE-020 is not a generic InternationalTextType mismatch. It is the **Common V2.3 authority split** between:
- official Common V2.3 (default authority), whose InternationalTextType uses `xs:string` / `xs:language`;
- retained upstream PR #30 (explicit candidate overlay), whose InternationalTextType uses `IBIS-IP.string` / `IBIS-IP.language` and therefore matches the official PDF wording.

The two XSD variants accept different instance shapes. There is no latest-wins behaviour.

## Lower boundary
Common V2.2 uses the primitive `xs:string` / `xs:language` form and has no corresponding retained alternate authority variant in the canonical variant inventory. CE-020 therefore does not extend backward to V2.2.

## Affected boundary
Common V2.3 has two explicit executable authorities:
1. official V2.3 XSD — default;
2. PR #30 candidate overlay — explicit opt-in only.

Actual PASS/FAIL always follows the explicitly selected XSD variant.

## Upper boundary
Selected Common V2.4 again uses the primitive `xs:string` / `xs:language` form and has no corresponding retained alternate authority variant. CE-020 therefore does not extend forward to V2.4.

## Boundary conclusion
Existing scope is confirmed unchanged:
- Common V2.3 official authority;
- Common V2.3 PR #30 candidate/integration authority.

No predecessor or successor authority split is present.

## SDK consequence
The SDK must require explicit authority/variant selection whenever this V2.3 split is relevant. It must never silently replace official V2.3 with PR #30 or vice versa, and must never apply latest-wins semantics.
