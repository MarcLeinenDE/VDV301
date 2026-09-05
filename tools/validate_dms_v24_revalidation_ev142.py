#!/usr/bin/env python3
"""EV-142 fail-closed revalidation evidence for frozen DMS V2.4 finding DRDMS24-001.

The finding is documentation-only: the official DeviceManagementService V2.4
foreword describes HtmlDisplayService.  The candidate/integration V2.4 XSD is
used only as corroborating service-identity context and is never promoted to an
official release authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/DMS_V2.4.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.4.md")
DELTA = Path("audit_registry/deep_read_findings_delta_dms_v24_2026-08-28.json")
REG_DELTA = Path("audit_registry/deep_read_registry_delta_dms_v24_2026-08-28.json")
DMS_XSD = Path("IBIS-IP_DeviceManagementService_V2.4.xsd")
COMMON = Path("IBIS-IP_common_V2.4.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.4.xsd")
EV108 = Path("tools/validate_dms_v24_deep_read_ev108.py")
OUT_DIR = Path(os.environ.get("EV142_OUTPUT_DIR", "artifacts/ev142"))

EXPECTED_PDF_SHA256 = "347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd"
EXPECTED_PDF_SIZE = 1298127
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "dba69e23579186f1c6c26451f93d9f04ba5728b3"
EXPECTED_DELTA_BLOB = "3e07eec98384744b113cb25c37916c67ac23cc6f"
EXPECTED_REG_DELTA_BLOB = "edffb50eeb6e12c7eae8f6d5fcac3e6566482adc"
EXPECTED_DMS_BLOB = "d222dfd98b2be3777576388da7ace8f333d24c3f"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
EXPECTED_EV108_BLOB = "6a88fbc6546d73d9f68936889087a8120b118358"
FINDING = "DRDMS24-001"
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256(); size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk); size += len(chunk)
    return h.hexdigest(), size


def page_count() -> int:
    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True, errors="replace")
    match = re.search(r"^Pages:\s*(\d+)\s*$", info, re.MULTILINE)
    require(match is not None, "pdfinfo did not expose page count")
    return int(match.group(1))


def page_text(page: int) -> str:
    return subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True, errors="replace"
    )


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def contexts(text: str, needle: str, radius: int = 260) -> list[str]:
    low = text.lower(); token = needle.lower(); out: list[str] = []
    start = 0
    while True:
        idx = low.find(token, start)
        if idx < 0:
            break
        out.append(compact(text[max(0, idx-radius): min(len(text), idx+len(needle)+radius)]))
        start = idx + len(token)
    return out


def main() -> int:
    require(PDF.is_file(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        REG_DELTA: EXPECTED_REG_DELTA_BLOB,
        DMS_XSD: EXPECTED_DMS_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV108: EXPECTED_EV108_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal, pending) == (100, 92), f"unexpected pre-DMS-V2.4 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "DMS", f"unexpected next block {reg.get('next_revalidation_block')}")
    blocks = reg.get("revalidation_blocks", {})
    prev = blocks.get("DMS_V2.2", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "DMS_V2.4", "DMS V2.2 does not route to DMS V2.4")
    require(blocks.get("DMS", {}).get("state") == "completed", "legacy DMS block missing or changed")
    require("DMS_V2.4" not in blocks, "DMS V2.4 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "DMS_V2.4", "wrong DMS V2.4 delta document id")
    fresh = [x for x in delta.get("new_findings", []) if x.get("id") == FINDING]
    require(len(fresh) == 1, f"expected one {FINDING} record, found {len(fresh)}")
    finding = fresh[0]
    require(finding.get("classification") == "pdf_copy_paste_service_identity_error_candidate", "finding classification changed")
    require(finding.get("state") == "confirmed_text_needs_visual_review", "historical visual-review state changed")
    require(finding.get("normative_validation_impact") == "none; do not infer HTMLDisplay semantics, routes or validation rules for DeviceManagementService", "finding validation-impact statement changed")

    reg_delta = json.loads(REG_DELTA.read_text(encoding="utf-8"))
    update = reg_delta.get("document_updates", {}).get("DMS_V2.4", {})
    boundary = update.get("authority_boundary", {})
    require(boundary.get("pdf_authority") == "official_public_VDV_writing", "official PDF authority boundary changed")
    require(boundary.get("xsd_authority") == "candidate_or_integration_material_in_dev_schema_integration", "candidate XSD authority boundary changed")
    require("Do not describe" in str(boundary.get("rule")), "candidate authority guard missing")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "DRDMS24-001 - wrong service in the V2.4 foreword",
        "HtmlDisplayService",
        "PDF: official public VDV writing.",
        "candidate/integration material",
        "validation impact: none",
    ):
        require(anchor in deep, f"DMS V2.4 deep-read anchor missing: {anchor}")

    # Corroborating candidate/integration structure context only.  This does not
    # convert the XSD into official V2.4 release authority.
    tree = etree.parse(str(DMS_XSD))
    etree.XMLSchema(tree)
    root = tree.getroot()
    includes = [x.get("schemaLocation") for x in root.findall("xs:include", NS)]
    require("IBIS-IP_common_V2.4.xsd" in includes and "IBIS-IP_Enumerations_V2.4.xsd" in includes, "candidate V2.4 include route changed")
    group = root.find("xs:group[@name='DeviceManagementServiceGroup']/xs:sequence", NS)
    require(group is not None, "candidate DeviceManagementServiceGroup missing")
    op_names = [x.get("name") for x in group.findall("xs:element", NS) if x.get("name")]
    require(op_names and all(name.startswith("DeviceManagementService.") for name in op_names), "candidate DMS group contains non-DMS operation identity")
    require(not any("HtmlDisplayService" in name for name in op_names), "candidate DMS group unexpectedly contains HtmlDisplayService operation")

    ev108 = subprocess.run([sys.executable, str(EV108)], text=True, capture_output=True)
    print(ev108.stdout, end="")
    if ev108.stderr:
        print(ev108.stderr, file=sys.stderr, end="")
    require(ev108.returncode == 0, "preserved EV-108 rerun failed")
    require("PASSED: EV-108 DMS V2.4 candidate/integration declaration evidence confirmed" in ev108.stdout, "EV-108 success boundary missing")

    # Discover the original foreword evidence directly from the exact PDF.
    pages = page_count()
    html_pages: list[int] = []
    html_contexts: dict[str, list[str]] = {}
    title_pages: list[int] = []
    html_occurrences = 0
    for page in range(1, pages + 1):
        text = page_text(page)
        count = text.lower().count("htmldisplayservice".lower())
        if count:
            html_pages.append(page)
            html_occurrences += count
            html_contexts[str(page)] = contexts(text, "HtmlDisplayService")
        if page <= 6 and "DeviceManagementService" in text and ("V2.4" in text or "Version 2.4" in text):
            title_pages.append(page)

    require(html_pages, "official DMS V2.4 PDF contains no HtmlDisplayService foreword evidence")
    require(html_occurrences >= 2, f"expected German+English HtmlDisplayService occurrences, found {html_occurrences}")
    require(title_pages, "early official PDF pages do not establish DeviceManagementService V2.4 document identity")

    joined_context = " ".join(x for values in html_contexts.values() for x in values).lower()
    # Strongest counter-hypothesis: HtmlDisplayService is merely referenced as a
    # related service.  The fresh-read claim requires identity/purpose wording.
    identity_language = any(token in joined_context for token in (
        "dieses dokument", "this document", "beschreibt", "describes"
    ))
    html_purpose = ("html" in joined_context and ("web" in joined_context or "server" in joined_context))
    require(identity_language, "HtmlDisplayService context lacks document-identity/descriptive wording")
    require(html_purpose, "HtmlDisplayService context lacks the copied HTML/Web-server purpose wording")

    evidence_pages = sorted(set(title_pages + html_pages))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in evidence_pages), encoding="utf-8")
    (OUT_DIR / "page_map.json").write_text(json.dumps({
        "document_identity_pages": title_pages,
        "html_display_foreword_pages": html_pages,
        "html_display_occurrences": html_occurrences,
        "contexts": html_contexts,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = {
        "evidence_id": "EV-142",
        "finding_block": [FINDING],
        "pdf_source_id": "DMS_V2.4",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": pages,
        "evidence_pages": evidence_pages,
        "html_display_foreword_pages": html_pages,
        "html_display_occurrences": html_occurrences,
        "authority": {
            "pdf": "official_public_VDV_writing",
            "xsd": "candidate_or_integration_material_in_dev_schema_integration",
            "official_release_xsd_claimed": False,
            "latest_xsd_wins": False,
        },
        "active_disproof": {
            "hypothesis": "HtmlDisplayService is only a related-service reference, not copied document identity/purpose prose",
            "result": "rejected_by_foreword_identity_language_plus_HTML_Web_server_purpose_context",
        },
        "candidate_structure_context": {
            "service_group": "DeviceManagementServiceGroup",
            "all_group_operations_are_DeviceManagementService_prefixed": True,
            "HtmlDisplayService_operation_present": False,
            "EV-108": "rerun unchanged PASS",
        },
        "terminal_revalidation_recommendations": {FINDING: "context_verified"},
        "executable_evidence_reason_not_applicable": "The finding is a documentation copy/paste service-identity error and does not define XML instance validity; candidate XSD execution is corroborating context only.",
        "visual_review": "all discovered substantive pages must be rendered and inspected before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW",
    }
    (OUT_DIR / "ev142_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_CONTEXT: EV-142 DMS V2.4 DRDMS24-001; visual page review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
