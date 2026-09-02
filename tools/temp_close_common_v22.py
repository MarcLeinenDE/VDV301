#!/usr/bin/env python3
"""Temporary bootstrap for the COMMON V2.2 closure script chunks."""
from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parts = sorted((ROOT / ".github/tmp").glob("common_v22_closure_*.b64"))
if len(parts) != 7:
    raise RuntimeError(f"expected 7 closure chunks, found {len(parts)}")
payload = "".join(p.read_text(encoding="ascii") for p in parts)
source = base64.b64decode(payload, validate=True).decode("utf-8")
exec(compile(source, __file__, "exec"), globals(), globals())
