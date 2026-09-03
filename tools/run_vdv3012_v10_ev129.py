#!/usr/bin/env python3
"""Run EV-129 with RFC text whitespace normalized before authority-anchor checks.

RFC Editor plain-text files may wrap normative sentences across physical lines.
The underlying EV-129 validator already normalizes VDV PDF page text; this runner
applies the same whitespace normalization to fetched RFC primary-source text so
line wrapping cannot create a false gate failure.
"""
from __future__ import annotations

import validate_vdv3012_v10_ev129 as ev129

_original_fetch_text = ev129.fetch_text


def fetch_normalized(url: str) -> str:
    return ev129.normalize(_original_fetch_text(url))


ev129.fetch_text = fetch_normalized

if __name__ == "__main__":
    raise SystemExit(ev129.main())
