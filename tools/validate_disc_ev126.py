#!/usr/bin/env python3
"""EV-126: revalidate DISC-001..003 against exact official VDV PDFs and RFC Editor sources.

This is deliberately a non-XSD evidence lane. It proves documentation/discovery
context only and must not mutate or infer any XML schema contract.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

SOURCES = {
    "VDV301-2_V1.0_DE": {
        "url": "https://www.vdv.de/301-2sds-v1-0.pdfx",
        "sha256": "2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75",
        "size": 1790447,
        "pages": 86,
    },
    "VDV301-2_BASE_V2.0": {
        "url": "https://www.vdv.de/301-2-sds-v-2-0.pdfx",
        "sha256": "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37",
        "size": 2374295,
        "pages": 115,
    },
    "VDV301-2_BASE_V2.1": {
        "url": "https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx",
        "sha256": "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a",
        "size": 2671005,
        "pages": 130,
    },
    "VDV301-2_GC_V2.2": {
        "url": "https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx",
        "sha256": "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051",
        "size": 1562305,
        "pages": 79,
    },
    "VDV301-2_GC_V2.3": {
        "url": "https://www.vdv.de/301-2-sdes-v2-3-common-conventions.pdfx",
        "sha256": "4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603",
        "size": 1057483,
        "pages": 80,
    },
    "VDV301-2_GC_V2.4": {
        "url": "https://www.vdv.de/301-2-sde-v2.4-common-conventions.pdfx",
        "sha256": "048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d",
        "size": 1767094,
        "pages": 84,
    },
}

RFC_URLS = {
    "2927": "https://www.rfc-editor.org/rfc/rfc2927.txt",
    "3927": "https://www.rfc-editor.org/rfc/rfc3927.txt",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "VDV301-audit-EV126/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def page_text(pdf: Path, page: int) -> str:
    proc = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return " ".join(proc.stdout.split())


def require(text: str, *needles: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(f"Missing expected text: {missing!r}")


def forbid(text: str, *needles: str) -> None:
    present = [needle for needle in needles if needle in text]
    if present:
        raise AssertionError(f"Unexpected text present: {present!r}")


def main() -> None:
    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        raise SystemExit("EV-126 requires poppler-utils (pdftotext + pdfinfo)")

    with tempfile.TemporaryDirectory(prefix="vdv301-ev126-") as tmp:
        root = Path(tmp)
        pdfs: dict[str, Path] = {}

        for sid, meta in SOURCES.items():
            data = fetch(meta["url"])
            digest = hashlib.sha256(data).hexdigest()
            if digest != meta["sha256"]:
                raise AssertionError(f"{sid}: SHA-256 changed: {digest}")
            if len(data) != meta["size"]:
                raise AssertionError(f"{sid}: size changed: {len(data)}")
            pdf = root / f"{sid}.pdf"
            pdf.write_bytes(data)
            info = subprocess.run(
                ["pdfinfo", str(pdf)], check=True, stdout=subprocess.PIPE, text=True
            ).stdout
            pages = None
            for line in info.splitlines():
                if line.startswith("Pages:"):
                    pages = int(line.split(":", 1)[1].strip())
                    break
            if pages != meta["pages"]:
                raise AssertionError(f"{sid}: page count changed: {pages}")
            pdfs[sid] = pdf
            print(f"PIN_OK {sid} sha256={digest} size={len(data)} pages={pages}")

        # DISC-002 historical root: V1.0 itself cites RFC 2927 for link-local addressing,
        # while its bibliography identifies RFC 2927 as the LDAP-schema MIME profile.
        v10_ip = page_text(pdfs["VDV301-2_V1.0_DE"], 20)
        require(v10_ip, "Zero Conf", "RFC 2927", "169.254.xxx.xxx")
        v10_refs = page_text(pdfs["VDV301-2_V1.0_DE"], 80)
        require(v10_refs, "RFC 2927", "MIME Directory Profile for LDAP Schema")

        # V2.0/V2.1: same page contains German RFC 3927 and English RFC 2927.
        for sid, page in (("VDV301-2_BASE_V2.0", 21), ("VDV301-2_BASE_V2.1", 22)):
            text = page_text(pdfs[sid], page)
            require(text, "RFC 3927", "RFC 2927", "169.254.xxx.xxx", "Zero Conf")

        # DISC-001 strongest disproof: V2.2+ language tracks are materially different,
        # not merely a translated RFC-number typo.
        for sid, de_page, en_page in (
            ("VDV301-2_GC_V2.2", 17, 20),
            ("VDV301-2_GC_V2.3", 17, 20),
            ("VDV301-2_GC_V2.4", 20, 23),
        ):
            de = page_text(pdfs[sid], de_page)
            en = page_text(pdfs[sid], en_page)
            require(de, "IP-Adressvergabe", "existieren nicht", "DHCP")
            forbid(de, "RFC 2927", "169.254.xxx.xxx", "Zero Conf")
            require(en, "Zero Conf", "RFC 2927", "169.254.xxx.xxx", "DHCP")

        # DISC-003 strongest disproof: the V2.4 history note corresponds to a real
        # German Table-3 expansion compared with V2.3, not merely a history typo.
        v23_table = page_text(pdfs["VDV301-2_GC_V2.3"], 27)
        require(v23_table, "Tabelle 3", "sntp-server")
        forbid(v23_table, "coachnumber", "deviceclass", "deviceID")

        v24_table = " ".join(
            [
                page_text(pdfs["VDV301-2_GC_V2.4"], 30),
                page_text(pdfs["VDV301-2_GC_V2.4"], 31),
            ]
        )
        require(v24_table, "Tabelle 3", "coachnumber", "deviceclass", "deviceID")
        v24_history = page_text(pdfs["VDV301-2_GC_V2.4"], 75).lower()
        require(v24_history, "fehlende einträge", "tabelle 3", "missing entries", "table 3 added")

        # Definition provenance for DISC-002 from the authoritative RFC Editor.
        rfc2927 = fetch(RFC_URLS["2927"]).decode("utf-8", errors="replace")
        rfc3927 = fetch(RFC_URLS["3927"]).decode("utf-8", errors="replace")
        require(rfc2927, "MIME Directory Profile for LDAP Schema")
        require(rfc3927, "Dynamic Configuration of IPv4 Link-Local Addresses", "169.254/16")

    print("PASSED: EV-126 DISC-001..003 exact VDV source and RFC provenance revalidation")
    print("XSD_LANE: not applicable; no XSD contract selected or modified")


if __name__ == "__main__":
    main()
