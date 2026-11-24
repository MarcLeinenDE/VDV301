# DRTRAINSET21-002 — independent source/body and version boundary review

Date: 2026-11-24. Frozen identity unchanged; scope extended V2.1 to V2.1+V2.2.

## Original visible evidence

- V2.1 printed p44 §9.1.4 Possible implementation for non-OBU devices in the coach IP network: final paragraph incorrectly attributes equally named composition operations to TrainSetDataService. EV-148 run 34029363792 artifact 9988086415 ZIP sha256 c4e963de40e4684a9625644f9df2fc8f63ebedc8b2bba38736e83723d1c8dfea, p44 PNG ac44110da51217c7e2c9dbee4a30c8ad8eb49964722495a7a4f3c144570ed7fc; rehashed and visually inspected. Raw source pin historical EV148, also raw PDF SHA reverified earlier today in run 45385075482.
- V2.2 printed p46 same visible section and same erroneous attribution. PNG SHA 2723da34cbce712dfabc1b3c234a3706607da79ae70476c809c6780f0bbe509b. Run 45402521643 artifact 14922903550 ZIP SHA256 6e9fa8bbde483cb23c3548541c1a29ee4c012248980e547204d1610a6a37cf1f; exact raw PDF SHA c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e size 1744296; all nine PNG hashes/sizes verified; p24,31,34,35,46 visually inspected.
- V2.2 p31 §5.5.3 and §5.5.3.2 explicitly describe identical composition structure supplied by InformationService and ManagementService and the TSI response type. The unnumbered operation table under §4.5 p24 lists InformationService Get/Subscribe/UnsubscribeTrainSetComposition; the §6.5 table p34–35 lists only TripRef/TripInformation Retrieve/Subscribe/Unsubscribe. These body controls were visually inspected, not inferred from TOC. Other four render pages (25, 26, 30, 45) were hash-checked but not claimed visually inspected. The adjacent GetTrainSetCompositon typo remains separate DRTRAINSET21-003.

## Exact XSD authority and disproof

V2.1
- IBIS-IP_TrainSetInformationService_V2.1.xsd blob 897f373e31b76aa23d8bc206854b042524e4c102 lines 36: Global composition response uses TrainSetInformationService.GetTrainSetCompositionResponseStructure.
- IBIS-IP_TrainSetManagementService_V2.1.xsd blob add9d1cb37e5759ff7a77855b239108d38373206 lines 44: Global composition response uses the same TSI structure. Historical root/group naming differences are separately tracked.
- IBIS-IP_TrainSetDataService_V2.1.xsd blob c2cdb73fcae265a2e4e0349ac6072e3548e36d8b lines 8-27; globals 34-69: TripRef and TripInformation only; no TrainSetComposition operation. Generic subscription context is not a local Composition alias.

V2.2
- IBIS-IP_TrainSetInformationService_V2.2.xsd blob 7ab1f8f892bfcea2a8b8a055f07de92c143356f9 lines 36: Global composition response uses TrainSetInformationService.GetTrainSetCompositionResponseStructure.
- IBIS-IP_TrainSetManagementService_V2.2.xsd blob da9465d6683e3f7d54a546ab4a13739fb3c3e902 lines 44: Global composition response uses the same TSI structure. Historical root/group naming differences are separately tracked.
- IBIS-IP_TrainSetDataService_V2.2.xsd blob 7a132894c281d613e16514a6fa1bcbffe713d066 lines 8-45; globals 52-98: TripRef and TripInformation only; no TrainSetComposition operation. Generic subscription context is not a local Composition alias.

All six blobs match exact upstream VDVde/VDV301 tags VDV-301-2.1/VDV-301-2.2 and work branch. Local operation inventories alone are not universal protocol inventories; the explicit PDF positive/negative controls and XSD globals/groups jointly refute the alternate service-alias explanation. TSM-001/002 historical root/group differences and TSI-001 remain independent, unchanged. ManagementService is the likely intended reference, not an official erratum. No new executable claim, no new XML test required for PDF-only defect; existing EV-109 counter-context retained.

## Scope

Official VDV index https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-24 lists dedicated V2.1 and V2.2 only; no earlier or later dedicated edition found. §9.1.4 is the English technical body shared by the bilingual publication; no separate German §9.1.4 track. First affected V2.1, latest available affected V2.2. No separate German target section; do not assert two independent language occurrences. One logical error; no new ID. No XSD mutation, runtime diagnostic or compatibility alias. Classification confirmed_pdf_defect, documentation_only, no_runtime_effect, no_runtime_diagnostic. All semantic/locator/boundary/body/mapping reference and status mirrors updated; full gates required before terminal closure.
