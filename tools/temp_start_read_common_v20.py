#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import urllib.request

import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "COMMON_V2.0"
URL = "https://www.vdv.de/301-2-1-sds-v-2-0.pdfx"
RUN_ID = os.environ["GITHUB_RUN_ID"]
COMMON_XSD = "IBIS-IP_common_V2.0.xsd"
ENUM_XSD = "IBIS-IP_Enumerations_V2.0.xsd"
EXPECTED_COMMON_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"
OFFICIAL_TAG = "VDV-301-2.0"


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj) -> None:
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


# Fail closed on exact XSD authority before touching the source-pin registry.
common_bytes = (ROOT / COMMON_XSD).read_bytes()
enum_bytes = (ROOT / ENUM_XSD).read_bytes()
common_blob = git_blob_sha(common_bytes)
enum_blob = git_blob_sha(enum_bytes)
if common_blob != EXPECTED_COMMON_BLOB:
    raise SystemExit(f"COMMON V2.0 blob mismatch: {common_blob} != {EXPECTED_COMMON_BLOB}")
if enum_blob != EXPECTED_ENUM_BLOB:
    raise SystemExit(f"ENUM V2.0 blob mismatch: {enum_blob} != {EXPECTED_ENUM_BLOB}")
if b'schemaLocation="IBIS-IP_Enumerations_V2.0.xsd"' not in common_bytes:
    raise SystemExit("COMMON V2.0 does not include the expected Enumerations V2.0 filename")
print("COMMON_V20_XSD_AUTHORITY_OK", OFFICIAL_TAG, common_blob, enum_blob)

req = urllib.request.Request(URL, headers={"User-Agent": "VDV301-audit-source-pin/1.0"})
with urllib.request.urlopen(req, timeout=90) as response:
    data = response.read()
if not data.startswith(b"%PDF-"):
    raise SystemExit("COMMON V2.0 source is not a PDF")

sha = hashlib.sha256(data).hexdigest()
size = len(data)
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
print("COMMON_V20_PIN", sha, size, ts, "RUN", RUN_ID)

pins_rel = "audit_registry/pdf_source_pins_v0.1.json"
pins = load_json(pins_rel)
if any(x.get("source_id") == SOURCE_ID for x in pins["sources"]):
    raise SystemExit("COMMON_V2.0 is already pinned")
pins["sources"].append({
    "source_id": SOURCE_ID,
    "expected_sha256": sha,
    "expected_size_bytes": size,
    "pinned_at_utc": ts,
    "deep_read_source_ready": True,
    "evidence_run_id": RUN_ID,
})
write_json(pins_rel, pins)

out = ROOT / "audit-results" / "common-v20-pinned-read"
pages_dir = out / "pages"
pages_dir.mkdir(parents=True, exist_ok=True)
doc = fitz.open(stream=data, filetype="pdf")
texts = []
page_hashes = {}
matrix = fitz.Matrix(120 / 72, 120 / 72)
for i, page in enumerate(doc):
    texts.append(f"===== PAGE {i + 1} =====\n" + page.get_text("text"))
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    p = pages_dir / f"page_{i + 1:03d}.png"
    pix.save(p)
    page_hashes[str(i + 1)] = hashlib.sha256(p.read_bytes()).hexdigest()

fulltext = "\n".join(texts)
fulltext_sha = hashlib.sha256(fulltext.encode("utf-8")).hexdigest()
(out / "fulltext.txt").write_text(fulltext, encoding="utf-8")
(out / "manifest.json").write_text(json.dumps({
    "source_id": SOURCE_ID,
    "official_url": URL,
    "pdf_sha256": sha,
    "pdf_size_bytes": size,
    "page_count": doc.page_count,
    "render_dpi": 120,
    "fulltext_sha256": fulltext_sha,
    "page_png_sha256": page_hashes,
    "run": RUN_ID,
    "xsd_authority": {
        "official_tag": OFFICIAL_TAG,
        "common_blob": common_blob,
        "enumerations_blob": enum_blob,
        "branch_bytes_match_official_tag": True,
    },
}, indent=2) + "\n", encoding="utf-8")
print("COMMON_V20_FULLTEXT_SHA", fulltext_sha)
print("COMMON_V20_PAGES", doc.page_count)

