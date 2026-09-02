#!/usr/bin/env python3
"""Close COMMON V2.1 after frozen fresh read and successful EV-119."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
REG_DELTA = ROOT / "audit_registry/deep_read_registry_delta_common_v21_2026-09-02.json"
FIND_DELTA = ROOT / "audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json"
REPORT = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.1.md"
HANDOFF = ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V21_DEEP_READ_2026-09-02.md"

FREEZE = "11c16e618e1d86504ba4517f9d9891429d40d2ce"
EV_RUN = "33609779315"
EV_JOB = "100181942929"
EV_HEAD = "0e5d0213cdbbac73ed8991153893faaf85db15e9"
COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
ENUMS_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
PDF_SHA = "a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32"
FULLTEXT_SHA = "5dce4c8ecc770574bdce8d5961fefbc01f88b1547e3957855013d9b077fc24b0"

MAPPING = {
    "FR-COM21-OBS-001": ["DRCOM20-001"],
    "FR-COM21-OBS-002": ["CE-013"],
    "FR-COM21-OBS-003": ["CE-026"],
    "FR-COM21-OBS-004": ["DRCOM10-002"],
    "FR-COM21-OBS-005": ["CE-014", "CE-012", "CE-018", "DRCOM10-003"],
    "FR-COM21-OBS-006": ["CE-015"],
    "FR-COM21-OBS-007": ["CE-016"],
    "FR-COM21-OBS-008": ["DRCOM10-004"],
    "FR-COM21-OBS-009": ["CE-021"],
    "FR-COM21-OBS-010": ["CE-022"],
    "FR-COM21-OBS-011": ["CE-019"],
    "FR-COM21-OBS-012": ["DRCOM10-005"],
    "FR-COM21-OBS-013": ["DRCOM21-001"],
    "FR-COM21-OBS-014": ["CE-025"],
    "FR-COM21-OBS-015": ["CE-005"],
    "FR-COM21-OBS-016": ["CE-017"],
    "FR-COM21-OBS-017": ["CE-015"],
    "FR-COM21-OBS-018": ["DRCOM10-006", "CE-007"],
    "FR-COM21-OBS-019": ["DRCOM10-007"],
    "FR-COM21-OBS-020": ["DRCOM10-007"],
}

FINDINGS = {
    "CE-005": "V2.1_scope_visible_table_and_version_history_plus_executable_0to1_boundary_EV-119",
    "CE-007": "V2.1_scope_executable_GNSS_TicketValidation_VehicleMode_enum_lexeme_boundaries_EV-119",
    "CE-012": "V2.1_scope_executable_empty_DeviceSpecificationWithStateList_EV-119",
    "CE-013": "V2.1_scope_executable_optional_choice_and_SpecificPoint_name_boundary_EV-119",
    "CE-014": "V2.1_scope_executable_empty_DataVersionList_EV-119",
    "CE-015": "V2.1_scope_visible_FareZoneInformation_and_ZoneType_case_boundaries_plus_EV-119",
    "CE-016": "V2.1_scope_executable_GlobalCardStausID_boundary_EV-119",
    "CE-017": "V2.1_scope_executable_TSPPoint_Description_vs_Desciption_EV-119",
    "CE-018": "V2.1_scope_visible_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-119",
    "CE-019": "V2.1_scope_visible_type_reference_plus_exact_ServiceIdentificationWithStateStructure_EV-119",
    "CE-021": "V2.1_scope_executable_MessageBody_vs_Message_boundary_EV-119",
    "CE-022": "V2.1_scope_executable_outer_ServiceName_vs_Service_boundary_EV-119",
    "CE-025": "V2.1_scope_executable_Reply-Path_vs_ReplyPath_boundaries_EV-119",
    "CE-026": "V2.1_scope_executable_BeaconPoint_Description_vs_Desciption_EV-119",
    "DRCOM10-002": "V2.1_scope_executable_DataAcceptedResponse_choice_boundary_EV-119",
    "DRCOM10-003": "V2.1_scope_executable_empty_ServiceSpecificationWithStateList_EV-119",
    "DRCOM10-004": "V2.1_scope_executable_JourneyStop_Announcement_FareZone_0to1_EV-119",
    "DRCOM10-005": "V2.1_scope_child_name_facet_persists_type_facet_aligned_exact_XSD_EV-119",
    "DRCOM10-006": "V2.1_scope_executable_DoorCountingObjectClass_lexemes_EV-119",
    "DRCOM10-007": "V2.1_scope_context_verified_GNSS_identifier_and_grouped_editorial_residue",
    "DRCOM20-001": "V2.1_scope_executable_pdf_wrapper_reference_vs_xsd_primitive_instance_shape_EV-119",
    "DRCOM21-001": "executable_confirmed_EV-119_StopInformationRequest_StopName_pdf_0to1_vs_xsd_0toStar",
}


def dump(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    audit = state["audit"]
    assert audit["deep_read_current_document_id"] == "COMMON_V2.1"
    assert audit["deep_read_textual_fresh_read_completed"] == 33
    assert audit["deep_read_needs_visual_review"] == 33
    assert audit["deep_read_in_progress"] == 1

    delta = json.loads(REG_DELTA.read_text(encoding="utf-8"))
    doc = delta["document_updates"]["COMMON_V2.1"]
    assert doc["fresh_read_freeze"]["status"] == "frozen"
    assert doc["fresh_read_freeze"]["observation_count"] == 20
    assert doc["authority_status"]["common_blob"] == COMMON_BLOB
    assert doc["authority_status"]["enumerations_blob"] == ENUMS_BLOB
    assert doc["source_pin"]["sha256"] == PDF_SHA
    assert doc["render_read_evidence"]["fulltext_sha256"] == FULLTEXT_SHA

    report = REPORT.read_text(encoding="utf-8")
    assert "Twenty independent observations are frozen" in report
    assert "## Historical reconciliation and closure" not in report

    findings_delta = {
        "delta_version": "0.1",
        "date": "2026-09-02",
        "document_id": "COMMON_V2.1",
        "fresh_read_freeze": FREEZE,
        "source_evidence": {
            "pdf_sha256": PDF_SHA,
            "size_bytes": 1274051,
            "pin_render_read_run": "33608210402",
            "artifact_id": "9837875704",
            "artifact_zip_sha256": "f76b9cbc078edbe4646bf8d8754d486e6046bda460f885a7d52889c78a29ee34",
            "page_count": 48,
            "fulltext_sha256": FULLTEXT_SHA,
        },
        "exact_xsd_authority": {
            "official_tag": "VDV-301-2.1",
            "common_blob": COMMON_BLOB,
            "enumerations_blob": ENUMS_BLOB,
            "branch_bytes_match_official_tag": True,
        },
        "executable_evidence": {
            "evidence_id": "EV-119",
            "checker": "tools/validate_common_v21_ev119.py",
            "run": EV_RUN,
            "job": EV_JOB,
            "head_tested": EV_HEAD,
            "result": "PASS",
            "authority": "exact_official_VDV-301-2.1_Common_Enumerations_family",
        },
        "procedural_independence_note": (
            "CURRENT_STATE historical COMMON V2.0 metadata became visible after the independent V2.1 observation list "
            "had been completed but before the formal freeze commit. The frozen observation list was not changed from that metadata."
        ),
        "observation_to_finding_mapping": MAPPING,
        "revalidated_or_scope_extended_findings": {k: v for k, v in FINDINGS.items() if k != "DRCOM21-001"},
        "new_unique_findings": {
            "DRCOM21-001": {
                "state": "executable_confirmed_EV-119",
                "classification": "cardinality_xsd_more_permissive_than_pdf",
                "summary": (
                    "COMMON V2.1 PDF StopInformationRequest documents StopName 0:1, while exact official V2.1 XSD "
                    "declares StopName minOccurs=0 maxOccurs=unbounded. EV-119 validates an instance containing two StopName entries."
                ),
                "executable_effect": True,
            }
        },
        "explicit_non_extension": {
            "CE-020": "not scope-extended: CE-020 identity includes the V2.3 PR #30 same-path authority collision; DRCOM20-001 covers the primitive-vs-wrapper PDF/XSD mismatch for V2.1",
            "DRCOM10-001": "not scope-extended: V1.x revision-vs-unchanged-V1.0-XSD drift is not the V2.1 authority situation",
            "CE-011": "not scope-extended: the repeated Connection TransportMode/ConnectionMode V2.3 issue was not present in the V2.1 fresh observation set",
            "CE-023": "not scope-extended: duplicate/corrupt second NetexMode table remains V2.3-specific in the checked chain",
            "CE-024": "not scope-extended: V2.1 SubscribeResponse/UnsubscribeResponse choice/cardinality was independently found aligned",
        },
        "active_falsification": [
            "VDV -1:1 notation is treated as XML choice, never negative cardinality",
            "PointType, SubscribeResponse and UnsubscribeResponse choices align in V2.1",
            "Connection and StopInformation checked multiplicities align and are not carried forward as false positives",
            "PointSequence minimum two and ServiceInformationList/ServiceStartList one-or-more minimums align",
            "V2.1 service-name additions align between PDF and exact Enumerations V2.1",
            "enumeration ordering differences are ignored",
            "no XSD change is proposed or performed",
        ],
        "next_natural_document_id": "COMMON_V2.2",
    }
    dump(FIND_DELTA, findings_delta)

    reconciliation = """

