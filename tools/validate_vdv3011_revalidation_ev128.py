#!/usr/bin/env python3
"""EV-128: fail-closed revalidation of DR3011-001..DR3011-003.

The three findings are documentation/context findings.  The checker verifies the
exact byte-pinned Part 1 and Part 2 V1.0 PDFs, binds the relevant Part 1 pages to
the previously rendered visual artifact, and cross-checks the historical
SystemManagementService XSD terminology without changing validation behavior.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from lxml import etree

SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
VISUAL_RECORD = Path("audit_registry/vdv3011_visual_revalidation_evidence_2026-09-03.json")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
SOURCE_IDS = ("VDV301-1_V1.0_DE", "VDV301-2_V1.0_DE")
EXPECTED_VISUAL = {
    2: "273f40033887eb7adcb0baf81650dcdc207550c987b80b00e99d645951c5664c",
    10: "5a26585cca263b2749e023f2f52c0bcc25d93a4cf88a9abcff31ff96889314ac",
    11: "16fe0129866d3ca79ea64f047354fd2ea90c824e18e06332581e5b3d547d4bef",
    34: "c61689499c594d47cd99cc7b61de57b4f0183b20ca9c33ee508ab411bc7a709b",
}
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def record(data: dict, source_id: str) -> dict:
    matches = [item for item in data.get("sources", []) if item.get("source_id") == source_id]
    require(len(matches) == 1, f"{source_id}: expected one registry record, found {len(matches)}")
    return matches[0]


def fetch(url: str, attempts: int = 5, timeout: int = 90) -> bytes:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VDV301-audit-EV128/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except (OSError, urllib.error.URLError) as exc:
            last = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise RuntimeError(f"unable to fetch {url}: {last}")


def fetch_pinned(tmp: Path) -> dict[str, Path]:
    sources = load(SOURCE_REGISTRY)
    pins = load(PIN_REGISTRY)
    out: dict[str, Path] = {}
    for source_id in SOURCE_IDS:
        src = record(sources, source_id)
        pin = record(pins, source_id)
        require(pin.get("deep_read_source_ready") is True, f"{source_id}: not source-ready")
        data = fetch(str(src["official_url"]))
        sha = hashlib.sha256(data).hexdigest()
        size = len(data)
        require(data.startswith(b"%PDF-"), f"{source_id}: response is not PDF")
        require(sha == pin.get("expected_sha256"), f"{source_id}: SHA changed: {sha}")
        require(size == pin.get("expected_size_bytes"), f"{source_id}: size changed: {size}")
        path = tmp / f"{source_id}.pdf"
        path.write_bytes(data)
        out[source_id] = path
        print(f"PIN_OK {source_id} sha256={sha} size={size}")
    return out


def page_text(pdf: Path, page: int) -> str:
    proc = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.stdout


def full_text(pdf: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.stdout


def compact_alnum(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", text)


def visual_page(visual: dict, page: int) -> dict:
    matches = [item for item in visual.get("reviewed_pages", []) if item.get("page") == page]
    require(len(matches) == 1, f"visual page {page}: expected one record")
    item = matches[0]
    require(item.get("png_sha256") == EXPECTED_VISUAL[page], f"visual page {page}: PNG hash changed")
    return item


def has_observation(item: dict, phrase: str) -> bool:
    return any(phrase in str(obs) for obs in item.get("observations", []))


def main() -> int:
    require(shutil.which("pdftotext") is not None, "EV-128 requires pdftotext")
    visual = load(VISUAL_RECORD)
    require(visual.get("pdf_sha256") == "5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2", "Part 1 visual source SHA changed")
    require(visual.get("render_run_id") == "33725750019", "Part 1 visual render run changed")
    require(visual.get("render_artifact_id") == "9881897572", "Part 1 visual artifact changed")
    require(visual.get("render_artifact_digest") == "sha256:b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510", "Part 1 visual artifact digest changed")
    for page in EXPECTED_VISUAL:
        visual_page(visual, page)

    require(SYSTEM_MGMT_XSD.is_file(), f"missing {SYSTEM_MGMT_XSD}")
    tree = etree.parse(str(SYSTEM_MGMT_XSD))
    etree.XMLSchema(tree)
    root = tree.getroot()
    group_names = set(root.xpath("./xs:group[@name='SystemManagementServiceGroup']/xs:sequence/xs:element/@name", namespaces=NS))
    global_names = set(root.xpath("./xs:element/@name", namespaces=NS))
    require("SystemManagementService.GetDeviceStatusResponse" in group_names | global_names, "SystemManagement XSD lacks GetDeviceStatus response terminology")
    require("SystemManagementService.GetServiceStatusResponse" in group_names | global_names, "SystemManagement XSD lacks GetServiceStatus response terminology")
    require(not any("GetDeviceState" in name for name in group_names | global_names), "SystemManagement XSD unexpectedly exposes GetDeviceState alias")
    require(not any("GetSystemStatus" in name for name in group_names | global_names), "SystemManagement XSD unexpectedly exposes GetSystemStatus alias")
    print("XSD_CONTEXT_OK SystemManagement V1.0 uses DeviceStatus/ServiceStatus response terminology without State/SystemStatus aliases")

    with tempfile.TemporaryDirectory(prefix="vdv301-ev128-") as tmp_name:
        pdfs = fetch_pinned(Path(tmp_name))
        p1 = pdfs["VDV301-1_V1.0_DE"]
        p2 = pdfs["VDV301-2_V1.0_DE"]

        # DR3011-001: section identity and erroneous reference are both visible.
        toc = compact_alnum(page_text(p1, 2))
        example = compact_alnum(page_text(p1, 10))
        require("512SystemDokumentation" in toc and "513SystemManagement" in toc, "DR3011-001: TOC section identities missing")
        require("SystemManagementService" in example and "SystemManagement" in example and "vgl512" in example, "DR3011-001: wrong 5.1.2 example reference missing")
        v2 = visual_page(visual, 2)
        v10 = visual_page(visual, 10)
        require(has_observation(v2, "5.1.2") and has_observation(v2, "5.1.3"), "DR3011-001: visual TOC observation missing")
        require(has_observation(v10, "5.1.2"), "DR3011-001: visual wrong-reference observation missing")
        print("OK DR3011-001 wrong 5.1.2 System-Management cross-reference confirmed")

        # DR3011-002: Part 1 architecture example uses stale/conceptual names;
        # official Part 2 V1.0 and selected historical XSD use final status names.
        architecture = compact_alnum(page_text(p1, 11))
        for token in ("GetDeviceState", "GetSystemStatus", "SubscribeDeviceStatus", "SubscribeSystemStatus", "UnsubscribeDeviceStatus", "UnsubscribeSystemStatus"):
            require(token in architecture, f"DR3011-002: Part 1 example missing {token}")
        part2 = compact_alnum(full_text(p2))
        for token in ("GetDeviceStatus", "GetServiceStatus", "SubscribeServiceStatus", "UnsubscribeServiceStatus"):
            require(token in part2, f"DR3011-002: official Part 2 V1.0 missing {token}")
        v11 = visual_page(visual, 11)
        require(has_observation(v11, "GetDeviceState") and has_observation(v11, "GetSystemStatus"), "DR3011-002: visual stale Get names missing")
        require(has_observation(v11, "SubscribeSystemStatus"), "DR3011-002: visual SystemStatus subscription name missing")
        print("OK DR3011-002 stale/conceptual Part 1 operation terminology confirmed against official Part 2 V1.0 and selected XSD")

        # DR3011-003: visible duplicate abbreviation rows; no semantic impact.
        abbreviations = compact_alnum(page_text(p1, 34))
        require(abbreviations.count("IBISIP") >= 2, "DR3011-003: duplicate IBIS-IP abbreviation entries not present in page text")
        v34 = visual_page(visual, 34)
        require(has_observation(v34, "two consecutive IBIS-IP rows"), "DR3011-003: visual duplicate-row observation missing")
        print("OK DR3011-003 duplicate IBIS-IP abbreviation rows confirmed")

    result = {
        "evidence_id": "EV-128",
        "finding_block": ["DR3011-001", "DR3011-002", "DR3011-003"],
        "result": "PASS",
        "terminal_revalidation_recommendations": {
            "DR3011-001": "context_verified",
            "DR3011-002": "context_verified",
            "DR3011-003": "context_verified"
        },
        "validation_behavior": "none; documentation/context findings only",
        "sdk_rule_effect": "none; do not invent Part 1 stale operation aliases",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASSED: EV-128 DR3011-001..003 revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
