#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone

import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "COMMON_V2.1"
URL = "https://www.vdv.de/301-2-1-sds-v2-1-commonstructure-enums.pdfx"
RUN_ID = os.environ["GITHUB_RUN_ID"]
COMMON = "IBIS-IP_common_V2.1.xsd"
ENUMS = "IBIS-IP_Enumerations_V2.1.xsd"
COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
ENUMS_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
EXPECTED_PDF_SHA = "a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32"
EXPECTED_PDF_SIZE = 1274051
PRIOR_EVIDENCE_RUN = "33393002497"
PRIOR_ARTIFACT_ID = "9758203545"
PRIOR_FULLTEXT_SHA = "5dce4c8ecc770574bdce8d5961fefbc01f88b1547e3957855013d9b077fc24b0"


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


# Exact XSD authority must remain byte-identical to the official VDV-301-2.1 tag.
common_bytes = (ROOT / COMMON).read_bytes()
enum_bytes = (ROOT / ENUMS).read_bytes()
if git_blob_sha(common_bytes) != COMMON_BLOB:
    raise SystemExit("COMMON V2.1 branch Common blob does not match official VDV-301-2.1")
if git_blob_sha(enum_bytes) != ENUMS_BLOB:
    raise SystemExit("COMMON V2.1 branch Enumerations blob does not match official VDV-301-2.1")
if b"IBIS-IP_Enumerations_V2.1.xsd" not in common_bytes:
    raise SystemExit("COMMON V2.1 does not include expected Enumerations V2.1 dependency")
print("COMMON_V21_XSD_AUTHORITY_OK", COMMON_BLOB, ENUMS_BLOB)

# Fresh retrieval: recovery may only proceed when the official source is exactly the
# same byte sequence already evidenced by run 33393002497.
req = urllib.request.Request(URL, headers={"User-Agent": "VDV301-audit-source-pin/1.0"})
with urllib.request.urlopen(req, timeout=90) as response:
    data = response.read()
if not data.startswith(b"%PDF-"):
    raise SystemExit("COMMON V2.1 source is not a PDF")
sha = hashlib.sha256(data).hexdigest()
size = len(data)
if sha != EXPECTED_PDF_SHA or size != EXPECTED_PDF_SIZE:
    raise SystemExit(
        f"SOURCE_CHANGED_SINCE_AUDIT COMMON_V2.1 sha={sha} size={size} "
        f"expected_sha={EXPECTED_PDF_SHA} expected_size={EXPECTED_PDF_SIZE}"
    )
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
print("COMMON_V21_RECOVERY_PIN", sha, size, ts, "RUN", RUN_ID, "FROM", PRIOR_EVIDENCE_RUN)

pins_rel = "audit_registry/pdf_source_pins_v0.1.json"
pins = load_json(pins_rel)
if any(x.get("source_id") == SOURCE_ID for x in pins["sources"]):
    raise SystemExit("COMMON_V2.1 is already pinned; refusing to overwrite existing pin")
pins["sources"].append({
    "source_id": SOURCE_ID,
    "expected_sha256": sha,
    "expected_size_bytes": size,
    "pinned_at_utc": ts,
    "deep_read_source_ready": True,
    "evidence_run_id": RUN_ID,
    "recovered_from_evidence_run_id": PRIOR_EVIDENCE_RUN,
    "recovery_note": "Original 2026-08-31 pin timestamp was not retained in the uploaded evidence artifact; pinned_at_utc is this fresh byte-identical recovery retrieval/pin time."
})
write_json(pins_rel, pins)

# Re-render all pages as transient evidence. These bytes are uploaded as an Actions
# artifact and explicitly removed before any repository commit.
out = ROOT / ".tmp_common_v21_recovery_evidence"
pages_dir = out / "pages"
pages_dir.mkdir(parents=True, exist_ok=True)
doc = fitz.open(stream=data, filetype="pdf")
if doc.page_count != 48:
    raise SystemExit(f"Unexpected page count {doc.page_count}, expected 48")
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
    "pinned_at_utc": ts,
    "page_count": doc.page_count,
    "render_dpi": 120,
    "fulltext_sha256": fulltext_sha,
    "page_png_sha256": page_hashes,
    "run": RUN_ID,
    "official_tag": "VDV-301-2.1",
    "common_blob": COMMON_BLOB,
    "enumerations_blob": ENUMS_BLOB,
    "recovery_from_evidence_run": PRIOR_EVIDENCE_RUN,
    "recovery_from_artifact_id": PRIOR_ARTIFACT_ID,
    "prior_artifact_fulltext_sha256": PRIOR_FULLTEXT_SHA,
    "pdf_bytes_match_prior_evidence": True
}, indent=2) + "\n", encoding="utf-8")
print("COMMON_V21_RECOVERY_FULLTEXT_SHA", fulltext_sha)
print("COMMON_V21_RECOVERY_PAGES", doc.page_count)

