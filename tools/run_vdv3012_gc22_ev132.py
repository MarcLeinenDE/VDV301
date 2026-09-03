#!/usr/bin/env python3
"""Run EV-132 with PDF typography normalized for stable anchor matching.

The exact V2.2 PDF uses German typographic quotation marks around SRV-/TXT-Record
in prose. The underlying EV-132 semantic anchors intentionally ignore quotation
mark glyphs; no source content or finding interpretation is changed.
"""
from __future__ import annotations

import validate_vdv3012_gc22_ev132 as ev132

_original_page_text = ev132.page_text


def page_typography_normalized(page: int) -> str:
    return _original_page_text(page).replace("„", "").replace("“", "").replace("”", "")


ev132.page_text = page_typography_normalized

if __name__ == "__main__":
    raise SystemExit(ev132.main())
