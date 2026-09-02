#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "COMMON_V2.2"
URL = "https://www.vdv.de/301-2-1-sdes-v2-2-commonstructure-enums.pdfx"
RUN_ID = os.environ["GITHUB_RUN_ID"]
COMMON = "IBIS-IP_common_V2.2.xsd"
ENUMS = "IBIS-IP_Enumerations_V2.2.xsd"
COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
ENUMS_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
COMMON_LAST_MOD_COMMIT = "775def7b24901bfd515c80fa5fe57f12562873fd"
ENUMS_LAST_MOD_COMMIT = "591ca66d8b94bb5c2a7f9440b3e31e28f8261a88"


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


common_bytes = (ROOT / COMMON).read_bytes()
enum_bytes = (ROOT / ENUMS).read_bytes()
if git_blob_sha(common_bytes) != COMMON_BLOB:
    raise SystemExit("COMMON V2.2 branch Common blob does not match historical upstream authority")
if git_blob_sha(enum_bytes) != ENUMS_BLOB:
    raise SystemExit("COMMON V2.2 branch Enumerations blob does not match historical upstream authority")
if b'IBIS-IP_Enumerations_V2.2.xsd' not in common_bytes:
    raise SystemExit("COMMON V2.2 does not include expected Enumerations V2.2 dependency")
print("COMMON_V22_XSD_AUTHORITY_OK", COMMON_BLOB, ENUMS_BLOB, COMMON_LAST_MOD_COMMIT, ENUMS_LAST_MOD_COMMIT)

req = urllib.request.Request(URL, headers={"User-Agent": "VDV301-audit-source-pin/1.0"})
last_exc = None
for attempt in range(1, 4):
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
        break
    except Exception as exc:
        last_exc = exc
        print(f"COMMON_V22_FETCH_ATTEMPT_{attempt}_FAILED", repr(exc))
        if attempt < 3:
            time.sleep(5 * attempt)
else:
    raise SystemExit(f"COMMON V2.2 official PDF download failed after 3 attempts: {last_exc!r}")

if not data.startswith(b"%PDF-"):
    raise SystemExit("COMMON V2.2 source is not a PDF")

sha = hashlib.sha256(data).hexdigest()
size = len(data)
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
print("COMMON_V22_PIN", sha, size, ts, "RUN", RUN_ID)

pins_rel = "audit_registry/pdf_source_pins_v0.1.json"
pins = load_json(pins_rel)
if any(x.get("source_id") == SOURCE_ID for x in pins["sources"]):
    raise SystemExit("COMMON_V2.2 is already pinned")
pins["sources"].append({
    "source_id": SOURCE_ID,
    "expected_sha256": sha,
    "expected_size_bytes": size,
    "pinned_at_utc": ts,
    "deep_read_source_ready": True,
    "evidence_run_id": RUN_ID,
})
write_json(pins_rel, pins)

out = ROOT / "audit-results" / "common-v22-pinned-read"
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
    "xsd_authority_model": "historical_upstream_file_lineage_no_release_tag",
    "common_blob": COMMON_BLOB,
    "enumerations_blob": ENUMS_BLOB,
    "common_last_modification_commit": COMMON_LAST_MOD_COMMIT,
    "enumerations_last_modification_commit": ENUMS_LAST_MOD_COMMIT,
}, indent=2) + "\n", encoding="utf-8")
print("COMMON_V22_FULLTEXT_SHA", fulltext_sha)
print("COMMON_V22_PAGES", doc.page_count)

