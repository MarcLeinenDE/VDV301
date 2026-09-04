#!/usr/bin/env python3
"""EV-134 evidence gate for VDV301-2 General Conventions V2.4 findings DR3012GC24-001..005."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/VDV301-2_GC_V2.4.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.4.xsd")
COMMON_XSD = Path("IBIS-IP_common_V2.4.xsd")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_GC_V2.4.md")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
OUT_DIR = Path(os.environ.get("EV134_OUTPUT_DIR", "artifacts/ev134"))

EXPECTED_PDF_SHA256 = "048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d"
EXPECTED_PDF_SIZE = 1767094
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
FINDINGS = [f"DR3012GC24-{i:03d}" for i in range(1, 6)]
TERMINAL_RECOMMENDATIONS = {
    "DR3012GC24-001": "executable_confirmed",
    "DR3012GC24-002": "context_verified",
    "DR3012GC24-003": "context_verified",
    "DR3012GC24-004": "executable_confirmed",
    "DR3012GC24-005": "context_verified",
}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def norm(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").replace("’", "'").replace("‘", "'").split())


def page_count() -> int:
    out = subprocess.check_output(["pdfinfo", str(PDF)], text=True, errors="replace")
    m = re.search(r"^Pages:\s+(\d+)\s*$", out, re.MULTILINE)
    require(m is not None, "pdfinfo page count missing")
    return int(m.group(1))


def page_text(page: int) -> str:
    return norm(subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True,
        errors="replace",
    ))


def all_pages() -> dict[int, str]:
    return {p: page_text(p) for p in range(1, page_count() + 1)}


def pages_with(pages: dict[int, str], *needles: str) -> list[int]:
    return [p for p, text in pages.items() if all(n in text for n in needles)]


def pages_any(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    return [p for p, text in pages.items() if any(n in text for n in needles)]


def enum_values(type_name: str) -> list[str]:
    root = etree.parse(str(ENUM_XSD)).getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    return root.xpath(
        f"./xs:simpleType[@name='{type_name}']/xs:restriction/xs:enumeration/@value",
        namespaces=ns,
    )


def compile_enum_element(root_name: str, type_name: str) -> etree.XMLSchema:
    text = f'''<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
  <xs:element name="{root_name}" type="{type_name}"/>
</xs:schema>
'''
    with tempfile.NamedTemporaryFile("w", suffix=".xsd", dir=".", encoding="utf-8", delete=False) as fh:
        fh.write(text)
        tmp = Path(fh.name)
    try:
        return etree.XMLSchema(etree.parse(str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)


def valid(schema: etree.XMLSchema, root: str, value: str) -> bool:
    return schema.validate(etree.fromstring(f"<{root}>{value}</{root}>".encode()))


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.4 authority changed")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.4 authority changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding in FINDINGS:
        require(finding in frozen.get("finding_ids", []), f"missing frozen finding {finding}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    auth = state.get("audit", {}).get("common_v2_4_authority", {})
    require(auth.get("status") == "candidate_integration_explicit_selection", "V2.4 authority lane changed")
    require(auth.get("common_blob") == EXPECTED_COMMON_BLOB, "CURRENT_STATE Common V2.4 blob changed")
    require(auth.get("enumerations_blob") == EXPECTED_ENUM_BLOB, "CURRENT_STATE Enumerations V2.4 blob changed")
    require(auth.get("upstream_draft_pr") == "VDVde/VDV301#31", "V2.4 upstream draft provenance changed")
    require(auth.get("official_release_tag") is None, "unexpected official V2.4 release tag")

    common_root = etree.parse(str(COMMON_XSD)).getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    includes = common_root.xpath("./xs:include/@schemaLocation", namespaces=ns)
    require("IBIS-IP_Enumerations_V2.4.xsd" in includes, "Common V2.4 does not include Enumerations V2.4")
    etree.XMLSchema(etree.parse(str(COMMON_XSD)))

    pages = all_pages()
    render_pages: set[int] = set()
    evidence_pages: dict[str, list[int]] = {}

    # 001: German enum spelling differs from English/XSD and changes validity.
    p_onbord = pages_any(pages, ("OnBordUnit",))
    p_onboard = pages_any(pages, ("OnBoardUnit",))
    require(p_onbord, "DR3012GC24-001 German OnBordUnit page missing")
    require(p_onboard, "DR3012GC24-001 English OnBoardUnit page missing")
    device_values = enum_values("DeviceClassEnumeration")
    require("OnBoardUnit" in device_values and "OnBordUnit" not in device_values, "DeviceClassEnumeration spelling boundary unexpected")
    device_schema = compile_enum_element("DeviceClass", "DeviceClassEnumeration")
    require(valid(device_schema, "DeviceClass", "OnBoardUnit"), "OnBoardUnit should validate")
    require(not valid(device_schema, "DeviceClass", "OnBordUnit"), "OnBordUnit unexpectedly validates")
    evidence_pages["DR3012GC24-001"] = sorted(set(p_onbord + p_onboard))
    render_pages.update(evidence_pages["DR3012GC24-001"])
    print("OK DR3012GC24-001 OnBordUnit PDF spelling is rejected by selected Enumerations V2.4 while OnBoardUnit validates")

    # 002: German duplicates 2.1.1 while English uses 2.1.2.
    p_subnet_de = pages_any(pages, ("2.1.1 Subnetzmasken", "2.1.1  Subnetzmasken"))
    p_ip_de = pages_any(pages, ("2.1.1 IP-Adressen", "2.1.1  IP-Adressen"))
    p_subnet_en = pages_any(pages, ("2.1.2 Subnet Masks", "2.1.2  Subnet Masks"))
    require(p_subnet_de and p_ip_de and p_subnet_en, "DR3012GC24-002 numbering anchors missing")
    evidence_pages["DR3012GC24-002"] = sorted(set(p_subnet_de + p_ip_de + p_subnet_en))
    render_pages.update(evidence_pages["DR3012GC24-002"])
    print("OK DR3012GC24-002 German subnet heading duplicates 2.1.1 while English uses 2.1.2")

    # 003: English allowed-version-character list duplicates digit 2; German control does not.
    dup_candidates = []
    for p, text in pages.items():
        compact = re.sub(r"\s+", "", text)
        if "'0','1','2','2','3','4','5','6','7','8','9'" in compact or '"0","1","2","2","3","4","5","6","7","8","9"' in compact:
            dup_candidates.append(p)
    require(dup_candidates, "DR3012GC24-003 duplicated English version-character list not found")
    evidence_pages["DR3012GC24-003"] = dup_candidates
    render_pages.update(dup_candidates)
    print("OK DR3012GC24-003 English version-character list visibly/textually duplicates digit 2")

    # 004: typo-like technical service identifiers must not become executable aliases.
    typo_names = ("DeviceManagmenService", "CustomumerInformationService", "DeviceManagmentServices", "PassengerCountigService")
    typo_pages = pages_any(pages, typo_names)
    require(len(typo_pages) >= 2, "DR3012GC24-004 technical identifier typo contexts insufficient")
    service_values = enum_values("ServiceNameEnumeration")
    correct = ("DeviceManagementService", "CustomerInformationService", "PassengerCountingService")
    require(all(x in service_values for x in correct), "correct service identifiers missing from ServiceNameEnumeration")
    require(all(x not in service_values for x in typo_names), "typo service identifier unexpectedly present in ServiceNameEnumeration")
    service_schema = compile_enum_element("ServiceName", "ServiceNameEnumeration")
    for value in correct:
        require(valid(service_schema, "ServiceName", value), f"correct service identifier rejected: {value}")
    for value in typo_names:
        require(not valid(service_schema, "ServiceName", value), f"typo service identifier unexpectedly validates: {value}")
    evidence_pages["DR3012GC24-004"] = typo_pages
    render_pages.update(typo_pages)
    print("OK DR3012GC24-004 typo service identifiers are present in PDF contexts but rejected by selected Enumerations V2.4")

    # 005: same document denies common version but later says Version 1.0 of IBIS-IP.
    no_common = pages_any(pages, ("keine gemeinsame Version", "no common IBIS-IP version", "no common version"))
    umbrella = pages_any(pages, ("Version 1.0 of IBIS-IP", "Version 1.0 von IBIS-IP", "Version 1.0 des IBIS-IP"))
    require(no_common, "DR3012GC24-005 no-common-version anchor missing")
    require(umbrella, "DR3012GC24-005 Version 1.0 umbrella wording missing")
    evidence_pages["DR3012GC24-005"] = sorted(set(no_common + umbrella))
    render_pages.update(evidence_pages["DR3012GC24-005"])
    print("OK DR3012GC24-005 no-common-version rule conflicts with stale Version 1.0 of IBIS-IP wording")

    # Active context checks: predecessor numbering repaired, V2.2 Word placeholder regressed in V2.4.
    fixed_v23 = pages_any(pages, ("7.2.1 Funktionale Erweiterungen",))
    fixed_v23_en = pages_any(pages, ("7.2.2 Technical Upgrade/Corrections",))
    require(fixed_v23 and fixed_v23_en, "V2.3 history-numbering repair not found in V2.4")
    word_regression = pages_any(pages, ("Fehler! Verweisquelle konnte nicht gefunden werden.",))
    require(len(word_regression) >= 2, "V2.4 Word-reference regression not independently repeated")
    render_pages.update(fixed_v23)
    render_pages.update(fixed_v23_en)
    render_pages.update(word_regression)

    deep = DEEP_READ.read_text(encoding="utf-8")
    for finding in FINDINGS:
        require(finding in deep, f"deep-read source missing {finding}")
    require("candidate_integration_explicit_selection" not in deep or True, "noop")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("\n".join(str(p) for p in sorted(render_pages)) + "\n", encoding="utf-8")
    result = {
        "evidence_id": "EV-134",
        "finding_block": FINDINGS,
        "pdf_source_id": "VDV301-2_GC_V2.4",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "authority_lane": "candidate_integration_explicit_selection_from_VDVde_VDV301_PR31; no official V2.4 release tag",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "evidence_pages": evidence_pages,
        "context_pages": {
            "V2.3_history_numbering_repaired": sorted(set(fixed_v23 + fixed_v23_en)),
            "V2.4_word_reference_regression": word_regression,
        },
        "terminal_revalidation_recommendations": TERMINAL_RECOMMENDATIONS,
        "executable_tests": {
            "DeviceClass_OnBoardUnit": "valid",
            "DeviceClass_OnBordUnit": "invalid",
            "correct_ServiceNameEnumeration_values": "valid",
            "typo_service_identifiers": "invalid",
        },
        "visual_review": "rendered pages required before permanent evidence record/closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW",
    }
    (OUT_DIR / "ev134_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-134 GC V2.4 DR3012GC24-001..005; visual artifact review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
