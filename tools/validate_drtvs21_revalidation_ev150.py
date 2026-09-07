#!/usr/bin/env python3
"""EV-150: fail-closed revalidation of DRTVS21-001..004.

TicketValidationService V2.1 uses its exact official mixed-version XSD route:
service V2.1 -> Common V1.0 -> Enumerations V1.0. PDF-only editorial findings
remain documentation findings. EV-150 also corrects a stale Deep Read support
statement: the exact V2.1 service XSD operation group does not model either
SubscribeCurrentStopPoint or SubscribeCurrentStop as a local operation member.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from lxml import etree

SOURCE_ID = "TVS_V2.1"
PDF_SHA256 = "676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d"
PDF_SIZE = 752652
ORIGINAL_PIN_EVIDENCE_RUN = "33248946083"
OFFICIAL_URL = "https://www.vdv.de/301-2-16-sds-v2-1-ticketvalidation.pdfx"
LOCAL_FILENAME = "TVS_V2.1.pdf"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "d658d818833bfe7a436f92708ff4ec89402b51b3"
EV112_BLOB = "ac95c53ac1ca1900f51df0b06fe3f0ed623700f5"
XSD_BLOBS = {
    "IBIS-IP_TicketValidationService_V2.1.xsd": "f6497e6469b82ee19b185c4de749d13a7ca60bed",
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
}
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def fail(msg: str) -> None:
    raise AssertionError(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(root: Path, rel: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{rel}"], cwd=root, text=True
    ).strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compact_case(text: str) -> str:
    return re.sub(r"\s+", "", text.replace("\u00ad", ""))


def norm(text: str) -> str:
    return compact_case(text).lower()


def page_count(pdf: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace")
    m = re.search(r"^Pages:\s+(\d+)\s*$", info, flags=re.MULTILINE)
    if not m:
        fail("pdfinfo did not expose a page count")
    count = int(m.group(1))
    if count < 15 or count > 50:
        fail(f"implausible TVS V2.1 PDF page count: {count}")
    return count


def extract_page(pdf: Path, page: int, out_dir: Path) -> tuple[str, str]:
    layout_target = out_dir / f"page-{page:02d}-layout.txt"
    raw_target = out_dir / f"page-{page:02d}-raw.txt"
    subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), str(layout_target)],
        check=True,
    )
    subprocess.run(
        ["pdftotext", "-raw", "-f", str(page), "-l", str(page), str(pdf), str(raw_target)],
        check=True,
    )
    return (
        layout_target.read_text(encoding="utf-8", errors="replace"),
        raw_target.read_text(encoding="utf-8", errors="replace"),
    )


def render_page(pdf: Path, page: int, out_dir: Path) -> Path:
    prefix = out_dir / f"page-{page:02d}"
    subprocess.run(
        [
            "pdftoppm", "-f", str(page), "-l", str(page), "-singlefile",
            "-png", "-r", "180", str(pdf), str(prefix),
        ],
        check=True,
    )
    png = prefix.with_suffix(".png")
    if not png.exists() or png.stat().st_size == 0:
        fail(f"render missing for physical PDF page {page}")
    return png


def combined(pair: tuple[str, str]) -> str:
    return pair[0] + "\n" + pair[1]


def locate_case(texts: dict[int, tuple[str, str]], label: str, *tokens: str) -> int:
    needles = [compact_case(t) for t in tokens]
    hits = []
    for p, pair in texts.items():
        hay = compact_case(combined(pair))
        if all(t in hay for t in needles):
            hits.append(p)
    if len(hits) != 1:
        fail(f"{label}: expected exactly one physical-page hit, got {hits}; tokens={tokens}")
    return hits[0]


def exact_word_pages(texts: dict[int, tuple[str, str]], token: str) -> list[int]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_.]){re.escape(token)}(?![A-Za-z0-9_.])")
    return [p for p, pair in texts.items() if pattern.search(combined(pair))]


def schema_names(tree: etree._ElementTree, kind: str) -> set[str]:
    return {
        x for x in tree.xpath(f"//xs:{kind}/@name", namespaces=NS)
        if isinstance(x, str)
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev150")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_dir = out / "page_text"
    render_dir = out / "renders"
    text_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/TVS_V2.1.md": DEEP_READ_BLOB,
        "tools/validate_tvs_v21_ev112.py": EV112_BLOB,
        **XSD_BLOBS,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        if actual != expected:
            fail(f"canonical authority changed: {rel}: {actual} != {expected}")

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pins = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source = next(x for x in sources["sources"] if x["source_id"] == SOURCE_ID)
    pin = next(x for x in pins["sources"] if x["source_id"] == SOURCE_ID)
    assert source["official_url"] == OFFICIAL_URL
    assert source["local_filename"] == LOCAL_FILENAME
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE
    assert str(pin["evidence_run_id"]) == ORIGINAL_PIN_EVIDENCE_RUN
    assert pin["deep_read_source_ready"] is True

    pdf = root / "local_sources/vdv_pdfs" / LOCAL_FILENAME
    if not pdf.exists():
        fail(f"missing fetched/recovered PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("TVS V2.1 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRTVS21"
    scope = ["DRTVS21-001", "DRTVS21-002", "DRTVS21-003", "DRTVS21-004"]
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    # Exact mixed-version authority route.
    service = etree.parse(str(root / "IBIS-IP_TicketValidationService_V2.1.xsd"))
    common = etree.parse(str(root / "IBIS-IP_common_V1.0.xsd"))
    enums = etree.parse(str(root / "IBIS-IP_Enumerations_V1.0.xsd"))
    includes = service.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    assert includes == ["IBIS-IP_common_V1.0.xsd", "IBIS-IP_Enumerations_V1.0.xsd"]
    etree.XMLSchema(service)

    # DRTVS21-001 exact declaration support; executable compile behaviour is
    # independently rerun by EV-112 in the workflow.
    trip_type = service.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentStopPointDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)", namespaces=NS)
    assert trip_type == "IBIS-IP.NMTOKEN"
    common_types = schema_names(common, "complexType")
    assert "IBIS-IP.NMTOKEN" in common_types
    assert "IBIS-IP.NMToken" not in common_types

    # DRTVS21-002 exact response-type support.
    line_type = service.xpath(
        "string(//xs:complexType[@name='TicketValidationService.GetCurrentLineResponseStructure']"
        "/xs:choice/xs:element[@name='CurrentLineData']/@type)", namespaces=NS)
    assert line_type == "TicketValidationService.CurrentLineDataStructure"
    service_types = schema_names(service, "complexType")
    assert "TicketValidationServiceCurrentLineData" not in service_types

    # Important revalidation correction for DRTVS21-003: contrary to one
    # supporting sentence in the historical Deep Read, the exact V2.1 service
    # XSD operation group/global inventory contains neither local Subscribe name.
    group_names = {
        x.get("name") for x in service.xpath(
            "/xs:schema/xs:group[@name='TicketValidationServiceOperations']//xs:element",
            namespaces=NS) if x.get("name")
    }
    global_names = {
        x.get("name") for x in service.xpath("/xs:schema/xs:element", namespaces=NS)
        if x.get("name")
    }
    for name in [
        "TicketValidationService.SubscribeCurrentStopPoint",
        "TicketValidationService.SubscribeCurrentStop",
    ]:
        assert name not in group_names
        assert name not in global_names

    count = page_count(pdf)
    texts = {p: extract_page(pdf, p, text_dir) for p in range(1, count + 1)}

    # DRTVS21-001: preserve case; lowercasing would erase the actual defect.
    p_nm_token = locate_case(texts, "DRTVS21-001 CurrentTripRef NMToken display", "CurrentTripRef", "IBIS-IP.NMToken")

    # DRTVS21-002: missing service-name separator dot in one response display,
    # while the immediately following structure label shows the separated form.
    p_current_line = locate_case(
        texts,
        "DRTVS21-002 CurrentLineData display",
        "TicketValidationServiceCurrentLineData",
        "TicketValidationService. CurrentLineData",
    )

    # DRTVS21-003: exact-word boundaries separate the editorial short form from
    # the formal ...StopPoint name instead of treating it as a substring hit.
    short_pages = exact_word_pages(texts, "SubscribeCurrentStop")
    formal_pages = exact_word_pages(texts, "SubscribeCurrentStopPoint")
    if len(short_pages) < 2:
        fail(f"DRTVS21-003: expected bilingual SubscribeCurrentStop flow-text hits, got {short_pages}")
    if len(formal_pages) < 2:
        fail(f"DRTVS21-003: expected formal SubscribeCurrentStopPoint hits, got {formal_pages}")
    if set(short_pages) == set(formal_pages):
        fail("DRTVS21-003: short and formal operation-name evidence unexpectedly collapses to same page set")

    # DRTVS21-004: non-executable editorial residue.
    p_unscubscribe = locate_case(texts, "DRTVS21-004 Unscubscribe residue", "Unscubscribe")
    p_caption_typos = locate_case(
        texts,
        "DRTVS21-004 response-caption residue",
        "GetrazziaResponsetData",
        "Error Respone",
    )

    evidence_pages = sorted({
        p_nm_token, p_current_line, p_unscubscribe, p_caption_typos,
        *short_pages, *formal_pages,
    })
    render_hashes = {}
    for p in evidence_pages:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    states = {
        "DRTVS21-001": "executable_confirmed",
        "DRTVS21-002": "context_verified",
        "DRTVS21-003": "context_verified",
        "DRTVS21-004": "context_verified",
    }
    result = {
        "evidence_id": "EV-150",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "source_id": SOURCE_ID,
        "authority": {
            "publication": "VDV 301-2-16 TicketValidationService V2.1",
            "official_url": OFFICIAL_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pdf_page_count": count,
            "original_pin_evidence_run": ORIGINAL_PIN_EVIDENCE_RUN,
            "deep_read_blob": DEEP_READ_BLOB,
            "ev112_blob": EV112_BLOB,
            "xsd_blobs": XSD_BLOBS,
            "exact_include_route": includes,
            "latest_xsd_wins_applicable": False,
        },
        "matched_physical_pages": {
            "DRTVS21-001": p_nm_token,
            "DRTVS21-002": p_current_line,
            "DRTVS21-003": {
                "SubscribeCurrentStop_flow_text_pages": short_pages,
                "SubscribeCurrentStopPoint_formal_pages": formal_pages,
            },
            "DRTVS21-004": {
                "Unscubscribe": p_unscubscribe,
                "response_caption_typos": p_caption_typos,
            },
        },
        "finding_checks": {
            "DRTVS21-001": "PDF prints IBIS-IP.NMToken for CurrentTripRef; exact selected V2.1 authority declares IBIS-IP.NMTOKEN and has no NMToken alias. EV-112 rerun supplies negative compile evidence.",
            "DRTVS21-002": "PDF response display concatenates TicketValidationServiceCurrentLineData while adjacent structure display uses a service separator; exact selected XSD uses TicketValidationService.CurrentLineDataStructure. Structure-suffix omission alone is not treated as the defect.",
            "DRTVS21-003": "Bilingual flow text uses SubscribeCurrentStop while formal PDF operation material uses SubscribeCurrentStopPoint. Exact V2.1 service XSD does not model either local Subscribe name in its operation/global inventory, so the finding rests on same-document formal-vs-flow consistency, not on the stale Deep Read XSD-support sentence.",
            "DRTVS21-004": "Visible PDF prose/captions contain Unscubscribe, GetrazziaResponsetData and Error Respone; these are documentation-only editorial residues.",
        },
        "active_disproof": {
            "DRTVS21-001": "Case-insensitive or alias interpretation rejected by exact XML Schema identifiers and EV-112 negative compile probe.",
            "DRTVS21-002": "A generic shortened-display convention was considered and retained as context: omission of Structure is not classified. The material anomaly is the missing separator between service name and CurrentLineData, supported by adjacent PDF display and exact XSD type spelling.",
            "DRTVS21-003": "Legacy/alternate formal operation-name interpretation is rejected by the same V2.1 PDF's formal overview/detail material. Exact XSD cannot be used as positive operation-name evidence here because neither local Subscribe spelling is represented in its operation/global inventory.",
            "DRTVS21-004": "Executable-identifier interpretation rejected: the strings occur only in prose/table captions and do not define XSD names.",
        },
        "audit_correction": {
            "required": True,
            "subject": "DRTVS21-003 historical Deep Read supporting sentence",
            "stale_statement": "the exact XSD operation group also uses SubscribeCurrentStopPoint",
            "current_exact_evidence": "TicketValidationServiceOperations/global V2.1 inventory contains neither SubscribeCurrentStopPoint nor SubscribeCurrentStop",
            "finding_survives": True,
            "finding_basis_after_correction": "same-document formal operation overview/detail vs bilingual flow text",
        },
        "executable_evidence": {
            "DRTVS21-001": "EV-112 rerun required by workflow",
            "DRTVS21-002": "EV-112 exact-type support; terminal state remains context_verified because the finding is a PDF display typo",
            "DRTVS21-003": "not applicable to terminal state; exact service XSD does not encode either local Subscribe spelling",
            "DRTVS21-004": "not applicable; documentation-only residue",
        },
        "xsd_operation_inventory": {
            "TicketValidationServiceOperations": sorted(group_names),
            "global_elements": sorted(global_names),
            "SubscribeCurrentStopPoint_present": False,
            "SubscribeCurrentStop_present": False,
        },
        "fresh_visual_physical_pages": evidence_pages,
        "fresh_render_hashes": render_hashes,
        "manual_visual_review_status": "pending_human_inspection_of_EV150_artifact_before_registry_closure",
        "text_extraction_modes": ["pdftotext-layout", "pdftotext-raw"],
        "xsd_pool_role": "repository-regression-only",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev150_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-150 DRTVS21 revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
