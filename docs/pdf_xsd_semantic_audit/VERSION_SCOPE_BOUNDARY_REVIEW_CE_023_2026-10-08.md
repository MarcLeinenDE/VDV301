# Version-scope boundary review — CE-023 — 2026-10-08

Status: **verified / corrected V2.2-V2.3 scope confirmed**.

## Finding
CE-023 is documentation-only: a second table labelled as `NetexMode` actually contains the `Message` structure fields. The exact selected XSDs contain the correct NetexMode choice model, so no XML validation exception follows.

## Lower boundary
Common V2.1 is not affected. The relevant NetexMode family is introduced in V2.2; there is no corresponding duplicate-table defect to extend CE-023 backward.

## Affected releases
### V2.2
Printed p.26 visibly shows section 2.34 NetexMode with a table body containing Message-ID, TimeStamp, MessageType and MessageText, while the exact V2.2 XSD contains the proper NetexMode choice model.

### V2.3
The prior V2.3 scope withdrawal is superseded. Exact-byte visible revalidation showed that p.26 begins section 2.34 and p.27 continues with the corrupt Message table captioned as NetexMode. V2.3 is therefore affected.

## Upper boundary
Common V2.4 is an explicit negative control. Visible p.29 has section 2.34 `Point`; the corrupt second NetexMode table is absent.

## Boundary conclusion
CE-023 affects **Common V2.2 and V2.3 only**. V2.1 and V2.4 are outside scope.

The older 2026-09-28 V2.2-only conclusion is retained solely as historical evidence and is superseded by the 2026-10-06 exact-byte correction.

## SDK consequence
No XSD special handling, alias, patch, PASS/FAIL override or runtime matcher is created. CE-023 remains documentation-only informational guidance for V2.2/V2.3 documentation context.
