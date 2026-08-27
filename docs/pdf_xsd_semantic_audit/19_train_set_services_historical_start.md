# TrainSet services V2.1 / V2.2 historical audit start

Status: provenance, dependency routing and semantic first pass completed. Local XSD compilation/sample validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
c4a23a218eb55458026f7720915a23c7637f08dd
```

Scope:

```text
VDV 301-2-14 TrainSetInformationService / TrainSetManagementService / TrainSetDataService V2.1
VDV 301-2-14 same three services V2.2
official VDVde/VDV301 tags VDV-301-2.1 and VDV-301-2.2
```

## 1. Service profiles must remain separate

The document groups three services, but the XSD dependency families are not interchangeable.

### V2.1

```text
TrainSetDataService V2.1
  -> Common V2.0
  -> Enumerations V2.0
  -> CustomerInformationService V2.0 (direct include)

TrainSetInformationService V2.1
  -> Common V2.0

TrainSetManagementService V2.1
  -> Common V2.0
  -> Enumerations V2.0
  -> TrainSetInformationService V2.1
```

Official blobs:

```text
TrainSetDataService_V2.1         c2cdb73fcae265a2e4e0349ac6072e3548e36d8b
TrainSetInformationService_V2.1  897f373e31b76aa23d8bc206854b042524e4c102
TrainSetManagementService_V2.1   add9d1cb37e5759ff7a77855b239108d38373206
```

### V2.2

```text
TrainSetDataService V2.2
  -> Common V2.2
  -> Enumerations V2.2
  [CustomerInformationService V2.2 include is commented out]

TrainSetInformationService V2.2
  -> Common V2.2

TrainSetManagementService V2.2
  -> Common V2.2
  -> Enumerations V2.2
  -> TrainSetInformationService V2.2
```

Official blobs:

```text
TrainSetDataService_V2.2         7a132894c281d613e16514a6fa1bcbffe713d066
TrainSetInformationService_V2.2  7ab1f8f892bfcea2a8b8a055f07de92c143356f9
TrainSetManagementService_V2.2   da9465d6683e3f7d54a546ab4a13739fb3c3e902
```

The V2.2 branch files match those official blobs.

## 2. V2.1 -> V2.2 is a technical-correction release

The V2.2 document history states there are no functional upgrades, but records technical corrections including:

```text
- TrainSetInformationService composition response corrected to support multiple coaches through SingleCoachInATrainSet.
- TrainSetManagementService response root renamed from TrainSetManagementService.GetTrainSetComposition to ...GetTrainSetCompositionResponse.
- TrainSetDataService receives specific TrainSetSubscribeRequestStructure and TrainSetUnsubscribeRequestStructure for parameterized Retrieve subscriptions.
```

This history is direct evidence for the historical XSD findings below.

## 3. Initial findings

```text
TSI-001  V2.1 composition structure cannot represent the documented sequence of coaches; corrected in V2.2.
TSM-001  V2.1 GetTrainSetComposition response root lacks Response suffix; explicitly corrected in V2.2.
TSM-002  V2.2 global root is corrected, but TrainSetManagementServiceOperations still contains the stale V2.1 name.
TSD-001  V2.1 PDF defines parameterized Subscribe/Unsubscribe TripRef/TripInformation operations, but V2.1 service XSD contains only Retrieve operations; V2.2 adds the missing technical model.
TSD-002  V2.2 operation overview still lists Retrieve*RequestStructure for Unsubscribe requests while detailed text and XSD use TrainSetUnsubscribeRequestStructure.
TSD-003  V2.2 Subscribe*Response names have generic SubscribeResponseStructure types in the operation group but Retrieve*ResponseStructure types as global elements; generic-response modelling requires targeted technical review.
```

No XSD is changed by this audit block.
