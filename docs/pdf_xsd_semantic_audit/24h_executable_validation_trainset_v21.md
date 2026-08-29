# EV-109 – TrainSet V2.1 Deep Read executable evidence

Status: completed 2026-08-29.

## Purpose

EV-109 turns the three material V2.1 TrainSet findings from static observations into executable evidence against the exact official V2.1 schema families.

No schema is modified by this harness.

Tool:

```text
tools/validate_trainset_v21_ev109.py
```

Canonical workflow:

```text
.github/workflows/schema-audit-validation.yml
trigger: workflow_dispatch only
```

Successful run:

```text
run_id: 33228250613
result: PASS
artifact_id: 9707593736
artifact_zip_sha256: 853fec658c7f76f9afedca18ee2017259c9ad3d94b6ac7f6cd42f02b08126b78
```

## Authority

Exact official VDV-301-2.1 service schemas:

```text
TSI V2.1  IBIS-IP_TrainSetInformationService_V2.1.xsd
           blob 897f373e31b76aa23d8bc206854b042524e4c102

TSM V2.1  IBIS-IP_TrainSetManagementService_V2.1.xsd
           blob add9d1cb37e5759ff7a77855b239108d38373206

TSD V2.1  IBIS-IP_TrainSetDataService_V2.1.xsd
           blob c2cdb73fcae265a2e4e0349ac6072e3548e36d8b
```

The stored files are byte-identical to the official upstream tag `VDV-301-2.1`.

## TSI-001

EV-109 confirms:

```text
flat field order:
CoachType
CoachNumber
FrontCabin
RearCabin
CoachPositionInTrainSet
CoupledSide
CoachState

repeated coach wrapper: absent
one coach record: VALID
second PDF-described coach record: INVALID
```

Representative rejection:

```text
Element 'CoachNumber': This element is not expected.
```

Result:

```text
TSI-001 executable-confirmed
```

## TSM-001

EV-109 confirms:

```text
V2.1 global root:
TrainSetManagementService.GetTrainSetComposition
  -> TrainSetInformationService.GetTrainSetCompositionResponseStructure

later corrected root:
TrainSetManagementService.GetTrainSetCompositionResponse
  -> absent in V2.1
```

Samples:

```text
old-name V2.1 root: VALID
later ...Response root: INVALID / no matching global declaration
```

Result:

```text
TSM-001 executable-confirmed
```

## TSD-001

EV-109 confirms that the V2.1 TrainSetDataService operation group and global roots contain the four Retrieve members:

```text
RetrieveTripRefRequest
RetrieveTripRefResponse
RetrieveTripInformationRequest
RetrieveTripInformationResponse
```

The service-prefixed Subscribe/Unsubscribe members described by the PDF are absent from the V2.1 service schema.

Control:

```text
generic Common V2.0 Subscribe/Unsubscribe structures exist
```

Therefore the precise finding is not "subscription is impossible"; it is the service-specific TrainSetDataService operation/root modelling gap.

Result:

```text
TSD-001 executable-confirmed with generic-subscription context note
```

## Full-suite result

The same run also confirmed:

```text
50/50 root XSD compile
39 XSD service profiles
84 direct include edges
existing EV suite PASS
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

## SDK rule

EV-109 does not authorize schema repair or aliases.

```text
TSI V2.1 -> validate exactly against the flat official V2.1 response model
TSM V2.1 -> retain the exact old root name; no later-version alias
TSD V2.1 -> do not invent service-prefixed subscription roots absent from the selected XSD
```

The findings may explain strict-validation results; the selected XSD remains normative executable authority.
