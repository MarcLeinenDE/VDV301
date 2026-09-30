# External protocol and referenced-standard authority policy

Status: SDK/audit governance baseline.

## Purpose

VDV 301 uses standardized protocols such as HTTP, TCP, UDP, DNS/DNS-SD, SNTP/NTP, RTSP and RTP. The SDK must validate not only the VDV-specific selection and specialization of those protocols, but also the externally standardized protocol semantics that are actually required by that selected VDV profile.

This policy defines how such external requirements become executable audit authority without inventing requirements that VDV 301 did not select.

## Authority chain

For every protocol/runtime check, resolve the authority chain in this order:

1. Select the exact VDV service/document/profile/version that applies.
2. Establish whether that VDV profile requires, selects, references, permits or specializes an external protocol.
3. Resolve the exact external standard/version selected by the VDV profile where the VDV source identifies one.
4. Identify the exact external normative requirement needed for the VDV-selected protocol use.
5. Apply any explicit VDV profile exception or specialization before generic external-standard behavior.
6. Execute only checks whose applicability to the selected VDV profile has been proven.

The result must retain both the VDV source and the external-standard source. An external standard does not become a free-standing source of new VDV requirements merely because the technology is used somewhere in IBIS-IP.

## Normative result classes

### VDV-native requirement

An explicit VDV requirement is reported as VDV normative authority.

### External normative requirement referenced/selected by VDV

When correct implementation of a protocol selected by the applicable VDV profile necessarily depends on an external normative requirement, the SDK may enforce that requirement.

A hard failure requires all of the following:

- the applicable VDV profile selects or requires the relevant protocol/use;
- the exact external standard/version authority is resolved or the applicable external requirement is otherwise unambiguous for that profile;
- the cited external requirement is normative for the observed behavior;
- the requirement is applicable to the concrete message/role/state under test;
- no VDV-specific exception or specialization overrides it.

Diagnostics must identify the VDV selection/profile and the exact external normative source separately.

### External standard not selected by VDV

A modern, successor or generally recommended external standard must not silently replace the standard selected by the VDV profile.

It may be used for an informational compatibility/security observation only when clearly labelled as such.

## Requirement levels

External-standard keywords and semantics must retain their real normative strength.

- mandatory normative requirement applicable to the selected profile -> eligible for FAIL;
- conditional mandatory requirement -> FAIL only when its condition is proven true;
- recommendation/SHOULD -> warning/advisory unless another applicable authority makes it mandatory;
- MAY/optional behavior -> never fail merely because it is not implemented;
- implementation guidance/best practice -> diagnostic only.

The SDK must not convert a SHOULD, recommendation or best practice into a VDV hard failure.

## VDV specialization wins within the selected profile

If a VDV service/profile deliberately specializes generic protocol behavior, the VDV-specific rule governs that VDV profile.

The generic standard remains relevant for all non-overridden semantics. The specialization must be recorded explicitly; it must not be generalized to unrelated services or versions.

## No latest-standard-wins

External protocol authority is version-bound just like VDV/XSD authority.

If a historical VDV profile explicitly selects an older RFC/standard, a newer RFC that obsoletes it must not silently change historical PASS/FAIL behavior. Newer standards may be reported separately as compatibility, security or modernization information.

## Evidence required before implementation

Every executable external-protocol rule must record at least:

- stable rule/check ID;
- applicable VDV service/profile/version;
- exact VDV source locator establishing protocol selection/reference/specialization;
- external standard identifier and version/revision;
- exact section locator for the external normative requirement;
- normative strength and any applicability condition;
- validation layer and observable trigger;
- result severity;
- any VDV exception/specialization;
- bilingual DE/EN diagnostic text before public SDK exposure.

Where practical, deterministic executable evidence should prove both a conforming and a violating case.

## Interaction with XSD authority

XSD remains the executable authority for XML structure/content in the selected schema profile. External protocol checks are separate validation layers.

A payload can therefore be XSD-valid and still fail an applicable HTTP/DNS-SD/SNTP/etc. requirement, or be protocol-valid while its XML fails XSD validation. The SDK must report these as separate checks with separate authority sources.

## HTTP Content-Type example

If the selected VDV profile uses HTTP to transfer an XML representation:

- VDV establishes the applicable HTTP/XML communication context;
- HTTP media-type syntax and semantics come from the applicable HTTP standard;
- XML media-type semantics may additionally come from the applicable XML media-type standard;
- an invalid media-type syntax may be an external-protocol FAIL when the normative rule and applicability are proven;
- absence of Content-Type must not be called a VDV hard failure merely because sending it is recommended by an external standard;
- a declared non-XML media type for a payload that the selected VDV profile requires to be XML may be evaluated as combined VDV + external-standard semantics, with both authorities disclosed.

This preserves the distinction between a VDV requirement, a referenced external normative requirement and engineering best practice.

## Runtime authority classes

Use the existing authority classes consistently:

- `vdv_normative`
- `external_normative`
- `external_normative_referenced_by_vdv`
- `vdv_profile_exception_or_specialization`
- `combined_semantics`
- `diagnostic_heuristic`

For conformance auditing, prefer `external_normative_referenced_by_vdv` when the external requirement is enforced specifically because the selected VDV profile requires/selects that protocol.

`external_normative` alone does not imply that the rule is automatically a VDV conformance hard-fail.

## Audit rule

Before terminalizing a transport/protocol finding or implementing its runtime matcher, explicitly answer:

1. What exact VDV profile/version applies?
2. What protocol/use does VDV require, select, reference, permit or specialize?
3. What exact external standard/version applies?
4. What exact normative clause is being tested?
5. Is the clause mandatory, conditional, recommended or optional?
6. Is its applicability condition proven by the observed VDV communication?
7. Does VDV override/specialize the generic rule?
8. What result and authority labels will the SDK expose?

If any material authority link is unresolved, do not invent a hard failure. Keep the rule unresolved/profile-check/advisory until the authority chain is complete.
