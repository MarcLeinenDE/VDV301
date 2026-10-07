# Version-scope boundary review — CE-004 — 2026-10-07

Status: **verified / scope unchanged / V2.1 predecessor proven unaffected**.

## Finding
`CE-004` is the stale `ServiceNameEnumeration` documentation defect: from V2.2 onward the PDF table continues to list `SystemDocumentationService` and `SystemManagementService` although the V2.2 history records their deletion and the addition of `SystemMonitoringService`. The exact selected XSDs do not accept the stale values.

## V2.1 predecessor
The official V2.1 publication and exact official Enumerations V2.1 XSD were checked independently.

The V2.1 PDF ServiceNameEnumeration table contains:
- `SystemDocumentationService`
- `SystemManagementService`

and does not contain `SystemMonitoringService`.

Official `IBIS-IP_Enumerations_V2.1.xsd`, blob `311464690ad60749ed8d326217787e4b8ed0b718`, likewise contains both old names. Therefore they are not stale in V2.1.

## V2.2 first affected boundary
Existing byte-pinned visible-body evidence proves:
- V2.2 history: `SystemDocumentationService` and `SystemManagementService` deleted; `SystemMonitoringService` added;
- V2.2 ServiceNameEnumeration table nevertheless still lists the removed names;
- exact official Enumerations V2.2 contains `SystemMonitoringService` and omits both removed names.

V2.2 is therefore the first affected official version.

## Persistence
- V2.3 official PDF retains the stale names; official Common V2.3 reuses exact Enumerations V2.2.
- V2.4 official PDF retains the stale names; selected candidate/integration Enumerations V2.4 omits them.
- current VDV publication index lists no later Common publication after V2.4.

## Renderer note
The interactive V2.1 screenshot path returned cache-miss. The deterministic fallback cannot redownload from the VDV host in the present runtime because DNS resolution is unavailable. The V2.1 predecessor conclusion is therefore based on official PDF text extraction plus exact official release-tag XSD evidence. Existing V2.2-V2.4 visible-body locators remain byte-pinned.

## Boundary conclusion
- V2.1: unaffected predecessor;
- V2.2: first affected official release;
- V2.3: affected official persistence;
- V2.4: affected official PDF / candidate-integration XSD lane;
- successor after V2.4: none currently published.

Existing semantic scope remains unchanged.

## Consequence
Under the exactly selected XSD, `SystemDocumentationService` and `SystemManagementService` must fail where the selected enumeration omits them. The stale PDF table is explanatory context only and never creates aliases.
