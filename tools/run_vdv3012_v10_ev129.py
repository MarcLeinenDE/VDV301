#!/usr/bin/env python3
"""Run EV-129 with extraction-only whitespace normalization.

RFC Editor plain-text files may wrap normative sentences across physical lines.
Poppler can likewise split the literal `IBIS-IP.*` token at a table line break as
`IBIS- IP.*`. These are extraction/layout artifacts only; this runner normalizes
them before the EV-129 anchor checks without changing any source or claim.
"""
from __future__ import annotations

import validate_vdv3012_v10_ev129 as ev129

_original_fetch_text = ev129.fetch_text
_original_page_text = ev129.page_text


def fetch_normalized(url: str) -> str:
    return ev129.normalize(_original_fetch_text(url))


def page_normalized(page: int) -> str:
    text = _original_page_text(page)
    return text.replace("IBIS- IP.", "IBIS-IP.").replace("IBIS- IP", "IBIS-IP")


ev129.fetch_text = fetch_normalized
ev129.page_text = page_normalized

if __name__ == "__main__":
    raise SystemExit(ev129.main())
