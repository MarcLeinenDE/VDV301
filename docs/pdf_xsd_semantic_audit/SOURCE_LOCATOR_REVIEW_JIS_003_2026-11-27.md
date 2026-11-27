# Source locator review — JIS-003

Date: 2026-11-27. Existing confirmed cross_artifact_mismatch, selected_xsd, error_with_advisory, xsd_invalid_advisory, reviewed_not_implemented unchanged.

## Original body and independent version context

JIS V1.0 PDF ListAllLineInformation response data permits LineInformation 1:* in EN January 2014 and DE July 2016, while both exact historical and selected official XSDs omit maxOccurs (default 1). Existing cross_artifact_mismatch/error_with_advisory unchanged; no XSD or runtime change.

- EN January 2014: p79 §9.6.16 ListAllLineInformation, §9.6.16.1 no request structure; p80 §9.6.16.2, Table 76 outer choice; Table 77 inner ordinary LineInformation 1:* and TimeStamp 1:1. Table 75 DisplayContent and Table 79 Destination use 1:* in adjacent list structures. Body headings/captions visually inspected from the pinned fallback.
- DE July 2016: p19 §1.17 and §1.17.2, Table 28 outer choice, Table 29 inner ordinary LineInformation 1:* and TimeStamp 1:1. No choice marker or grouping on the member. Archived pinned DE render verified and visually inspected.

## Exact XSD and active disproof

Historical official VDV-301-1.0 type-only JIS line 178 and selected official VDV-301-2.0 JIS line 233 both declare LineInformation of LineInformationStructure without minOccurs/maxOccurs. Both default to 1. The historical aggregate declares the same response root and includes the exact historical type file. Common and Enum identities unchanged. Common LineInformationStructure has exactly one LineRef, optional repeatable names; no nested list of independent lines. Thus neither the outer choice nor localized names nor historical packaging nor version mismatch explains away the discrepancy. In selected JIS, other list members DisplayContent (219), Destination (247), ViaPoint (261), AdditionalDisplayInformation (275) explicitly use maxOccurs=unbounded. This strongly suggests a missing maxOccurs in JIS, but without an authoritative correction source retain cross_artifact_mismatch, not confirmed XSD attribution. Official tags 2.1/2.2/2.3 and current upstream master JIS unchanged. JIS-001 boundary catalog reused, not newly queried. No earlier/later standalone edition independently verified.

## Executable evidence and SDK impact

Archived EV-152 positive one-line sample PASS and otherwise equivalent two-line sample FAIL, unexpected LineInformation; checked both samples and result JSON against the verified archive. No new dedicated EV-152 execution or historical aggregate compilation. Existing runtime mapping requires exact selected profile and normative XSD INVALID caused by second LineInformation in AllLineInformationData. Preserve FAIL, add bilingual advisory only; no override, normalization or XSD patch. No implementation or classification changes.

## Evidence

- EV-152 run 34113437268 SUCCESS rechecked, artifact 10015273758 ZIP SHA256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently verified; DE page 19 PNG SHA256 e011920ad88ddb14bef706c77f24993838a4748ef8c45c1e63653504f5c237cf (280952 bytes) visually read. PDF JIS_V1.0 SHA256 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73 size 772125; pin run 34103529949, artifact 10011459459. No fresh DE raw PDF download.
- EN exact-source fallback run 45954025437, artifact 15178500096 ZIP SHA256 a3bbea84c8a4b07d75a606424152d9b2211bbeacf2fea099bfb3099a85708ff8 verified; source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; EN p79 PNG c290c08882023b58cae3ea2f49b5b3921f5e7475b1ed7221fd9e0476919dba5d (259498 bytes), p80 6cd3d88ce250f80b8839bd2a320b4d6c9f38f7375f57a4f0e622f8ec946b3530 (247793 bytes), both verified against manifest and visually read.
- Exact upstream VDV-301-1.0 JIS type-only blob 1ee4d7aeb15f3269c5335313be9e214bdb519d2e lines 175-180 and aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4 lines 4-7,58,91; selected VDV-301-2.0 JIS 8c303db5a9c0548d66b90174d9c329d33092ad24 lines 223-235; upstream 2.1/2.2/2.3/master same JIS blob rechecked. Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enum a9bea5bc73003ed91ded8519db06c32c4067831d identical in historical and selected routes. Common LineInformationStructure lines 380-387 has required singular LineRef and optional repeatable text fields, not a list of lines.
- EV-152 archived sample and JSON independently checked: one line PASS, two lines FAIL (unexpected LineInformation); positive XML SHA256 87d40e3dc94234fe125d82dde97a78ad8cc6bbcd18d4ee9d49eaec8ddd65e7aa, negative e13cccaf1db69b0b7c77621824aa2ed3ee964aa9fdac182fb9eebbd579271b64. Existing selected-route execution, no fresh dedicated test or historical aggregate compilation claimed.
- Reuse JIS-001 catalog boundary dated 2026-11-25; no separately established DE aggregate 2014, EN standalone 2016 or earlier/later standalone publication. Both original body tables directly checked, not extrapolated. No fresh catalog lookup.

## Closure

130/192 locator/body/boundary entries pending both CI gates. Next JIS-004 only after terminal closure and memory review.
