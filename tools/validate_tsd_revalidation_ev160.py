#!/usr/bin/env python3
"""EV-160: fail-closed revalidation evidence for TSD-001..TSD-004.

This validator does not mutate the audit registry or any XSD. It binds the
current post-TS pre-TSD state to byte-pinned official TrainSet PDFs, the V2.2
General Conventions context, and the exact TrainSetDataService XSD behaviour.
The historical executable checks EV-109, EV-110 and EV-104 are rerun by CI as
independent controls; this script adds the cross-source closure gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from lxml import etree

ROOT_XSD_COUNT = 50
SOURCE_RUN = 34816735900
SOURCE_JOB = 103888867262
SOURCE_ARTIFACT = 10336466475
SOURCE_DIGEST = "sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb"
SOURCE_HEAD = "20785d8ee41e812a5902d49b6d4b800ef238e311"

PDFS = {
    "v21": {
        "sha256": "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e",
        "bytes": 1708401,
        "pages": 51,
        "full_text_sha256": "81a051867f271b03c841b0d1d391dfd07209c13c73789cf5f8a8af79987ee13c",
        "page_hashes": {
            33: "626312405c372133d40214e6cd3c88f0ca7ef6ec3b54a0e10bbb1e2bff93739c",
            34: "4f90cd0d70dd79e55476e292db5b7d5fadbf92221a3be7a0f077ecb1c06b6224",
        },
    },
    "v22": {
        "sha256": "c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e",
        "bytes": 1744296,
        "pages": 54,
        "full_text_sha256": "a4480d9a425c55ca3e488136d64c5c367e924144dd53dadd677f7a5ae4711882",
        "page_hashes": {
            34: "d33b66d6f00e9d1978d00ff1dfc481b463778796b7a0b8167e6be4a9ac6f5a34",
            35: "1b22492a513a96c47b8985d46863d5313d0b9c12ff4fd84761950946841963b4",
            38: "10e7b34120df8f572cf1492224708017d65c1b4bc934bed331e98dbb073bbe62",
            40: "8d320577148343ef3161af15f36f02d9d2dddb822b887f4450bf7541462ef2d2",
        },
    },
    "gc22": {
        "sha256": "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051",
        "bytes": 1562305,
        "pages": 79,
        "full_text_sha256": "79f27be364a478f1e8899ee64035dc54e78efcf29d0455953ffaa2066f647195",
        "page_hashes": {
            47: "51230dfe6c6078f7d94be04bfde39f7c4e0fa40224c06f62a347548ca11f066d",
            48: "c894c4b88d2f9584a9b38061f9de5a906c5be8621e32b9c37113fa0e65345097",
            49: "cc37bec8b07fc2307b2abff9e4bf7942f6b2f92c46516b55a1b134c157eb782a",
        },
    },
}

TARGET_STATES = {
    "TSD-001": "executable_confirmed",
    "TSD-002": "executable_confirmed",
    "TSD-003": "contextual_not_defect",
    "TSD-004": "context_verified",
}

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"OK  {message}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pdftotext(pdf: Path, page: int | None = None) -> str:
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        cmd = ["pdftotext", "-layout"]
        if page is not None:
            cmd += ["-f", str(page), "-l", str(page)]
        cmd += [str(pdf), tmp.name]
        subprocess.run(cmd, check=True)
        return Path(tmp.name).read_text(encoding="utf-8")


def pdf_pages(pdf: Path) -> int:
    proc = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True)
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    fail(f"pdfinfo did not return Pages for {pdf}")
    return -1


def check_pdf(label: str, pdf: Path, spec: dict) -> dict[int, str]:
    require(pdf.is_file(), f"{label} PDF exists")
    require(sha256(pdf) == spec["sha256"], f"{label} PDF SHA-256 is exact")
    require(pdf.stat().st_size == spec["bytes"], f"{label} PDF byte count is exact")
    require(pdf_pages(pdf) == spec["pages"], f"{label} PDF page count is exact")
    full = pdftotext(pdf)
    require(text_sha256(full) == spec["full_text_sha256"], f"{label} layout-text fingerprint is exact")
    page_texts: dict[int, str] = {}
    for page, expected in spec["page_hashes"].items():
        text = pdftotext(pdf, page)
        require(text_sha256(text) == expected, f"{label} physical page {page} fingerprint is exact")
        page_texts[page] = text
    return page_texts


def collect_findings(value) -> list[dict]:
    out: list[dict] = []
    if isinstance(value, dict):
        if {"finding_id", "revalidation_state", "terminal_state_source"} <= set(value):
            out.append(value)
        for child in value.values():
            out.extend(collect_findings(child))
    elif isinstance(value, list):
        for child in value:
            out.extend(collect_findings(child))
    return out


def assert_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{label} contains required semantic tokens" + (f"; missing={missing}" if missing else ""))


def element_maps(path: Path, group_name: str) -> tuple[dict[str, str | None], dict[str, str | None]]:
    tree = etree.parse(str(path))
    etree.XMLSchema(tree)
    globals_ = {
        node.get("name"): node.get("type")
        for node in tree.xpath("/xs:schema/xs:element", namespaces=NS)
    }
    group = {
        node.get("name"): node.get("type")
        for node in tree.xpath(
            f"/xs:schema/xs:group[@name='{group_name}']//xs:element",
            namespaces=NS,
        )
    }
    return globals_, group


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--source-evidence-dir", type=Path, required=True)
    ap.add_argument("--v21-pdf", type=Path, required=True)
    ap.add_argument("--v22-pdf", type=Path, required=True)
    ap.add_argument("--general-pdf", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    root = args.repo_root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    state = json.loads((root / "00_START_HERE/CURRENT_STATE.json").read_text(encoding="utf-8"))
    registry = json.loads((root / "audit_registry/finding_revalidation_registry_v0.1.json").read_text(encoding="utf-8"))
    audit = state["audit"]

    require(state["canonical_branch"] == "dev/schema-integration", "canonical branch is dev/schema-integration")
    require(audit["finding_inventory_count"] == 192, "frozen finding inventory count is 192")
    require(audit["finding_revalidation_completed_findings"] == 157, "prestate terminal count is 157")
    require(audit["finding_revalidation_pending_findings"] == 35, "prestate pending count is 35")
    require(audit["finding_revalidation_next_block"] == "TSD", "prestate next block is TSD")
    require(audit["finding_revalidation_latest_completed_block"] == "TS", "latest completed block is TS")
    require(audit["latest_executable_evidence_id"] == "EV-159", "latest executable evidence before TSD is EV-159")
    require(registry["next_revalidation_block"] == "TSD", "registry next block is TSD")

    findings = collect_findings(registry)
    by_id: dict[str, dict] = {}
    for item in findings:
        fid = item["finding_id"]
        require(fid not in by_id, f"finding {fid} occurs once in ordered registry")
        by_id[fid] = item
    require(len(by_id) == 192, "registry contains exactly 192 ordered finding states")
    pending = [item["finding_id"] for item in findings if item["revalidation_state"] == "pending"]
    require(len(pending) == 35, "registry contains exactly 35 pending findings")
    require(pending[0] == "TSD-001", "first pending finding is TSD-001")
    for fid in TARGET_STATES:
        require(by_id[fid]["revalidation_state"] == "pending", f"{fid} is still pending before EV-160 closure")
        require(by_id[fid]["terminal_state_source"] is None, f"{fid} has no premature terminal source")

    projected = [(item["finding_id"], TARGET_STATES.get(item["finding_id"], item["revalidation_state"])) for item in findings]
    projected_pending = [fid for fid, status in projected if status == "pending"]
    require(len(projected_pending) == 31, "projected post-TSD pending count is dynamically 31")
    require(192 - len(projected_pending) == 161, "projected post-TSD terminal count is dynamically 161")
    require(projected_pending[0] == "TSI-001", "projected next finding is TSI-001")

    require(audit["trainset_v2_1_source_pin"]["sha256"] == PDFS["v21"]["sha256"], "CURRENT_STATE V2.1 TrainSet source pin matches EV-160")
    require(audit["trainset_v2_1_source_pin"]["size_bytes"] == PDFS["v21"]["bytes"], "CURRENT_STATE V2.1 TrainSet size pin matches EV-160")
    require(audit["trainset_v2_2_source_pin"]["sha256"] == PDFS["v22"]["sha256"], "CURRENT_STATE V2.2 TrainSet source pin matches EV-160")
    require(audit["trainset_v2_2_source_pin"]["size_bytes"] == PDFS["v22"]["bytes"], "CURRENT_STATE V2.2 TrainSet size pin matches EV-160")

    source_manifest = json.loads((args.source_evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    require(source_manifest["evidence"] == "EV-160 source acquisition", "source artifact identifies EV-160 acquisition")
    require(source_manifest["head_sha"] == SOURCE_HEAD, "source artifact head SHA is exact")
    require(source_manifest["prestate"] == {"terminal": 157, "pending": 35, "first_pending": "TSD-001", "next_block": "TSD"}, "source artifact prestate is exact")
    require(source_manifest["xsd_mutated"] is False, "source artifact records no XSD mutation")
    require(source_manifest["audit_state_mutated"] is False, "source artifact records no audit-state mutation")
    for source_key, spec_key in (("TRAINSET_V2.1", "v21"), ("TRAINSET_V2.2", "v22")):
        src = source_manifest["sources"][source_key]
        spec = PDFS[spec_key]
        require(src["pdf_sha256"] == spec["sha256"], f"source artifact {source_key} PDF hash is exact")
        require(src["pdf_bytes"] == spec["bytes"], f"source artifact {source_key} byte count is exact")
        require(src["pages"] == spec["pages"], f"source artifact {source_key} page count is exact")
        require(src["full_text_sha256"] == spec["full_text_sha256"], f"source artifact {source_key} text fingerprint is exact")
    require(sha256(args.source_evidence_dir / "pdfs/TRAINSET_V2.1.pdf") == PDFS["v21"]["sha256"], "source artifact embeds exact V2.1 PDF")
    require(sha256(args.source_evidence_dir / "pdfs/TRAINSET_V2.2.pdf") == PDFS["v22"]["sha256"], "source artifact embeds exact V2.2 PDF")

    v21_pages = check_pdf("TrainSet V2.1", args.v21_pdf, PDFS["v21"])
    v22_pages = check_pdf("TrainSet V2.2", args.v22_pdf, PDFS["v22"])
    gc_pages = check_pdf("General Conventions V2.2", args.general_pdf, PDFS["gc22"])

    assert_tokens(v21_pages[33], [
        "triple of operations for each requested dataset: RetrieveX, SubscribeX and",
        "UnsubscribeX.", "SubscribeTripRef", "UnsubscribeTripRef", "SubscribeResponseStructure",
    ], "TSD-001 V2.1 page 33")
    assert_tokens(v21_pages[34], ["SubscribeTripInformation", "UnsubscribeTripInformation", "SubscribeResponseStructure"], "TSD-001 V2.1 page 34")

    v21_xsd = root / "IBIS-IP_TrainSetDataService_V2.1.xsd"
    v21_globals, v21_group = element_maps(v21_xsd, "TrainSetDataServiceOperations")
    retrieve_v21 = {
        "TrainSetDataService.RetrieveTripRefRequest",
        "TrainSetDataService.RetrieveTripRefResponse",
        "TrainSetDataService.RetrieveTripInformationRequest",
        "TrainSetDataService.RetrieveTripInformationResponse",
    }
    subscription_v21 = {
        "TrainSetDataService.SubscribeTripRefRequest", "TrainSetDataService.SubscribeTripRefResponse",
        "TrainSetDataService.UnsubscribeTripRefRequest", "TrainSetDataService.UnsubscribeTripRefResponse",
        "TrainSetDataService.SubscribeTripInformationRequest", "TrainSetDataService.SubscribeTripInformationResponse",
        "TrainSetDataService.UnsubscribeTripInformationRequest", "TrainSetDataService.UnsubscribeTripInformationResponse",
    }
    require(retrieve_v21 <= set(v21_globals) and retrieve_v21 <= set(v21_group), "TSD-001 V2.1 XSD contains all Retrieve roots and operation-group members")
    require(not (subscription_v21 & set(v21_globals)) and not (subscription_v21 & set(v21_group)), "TSD-001 V2.1 XSD omits service-specific Subscribe/Unsubscribe roots and operation members")
    common20 = etree.parse(str(root / "IBIS-IP_common_V2.0.xsd"))
    common_types = {node.get("name") for node in common20.xpath("/xs:schema/xs:complexType", namespaces=NS)}
    require({"SubscribeRequestStructure", "SubscribeResponseStructure", "UnsubscribeRequestStructure", "UnsubscribeResponseStructure"} <= common_types, "TSD-001 generic V2.0 subscription infrastructure exists")

    assert_tokens(v22_pages[34], ["UnsubscribeTripRef", "TrainSetDataService.RetrieveTripRefRequestStructure", "UnsubscribeResponseStructure"], "TSD-002 V2.2 page 34 overview")
    assert_tokens(v22_pages[35], ["UnsubscribeTripInformation", "TrainSetDataService.RetrieveTripInformationRequestStructure", "Specific TrainSetUnsubscribeRequestStructure", "Client-IP-Address", "CoachNumber"], "TSD-002 V2.2 page 35 overview/detail")

    v22_xsd = root / "IBIS-IP_TrainSetDataService_V2.2.xsd"
    v22_globals, v22_group = element_maps(v22_xsd, "TrainSetDataServiceOperations")
    require(v22_group.get("TrainSetDataService.UnsubscribeTripRefRequest") == "TrainSetDataService.TrainSetUnsubscribeRequestStructure", "TSD-002 XSD TripRef Unsubscribe uses special request structure")
    require(v22_group.get("TrainSetDataService.UnsubscribeTripInformationRequest") == "TrainSetDataService.TrainSetUnsubscribeRequestStructure", "TSD-002 XSD TripInformation Unsubscribe uses special request structure")

    assert_tokens(gc_pages[47], ["Such subscriptions to", "data are not meaningful, and are thus not planned.", "Retrieve"], "TSD-003 General Conventions page 47")
    assert_tokens(gc_pages[48], ["Conventions for Get/Subscribe/Unsubscribe", "Subscribe and/or Unsubscribe operation exists", "Get operation"], "TSD-003 General Conventions page 48")
    assert_tokens(gc_pages[49], ["For this reason, subscriptions can be set up as well.", "Retrieve operations do not refer to currently valid data"], "TSD-003 General Conventions page 49")
    assert_tokens(v22_pages[34], ["In addition to the existing IBIS-IP concept", "subscription", "parameter related Retrieve operations"], "TSD-003 TrainSet service-specific extension context")
    require(v22_group.get("TrainSetDataService.SubscribeTripRefResponse") == "SubscribeResponseStructure", "TSD-003 operation group TripRef response is immediate Subscribe acknowledgement")
    require(v22_group.get("TrainSetDataService.SubscribeTripInformationResponse") == "SubscribeResponseStructure", "TSD-003 operation group TripInformation response is immediate Subscribe acknowledgement")
    require(v22_globals.get("TrainSetDataService.SubscribeTripRefResponse") == "TrainSetDataService.RetrieveTripRefResponseStructure", "TSD-003 global TripRef subscription event uses Retrieve response structure")
    require(v22_globals.get("TrainSetDataService.SubscribeTripInformationResponse") == "TrainSetDataService.RetrieveTripInformationResponseStructure", "TSD-003 global TripInformation subscription event uses Retrieve response structure")
    assert_tokens(v22_pages[38], ["SubscribeResponseStructure", "event based updates via the RetrieveTripRefResponseStructure"], "TSD-003 V2.2 page 38 acknowledgement/event split")

    assert_tokens(v22_pages[40], ["Operation SubscribeTripInformation", "SubscribeResponseStructure", "event based updates via the RetrieveTripRefResponseStructure", "TrainSetUnsubscribeRequestStructure"], "TSD-004 V2.2 page 40 visible mismatch")
    require(v22_globals.get("TrainSetDataService.SubscribeTripInformationResponse") == "TrainSetDataService.RetrieveTripInformationResponseStructure", "TSD-004 XSD uses RetrieveTripInformationResponseStructure for TripInformation event root")
    require(v22_globals.get("TrainSetDataService.SubscribeTripRefResponse") == "TrainSetDataService.RetrieveTripRefResponseStructure", "TSD-004 TripRef parallel is internally consistent")

    manifest = {
        "evidence_id": "EV-160",
        "scope": ["TSD-001", "TSD-002", "TSD-003", "TSD-004"],
        "source_acquisition": {
            "run_id": SOURCE_RUN,
            "job_id": SOURCE_JOB,
            "artifact_id": SOURCE_ARTIFACT,
            "artifact_digest": SOURCE_DIGEST,
            "head_sha": SOURCE_HEAD,
        },
        "prestate": {"terminal": 157, "pending": 35, "first_pending": "TSD-001", "next_block": "TSD", "latest_evidence": "EV-159"},
        "target_states": TARGET_STATES,
        "projected_poststate": {"terminal": 161, "pending": 31, "first_pending": "TSI-001", "next_block": "TSI"},
        "sources": {
            "TRAINSET_V2.1": PDFS["v21"],
            "TRAINSET_V2.2": PDFS["v22"],
            "VDV301-2_GC_V2.2": PDFS["gc22"],
        },
        "controls": ["EV-109", "EV-110", "EV-104", "50-root-XSD regression pool"],
        "xsd_mutation": False,
        "audit_state_mutation": False,
        "closure_authorized_only_after_ci_success": True,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASSED: EV-160 TSD revalidation gate; projected 161/192 terminal, 31 pending, next TSI-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