reg_rel = "audit_registry/deep_read_registry_delta_common_v20_2026-08-30.json"
reg = {
    "delta_version": "0.1",
    "date": "2026-08-30",
    "base_registry": "audit_registry/deep_read_registry_v0.1.json",
    "document_updates": {
        SOURCE_ID: {
            "state": "source_pinned_render_complete_pending_independent_fresh_read",
            "official_url": URL,
            "publication": "VDV 301-2-1 V2.0, Common Data Structures and Enumerations",
            "source_pin": {
                "sha256": sha,
                "size_bytes": size,
                "pinned_at_utc": ts,
                "evidence_run": RUN_ID,
            },
            "authority_status": {
                "official_pdf": "official_public_VDV_writing",
                "xsd_lane": "xsd",
                "exact_xsd_authority": "official_VDV-301-2.0_exact_family",
                "official_tag": OFFICIAL_TAG,
                "common_blob": common_blob,
                "enumerations_blob": enum_blob,
                "branch_bytes_match_official_tag": True,
                "latest_xsd_wins": False,
            },
            "historical_common_findings_quarantined_until_fresh_read_freeze": True,
            "fresh_read_rule": "derive observations from exact pinned COMMON V2.0 PDF against exact official VDV-301-2.0 Common/Enumerations family before consulting historical Common findings",
            "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
            "render_read_evidence": {
                "run": RUN_ID,
                "artifact_name": "common-v20-pinned-read",
                "pdf_page_count": doc.page_count,
                "all_pages_rendered": True,
                "render_dpi": 120,
                "fulltext_sha256": fulltext_sha,
            },
        }
    },
}
write_json(reg_rel, reg)

state_rel = "00_START_HERE/CURRENT_STATE.json"
state = load_json(state_rel)
state["date"] = "2026-08-30"
a = state["audit"]
if a.get("deep_read_in_progress") != 0 or a.get("next_natural_deep_read_document_id") != SOURCE_ID:
    raise SystemExit("CURRENT_STATE is not at the expected closed COMMON V1.0 boundary")
a["deep_read_needs_visual_review"] = 33
a["deep_read_textual_fresh_read_completed"] = 33
a["deep_read_in_progress"] = 1
a["deep_read_current_document_id"] = SOURCE_ID
a["deep_read_previous_document_id"] = "COMMON_V1.0"
a["next_natural_deep_read_document_id"] = SOURCE_ID
a["latest_deep_read_registry_delta"] = reg_rel
a["pdf_sources_byte_pinned"] = 28
if SOURCE_ID not in a["pinned_active_sources"]:
    a["pinned_active_sources"].append(SOURCE_ID)
a["common_v2_0_source_pin"] = {
    "sha256": sha,
    "size_bytes": size,
    "evidence_run": RUN_ID,
    "pinned_at_utc": ts,
    "pdf_authority": "official_public_VDV_writing",
    "xsd_authority_status": "official_VDV-301-2.0_exact_family",
}
a["common_v2_0_authority"] = {
    "official_tag": OFFICIAL_TAG,
    "Common_V2.0_blob": common_blob,
    "Enumerations_V2.0_blob": enum_blob,
    "integration_branch_matches_official_tag": True,
}
a["common_v2_0_render_read"] = {
    "run": RUN_ID,
    "artifact_name": "common-v20-pinned-read",
    "pdf_page_count": doc.page_count,
    "all_pages_rendered": True,
    "fulltext_sha256": fulltext_sha,
}
state["evidence"]["latest_pdf_source_pin_run"] = RUN_ID
state["evidence"]["latest_pdf_visual_render_run"] = RUN_ID
state["next_actions"] = [
    "Complete independent Fresh Read of COMMON V2.0 from the exact pinned full-text/render artifact before reopening historical Common findings.",
    "Falsify material table/cardinality/type/enumeration observations against exact official VDV-301-2.0 Common/Enumerations blobs.",
    "Visually inspect material pages from the exact pinned render artifact.",
    "Freeze COMMON V2.0 fresh observations before historical Common reconciliation.",
    "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze."
]
write_json(state_rel, state)

for rel in [pins_rel, reg_rel, state_rel]:
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

# Self-clean both temporary files; the workflow commit will stage their deletion.
Path(__file__).unlink()
workflow = ROOT / ".github/workflows/temp-start-read-common-v20.yml"
if workflow.exists():
    workflow.unlink()
print("COMMON_V20_START_READ_READY")