## Historical reconciliation and closure — 2026-09-02

Historical COMMON material was deliberately mapped only after the formal fresh-read freeze commit `11c16e618e1d86504ba4517f9d9891429d40d2ce`.

The earlier procedural note remains part of the audit record: `CURRENT_STATE.json` exposed historical COMMON V2.0 metadata after the independent V2.1 observation list had already been completed but before the formal freeze commit. The frozen twenty-observation list was not altered from that metadata.

### Deduplication / scope extension

Nineteen of the twenty fresh observation groups map to existing Common finding identities. `FR-COM21-OBS-018` intentionally maps to two existing identities because the historic registry separates `DoorCountingObjectClassEnumeration` (`DRCOM10-006`) from the other case-sensitive enumeration lexeme boundaries (`CE-007`). `FR-COM21-OBS-005` intentionally maps to the four existing list-minimum identities it groups.

The V2.1 mapping is recorded machine-readably in `audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json`.

The only new V2.1-specific identity required is:

```text
DRCOM21-001: StopInformationRequest.StopName PDF 0:1 vs exact V2.1 XSD 0:*
```

`CE-020` is not broadened: that identity includes the V2.3 PR #30 same-path authority collision. The V2.1 `InternationalTextType` primitive-vs-wrapper boundary therefore scope-extends `DRCOM20-001`, which was created specifically to isolate that PDF/XSD shape mismatch from the later candidate-authority collision.

