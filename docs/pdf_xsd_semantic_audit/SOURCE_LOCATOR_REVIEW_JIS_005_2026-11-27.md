# Source locator review — JIS-005

Date: 2026-11-27. Existing confirmed_pdf_defect, selected_xsd, error_with_advisory, xsd_invalid_advisory, reviewed_not_implemented unchanged.

## Original body and independent version context

JIS V1.0 RetrieveSpecificGNSSPointInformationResponse successful choice row is SpecificGNSSPointInformationData in EN January 2014 p78 Table 69 and DE July 2016 p17 Table 21, whereas both exact historical and selected official XSDs name the element SpecificGNSSPointInformation and its type JourneyInformationService.SpecificGNSSPointInformationData. Archived EV-152 confirms correct name PASS and PDF name FAIL. Retain confirmed_pdf_defect, error_with_advisory and strict XSD authority; no alias, XSD or runtime change.

- EN January 2014 p78 §9.6.13.2 Table 69 successful choice label SpecificGNSSPointInformationData, correct qualified structure type, alternative OperationErrorMessage; Table 70 correct structure name and required TimeStamp/GNSSPoint. Request Table 68 GNSSPointRef unchanged. EN p77 Tables 63/66 and p79 Table 72 use Data suffix for TSP, Timing and Beacon, consistent with the corresponding XSDs.
- DE July 2016 p17 §1.14.2 Tables 21/22 show same name/type conflict. Table 20 GNSSPointRef unchanged. Exact pinned renders visually checked.

## Exact XSD and active disproof

Historical official VDV-301-1.0 type-only JIS lines 125-136 and aggregate global 54 / group 87 define the same local choice name as selected official VDV-301-2.0 JIS lines 175-187. Both use a required choice of SpecificGNSSPointInformation (type JourneyInformationService.SpecificGNSSPointInformationData) or OperationErrorMessage. The latter is not a second successful alias. The type defines required TimeStamp and GNSSPoint. The Data suffix is common in neighboring choice declarations (Stop, TSP, Timing and Beacon), but not this one; pattern-derived renaming or inferring name from type is unsafe. The mismatch is present in both verified historical editions, not a later translation issue. Prior JIS-001 catalog boundary and JIS-003 later tag/branch checks reused, no fresh catalog query. No independently established later official correction. Selected XSD remains normative; classification unchanged, no attribution of definitive original author intention.

## Executable evidence and SDK impact

Archived EV-152 positive and negative XML samples inspected and hashed; only the choice name differs. Archived result positive true and negative false: unexpected SpecificGNSSPointInformationData, expected SpecificGNSSPointInformation or OperationErrorMessage. This is reused executable evidence, not a new EV-152 test or fresh historical aggregate compile. The reviewed runtime mapping is not implemented; only decorate existing INVALID for exact official JIS V1.0 and matching choice-element error; no normalization or alias. No XSD mutation, no new runtime implementation.

## Evidence

- EV-152 run 34113437268 SUCCESS previously rechecked; archived ZIP 10015273758 SHA256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently rechecked. DE original p17 PNG SHA256 05e250698030a3d2af1b569d918c82e47c2b14092a8510030b261d206368b6ef size 346188 verified and visually inspected. JIS_V1.0 PDF SHA256 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73 size 772125, pin 34103529949. No new DE raw download.
- EN exact-source fallback run 45997275428 SUCCESS artifact 15196706616 ZIP SHA256 ab7326c057c7b19bd3ff94be20c928b8b8845f19b1894755b082e093f8c9a3c9; VDV301-2_V1.0_EN source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; p77 PNG 35c4cd2cef7231838f50005e8eb94b13bad5657ee333378fb210d9e0d216f604 size 283763; p78 1cfd97a9e5aa56ab4fe9391b97397f7901dac6741420d409b08c3e4cfc06e85d size 230158; p79 c290c08882023b58cae3ea2f49b5b3921f5e7475b1ed7221fd9e0476919dba5d size 259498. ZIP and all manifest PNG hashes and sizes verified; all three pages visually inspected.
- Historical official VDV-301-1.0 JIS type-only blob 1ee4d7aeb15f3269c5335313be9e214bdb519d2e lines 120-136 (choice 127; type 131-136) and aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4 globals 53-54 and group 86-87; selected VDV-301-2.0 JIS 8c303db5a9c0548d66b90174d9c329d33092ad24 lines 169-187 (root 175, choice 178, data type 182-187); actual selected branch blob identical. Prior JIS-003 later upstream tags/branch identical JIS blob check retained. Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enum a9bea5bc73003ed91ded8519db06c32c4067831d exact route unchanged.
- EV-152 archived result JSON SHA256 cd219d84e018a5f9809799334c364e1a87ab71b1d90fef757d9da0f27e5cb7c8; positive sample 5c11ea4f8b07e796f1c281d13c27ed71ed47e5293c9c1d67b6fcdb84492019a6 size 519; negative sample 65f6ea8d74989c8f6fad201dc241a554936e88427094781d515417cc462cb61c size 527. Inspected same payload with only choice start/end tag renamed; archived positive true, negative false, expected SpecificGNSSPointInformation or OperationErrorMessage. No new instance run or historical aggregate compilation.
- Neighboring EN p77 Tables 63/66 and p79 Table 72 show Data-suffixed TSP, Timing and Beacon choice rows matching historical and selected XSDs (selected lines 138,158,198); Stop line 118 also uses Data. GNSS is an exception in these declarations; naming pattern is not executable authority. The matching type and fields TimeStamp/GNSSPoint remain unchanged. Runtime mapping reviewed_not_implemented, exact official scope, xsd_invalid_advisory with xsd_result_invalid and decorate_existing_invalid; no normalization.
- JIS-001 catalog boundary dated 2026-11-25 reused: no independently established separate DE 2014 aggregate, EN 2016 standalone, earlier/later standalone publication. No fresh catalog lookup; both language body tables directly checked.

## Closure

132/192 locator/body/boundary entries pending both CI gates. All five JIS findings covered. Next LS-001 only after terminal closure and memory review.
