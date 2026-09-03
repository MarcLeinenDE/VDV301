# Audit correction — COMMON V2.4 InternationalTextType authority — 2026-09-03

## Corrected historical statement

The earlier first-pass file `01g_common_enums_v2_4_datatypes_core_structures.md` stated that the V2.4 XSD model for `InternationalTextType` used `IBIS-IP.string` and `IBIS-IP.language` and therefore aligned with the PDF table. That statement is superseded.

The exact selected V2.4 candidate/integration blobs used by the final Deep Read are:

- `IBIS-IP_common_V2.4.xsd` blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`
- `IBIS-IP_Enumerations_V2.4.xsd` blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`

In that Common blob, `InternationalTextType.Value` is `xs:string` and `Language` is `xs:language`. The official V2.4 PDF table prints the wrapper-reference names `IBIS-IP.string` and `IBIS-IP.language`. EV-122 confirms the executable shape boundary.

## Authority qualification

These XSD bytes are candidate/integration authority, byte-identical to `candidate/dms-v2.4-xsd` / open draft `VDVde/VDV301#31`. They are not promoted to official release authority. No `VDV-301-2.4` release tag resolves.

## Effect

- The historical first-pass conclusion is retained only for provenance, not as current audit truth.
- The authoritative current audit identity for this V2.4 boundary is `DRCOM20-001` extended/revalidated to the selected candidate scope by EV-122.
- No XSD is modified.
