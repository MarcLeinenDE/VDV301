#!/usr/bin/env python3
"""Write CIS legacy-revalidation closure records after EV-125 has passed."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = os.environ["EV_RUN_ID"]
HEAD = os.environ["EV_HEAD"]
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
REVALIDATION = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_CIS_2026-09-03.md"
CORRECTION = "docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CIS_V11_PROVENANCE_2026-09-03.md"
HANDOFF = "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_CIS_REVALIDATION_2026-09-03.md"
EVIDENCE = "audit_registry/revalidation_evidence_ev125_cis_block_2026-09-03.json"
STATES = {
    "CIS-001": "unresolved",
    "CIS-002": "contextual_not_defect",
    "CIS-003": "executable_confirmed",
    "CIS-004": "executable_confirmed",
    "CIS-005": "executable_confirmed",
}
PDF_PINS = [
    ("CIS_V1.1", "89080a41da387270ecac5b228df6aa4903ccb123a0d37e9e73cd98396786931b", 985025, "1d2098ad9eecc462ed03e2a9646e2280199918e03eafd56f56aef84ea39cd1bb", 27),
    ("CIS_V2.0", "0e3041d6354c040d532767391947476238a8afcab7a8df4276da1e7cad0cfa2b", 878454, "7fc6654639ea136951df666239d3f30650461588de5aef67ebba453bd4acf6fe", 26),
    ("CIS_V2.2", "3fcd258cf21c60527c48bd438c4d09a2a139c7093c0ff6984185e7c81efb8802", 831079, "4dbc9ed36d19c3dd446b3d8cc42ac2baf01edbaa239cd7fa173cf61732617997", 26),
    ("CIS_V2.3", "3f427901177e372daf0fee974648240e38da267c30030a909ccb712686f71ab1", 1035224, "219936ed35725ddd45a4c2225780eb95095edb85e06648d13cdf264965fe5e23", 26),
]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def dump(path: str, value) -> None:
    (ROOT / path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_docs() -> None:
    evidence = {
        "evidence_id": "EV-125",
        "date": "2026-09-03",
        "purpose": "CIS-001..CIS-005 legacy revalidation closure",
        "run_id": RUN,
        "head_tested": HEAD,
        "result": "PASS",
        "historical_v11": {
            "upstream_commit": "0a5228a768c7d710c40f5f99fbdce2e544d19883",
            "release_tag": None,
            "authority": "historical_working_snapshot_not_release_authority",
            "cis_blob": "5957e27f128a191c794b0c8081b531a07126784a",
            "common_blob": "bdf839813b4b19dd000a32a684ce985878adaca9",
            "enumerations_blob": "5a9957a6931be2e4460665f8a52c76765fbfbcde",
        },
        "official_routes": {
            "V2.0": {"cis_blob": "fa8f0a51ad5f612660c9532c8557ad1ca473a908", "common_blob": "8608e3dcd665c197c34da7f6ec6af5a3758da164", "enumerations_blob": "27e3c183b00381d959622d13c10543123af8eef6"},
            "V2.2": {"cis_blob": "ddc70ed9d6238f1377be1d7728ff46b36a22ee1e", "common_blob": "468fee6d177e7185dbcd5d3f90cfb114e29e01ae", "enumerations_blob": "2a23b512379b18e8f122ac1272cef8229fb86283"},
            "V2.3": {"cis_blob": "bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e", "common_blob": "0d8926c4063c12de9a5e68b6f0addaab35a55dc1", "enumerations_blob": "2a23b512379b18e8f122ac1272cef8229fb86283"},
        },
        "finding_states": STATES,
        "pdf_pin_run_id": "33736316368",
        "pdf_pin_job_id": "100587592810",
        "pdf_pin_artifact_id": "9885887536",
        "pdf_pin_artifact_digest": "sha256:8a514d33d5c9f23408a14dd1302366845b319027e280773407a2188c27b23cfe",
        "rendered_pages": 105,
        "xsd_mutation": False,
    }
    dump(EVIDENCE, evidence)

    (ROOT / REVALIDATION).write_text(
        f"""# CIS legacy finding revalidation — 2026-09-03

Status: **closed under the current Finding Evidence Gate** for `CIS-001..CIS-005`.