### Executable evidence — EV-119

EV-119 run `33609779315` / job `100181942929` PASS on head `0e5d0213cdbbac73ed8991153893faaf85db15e9` against exact official V2.1 blobs:

```text
IBIS-IP_common_V2.1.xsd        05977c9f86c7c9dd0b48f36a4a4e9be32e94659e
IBIS-IP_Enumerations_V2.1.xsd  311464690ad60749ed8d326217787e4b8ed0b718
```

The checker `tools/validate_common_v21_ev119.py` verifies the exact blob identities, static declarations, and positive/negative XML behavior. Among the executable boundaries it confirms:

- flat `InternationalTextType` validates while PDF wrapper-shaped `Value`/`Language` does not;
- optional `AdditionalAnnouncement` choice and XSD `SpecificPoint` behavior;
- exclusive `DataAcceptedResponse` choice;
- empty containers validate for the four PDF `1:*` list structures;
- PDF/XSD element-name and case boundaries for FareZone, GlobalCardStatus, Message, Service, ReplyPath, BeaconPoint, TSPPoint and ZoneType;
- a second `Announcement` or `FareZone` in `JourneyStopInformation` is rejected;
- a second `AdditionalTextMessage` in `TripInformation` is rejected even though the PDF table and its own V2.0 correction history say repeatable;
- two `StopName` entries in `StopInformationRequest` are accepted by the exact XSD, proving new `DRCOM21-001`;
- the exact XSD enumeration lexemes validate while the mismatching PDF-side lexemes fail.

### Closure

COMMON V2.1 is complete for Deep Read Pass 2 as `needs_visual_review`, not `exhaustive_read`: the complete extracted text was read across all 48 pinned pages and all material finding pages received targeted visible review, but this was not a pixel-by-pixel exhaustive visual pass.

