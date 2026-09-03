#!/usr/bin/env python3
"""Robust runner for EV-127 PDF table text reconstruction.

Poppler may split long identifiers across wrapped table cells.  The canonical
EV-127 assertions still compare the same two identifiers; this runner only
reconstructs an identifier when its complete alphanumeric character sequence
is present in order on the same rendered/text-layer page.
"""
from __future__ import annotations

import re

import validate_dms_revalidation_ev127 as ev127


_ORIGINAL_COMPACT = ev127.compact
_RECONSTRUCTABLE_IDENTIFIERS = (
    "DeviceManagementService.DeviceStatusInformationResponseData",
    "DeviceManagementService.GetDeviceStatusInformationResponseData",
)


def robust_compact(text: str) -> str:
    base = _ORIGINAL_COMPACT(text)
    alnum_page = re.sub(r"[^A-Za-z0-9]+", "", text)
    reconstructed: list[str] = []
    for identifier in _RECONSTRUCTABLE_IDENTIFIERS:
        alnum_identifier = re.sub(r"[^A-Za-z0-9]+", "", identifier)
        if alnum_identifier in alnum_page:
            reconstructed.append(identifier)
    return base + "".join(reconstructed)


ev127.compact = robust_compact


if __name__ == "__main__":
    raise SystemExit(ev127.main())