# Start-state delta only. Fresh-read completion counters MUST NOT be advanced here.
delta_date = ts[:10]
reg_rel = f"audit_registry/deep_read_registry_delta_common_v21_{delta_date}.json"
reg = {
    "delta_version": "0.1",
    "date": delta_date,
    "base_registry": "audit_registry/deep_read_registry_v0.1.json",
    "document_updates": {
        SOURCE_ID: {
            "state": "source_pinned_render_complete_pending_independent_fresh_read",
            "official_url": URL,
            "publication": "VDV 301-2-1 V2.1, Common Data Structures and Enumerations",
            "source_pin": {
                "sha256": sha,
                "size_bytes": size,
                "pinned_at_utc": ts,
                "evidence_run": RUN_ID,
                "recovered_from_evidence_run": PRIOR_EVIDENCE_RUN,
                "original_2026_08_31_pin_timestamp_status": "not_recoverable_from_retained_artifact",
                "fresh_retrieval_matches_prior_pdf_bytes": True
            },
            "authority_status": {
                "official_pdf": "official_public_VDV_writing",
                "xsd_lane": "xsd",
                "exact_xsd_authority": "official_VDV-301-2.1_exact_family",
                "official_tag": "VDV-301-2.1",
                "common_blob": COMMON_BLOB,
                "enumerations_blob": ENUMS_BLOB,
                "branch_bytes_match_official_tag": True,
                "latest_xsd_wins": False
            },
            "historical_common_findings_quarantined_until_fresh_read_freeze": True,
            "fresh_read_rule": "derive observations from exact pinned COMMON V2.1 PDF against exact official VDV-301-2.1 Common/Enumerations family before consulting historical Common findings",
            "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
            "render_read_evidence": {
                "run": RUN_ID,
                "artifact_name": "common-v21-recovery-read",
                "prior_evidence_run": PRIOR_EVIDENCE_RUN,
                "prior_artifact_id": PRIOR_ARTIFACT_ID,
                "pdf_page_count": doc.page_count,
                "all_pages_rendered": True,
                "render_dpi": 120,
                "fulltext_sha256": fulltext_sha
            },
            "fresh_read_freeze": "not_started"
        }
    }
}
write_json(reg_rel, reg)

state_rel = "00_START_HERE/CURRENT_STATE.json"
state = load_json(state_rel)
a = state["audit"]
if a.get("deep_read_in_progress") != 0 or a.get("next_natural_deep_read_document_id") != SOURCE_ID:
    raise SystemExit("CURRENT_STATE is not at expected post-COMMON-V2.0 boundary")
state["date"] = delta_date
a["deep_read_in_progress"] = 1
a["deep_read_current_document_id"] = SOURCE_ID
a["deep_read_previous_document_id"] = "COMMON_V2.0"
a["next_natural_deep_read_document_id"] = SOURCE_ID
a["latest_deep_read_registry_delta"] = reg_rel
a["pdf_sources_byte_pinned"] = int(a["pdf_sources_byte_pinned"]) + 1
if SOURCE_ID not in a["pinned_active_sources"]:
    a["pinned_active_sources"].append(SOURCE_ID)
a["common_v2_1_source_pin"] = {
    "sha256": sha,
    "size_bytes": size,
    "evidence_run": RUN_ID,
    "pinned_at_utc": ts,
    "recovered_from_evidence_run": PRIOR_EVIDENCE_RUN,
    "original_2026_08_31_pin_timestamp_status": "not_recoverable_from_retained_artifact",
    "fresh_retrieval_matches_prior_pdf_bytes": True,
    "pdf_authority": "official_public_VDV_writing",
    "xsd_authority_status": "official_VDV-301-2.1_exact_family"
}
a["common_v2_1_authority"] = {
    "official_tag": "VDV-301-2.1",
    "Common_V2.1_blob": COMMON_BLOB,
    "Enumerations_V2.1_blob": ENUMS_BLOB,
    "integration_branch_matches_official_tag": True
}
a["common_v2_1_render_read"] = {
    "run": RUN_ID,
    "artifact_name": "common-v21-recovery-read",
    "prior_evidence_run": PRIOR_EVIDENCE_RUN,
    "pdf_page_count": doc.page_count,
    "all_pages_rendered": True,
    "fulltext_sha256": fulltext_sha,
    "fresh_read_freeze": "not_started"
}
state["evidence"]["latest_pdf_source_pin_run"] = RUN_ID
state["evidence"]["latest_pdf_visual_render_run"] = RUN_ID
state["next_actions"] = [
    "Complete the independent Fresh Read of COMMON V2.1 from the exact pinned full-text/render artifact before reopening historical Common findings.",
    "Visually falsify material table/cardinality/type observations against the exact pinned page renders.",
    "Freeze COMMON V2.1 fresh observations before historical Common reconciliation.",
    "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze."
]
write_json(state_rel, state)

for rel in [pins_rel, reg_rel, state_rel]:
    json.loads((ROOT / rel).read_text(encoding="utf-8"))

print("COMMON_V21_RECOVERY_START_READY", reg_rel)
