#!/usr/bin/env python3
"""EV-138 fail-closed revalidation evidence for COMMON V2.2 DRCOM22-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V2.2.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.2.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json")
COMMON = Path("IBIS-IP_common_V2.2.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.2.xsd")
EV120 = Path("tools/validate_common_v22_ev120.py")
OUT_DIR = Path(os.environ.get("EV138_OUTPUT_DIR", "artifacts/ev138"))

EXPECTED_PDF_SHA256 = "85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203"
EXPECTED_PDF_SIZE = 1411558
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "38e3c3f0f96486acf7aea40652398e00f575a1b4"
EXPECTED_DELTA_BLOB = "6b0208d153761bef6e0cbf0041888251b99cdca4"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV120_BLOB = "ca6aa03c50f7f63057e46623df639da77a1b67d7"
FINDING = "DRCOM22-001"
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


def occurs(node: etree._Element, attr: str) -> str:
    return node.get(attr, "1")


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV120: EXPECTED_EV120_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable source {path}")
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
    require((terminal, pending) == (93, 99), f"unexpected pre-V2.2 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    prev = reg.get("revalidation_blocks", {}).get("COMMON_V2.1", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.2", "COMMON V2.1 does not route to COMMON V2.2")
    require("COMMON_V2.2" not in reg.get("revalidation_blocks", {}), "COMMON V2.2 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "COMMON_V2.2", "wrong V2.2 delta document id")
    auth = delta.get("exact_xsd_authority", {})
    require(auth.get("authority_route") == "historical_upstream_V2.2_file_lineage_exact_family", "wrong V2.2 authority route")
    require(auth.get("release_tag") is None, "V2.2 unexpectedly gained a release tag")
    require(auth.get("latest_xsd_wins") is False, "V2.2 latest-wins guard changed")
    unique = delta.get("new_unique_findings", {}).get(FINDING, {})
    require(unique.get("state") == "executable_confirmed_EV-120", "historical V2.2 finding state changed")
    require(unique.get("classification") == "compositor_xsd_more_permissive_than_pdf", "V2.2 finding classification changed")
    require(unique.get("executable_effect") is True, "V2.2 finding lost executable effect")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "FR-COM22-002",
        "NetexMode choice groups are mandatory in the PDF but optional in XSD",
        "Pinned page 15 visibly uses VDV choice notation",
        "two separate `<xs:choice minOccurs=\"0\">` compositors",
    ):
        require(anchor in deep, f"Deep Read anchor missing: {anchor}")

    root = etree.parse(str(COMMON)).getroot()
    include = root.find("xs:include", NS)
    require(include is not None and include.get("schemaLocation") == "IBIS-IP_Enumerations_V2.2.xsd", "Common V2.2 include route changed")
    netex = root.find("xs:complexType[@name='NetexMode']", NS)
    require(netex is not None, "NetexMode missing")
    choices = netex.findall("./xs:sequence/xs:choice", NS)
    require(len(choices) == 2, f"NetexMode expected two top-level choices, got {len(choices)}")
    require(all(occurs(choice, "minOccurs") == "0" for choice in choices), "NetexMode choice minOccurs boundary changed")
    require([n.get("name") for n in choices[0].findall("xs:element", NS)] == ["PtMainMode", "PrivateMainMode"], "NetexMode main-mode branches changed")
    require([n.get("ref") for n in choices[1].findall("xs:group", NS)] == ["PtSubmodeChoiceGroup", "PrivateSubmodeChoiceGroup"], "NetexMode submode branches changed")
    etree.XMLSchema(etree.parse(str(COMMON)))

    ev120 = subprocess.run([sys.executable, str(EV120)], text=True, capture_output=True)
    print(ev120.stdout, end="")
    if ev120.stderr:
        print(ev120.stderr, file=sys.stderr, end="")
    require(ev120.returncode == 0, "preserved EV-120 rerun failed")
    require(
        "NetexMode empty structure accepted by XSD: VALID as expected" in ev120.stdout,
        "EV-120 empty NetexMode executable boundary missing",
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("15\n", encoding="utf-8")
    result = {
        "evidence_id": "EV-138",
        "finding_block": [FINDING],
        "pdf_source_id": "COMMON_V2.2",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "evidence_pages": {FINDING: [15]},
        "authority_lane": "historical_upstream_V2.2_file_lineage_exact_family",
        "official_release_tag": None,
        "common_last_modification_commit": "775def7b24901bfd515c80fa5fe57f12562873fd",
        "enumerations_last_modification_commit": "591ca66d8b94bb5c2a7f9440b3e31e28f8261a88",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-120 rerun unchanged",
        "active_disproof": {
            "PDF_claim": "both NetexMode one-of groups visibly mandatory on page 15",
            "exact_XSD_declaration": "two top-level xs:choice compositors each minOccurs=0",
            "empty_NetexMode_instance": "VALID in preserved EV-120 rerun"
        },
        "terminal_revalidation_recommendations": {FINDING: "executable_confirmed"},
        "visual_review": "rendered page 15 required before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW"
    }
    (OUT_DIR / "ev138_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-138 COMMON V2.2 DRCOM22-001; visual page 15 review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