No XSD was changed. Exact `VDV-301-2.1` Common/Enumerations remains executable authority. Next natural Deep Read unit: `COMMON_V2.2`.
"""
    REPORT.write_text(report.rstrip() + reconciliation + "\n", encoding="utf-8")

    doc["state"] = "historical_reconciliation_complete_executable_evidence_pass"
    doc["fresh_read_freeze"]["historical_reconciliation_started"] = True
    doc["fresh_read_freeze"]["historical_reconciliation_completed"] = True
    doc["fresh_read_freeze"]["executable_evidence_status"] = "EV-119_PASS"
    doc["executable_evidence"] = findings_delta["executable_evidence"]
    doc["historical_reconciliation"] = {
        "status": "complete",
        "findings_delta": "audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json",
        "revalidated_or_scope_extended_count": len(findings_delta["revalidated_or_scope_extended_findings"]),
        "new_unique_findings": ["DRCOM21-001"],
        "next_natural_document_id": "COMMON_V2.2",
    }
    dump(REG_DELTA, delta)

    audit["deep_read_needs_visual_review"] = 34
    audit["deep_read_textual_fresh_read_completed"] = 34
    audit["deep_read_in_progress"] = 0
    audit["deep_read_current_document_id"] = "COMMON_V2.1"
    audit["deep_read_previous_document_id"] = "COMMON_V2.1"
    audit["next_natural_deep_read_document_id"] = "COMMON_V2.2"
    audit["latest_deep_read_finding"] = "DRCOM21-001"
    audit["latest_deep_read_revalidation"] = "DRCOM21-001_V2.1_scope_executable_StopInformationRequest_StopName_0toStar_EV-119"
    audit["latest_common_finding"] = "DRCOM21-001"
    audit["latest_deep_read_findings_delta"] = "audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json"
    audit["common_v2_1_deep_read_report"] = "docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.1.md"
    audit["common_v2_1_handoff"] = "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V21_DEEP_READ_2026-09-02.md"
    audit["common_v2_1_render_read"]["fresh_read_freeze"] = f"frozen_commit_{FREEZE}"
    audit["common_v2_1_fresh_read_status"] = "historical_reconciliation_complete"
    audit["common_v2_1_findings"] = FINDINGS
    audit["common_v2_1_executable_evidence"] = {
        "evidence_id": "EV-119",
        "run": EV_RUN,
        "job": EV_JOB,
        "checker": "tools/validate_common_v21_ev119.py",
        "result": "PASS",
        "Common_V2.1_blob": COMMON_BLOB,
        "Enumerations_V2.1_blob": ENUMS_BLOB,
    }
    state["evidence"]["latest_targeted_xsd_evidence_run"] = EV_RUN
    state["evidence"]["latest_targeted_xsd_evidence"] = "EV-119"
    state["evidence"]["common_v2_1_executable_evidence"] = f"EV-119 / {EV_RUN}"
    state["next_actions"] = [
        "Start COMMON V2.2 Deep Read from the official source; byte-pin/render the exact source and establish exact Common/Enumerations authority before historical reconciliation.",
        "Complete independent COMMON V2.2 Fresh Read and targeted visible review before reopening historical Common findings for that document.",
        "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze.",
    ]
    dump(STATE, state)

    HANDOFF.write_text(f"""# Audit handoff delta — COMMON V2.1 Deep Read — 2026-09-02

## Completed block

`COMMON_V2.1` is closed for Deep Read Pass 2 as `needs_visual_review` with historical reconciliation complete.

- Fresh-read freeze: `{FREEZE}`
- Official PDF SHA-256: `{PDF_SHA}`; 1,274,051 bytes; 48 pages.
- Recovery pin/render/read run: `33608210402`; retained prior evidence run: `33393002497`.
- Exact authority: official `VDV-301-2.1`.
- Common blob: `{COMMON_BLOB}`.
- Enumerations blob: `{ENUMS_BLOB}`.
- EV-119: PASS, run `{EV_RUN}`, job `{EV_JOB}`, checker `tools/validate_common_v21_ev119.py`.
- New unique finding: `DRCOM21-001` — `StopInformationRequest.StopName` PDF `0:1` vs exact XSD `0:*`; two StopName entries validate in EV-119.
- Remaining fresh observations deduplicate/scope-extend existing Common findings; exact mapping is in `audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json`.

## Independence/provenance note

The independent twenty-observation V2.1 list was completed before historical Common findings were intentionally reopened. While preparing the freeze state, `CURRENT_STATE.json` exposed historical COMMON V2.0 finding metadata after the list was already complete but before the formal freeze commit. The list was not changed using that metadata; the exposure is recorded in the freeze report and registry delta.

## Guardrails

- No XSD was changed.
- Exact selected XSD remains executable authority.
- `-1:1` is VDV choice notation, not negative cardinality.
- Do not latest-wins substitute a later Common/Enumerations family.
- Historical findings require current Evidence-Gate revalidation; EV-119 is the V2.1 executable evidence.

## Next natural unit

`COMMON_V2.2`.

Start from source/authority evidence, not old chat history. Byte-pin and render the official COMMON V2.2 PDF, establish the exact authority route, complete an independent fresh read and freeze it before historical Common reconciliation.
""", encoding="utf-8")

    # Final local semantic assertions before the workflow stages anything.
    state2 = json.loads(STATE.read_text(encoding="utf-8"))
    assert state2["audit"]["deep_read_textual_fresh_read_completed"] == 34
    assert state2["audit"]["deep_read_needs_visual_review"] == 34
    assert state2["audit"]["deep_read_in_progress"] == 0
    assert state2["audit"]["next_natural_deep_read_document_id"] == "COMMON_V2.2"
    assert state2["audit"]["latest_common_finding"] == "DRCOM21-001"
    assert json.loads(FIND_DELTA.read_text(encoding="utf-8"))["executable_evidence"]["result"] == "PASS"
    assert json.loads(REG_DELTA.read_text(encoding="utf-8"))["document_updates"]["COMMON_V2.1"]["state"] == "historical_reconciliation_complete_executable_evidence_pass"
    print("COMMON_V21_CLOSURE_STATE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
