#!/usr/bin/env python3
"""Layout-robust runner for EV-135 without altering the underlying evidence checks."""
from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_common_v10_revalidation_ev135 as ev135  # noqa: E402


def canon(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.replace("\u00ad", "").lower())


def pages_any(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    wanted = [canon(n) for n in needles]
    return [p for p, text in pages.items() if any(n in canon(text) for n in wanted)]


def pages_all(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    wanted = [canon(n) for n in needles]
    return [p for p, text in pages.items() if all(n in canon(text) for n in wanted)]


ev135.pages_any = pages_any
ev135.pages_all = pages_all

if __name__ == "__main__":
    raise SystemExit(ev135.main())