Evidence: `EV-125` (Actions run `{RUN}`) plus official byte-pinned CIS PDFs from run `33736316368`, job `100587592810`, artifact `9885887536`. The four PDFs total **105 rendered pages**; source and page hashes were verified and the finding-bearing pages were visually inspected.

| Finding | Terminal state | Revalidated conclusion |
|---|---|---|
| CIS-001 | `unresolved` | The old claim “no CIS V1.1 XSD found” is corrected. Official Git history contains an untagged V1.1 working family at `0a5228a…`, but there is no `VDV-301-1.1` release tag and the working CIS V1.1 schema lacks published-PDF fields `SpeakerActive` and `StopInformationActive`. It therefore cannot be promoted to a strict published V1.1 release authority. |
| CIS-002 | `contextual_not_defect` | Subscribe/Unsubscribe are generic Common structures; their absence from the CIS-specific operation group is intentional shared modelling, not a CIS schema defect. |
| CIS-003 | `executable_confirmed` | PDF detail label `GetCurrentConnectionResponse` differs from executable XSD root `CustomerInformationService.GetCurrentConnectionInformationResponse`; EV-125 proves correct root valid / PDF short root invalid on V2.0, V2.2 and V2.3. |
| CIS-004 | `executable_confirmed` | PDF detail label `RetrievePartialStopRequest` differs from executable XSD root `CustomerInformationService.RetrievePartialStopSequenceRequest`; EV-125 proves the root boundary on all three official routes. |
| CIS-005 | `executable_confirmed` | PDF internally types `MyOwnVehicleMode` inconsistently (`NetexMode` vs `PtModesEnumeration`). V2.2/V2.3 XSD use `NetexMode`; EV-125 proves structured NetexMode valid and scalar text invalid. |

## Disproof / context checks

- V1.1 was searched in official Git history rather than inferred from release tags.
- The strongest alternative for CIS-001 — treating the untagged working files as publication authority — fails because no V1.1 release tag exists and the working XSD is materially behind the published PDF.
- CIS-002 was tested against Common generic subscribe/unsubscribe definitions and CIS operation-group scope.
- CIS-003/004 were checked as global-root naming questions, not merely table wording.
- CIS-005 was checked against the shared `VehicleInformationGroup`, not an isolated PDF row.

No XSD correction or mutation is authorized by this revalidation.
""",
        encoding="utf-8",
    )

    (ROOT / CORRECTION).write_text(
        """# Audit correction delta — CIS V1.1 provenance — 2026-09-03

This overlay corrects earlier first-pass statements that no CIS V1.1 XSD had been confirmed.

Fresh provenance establishes an official-upstream **working** V1.1 family at commit `0a5228a768c7d710c40f5f99fbdce2e544d19883` immediately before the V2.0 release lineage:

- CIS: `5957e27f128a191c794b0c8081b531a07126784a`
- Common: `bdf839813b4b19dd000a32a684ce985878adaca9`
- Enumerations: `5a9957a6931be2e4460665f8a52c76765fbfbcde`

The official tag set contains no `VDV-301-1.1` release tag. The working CIS V1.1 schema also lacks `SpeakerActive` and `StopInformationActive`, both visible in the published V1.1 PDF and executable in V2.0. Therefore the historical files prove development provenance but **do not establish a strict published V1.1 release validation authority**.

Historical reports are preserved; this correction overlay supersedes only their “V1.1 XSD not found” provenance conclusion. No XSD is imported or modified by this correction.
""",
        encoding="utf-8",
    )

    (ROOT / HANDOFF).write_text(
        f"""# Audit handoff delta — CIS revalidation — 2026-09-03

CIS revalidation is complete under the current Evidence Gate.

