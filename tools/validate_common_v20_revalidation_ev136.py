#!/usr/bin/env python3
"""EV-136 fail-closed revalidation evidence for COMMON V2.0 DRCOM20-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V2.0.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.0.md")
COMMON = Path("IBIS-IP_common_V2.0.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.0.xsd")
EV118 = Path("tools/validate_common_v20_ev118.py")
OUT_DIR = Path(os.environ.get("EV136_OUTPUT_DIR", "artifacts/ev136"))

EXPECTED_PDF_SHA256 = "23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088"
EXPECTED_PDF_SIZE = 946088
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "dd436b990a4a80d7c0c2768181a1c3d27befd049"
EXPECTED_COMMON_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"
EXPECTED_EV118_BLOB = "6db122b1726376b11ac24cfec68dbfbd758b079e"
FINDING = "DRCOM20-001"
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
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def canon(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.replace("\u00ad", "").lower())


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(blob(DEEP_READ) == EXPECTED_DEEP_READ_BLOB, "COMMON V2.0 Deep Read changed")
    require(blob(COMMON) == EXPECTED_COMMON_BLOB, "Common V2.0 authority changed")
    require(blob(ENUMS) == EXPECTED_ENUM_BLOB, "Enumerations V2.0 authority changed")
    require(blob(EV118) == EXPECTED_EV118_BLOB, "preserved EV-118 checker changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_id = {x.get("finding_id"): x for x in reg.get("inventory", {}).get("entries", [])}
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    require(reg.get("revalidation_blocks", {}).get("COMMON_V1.0", {}).get("next_subblock") == "COMMON_V2.0", "COMMON V1.0 does not route to COMMON V2.0")
    require("COMMON_V2.0" not in reg.get("revalidation_blocks", {}), "COMMON V2.0 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "DRCOM20-001: pdf_type_reference_vs_xsd_primitive_instance_shape_mismatch",
        "Pinned page 13 visibly documents `InternationalTextType`",
        "IBIS-IP.string",
        "IBIS-IP.language",
        "xs:string",
        "xs:language",
        "EV-118 run `33280224191`",
    ):
        require(anchor in deep, f"Deep Read anchor missing: {anchor}")

    root = etree.parse(str(COMMON)).getroot()
    include = root.find("xs:include", NS)
    require(include is not None and include.get("schemaLocation") == "IBIS-IP_Enumerations_V2.0.xsd", "Common V2.0 include route changed")
    intl = root.find("xs:complexType[@name='InternationalTextType']", NS)
    require(intl is not None, "InternationalTextType missing")
    value = intl.find("xs:sequence/xs:element[@name='Value']", NS)
    language = intl.find("xs:sequence/xs:element[@name='Language']", NS)
    require(value is not None and value.get("type") == "xs:string", "InternationalTextType.Value is not xs:string")
    require(language is not None and language.get("type") == "xs:language", "InternationalTextType.Language is not xs:language")
    etree.XMLSchema(etree.parse(str(COMMON)))

    # Preserve and rerun the original exact-authority executable evidence.
    ev118 = subprocess.run([sys.executable, str(EV118)], text=True)
    require(ev118.returncode == 0, "preserved EV-118 rerun failed")

    # The frozen Fresh Read identifies page 13 as the substantive visual source.
    # Canonicalize the extracted text because the table may line-wrap type names.
    page13 = subprocess.check_output(
        ["pdftotext", "-f", "13", "-l", "13", "-layout", str(PDF), "-"],
        text=True,
        errors="replace",
    )
    page13_canon = canon(page13)
    for anchor in ("InternationalTextType", "IBIS-IP.string", "IBIS-IP.language"):
        require(canon(anchor) in page13_canon, f"page 13 canonical visual-text anchor missing: {anchor}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("13\n", encoding="utf-8")
    result = {
        "evidence_id": "EV-136",
        "finding_block": [FINDING],
        "pdf_source_id": "COMMON_V2.0",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "evidence_pages": {FINDING: [13]},
        "authority_lane": "exact_official_VDV-301-2.0_release_family",
        "official_release_tag": "VDV-301-2.0",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-118 rerun unchanged",
        "active_disproof": {
            "exact_primitive_shape": "VALID in EV-118",
            "PDF_wrapper_shaped_Value_Language": "INVALID in EV-118"
        },
        "terminal_revalidation_recommendations": {FINDING: "executable_confirmed"},
        "visual_review": "rendered page 13 required before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW"
    }
    (OUT_DIR / "ev136_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-136 COMMON V2.0 DRCOM20-001; visual page 13 review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
