#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone

import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "COMMON_V1.0"
URL = "https://www.vdv.de/301-2-1-sds.pdfx"
RUN_ID = os.environ["GITHUB_RUN_ID"]


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


req = urllib.request.Request(URL, headers={"User-Agent": "VDV301-audit-source-pin/1.0"})
with urllib.request.urlopen(req, timeout=90) as response:
    data = response.read()
if not data.startswith(b"%PDF-"):
    raise SystemExit("COMMON V1.0 source is not a PDF")

sha = hashlib.sha256(data).hexdigest()
size = len(data)
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
print("COMMON_V10_PIN", sha, size, ts, "RUN", RUN_ID)

pins_rel = "audit_registry/pdf_source_pins_v0.1.json"
pins = load_json(pins_rel)
if any(x.get("source_id") == SOURCE_ID for x in pins["sources"]):
    raise SystemExit("COMMON_V1.0 is already pinned")
pins["sources"].append({
    "source_id": SOURCE_ID,
    "expected_sha256": sha,
    "expected_size_bytes": size,
    "pinned_at_utc": ts,
    "deep_read_source_ready": True,
    "evidence_run_id": RUN_ID,
})
write_json(pins_rel, pins)

out = ROOT / "audit-results" / "common-v10-pinned-read"
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
}, indent=2) + "\n", encoding="utf-8")
print("COMMON_V10_FULLTEXT_SHA", fulltext_sha)
print("COMMON_V10_PAGES", doc.page_count)

reg_rel = "audit_registry/deep_read_registry_delta_common_v10_2026-08-29.json"
reg = {
    "delta_version": "0.1",
    "date": "2026-08-29",
    "base_registry": "audit_registry/deep_read_registry_v0.1.json",
    "document_updates": {
        SOURCE_ID: {
            "state": "source_pinned_render_complete_pending_independent_fresh_read",
            "official_url": URL,
            "publication": "VDV 301-2-1 V1.0, Gemeinsame Datenstrukturen und Aufzählungstypen",
            "source_pin": {
                "sha256": sha,
                "size_bytes": size,
                "pinned_at_utc": ts,
                "evidence_run": RUN_ID,
            },
            "authority_status": {
                "official_pdf": "official_public_VDV_writing",
                "xsd_lane": "xsd",
                "exact_xsd_authority": "pending_independent_release_history_resolution",
                "latest_xsd_wins": False,
            },
            "historical_common_findings_quarantined_until_fresh_read_freeze": True,
            "fresh_read_rule": "derive observations from the exact pinned COMMON V1.0 PDF and independently establish exact official XSD/dependency authority before consulting historical Common findings",
            "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
            "render_read_evidence": {
                "run": RUN_ID,
                "artifact_name": "common-v10-pinned-read",
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
a = state["audit"]
a["deep_read_needs_visual_review"] = 31
a["deep_read_textual_fresh_read_completed"] = 31
a["deep_read_in_progress"] = 1
a["deep_read_current_document_id"] = SOURCE_ID
a["deep_read_previous_document_id"] = "VDV301-3_02-2020"
a["next_natural_deep_read_document_id"] = SOURCE_ID
a["latest_deep_read_finding"] = "DRNET20-003"
a["latest_deep_read_revalidation"] = "NET-003_context_verified_exact_pinned_pdf"
a["latest_deep_read_registry_delta"] = reg_rel
a["latest_deep_read_findings_delta"] = "audit_registry/deep_read_findings_delta_vdv301_3_02_2020_2026-08-29.json"
a["network_vdv301_3_deep_read_report"] = "docs/pdf_xsd_semantic_audit/deep_read/VDV301-3_02-2020.md"
a["network_vdv301_3_handoff"] = "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VDV301_3_02_2020_DEEP_READ_2026-08-29.md"
a["network_vdv301_3_fresh_read_status"] = "historical_reconciliation_complete"
a["network_vdv301_3_findings"] = {
    "NET-001": "context_verified_exact_pinned_pdf",
    "NET-002": "context_verified_exact_pinned_pdf",
    "NET-003": "context_verified_exact_pinned_pdf",
    "DRNET20-001": "context_verified_internal_pdf_conflict_plus_external_IEEE_interpretation",
    "DRNET20-002": "context_verified_bilingual_safety_security_semantic_conflict",
    "DRNET20-003": "context_verified_grouped_editorial_residue_excluding_NET-003",
}
a["network_vdv301_3_adjacent_runtime_evidence"] = {
    "RV-002_corrected_rerun": "33267198470",
    "job": "99139252921",
    "status": "PASS",
    "boundary": "deterministic DNS-SD classifier only",
}
a["pdf_sources_byte_pinned"] = 27
if SOURCE_ID not in a["pinned_active_sources"]:
    a["pinned_active_sources"].append(SOURCE_ID)
a["common_v1_0_source_pin"] = {
    "sha256": sha,
    "size_bytes": size,
    "evidence_run": RUN_ID,
    "pinned_at_utc": ts,
    "pdf_authority": "official_public_VDV_writing",
    "xsd_authority_status": "pending_independent_release_history_resolution",
}
a["common_v1_0_render_read"] = {
    "run": RUN_ID,
    "artifact_name": "common-v10-pinned-read",
    "pdf_page_count": doc.page_count,
    "all_pages_rendered": True,
    "fulltext_sha256": fulltext_sha,
}
state["evidence"]["latest_pdf_source_pin_run"] = RUN_ID
state["evidence"]["latest_pdf_visual_render_run"] = RUN_ID
state["next_actions"] = [
    "Independently establish exact official COMMON V1.0 XSD and dependency authority from VDV repository history; do not use latest-XSD-wins.",
    "Complete the independent Fresh Read of COMMON V1.0 from the exact pinned full-text/render artifact before reopening historical Common findings.",
    "Visually falsify material table/cardinality/type observations against the exact pinned page renders.",
    "Freeze COMMON V1.0 fresh observations before historical Common reconciliation.",
    "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze."
]
write_json(state_rel, state)

for rel in [pins_rel, reg_rel, state_rel]:
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

Path(__file__).unlink()
print("COMMON_V10_START_READ_READY")
