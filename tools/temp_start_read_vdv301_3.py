#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, os, urllib.request
from datetime import datetime, timezone
import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "VDV301-3_02-2020"
URL = "https://www.vdv.de/301-3-sdes-network-infrastructure.pdfx"
RUN_ID = os.environ["GITHUB_RUN_ID"]

def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def write_json(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

req = urllib.request.Request(URL, headers={"User-Agent":"VDV301-audit-source-pin/1.0"})
with urllib.request.urlopen(req, timeout=90) as response:
    data = response.read()
if not data.startswith(b"%PDF-"):
    raise SystemExit("VDV301-3 source is not a PDF")
sha = hashlib.sha256(data).hexdigest()
size = len(data)
ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
print("VDV301_3_PIN", sha, size, ts, "RUN", RUN_ID)

pins_rel = "audit_registry/pdf_source_pins_v0.1.json"
pins = load_json(pins_rel)
if any(x.get("source_id") == SOURCE_ID for x in pins["sources"]):
    raise SystemExit("VDV301-3_02-2020 is already pinned")
pins["sources"].append({"source_id":SOURCE_ID,"expected_sha256":sha,"expected_size_bytes":size,"pinned_at_utc":ts,"deep_read_source_ready":True,"evidence_run_id":RUN_ID})
write_json(pins_rel, pins)

out = ROOT / "audit-results" / "vdv301-3-02-2020-pinned-read"
pages_dir = out / "pages"
pages_dir.mkdir(parents=True, exist_ok=True)
doc = fitz.open(stream=data, filetype="pdf")
if doc.page_count != 37:
    raise SystemExit(f"Unexpected VDV301-3 page count: {doc.page_count}, expected 37")
texts=[]; page_hashes={}; matrix=fitz.Matrix(120/72,120/72)
for i,page in enumerate(doc):
    texts.append(f"===== PAGE {i+1} =====\n" + page.get_text("text"))
    pix=page.get_pixmap(matrix=matrix,alpha=False)
    p=pages_dir/f"page_{i+1:03d}.png"; pix.save(p)
    page_hashes[str(i+1)]=hashlib.sha256(p.read_bytes()).hexdigest()
fulltext="\n".join(texts)
fulltext_sha=hashlib.sha256(fulltext.encode("utf-8")).hexdigest()
(out/"fulltext.txt").write_text(fulltext,encoding="utf-8")
(out/"manifest.json").write_text(json.dumps({"source_id":SOURCE_ID,"official_url":URL,"pdf_sha256":sha,"pdf_size_bytes":size,"page_count":doc.page_count,"render_dpi":120,"fulltext_sha256":fulltext_sha,"page_png_sha256":page_hashes,"run":RUN_ID},indent=2)+"\n",encoding="utf-8")
print("NETWORK_FULLTEXT_SHA",fulltext_sha); print("NETWORK_PAGES",doc.page_count)

delta_rel="audit_registry/deep_read_registry_delta_vdv301_3_02_2020_2026-08-29.json"
delta={"delta_version":"0.1","date":"2026-08-29","base_registry":"audit_registry/deep_read_registry_v0.1.json","document_updates":{SOURCE_ID:{"state":"source_pinned_render_complete_pending_independent_fresh_read","official_url":URL,"publication":"VDV-Schrift 301-3, Netzwerkinfrastruktur / Network infrastructure, 02/2020","source_pin":{"sha256":sha,"size_bytes":size,"pinned_at_utc":ts,"evidence_run":RUN_ID},"authority_status":{"official_pdf":"official_public_VDV_writing","xsd_lane":"network_protocol","xsd_required":False,"validation_lane":"physical_network_protocol_profile","latest_external_protocol_version_wins":False},"historical_network_findings_quarantined_until_fresh_read_freeze":True,"fresh_read_rule":"derive network/topology/physical-interface observations from the pinned official VDV301-3 source before consulting historical network/discovery findings or RV-002 results","evidence_gate":"docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md","render_read_evidence":{"run":RUN_ID,"artifact_name":"vdv301-3-02-2020-pinned-read","pdf_page_count":doc.page_count,"all_pages_rendered":True,"render_dpi":120,"fulltext_sha256":fulltext_sha}}}}
write_json(delta_rel,delta)

state_rel="00_START_HERE/CURRENT_STATE.json"; state=load_json(state_rel); a=state["audit"]
a["deep_read_in_progress"]=1; a["deep_read_current_document_id"]=SOURCE_ID; a["deep_read_previous_document_id"]="ARA_V2.4"; a["next_natural_deep_read_document_id"]=SOURCE_ID
a["pdf_sources_byte_pinned"]=26
if SOURCE_ID not in a["pinned_active_sources"]: a["pinned_active_sources"].append(SOURCE_ID)
a["latest_deep_read_registry_delta"]=delta_rel
a["network_vdv301_3_source_pin"]={"sha256":sha,"size_bytes":size,"evidence_run":RUN_ID,"pinned_at_utc":ts,"pdf_authority":"official_public_VDV_writing","validation_lane":"physical_network_protocol_profile"}
a["network_vdv301_3_render_read"]={"run":RUN_ID,"artifact_name":"vdv301-3-02-2020-pinned-read","pdf_page_count":doc.page_count,"all_pages_rendered":True,"fulltext_sha256":fulltext_sha}
state["evidence"]["latest_pdf_source_pin_run"]=RUN_ID; state["evidence"]["latest_pdf_visual_render_run"]=RUN_ID
state["next_actions"]=["Complete the independent Fresh Read of VDV301-3_02-2020 from the exact pinned render/text artifact.","Visually falsify material network/topology/connector/switching claims against the pinned page renders.","Freeze fresh observations before reopening historical network/discovery findings or RV-002 comparison.","Keep VDV network requirements, incorporated external standards and diagnostic heuristics as separate authority classes.","After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze."]
write_json(state_rel,state)
for rel in [pins_rel,delta_rel,state_rel]: json.loads((ROOT/rel).read_text(encoding="utf-8"))
Path(__file__).unlink()
print("VDV301_3_START_READ_READY")