- terminal findings: `CIS-001..CIS-005`
- EV: `EV-125`, run `{RUN}`
- states: 1 unresolved provenance/routing finding, 1 contextual-not-defect, 3 executable-confirmed documentation/XSD boundaries
- four official CIS PDF sources byte-pinned by run `33736316368`; 105 rendered pages total
- V1.1 historical working files are provenance evidence only, not release authority
- no XSD changes
- next legacy revalidation block: `DISC`
""",
        encoding="utf-8",
    )


def update_revalidation_registry() -> None:
    path = "audit_registry/finding_revalidation_registry_v0.1.json"
    registry = load(path)
    entries = {entry["finding_id"]: entry for entry in registry["inventory"]["entries"]}
    for finding_id, state in STATES.items():
        assert entries[finding_id]["revalidation_state"] == "pending", entries[finding_id]
        entries[finding_id]["revalidation_state"] = state
        entries[finding_id]["terminal_state_source"] = REVALIDATION
    dump(path, registry)


def update_pdf_pins() -> int:
    path = "audit_registry/pdf_source_pins_v0.1.json"
    registry = load(path)
    existing = {entry["source_id"]: entry for entry in registry["sources"]}
    for source_id, sha, size, fulltext_sha, pages in PDF_PINS:
        if source_id in existing:
            assert existing[source_id]["expected_sha256"] == sha
            assert existing[source_id]["expected_size_bytes"] == size
            continue
        registry["sources"].append(
            {
                "source_id": source_id,
                "expected_sha256": sha,
                "expected_size_bytes": size,
                "pinned_at_utc": "2026-09-03T08:59:53Z",
                "deep_read_source_ready": True,
                "evidence_run_id": "33736316368",
                "evidence_job_id": "100587592810",
                "evidence_artifact_id": "9885887536",
                "fulltext_sha256": fulltext_sha,
                "rendered_pages": pages,
                "pin_note": "CIS legacy revalidation pin; full render and per-page hash manifest verified",
            }
        )
    assert len({entry["source_id"] for entry in registry["sources"]}) == len(registry["sources"])
    dump(path, registry)
    return len(registry["sources"])


def update_current_state(pin_count: int) -> None:
    path = "00_START_HERE/CURRENT_STATE.json"
    state = load(path)
    audit = state["audit"]
    audit["pdf_sources_byte_pinned"] = pin_count
    for source_id, *_ in PDF_PINS:
        if source_id not in audit["pinned_active_sources"]:
            audit["pinned_active_sources"].append(source_id)
    audit["finding_revalidation_next_block"] = "DISC"
    audit["finding_revalidation_completed_findings"] = 47
    audit["finding_revalidation_pending_findings"] = 145
    audit["finding_revalidation_current_block"] = "CIS"
    audit["finding_revalidation_latest_completed_block"] = "CIS"
    audit["finding_revalidation_latest_terminal_state_source"] = REVALIDATION
    audit["latest_executable_evidence_id"] = "EV-125"
    audit["latest_executable_evidence_run_id"] = RUN
    audit["latest_executable_evidence_run"] = RUN
    audit["latest_audit_correction"] = CORRECTION
    audit["cis_revalidation"] = {
        "status": "complete",
        "completed_at": NOW,
        "evidence_id": "EV-125",
        "run_id": RUN,
        "terminal_states": STATES,
        "pdf_pin_run_id": "33736316368",
        "pdf_pin_artifact_id": "9885887536",
        "rendered_pages": 105,
        "next_block": "DISC",
        "xsd_mutation": False,
    }
    completed = state.get("evidence", {}).get("xsd_ev_completed")
    if isinstance(completed, list) and completed and all(isinstance(item, str) for item in completed):
        if "EV-125" not in completed:
            completed.append("EV-125")
    dump(path, state)


def append_correction_pointers() -> None:
    marker = (
        "\n## Post-audit correction — 2026-09-03\n\n"
        "The earlier V1.1 provenance statement is superseded by "
        "`AUDIT_CORRECTION_DELTA_CIS_V11_PROVENANCE_2026-09-03.md`. "
        "A historical untagged V1.1 working XSD family exists, but it is not a V1.1 "
        "release-tag authority and does not match all published V1.1 PDF fields. "
        "See also `FINDING_REVALIDATION_CIS_2026-09-03.md` / `EV-125`.\n"
    )
    for relative in (
        "docs/pdf_xsd_semantic_audit/05c_cis_v1_1_mapping.md",
        "docs/pdf_xsd_semantic_audit/05g_cis_findings_and_v2_0_v2_2_v2_3_closure.md",
        "docs/pdf_xsd_semantic_audit/CIS_HISTORICAL_XSD_INTEGRATION_DECISION.md",
    ):
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        if "## Post-audit correction — 2026-09-03" not in text:
            path.write_text(text.rstrip() + marker + "\n", encoding="utf-8")


def main() -> int:
    write_docs()
    update_revalidation_registry()
    pin_count = update_pdf_pins()
    assert pin_count == 36, pin_count
    update_current_state(pin_count)
    append_correction_pointers()
    print("PASSED: CIS revalidation closure records written; no XSD mutation requested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
