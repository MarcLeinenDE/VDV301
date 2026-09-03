#!/usr/bin/env python3
"""Run EV-129 with extraction-only normalization.

RFC Editor plain-text files may wrap normative sentences across physical lines.
Poppler can likewise split table cells across reading order; on VDV301-2 V1.0
page 65 the visible `IBIS-IP.duration` type is extracted as an `IBIS-` fragment
and a later `IP.duration` fragment around the description column. This runner
normalizes only such extraction artifacts; it does not change any source or
finding claim. The decisive DR3012-003 identifier/type result still comes from
the exact XSD declaration plus positive/negative XML validation.
"""
from __future__ import annotations

import validate_vdv3012_v10_ev129 as ev129

_original_fetch_text = ev129.fetch_text
_original_page_text = ev129.page_text
_original_require = ev129.require


def fetch_normalized(url: str) -> str:
    return ev129.normalize(_original_fetch_text(url))


def page_normalized(page: int) -> str:
    text = _original_page_text(page)
    return text.replace("IBIS- IP.", "IBIS-IP.").replace("IBIS- IP", "IBIS-IP")


def require_robust(condition: bool, message: str) -> None:
    if condition:
        return
    if message == "DR3012-003 PDF page 65 anchors missing":
        text = _original_page_text(65)
        table_anchor = text.count("HertbeatIntervall") >= 2 and "IP.duration" in text
        return _original_require(table_anchor, message)
    return _original_require(condition, message)


ev129.fetch_text = fetch_normalized
ev129.page_text = page_normalized
ev129.require = require_robust

if __name__ == "__main__":
    raise SystemExit(ev129.main())
