# Common/Enums V1.0 -> V2.0 XSD enumeration diff

Status: XSD-side first-pass diff.

Source files:

```text
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

Generated CSV:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.csv
```

Inventory CSV:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_v2_0_xsd_inventory.csv
```

## Summary

| Change | V1.0 | V2.0 | Status | Notes |
|---|---|---|---|---|
| Type spelling change | `DataIntervallEnumeration` | `DataIntervalEnumeration` | confirmed XSD delta | Same value set; PDF/history check pending. |
| Type no longer observed | `IBIS-IP-VersionEnumeration` | not observed | confirmed XSD delta | V1.0 had value `1.0`; PDF/history check pending. |
| DeviceState value added | - | `readyForShutdown` | confirmed XSD delta | V2.0 XSD comment explicitly mentions this. |
| Type added | - | `RouteDirectionEnumeration` | confirmed XSD delta | PDF/history check pending. |
| ServiceName value added | - | `PassengerCountingService` | confirmed XSD delta | PDF/history check pending. |
| ServiceName value added | - | `VideoLiveService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceName value added | - | `VideoRecordingService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceName value added | - | `VideoDisplayService` | confirmed XSD delta | V2.0 XSD comment mentions video services added. |
| ServiceState value added | - | `starting` | confirmed XSD delta | PDF/history check pending. |

## Interpretation

No new Common/Enums CE finding is opened by this XSD-side pass alone.

Reason:

```text
The observed changes are XSD-side historical deltas. They become findings only if the matching PDF version/history contradicts, omits or misstates them after PDF-side checking.
```

## Next required check

```text
Compare VDV 301-2-1 V1.0 and V2.0 PDF version history/tables against these XSD deltas.
```
