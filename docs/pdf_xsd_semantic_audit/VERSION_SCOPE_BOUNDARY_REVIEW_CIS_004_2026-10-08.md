# Version-scope boundary review — CIS-004 — 2026-10-08

Status: **verified / confirmed PDF defect / scope unchanged**.

## Finding
CIS V2.0, V2.2 and V2.3 PDF request-detail Table 18 calls the global XML request `CustomerInformationService.RetrievePartialStopRequest`. In contrast, each version's own Table 1 names `RetrievePartialStopSequence`, and each exact official release XSD declares `CustomerInformationService.RetrievePartialStopSequenceRequest` as the global request element. The short name is no supported alias.

## Lower boundary
The official CIS V1.0 XSD does not yet declare either V2.x global request root. CIS V1.1 is not a selectable strict official profile (CIS-001 authority gap). The **first affected proven publication** is CIS V2.0: p.20 Table 18 short name, p.12 Table 1 full name, tagged XSD `fa8f0a51ad5f612660c9532c8557ad1ca473a908` full global root.

## Continuity
- The global `VDV-301-2.1` release reuses CIS V2.0 XSD, and is not a distinct CIS V2.1 service edition.
- CIS V2.2 PDF p.21 Table 18 repeats the short name; official XSD blob `ddc70ed9d6238f1377be1d7728ff46b36a22ee1e` requires the full name.
- CIS V2.3 PDF p.21 Table 18 repeats the short name; official XSD blob `bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e` requires the full name.

EV-125 run `33744039627` independently confirms valid full XML root versus invalid PDF short name on every in-scope official profile. Exact visible PDF body evidence: `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_CIS_004_2026-10-06.md`.

## Upper boundary
Candidate/integration CIS V2.4 XSD retains the full name, but an official CIS V2.4 PDF documenting the same error is not established. The official-PDF finding cannot be widened on an unsupported assumption.

## SDK
Keep the affected semantic/runtime scope **CIS V2.0 / V2.2 / V2.3** only. The exact selected XSD remains authoritative: using `RetrievePartialStopRequest` as global XML root is **INVALID** and merits explanatory advisory, never normalization or a compatibility alias.
