# Finding revalidation — TicketValidationService (TVS)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `TVS-001` through `TVS-003`. Frozen inventory remains exactly **192 entries**.

## Evidence and authority

- Aggregate evidence: **EV-163**; closure run **34835864267**.
- Successful EV-163 validation run: **34835469790**, job **103948172257**, artifact **10343689439**, digest `sha256:dbba3bbd71adf72f0d44ba540d214291190749f5f8cbe5d0a6341461ad68f140`, head `b2dc3c28bce9dc21591a3e232e12cace90637616`.
- EV-112: official VDV-301-2.1 executable route.
- EV-113: official VDV-301-2.2 executable route.
- EV-114: official VDV-301-2.3 route; the release routes TicketValidationService through the V2.2-named service XSD.
- EV-115: V2.4 **candidate/integration** executable evidence only. No VDV-301-2.4 release tag exists; EV-115 is **not official-release V2.4 XSD conformance**.
- Complete **50-root-XSD pool** passed again. No XSD or frozen-inventory mutation occurred.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| `TVS-001` | `executable_confirmed` | Upstream-master structural confirmation plus EV-115 candidate/integration executable evidence confirms the omitted `GetCurrentShortHaulStopsResponse` operation-group boundary. This does **not** elevate the V2.4 candidate lane to official release authority. |
| `TVS-002` | `executable_confirmed` | Official executable evidence EV-112/EV-113/EV-114 confirms the `VehicleData.RouteDeviation` type behavior across official release routes; EV-115 adds candidate/integration continuity only. |
| `TVS-003` | `executable_confirmed` | Official executable evidence EV-113/EV-114 confirms the `CurrentStopPoint` → `CurrentTariffStop` rename boundary; EV-115 adds candidate/integration continuity only. |

## Post-state

- Terminal: **168 / 192**
- Pending: **24 / 192**
- Next block: **VDS**
- First pending finding: **VDS-001**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
