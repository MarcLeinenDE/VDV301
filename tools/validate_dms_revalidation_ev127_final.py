#!/usr/bin/env python3
"""EV-127 final fail-closed DMS revalidation gate.

Text/XSD assertions are executable. Layout-dependent DMS-005/DMS-006 evidence
is bound to the independently rendered, byte-pinned visual review record in
`audit_registry/dms_visual_revalidation_evidence_2026-09-03.json`.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

import validate_dms_revalidation_ev127 as base

VISUAL_EVIDENCE = Path("audit_registry/dms_visual_revalidation_evidence_2026-09-03.json")
EXPECTED_VISUAL_RUN = "33758274931"
EXPECTED_VISUAL_ARTIFACT = "9894357560"
EXPECTED_VISUAL_DIGEST = "sha256:6cd210a39445cbeecff14b918d2f2e9a424a82f3f43d8a0e41cb7dfd8b7df892"


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"FAIL {message}")
        raise SystemExit(1)


def visual_page(record: dict, source_id: str, page: int) -> dict:
    matches = [
        item for item in record.get("reviewed_pages", [])
        if item.get("source_id") == source_id and item.get("page") == page
    ]
    require(len(matches) == 1, f"visual evidence {source_id} page {page}: expected one record, found {len(matches)}")
    return matches[0]


def has_observation(page_record: dict, phrase: str) -> bool:
    return any(phrase in str(item) for item in page_record.get("observations", []))


def main() -> int:
    require(shutil.which("pdftotext") is not None, "EV-127 final requires pdftotext")
    require(VISUAL_EVIDENCE.is_file(), f"missing {VISUAL_EVIDENCE}")
    visual = json.loads(VISUAL_EVIDENCE.read_text(encoding="utf-8"))
    require(visual.get("render_run_id") == EXPECTED_VISUAL_RUN, "visual render run changed")
    require(visual.get("render_artifact_id") == EXPECTED_VISUAL_ARTIFACT, "visual artifact id changed")
    require(visual.get("render_artifact_digest") == EXPECTED_VISUAL_DIGEST, "visual artifact digest changed")
    require(visual.get("visual_review_status") == "completed", "visual review not completed")
    require(visual.get("frozen_inventory_mutated") is False, "visual record claims frozen inventory mutation")
    require(visual.get("xsd_mutated") is False, "visual record claims XSD mutation")

    roots = {version: base.parse_xsd(path) for version, path in base.XSD_PATHS.items()}

    with tempfile.TemporaryDirectory(prefix="vdv301-ev127-final-") as tmp_name:
        pdfs = base.fetch_pinned_pdfs(Path(tmp_name))

        # DMS-001: generic Common subscription structures are intentional;
        # the surviving V2.0 finding is the incomplete DMS wrapper/group model.
        v20_group = base.group_names(roots["v20"])
        v20_globals = base.global_names(roots["v20"])
        v21_group = base.group_names(roots["v21"])
        v21_globals = base.global_names(roots["v21"])
        expected_v20_group = [
            "DeviceManagementService.GetDeviceInformationResponse",
            "DeviceManagementService.GetDeviceConfigurationResponse",
            "DeviceManagementService.SetDeviceConfigurationRequest",
            "DeviceManagementService.GetDeviceStatusResponse",
            "DeviceManagementService.GetDeviceErrorMessagesResponse",
            "DeviceManagementService.GetServiceInformationResponse",
            "DeviceManagementService.GetServiceStatusResponse",
            "DeviceManagementService.StartServiceRequest",
            "DeviceManagementService.RestartServiceRequest",
            "DeviceManagementService.StopServiceRequest",
        ]
        require(v20_group == expected_v20_group, f"DMS-001 V2.0 service group changed: {v20_group!r}")
        for name in (
            "DeviceManagementService.SetDeviceConfigurationResponse",
            "DeviceManagementService.RestartDeviceResponse",
        ):
            require(name in v20_globals and name not in v20_group, f"DMS-001 V2.0 global/group asymmetry missing for {name}")
        for name in (
            "DeviceManagementService.ActivateDeviceResponse",
            "DeviceManagementService.DeactivateDeviceResponse",
        ):
            require(name not in v20_globals, f"DMS-001 unexpected V2.0 wrapper {name}")
            require(name in v21_globals and name in v21_group, f"DMS-001 V2.1 expansion missing {name}")
        for name in (
            "DeviceManagementService.SetDeviceConfigurationResponse",
            "DeviceManagementService.RestartDeviceResponse",
            "DeviceManagementService.SubscribeDeviceInformationRequest",
            "DeviceManagementService.SubscribeDeviceInformationResponse",
        ):
            require(name in v21_group, f"DMS-001 V2.1 explicit group entry missing {name}")
        v20_ops = base.page_text(pdfs["VDV301-2_BASE_V2.0"], 90) + " " + base.page_text(pdfs["VDV301-2_BASE_V2.0"], 91)
        for phrase in (
            "SubscribeDeviceInformation", "SubscribeRequestStructure", "SubscribeResponseStructure",
            "RestartDevice", "DeactivateDevice", "ActivateDevice", "DataAcceptedResponseStructure",
        ):
            require(phrase in v20_ops, f"DMS-001 V2.0 operation evidence missing {phrase}")
        print("OK DMS-001 refined historical DMS wrapper/group asymmetry confirmed")

        # DMS-002: documentation-only broken cross references.
        broken = "Fehler! Verweisquelle konnte nicht gefunden werden."
        count20 = base.full_text(pdfs["VDV301-2_BASE_V2.0"]).count(broken)
        count21 = base.full_text(pdfs["VDV301-2_BASE_V2.1"]).count(broken)
        require(count20 >= 2, f"DMS-002 expected repeated V2.0 broken references, found {count20}")
        require(count21 == 0, f"DMS-002 V2.1 still contains broken-reference marker count={count21}")
        p76 = visual_page(visual, "VDV301-2_BASE_V2.0", 76)
        require(p76.get("png_sha256") == "29e162540456fd549fc5f7e9856909c2f97bc8271211f66182609af4477c4d0e", "DMS-002 visual PNG hash changed")
        require(has_observation(p76, broken), "DMS-002 visual observation missing")
        print(f"OK DMS-002 repeated V2.0 broken references confirmed count={count20}")

        # DMS-003: 10:* through V2.2, later V2.4 correction to 0:*.
        for version in ("v20", "v21", "v22"):
            el = base.seq_element(roots[version], "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure", "ErrorMessage")
            require(base.occurs(el) == ("10", "unbounded"), f"DMS-003 {version} cardinality changed: {base.occurs(el)}")
        el24 = base.seq_element(roots["v24"], "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure", "ErrorMessage")
        require(base.occurs(el24) == ("0", "unbounded"), f"DMS-003 V2.4 candidate cardinality changed: {base.occurs(el24)}")
        require("ErrorMessage 10:*" in base.page_text(pdfs["DMS_V2.2"], 20), "DMS-003 V2.2 PDF 10:* missing")
        require("ErrorMessage 0:*" in base.page_text(pdfs["DMS_V2.4"], 19), "DMS-003 V2.4 PDF 0:* missing")
        print("OK DMS-003 historical cardinality and V2.4 correction confirmed")

        # DMS-004: InstallUpdate requiredness changed only in later V2.4.
        old = {"UpdateID": "1", "UpdateTimestamp": "1", "UpdateURL": "1", "UpdateFileChecksum": "0", "UpdateFileSize": "0"}
        for version in ("v21", "v22"):
            require(base.install_requiredness(roots[version]) == old, f"DMS-004 {version} requiredness changed")
        new = {key: "0" for key in old}
        require(base.install_requiredness(roots["v24"]) == new, "DMS-004 V2.4 candidate requiredness changed")
        v22_install = base.page_text(pdfs["DMS_V2.2"], 26)
        v24_install = base.page_text(pdfs["DMS_V2.4"], 25)
        for phrase in ("UpdateID 1:1", "UpdateTimestamp 1:1", "UpdateURL 1:1"):
            require(phrase in v22_install, f"DMS-004 V2.2 PDF missing {phrase}")
        for phrase in ("UpdateID 0:1", "UpdateTimestamp 0:1", "UpdateURL 0:1"):
            require(phrase in v24_install, f"DMS-004 V2.4 PDF missing {phrase}")
        print("OK DMS-004 profile-specific InstallUpdate requiredness confirmed")

        # DMS-005: exact XSD branch plus visual table evidence.  We do not
        # reconstruct the wrapped PDF cell from interleaved pdftotext columns.
        exact_branch = "DeviceManagementService.GetDeviceStatusInformationResponseData"
        pdf_branch = "DeviceManagementService.DeviceStatusInformationResponseData"
        for version in ("v22", "v24"):
            branches = base.response_choice_names(roots[version])
            require(exact_branch in branches, f"DMS-005 {version} exact branch missing")
            require(pdf_branch not in branches, f"DMS-005 {version} PDF-only alias unexpectedly exists")
        for source_id, page, png_hash in (
            ("DMS_V2.2", 23, "caa6a73b3117d766f48630114cc6c13ddcb30f65d42b861c1f6c677ef1c3c5b1"),
            ("DMS_V2.4", 22, "97a4a83efd7dda8dc81b4d966ff0cbe217878f9622adb2cf67f4a0b26db4696a"),
        ):
            rec = visual_page(visual, source_id, page)
            require(rec.get("png_sha256") == png_hash, f"DMS-005 {source_id} visual hash changed")
            require(has_observation(rec, pdf_branch), f"DMS-005 {source_id} non-Get visual observation missing")
            require(has_observation(rec, exact_branch), f"DMS-005 {source_id} Get-prefixed visual observation missing")
        print("OK DMS-005 PDF/XSD branch-name mismatch confirmed by byte-pinned visual evidence")

        # DMS-006: V2.2 PDF omits two XSD-required fields; V2.4 cardinalities
        # align, while a newly discovered visual spelling typo is tracked apart.
        req22 = base.status_requiredness(roots["v22"])
        require(req22 == {"DeviceStatusName": "1", "DeviceStatusFlag": "1", "DeviceStatusImpact": "1", "DeviceStatusPriority": "1"}, f"DMS-006 V2.2 requiredness changed: {req22!r}")
        req24 = base.status_requiredness(roots["v24"])
        require(req24 == {"DeviceStatusName": "1", "DeviceStatusFlag": "1", "DeviceStatusImpact": "0", "DeviceStatusPriority": "0"}, f"DMS-006 V2.4 requiredness changed: {req24!r}")
        p22 = visual_page(visual, "DMS_V2.2", 23)
        require(has_observation(p22, "only DeviceStatusName 1:1 and DeviceStatusFlag 1:1"), "DMS-006 V2.2 visual omission observation missing")
        p24 = visual_page(visual, "DMS_V2.4", 23)
        require(has_observation(p24, "DeviceStatusImpact as 0:1"), "DMS-006 V2.4 impact observation missing")
        print("OK DMS-006 V2.2 PDF omission/XSD requirement and V2.4 cardinality alignment confirmed")

        # DMS-007: GetUpdateStates is documentation text only; operation model
        # and XSD annotation consistently use GetUpdateHistory.
        for version in ("v22", "v24"):
            annotation = base.update_timestamp_annotation(roots[version])
            require("GetUpdateHistory" in annotation and "RetrieveUpdateState" in annotation, f"DMS-007 {version} authoritative annotation changed")
            require("GetUpdateStates" not in annotation, f"DMS-007 {version} candidate annotation unexpectedly uses GetUpdateStates")
        for version in ("v21", "v22", "v24"):
            names = base.group_names(roots[version]) + list(base.global_names(roots[version]))
            require(any("GetUpdateHistory" in name for name in names), f"DMS-007 {version} GetUpdateHistory model missing")
            require(not any("GetUpdateStates" in name for name in names), f"DMS-007 {version} GetUpdateStates alias unexpectedly exists")
        require("GetUpdateStates" in base.page_text(pdfs["DMS_V2.2"], 26), "DMS-007 V2.2 PDF typo text missing")
        require("GetUpdateStates" in base.page_text(pdfs["DMS_V2.4"], 25), "DMS-007 V2.4 PDF typo text missing")
        print("OK DMS-007 GetUpdateStates documentation typo / GetUpdateHistory operation model confirmed")

        # Post-freeze visual delta DRDMS24-002: documentation-only typo.
        delta = visual.get("post_freeze_visual_delta", {})
        require(delta.get("id") == "DRDMS24-002", "post-freeze visual delta id changed")
        require(delta.get("state") == "context_verified", "DRDMS24-002 must be terminal context_verified")
        require(delta.get("validation_behavior") == "none; do not create an eDeviceStatusPriority alias and do not reject/accept XML based on the PDF typo", "DRDMS24-002 validation behavior changed")
        globals24 = base.global_names(roots["v24"])
        require("eDeviceStatusPriority" not in globals24, "unexpected V2.4 global eDeviceStatusPriority alias")
        status24 = base.status_requiredness(roots["v24"])
        require("DeviceStatusPriority" in status24, "DRDMS24-002 candidate XSD DeviceStatusPriority missing")
        require(has_observation(p24, "eDeviceStatusPriority 0:1"), "DRDMS24-002 visual typo observation missing")
        print("OK DRDMS24-002 post-freeze visual documentation typo recorded without schema rule")

    result = {
        "evidence_id": "EV-127",
        "finding_block": [f"DMS-{i:03d}" for i in range(1, 8)],
        "result": "PASS",
        "visual_evidence_run_id": EXPECTED_VISUAL_RUN,
        "visual_evidence_artifact_id": EXPECTED_VISUAL_ARTIFACT,
        "post_freeze_visual_delta": "DRDMS24-002",
        "terminal_revalidation_recommendations": {
            "DMS-001": "context_verified",
            "DMS-002": "context_verified",
            "DMS-003": "executable_confirmed",
            "DMS-004": "executable_confirmed",
            "DMS-005": "executable_confirmed",
            "DMS-006": "executable_confirmed",
            "DMS-007": "context_verified"
        },
        "frozen_inventory_mutated": False,
        "xsd_mutated": False
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASSED: EV-127 final DMS-001..007 revalidation plus DRDMS24-002 visual delta guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