reg_rel = "audit_registry/deep_read_registry_delta_common_v22_2026-09-02.json"
reg = {
    "delta_version": "0.1",
    "date": "2026-09-02",
    "base_registry": "audit_registry/deep_read_registry_v0.1.json",
    "document_updates": {
        SOURCE_ID: {
            "state": "source_pinned_render_complete_pending_independent_fresh_read",
            "official_url": URL,
            "publication": "VDV 301-2-1 V2.2, Common Data Structures and Enumerations",
            "source_pin": {
                "sha256": sha,
                "size_bytes": size,
                "pinned_at_utc": ts,
                "evidence_run": RUN_ID,
            },
            "authority_status": {
                "official_pdf": "official_public_VDV_writing",
                "xsd_lane": "xsd",
                "exact_xsd_authority": "historical_upstream_V2.2_file_lineage_exact_family",
                "release_tag": None,
                "release_tag_status": "no_VDV-301-2.2_tag_resolved_in_upstream_repository",
                "common_blob": COMMON_BLOB,
                "enumerations_blob": ENUMS_BLOB,
                "common_last_modification_commit": COMMON_LAST_MOD_COMMIT,
                "enumerations_last_modification_commit": ENUMS_LAST_MOD_COMMIT,
                "branch_bytes_match_historical_upstream": True,
                "latest_xsd_wins": False,
            },
            "historical_common_findings_quarantined_until_fresh_read_freeze": True,
            "fresh_read_rule": "derive observations from exact pinned COMMON V2.2 PDF against exact historical upstream V2.2 Common/Enumerations family before consulting historical Common findings",
            "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
            "render_read_evidence": {
                "run": RUN_ID,
                "artifact_name": "common-v22-pinned-read",
                "pdf_page_count": doc.page_count,
                "all_pages_rendered": True,
                "render_dpi": 120,
                "fulltext_sha256": fulltext_sha,
                "fresh_read_freeze": "not_started",
            },
        }
    },
}
write_json(reg_rel, reg)

state_rel = "00_START_HERE/CURRENT_STATE.json"
state = load_json(state_rel)
a = state["audit"]
if a.get("deep_read_in_progress") != 0:
    raise SystemExit("CURRENT_STATE unexpectedly has a Deep Read in progress")
if a.get("next_natural_deep_read_document_id") != SOURCE_ID:
    raise SystemExit("CURRENT_STATE is not at expected post-COMMON-V2.1 boundary")
if a.get("deep_read_textual_fresh_read_completed") != 34 or a.get("deep_read_needs_visual_review") != 34:
    raise SystemExit("CURRENT_STATE Deep Read counters are not the expected 34/34 baseline")
state["date"] = "2026-09-02"
a["deep_read_in_progress"] = 1
a["deep_read_current_document_id"] = SOURCE_ID
a["deep_read_previous_document_id"] = "COMMON_V2.1"
a["next_natural_deep_read_document_id"] = SOURCE_ID
a["latest_deep_read_registry_delta"] = reg_rel
a["pdf_sources_byte_pinned"] = int(a["pdf_sources_byte_pinned"]) + 1
if SOURCE_ID not in a["pinned_active_sources"]:
    a["pinned_active_sources"].append(SOURCE_ID)
a["common_v2_2_source_pin"] = {
    "sha256": sha,
    "size_bytes": size,
    "evidence_run": RUN_ID,
    "pinned_at_utc": ts,
    "pdf_authority": "official_public_VDV_writing",
    "xsd_authority_status": "historical_upstream_V2.2_file_lineage_exact_family",
}
a["common_v2_2_authority"] = {
    "release_tag": None,
    "release_tag_status": "no_VDV-301-2.2_tag_resolved_in_upstream_repository",
    "Common_V2.2_blob": COMMON_BLOB,
    "Enumerations_V2.2_blob": ENUMS_BLOB,
    "Common_last_modification_commit": COMMON_LAST_MOD_COMMIT,
    "Enumerations_last_modification_commit": ENUMS_LAST_MOD_COMMIT,
    "integration_branch_matches_historical_upstream": True,
}
a["common_v2_2_render_read"] = {
    "run": RUN_ID,
    "artifact_name": "common-v22-pinned-read",
    "pdf_page_count": doc.page_count,
    "all_pages_rendered": True,
    "fulltext_sha256": fulltext_sha,
    "fresh_read_freeze": "not_started",
}
state["evidence"]["latest_pdf_source_pin_run"] = RUN_ID
state["evidence"]["latest_pdf_visual_render_run"] = RUN_ID
state["next_actions"] = [
    "Complete the independent Fresh Read of COMMON V2.2 from the exact pinned full-text/render artifact before reopening historical Common findings.",
    "Visually falsify material table/cardinality/type observations against the exact pinned page renders.",
    "Freeze COMMON V2.2 fresh observations before historical Common reconciliation.",
    "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze."
]
write_json(state_rel, state)

for rel in [pins_rel, reg_rel, state_rel]:
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

print("COMMON_V22_START_READ_READY")
