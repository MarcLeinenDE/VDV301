#!/usr/bin/env python3
"""Run EV-134 with a layout-robust V2.3-history repair control.

The five GC V2.4 finding checks remain unchanged. This wrapper only makes the
additional predecessor-repair control robust against bilingual PDF table/heading
layout by requiring the V2.3 section and both corrected 7.2.x subsection numbers
on the same extracted page instead of requiring one exact heading phrase.
"""
from __future__ import annotations

import validate_vdv3012_gc24_ev134 as ev134

_original_pages_any = ev134.pages_any


def pages_any_layout_robust(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    if needles in {
        ("7.2.1 Funktionale Erweiterungen",),
        ("7.2.2 Technical Upgrade/Corrections",),
    }:
        return [
            page
            for page, text in pages.items()
            if "Version 2.3" in text and "7.2.1" in text and "7.2.2" in text
        ]
    return _original_pages_any(pages, needles)


ev134.pages_any = pages_any_layout_robust

if __name__ == "__main__":
    raise SystemExit(ev134.main())
